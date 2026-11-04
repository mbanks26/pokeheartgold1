"""Replay Sabrina's original Gym puzzle, battle victory and defeat recovery."""
from pathlib import Path
import argparse,json,gzip,struct,binascii,re
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
from inspect_story_pokemon import crypt,OFFSETS,decode_mon
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for name in ['core','rom','symbols','output']:p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
layout=json.loads((ROOT/'tests/fixtures/companion/save-layout.json').read_text());commands=json.loads((ROOT/'tests/fixtures/release/gym-inputs.json').read_text())['commands'];reports=[]
for mode in ['victory','defeat']:
    folder=a.output/mode;rom=isolated_rom(a.rom,folder);raw=bytearray(gzip.decompress((ROOT/'tests/fixtures/release/saffron-pre-gym.sav.gz').read_bytes()))
    # Isolate the leader/puzzle from random line-of-sight interruptions. These
    # prerequisites are authored, not claimed as four newly played victories.
    for base in [0,0x40000]:
        if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
        start=base+layout['4']['offset'];flags=start+0x2e0
        constants=(ROOT/'include/constants/trainers.h').read_text()
        for name in ['MEDIUM_DARCY','PSYCHIC_M_JARED','MEDIUM_REBECCA','PSYCHIC_M_FRANKLIN']:
            trainer=int(re.search(r'^#define TRAINER_'+name+r'\s+(\d+)',constants,re.M).group(1))
            flag=0x550+trainer;raw[flags+flag//8]|=1<<(flag%8)
        size=layout['4']['size'];struct.pack_into('<H',raw,start+size-4,binascii.crc_hqx(raw[start:start+size-4],65535))
        struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
    if mode=='defeat':
        for base in [0,0x40000]:
            if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
            party=base+layout['2']['offset'];mon=party+8;pid=struct.unpack_from('<I',raw,mon)[0];checksum=struct.unpack_from('<H',raw,mon+6)[0]
            box=crypt(raw[mon+8:mon+136],checksum);off=OFFSETS[(pid&0x3e000)>>13][1];box[off+8:off+12]=bytes(4)
            checksum=sum(struct.unpack('<64H',box))&65535;struct.pack_into('<H',raw,mon+6,checksum);raw[mon+8:mon+136]=crypt(box,checksum)
            stats=crypt(raw[mon+136:mon+236],pid);struct.pack_into('<H',stats,6,1);raw[mon+136:mon+236]=crypt(stats,pid)
            size=layout['2']['size'];struct.pack_into('<H',raw,party+size-4,binascii.crc_hqx(raw[party:party+size-4],65535));struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
    fixture=folder/'input.sav';fixture.write_bytes(raw);wrap_save(fixture,rom.with_suffix('.dsv'))
    s=EmulatorSession(a.core,rom,a.symbols,folder,mode)
    for step,command in enumerate(commands if mode=='victory' else commands[:69],1):
        command=dict(command)
        if step==44:command.update(dump='gym-battle.bin',inspect=True)
        result=s.send(command)
        if step==40:
            g=result['game'];assert g['task']=='0x0' and next(o['xyz'] for o in g['objects'] if o['id']==255)==[15,4,14],'Native Gym puzzle trace diverged before leader interaction'
    if mode=='defeat':
        s.send({'talk':70});s.send({'frames':600});
        for button in ['DOWN','LEFT','UP','RIGHT']:s.send({'frames':32,'buttons':[button]})
    g=s.send({'frames':180,'inspect':True,'shot':'final-'+mode+'.png','dump':'final-'+mode+'.bin'})['game']
    assert g['joined'] and g['task']=='0x0' and not g['battle_paired']
    assert sum(o['id']==252 for o in g['objects'])==1 and sum(o['id']==253 for o in g['objects'])==1
    sd=int(g['save_address'],16)
    def block(i):return sd+16+int.from_bytes(bytes.fromhex(s.send({'read':[hex(sd+0x23014+i*16+8),4]})['read']),'little')
    profile=bytes.fromhex(s.send({'read':[hex(block(1)+4),32]})['read']);marsh=bool(profile[31]&0x20)
    flags=int(g['flag_address'],16);trainerflag=bool(int(s.send({'read':[hex(flags+0x652//8),1]})['read'],16)&(1<<(0x652%8)))
    bag=bytes.fromhex(s.send({'read':[hex(block(3)+860),404]})['read']);tm=sum(q for item,q in struct.iter_unpack('<HH',bag) if item==375)
    # The original Gym script tracks completion by badge and sets its four
    # subordinate trainer flags. Direct TrainerBattle does not set the leader's
    # common-NPC trainer flag; requiring it would be a false regression.
    assert marsh==(mode=='victory') and tm==(1 if mode=='victory' else 0)
    if mode=='defeat':assert not trainerflag
    battle=(folder/'gym-battle.bin').read_bytes();marker=struct.pack('<4I',0,258,0,0);pos=0;parties=[]
    while True:
        pos=battle.find(marker,pos)
        if pos<0:break
        start=pos-0x18;pos+=1
        if start<0 or struct.unpack_from('<I',battle,start)[0]!=1:continue
        ptr=struct.unpack_from('<I',battle,start+8)[0]-0x2000000
        if not 0<=ptr<len(battle)-8:continue
        count=struct.unpack_from('<I',battle,ptr+4)[0]
        if count!=3:continue
        team=[decode_mon(battle[ptr+8+i*236:ptr+8+(i+1)*236]) for i in range(count)]
        assert [(m['species'],m['level']) for m in team]==[(196,53),(122,53),(65,55)];parties.append(team)
    assert parties,'Native original Sabrina Single team not found'
    s.save();s.close()
    report={'mode':mode,'Marsh_Badge':marsh,'defeated_trainer_flag':trainerflag,'TM48_quantity':tm,'joined':True,'follower_counts':{'252':1,'253':1},'return_map':g['map'],
        'battle_type':'Native Trainer Single 0x1','enemy_trainer':258,'enemy_team':parties[0],
        'scope':'Native Gym entry, teleporter puzzle, battle result and recovery. High-level party/location and four defeated subtrainers are authored prerequisites; defeat sets only HP 1 and PP 0 before boot; no runtime writes.'}
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report);print(json.dumps(report),flush=True)
(a.output/'results.json').write_text(json.dumps(reports,indent=2)+'\n')
