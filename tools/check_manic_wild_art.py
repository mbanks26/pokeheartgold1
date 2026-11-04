"""Capture native wild intro/throw frames from explicitly authored location prerequisites."""
from pathlib import Path
import argparse,json,gzip,struct,binascii
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for k in ['core','rom','symbols','output']:p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();rom=isolated_rom(a.rom,a.output)
raw=bytearray(gzip.decompress((ROOT/'tests/fixtures/release/ledge-input.sav.gz').read_bytes()));layout=json.loads((ROOT/'tests/fixtures/companion/save-layout.json').read_text())
for base in [0,0x40000]:
 if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
 local=base+layout['5']['offset'];struct.pack_into('<5i',raw,local,33,-1,638,398,2)
 raw[local+106]=0;struct.pack_into('<i',raw,local+112,0)
 objs=base+layout['10']['offset'];actors=[]
 for i in range(64):
  r=bytearray(raw[objs+i*80:objs+(i+1)*80])
  if struct.unpack_from('<I',r)[0]&1 and r[8]in[255,253]:
   x=638+(r[8]==253);r[12:15]=bytes([2]*3);struct.pack_into('<6h',r,32,x,2,398,x,2,398);struct.pack_into('<i',r,44,65536);actors.append(r)
 assert len(actors)==2
 raw[objs:objs+5120]=b''.join(actors)+bytes(5120-160)
 raw[base+layout['21']['offset']+101]=0
 for block in [5,10,21]:
  start=base+layout[str(block)]['offset'];size=layout[str(block)]['size'];struct.pack_into('<H',raw,start+size-4,binascii.crc_hqx(raw[start:start+size-4],65535))
 struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
fixture=a.output/'input.sav';fixture.write_bytes(raw);wrap_save(fixture,rom.with_suffix('.dsv'))
s=EmulatorSession(a.core,rom,a.symbols,a.output,'wild')
try:
 s.boot_continue();s.send({'frames':120,'shot':'field.png'})
 for n in range(50):
  s.send({'frames':16,'buttons':['LEFT'if n%16<8 else'RIGHT']});g=s.send({'frames':30,'inspect':True})['game']
  if g['battle_paired']:break
 else:raise AssertionError('No native wild encounter reached in this authored grass location')
 for frame in range(0,480,8):s.send({'frames':8,'shot':f'intro-{frame:03d}.png'})
 s.close();(a.output/'result.json').write_text(json.dumps({'native_wild_paired_intro':True,'scope':'Authored Route29 location and Repel removal; encounter and animation through native inputs; captured 60 consecutive 8-frame samples. Visual review is separate.'},indent=2)+'\n')
except BaseException:s.abort();raise
