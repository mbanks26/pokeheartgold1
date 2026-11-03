"""Exercise actual context selection and input guards with engine stubs."""
from pathlib import Path
import subprocess,tempfile,os,json,re
ROOT=Path(__file__).resolve().parents[1]
code='\n'.join(x for x in (ROOT/'src/field/sabrina_dialogue.inc').read_text().splitlines()if not x.startswith('#include'))
headers=''.join('#include "constants/'+x+'.h"\n' for x in ['flags','vars','badge','player_avatar','global_fieldmap','map_sections','std_script','sabrina_story'])
stub=r'''
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
typedef int BOOL;typedef unsigned short u16;
#define TRUE 1
#define FALSE 0
#define PAD_BUTTON_SELECT 4
#define PAD_PLUS_KEY_MASK 240
#define SABRINA_COMPANION_OBJECT_ID 252
typedef struct {unsigned char bits[364];u16 vars[368];} SaveVarsFlags;
typedef struct {unsigned badges;} PlayerProfile;
typedef struct {SaveVarsFlags flags;PlayerProfile profile;int joined;} SaveData;
typedef struct {int state;} Avatar;
typedef struct {int present,foreign;} Manager;
typedef struct {int mapId;} Location;
typedef struct {SaveData *saveData;Avatar *playerAvatar;Manager *mapObjectManager;Location *location;} FieldSystem;
typedef struct {unsigned newKeys,heldKeys;int unk0_8;} FieldInput;
static int section,scheduled;static SaveVarsFlags *Save_VarsFlags_Get(SaveData*s){return &s->flags;}
static PlayerProfile *Save_PlayerData_GetProfile(SaveData*s){return &s->profile;}
static int PlayerProfile_TestBadgeFlag(PlayerProfile*p,int n){return !!(p->badges&(1u<<n));}
static int Save_VarsFlags_CheckFlagInArray(SaveVarsFlags*f,int n){return !!(f->bits[n/8]&(1<<(n%8)));}
static u16 *Save_VarsFlags_GetVarAddr(SaveVarsFlags*f,int n){return &f->vars[n-0x4000];}
static int MapHeader_GetMapSec(int map){return section;}
static int PlayerAvatar_GetState(Avatar*a){return a->state;}
static int SabrinaCompanion_IsJoined(SaveData*s){return s->joined;}
static Manager *MapObjectManager_GetFirstActiveObjectByID(Manager*m,int id){return m->present?m:NULL;}
static int SabrinaCompanion_IsSolid(Manager*m){return m->foreign;}
static void StartMapSceneScript(FieldSystem*f,int script,void*actor){assert(script==std_sabrina_conversation&&actor==NULL);scheduled++;}
'''
test=r'''
#define CHECK(x) do{n++;assert(x);}while(0)
static void flag(SaveData*s,int f){s->flags.bits[f/8]|=1<<(f%8);}
int main(void){int n=0;SaveData s={0};Avatar a={0};Manager m={1,0};Location l={60};FieldSystem f={&s,&a,&m,&l};FieldInput in={4,0,1};
section=MAPSEC_NEW_BARK_TOWN;CHECK(!SabrinaStory_TryConversation(&f,&in));s.joined=1;CHECK(SabrinaStory_TryConversation(&f,&in));CHECK(scheduled==1&&s.flags.vars[0x16e]==MSG_SABRINA_CONTEXT_BASE);
in.heldKeys=16;CHECK(!SabrinaStory_TryConversation(&f,&in));in.heldKeys=0;m.foreign=1;CHECK(!SabrinaStory_TryConversation(&f,&in));m.foreign=0;m.present=0;CHECK(!SabrinaStory_TryConversation(&f,&in));m.present=1;a.state=1;CHECK(!SabrinaStory_TryConversation(&f,&in));a.state=0;in.unk0_8=0;CHECK(!SabrinaStory_TryConversation(&f,&in));in.unk0_8=1;in.newKeys=0;CHECK(!SabrinaStory_TryConversation(&f,&in));
section=MAPSEC_VIOLET_CITY;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+2);s.profile.badges|=1<<BADGE_ZEPHYR;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+3);
section=MAPSEC_GOLDENROD_CITY;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+6);flag(&s,FLAG_BEAT_RADIO_TOWER_ROCKETS);CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+7);
section=MAPSEC_MAHOGANY_TOWN;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+11);flag(&s,FLAG_ROCKET_HIDEOUT_CLEARED);CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+12);
section=MAPSEC_INDIGO_PLATEAU;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+15);flag(&s,FLAG_GAME_CLEAR);CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+16);
section=MAPSEC_SAFFRON_CITY;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+17);s.profile.badges|=1<<BADGE_MARSH;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+18);
section=MAPSEC_CHERRYGROVE_CITY;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+1);s.flags.vars[VAR_SCENE_CHERRYGROVE_CITY_OW-0x4000]=4;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+25);
section=MAPSEC_ECRUTEAK_CITY;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+8);s.flags.vars[VAR_UNK_40A1-0x4000]=1;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+26);
section=MAPSEC_LAKE_OF_RAGE;CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+23);flag(&s,FLAG_CAUGHT_RED_GYARADOS);CHECK(SabrinaStory_Dialogue(&f)==MSG_SABRINA_CONTEXT_BASE+27);printf("PASS %d context/input assertions (host engine stubs)\n",n);}
'''
with tempfile.TemporaryDirectory()as d:
 p=Path(d);(p/'test.c').write_text(headers+stub+code+test);subprocess.run(['cc','-iquote',str(ROOT/'include'),'-fsanitize=address,undefined','-O1',str(p/'test.c'),'-o',str(p/'test')],check=True);subprocess.run([str(p/'test')],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
original=json.loads(subprocess.check_output(['git','show','bcf2f8fd:files/msgdata/msg/msg_0040.json'],cwd=ROOT));current=json.loads((ROOT/'files/msgdata/msg/msg_0040.json').read_text());assert current['messages'][:117]==original['messages']
for m in current['messages'][117:]:
 for page in m['en_US'].split('\r'):
  assert len(page.split('\n'))<=2
  for line in page.split('\n'):assert len(re.sub(r'\{[^}]+\}','ABCDEFG',line))<=32
print('PASS new conversation pagination and original common-text preservation')
