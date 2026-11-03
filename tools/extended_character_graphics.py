#!/usr/bin/env python3
"""Apply numbered 32x32 indexed action textures, preserving native BTX metadata."""
import json,sys
from pathlib import Path
from PIL import Image
from character_graphics import ROOT,original,u16,u32,dictionary_entries,packed4,palette_bytes,digest

def apply(i):
    path=f'files/data/mmodel/mmodel/mmodel_{i:08}.NSBTX'
    b=original(path);out=bytearray(b);base=u32(b,16)
    sheet=Image.open(ROOT/f'characters/actions/{i}.png')
    entries=dictionary_entries(b,base+u16(b,base+14))
    assert sheet.width==128 and sheet.height==32*((len(entries)+3)//4)
    assert sheet.mode=='P' and sheet.info.get('transparency')==0
    ranges=[]
    for label,e in entries:
        params=u16(b,e+2);assert (params>>10)&7==3 and params&0x2000
        assert 8<<((params>>4)&7)==32 and 8<<((params>>7)&7)==32
        j=int(label.rsplit('.',1)[1])-1
        frame=sheet.crop((j%4*32,j//4*32,j%4*32+32,j//4*32+32))
        p=base+u32(b,base+20)+u16(b,e)*8
        payload=packed4(frame);assert len(payload)==512
        out[p:p+512]=payload;ranges.append((p,p+512))
        assert list(frame.getdata())==[v for x in payload for v in (x&15,x>>4)]
    pals=dictionary_entries(b,base+u32(b,base+52));assert len(pals)==1
    p=base+u32(b,base+56)+u16(b,pals[0][1])*8
    out[p:p+32]=palette_bytes(sheet);ranges.append((p,p+32))
    before=bytearray(b);after=bytearray(out)
    for a,z in ranges:before[a:z]=after[a:z]=b'\0'*(z-a)
    assert before==after and len(out)==len(b)
    (ROOT/path).write_bytes(out)
    return {'texture_id':i,'frames':len(entries),'metadata_preserved':True,'pixel_roundtrip':True,'sha256':digest(out)}

if __name__=='__main__':
    report=[apply(int(i)) for i in sys.argv[1:]]
    print(json.dumps(report,indent=2))
