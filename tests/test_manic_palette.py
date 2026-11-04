"""Check real converted palette usage and native animation layout constraints."""
from pathlib import Path
from PIL import Image
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from character_graphics import members
im=Image.open(ROOT/'characters/male/battle-back.png');assert im.mode=='P' and im.size==(80,640) and im.info['transparency']==0
for i in range(8):
 frame=im.crop((0,i*80,80,(i+1)*80));face=frame.crop((0,0,40,40));p=list(face.getdata())
 assert sum(x in [6,7,8] for x in p)>10,(i,'male face has no brown skin')
 assert 9 in list(frame.getdata()),(i,'red clothing lost')
 assert frame.getbbox()[1]>0 and frame.getbbox()[3]<=79,(i,'frame clipping')
pal=im.getpalette()
for i in [6,7,8]:
 r,g,b=pal[i*3:i*3+3];assert r>g>b and g-b>=20
baseline=members(subprocess.check_output(['git','show','0cb6b13b:files/a/0/0/6'],cwd=ROOT));current=members((ROOT/'files/a/0/0/6').read_bytes())
assert len(current)==len(baseline)==100
assert [i for i,(a,b)in enumerate(zip(baseline,current))if a!=b]==[0,1,4,75,76,79]
assert all(current[i]==baseline[i]for i in [2,3,77,78,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99])
trainers=json.loads((ROOT/'files/poketool/trainer/trainers.json').read_text())
records=next(v for v in trainers.values()if isinstance(v,list))
assert [t['name']for t in records[738:743]]==['{TRNAME}Lyra']*5
print('PASS all eight frames retain brown face pixels, red clothing, fixed bounds, transparent index; solo/partner/OAM/timing resources preserved; five Lyra trainer names')
