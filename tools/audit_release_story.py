"""Check native dispatch/event preservation; this is not a campaign playthrough."""
from pathlib import Path
import argparse,subprocess,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE='bcf2f8fd9377e001c36d67308dc0c2402c4f2505'
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
paths=git('ls-tree','-r','--name-only',BASE).decode().splitlines();scripts=[];events=[];battle=[];changed_scripts=[]
for path in paths:
    if path.startswith('files/fielddata/script/scr_seq/') and path.endswith('.s'):
        old=git('show',BASE+':'+path).decode();current=(ROOT/path).read_text()
        before=re.findall(r'^\s*ScrDef\s+(\w+)',old,re.M);after=re.findall(r'^\s*ScrDef\s+(\w+)',current,re.M)
        assert after[:len(before)]==before,'Original dispatch order changed: '+path
        scripts.append(path)
        if old!=current:changed_scripts.append(path)
    elif path.startswith('files/fielddata/eventdata/zone_event/') and path.endswith('.json'):
        old=json.loads(git('show',BASE+':'+path));current=json.loads((ROOT/path).read_text())
        for key in ['warps','bgs','coords','objects']:
            assert current.get(key,[])[:len(old.get(key,[]))]==old.get(key,[]),'Original event data replaced: '+path+'/'+key
        events.append(path)
    elif path.startswith('src/battle/') or path.startswith('asm/overlay_12') or path.startswith('asm/overlay_10'):
        assert git('show',BASE+':'+path)==(ROOT/path).read_bytes(),'Native battle/AI source changed: '+path
        battle.append(path)
new_texts=0
for path in paths:
    if not(path.startswith('files/msgdata/msg/') and path.endswith('.json')):continue
    old=json.loads(git('show',BASE+':'+path));current=json.loads((ROOT/path).read_text());before={m['id']:m.get('en_US') for m in old.get('messages',[])}
    for message in current.get('messages',[]):
        value=message.get('en_US')
        if value==before.get(message['id']):continue
        assert isinstance(value,str)
        for page in value.split('\r'):
            assert len(page.split('\n'))<=2,message['id']
            for line in page.split('\n'):
                assert len(re.sub(r'\{[^}]+\}','ABCDEFG',line))<=32,(message['id'],line)
        new_texts+=1
gold=(ROOT/'files/fielddata/script/scr_seq/scr_seq_0885_T25.s').read_text().split('scr_seq_T25_033:',1)[1]
assert gold.index('GoToIfSet FLAG_STORY_DISABLED_FOR_FEMALE')<gold.index('GoToIfSet FLAG_SISTER_RECEIVED_EEVEE')
assert 'GoToIfUnset FLAG_SABRINA_COMPANION_JOINED, T25_Sister_WithoutSabrina' in gold
original_events=['files/fielddata/script/scr_seq/scr_seq_0892_T25R0401.s','files/fielddata/script/scr_seq/scr_seq_0090_D35R0103.s','files/fielddata/script/scr_seq/scr_seq_0829_T11GYM0101.s','files/fielddata/script/scr_seq/scr_seq_0832_T11R0101.s']
for path in original_events:assert git('show',BASE+':'+path)==(ROOT/path).read_bytes()
report={'baseline':BASE,'original_script_dispatch_tables_preserved':len(scripts),'original_map_event_collections_preserved':len(events),'native_battle_AI_files_unchanged':len(battle),'reviewed_changed_or_added_messages':new_texts,'protected_Bill_Lance_Sabrina_Gym_and_Dojo_scripts':'byte-identical','Goldenrod_female_and_disabled_guards':'PASS','changed_scripts_since_baseline':changed_scripts,'scope':'Static source/dispatch/event preservation and two-line 32-character formatting checks; no claim of native campaign completion or pixel-perfect font measurement'}
a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='changed_scripts_since_baseline'}))
