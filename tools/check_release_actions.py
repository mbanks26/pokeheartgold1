"""Native field action QA; test prerequisites are explicitly authored."""
from pathlib import Path
import sys,struct,json,binascii,gzip,argparse
repo=Path(__file__).resolve().parents[1]
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
from inspect_story_pokemon import inspect_ram
p=argparse.ArgumentParser(description='Native cycling, corners, Surf and restoration with an authored action fixture')
for name in ['core','rom','symbols','output']:p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
layout=json.loads((repo/'tests/fixtures/companion/save-layout.json').read_text())
raw=bytearray(gzip.decompress((repo/'tests/fixtures/release/actions-input.sav.gz').read_bytes()))
for base in [0,0x40000]:
 if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
 # Test-only: running shoes and Repel prevent encounter timing from obscuring field actions.
 # Native running shoes flag is left as saved; running cannot be claimed if absent.
 roam=base+layout['21']['offset'];raw[roam+101]=255
 size=layout['21']['size'];struct.pack_into('<H',raw,roam+size-4,binascii.crc_hqx(raw[roam:roam+size-4],65535))
 struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
fixture=out/'input.sav';fixture.write_bytes(raw);rom=isolated_rom(a.rom,out);wrap_save(fixture,rom.with_suffix('.dsv'))
s=EmulatorSession(a.core,rom,a.symbols,out,'actions');report=[]
def inspect(name,counts=None,state=None):
 c={'frames':120,'inspect':True,'shot':name+'.png'}
 if counts is not None:c['expect']={'counts':counts,'avatar_state':state,'joined':True}
 r=s.send(c);g=r['game'];report.append({'checkpoint':name,'state':g.get('avatar_state'),'task':g.get('task'),'counts':{i:sum(o['id']==i for o in g.get('objects',[])) for i in [252,253]},'player':next(o['xyz'] for o in g['objects'] if o['id']==255)});return g
def move(button,frames=48):s.send({'frames':frames,'buttons':[button]});s.send({'frames':60})
try:
 s.boot_continue();s.send({'talk':60});move('DOWN',48);inspect('walking',{252:1,253:1},0)
 s.send({'frames':8,'buttons':['Y']});inspect('cycling',{252:0},1)
 move('LEFT',24);s.send({'frames':8,'buttons':['Y']});s.send({'frames':120});move('LEFT',32);move('RIGHT',48);inspect('cycling-restored',{252:1,253:1},0)
 # Walk to a known safe south-town strip; repeated corners and stops stay in native terrain.
 for repeat in range(8):
  for direction in ['LEFT','DOWN','RIGHT','UP']:move(direction,32)
  inspect('corner-loop-'+str(repeat),{252:1,253:1},0)
 g=inspect('before-shore');player=next(o['xyz'] for o in g['objects'] if o['id']==255)
 # Axis waypoints stay below New Bark's buildings.
 for axis,target,positive,negative in [(2,400,'DOWN','UP'),(0,700,'RIGHT','LEFT')]:
  for _ in range(3):
   g=s.send({'frames':1,'inspect':True})['game'];v=next(o['xyz'] for o in g['objects'] if o['id']==255)[axis];delta=target-v
   if not delta:break
   move(positive if delta>0 else negative,abs(delta)*16)
  assert next(o['xyz'] for o in s.send({'frames':1,'inspect':True})['game']['objects'] if o['id']==255)[axis]==target
 move('RIGHT',8);inspect('surf-shore')
 for _ in range(8):
  s.send({'frames':8,'buttons':['A']});g=s.send({'frames':180,'inspect':True})['game']
  if g['avatar_state']==2:break
 inspect('surfing',{252:0},2)
 move('RIGHT',24);move('LEFT',96);s.send({'talk':15,'button':'B'});move('LEFT',48)
 inspect('surfing-restored',{252:1,253:1},0)
 s.save();s.send({'frames':1,'dump':'after-actions.bin'});s.close()
 (out/'results.json').write_text(json.dumps({'scope':'Isolated authored item/badge/party/Repel prerequisites; movement and restoration through native UI, no runtime writes','checkpoints':report},indent=2)+'\n')
 print(json.dumps(report),flush=True)
except BaseException:
 s.send({'frames':1,'inspect':True,'shot':'failure.png'});s.close();raise
