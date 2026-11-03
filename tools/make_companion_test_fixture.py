"""Make an isolated late-game test fixture from our own starter save.

Never edits the source save or ROM; these are deliberately authored test states,
not evidence of a normal complete playthrough. Coordinates/party/items are setup.
"""
from pathlib import Path
import argparse,struct,json,binascii,re,hashlib
p=argparse.ArgumentParser();p.add_argument('base',type=Path);p.add_argument('output',type=Path);p.add_argument('--map',type=int,required=True);p.add_argument('--x',type=int,required=True);p.add_argument('--z',type=int,required=True);p.add_argument('--height',type=int,default=2);p.add_argument('--camera',type=int,default=0);p.add_argument('--battle-ready',action='store_true');p.add_argument('--repel-steps',type=int,choices=range(256),default=0);p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--layout',type=Path,default=Path(__file__).resolve().parents[1]/'tests/fixtures/companion/save-layout.json');args=p.parse_args();assert args.base.resolve()!=args.output.resolve() and not args.output.exists()
data=bytearray(args.base.read_bytes());layout=json.loads(args.layout.read_text());changes=[]
def u32(o):return struct.unpack_from('<I',data,o)[0]
def block(b,id):v=layout[str(id)];return b+v['offset'],v['size']
def crypt(raw,seed):
 out=bytearray(raw)
 for i in range(0,len(out),2):
  seed=(seed*0x41c64e6d+0x6073)&0xffffffff
  struct.pack_into('<H',out,i,struct.unpack_from('<H',out,i)[0]^(seed>>16))
 return out
source=(args.repo/'src/pokemon.c').read_text();table=source.split('static const u8 offsets[32][4] = {')[1].split('};')[0];rows=[tuple(int(x,16) for x in re.findall('0x[0-9A-Fa-f]+',row)) for row in re.findall(r'\{([^}]+)\}',table)]
for base in (0,0x40000):
 if u32(base+0xf620)!=0x20060623:continue
 assert binascii.crc_hqx(data[base:base+0xf618],65535)==struct.unpack_from('<H',data,base+0xf626)[0]
 local,size=block(base,5)
 struct.pack_into('<iiiii',data,local,args.map,-1,args.x,args.z,0)
 data[local+106]=args.camera;struct.pack_into('<i',data,local+112,0)
 objects,size=block(base,10);original=bytes(data[objects:objects+5120]);actors=[]
 for i in range(64):
  a=bytearray(original[i*80:(i+1)*80]);id=a[8]
  if struct.unpack_from('<I',a)[0]&1 and id in (255,253):
   # Only player/native Pokemon survive fixture relocation. Native map entry
   # subsequently creates official NPCs from untouched event data.
   x=args.x;z=args.z+(id==253)
   a[12:15]=bytes([0,0,0]);struct.pack_into('<hhhhhh',a,32,x,args.height,z,x,args.height,z);struct.pack_into('<i',a,44,args.height*8*4096);actors.append(a)
 assert len(actors)==2
 data[objects:objects+5120]=b''.join(actors)+bytes(5120-len(actors)*80)
 bag,size=block(base,3);struct.pack_into('<HHHH',data,bag+660,450,1,445,1);struct.pack_into('<HH',data,bag+1944,450,0)
 player,size=block(base,1);options=struct.unpack_from('<H',data,player)[0];struct.pack_into('<H',data,player,(options&~15)|2)
 # Only the Fog Badge enables native Surf for the action fixture.
 data[player+4+26]|=8
 if args.battle_ready:
  party,size=block(base,2);a=party+8;pid=u32(a);flags,checksum=struct.unpack_from('<HH',data,a+4);assert flags&3==0
  box=crypt(data[a+8:a+136],checksum);assert sum(struct.unpack('<64H',box))&65535==checksum
  offsets=rows[(pid&0x3e000)>>13];assert struct.unpack_from('<H',box,offsets[0])[0]==152
  struct.pack_into('<H',box,offsets[0],160);struct.pack_into('<I',box,offsets[0]+8,1059860);box[offsets[0]+13]=67
  struct.pack_into('<4H',box,offsets[1],242,57,127,70);box[offsets[1]+8:offsets[1]+12]=bytes([15]*4)
  checksum=sum(struct.unpack('<64H',box))&65535;struct.pack_into('<H',data,a+6,checksum);data[a+8:a+136]=crypt(box,checksum)
  party_part=crypt(data[a+136:a+236],pid);struct.pack_into('<I',party_part,0,0);party_part[4]=100;struct.pack_into('<7H',party_part,6,350,350,350,250,250,200,230);data[a+136:a+236]=crypt(party_part,pid)
 if args.repel_steps:
  roamers,size=block(base,21);data[roamers+101]=args.repel_steps
 for id in [1,2,3,5,10]+([21] if args.repel_steps else []):
  start,size=block(base,id);struct.pack_into('<H',data,start+size-4,binascii.crc_hqx(data[start:start+size-4],65535))
 struct.pack_into('<H',data,base+0xf626,binascii.crc_hqx(data[base:base+0xf618],65535));changes.append(base)
assert changes
args.output.write_bytes(data)
report={'source':str(args.base),'source_sha256':hashlib.sha256(args.base.read_bytes()).hexdigest(),'output':str(args.output),'output_sha256':hashlib.sha256(data).hexdigest(),'test_fixture_only':True,'map':args.map,'coordinates':[args.x,args.height,args.z],'changed_save_slots':changes,'setup':['relocated saved player/native Pokemon; removed stale NPC records','Bicycle and Old Rod; bicycle registered','Fog Badge to allow Surf','fast text']+(['Feraligatr level 100, test stats, Crunch/Surf/Waterfall/Strength'] if args.battle_ready else [])+([f'native Repel counter {args.repel_steps}'] if args.repel_steps else [])}
args.output.with_suffix('.fixture.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
