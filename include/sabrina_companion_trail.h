#ifndef POKEHEARTGOLD_SABRINA_COMPANION_TRAIL_H
#define POKEHEARTGOLD_SABRINA_COMPANION_TRAIL_H

#define SABRINA_TRAIL_CAPACITY 16
typedef struct SabrinaTrailTile { int x, y, z, direction; } SabrinaTrailTile;
typedef struct SabrinaTrail {
    SabrinaTrailTile tiles[SABRINA_TRAIL_CAPACITY];
    SabrinaTrailTile last;
    int head, count, lastValid;
} SabrinaTrail;

static void SabrinaTrail_Reset(SabrinaTrail *trail) {
    trail->head = trail->count = trail->lastValid = 0;
}
static int SabrinaTrail_Abs(int value) { return value < 0 ? -value : value; }
static int SabrinaTrail_Same(SabrinaTrailTile a, SabrinaTrailTile b) {
    return a.x == b.x && a.y == b.y && a.z == b.z;
}
/* Returns 1 for continuous history, 0 when history was safely resynchronized. */
static int SabrinaTrail_Record(SabrinaTrail *trail, SabrinaTrailTile tile) {
    int continuous = 1;
    if (trail->lastValid && SabrinaTrail_Same(trail->last, tile)) { return 1; }
    if ((trail->lastValid && (SabrinaTrail_Abs(trail->last.x - tile.x)
        + SabrinaTrail_Abs(trail->last.z - tile.z) != 1
        || SabrinaTrail_Abs(trail->last.y - tile.y) > 1))
        || trail->count == SABRINA_TRAIL_CAPACITY) {
        SabrinaTrail_Reset(trail);
        continuous = 0;
    }
    trail->tiles[(trail->head + trail->count) % SABRINA_TRAIL_CAPACITY] = tile;
    trail->count++;
    trail->last = tile;
    trail->lastValid = 1;
    return continuous;
}
static SabrinaTrailTile *SabrinaTrail_First(SabrinaTrail *trail) {
    return trail->count ? &trail->tiles[trail->head] : 0;
}
static void SabrinaTrail_Pop(SabrinaTrail *trail) {
    if (trail->count) {
        trail->head = (trail->head + 1) % SABRINA_TRAIL_CAPACITY;
        trail->count--;
    }
}
#endif
