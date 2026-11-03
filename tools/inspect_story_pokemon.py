"""Read actual encrypted Pokemon data from isolated emulator RAM or battery saves."""
from pathlib import Path
import struct,json,re,argparse
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'src/pokemon.c').read_text();table=source.split('static const u8 offsets[32][4] = {')[1].split('};')[0]
OFFSETS=[tuple(int(x,16)for x in re.findall('0x[0-9A-Fa-f]+',row))for row in re.findall(r'\{([^}]+)\}',table)]
def crypt(raw,seed):
 out=bytearray(raw)
 for i in range(0,len(out),2):
  seed=(seed*0x41c64e6d+0x6073)&0xffffffff;struct.pack_into('<H',out,i,struct.unpack_from('<H',out,i)[0]^(seed>>16))
 return out

def decode_mon(raw):
 pid=struct.unpack_from('<I',raw)[0];flags,checksum=struct.unpack_from('<HH',raw,4);assert flags&3==0,'Read when native Pokemon locks are released'
 box=crypt(raw[8:136],checksum);assert sum(struct.unpack('<64H',box))&65535==checksum,'Pokemon checksum mismatch'
 a,b,c,d=OFFSETS[(pid&0x3e000)>>13];ot=struct.unpack_from('<I',box,a+4)[0];party=crypt(raw[136:236],pid);xor=((ot>>16)^(ot&65535)^(pid>>16)^(pid&65535))&65535
 return {'held_item':struct.unpack_from('<H',box,a+2)[0],'species':struct.unpack_from('<H',box,a)[0],'level':party[4],'ability':box[a+13],'experience':struct.unpack_from('<I',box,a+8)[0],'moves':list(struct.unpack_from('<4H',box,b)),'PP':list(box[b+8:b+12]),'PID':pid,'OT_ID':ot,'nature':pid%25,'shiny_xor':xor,'genuinely_shiny':xor<8,'checksum_valid':True,'HP':struct.unpack_from('<H',party,6)[0],'max_HP':struct.unpack_from('<H',party,8)[0]}

def inspect_ram(raw,symbols):
 match=re.search(r'^\s*([0-9a-fA-F]{8})\s+[0-9a-fA-F]{8}\s+\.bss\s+sFieldSysPtr\b',symbols,re.M);assert match
 u=lambda a:struct.unpack_from('<I',raw,a-0x2000000)[0]
 fs=u(int(match.group(1),16));sd=u(fs+12);party=sd+16+u(sd+0x23014+2*16+8);player=sd+16+u(sd+0x23014+1*16+8)
 return {'player_OT_ID':u(player+4+16),'party':[decode_mon(raw[party+8+i*236-0x2000000:party+8+(i+1)*236-0x2000000])for i in range(u(party+4))]}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ram',type=Path);p.add_argument('--symbols',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--species',type=int);a=p.parse_args();r=inspect_ram(a.ram.read_bytes(),a.symbols.read_text())
 if a.species is not None:
  m=r['party'][0];assert m['species']==a.species and m['level']==5 and m['genuinely_shiny'] and m['OT_ID']==r['player_OT_ID'];assert m['held_item']==0;assert m['ability']=={152:65,155:66,158:67}[a.species];assert m['moves']=={152:[33,45,0,0],155:[33,43,0,0],158:[10,43,0,0]}[a.species]
 if a.output:a.output.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
