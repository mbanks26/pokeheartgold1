"""Append a compatible partner presentation using Sabrina's existing three poses.
No original PNG, palette, NARC member, or combined male/Sabrina artwork is replaced.
"""
from pathlib import Path
import hashlib,json,struct,subprocess,tempfile,sys
from PIL import Image
root=Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name=='tools' else Path('/workspace/work/recovery/pokeheartgold1')
sys.path.insert(0,str(root/'tools'))
from character_graphics import members,u32,palette_bytes,packed4,encrypt_portrait
b=(root/'files/a/0/0/6').read_bytes();old=members(b);assert len(old)==95
ncgr,nclr,ncer,nanr,ncbr=old[:5]
src=root/'characters/sabrina/battle-front.png';im=Image.open(src);assert im.mode=='P' and im.size==(80,240)
sequence=[0,0,1,1,2,2,1,0];sheet=Image.new('P',(80,640),0);sheet.putpalette(im.getpalette());sheet.info['transparency']=0
for i,pose in enumerate(sequence):sheet.paste(im.crop((0,pose*80,80,(pose+1)*80)),(0,i*80))
gfx=root/'build/story-integration/tools/nitrogfx/nitrogfx'
with tempfile.TemporaryDirectory()as d:
 p=Path(d);(p/'layout.NCER').write_bytes(ncer);subprocess.run([str(gfx),str(p/'layout.NCER'),str(p/'layout.json')],check=True)
 layout=json.loads((p/'layout.json').read_text());assert layout['cellCount']==8
 atlas=Image.new('P',(80,647),0);atlas.putpalette(im.getpalette())
 for i in range(8):atlas.paste(sheet.crop((0,i*80,80,(i+1)*80)),(0,i*81))
 atlas.save(p/'atlas.png',bits=4);subprocess.run([str(gfx),str(p/'atlas.png'),str(p/'new.NCGR'),'-cell',str(p/'layout.json'),'-clobbersize','-version101','-mappingtype','64','-vram'],check=True)
 char=(p/'new.NCGR').read_bytes();assert len(char)==len(ncgr);char=ncgr[:48]+char[48:];pal=bytearray(nclr);pal[40:72]=palette_bytes(im)
 (p/'new.NCGR').write_bytes(char);(p/'new.NCLR').write_bytes(pal);subprocess.run([str(gfx),str(p/'new.NCGR'),str(p/'decoded.png'),'-palette',str(p/'new.NCLR'),'-cell',str(p/'layout.json')],check=True);decoded=Image.open(p/'decoded.png')
 for i in range(8):assert list(decoded.crop((0,i*81,80,i*81+80)).getdata())==list(sheet.crop((0,i*80,80,(i+1)*80)).getdata())
 portrait=Image.new('P',(160,80),0);portrait.putpalette(im.getpalette());portrait.paste(im.crop((0,0,80,80)),(0,0));portrait.paste(im.crop((0,160,80,240)),(80,0));added=[char,bytes(pal),ncer,nanr,encrypt_portrait(packed4(portrait),ncbr)]
fat_end=16+u32(b,20);gmif=fat_end+u32(b,fat_end+4);payload=bytearray(b[gmif+8:]);entries=[struct.unpack_from('<II',b,28+8*i)for i in range(95)]
for raw in added:
 while len(payload)%4:payload.append(255)
 start=len(payload);payload+=raw;entries.append((start,len(payload)))
while len(payload)%4:payload.append(255)
fat=struct.pack('<4sIHH',b'BTAF',12+8*len(entries),len(entries),0)+b''.join(struct.pack('<II',*x)for x in entries);body=fat+b[fat_end:gmif]+struct.pack('<4sI',b'GMIF',8+len(payload))+payload;head=bytearray(b[:16]);struct.pack_into('<I',head,8,16+len(body));result=bytes(head)+body;assert members(result)[:95]==old
(root/'files/a/0/0/6').write_bytes(result);sheet.save(root/'characters/sabrina/partner-presentation.png',bits=4,transparency=0)
report={'source':str(src.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_poses':sequence,'original_members_preserved':95,'appended_backpic_id':19,'NCGR_OAM_roundtrip':'PASS','new_design_drawn':False,'presentation_limit':'Existing front/profile psychic poses are reused in the partner slot; no dedicated newly drawn back/throw sheet.'}
(root/'docs/story/partner-graphics.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
