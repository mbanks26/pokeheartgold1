"""Validate native fixture integrity, DSV metadata and non-overwrite behavior."""
from pathlib import Path
import gzip,sys,tempfile,struct
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from prepare_desmume_save import wrap_save,NOTICE,COOKIE,SIZE
fixture=ROOT/'tests/fixtures/story/practice-input.sav.gz'
with tempfile.TemporaryDirectory() as folder:
    out=Path(folder)/'fixture.dsv';result=wrap_save(fixture,out)
    raw=gzip.decompress(fixture.read_bytes());wrapped=out.read_bytes()
    assert wrapped[:SIZE]==raw and result['valid_sectors']
    assert wrapped[SIZE:SIZE+len(NOTICE)]==NOTICE
    assert struct.unpack_from('<6I',wrapped,SIZE+len(NOTICE))==(SIZE,SIZE,6,3,SIZE,0)
    assert wrapped.endswith(COOKIE)
    try:wrap_save(fixture,out)
    except FileExistsError:pass
    else:raise AssertionError('Existing save overwritten')
    assert out.read_bytes()==wrapped
    bad=Path(folder)/'bad.sav';bad.write_bytes(bytes(SIZE))
    try:wrap_save(bad,Path(folder)/'bad.dsv')
    except ValueError:pass
    else:raise AssertionError('Invalid save accepted')
    assert not (Path(folder)/'bad.dsv').exists()
print('PASS raw-save CRC validation, DSV footer and refusal to overwrite saves')
