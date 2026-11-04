"""Validate separate native AI parties, legal moves and protected battle routes.

These are static/data checks; emulator evidence is recorded separately.
"""
from pathlib import Path
import json,re,struct,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from character_graphics import members
def constants(file,prefix):
    return {k:int(v,0) for k,v in re.findall(r'^#define ('+prefix+r'\w+)\s+(0x[0-9a-fA-F]+|\d+)\b',(ROOT/file).read_text(),re.M)}
species=constants('include/constants/species.h','SPECIES_')
moves=constants('include/constants/moves.h','MOVE_')
personal=json.loads((ROOT/'files/poketool/personal/personal.json').read_text())['baseStats']
learn=members((ROOT/'files/poketool/personal/wotbl.narc').read_bytes())
tm_source=(ROOT/'src/item.c').read_text().split('sTMHMMoves')[1].split('};')[0]
tm=[moves[x] for x in re.findall(r'\bMOVE_\w+',tm_source)]
assert len(tm)==100
trainers=json.loads((ROOT/'files/poketool/trainer/trainers.json').read_text())['trainers']
assert len(trainers)==750
count=0
for t in trainers[743:]:
    assert t['type']=='TRTYPE_MON_MOVES' and t['ai_flags']==7 and not t['items']
    for mon in t['party']:
        s=species[mon['species']]; level=mon['level'];p=personal[s]
        legal={x&511 for x in struct.unpack('<'+'H'*(len(learn[s])//2),learn[s]) if x!=65535 and x>>9<=level}
        legal|={tm[x-1] for x in p['tms']}|{tm[91+x] for x in p['hms']}
        for move in mon['moves']:
            assert moves[move] in legal,(mon['species'],level,move)
            count+=1
        assert mon['difficulty']<=255 and mon['abilityOverride']=='TRPOKE_ABILITY_OVERRIDE_OFF'
assert [m['species'] for m in trainers[743]['party']]==['SPECIES_KADABRA']
assert len(trainers[744]['party'])==len(trainers[745]['party'])==2
base='bcf2f8fd9377e001c36d67308dc0c2402c4f2505'
for path in ['src/encounter.c','src/battle/trainer_ai.c','src/scrcmd_battle.c']:
    assert subprocess.check_output(['git','show',base+':'+path],cwd=ROOT)==(ROOT/path).read_bytes()
encounter=(ROOT/'src/encounter.c').read_text()
assert 'BATTLE_TYPE_TRAINER | BATTLE_TYPE_DOUBLES | BATTLE_TYPE_MULTI | BATTLE_TYPE_AI' in encounter
assert 'setup->trainerId[BATTLER_PLAYER2] = followerTrainerNum' in encounter
for area in ['D26R0102','D23R0105']:
    s=next((ROOT/'files/fielddata/script/scr_seq').glob('*_'+area+'.s')).read_text()
    assert s.count('MultiBattle TRAINER_SABRINA_PARTNER_')==1
    assert s.index('CheckBattleWon',s.index('SabrinaPartner_'+area+'_Check:'))<s.index('SetFlag FLAG_SABRINA_PARTNER_')
    assert 'WhiteOut' in s and 'FLAG_SABRINA_COMPANION_JOINED' in s
report=json.loads((ROOT/'docs/story/partner-graphics.json').read_text())
assert report['original_members_preserved']==95 and not report['new_design_drawn']
assert len(members((ROOT/'files/a/0/0/6').read_bytes()))==100
print(f'PASS {count} legal partner/opponent moves, 7 separate trainer records, native AI/Multi route and preserved graphics')
