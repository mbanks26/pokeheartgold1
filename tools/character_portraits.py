#!/usr/bin/env python3
"""Convert the existing custom front art into intro and Trainer Card resources."""
from pathlib import Path
from PIL import Image
import json,struct
from character_graphics import ROOT,original,members,patch_members,palette_bytes

def portrait(name,w,h,height):
    im=Image.open(ROOT/f'characters/{name}/battle-front.png').crop((0,0,80,80))
    im=im.crop(im.getbbox());scale=min((w-4)/im.width,height/im.height)
    resized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
    out=Image.new('P',(w,h));out.putpalette(im.getpalette())
    out.paste(resized,((w-resized.width)//2,h-resized.height-3))
    out.info['transparency']=0
    return out

def tiles(im,bpp=4):
    out=bytearray()
    for y in range(0,im.height,8):
        for x in range(0,im.width,8):
            p=list(im.crop((x,y,x+8,y+8)).getdata())
            out.extend(p if bpp==8 else [p[i]|p[i+1]<<4 for i in range(0,64,2)])
    return bytes(out)

report={'intro':[],'card':[],'art_source':'Existing custom front battle art adapted to native portrait sizes; four intro display slots share the same new pose.'}
for name,first,pal_id in [('male',12,16),('female',17,21)]:
    im=portrait(name,64,128,112)
    im.save(ROOT/f'characters/{name}/intro.png',bits=4)
    data=tiles(im)
    for i in range(first,first+4):
        path=f'files/demo/intro/intro/intro_{i:08}.NCGR';b=bytearray(original(path))
        assert len(data)==4096;b[48:4144]=data;(ROOT/path).write_bytes(b);report['intro'].append(path)
    path=f'files/demo/intro/intro/intro_{pal_id:08}.NCLR';b=bytearray(original(path));b[40:72]=palette_bytes(im);(ROOT/path).write_bytes(b)

path='files/a/0/4/9';b=original(path);m=members(b);changes={}
atlas=bytearray(8192)
for name,screen_id,tile_start,bank in [('female',55,1,64),('male',54,61,80)]:
    im=portrait(name,48,80,68);im.save(ROOT/f'characters/{name}/trainer-card.png',bits=4)
    p=list(im.getdata());mapped=Image.new('P',im.size);mapped.putdata([v+bank if v else 0 for v in p])
    raw=tiles(mapped,8);assert len(raw)==3840
    atlas[tile_start*64:tile_start*64+3840]=raw
    screen=bytearray(m[screen_id]);screen[36:]=b'\0'*(len(screen)-36)
    for j in range(60):struct.pack_into('<H',screen,36+2*((5+j//6)*32+23+j%6),tile_start+j)
    changes[screen_id]=bytes(screen)
    pal=palette_bytes(im)
    for i,old in enumerate(m):
        if old[:4]==b'RLCN' and old[168:232]==m[0][168:232]:
            new=bytearray(changes.get(i,old));new[40+2*bank:40+2*bank+32]=pal;changes[i]=bytes(new)
native=bytearray(m[44]);native[48:8240]=atlas;changes[44]=bytes(native)
updated=patch_members(b,changes);(ROOT/path).write_bytes(updated)
assert all(a==z for i,(a,z) in enumerate(zip(m,members(updated))) if i not in changes)
report['card']={'archive':path,'members':sorted(changes),'file_size_preserved':True,'unrelated_members_preserved':True}
(ROOT/'characters/portrait-conversion.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
