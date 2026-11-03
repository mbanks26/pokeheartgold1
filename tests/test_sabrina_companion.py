"""Host state-machine checks on the actual companion source with engine stubs.

These test decisions and object lifetimes, not rendering, collision or emulation.
Run with python3 tests/test_sabrina_companion.py; requires a host C compiler.
"""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
source='\n'.join(l for l in (root/'src/field/sabrina_companion.inc').read_text().splitlines() if not l.startswith('#include'))
stub=r'''
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
typedef unsigned u32; typedef int s32; typedef int BOOL; typedef int MapObjectFlagBits;
#define TRUE 1
#define FALSE 0
#define SPRITE_GSLEADER10 369
#define PLAYER_GENDER_MALE 0
#define PLAYER_STATE_WALKING 0
#define MAP_NOTHING 1
#define MOVEMENT_RUN_UP 16
#define DIR_NORTH 0
#define DIR_SOUTH 1
#define DIR_WEST 2
#define DIR_EAST 3
#define MAPOBJECTFLAG_UNK13 8192
#define MAPOBJECTFLAG_UNK8 256
#define MAPOBJECTFLAG_UNK7 128
typedef struct Obj {int x,z,y,px,pz,py,sprite,id,visible,paused,dir,finished;} LocalMapObject;
typedef struct {int gender,state,x,z;} Avatar;
typedef struct {int count,ids[8];} Preload;
typedef struct {void *mapObjectManager;Avatar *playerAvatar;Preload *mapObjectsToPreload;} FieldSystem;
static LocalMapObject actor,mon; static int exists,active,visible,task,createFail,steps,warps,deletes,creates,lastCommand,lastScript;
static LocalMapObject *MapObjectManager_GetFirstActiveObjectByID(void*m,u32 id){return exists?&actor:NULL;}
static u32 MapObject_GetSpriteID(LocalMapObject*o){return o->sprite;}
static u32 PlayerAvatar_GetGender(Avatar*a){return a->gender;}
static u32 PlayerAvatar_GetState(Avatar*a){return a->state;}
static u32 PlayerAvatar_GetXCoord(Avatar*a){return a->x;}
static u32 PlayerAvatar_GetZCoord(Avatar*a){return a->z;}
static BOOL FollowMon_IsActive(FieldSystem*f){return active;}
static BOOL FollowMon_IsVisible(FieldSystem*f){return visible;}
static LocalMapObject *FollowMon_GetMapObject(FieldSystem*f){return &mon;}
static void MapObject_Delete(LocalMapObject*o){exists=0;deletes++;}
static BOOL MapObject_CheckMovementPaused(LocalMapObject*o){return o->paused;}
static BOOL FieldSystem_TaskIsRunning(FieldSystem*f){return task;}
static u32 MapObject_GetPreviousXCoord(LocalMapObject*o){return o->px;}
static u32 MapObject_GetPreviousZCoord(LocalMapObject*o){return o->pz;}
static u32 MapObject_GetPreviousYCoord(LocalMapObject*o){return o->py;}
static u32 MapObject_GetXCoord(LocalMapObject*o){return o->x;}
static u32 MapObject_GetZCoord(LocalMapObject*o){return o->z;}
static u32 MapObject_GetFacingDirection(LocalMapObject*o){return o->dir;}
static void MapObject_SetVisible(LocalMapObject*o,BOOL b){o->visible=b;}
static BOOL MapObject_CheckVisible(LocalMapObject*o){return o->visible;}
static LocalMapObject *MapObject_Create(void*m,u32 x,u32 z,u32 d,u32 s,u32 v,u32 map){if(createFail)return NULL;actor=(LocalMapObject){.x=x,.z=z,.sprite=s,.visible=1,.finished=1};exists=1;creates++;return &actor;}
static void MapObject_SetID(LocalMapObject*o,u32 id){o->id=id;}
static void MapObject_SetType(LocalMapObject*o,u32 t){}
static void MapObject_SetScriptID(LocalMapObject*o,u32 s){lastScript=s;}
static void MapObject_SetEventFlag(LocalMapObject*o,u32 f){}
static void MapObject_SetKeep(LocalMapObject*o,BOOL b){}
static void MapObject_SetXRange(LocalMapObject*o,int x){}
static void MapObject_SetYRange(LocalMapObject*o,int y){}
static void MapObject_SetFlag29(LocalMapObject*o,BOOL b){}
static void MapObject_SetFlagsBits(LocalMapObject*o,int f){}
static void MapObject_ClearFlagsBits(LocalMapObject*o,int f){}
static void MapObject_SetPositionFromXYZAndDirection(LocalMapObject*o,u32 x,u32 y,u32 z,u32 d){o->x=x;o->z=z;o->y=y;warps++;}
static BOOL MapObject_ClearHeldMovementIfActive(LocalMapObject*o){return o->finished;}
static void MapObject_SetHeldMovement(LocalMapObject*o,u32 cmd){steps++;lastCommand=cmd;}
'''
tests=r'''
int main(void){
 Avatar a={0,0,10,12};Preload p={1,{369}};FieldSystem f={(void*)1,&a,&p};
 mon=(LocalMapObject){.x=10,.z=11,.px=10,.pz=10,.py=2};
 visible=1;active=0;SabrinaCompanion_Tick(&f);assert(!exists);
 active=1;a.gender=1;SabrinaCompanion_Tick(&f);assert(!exists);
 a.gender=0;task=1;SabrinaCompanion_Tick(&f);assert(!exists);
 task=0;createFail=1;SabrinaCompanion_Tick(&f);assert(!exists);
 createFail=0;p.count=0;SabrinaCompanion_Tick(&f);assert(!exists);
 p.count=1;mon.px=-1;SabrinaCompanion_Tick(&f);assert(!exists);
 mon.px=10;SabrinaCompanion_Tick(&f);assert(exists&&creates==1&&actor.id==252&&lastScript==65535&&actor.y==2);
 SabrinaCompanion_Tick(&f);assert(creates==1&&steps==0);
 mon.pz=11;mon.z=12;a.z=13;SabrinaCompanion_Tick(&f);assert(steps==1&&lastCommand==17);
 actor.finished=0;SabrinaCompanion_Tick(&f);assert(steps==1);actor.finished=1;
 task=1;SabrinaCompanion_Tick(&f);assert(steps==1);task=0;
 mon.paused=1;SabrinaCompanion_Tick(&f);assert(steps==1);mon.paused=0;
 a.state=1;SabrinaCompanion_Tick(&f);assert(!actor.visible&&exists);
 a.state=0;SabrinaCompanion_Tick(&f);assert(actor.visible&&actor.z==11);
 actor.x=4;int before=warps;SabrinaCompanion_Tick(&f);assert(warps==before+1&&actor.x==10&&actor.z==11);
 actor.sprite=123;a.gender=1;before=deletes;SabrinaCompanion_Tick(&f);assert(exists&&deletes==before);
 actor.sprite=369;SabrinaCompanion_Tick(&f);assert(!exists&&deletes==before+1);
 puts("PASS: companion eligibility, allocation, identity, pause, movement, hide/restore, catch-up and cleanup decisions");return 0;
}
'''
with tempfile.TemporaryDirectory() as d:
    path=Path(d);(path/'test.c').write_text(stub+'\n'+source+'\n'+tests)
    subprocess.run(['cc','-std=c99',str(path/'test.c'),'-o',str(path/'test')],check=True)
    subprocess.run([str(path/'test')],check=True)
