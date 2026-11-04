"""Exercise the actual RTC reset policy; no engine or emulator is stubbed as tested."""
from pathlib import Path
import re,subprocess,tempfile,os
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'src/script_manager.c').read_text().split('void ClearDailyFlags(FieldSystem *fieldSystem) {',1)[1].split('\n}',1)[0]
flags=(ROOT/'include/constants/flags.h').read_text()
defines='\n'.join(x for x in flags.splitlines()if re.match(r'#define (DAILY_FLAG_BASE|NUM_DAILY_FLAGS|FLAG_SABRINA_STORY_INTRO_DONE)\b',x))
c='''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;
typedef struct { u8 flags[364]; } SaveVarsFlags;
typedef struct { SaveVarsFlags *saveData; } FieldSystem;
SaveVarsFlags *Save_VarsFlags_Get(SaveVarsFlags *p){return p;}
u8 *Save_VarsFlags_GetFlagAddr(SaveVarsFlags *p,unsigned flag){return &p->flags[flag/8];}
'''+defines+'\nvoid ClearDailyFlags(FieldSystem *fieldSystem) {'+source+'\n}\n'+'''
int main(void){
  unsigned n=0;
  for(unsigned tail=0;tail<256;tail++)for(unsigned seed=0;seed<32;seed++){
    SaveVarsFlags s,before;FieldSystem fs={&s};
    for(unsigned i=0;i<364;i++)s.flags[i]=(i*73+seed*41)&255;
    s.flags[363]=tail;before=s;ClearDailyFlags(&fs);
    for(unsigned i=0;i<340;i++)assert(s.flags[i]==before.flags[i]);
    for(unsigned i=340;i<362;i++)assert(s.flags[i]==0);
    assert(s.flags[362]==before.flags[362]);
    assert(s.flags[363]==(tail&0xe0));n++;
    ClearDailyFlags(&fs);assert(s.flags[362]==before.flags[362]);assert(s.flags[363]==(tail&0xe0));
  }
  printf("PASS %u native daily-reset cases: story, joined/deactivated status and female guard persist; ordinary daily flags clear\\n",n);
}
'''
with tempfile.TemporaryDirectory()as d:
    p=Path(d);(p/'test.c').write_text(c)
    subprocess.run(['cc','-fsanitize=address,undefined','-O1',str(p/'test.c'),'-o',str(p/'test')],check=True)
    subprocess.run([str(p/'test')],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
