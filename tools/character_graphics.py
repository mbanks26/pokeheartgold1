#!/usr/bin/env python3
"""Convert indexed character PNGs without changing native resource metadata.

Requires Pillow. Uses the repository's nitrogfx for the existing NCER/OAM layout.
All binary replacements are length-preserving. No game code is patched.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = '3fea383f5a229391d12ef3429f8095177638a44d'
FRONT = 'files/a/0/5/8'
BACK = 'files/a/0/0/6'
MMODEL = 'files/data/mmodel/mmodel/mmodel_{:08d}.NSBTX'
CHARACTERS = {
    'sabrina': {'textures': [163], 'front': 107, 'back': []},
    'male': {'textures': [69], 'front': 0, 'back': [0, 15]},
    'female': {'textures': [70], 'front': 1, 'back': [1, 16]},
}

def original(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)

def u16(b, off):
    return struct.unpack_from('<H', b, off)[0]

def u32(b, off):
    return struct.unpack_from('<I', b, off)[0]

def digest(b):
    return hashlib.sha256(b).hexdigest()

def narc_ranges(b):
    assert b[:4] == b'NARC' and b[16:20] == b'BTAF'
    count = u16(b, 24)
    btnf = 16 + u32(b, 20)
    gmif = btnf + u32(b, btnf + 4)
    assert b[gmif:gmif+4] == b'GMIF'
    start = gmif + 8
    return [(start + u32(b, 28+8*i), start + u32(b, 32+8*i)) for i in range(count)]

def members(b):
    return [b[a:z] for a, z in narc_ranges(b)]

def patch_members(b, replacements):
    out = bytearray(b)
    for i, payload in replacements.items():
        a, z = narc_ranges(b)[i]
        assert z-a == len(payload), (i, z-a, len(payload))
        out[a:z] = payload
    assert len(out) == len(b)
    return bytes(out)

def palette_bytes(im):
    assert im.mode == 'P' and max(im.getdata()) < 16
    p = im.getpalette()
    words = [round(p[3*i]/255*31) | round(p[3*i+1]/255*31)<<5 |
             round(p[3*i+2]/255*31)<<10 for i in range(16)]
    return struct.pack('<16H', *words)

def packed4(im):
    p = list(im.getdata())
    assert len(p) % 2 == 0 and max(p) < 16
    return bytes(p[i] | p[i+1]<<4 for i in range(0, len(p), 2))

def dictionary_entries(b, off):
    count = b[off+1]
    table = off + 12 + 4*count
    stride = u16(b, table)
    entries = table + 4
    names = entries + stride*count
    return [(b[names+16*i:names+16*(i+1)].split(b'\0')[0].decode(),
             entries+stride*i) for i in range(count)]

def apply_overworld(name, texture_id):
    path = MMODEL.format(texture_id)
    b = original(path)
    out = bytearray(b)
    assert b[:4] == b'BTX0'
    tex0 = u32(b, 16)
    assert b[tex0:tex0+4] == b'TEX0'
    tex_dict = tex0 + u16(b, tex0+14)
    tex_data = tex0 + u32(b, tex0+20)
    pal_dict = tex0 + u32(b, tex0+52)
    pal_data = tex0 + u32(b, tex0+56)
    sheet = Image.open(ROOT/'characters'/name/'overworld.png')
    assert sheet.size == (128, 128) and sheet.info.get('transparency') == 0
    textures = dictionary_entries(b, tex_dict)
    assert len(textures) in (16, 32)
    changed = []
    for label, entry in textures:
        params = u16(b, entry+2)
        assert (params >> 10) & 7 == 3 and params & 0x2000
        assert 8 << ((params >> 4)&7) == 32
        assert 8 << ((params >> 7)&7) == 32
        frame = (int(label.rsplit('.', 1)[1])-1) % 16
        im = sheet.crop((frame%4*32, frame//4*32, frame%4*32+32, frame//4*32+32))
        off = tex_data + u16(b, entry)*8
        payload = packed4(im)
        out[off:off+512] = payload
        assert list(im.getdata()) == [v for x in payload for v in (x&15, x>>4)]
        changed.append(label)
    palettes = dictionary_entries(b, pal_dict)
    assert len(palettes) == 1
    off = pal_data + u16(b, palettes[0][1])*8
    out[off:off+32] = palette_bytes(sheet)
    assert len(out) == len(b)
    (ROOT/path).write_bytes(out)
    return {'path': path, 'frames': changed, 'sha256': digest(out)}

def encrypt_portrait(raw, template):
    # DP-style backward scan is required for BOTH trainer portrait archives.
    # The final plaintext word is reserved for the stream seed and must be zero.
    assert raw[-2:] == b'\0\0' and len(raw) == 6400
    seed = u16(template, len(template)-2)
    encoded = bytearray(raw)
    for i in range(len(raw)-2, -1, -2):
        struct.pack_into('<H', encoded, i, u16(raw, i) ^ (seed & 65535))
        seed = (seed*1103515245 + 24691) & 0xffffffff
    decoded = bytearray(encoded)
    seed = u16(encoded, len(encoded)-2)
    for i in range(len(encoded)-2, -1, -2):
        struct.pack_into('<H', decoded, i, u16(encoded, i) ^ (seed & 65535))
        seed = (seed*1103515245 + 24691) & 0xffffffff
    assert decoded == raw
    return template[:48] + encoded

def apply_battle(name, archive, cls, direction, build):
    current = (ROOT/archive).read_bytes()
    stock = members(original(archive))
    offset = cls*5
    ncgr, nclr, ncer, nanr, ncbr = stock[offset:offset+5]
    im = Image.open(ROOT/'characters'/name/('battle-'+direction+'.png'))
    assert im.width == 80 and im.height % 80 == 0
    gfx = ROOT/build/'tools/nitrogfx/nitrogfx'
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        (temp/'layout.NCER').write_bytes(ncer)
        subprocess.run([str(gfx),str(temp/'layout.NCER'),str(temp/'layout.json')],check=True)
        layout = json.loads((temp/'layout.json').read_text())
        count = layout['cellCount']
        assert im.height == 80*count
        atlas = Image.new('P', (80,81*count-1), 0)
        atlas.putpalette(im.getpalette())
        for i in range(count):
            atlas.paste(im.crop((0,i*80,80,(i+1)*80)), (0,i*81))
        atlas.save(temp/'atlas.png',bits=4)
        subprocess.run([str(gfx),str(temp/'atlas.png'),str(temp/'result.NCGR'),
                        '-cell',str(temp/'layout.json'),'-clobbersize','-version101',
                        '-mappingtype','64','-vram'],check=True)
        generated = (temp/'result.NCGR').read_bytes()
        assert len(generated) == len(ncgr)
        generated = ncgr[:48] + generated[48:]
        pal = bytearray(nclr)
        pal[40:72] = palette_bytes(im)
        (temp/'result.NCGR').write_bytes(generated)
        (temp/'result.NCLR').write_bytes(pal)
        subprocess.run([str(gfx),str(temp/'result.NCGR'),str(temp/'decoded.png'),
                        '-palette',str(temp/'result.NCLR'),'-cell',str(temp/'layout.json')],check=True)
        decoded = Image.open(temp/'decoded.png')
        for i in range(count):
            region=(0,i*81,80,i*81+80)
            assert list(decoded.crop(region).getdata()) == list(atlas.crop(region).getdata()), 'NCGR/OAM roundtrip failed'
        portrait = Image.new('P',(160,80),0)
        portrait.putpalette(im.getpalette())
        for i in range(2):
            frame = min(i, count-1)
            portrait.paste(im.crop((0,frame*80,80,(frame+1)*80)), (i*80,0))
        portrait_data = encrypt_portrait(packed4(portrait), ncbr)
        replacements = {offset:generated,offset+1:bytes(pal),offset+4:portrait_data}
        updated = patch_members(current, replacements)
        after = members(updated)
        before = members(current)
        assert all(a==b for i,(a,b) in enumerate(zip(before,after)) if i not in replacements)
        assert after[offset+2] == ncer and after[offset+3] == nanr
        (ROOT/archive).write_bytes(updated)
        return {'archive': archive, 'class': cls, 'frames': count,
                'changed_members': sorted(replacements), 'NCER_NANR_preserved': True,
                'NCGR_roundtrip': True, 'portrait_encryption_roundtrip': True}

def rom_files(b):
    fnt, fnt_size, fat, fat_size = struct.unpack_from('<4I', b, 0x40)
    result = {}
    def walk(directory, prefix):
        entry = fnt + (directory-0xf000)*8
        table, file_id = struct.unpack_from('<IH', b, entry)
        pos = fnt+table
        while b[pos]:
            length = b[pos];pos += 1
            name = b[pos:pos+(length&127)].decode('ascii');pos += length&127
            if length&128:
                child = u16(b,pos);pos += 2;walk(child,prefix+name+'/')
            else:
                result[prefix+name] = struct.unpack_from('<II',b,fat+file_id*8)
                file_id += 1
    walk(0xf000,'')
    return result

def verify(stock_path, modified_path, stages):
    stock = stock_path.read_bytes(); modified = modified_path.read_bytes()
    assert hashlib.sha1(stock).hexdigest() == '4fcded0e2713dc03929845de631d0932ea2b5a37'
    assert len(stock) == len(modified) == 134217728
    fs = rom_files(stock); assert fs == rom_files(modified), 'Filesystem offsets changed'
    changed = [p for p,(a,z) in fs.items() if stock[a:z] != modified[a:z]]
    allowed = {'a/0/8/1','a/0/5/8'}
    if any(n!='sabrina' for n in stages): allowed.add('a/0/0/6')
    assert set(changed) == allowed, changed
    a = bytearray(stock);b = bytearray(modified)
    for path in allowed:
        start,end = fs[path];a[start:end]=b'\0'*(end-start);b[start:end]=b'\0'*(end-start)
    assert a == b, 'A byte outside the allowed graphics archives changed'
    expected_tex = {i for n in stages for i in CHARACTERS[n]['textures']}
    start,end = fs['a/0/8/1']
    original_mm = members(stock[start:end]);custom_mm = members(modified[start:end])
    actual_tex = {i for i,(a,b) in enumerate(zip(original_mm,custom_mm)) if a!=b}
    assert actual_tex == expected_tex, (actual_tex, expected_tex)
    for path,key in [('a/0/5/8','front'),('a/0/0/6','back')]:
        if path not in allowed:continue
        start,end=fs[path];a=members(stock[start:end]);b=members(modified[start:end])
        classes = [CHARACTERS[n]['front'] for n in stages] if key=='front' else [i for n in stages for i in CHARACTERS[n]['back']]
        expect={i*5+j for i in classes for j in (0,1,4)}
        actual={i for i,(x,y) in enumerate(zip(a,b)) if x!=y}
        assert actual==expect,(path,actual,expect)
    return {'stages': stages, 'rom_sha1':hashlib.sha1(modified).hexdigest(),
            'rom_size':len(modified), 'changed_files':changed,
            'changed_overworld_members':sorted(actual_tex),
            'all_other_ROM_bytes_identical_to_stock':True,
            'gameplay_story_naming_following_Pokemon_unchanged':True,
            'emulator_gameplay_tested':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    apply=sub.add_parser('apply');apply.add_argument('character',choices=CHARACTERS)
    apply.add_argument('--build',default='build/recovery-verification')
    check=sub.add_parser('verify');check.add_argument('--stock',type=Path,required=True)
    check.add_argument('--rom',type=Path,required=True);check.add_argument('--stages',nargs='+',required=True,choices=CHARACTERS)
    check.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    if args.command=='apply':
        cfg=CHARACTERS[args.character]
        report={'character':args.character,'overworld':[apply_overworld(args.character,i) for i in cfg['textures']]}
        report['battle']=[apply_battle(args.character,FRONT,cfg['front'],'front',args.build)]
        report['battle'] += [apply_battle(args.character,BACK,i,'back',args.build) for i in cfg['back']]
        (ROOT/'characters'/args.character/'conversion.json').write_text(json.dumps(report,indent=2)+'\n')
    else:
        report=verify(args.stock,args.rom,args.stages);args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
