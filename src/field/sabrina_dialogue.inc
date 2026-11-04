/* Select talks to the independent companion without borrowing an NPC pointer.
 * Native interactions, story triggers, transitions and phone calls run first. */
#include "sabrina_companion.h"
#include "constants/sabrina_story.h"
#include "constants/map_sections.h"
static u16 SabrinaStory_Dialogue(FieldSystem *fs) {
    SaveVarsFlags *flags = Save_VarsFlags_Get(fs->saveData);
    PlayerProfile *profile = Save_PlayerData_GetProfile(fs->saveData);
    int page = 23;
    switch (MapHeader_GetMapSec(fs->location->mapId)) {
    case MAPSEC_NEW_BARK_TOWN: page = 0; break;
    case MAPSEC_CHERRYGROVE_CITY: page = *Save_VarsFlags_GetVarAddr(flags, VAR_SCENE_CHERRYGROVE_CITY_OW) >= 4 ? 25 : 1; break;
    case MAPSEC_VIOLET_CITY: page = PlayerProfile_TestBadgeFlag(profile, BADGE_ZEPHYR) ? 3 : 2; break;
    case MAPSEC_AZALEA_TOWN: page = Save_VarsFlags_CheckFlagInArray(flags, FLAG_BEAT_AZALEA_ROCKETS) ? 5 : 4; break;
    case MAPSEC_GOLDENROD_CITY:
    case MAPSEC_GOLDENROD_TUNNEL: page = Save_VarsFlags_CheckFlagInArray(flags, FLAG_BEAT_RADIO_TOWER_ROCKETS) ? 7 : 6; break;
    case MAPSEC_ECRUTEAK_CITY: page = *Save_VarsFlags_GetVarAddr(flags, VAR_UNK_40A1) ? 26 : 8; break;
    case MAPSEC_OLIVINE_CITY: page = PlayerProfile_TestBadgeFlag(profile, BADGE_MINERAL) ? 10 : 9; break;
    case MAPSEC_LAKE_OF_RAGE: page = Save_VarsFlags_CheckFlagInArray(flags, FLAG_CAUGHT_RED_GYARADOS) ? 27 : 23; break;
    case MAPSEC_MAHOGANY_TOWN: page = Save_VarsFlags_CheckFlagInArray(flags, FLAG_ROCKET_HIDEOUT_CLEARED) ? 12 : 11; break;
    case MAPSEC_BLACKTHORN_CITY: page = PlayerProfile_TestBadgeFlag(profile, BADGE_RISING) ? 14 : 13; break;
    case MAPSEC_INDIGO_PLATEAU: page = Save_VarsFlags_CheckFlagInArray(flags, FLAG_GAME_CLEAR) ? 16 : 15; break;
    case MAPSEC_SAFFRON_CITY: page = PlayerProfile_TestBadgeFlag(profile, BADGE_MARSH) ? 18 : 17; break;
    case MAPSEC_VERMILION_CITY: page = 19; break;
    case MAPSEC_CERULEAN_CITY: page = 20; break;
    case MAPSEC_CELADON_CITY: page = 21; break;
    case MAPSEC_LAVENDER_TOWN: page = 22; break;
    }
    if (page == 23 && *Save_VarsFlags_GetVarAddr(flags, VAR_STORY_DIALOGUE_TEXT) == MSG_SABRINA_CONTEXT_BASE + 23) { page = 24; }
    return MSG_SABRINA_CONTEXT_BASE + page;
}
static BOOL SabrinaStory_TryConversation(FieldSystem *fs, FieldInput *input) {
    if (!(input->newKeys & PAD_BUTTON_SELECT) || !input->unk0_8
        || (input->heldKeys & PAD_PLUS_KEY_MASK)
        || PlayerAvatar_GetState(fs->playerAvatar) != PLAYER_STATE_WALKING
        || !SabrinaCompanion_IsJoined(fs->saveData)
        || MapObjectManager_GetFirstActiveObjectByID(fs->mapObjectManager, SABRINA_COMPANION_OBJECT_ID) == NULL
        || SabrinaCompanion_IsSolid(MapObjectManager_GetFirstActiveObjectByID(fs->mapObjectManager, SABRINA_COMPANION_OBJECT_ID))) {
        return FALSE;
    }
    *Save_VarsFlags_GetVarAddr(Save_VarsFlags_Get(fs->saveData), VAR_STORY_DIALOGUE_TEXT) = SabrinaStory_Dialogue(fs);
    SabrinaCompanion_BeginConversation(fs);
    StartMapSceneScript(fs, std_sabrina_conversation, NULL);
    return TRUE;
}

/* Normal NPCs/objects retain priority. Only the formation's own objects qualify. */
static BOOL SabrinaStory_TryAConversation(FieldSystem *fs, LocalMapObject *target, BOOL menu) {
    LocalMapObject *human = MapObjectManager_GetFirstActiveObjectByID(fs->mapObjectManager, SABRINA_COMPANION_OBJECT_ID);
    LocalMapObject *player = PlayerAvatar_GetMapObject(fs->playerAvatar);
    int dx, dz, facing;
    if (!SabrinaCompanion_IsJoined(fs->saveData) || human == NULL || SabrinaCompanion_IsSolid(human)
        || PlayerAvatar_GetState(fs->playerAvatar) != PLAYER_STATE_WALKING) { return FALSE; }
    if (menu) {
        if (target != FollowMon_GetMapObject(fs)) { return FALSE; }
    } else {
        dx = (int)MapObject_GetXCoord(human) - (int)MapObject_GetXCoord(player);
        dz = (int)MapObject_GetZCoord(human) - (int)MapObject_GetZCoord(player);
        facing = PlayerAvatar_GetFacingDirection(fs->playerAvatar);
        if (MapObject_GetYCoord(human) != MapObject_GetYCoord(player)
            || !((dx == 0 && dz == -1 && facing == DIR_NORTH)
                || (dx == 0 && dz == 1 && facing == DIR_SOUTH)
                || (dx == -1 && dz == 0 && facing == DIR_WEST)
                || (dx == 1 && dz == 0 && facing == DIR_EAST))) { return FALSE; }
    }
    *Save_VarsFlags_GetVarAddr(Save_VarsFlags_Get(fs->saveData), VAR_STORY_DIALOGUE_TEXT) = SabrinaStory_Dialogue(fs);
    SabrinaCompanion_BeginConversation(fs);
    StartMapSceneScript(fs, menu ? std_sabrina_companion_menu : std_sabrina_conversation, menu ? target : NULL);
    return TRUE;
}
