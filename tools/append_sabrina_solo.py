#!/usr/bin/env python3
"""Append exact existing solo resources; never redraw or replace paired graphics."""
from pathlib import Path
import hashlib,json,struct,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from character_graphics import members,u32
root=Path(__file__).resolve().parents[1]
path='files/a/0/0/6'
base=subprocess.check_output(['git','show','4ea2dc8a:'+path],cwd=root)
solo=subprocess.check_output(['git','show','bda9631d:'+path],cwd=root)
old=members(base);source=members(solo);assert len(old)==85
fat_end=16+u32(base,20);gmif=fat_end+u32(base,fat_end+4)
payload=bytearray(base[gmif+8:]);entries=[struct.unpack_from('<II',base,28+8*i) for i in range(len(old))]
added=source[0:5]+source[75:80]
for data in added:
    while len(payload)%4:payload.append(255)
    start=len(payload);payload+=data;entries.append((start,len(payload)))
while len(payload)%4:payload.append(255)
fat=struct.pack('<4sIHH',b'BTAF',12+8*len(entries),len(entries),0)+b''.join(struct.pack('<II',*e) for e in entries)
body=fat+base[fat_end:gmif]+struct.pack('<4sI',b'GMIF',8+len(payload))+payload
head=bytearray(base[:16]);struct.pack_into('<I',head,8,16+len(body));result=bytes(head)+body
assert members(result)[:85]==old and members(result)[85:]==added
(root/path).write_bytes(result)
report={'unchanged_existing_members':85,'appended_backpic_ids':[17,18],
        'source_commit':'bda9631d','source_backpic_ids':[0,15],
        'original_archive_sha256':hashlib.sha256(base).hexdigest(),
        'extended_archive_sha256':hashlib.sha256(result).hexdigest(),
        'new_graphics_created':False}
out=root/'docs/companion';out.mkdir(parents=True,exist_ok=True)
(out/'graphics-preservation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
