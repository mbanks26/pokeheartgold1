"""Compile and exercise the actual controller/persistence/presentation code on host.

Engine calls are stubs; these are not emulator or visual-gameplay assertions.
Only the ARM32 integer/pointer transport is widened for the host ABI.
"""
from pathlib import Path
import subprocess,tempfile,os
ROOT=Path(__file__).resolve().parents[1]
def without_includes(text):
    return '\n'.join(x for x in text.splitlines() if not x.startswith('#include'))
header=without_includes((ROOT/'include/sabrina_companion.h').read_text())
header+='\n'+'\n'.join(line for line in (ROOT/'include/constants/flags.h').read_text().splitlines() if line.startswith('#define FLAG_SABRINA_COMPANION_'))
header+='\n'+'\n'.join(line for line in (ROOT/'include/constants/sabrina_story.h').read_text().splitlines() if line.startswith('#define FLAG_'))
trail=without_includes((ROOT/'include/sabrina_companion_trail.h').read_text())
policy=(ROOT/'src/pokemon.c').read_text().split('/* Presentation only:')[1].split('int TrainerClassToBackpicID(int trainerClass')[0]
policy='/* Presentation only:'+policy
controller=without_includes((ROOT/'src/field/sabrina_companion.inc').read_text()).replace('(int)&heightDelta','(intptr_t)&heightDelta')
serialization=(ROOT/'src/map_object.c').read_text().split('void FieldSystem_SyncMapObjectsToSaveEx(')[1].split('void MapObjectManager_RestoreFromSave(')[0]
serialization='void FieldSystem_SyncMapObjectsToSaveEx('+serialization
stub=r'''
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef unsigned u32; typedef int s32; typedef signed char s8; typedef int BOOL; typedef int MapObjectFlagBits;
#define TRUE 1
#define FALSE 0
#define FX32_ONE 4096
#define SPRITE_GSLEADER10 369
#define PLAYER_GENDER_MALE 0
#define PLAYER_STATE_WALKING 0
#define MAP_NOTHING 1
#define MAP_SAFFRON_GYM 410
#define MOVEMENT_RUN_UP 16
#define DIR_NORTH 0
#define DIR_SOUTH 1
#define DIR_WEST 2
#define DIR_EAST 3
#define MAPOBJECTFLAG_ACTIVE 1
#define MAPOBJECTFLAG_UNK13 8192
#define MAPOBJECTFLAG_UNK8 256
#define MAPOBJECTFLAG_UNK7 128
#define HIDDEN 512
#define BATTLE_TYPE_DOUBLES 2
#define BATTLE_TYPE_LINK 4
#define BATTLE_TYPE_MULTI 8
#define BATTLE_TYPE_FRONTIER 128
#define BATTLE_TYPE_TUTORIAL 1024
#define TRAINER_LEADER_SABRINA_SABRINA 258
#define TRAINER_LEADER_SABRINA_SABRINA_2 725
typedef struct {int x,y,z;} VecFx32;
typedef struct Obj {int x,y,z,px,py,pz,dir,id,sprite,script,map,flags,busy,paused,keep;} LocalMapObject;
typedef struct {LocalMapObject objects[12];} MapObjectManager;
typedef struct {unsigned char bits[364];} SaveVarsFlags;
typedef struct SaveData {SaveVarsFlags flags;int gender,partyCount;} SaveData;
typedef SaveData PlayerProfile; typedef SaveData Party;
typedef struct {int gender,state,x,z;LocalMapObject *object;} Avatar;
typedef struct {int count,ids[24];} Preload;
typedef struct {u32 mapId;} Location;
typedef struct FieldSystem {MapObjectManager *mapObjectManager;Avatar *playerAvatar;Preload *mapObjectsToPreload;Location *location;SaveData *saveData;} FieldSystem;
static MapObjectManager manager;static SaveData save;static Avatar avatar;static Preload preload;static Location location;static FieldSystem fs;
static int monActive,task,createFail,terrainBlocked,heightDelta,nativeBlocked,steps,warps,creates,deletes,lastCommand,checks;
#define CHECK(c) do{checks++;assert(c);}while(0)
static SaveVarsFlags *Save_VarsFlags_Get(SaveData*s){return &s->flags;}
static BOOL Save_VarsFlags_CheckFlagInArray(SaveVarsFlags*f,int id){assert(id<2912);return !!(f->bits[id/8]&(1<<(id%8)));}
static void Save_VarsFlags_SetFlagInArray(SaveVarsFlags*f,int id){assert(id<2912);f->bits[id/8]|=1<<(id%8);}
static void Save_VarsFlags_ClearFlagInArray(SaveVarsFlags*f,int id){assert(id<2912);f->bits[id/8]&=~(1<<(id%8));}
static PlayerProfile *Save_PlayerData_GetProfile(SaveData*s){return s;}
static int PlayerProfile_GetTrainerGender(PlayerProfile*p){return p->gender;}
static Party *SaveArray_Party_Get(SaveData*s){return s;}
static int Party_GetCount(Party*p){return p->partyCount;}
#define GET(name,field) static u32 name(LocalMapObject*o){return o->field;}
GET(MapObject_GetID,id) GET(MapObject_GetSpriteID,sprite) GET(MapObject_GetScriptID,script) GET(MapObject_GetMapID,map)
GET(MapObject_GetXCoord,x) GET(MapObject_GetZCoord,z) GET(MapObject_GetPreviousXCoord,px) GET(MapObject_GetPreviousYCoord,py) GET(MapObject_GetPreviousZCoord,pz) GET(MapObject_GetFacingDirection,dir)
static s32 MapObject_GetYCoord(LocalMapObject*o){return o->y;}
static BOOL MapObjectManager_GetNextObjectWithFlagFromIndex(MapObjectManager*m,LocalMapObject**p,s32*i,int flags){while(*i<12){LocalMapObject*o=&m->objects[(*i)++];if(o->flags&flags){*p=o;return 1;}}return 0;}
static LocalMapObject *MapObjectManager_GetFirstActiveObjectByID(MapObjectManager*m,u32 id){int i;for(i=0;i<12;i++)if((m->objects[i].flags&1)&&m->objects[i].id==id)return &m->objects[i];return NULL;}
static LocalMapObject *MapObject_CreateWithID(MapObjectManager*m,u32 id,u32 x,u32 z,u32 d,u32 sprite,u32 movement,u32 map){int i;if(createFail)return NULL;for(i=2;i<12;i++)if(!(m->objects[i].flags&1)){LocalMapObject*o=&m->objects[i];memset(o,0,sizeof(*o));o->id=id;o->x=x;o->z=z;o->dir=d;o->sprite=sprite;o->map=map;o->flags=1;creates++;return o;}return NULL;}
static void MapObject_Delete(LocalMapObject*o){o->flags=0;deletes++;}
#define SET(name,field) static void name(LocalMapObject*o,u32 v){o->field=v;}
SET(MapObject_SetID,id) SET(MapObject_SetScriptID,script)
static void MapObject_SetOrQueueFacing(LocalMapObject*o,u32 v){o->dir=v;}
static void MapObject_SetType(LocalMapObject*o,u32 v){}
static void MapObject_SetEventFlag(LocalMapObject*o,u32 v){}
static void MapObject_SetKeep(LocalMapObject*o,BOOL v){o->keep=v;}
static void MapObject_SetXRange(LocalMapObject*o,int v){}
static void MapObject_SetYRange(LocalMapObject*o,int v){}
static void MapObject_SetFlag29(LocalMapObject*o,BOOL v){}
static void MapObject_SetFlagsBits(LocalMapObject*o,int v){o->flags|=v;}
static void MapObject_ClearFlagsBits(LocalMapObject*o,int v){o->flags&=~v;}
static void MapObject_ClearFlag18(LocalMapObject*o,BOOL v){if(!v)o->flags|=1<<18;else o->flags&=~(1<<18);}
static void MapObject_SetFlag19(LocalMapObject*o,BOOL v){if(v)o->flags|=1<<19;else o->flags&=~(1<<19);}
/* Match native hidden-bit semantics, not the old prototype's incorrect stub. */
static void MapObject_SetVisible(LocalMapObject*o,BOOL v){if(v)o->flags|=HIDDEN;else o->flags&=~HIDDEN;}
static BOOL MapObject_CheckVisible(LocalMapObject*o){return !!(o->flags&HIDDEN);}
static BOOL MapObject_CheckMovementPaused(LocalMapObject*o){return o->paused;}
static BOOL MapObject_CheckSingleMovement(LocalMapObject*o){return o->busy;}
static BOOL MapObject_ClearHeldMovementIfActive(LocalMapObject*o){return !o->busy;}
static void MapObject_SetHeldMovement(LocalMapObject*o,u32 cmd){steps++;lastCommand=cmd;o->px=o->x;o->pz=o->z;o->busy=1;switch(cmd-16){case 0:o->z--;break;case 1:o->z++;break;case 2:o->x--;break;case 3:o->x++;break;}}
static void MapObject_SetPositionFromXYZAndDirection(LocalMapObject*o,u32 x,u32 y,u32 z,u32 d){o->x=x;o->y=y;o->z=z;o->dir=d;warps++;}
static BOOL FieldSystem_TaskIsRunning(FieldSystem*f){return task;}
static BOOL FollowMon_IsActive(FieldSystem*f){return monActive;}
static LocalMapObject *FollowMon_GetMapObject(FieldSystem*f){return &f->mapObjectManager->objects[1];}
static BOOL FollowMon_IsVisible(FieldSystem*f){return monActive&&!MapObject_CheckVisible(FollowMon_GetMapObject(f));}
static u32 PlayerAvatar_GetGender(Avatar*a){return a->gender;}
static u32 PlayerAvatar_GetState(Avatar*a){return a->state;}
static LocalMapObject *PlayerAvatar_GetMapObject(Avatar*a){return a->object;}
static BOOL sub_020549A8(FieldSystem*f,VecFx32*p,int x,int z,intptr_t output){*(s8*)output=heightDelta;return terrainBlocked;}
static u32 sub_02060BB8(LocalMapObject*o,u32 direction){return nativeBlocked;}
'''
save_stub=r'''
#define GF_ASSERT assert
typedef struct {int objId;} SavedMapObject;
static void SavedMapObject_InitFromLocalMapObject(FieldSystem*f,LocalMapObject*o,SavedMapObject*s){s->objId=o->id;}
'''
tests=r'''
static LocalMapObject *companion(void){return MapObjectManager_GetFirstActiveObjectByID(&manager,252);}
static void tick(int n){while(n--)SabrinaCompanion_Tick(&fs);}
static void fresh(void){
 memset(&manager,0,sizeof(manager));memset(&save,0,sizeof(save));memset(&avatar,0,sizeof(avatar));memset(&preload,0,sizeof(preload));
 manager.objects[0]=(LocalMapObject){.x=10,.z=11,.id=255,.flags=1};
 manager.objects[1]=(LocalMapObject){.x=10,.z=10,.px=10,.pz=9,.id=253,.flags=1};
 avatar.object=&manager.objects[0];preload.count=1;preload.ids[0]=369;location.mapId=59;
 fs=(FieldSystem){&manager,&avatar,&preload,&location,&save};save.partyCount=1;
 monActive=1;task=createFail=terrainBlocked=heightDelta=nativeBlocked=steps=warps=creates=deletes=0;
 SabrinaCompanion_Reset();
}
static void moveMon(int px,int pz,int x,int z){manager.objects[1].px=px;manager.objects[1].pz=pz;manager.objects[1].x=x;manager.objects[1].z=z;manager.objects[0].x=x;manager.objects[0].z=z+1;}
int main(void){
 LocalMapObject *a;SavedMapObject saved[12];SaveVarsFlags stored;SabrinaTrail trail;int i,before;
 fresh();save.gender=1;SabrinaCompanion_InitializeIfNeeded(&save);CHECK(Save_VarsFlags_CheckFlagInArray(&save.flags,FLAG_STORY_DISABLED_FOR_FEMALE));CHECK(!SabrinaCompanion_IsJoined(&save));
 fresh();save.partyCount=0;monActive=0;tick(1);CHECK(!SabrinaCompanion_IsJoined(&save)&&!companion());
 save.partyCount=1;tick(1);CHECK(SabrinaCompanion_IsJoined(&save)&&!companion());
 monActive=1;tick(10);CHECK(companion()!=NULL);a=companion();
 CHECK(!(a->flags&HIDDEN));CHECK(a->flags&(1<<18));CHECK(a->flags&(1<<19));CHECK(!SabrinaCompanion_IsSolid(a));CHECK(creates==1);
 FieldSystem_SyncMapObjectsToSaveEx(&fs,&manager,saved,12);CHECK(saved[0].objId==255&&saved[1].objId==253&&saved[2].objId==0);
 tick(5);CHECK(creates==1&&steps==0);CHECK(!a->keep);
 moveMon(10,10,10,11);tick(1);CHECK(lastCommand==17&&steps==1);
 moveMon(11,10,11,11);tick(1);CHECK(steps==1&&sSabrinaCompanion.trail.count==1);
 a->busy=0;tick(1);CHECK(lastCommand==19&&steps==2);a->busy=0;tick(3);CHECK(steps==2);
 a->busy=0;moveMon(11,9,11,8);manager.objects[0].x=20;manager.objects[0].z=20;tick(1);CHECK(lastCommand==16&&steps==3);
 a->busy=0;moveMon(10,9,9,9);manager.objects[0].x=20;manager.objects[0].z=20;tick(1);CHECK(lastCommand==18&&steps==4);a->busy=0;
 /* A real reverse-turn collision must discard the human rather than block. */
 manager.objects[0].x=a->x;manager.objects[0].z=a->z;tick(1);CHECK(!companion());
 /* Native idle completion resets previous coordinates onto the occupied tile. */
 fresh();tick(1);a=companion();manager.objects[1].px=manager.objects[1].x;manager.objects[1].pz=manager.objects[1].z;
 tick(180);CHECK(companion()==a&&creates==1&&deletes==0&&steps==0);CHECK(a->dir==DIR_SOUTH);
 fresh();manager.objects[1].px=manager.objects[1].x;manager.objects[1].pz=manager.objects[1].z;tick(20);CHECK(!companion()&&SabrinaCompanion_IsJoined(&save));
 fresh();tick(1);task=1;tick(1);CHECK(!companion()&&SabrinaCompanion_IsJoined(&save));task=0;tick(10);CHECK(companion()!=NULL);
 fresh();tick(1);manager.objects[1].paused=1;tick(1);CHECK(!companion());manager.objects[1].paused=0;tick(10);CHECK(companion()!=NULL);
 fresh();tick(1);avatar.state=1;tick(1);CHECK(!companion());avatar.state=0;tick(10);CHECK(companion()!=NULL);
 avatar.state=2;tick(1);CHECK(!companion());avatar.state=0;tick(10);CHECK(companion()!=NULL);
 fresh();terrainBlocked=1;tick(3);CHECK(!companion());terrainBlocked=0;heightDelta=2;tick(2);CHECK(!companion());heightDelta=0;tick(2);CHECK(companion()!=NULL);
 fresh();createFail=1;tick(2);CHECK(!companion());createFail=0;tick(1);CHECK(companion()!=NULL);
 fresh();preload.count=0;tick(2);CHECK(SabrinaCompanion_IsJoined(&save)&&!companion());
 fresh();manager.objects[1].px=-1;tick(1);CHECK(!companion());
 fresh();moveMon(10,10,10,10);tick(1);CHECK(!companion());
 fresh();tick(1);a=companion();nativeBlocked=1;moveMon(10,10,10,11);tick(3);CHECK(companion()==a&&steps==0&&deletes==0);
 nativeBlocked=0;tick(1);CHECK(companion()==a&&steps==1&&lastCommand==17&&deletes==0);
 fresh();tick(1);nativeBlocked=1;moveMon(10,10,10,11);tick(121);CHECK(!companion()&&steps==0);
 fresh();tick(1);moveMon(11,11,12,11);tick(1);CHECK(!companion()&&steps==0);tick(10);CHECK(companion()!=NULL);
 fresh();tick(1);a=companion();moveMon(10,10,10,11);tick(1);CHECK(a->busy);tick(121);CHECK(!companion());
 fresh();tick(1);stored=save.flags;SabrinaCompanion_OnMapExit(&fs);CHECK(!companion());CHECK(!memcmp(&stored,&save.flags,sizeof(stored)));
 location.mapId=60;moveMon(3,4,3,5);manager.objects[0].x=3;manager.objects[0].z=6;tick(1);CHECK(companion()!=NULL&&companion()->x==3);
 SabrinaCompanion_SetJoined(&save,0);tick(1);CHECK(!companion());stored=save.flags;SabrinaCompanion_Reset();save.flags=stored;tick(10);CHECK(!companion()&&!SabrinaCompanion_IsJoined(&save));
 SabrinaCompanion_SetJoined(&save,1);tick(10);CHECK(companion()!=NULL);
 fresh();save.gender=avatar.gender=1;tick(2);CHECK(!SabrinaCompanion_IsJoined(&save)&&!companion());
 fresh();tick(1);location.mapId=MAP_SAFFRON_GYM;tick(1);CHECK(!companion()&&SabrinaCompanion_IsJoined(&save));location.mapId=59;tick(10);CHECK(companion()!=NULL);
 fresh();manager.objects[4]=(LocalMapObject){.x=20,.z=20,.id=5,.sprite=369,.script=1,.map=59,.flags=1};tick(2);CHECK(!companion()&&(manager.objects[4].flags&1));
 fresh();manager.objects[4]=(LocalMapObject){.x=10,.z=9,.id=4,.sprite=1,.script=1,.map=59,.flags=1};tick(2);CHECK(!companion());
 fresh();manager.objects[4]=(LocalMapObject){.id=252,.sprite=369,.script=65535,.map=1,.flags=1};manager.objects[5]=manager.objects[4];tick(1);CHECK(deletes==2&&creates==1);
 fresh();manager.objects[4]=(LocalMapObject){.id=252,.sprite=12,.script=1,.map=59,.flags=1};tick(1);CHECK(manager.objects[4].sprite==12&&deletes==0&&creates==0);
 fresh();SabrinaCompanion_PrepareBattle(&save,59,0,0,0,1);CHECK(sSabrinaPairedBattleArt);
 SabrinaCompanion_PrepareBattle(&save,410,1,258,0,1);CHECK(!sSabrinaPairedBattleArt&&SabrinaCompanion_IsJoined(&save));
 SabrinaCompanion_PrepareBattle(&save,398,1,725,0,1);CHECK(!sSabrinaPairedBattleArt);
 SabrinaCompanion_PrepareBattle(&save,59,1,0,725,1);CHECK(!sSabrinaPairedBattleArt);
 for(i=1;i<=1024;i*=2){if(i&(2|4|8|128|1024)){SabrinaCompanion_PrepareBattle(&save,59,i,0,0,1);CHECK(!sSabrinaPairedBattleArt);}}
 SabrinaCompanion_SetJoined(&save,0);SabrinaCompanion_PrepareBattle(&save,59,0,0,0,1);CHECK(!sSabrinaPairedBattleArt);
 SabrinaCompanion_SetJoined(&save,1);SabrinaCompanion_PrepareBattle(&save,59,0,0,0,0);CHECK(!sSabrinaPairedBattleArt);
 SabrinaCompanion_PrepareBattle(&save,59,0,0,0,1);SabrinaCompanion_ClearBattlePresentation();CHECK(!sSabrinaPairedBattleArt);
 SabrinaTrail_Reset(&trail);for(i=0;i<16;i++)CHECK(SabrinaTrail_Record(&trail,(SabrinaTrailTile){i,0,0,3}));CHECK(trail.count==16);
 CHECK(!SabrinaTrail_Record(&trail,(SabrinaTrailTile){16,0,0,3})&&trail.count==1);
 CHECK(!SabrinaTrail_Record(&trail,(SabrinaTrailTile){100,0,100,3})&&trail.count==1);
 printf("PASS: %d assertions on actual controller, queue, persistence and battle-presentation code (host stubs; not emulator gameplay)\n",checks);return 0;
}
'''
with tempfile.TemporaryDirectory() as d:
    d=Path(d);(d/'test.c').write_text(stub+'\n'+header+'\n'+trail+'\n'+policy+'\n'+controller+'\n'+save_stub+'\n'+serialization+'\n'+tests)
    subprocess.run(['cc','-std=c99','-O1','-fsanitize=undefined,address','-fno-omit-frame-pointer',str(d/'test.c'),'-o',str(d/'test')],check=True)
    subprocess.run([str(d/'test')],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
