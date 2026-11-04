"""Validate the joined/disabled sister conversation and native save compatibility."""
from pathlib import Path
import argparse,json,gzip,struct,binascii
from release_emulator_session import EmulatorSession,isolated_rom
from prepare_desmume_save import wrap_save
from inspect_story_pokemon import decode_mon
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
for name in ['core','rom','symbols','output']:p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
layout=json.loads((ROOT/'tests/fixtures/companion/save-layout.json').read_text());reports=[]
for joined in [True,False]:
    folder=a.output/('joined' if joined else 'disabled');rom=isolated_rom(a.rom,folder)
    raw=bytearray(gzip.decompress((ROOT/'tests/fixtures/release/goldenrod-after-eevee.sav.gz').read_bytes()))
    sectors=[base for base in [0,0x40000] if struct.unpack_from('<I',raw,base+0xf620)[0]==0x20060623]
    latest=max(sectors,key=lambda base:struct.unpack_from('<I',raw,base+0xf618)[0])
    assert raw[latest+layout['4']['offset']+0x2e0+362]&2  # The older backup can precede the event.
    for base in [0,0x40000]:
        if struct.unpack_from('<I',raw,base+0xf620)[0]!=0x20060623:continue
        start=base+layout['4']['offset'];flags=start+0x2e0
        raw[flags+363]=(raw[flags+363]&0x3f)|0x40|(0x80 if joined else 0)
        size=layout['4']['size'];struct.pack_into('<H',raw,start+size-4,binascii.crc_hqx(raw[start:start+size-4],65535));struct.pack_into('<H',raw,base+0xf626,binascii.crc_hqx(raw[base:base+0xf618],65535))
    fixture=folder/'input.sav';fixture.write_bytes(raw);wrap_save(fixture,rom.with_suffix('.dsv'))
    s=EmulatorSession(a.core,rom,a.symbols,folder,'conversation');g=s.boot_continue()['game']
    def flag(n):return bool(int(s.send({'read':[hex(int(g['flag_address'],16)+n//8),1]})['read'],16)&(1<<(n%8)))
    def mon():return decode_mon(bytes.fromhex(s.send({'read':[hex(int(g['party_address'],16)+8),236]})['read']))
    assert g['joined']==joined and any(o['id']==240 for o in g['objects']);bill_before=flag(0x95);pokemon_before=mon()
    s.send({'frames':8,'buttons':['A']});s.send({'frames':180,'shot':'sister-page-1.png'})
    s.send({'frames':8,'buttons':['A']});s.send({'frames':180,'shot':'sister-page-2.png'})
    s.send({'talk':30});s.send({'frames':48,'buttons':['DOWN']});s.send({'frames':48,'buttons':['LEFT']})
    g=s.send({'frames':180,'inspect':True,'shot':'after-conversation.png','expect':{'joined':joined,'counts':{'252':int(joined),'253':1}}})['game']
    assert flag(0xB51) and flag(0x95)==bill_before and mon()==pokemon_before
    s.save();s.close()
    s=EmulatorSession(a.core,rom,a.symbols,folder,'cold');g=s.boot_continue()['game']
    assert g['joined']==joined and flag(0xB51) and flag(0x95)==bill_before and mon()==pokemon_before;s.close()
    report={'joined':joined,'sister_Eevee_record_retained':True,'player_Bill_gift_flag_unchanged':True,
            'player_Pokemon_data_unchanged':True,'native_save_and_cold_Continue':'PASS',
            'expected_page_2':'Sabrina: A formidable opponent.' if joined else 'It looks so innocent while I trip over myself.',
            'scope':'Native post-Eevee conversation; joined status authored in older native save; screenshot review verifies selected text'}
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report);print(json.dumps(report),flush=True)
(a.output/'results.json').write_text(json.dumps(reports,indent=2)+'\n')
