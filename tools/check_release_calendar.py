"""Exercise native elapsed-day callbacks with explicitly authored clock fixtures."""
from pathlib import Path
import argparse,json,struct,binascii,gzip,hashlib
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for name in ['core','rom','symbols','output']:p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
layout=json.loads((ROOT/'tests/fixtures/companion/save-layout.json').read_text())
source=gzip.decompress((ROOT/'tests/fixtures/story/practice-victory.sav.gz').read_bytes());reports=[]
for days,joined in [(1,True),(8,False)]:
    folder=a.output/(str(days)+'-day');rom=isolated_rom(a.rom,folder);raw=bytearray(source)
    for base in [0,0x40000]:
        if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
        sysinfo=base+layout['0']['offset'];old_day=struct.unpack_from('<i',raw,sysinfo+48)[0]
        struct.pack_into('<i',raw,sysinfo+48,old_day-days)
        flags=base+layout['4']['offset']+0x2e0
        raw[flags+0x964//8]|=1<<(0x964%8)  # Native FLAG_GAME_CLEAR, authored fixture only.
        raw[flags+0xB49//8]|=1<<(0xB49%8)
        raw[flags+362]=255
        raw[flags+363]=(raw[flags+363]&0x3f)|0x40|(0x80 if joined else 0)
        # Authored post-Champion badge state tests retention, not campaign completion.
        profile=base+layout['1']['offset']+4;raw[profile+26]=255;raw[profile+31]=255;raw[profile+29]=1
        for block in [0,1,4]:
            start=base+layout[str(block)]['offset'];size=layout[str(block)]['size']
            struct.pack_into('<H',raw,start+size-4,binascii.crc_hqx(raw[start:start+size-4],65535))
        struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
    fixture=folder/'input.sav';fixture.write_bytes(raw);wrap_save(fixture,rom.with_suffix('.dsv'))
    def verify(session,shot):
        g=session.send({'frames':1,'inspect':True,'shot':shot})['game'];address=int(g['flag_address'],16)
        data=bytes.fromhex(session.send({'read':[hex(address+0xB48//8),3]})['read'])
        assert not data[0]&(1<<(0xB49%8)),'Native elapsed-day reset did not clear sentinel'
        assert data[1]==255 and data[2]&0xc0==(0xc0 if joined else 0x40)
        assert g['joined']==joined and g['initialized']
        native_clear=int(session.send({'read':[hex(address+0x964//8),1]})['read'],16)
        assert native_clear&(1<<(0x964%8))
        sd=int(g['save_address'],16);offset=int.from_bytes(bytes.fromhex(session.send({'read':[hex(sd+0x23014+16+8),4]})['read']),'little')
        profile=bytes.fromhex(session.send({'read':[hex(sd+16+offset+4),32]})['read'])
        assert profile[26]==255 and profile[31]==255 and profile[29]==1
        return {'custom_flag_bytes':data[1:].hex(),'joined':joined,'all_badges_and_game_clear_profile':True,'native_GAME_CLEAR_flag':True,'native_daily_sentinel_cleared':True}
    s=EmulatorSession(a.core,rom,a.symbols,folder,'calendar');s.boot_continue();first=verify(s,'calendar-loaded.png');s.save();s.close()
    saved=rom.with_suffix('.dsv').read_bytes();sectors=[b for b in [0,0x40000] if struct.unpack_from('<I',saved,b+0xf620)[0]==0x20060623];sector=max(sectors,key=lambda b:struct.unpack_from('<I',saved,b+0xf618)[0])
    assert binascii.crc_hqx(saved[sector:sector+0xf618],65535)==struct.unpack_from('<H',saved,sector+0xf626)[0]
    s=EmulatorSession(a.core,rom,a.symbols,folder,'calendar-cold');s.boot_continue();second=verify(s,'calendar-cold.png');assert second==first;s.close()
    report={'elapsed_days':days,'result':first,'native_save_CRC':'PASS','cold_Continue':'PASS','counter':struct.unpack_from('<I',saved,sector+0xf618)[0],
            'scope':'Stored day moved into past to exercise real calendar callbacks; post-Champion prerequisites authored; no runtime RAM writes'}
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report);print(json.dumps(report),flush=True)
(a.output/'results.json').write_text(json.dumps(reports,indent=2)+'\n')
