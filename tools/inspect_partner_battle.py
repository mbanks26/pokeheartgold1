"""Inspect a native BattleSetup captured from our isolated emulator test RAM."""
from pathlib import Path
import argparse,json,struct,gzip
from inspect_story_pokemon import decode_mon

def inspect(raw,enemy,ally,enemy2):
    marker=struct.pack('<4I',0,enemy,ally,enemy2)
    u=lambda offset:struct.unpack_from('<I',raw,offset)[0]
    found=[];start=0
    while True:
        pos=raw.find(marker,start)
        if pos<0:break
        start=pos+1;setup=pos-0x18
        if setup<0 or u(setup)!=0x4b:continue
        parties=[]
        for i in range(4):
            ptr=u(setup+4+i*4)-0x2000000
            assert 0<=ptr<len(raw)-8 and 1<=u(ptr+4)<=6
            parties.append([decode_mon(raw[ptr+8+j*236:ptr+8+(j+1)*236])for j in range(u(ptr+4))])
        found.append({'setup_address':hex(setup+0x2000000),'battle_type':'0x4b TRAINER|DOUBLES|MULTI|AI','trainer_ids':[0,enemy,ally,enemy2],'parties_player_enemy_ally_enemy2':parties})
    assert found,'No matching native AI Multi BattleSetup found'
    return found

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('ram',type=Path);p.add_argument('--enemy',type=int,required=True);p.add_argument('--ally',type=int,required=True);p.add_argument('--enemy2',type=int,required=True);p.add_argument('--output',type=Path);a=p.parse_args()
    raw=a.ram.read_bytes();result=inspect(gzip.decompress(raw) if a.ram.suffix=='.gz' else raw,a.enemy,a.ally,a.enemy2);out=json.dumps(result,indent=2)+'\n'
    if a.output:a.output.write_text(out)
    print(out)
