/* Independent companion controller. Native bit 9 is HIDDEN despite its name. */
#include "sabrina_companion.h"
#include "sabrina_companion_trail.h"
#include "follow_mon.h"
#include "task.h"
#include "unk_02062108.h"
#include "unk_02054648.h"
#include "constants/sprites.h"
#include "constants/global_fieldmap.h"
#include "constants/maps.h"

extern u32 sub_02060BB8(LocalMapObject *object, u32 direction);
static struct {
    FieldSystem *owner;
    MapObjectManager *manager;
    u32 map;
    SabrinaTrail trail;
    int stepFrames;
    int blockedFrames;
    int cooldown;
} sSabrinaCompanion;

static void SabrinaCompanion_Reset(void) {
    sSabrinaCompanion.owner = NULL;
    sSabrinaCompanion.manager = NULL;
    SabrinaTrail_Reset(&sSabrinaCompanion.trail);
    sSabrinaCompanion.stepFrames = sSabrinaCompanion.blockedFrames = sSabrinaCompanion.cooldown = 0;
}
static void SabrinaCompanion_RemoveObjects(FieldSystem *fs) {
    s32 index = 0;
    LocalMapObject *object;
    if (fs->mapObjectManager == NULL) { return; }
    while (MapObjectManager_GetNextObjectWithFlagFromIndex(fs->mapObjectManager, &object, &index, MAPOBJECTFLAG_ACTIVE)) {
        if (!SabrinaCompanion_IsSolid(object)) { MapObject_Delete(object); }
    }
}
static void SabrinaCompanion_Drop(FieldSystem *fs) {
    SabrinaCompanion_RemoveObjects(fs);
    SabrinaTrail_Reset(&sSabrinaCompanion.trail);
    sSabrinaCompanion.stepFrames = sSabrinaCompanion.blockedFrames = 0;
    sSabrinaCompanion.cooldown = 8;
}
static void SabrinaCompanion_OnMapExit(FieldSystem *fs) {
    SabrinaCompanion_RemoveObjects(fs);
    SabrinaCompanion_Reset();
}
static BOOL SabrinaCompanion_HasTexture(FieldSystem *fs) {
    int i;
    for (i = 0; i < fs->mapObjectsToPreload->count; i++) {
        if (fs->mapObjectsToPreload->ids[i] == SPRITE_GSLEADER10) { return TRUE; }
    }
    return FALSE;
}
static BOOL SabrinaCompanion_HasCanonicalNPC(FieldSystem *fs) {
    s32 index = 0;
    LocalMapObject *object;
    while (MapObjectManager_GetNextObjectWithFlagFromIndex(fs->mapObjectManager, &object, &index, MAPOBJECTFLAG_ACTIVE)) {
        if (MapObject_GetSpriteID(object) == SPRITE_GSLEADER10 && SabrinaCompanion_IsSolid(object)
            && !MapObject_CheckVisible(object)) { return TRUE; }
    }
    return FALSE;
}
static BOOL SabrinaCompanion_Occupied(FieldSystem *fs, LocalMapObject *self, SabrinaTrailTile tile) {
    s32 index = 0;
    LocalMapObject *object;
    LocalMapObject *mon = FollowMon_GetMapObject(fs);
    LocalMapObject *player = PlayerAvatar_GetMapObject(fs->playerAvatar);
    while (MapObjectManager_GetNextObjectWithFlagFromIndex(fs->mapObjectManager, &object, &index, MAPOBJECTFLAG_ACTIVE)) {
        if (object == self || !SabrinaCompanion_IsSolid(object)) { continue; }
        if (MapObject_GetXCoord(object) == tile.x && MapObject_GetZCoord(object) == tile.z
            && SabrinaTrail_Abs(MapObject_GetYCoord(object) - tile.y) < 2) { return TRUE; }
        if (object != mon && object != player && MapObject_CheckSingleMovement(object)
            && MapObject_GetPreviousXCoord(object) == tile.x && MapObject_GetPreviousZCoord(object) == tile.z
            && SabrinaTrail_Abs((int)MapObject_GetPreviousYCoord(object) - tile.y) < 2) { return TRUE; }
    }
    return FALSE;
}
static BOOL SabrinaCompanion_SafeTile(FieldSystem *fs, LocalMapObject *self, SabrinaTrailTile tile) {
    VecFx32 pos;
    s8 heightDelta = 0;
    if (tile.x < 0 || tile.z < 0 || SabrinaCompanion_Occupied(fs, self, tile)) { return FALSE; }
    pos.x = (tile.x * 16 + 8) * FX32_ONE;
    pos.y = tile.y * 8 * FX32_ONE;
    pos.z = (tile.z * 16 + 8) * FX32_ONE;
    /* Same ground/height collision query as native movement. No blind teleport. */
    return !sub_020549A8(fs, &pos, tile.x, tile.z, (int)&heightDelta) && heightDelta == 0;
}
static void SabrinaCompanion_Tick(FieldSystem *fs) {
    LocalMapObject *sabrina;
    LocalMapObject *mon;
    SabrinaTrailTile tile, here;
    SabrinaTrailTile *next;
    int dx, dz, direction;
    BOOL continuous;
    if (fs->mapObjectManager == NULL || fs->playerAvatar == NULL || fs->location == NULL || fs->mapObjectsToPreload == NULL) { return; }
    SabrinaCompanion_InitializeIfNeeded(fs->saveData);
    if (sSabrinaCompanion.owner != fs || sSabrinaCompanion.manager != fs->mapObjectManager
        || sSabrinaCompanion.map != fs->location->mapId) {
        /* Also removes objects restored by an older prototype save. */
        SabrinaCompanion_RemoveObjects(fs);
        SabrinaCompanion_Reset();
        sSabrinaCompanion.owner = fs;
        sSabrinaCompanion.manager = fs->mapObjectManager;
        sSabrinaCompanion.map = fs->location->mapId;
    }
    if (!SabrinaCompanion_IsJoined(fs->saveData) || PlayerAvatar_GetGender(fs->playerAvatar) != PLAYER_GENDER_MALE
        || !FollowMon_IsActive(fs) || !FollowMon_IsVisible(fs) || !SabrinaCompanion_HasTexture(fs)
        || PlayerAvatar_GetState(fs->playerAvatar) != PLAYER_STATE_WALKING
        || fs->location->mapId == MAP_SAFFRON_GYM || SabrinaCompanion_HasCanonicalNPC(fs)
        || FieldSystem_TaskIsRunning(fs)) {
        SabrinaCompanion_Drop(fs); return;
    }
    mon = FollowMon_GetMapObject(fs);
    if (mon == NULL || MapObject_CheckMovementPaused(mon)) { SabrinaCompanion_Drop(fs); return; }
    if (sSabrinaCompanion.cooldown) { sSabrinaCompanion.cooldown--; return; }
    sabrina = MapObjectManager_GetFirstActiveObjectByID(fs->mapObjectManager, SABRINA_COMPANION_OBJECT_ID);
    if (sabrina != NULL && SabrinaCompanion_IsSolid(sabrina)) { return; }
    tile.x = MapObject_GetPreviousXCoord(mon);
    tile.y = MapObject_GetPreviousYCoord(mon);
    tile.z = MapObject_GetPreviousZCoord(mon);
    tile.direction = MapObject_GetFacingDirection(mon);
    if (tile.x < 0 || tile.z < 0) { SabrinaCompanion_Drop(fs); return; }
    /* Native previous coordinates reset to current on a completed step. Only
     * record a vacated tile: recording the settled Pokemon tile would make
     * Sabrina chase into the Pokemon and disappear every time the player stops. */
    continuous = TRUE;
    if (tile.x != MapObject_GetXCoord(mon) || tile.z != MapObject_GetZCoord(mon)) {
        continuous = SabrinaTrail_Record(&sSabrinaCompanion.trail, tile);
    } else if (sabrina == NULL) {
        if (!sSabrinaCompanion.trail.lastValid) { return; }
        tile = sSabrinaCompanion.trail.last; /* Checked vacated tile, never the settled Pokemon tile. */
    }
    if (!continuous && sabrina != NULL) { SabrinaCompanion_Drop(fs); return; }
    if (sabrina == NULL) {
        /* Fresh placement always uses the most recent traversed, unoccupied tile. */
        if (!SabrinaCompanion_SafeTile(fs, NULL, tile)) { return; }
        sabrina = MapObject_CreateWithID(fs->mapObjectManager, SABRINA_COMPANION_OBJECT_ID, tile.x, tile.z, tile.direction, SPRITE_GSLEADER10, 0, MAP_NOTHING);
        if (sabrina == NULL) { return; }
        MapObject_SetID(sabrina, SABRINA_COMPANION_OBJECT_ID);
        MapObject_SetType(sabrina, 0);
        MapObject_SetScriptID(sabrina, 0xffff);
        MapObject_SetEventFlag(sabrina, 0);
        MapObject_SetKeep(sabrina, FALSE);
        MapObject_SetXRange(sabrina, -1); MapObject_SetYRange(sabrina, -1);
        MapObject_SetFlag29(sabrina, TRUE);
        MapObject_SetFlagsBits(sabrina, MAPOBJECTFLAG_UNK13);
        MapObject_ClearFlagsBits(sabrina, (MapObjectFlagBits)(MAPOBJECTFLAG_UNK8 | MAPOBJECTFLAG_UNK7));
        MapObject_ClearFlag18(sabrina, FALSE); /* Native ignored-obstacle bit. */
        MapObject_SetFlag19(sabrina, TRUE);   /* No event/interaction interception. */
        MapObject_SetPositionFromXYZAndDirection(sabrina, tile.x, tile.y, tile.z, tile.direction);
        MapObject_SetVisible(sabrina, FALSE); /* FALSE means shown in this engine. */
        SabrinaTrail_Reset(&sSabrinaCompanion.trail);
        SabrinaTrail_Record(&sSabrinaCompanion.trail, tile);
        SabrinaTrail_Pop(&sSabrinaCompanion.trail);
        return;
    }
    here.x = MapObject_GetXCoord(sabrina); here.y = MapObject_GetYCoord(sabrina); here.z = MapObject_GetZCoord(sabrina);
    here.direction = MapObject_GetFacingDirection(sabrina);
    if (SabrinaCompanion_Occupied(fs, sabrina, here)) { SabrinaCompanion_Drop(fs); return; }
    if (!MapObject_ClearHeldMovementIfActive(sabrina)) {
        if (++sSabrinaCompanion.stepFrames > 120) { SabrinaCompanion_Drop(fs); }
        return;
    }
    sSabrinaCompanion.stepFrames = 0;
    next = SabrinaTrail_First(&sSabrinaCompanion.trail);
    while (next != NULL && SabrinaTrail_Same(*next, here)) {
        SabrinaTrail_Pop(&sSabrinaCompanion.trail);
        next = SabrinaTrail_First(&sSabrinaCompanion.trail);
    }
    if (next == NULL) {
        sSabrinaCompanion.blockedFrames = 0;
        /* A corner can end on Sabrina's tile without another step. Face the
         * adjacent Pokemon instead of retaining the last walking direction. */
        dx = (int)MapObject_GetXCoord(mon) - here.x;
        dz = (int)MapObject_GetZCoord(mon) - here.z;
        if (SabrinaTrail_Abs(dx) + SabrinaTrail_Abs(dz) == 1) {
            direction = dx == 1 ? DIR_EAST : dx == -1 ? DIR_WEST : dz == 1 ? DIR_SOUTH : DIR_NORTH;
            MapObject_SetOrQueueFacing(sabrina, direction);
        }
        return;
    }
    dx = next->x - here.x; dz = next->z - here.z;
    if (SabrinaTrail_Abs(dx) + SabrinaTrail_Abs(dz) != 1 || SabrinaTrail_Abs(next->y - here.y) > 1
        || !SabrinaCompanion_SafeTile(fs, sabrina, *next)) {
        SabrinaCompanion_Drop(fs); return;
    }
    direction = dx == 1 ? DIR_EAST : dx == -1 ? DIR_WEST : dz == 1 ? DIR_SOUTH : DIR_NORTH;
    /* Native collision keeps a moving Pokemon's previous footprint occupied
     * until its step finishes. Wait for that footprint instead of blinking out. */
    if (sub_02060BB8(sabrina, direction) != 0) {
        if (++sSabrinaCompanion.blockedFrames > 120) { SabrinaCompanion_Drop(fs); }
        return;
    }
    sSabrinaCompanion.blockedFrames = 0;
    MapObject_SetHeldMovement(sabrina, MOVEMENT_RUN_UP + direction);
    SabrinaTrail_Pop(&sSabrinaCompanion.trail);
}
