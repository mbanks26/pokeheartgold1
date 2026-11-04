"""Drive native practice/victory/save/Continue in an isolated authored fixture.

No battle Pokemon or results are written by this driver. Its player chooses
Crunch; Sabrina's actions are native AI. Requires companion_emulator_runner,
DeSmuME libretro, matching ROM/symbols, and a prepared post-Marsh Saffron save.
"""
from pathlib import Path
import argparse,json,subprocess,sys,struct,binascii,atexit
from prepare_desmume_save import wrap_save

p=argparse.ArgumentParser();p.add_argument('--core',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--symbols',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--save-fixture',type=Path,help='Raw .sav or .sav.gz; requires a separate ROM path without an existing .dsv');a=p.parse_args()
ROOT=Path(__file__).resolve().parents[1];out=a.output.resolve();out.mkdir(exist_ok=True)
if a.save_fixture:
    (out/'save-import.json').write_text(json.dumps(wrap_save(a.save_fixture,a.rom.with_suffix('.dsv')),indent=2)+'\n')

def launch(label):
    proc=subprocess.Popen([sys.executable,'-u',str(ROOT/'tools/companion_emulator_runner.py'),'--core',str(a.core),'--rom',str(a.rom),'--symbols',str(a.symbols),'--output',str(out)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
    def cleanup():
        if proc.poll() is None:
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=10)
    atexit.register(cleanup)
    log=(out/(label+'.stdout.log')).open('w')
    def response(ready=False):
        while True:
            line=proc.stdout.readline()
            if not line:raise RuntimeError('Emulator closed unexpectedly: '+str(proc.poll()))
            log.write(line);log.flush()
            try:r=json.loads(line)
            except json.JSONDecodeError:continue
            if 'failed'in r:raise AssertionError(r['failed'])
            if (ready and r.get('ready'))or(not ready and 'frame'in r):return r
    response(True)
    def send(c):
        proc.stdin.write(json.dumps(c)+'\n');proc.stdin.flush();return response()
    return proc,log,send

def boot(send):
    for c in [{'frames':600},{'frames':3,'buttons':['A']},{'frames':180},{'frames':3,'buttons':['A']},{'frames':300},{'frames':8,'buttons':['A']},{'frames':600}]:send(c)

def close(proc,log,send):
    send({'exit':True});proc.wait(timeout=30);log.close();assert proc.returncode==0

def won(send):
    g=send({'frames':1,'inspect':True})['game']
    assert 'flag_address' in g,'No field save loaded; use --save-fixture to import raw SAV with its required DSV footer'
    addr=int(g['flag_address'],16)+0xb54//8
    return bool(int(send({'read':[hex(addr),1]})['read'],16)&0x10)

def formation(send,shot):
    send({'talk':20,'button':'B'})
    for c in [{'frames':32,'buttons':['DOWN']},{'frames':64,'buttons':['LEFT']},{'frames':120}]:send(c)
    return send({'frames':1,'inspect':True,'shot':shot,'expect':{'joined':True,'avatar_state':0,'counts':{'252':1,'253':1}}})

proc,log,send=launch('practice');boot(send);assert not won(send)
for direction in ['DOWN','LEFT','UP','RIGHT']:send({'frames':16,'buttons':[direction]})
send({'frames':180,'inspect':True,'shot':'practice-native-formation.png'})
send({'frames':8,'buttons':['A']});send({'frames':180,'shot':'practice-offer.png'});send({'talk':6});send({'frames':900,'shot':'practice-native-battle.png','dump':'practice-native-battle.bin'})
for turn in range(12):
    if won(send):break
    # Reset a pending target/move menu, then issue only the player's command.
    for c in [{'frames':8,'buttons':['B']},{'frames':90},{'frames':8,'buttons':['B']},{'frames':90},{'frames':2,'touch':[128,80]},{'frames':180},{'frames':2,'touch':[60,45]},{'frames':180},{'frames':2,'touch':([192,45]if turn%2==0 else[60,45])},{'frames':3600,'shot':f'practice-turn-{turn+1}.png'}]:send(c)
assert won(send),'Practice did not complete within the bounded native UI scenario'
formation(send,'practice-victory-formation.png');send({'frames':1,'dump':'practice-victory.bin','state':'practice-victory.state'})
for c in [{'frames':8,'buttons':['X']},{'frames':180},{'frames':2,'touch':[128,74]},{'frames':360,'shot':'practice-save-confirmation.png'},{'frames':8,'buttons':['A']},{'frames':360},{'frames':8,'buttons':['A']},{'frames':2400},{'frames':8,'buttons':['B']},{'frames':180},{'frames':8,'buttons':['B']},{'frames':180}]:send(c)
close(proc,log,send)
raw=a.rom.with_suffix('.dsv').read_bytes();layout=json.loads((ROOT/'tests/fixtures/companion/save-layout.json').read_text());sectors=[s for s in[0,0x40000]if struct.unpack_from('<I',raw,s+0xf620)[0]==0x20060623];sector=max(sectors,key=lambda s:struct.unpack_from('<I',raw,s+0xf618)[0]);assert binascii.crc_hqx(raw[sector:sector+0xf618],65535)==struct.unpack_from('<H',raw,sector+0xf626)[0]
flags=sector+layout['4']['offset']+0x2e0;assert raw[flags+362]&0x10 and raw[flags+363]&0x80
proc,log,send=launch('cold-continue');boot(send);assert won(send);formation(send,'practice-cold-continued-formation.png');send({'frames':1,'dump':'practice-cold-continue.bin'});close(proc,log,send)
result={'native_Multi_victory':True,'native_battery_save_CRC':'PASS','saved_practice_flag_B54':True,'saved_joined_B5F':True,'counter':struct.unpack_from('<I',raw,sector+0xf618)[0],'cold_Continue_and_single_follower_objects':'PASS','player_commands':'Crunch only; no commands for Sabrina'}
(out/'roundtrip-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
