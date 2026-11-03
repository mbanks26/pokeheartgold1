"""Verify recovered designs, original trainers and protected native story events."""
from pathlib import Path
import subprocess,json,sys
from character_graphics import members
root=Path(__file__).resolve().parents[1];base='bcf2f8fd9377e001c36d67308dc0c2402c4f2505'
def git(*args,**kwargs):return subprocess.check_output(['git',*args],cwd=root,**kwargs)
rows=[]
for line in git('ls-tree','-r',base).decode().splitlines():
 meta,path=line.split('\t')
 if Path(path).suffix.lower() in {'.png','.nsbtx','.ncgr','.nclr','.ncer','.nanr','.nscr'}:rows.append((path,meta.split()[2]))
actual=git('hash-object','--stdin-paths',input=('\n'.join(p for p,_ in rows)+'\n').encode()).decode().splitlines();assert len(actual)==len(rows);assert all(want==got for(_,want),got in zip(rows,actual))
before=members(git('show',base+':files/a/0/0/6'));after=members((root/'files/a/0/0/6').read_bytes());assert after[:len(before)]==before
original=json.loads(git('show',base+':files/poketool/trainer/trainers.json'))['trainers'];current=json.loads((root/'files/poketool/trainer/trainers.json').read_text())['trainers'];assert current[:len(original)]==original
protected=['files/fielddata/script/scr_seq/scr_seq_0892_T25R0401.s','files/fielddata/script/scr_seq/scr_seq_0090_D35R0103.s']
for p in protected:assert git('show',base+':'+p)==(root/p).read_bytes(),p
report={'baseline':base,'unchanged_existing_graphics':len(rows),'preserved_back_members':len(before),'appended_partner_members':len(after)-len(before),'unchanged_original_trainers':len(original),'appended_trainers':len(current)-len(original),'player_Bill_Eevee_event':'unchanged','Lance_partner_event':'unchanged','save_structure':'unchanged','changed_files':git('diff','--name-only',base).decode().splitlines()}
if len(sys.argv)>1:(root/sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
