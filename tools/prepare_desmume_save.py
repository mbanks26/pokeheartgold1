"""Wrap a verified HeartGold battery save for DeSmuME; never replace a save.

The libretro core expects its DSV footer. Renaming a raw SAV to DSV can make
the core silently autodetect an empty cartridge instead of importing it.
"""
from pathlib import Path
import argparse
import binascii
import gzip
import hashlib
import struct

NOTICE = b'|<--Snip above here to create a raw sav by excluding this DeSmuME savedata footer:'
COOKIE = b'|-DESMUME SAVE-|'
SIZE = 512 * 1024


def wrap_save(source: Path, output: Path):
    raw = source.read_bytes()
    if source.suffix == '.gz':
        raw = gzip.decompress(raw)
    if len(raw) != SIZE:
        raise ValueError('Expected a raw 512 KiB HeartGold battery save')
    valid = []
    for sector in (0, 0x40000):
        magic = struct.unpack_from('<I', raw, sector + 0xf620)[0]
        checksum = struct.unpack_from('<H', raw, sector + 0xf626)[0]
        if magic == 0x20060623 and binascii.crc_hqx(raw[sector:sector + 0xf618], 65535) == checksum:
            valid.append(sector)
    if not valid:
        raise ValueError('No valid native main-save sector; refusing to use fixture')
    # Native mc.cpp footer: data size, padded size, FLASH 4Mbit type (6),
    # address width (3), memory size, format version (0), recognition cookie.
    footer = NOTICE + struct.pack('<6I', SIZE, SIZE, 6, 3, SIZE, 0) + COOKIE
    with output.open('xb') as handle:
        handle.write(raw + footer)
    return {'raw_sha256': hashlib.sha256(raw).hexdigest(), 'valid_sectors': valid,
            'raw_bytes': len(raw), 'dsv_bytes': SIZE + len(footer)}


if __name__ == '__main__':
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    print(json.dumps(wrap_save(args.source, args.output)))
