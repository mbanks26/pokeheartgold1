"""Native Select/A companion dialogue and follower restoration with an old battery save."""
from pathlib import Path
import argparse,json,gzip
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
p=argparse.ArgumentParser(description=__doc__)
for k in ['core','rom','symbols','output','save']:p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();out=a.output;rom=isolated_rom(a.rom,out)
raw=a.save.read_bytes();raw=gzip.decompress(raw)if a.save.suffix=='.gz'else raw
fixture=out/'input.sav';fixture.write_bytes(raw[:524288]);wrap_save(fixture,rom.with_suffix('.dsv'))
s=EmulatorSession(a.core,rom,a.symbols,out,'interaction');results=[]
def field(name,talking=None):
 g=s.send({'frames':120,'inspect':True,'shot':name+'.png'})['game']
 for identity in [252,253]:
  matches=[o for o in g['objects']if o['id']==identity];assert len(matches)==1,(name,identity,g)
  assert not(int(matches[0]['flags'],16)&512),(name,'hidden',matches[0])
 if talking is not None:assert (g['task']!='0x0')==talking,(name,g)
 results.append({'name':name,'task':g['task'],'objects':[o for o in g['objects']if o['id']in[252,253,255]]})
 return g
def press(key,frames=8):s.send({'frames':frames,'buttons':[key]});s.send({'frames':90})
def menu():
 g=s.send({'frames':1,'inspect':True})['game'];player=next(o for o in g['objects']if o['id']==255);mon=next(o for o in g['objects']if o['id']==253)
 dx=mon['xyz'][0]-player['xyz'][0];dz=mon['xyz'][2]-player['xyz'][2]
 assert abs(dx)+abs(dz)==1,g
 direction='RIGHT'if dx==1 else'LEFT'if dx==-1 else'DOWN'if dz==1 else'UP'
 index={'UP':0,'DOWN':1,'LEFT':2,'RIGHT':3}[direction]
 if player['direction']!=index:s.send({'frames':4,'buttons':[direction]});s.send({'frames':30})
 press('A');return field('a-menu',True)
try:
 s.boot_continue()
 for key in ['RIGHT','LEFT']:press(key,48)
 g=field('formation',False);human=next(o for o in g['objects']if o['id']==252)['address']
 for i in range(3):
  press('SELECT');g=field('select-'+str(i),True)
  assert next(o for o in g['objects']if o['id']==252)['address']==human
  s.send({'talk':30});field('select-resumed-'+str(i),False)
 menu();press('DOWN');press('A');field('a-sabrina',True);s.send({'talk':30});field('a-sabrina-resumed',False)
 menu();press('A');field('a-pokemon',True);s.send({'talk':40});field('a-pokemon-resumed',False)
 menu();press('B');field('a-cancel',False)
 s.save();s.close();s=EmulatorSession(a.core,rom,a.symbols,out,'interaction-cold');s.boot_continue()
 for key in ['RIGHT','LEFT']:press(key,48)
 field('cold-restored',False)
 s.send({'frames':4,'buttons':['RIGHT']});s.send({'frames':30});s.send({'frames':16,'buttons':['RIGHT']})
 g=field('direct-approach',False)
 player=next(o for o in g['objects']if o['id']==255);human=next(o for o in g['objects']if o['id']==252)
 assert human['xyz']==[player['xyz'][0]+1,player['xyz'][1],player['xyz'][2]] and player['direction']==3
 press('A');field('direct-a-sabrina',True);s.send({'talk':30});field('direct-a-resumed',False);s.close()
 (out/'result.json').write_text(json.dumps({'pass':True,'scope':'Native input from a compatible prior RC1 battery save; no runtime writes; Select repeated, A formation menu/Sabrina/native Pokemon/Cancel, real save and cold Continue, native approach/swapping past Pokemon then direct adjacent A','checkpoints':results},indent=2)+'\n')
 print('PASS native companion conversation visibility, A menu choices, repeated Select and save/cold restoration')
except BaseException:s.abort();raise
