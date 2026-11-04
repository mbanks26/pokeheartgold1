"""Choose all three starters in native UI, save, fully close and cold Continue."""
from pathlib import Path
import argparse,json,struct,binascii
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
from inspect_story_pokemon import inspect_ram

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for name in ['core','rom','symbols','output']:p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
commands=json.loads((ROOT/'tests/fixtures/story/starter-inputs.json').read_text())['commands'];reports=[]
for species,touch in [(152,[128,110]),(155,[181,40]),(158,[76,40])]:
    folder=a.output/str(species);rom=isolated_rom(a.rom,folder)
    imported=wrap_save(ROOT/'tests/fixtures/story/pre-starter-lab.sav.gz',rom.with_suffix('.dsv'))
    s=EmulatorSession(a.core,rom,a.symbols,folder,'selection')
    for step,command in enumerate(commands,1):
        if step==13:command={'frames':3,'touch':touch}
        s.send(command)
    g=s.send({'frames':1,'dump':'selected.bin','inspect':True,'shot':'selected.png'})['game']
    assert g['task']=='0x0' and sum(o['id']==253 for o in g['objects'])==1
    original=inspect_ram((folder/'selected.bin').read_bytes(),a.symbols.read_text())
    mon=original['party'][0]
    assert mon['species']==species and mon['level']==5 and mon['genuinely_shiny'] and mon['OT_ID']==original['player_OT_ID']
    assert mon['ability']=={152:65,155:66,158:67}[species]
    assert mon['moves']=={152:[33,45,0,0],155:[33,43,0,0],158:[10,43,0,0]}[species]
    s.save();s.close()
    raw=rom.with_suffix('.dsv').read_bytes();sectors=[base for base in (0,0x40000) if struct.unpack_from('<I',raw,base+0xf620)[0]==0x20060623]
    sector=max(sectors,key=lambda b:struct.unpack_from('<I',raw,b+0xf618)[0])
    assert binascii.crc_hqx(raw[sector:sector+0xf618],65535)==struct.unpack_from('<H',raw,sector+0xf626)[0]
    s=EmulatorSession(a.core,rom,a.symbols,folder,'cold-continue');s.boot_continue()
    s.send({'frames':64,'buttons':['LEFT']});s.send({'frames':48,'buttons':['DOWN']})
    s.send({'frames':180,'dump':'cold-loaded.bin','shot':'cold-loaded.png','inspect':True})
    loaded=inspect_ram((folder/'cold-loaded.bin').read_bytes(),a.symbols.read_text())
    assert loaded==original,'Native saved Pokemon differs after cold Continue'
    s.close()
    report={'species':species,'selected':original,'cold_Continue_identical':True,'native_save_CRC':'PASS',
            'save_counter':struct.unpack_from('<I',raw,sector+0xf618)[0],'fixture_import':imported,
            'scope':'Native selection/save/cold load; pre-starter progress is an existing native battery fixture'}
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report)
    print(json.dumps(report),flush=True)
(a.output/'results.json').write_text(json.dumps(reports,indent=2)+'\n')
