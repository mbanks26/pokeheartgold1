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

def make_patch(source,target):
    assert len(source)==len(target)
    assert hashlib.sha1(source).hexdigest()=='4fcded0e2713dc03929845de631d0932ea2b5a37'
    metadata=b'HeartGold character integration: Sabrina, male protagonist, female Lyra replacement; graphics only; gameplay testing pending.'
    patch=bytearray(b'BPS1')+number(len(source))+number(len(target))+number(len(metadata))+metadata
    runs=[]
    def run(kind,start,end):
        if runs and runs[-1][0]==kind and runs[-1][2]==start:
            runs[-1]=(kind,runs[-1][1],end)
        else:runs.append((kind,start,end))
    for off in range(0,len(source),4096):
        end=min(off+4096,len(source))
        if source[off:end]==target[off:end]:run(0,off,end);continue
        pos=off
        while pos<end:
            kind=int(source[pos]!=target[pos]);start=pos;pos+=1
            while pos<end and int(source[pos]!=target[pos])==kind:pos+=1
            run(kind,start,pos)
    for kind,start,end in runs:
        patch+=number(((end-start-1)<<2)|kind)
        if kind==1:patch+=target[start:end]
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
    out=bytearray()
    while len(out)<target_size:
        action=read_number();length=(action>>2)+1;kind=action&3
        if kind==0:out+=source[len(out):len(out)+length]
        elif kind==1:out+=patch[pos:pos+length];pos+=length
        else:raise ValueError('Unexpected patch action')
    assert len(out)==target_size and pos==len(patch)-12
    assert zlib.crc32(out)==struct.unpack_from('<I',patch,len(patch)-8)[0]
    return bytes(out)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('target',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();source=args.source.read_bytes();target=args.target.read_bytes()
    patch=make_patch(source,target);assert apply_patch(source,patch)==target
    args.output.write_bytes(patch)
    print(f'BPS patch roundtrip passed: {len(patch)} bytes; target SHA-1 {hashlib.sha1(target).hexdigest()}')
