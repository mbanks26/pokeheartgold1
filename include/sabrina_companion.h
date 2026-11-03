#ifndef POKEHEARTGOLD_SABRINA_COMPANION_H
#define POKEHEARTGOLD_SABRINA_COMPANION_H

#include "global.h"
#include "map_object.h"
#include "save.h"

/* Reserved from the existing unnamed tail of the save flag array. No resize. */
#define FLAG_SABRINA_COMPANION_INITIALIZED 0xB5E
#define FLAG_SABRINA_COMPANION_JOINED      0xB5F
#define SABRINA_COMPANION_OBJECT_ID 252
#define SABRINA_SOLO_BACKPIC 17
#define SABRINA_SOLO_LINK_BACKPIC 18

BOOL SabrinaCompanion_IsJoined(SaveData *save);
void SabrinaCompanion_SetJoined(SaveData *save, BOOL joined);
void SabrinaCompanion_InitializeIfNeeded(SaveData *save);
BOOL SabrinaCompanion_IsSolid(LocalMapObject *object);
void SabrinaCompanion_PrepareBattle(SaveData *save, u32 map, u32 type, int enemy1, int enemy2, BOOL male);
void SabrinaCompanion_ClearBattlePresentation(void);

#endif
