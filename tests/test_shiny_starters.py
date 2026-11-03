"""Compile the unchanged native shiny generator/check against deterministic RNG inputs."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1];s=(root/'src/pokemon.c').read_text();gen=s[s.index('u32 GenerateShinyPersonality(u32 otid) {'):s.index('void GetPokemonSpriteCharAndPlttNarcIds')];macro=s[s.index('#define SHINY_CHECK'):s.index('#define SHINY_CHECK')+500].split('\n\n')[0]
gen=gen.replace('(r5 << 16)', '((u32)r5 << 16)') # Explicit native unsigned bit transport for host UBSan.
check=s[s.index('u8 CalcShininessByOtIdAndPersonality(u32 otid, u32 pid) {'):s.index('u32 GenerateShinyPersonality(u32 otid) {')]
original=subprocess.check_output(['git','show','bcf2f8fd:src/pokemon.c'],cwd=root).decode()
start='void CreateMon(Pokemon *mon,';end='void CreateMonWithNature('
assert s[s.index(start):s.index(end)]==original[original.index(start):original.index(end)]
assert (root/'src/field/encounter_check.c').read_bytes()==subprocess.check_output(['git','show','bcf2f8fd:src/field/encounter_check.c'],cwd=root)
# The native checker is an XOR of trainer ID halves and personality halves < 8.
preamble='''#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint32_t u32;typedef uint16_t u16;typedef uint8_t u8;
static u32 seed;static u32 LCRandom(void){seed=seed*0x41c64e6d+0x6073;return seed>>16;}
static u32 MaskOfFlagNo(int n){return 1u<<n;}
'''
main='''int main(void){unsigned id,sp,i;const unsigned species[]={152,155,158};for(sp=0;sp<3;sp++)for(i=0;i<100000;i++){seed=i*101+species[sp];id=seed*0xdeadbeef;unsigned p=GenerateShinyPersonality(id);assert(CalcShininessByOtIdAndPersonality(id,p));}unsigned shiny=0;for(i=0;i<65536;i++)if(CalcShininessByOtIdAndPersonality(0x1234abcdu,(i<<16)|0x4567u))shiny++;assert(shiny==8);puts("PASS 300000 native shiny-PID generations across all starter choices; ordinary XOR threshold remains 8/65536");}'''
with tempfile.TemporaryDirectory()as d:
 p=Path(d);(p/'test.c').write_text(preamble+macro+"\n"+check+gen+main);subprocess.run(['cc','-fsanitize=undefined','-fno-sanitize-recover=all','-O2',str(p/'test.c'),'-o',str(p/'test')],check=True);subprocess.run([str(p/'test')],check=True)
