/* Experimental companion: no save-layout or HAVE_FOLLOWER flag changes. */
#include "follow_mon.h"
#include "task.h"
#include "unk_02062108.h"
#include "constants/sprites.h"
#include "constants/global_fieldmap.h"
#include "constants/maps.h"

#define SABRINA_COMPANION_ID 252

static void SabrinaCompanion_Tick(FieldSystem *fs) {
    LocalMapObject *sabrina;
    LocalMapObject *mon;
    s32 tx, tz, sx, sz, dx, dz;
    u32 direction;
    int i;
    BOOL preloaded = FALSE;
    if (fs->mapObjectManager == NULL || fs->playerAvatar == NULL || fs->mapObjectsToPreload == NULL) {
        return;
    }
    sabrina = MapObjectManager_GetFirstActiveObjectByID(fs->mapObjectManager, SABRINA_COMPANION_ID);
    /* Never alter a real event object that happens to have the reserved ID. */
    if (sabrina != NULL && MapObject_GetSpriteID(sabrina) != SPRITE_GSLEADER10) {
        return;
    }
    for (i = 0; i < fs->mapObjectsToPreload->count; i++) {
        if (fs->mapObjectsToPreload->ids[i] == SPRITE_GSLEADER10) {
            preloaded = TRUE;
        }
    }
    if (!preloaded || PlayerAvatar_GetGender(fs->playerAvatar) != PLAYER_GENDER_MALE
        || !FollowMon_IsActive(fs)) {
        if (sabrina != NULL) { MapObject_Delete(sabrina); }
        return;
    }
    mon = FollowMon_GetMapObject(fs);
    if (mon == NULL || !FollowMon_IsVisible(fs)
        || PlayerAvatar_GetState(fs->playerAvatar) != PLAYER_STATE_WALKING) {
        if (sabrina != NULL) { MapObject_SetVisible(sabrina, FALSE); }
        return;
    }
    /* Do not start movement while scripts, menus, battles or transitions run. */
    if (FieldSystem_TaskIsRunning(fs) || MapObject_CheckMovementPaused(mon)) {
        return;
    }
    tx = MapObject_GetPreviousXCoord(mon);
    tz = MapObject_GetPreviousZCoord(mon);
    if (tx < 0 || tz < 0) { return; }
    if ((tx == MapObject_GetXCoord(mon) && tz == MapObject_GetZCoord(mon))
        || (tx == PlayerAvatar_GetXCoord(fs->playerAvatar) && tz == PlayerAvatar_GetZCoord(fs->playerAvatar))) {
        return;
    }
    direction = MapObject_GetFacingDirection(mon);
    if (sabrina == NULL) {
        sabrina = MapObject_Create(fs->mapObjectManager, tx, tz, direction, SPRITE_GSLEADER10, 0, MAP_NOTHING);
        if (sabrina == NULL) { return; }
        MapObject_SetID(sabrina, SABRINA_COMPANION_ID);
        MapObject_SetType(sabrina, 0);
        MapObject_SetScriptID(sabrina, 0xffff);
        MapObject_SetEventFlag(sabrina, 0);
        MapObject_SetKeep(sabrina, FALSE);
        MapObject_SetXRange(sabrina, -1);
        MapObject_SetYRange(sabrina, -1);
        MapObject_SetFlag29(sabrina, TRUE);
        MapObject_SetFlagsBits(sabrina, MAPOBJECTFLAG_UNK13);
        MapObject_ClearFlagsBits(sabrina, (MapObjectFlagBits)(MAPOBJECTFLAG_UNK8 | MAPOBJECTFLAG_UNK7));
        MapObject_SetPositionFromXYZAndDirection(sabrina, tx, MapObject_GetPreviousYCoord(mon), tz, direction);
        return;
    }
    if (!MapObject_ClearHeldMovementIfActive(sabrina)) { return; }
    if (!MapObject_CheckVisible(sabrina)) {
        MapObject_SetPositionFromXYZAndDirection(sabrina, tx, MapObject_GetPreviousYCoord(mon), tz, direction);
        MapObject_SetVisible(sabrina, TRUE);
        return;
    }
    sx = MapObject_GetXCoord(sabrina); sz = MapObject_GetZCoord(sabrina);
    dx = tx - sx; dz = tz - sz;
    if (dx == 0 && dz == 0) { return; }
    /* Follow only an already traversed adjacent tile. Never cut a corner. */
    if ((dx == 0 && (dz == 1 || dz == -1)) || (dz == 0 && (dx == 1 || dx == -1))) {
        direction = dx == 1 ? DIR_EAST : dx == -1 ? DIR_WEST : dz == 1 ? DIR_SOUTH : DIR_NORTH;
        MapObject_SetHeldMovement(sabrina, MOVEMENT_RUN_UP + direction);
    } else {
        /* Catch up after a warp or fast movement, using the Pokemon's safe tile. */
        MapObject_SetPositionFromXYZAndDirection(sabrina, tx, MapObject_GetPreviousYCoord(mon), tz, direction);
    }
}
