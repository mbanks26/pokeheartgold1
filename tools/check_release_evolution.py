"""Validate native evolution, shiny PID/OT retention, saving and cold Continue."""
from pathlib import Path
import argparse,json,struct,binascii,sys,gzip
repo=Path(__file__).resolve().parents[1]
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
from inspect_story_pokemon import crypt,OFFSETS,decode_mon
p=argparse.ArgumentParser(description='Native shiny starter evolution with authored pre-evolution level/EXP/stats and Rare Candy')
for name in ['core','rom','symbols','output','starter_root']:p.add_argument('--'+name.replace('_','-'),type=Path,required=True)
p.add_argument('--species',type=int,choices=[152,155,158]);a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True); layout=json.loads((repo/'tests/fixtures/companion/save-layout.json').read_text());personal=json.loads((repo/'files/poketool/personal/personal.json').read_text())['baseStats'];reports=[]
for species,level,evolved in [(152,15,153),(155,13,156),(158,17,159)]:
 if a.species is not None and species!=a.species:continue
 folder=out/str(species);rom=isolated_rom(a.rom,folder);raw=bytearray((a.starter_root/str(species)/'test.dsv').read_bytes()[:524288]);slot_index=None
 for base in [0,0x40000]:
  if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
  party=base+layout['2']['offset']
  if struct.unpack_from('<I',raw,party+4)[0]!=1:continue
  mon=party+8;pid=struct.unpack_from('<I',raw,mon)[0];checksum=struct.unpack_from('<H',raw,mon+6)[0];box=crypt(raw[mon+8:mon+136],checksum);aa,bb,cc,dd=OFFSETS[(pid&0x3e000)>>13];assert struct.unpack_from('<H',box,aa)[0]==species
  struct.pack_into('<I',box,aa+8,6*level**3//5-15*level**2+100*level-140)
  ivword=struct.unpack_from('<I',box,bb+16)[0];ivs=[ivword>>(5*i)&31 for i in range(6)];evs=list(box[aa+16:aa+22]);stats=personal[species];bases=[stats[x] for x in ['hp','atk','def','speed','spatk','spdef']]
  values=[(2*b+iv+ev//4)*level//100+(level+10 if i==0 else 5) for i,(b,iv,ev) in enumerate(zip(bases,ivs,evs))]
  up,down=pid%25//5,pid%5
  if up!=down:values[1+up]=values[1+up]*110//100;values[1+down]=values[1+down]*90//100
  part=crypt(raw[mon+136:mon+236],pid);part[4]=level;struct.pack_into('<7H',part,6,values[0],*values);raw[mon+136:mon+236]=crypt(part,pid)
  checksum=sum(struct.unpack('<64H',box))&65535;struct.pack_into('<H',raw,mon+6,checksum);raw[mon+8:mon+136]=crypt(box,checksum)
  bag=base+layout['3']['offset'];slots=[struct.unpack_from('<HH',raw,bag+1312+i*4) for i in range(40)];empty=next(i for i,(_,qty) in enumerate(slots) if qty==0);struct.pack_into('<HH',raw,bag+1312+empty*4,50,1);slot_index=sum(q>0 for _,q in slots[:empty])
  for block in [2,3]:
   start=base+layout[str(block)]['offset'];size=layout[str(block)]['size'];struct.pack_into('<H',raw,start+size-4,binascii.crc_hqx(raw[start:start+size-4],65535))
  struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
 fixture=folder/'input.sav';fixture.write_bytes(raw);wrap_save(fixture,rom.with_suffix('.dsv'))
 s=EmulatorSession(a.core,rom,a.symbols,folder,'evolution');g=s.boot_continue()['game'];party=int(g['party_address'],16)
 def mondata():return decode_mon(bytes.fromhex(s.send({'read':[hex(party+8),236]})['read']))
 before=mondata();assert before['species']==species and before['genuinely_shiny'] and before['level']==level
 s.send({'frames':3,'touch':[45,130]});s.send({'frames':360});s.send({'frames':3,'touch':[48,16]});s.send({'frames':180,'shot':'medicine.png'})
 for i in range(slot_index):s.send({'frames':8,'buttons':['DOWN']});s.send({'frames':90})
 for phase in ['item','use','pokemon']:
  s.send({'frames':8,'buttons':['A']});s.send({'frames':300,'shot':phase+'.png'})
 for cycle in range(35):
  s.send({'frames':8,'buttons':['A']});s.send({'frames':180,'shot':'evolution-latest.png'})
  try:now=mondata()
  except AssertionError:continue
  print(json.dumps({'starter':species,'cycle':cycle,'species':now['species'],'level':now['level']}),flush=True)
  if now['species']==evolved:break
 else:raise AssertionError('Native Rare Candy evolution did not finish')
 s.send({'frames':1800,'shot':'evolved.png'})
 for _ in range(4):s.send({'frames':8,'buttons':['A']});s.send({'frames':180})
 for _ in range(3):s.send({'frames':8,'buttons':['B']});s.send({'frames':180})
 after=mondata();assert after['species']==evolved and after['level']==level+1 and after['PID']==before['PID'] and after['OT_ID']==before['OT_ID'] and after['genuinely_shiny']
 s.save();s.close();s=EmulatorSession(a.core,rom,a.symbols,folder,'evolution-cold');g=s.boot_continue()['game'];party=int(g['party_address'],16);assert mondata()==after;s.send({'frames':1,'shot':'evolved-cold.png'});s.close()
 report={'starter':species,'before':before,'after':after,'native_save_and_cold_Continue':'PASS','scope':'Level/EXP/stats calculated from original IV/EV/nature and one Rare Candy are authored prerequisites; native item use and evolution preserve original shiny PID/OT; no runtime writes'};(folder/'result.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report);print(json.dumps(report),flush=True)
(out/'results.json').write_text(json.dumps(reports,indent=2)+'\n')
