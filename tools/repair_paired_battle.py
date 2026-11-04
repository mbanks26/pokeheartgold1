"""Reconvert approved full-colour paired artwork with a reserved hardware palette.

No new poses are drawn. One crop, scale and anchor apply to the entire animation;
white background pixels never compete for the fifteen opaque palette entries.
"""
from pathlib import Path
from collections import deque
import json,hashlib
from PIL import Image
from character_graphics import ROOT,apply_battle
source=ROOT/'characters/male/paired-master.png'
master=Image.open(source).convert('RGBA');frames=[]
for i in range(8):
 x=i%4;y=i//4
 im=master.crop((round(x*master.width/4),round(y*master.height/2),round((x+1)*master.width/4),round((y+1)*master.height/2)))
 pixels=im.load();seen=set();q=deque([(a,b) for a in range(im.width) for b in [0,im.height-1]]+[(a,b)for b in range(im.height)for a in [0,im.width-1]])
 while q:
  a,b=q.popleft()
  if not(0<=a<im.width and 0<=b<im.height)or(a,b)in seen:continue
  seen.add((a,b))
  if min(pixels[a,b][:3])<=225:continue
  pixels[a,b]=(0,0,0,0);q.extend([(a-1,b),(a+1,b),(a,b-1),(a,b+1)])
 frames.append(im)
boxes=[im.getbbox() for im in frames];box=(min(b[0]for b in boxes),min(b[1]for b in boxes),max(b[2]for b in boxes),max(b[3]for b in boxes))
scale=min(78/(box[2]-box[0]),74/(box[3]-box[1]));size=(round((box[2]-box[0])*scale),round((box[3]-box[1])*scale))
colors=[(0,0,0),(8,8,8),(25,25,25),(58,49,49),(91,82,82),(247,247,239),(140,90,58),(181,123,82),(90,57,33),(189,66,66),(99,33,58),(25,49,49),(58,82,74),(156,58,90),(222,190,165),(222,173,74)]
colors=[tuple(round(round(v/255*31)*255/31)for v in c)for c in colors]
sheet=Image.new('P',(80,640));sheet.putpalette([v for c in colors for v in c]+[0]*(768-48));sheet.info['transparency']=0
cache={}
for i,im in enumerate(frames):
 im=im.crop(box).resize(size,Image.Resampling.NEAREST);indices=[]
 for r,g,b,a in im.getdata():
  if a<128:indices.append(0);continue
  rgb=(r,g,b)
  if rgb not in cache:cache[rgb]=min(range(1,16),key=lambda j:sum((rgb[k]-colors[j][k])**2 for k in range(3)))
  indices.append(cache[rgb])
 tile=Image.new('P',size);tile.putpalette(sheet.getpalette());tile.putdata(indices)
 sheet.paste(tile,((80-size[0])//2,i*80+79-size[1]))
sheet.save(ROOT/'characters/male/battle-back.png',bits=4,transparency=0)
reports=[apply_battle('male','files/a/0/0/6',n,'back',Path('build/release-candidate'))for n in [0,15]]
out=ROOT/'docs/repairs';out.mkdir(exist_ok=True)
(out/'paired-conversion.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fixed_crop':box,'fixed_scale':scale,'fixed_size':size,'palette':colors,'reserved_skin_indices':[6,7,8],'frames':8,'conversion':reports,'scope':'Conversion checks, not proof of rendered visual quality'},indent=2)+'\n')
