"""Read-only checks of custom texture pixels and the actual packaged ROM assets."""
from pathlib import Path
import argparse,hashlib,json,struct
from PIL import Image
from character_graphics import ROOT,rom_files,members,dictionary_entries,u16,u32,packed4,palette_bytes,original

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rom',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
rom=a.rom.read_bytes();filesystem=rom_files(rom)
for name,(start,end) in filesystem.items():assert 0<=start<=end<=len(rom),name
def asset(name):
    start,end=filesystem[name];return rom[start:end]

textures=members(asset('a/0/8/1'));checks=[]
sources={69:ROOT/'characters/male/overworld.png',70:ROOT/'characters/female/overworld.png',163:ROOT/'characters/sabrina/overworld.png'}
sources.update({int(f.stem):f for f in (ROOT/'characters/actions').glob('*.png')})
for index,png in sorted(sources.items()):
    path=f'files/data/mmodel/mmodel/mmodel_{index:08}.NSBTX';raw=(ROOT/path).read_bytes()
    assert textures[index]==raw,'ROM texture differs from checked source '+path
    base=u32(raw,16);sheet=Image.open(png);assert sheet.mode=='P' and sheet.info.get('transparency')==0
    ranges=[];entries=dictionary_entries(raw,base+u16(raw,base+14));effective={};aliases={}
    for label,entry in entries:
        params=u16(raw,entry+2);assert (params>>10)&7==3 and params&0x2000
        assert 8<<((params>>4)&7)==32 and 8<<((params>>7)&7)==32
        frame=int(label.rsplit('.',1)[1])-1
        if index in (69,70,163):frame%=16
        image=sheet.crop((frame%4*32,frame//4*32,frame%4*32+32,frame//4*32+32))
        start=base+u32(raw,base+20)+u16(raw,entry)*8
        # Native idle frames can share one data address. Preserve that layout:
        # the recovered converter writes in dictionary order, so the last
        # source frame for an alias address is the effective packaged image.
        effective[start]=packed4(image);aliases.setdefault(start,[]).append(label)
        ranges.append((start,start+512))
    for start,payload in effective.items():assert raw[start:start+512]==payload,(index,aliases[start])
    pals=dictionary_entries(raw,base+u32(raw,base+52));assert len(pals)==1
    start=base+u32(raw,base+56)+u16(raw,pals[0][1])*8
    assert raw[start:start+32]==palette_bytes(sheet);ranges.append((start,start+32))
    before=bytearray(original(path));after=bytearray(raw)
    for start,end in ranges:before[start:end]=after[start:end]=bytes(end-start)
    assert before==after,'Native texture metadata altered '+path
    checks.append({'index':index,'frames':len(entries),'effective_pixel_palette_and_metadata':'PASS','compiled_ROM_matches':True,
                   'native_shared_frames':[v for v in aliases.values() if len(v)>1],
                   'alias_policy':'Recovered dictionary-order last write, native addresses preserved'})

archives={}
for name in ['a/0/0/6','a/0/4/9','a/0/5/8']:
    expected=(ROOT/'files'/name).read_bytes();assert asset(name)==expected
    archives[name]={'members':len(members(expected)),'sha256':hashlib.sha256(expected).hexdigest(),'compiled_ROM_matches':True}
intro=members(asset('a/1/2/0'))
for file in json.loads((ROOT/'characters/portrait-conversion.json').read_text())['intro']:
    index=int(Path(file).stem.rsplit('_',1)[1]);assert intro[index]==(ROOT/file).read_bytes(),file

narcs=0;total_members=0
for name in filesystem:
    data=asset(name)
    if data[:4]!=b'NARC':continue
    assert u32(data,8)==len(data),name
    count=u16(data,24);parts=members(data);assert len(parts)==count
    narcs+=1;total_members+=count

bag=[]
for index in (55,74):
    path=f'files/graphic/bag/bag_graphics/bag_graphics_{index:05}.NSBMD'
    raw=(ROOT/path).read_bytes();assert raw==original(path)
    bag.append({'member':index,'status':'Original 3D model; custom 2D graphics do not replace it','sha256':hashlib.sha256(raw).hexdigest()})
report={'ROM_sha1':hashlib.sha1(rom).hexdigest(),'ROM_bytes':len(rom),'filesystem_files':len(filesystem),
        'NARC_archives_checked':narcs,'NARC_members_checked':total_members,'custom_overworld_textures':checks,
        'battle_and_card_archives':archives,'intro_custom_slots':8,'stock_Bag_3D_models':bag,
        'scope':'Static actual-ROM and source pixel checks; does not prove action animation alignment or gameplay'}
a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['custom_overworld_textures','battle_and_card_archives','stock_Bag_3D_models']}))
