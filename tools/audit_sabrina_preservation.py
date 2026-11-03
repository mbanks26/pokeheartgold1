#!/usr/bin/env python3
"""Check original artwork/resources and story assets against the recovery checkpoint."""
from pathlib import Path
import json,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from character_graphics import members
root=Path(__file__).resolve().parents[1]
def git(*args,**kwargs):return subprocess.check_output(['git',*args],cwd=root,**kwargs)
base='4ea2dc8a'
extensions={'.png','.nsbtx','.ncgr','.nclr','.ncer','.nanr','.nscr'}
entries=[]
for entry in git('ls-tree','-r',base).decode().splitlines():
    meta,path=entry.split('\t',1)
    if Path(path).suffix.lower() in extensions:entries.append((path,meta.split()[2]))
hashes=git('hash-object','--stdin-paths',input=('\n'.join(p for p,_ in entries)+'\n').encode()).decode().splitlines()
changed=[p for (p,expected),actual in zip(entries,hashes) if expected!=actual]
assert len(hashes)==len(entries) and not changed,changed
changed_assets=git('diff','--name-only',base,'--','files').decode().splitlines()
assert changed_assets==['files/a/0/0/6'],changed_assets
archive=members((root/'files/a/0/0/6').read_bytes())
original=members(git('show',base+':files/a/0/0/6'))
solo=members(git('show','bda9631d:files/a/0/0/6'))
assert len(original)==85 and len(archive)==95
assert archive[:85]==original and archive[85:]==solo[:5]+solo[75:80]
report={'baseline':base,'verified_existing_graphic_files':len(entries),'changed_existing_graphic_files':changed,
        'existing_backpic_members_preserved':85,'appended_existing_solo_resources':10,
        'changed_story_scripts':[],'other_changed_game_assets':[]}
(root/'docs/companion/art-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
