"""Native Sabrina Dojo rematch with an explicitly authored phone appointment."""
from pathlib import Path
import argparse,json,struct,binascii
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
from inspect_story_pokemon import decode_mon
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for name in ['core','rom','symbols','output','source_save']:p.add_argument('--'+name.replace('_','-'),type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);rom=isolated_rom(a.rom,a.output)
layout=json.loads((ROOT/'tests/fixtures/companion/save-layout.json').read_text());raw=bytearray(a.source_save.read_bytes()[:524288])
for base in [0,0x40000]:
    if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
    local=base+layout['5']['offset'];struct.pack_into('<5i',raw,local,59,-1,1321,205,0);struct.pack_into('<i',raw,local+112,0)
    objects=base+layout['10']['offset']
    for i in range(64):
        at=objects+i*80
        if not struct.unpack_from('<I',raw,at)[0]&1 or raw[at+8] not in [255,253]:continue
        z=205+(raw[at+8]==253);raw[at+12:at+15]=bytes(3);struct.pack_into('<6h',raw,at+32,1321,4,z,1321,4,z);struct.pack_into('<i',raw,at+44,4*32768)
    gear=base+layout['34']['offset'];raw[gear+0x4b8+35*4]|=1
    for block in [5,10,34]:
        start=base+layout[str(block)]['offset'];size=layout[str(block)]['size'];struct.pack_into('<H',raw,start+size-4,binascii.crc_hqx(raw[start:start+size-4],65535))
    struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
fixture=a.output/'input.sav';fixture.write_bytes(raw);wrap_save(fixture,rom.with_suffix('.dsv'))
s=EmulatorSession(a.core,rom,a.symbols,a.output,'rematch');s.boot_continue();s.send({'frames':32,'buttons':['UP']});g=s.send({'frames':600,'inspect':True,'shot':'dojo-entry.png'})['game']
assert g['map']==398 and any(o['sprite']==369 for o in g['objects']) and sum(o['id']==252 for o in g['objects'])==0
for button,frames in [('UP',96),('RIGHT',48),('UP',32)]:s.send({'frames':frames,'buttons':[button]});s.send({'frames':90})
g=s.send({'frames':180,'inspect':True,'shot':'before-rematch.png'})['game'];player=next(o['xyz'] for o in g['objects'] if o['id']==255);assert player[0]==10 and player[2]==6
s.send({'frames':8,'buttons':['A']});s.send({'frames':180});s.send({'talk':6});s.send({'frames':120,'shot':'rematch-entrance.png'});g=s.send({'frames':900,'inspect':True,'shot':'rematch-battle.png','dump':'rematch-battle.bin'})['game'];assert not g['battle_paired']
sd=int(g['save_address'],16)
def block(i):return sd+16+int.from_bytes(bytes.fromhex(s.send({'read':[hex(sd+0x23014+i*16+8),4]})['read']),'little')
def appointment():return bool(int(s.send({'read':[hex(block(34)+0x4b8+35*4),1]})['read'],16)&1)
for turn in range(60):
    if not appointment():break
    s.send({'frames':8,'buttons':['A']});s.send({'frames':360})
    if turn%10==0:print(json.dumps({'turn_input':turn}),flush=True)
assert not appointment(),'Native rematch did not complete within the bounded inputs'
s.send({'talk':35});
for button in ['DOWN','LEFT','UP','RIGHT']:s.send({'frames':32,'buttons':[button]})
g=s.send({'frames':180,'inspect':True,'shot':'rematch-restored.png','expect':{'joined':True,'counts':{'252':1,'253':1}}})['game'];sd=int(g['save_address'],16)
flag=int(g['flag_address'],16)+0x2bf//8;assert int(s.send({'read':[hex(flag),1]})['read'],16)&(1<<(0x2bf%8))
native=(a.output/'rematch-battle.bin').read_bytes();marker=struct.pack('<4I',0,725,0,0);pos=0;teams=[]
while True:
    pos=native.find(marker,pos)
    if pos<0:break
    start=pos-0x18;pos+=1
    if start<0 or struct.unpack_from('<I',native,start)[0]!=1:continue
    ptr=struct.unpack_from('<I',native,start+8)[0]-0x2000000
    if not 0<=ptr<len(native)-8:continue
    count=struct.unpack_from('<I',native,ptr+4)[0]
    if count==6:teams.append([decode_mon(native[ptr+8+i*236:ptr+8+(i+1)*236]) for i in range(count)])
assert teams,'Native original rematch trainer 725 / six-member roster not found'
s.save();s.close()
s=EmulatorSession(a.core,rom,a.symbols,a.output,'rematch-cold');g=s.boot_continue()['game'];sd=int(g['save_address'],16);assert g['joined'] and not appointment()
s.send({'frames':64,'buttons':['RIGHT']});s.send({'frames':180,'inspect':True,'shot':'rematch-cold.png','expect':{'joined':True,'counts':{'252':1,'253':1}}});s.close()
report={'enemy_trainer':725,'battle_type':'Native Trainer Single 0x1','paired_player_art':False,'enemy_team':teams[0],
    'native_appointment_cleared_after_victory':True,'canonical_NPC_hidden_after_victory':True,'both_followers_restored':True,'native_save_and_cold_Continue':'PASS',
    'scope':'Location and phone appointment authored from native Gym-victory battery save; native Dojo entry, rematch, victory and persistence. Natural phone-number acquisition and weekly scheduling are not tested.'}
(a.output/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
