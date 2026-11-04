"""Replay a blank-save opening for either gender using native inputs only."""
from pathlib import Path
import argparse,json,struct,binascii
from release_emulator_session import EmulatorSession,isolated_rom
from inspect_story_pokemon import inspect_ram

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for name in ['core','rom','symbols','output']:p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--gender',choices=['male','female'],required=True)
a=p.parse_args();rom=isolated_rom(a.rom,a.output)
s=EmulatorSession(a.core,rom,a.symbols,a.output)
commands=json.loads((ROOT/'tests/fixtures/story/opening-inputs.json').read_text())['commands']
for step,command in enumerate(commands,1):
    if a.gender=='female' and step==81:command={'frames':3,'touch':[192,100]}
    s.send(command)
    if step%20==0:print(json.dumps({'step':step}),flush=True)
result=s.send({'frames':1,'inspect':True,'dump':'fresh-opening.bin','shot':'fresh-opening.png'})
g=result['game'];expected_gender=int(a.gender=='female')
assert g['gender']==expected_gender and g['task']=='0x0' and g['map']==61
counts={i:sum(o['id']==i for o in g['objects']) for i in [252,253]}
assert counts[253]==1 and counts[252]==(1-expected_gender)
assert g['joined']==(a.gender=='male')
raw=(a.output/'fresh-opening.bin').read_bytes();pokemon=inspect_ram(raw,a.symbols.read_text())
mon=pokemon['party'][0]
assert mon['species']==152 and mon['level']==5 and mon['genuinely_shiny']
assert mon['OT_ID']==pokemon['player_OT_ID']
flags=int(g['flag_address'],16)-0x2000000
assert bool(raw[flags+0xB5D//8] & (1<<(0xB5D%8)))==bool(expected_gender)
report={'gender':a.gender,'scope':'Fresh native opening through starter; no authored progress or RAM writes',
        'custom_name_input':'CPDEX','counts':counts,'joined':g['joined'],'pokemon':pokemon,
        'female_story_guard':bool(expected_gender),'frames':result['frame']}
s.save();s.close()
saved=rom.with_suffix('.dsv').read_bytes();sectors=[base for base in [0,0x40000] if struct.unpack_from('<I',saved,base+0xf620)[0]==0x20060623];latest=max(sectors,key=lambda base:struct.unpack_from('<I',saved,base+0xf618)[0])
assert binascii.crc_hqx(saved[latest:latest+0xf618],65535)==struct.unpack_from('<H',saved,latest+0xf626)[0]
s=EmulatorSession(a.core,rom,a.symbols,a.output,'opening-cold');g=s.boot_continue()['game'];assert g['gender']==expected_gender and g['joined']==(a.gender=='male');s.close()
report.update(native_poststarter_save_and_cold_Continue='PASS',save_counter=struct.unpack_from('<I',saved,latest+0xf618)[0])
(a.output/'result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
