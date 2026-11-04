"""Test female Goldenrod entry without added sister/romance events.

Requires a real female post-starter battery save. Location fixtures are authored;
NPC creation, conversations and native saving are exercised through the engine.
"""
from pathlib import Path
import argparse,json,struct,binascii
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for name in ['core','rom','symbols','output','source_save']:p.add_argument('--'+name.replace('_','-'),type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);layout=json.loads((ROOT/'tests/fixtures/companion/save-layout.json').read_text())
def prepare(source,folder,mapid,x,z,height,camera,direction,keep_npcs):
    raw=bytearray(source.read_bytes()[:524288]);sectors=[base for base in [0,0x40000] if struct.unpack_from('<I',raw,base+0xf620)[0]==0x20060623];latest=max(sectors,key=lambda b:struct.unpack_from('<I',raw,b+0xf618)[0])
    assert raw[latest+layout['1']['offset']+4+24]==1 and struct.unpack_from('<I',raw,latest+layout['2']['offset']+4)[0]==1
    # Preserve native sector identity/counters and the matching boxed-data
    # generation. A first-save file must not acquire a fabricated backup block.
    for base in sectors:
        if struct.unpack_from('<I',raw,base+layout['2']['offset']+4)[0]!=1:continue
        local=base+layout['5']['offset'];struct.pack_into('<5i',raw,local,mapid,-1,x,z,direction);raw[local+106]=camera;struct.pack_into('<i',raw,local+112,0)
        objs=base+layout['10']['offset'];actors=[]
        for i in range(64):
            record=bytearray(raw[objs+i*80:objs+(i+1)*80])
            if not struct.unpack_from('<I',record)[0]&1:continue
            if record[8] in [255,253]:
                xx=x-(record[8]==253 and direction==3);zz=z-(record[8]==253 and direction==1);record[12:15]=bytes([direction]*3);struct.pack_into('<6h',record,32,xx,height,zz,xx,height,zz);struct.pack_into('<i',record,44,height*32768);actors.append(record)
            elif keep_npcs:actors.append(record)
        assert sum(record[8] in [255,253] for record in actors)==2
        raw[objs:objs+5120]=b''.join(actors)+bytes(5120-80*len(actors))
        for block in [5,10]:
            start=base+layout[str(block)]['offset'];size=layout[str(block)]['size'];struct.pack_into('<H',raw,start+size-4,binascii.crc_hqx(raw[start:start+size-4],65535))
        struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
    rom=isolated_rom(a.rom,folder);fixture=folder/'input.sav';fixture.write_bytes(raw);wrap_save(fixture,rom.with_suffix('.dsv'));return rom

folder=a.output/'native-entry';rom=prepare(a.source_save,folder,185,8,18,0,4,1,False)
s=EmulatorSession(a.core,rom,a.symbols,folder,'entry');s.boot_continue();s.send({'frames':48,'buttons':['DOWN']});g=s.send({'frames':600,'inspect':True,'shot':'female-goldenrod-entry.png'})['game']
assert g['map']==76 and g['gender']==1 and not g['joined']
assert not any(o['id'] in [240,252] for o in g['objects']) and any(o['id']==241 for o in g['objects'])
s.save();s.close()
folder=a.output/'breeder';rom=prepare(rom.with_suffix('.dsv'),folder,76,355,370,2,0,3,True)
s=EmulatorSession(a.core,rom,a.symbols,folder,'breeder');g=s.boot_continue()['game']
assert g['gender']==1 and not g['joined'] and next(o['sprite'] for o in g['objects'] if o['id']==255)==97
def flag(n):return bool(int(s.send({'read':[hex(int(g['flag_address'],16)+n//8),1]})['read'],16)&(1<<(n%8)))
assert flag(0xB5D) and not flag(0xB51);bill_before=flag(0x95)
s.send({'frames':8,'buttons':['A']});s.send({'frames':180,'shot':'female-neutral-page1.png'});s.send({'frames':8,'buttons':['A']});s.send({'frames':180,'shot':'female-neutral-page2.png'});s.send({'talk':30})
g=s.send({'frames':180,'inspect':True})['game'];assert g['task']=='0x0' and not flag(0xB51) and flag(0x95)==bill_before
assert not any(o['id'] in [240,252] for o in g['objects'])
s.save();s.close();s=EmulatorSession(a.core,rom,a.symbols,folder,'female-cold');g=s.boot_continue()['game'];assert g['gender']==1 and flag(0xB5D) and not flag(0xB51) and not g['joined'];s.send({'frames':1,'shot':'female-cold.png'});s.close()
report={'native_city_entry':'PASS','custom_female_avatar_sprite':97,'added_sister_and_Sabrina_objects':0,'breeder_response':'Neutral native-route dialogue; screenshot reviewed separately',
    'sister_Eevee_flag_not_awarded':True,'player_Bill_gift_flag_unchanged':True,'native_save_and_cold_Continue':'PASS',
    'scope':'Fresh female save relocated to Goldenrod PC, native door entry creates NPCs; city snapshot relocated beside breeder. Does not prove a full female campaign.'}
(a.output/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
