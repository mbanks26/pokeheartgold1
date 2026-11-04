#!/usr/bin/env python3
"""Create and roundtrip-check a standard BPS patch for the validated ROM."""
import argparse
import hashlib
from pathlib import Path
import struct
import zlib

def number(value):
    out=bytearray()
    while True:
        digit=value&127;value>>=7
        if not value:
            out.append(digit|128);return out
        out.append(digit);value-=1

def narc_member_ranges(data):
    """Return validated relative ranges, or None for a nonstandard archive."""
    if len(data)<32 or data[:4]!=b'NARC' or data[16:20]!=b'BTAF':return None
    count=struct.unpack_from('<H',data,24)[0]
    btnf=16+struct.unpack_from('<I',data,20)[0]
    if btnf+8>len(data):return None
    gmif=btnf+struct.unpack_from('<I',data,btnf+4)[0]
    if gmif+8>len(data) or data[gmif:gmif+4]!=b'GMIF':return None
    payload=gmif+8;ranges=[]
    for i in range(count):
        if 36+8*i>btnf:return None
        start,end=struct.unpack_from('<II',data,28+8*i)
        if not 0<=start<=end<=len(data)-payload:return None
        ranges.append((payload+start,payload+end))
    return ranges

def make_patch(source,target,metadata=None):
    assert len(source)==len(target)
    assert hashlib.sha1(source).hexdigest()=='4fcded0e2713dc03929845de631d0932ea2b5a37'
    if metadata is None:
        metadata=b'HeartGold character integration: Sabrina, male protagonist, female Lyra replacement; graphics only; gameplay testing pending.'
    patch=bytearray(b'BPS1')+number(len(source))+number(len(target))+number(len(metadata))+metadata
    runs=[]
    def run(kind,start,end,src):
        if start==end:return
        if runs and runs[-1][0]==kind and runs[-1][2]==start and (kind==1 or runs[-1][3]+runs[-1][2]-runs[-1][1]==src):
            old=runs[-1];runs[-1]=(kind,old[1],end,old[3])
        else:runs.append((kind,start,end,src))
    def compare(start,end,src):
        if src is None:run(1,start,end,0);return
        delta=src-start
        same_kind=0 if delta==0 else 2
        for off in range(start,end,4096):
            stop=min(off+4096,end)
            if source[off+delta:stop+delta]==target[off:stop]:run(same_kind,off,stop,off+delta);continue
            pos=off
            while pos<stop:
                equal=source[pos+delta]==target[pos];begin=pos;pos+=1
                while pos<stop and (source[pos+delta]==target[pos])==equal:pos+=1
                run(same_kind if equal else 1,begin,pos,begin+delta)
    # Match files by their NDS FAT ID, so relocation never embeds unchanged
    # game assets as literals. Changed-size overlay files remain literal runs.
    sfat,slen=struct.unpack_from('<II',source,0x48)
    tfat,tlen=struct.unpack_from('<II',target,0x48)
    assert slen==tlen and slen%8==0
    spans=[]
    for i in range(tlen//8):
        sa,se=struct.unpack_from('<II',source,sfat+8*i)
        ta,te=struct.unpack_from('<II',target,tfat+8*i)
        if te<=ta:continue
        if se-sa==te-ta:
            spans.append((ta,te,sa));continue
        # A changed archive size need not embed every unchanged member. Match
        # native NARC members by index, preserving source validation while
        # avoiding literal copies of thousands of unchanged game resources.
        sm=narc_member_ranges(source[sa:se]);tm=narc_member_ranges(target[ta:te])
        if sm is None or tm is None:
            spans.append((ta,te,None));continue
        for member,(start,end) in enumerate(tm):
            src=None
            if member<len(sm) and sm[member][1]-sm[member][0]==end-start:src=sa+sm[member][0]
            if end>start:spans.append((ta+start,ta+end,src))
    pos=0
    for start,end,src in sorted(spans):
        assert pos<=start<=end<=len(target)
        compare(pos,start,pos);compare(start,end,src);pos=end
    compare(pos,len(target),pos)
    relative=0
    for kind,start,end,src in runs:
        patch+=number(((end-start-1)<<2)|kind)
        if kind==1:patch+=target[start:end]
        elif kind==2:
            offset=src-relative
            patch+=number((abs(offset)<<1)|int(offset<0))
            relative=src+end-start
    patch+=struct.pack('<II',zlib.crc32(source),zlib.crc32(target))
    patch+=struct.pack('<I',zlib.crc32(patch))
    return bytes(patch)

def apply_patch(source,patch):
    assert patch[:4]==b'BPS1'
    assert zlib.crc32(patch[:-4])==struct.unpack_from('<I',patch,len(patch)-4)[0]
    pos=4
    def read_number():
        nonlocal pos
        value=0;shift=1
        while True:
            digit=patch[pos];pos+=1;value+=(digit&127)*shift
            if digit&128:return value
            shift<<=7;value+=shift
    source_size=read_number();target_size=read_number();meta_size=read_number();pos+=meta_size
    assert len(source)==source_size
    assert zlib.crc32(source)==struct.unpack_from('<I',patch,len(patch)-12)[0]
    out=bytearray();relative=0
    while len(out)<target_size:
        action=read_number();length=(action>>2)+1;kind=action&3
        if kind==0:out+=source[len(out):len(out)+length]
        elif kind==1:out+=patch[pos:pos+length];pos+=length
        elif kind==2:
            offset=read_number();relative+=-(offset>>1) if offset&1 else offset>>1
            assert 0<=relative and relative+length<=len(source)
            out+=source[relative:relative+length];relative+=length
        else:raise ValueError('Unexpected patch action')
    assert len(out)==target_size and pos==len(patch)-12
    assert zlib.crc32(out)==struct.unpack_from('<I',patch,len(patch)-8)[0]
    return bytes(out)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('target',type=Path);parser.add_argument('output',type=Path)
    parser.add_argument('--metadata',help='UTF-8 release description embedded in the BPS header')
    args=parser.parse_args();source=args.source.read_bytes();target=args.target.read_bytes()
    meta=args.metadata.encode('utf-8') if args.metadata is not None else (b'HeartGold custom graphics and experimental Sabrina plus Pokemon walking companion; emulator gameplay testing required.' if 'companion' in args.output.name else None)
    patch=make_patch(source,target,meta);assert apply_patch(source,patch)==target
    with args.output.open('xb') as handle:handle.write(patch)
    print(f'BPS patch roundtrip passed: {len(patch)} bytes; target SHA-1 {hashlib.sha1(target).hexdigest()}')
