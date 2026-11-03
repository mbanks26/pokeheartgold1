# Companion implementation and scope

This development build retains the original adventure and all existing character
art. It is a candidate for gameplay testing, not a claim of full-game validation.
The independent formation is player -> native lead Pokemon -> human Sabrina.

## Activation and persistence

The first eligible male save with a nonempty party sets initialized flag 0xB5E
and joined flag 0xB5F. This is temporary automatic activation for testing, not a
new story introduction. Movement is not the join trigger. Existing male saves
without the initialized bit migrate the same way on entering the field or battle.
Female saves do not automatically join. The avatar remains player-name selectable.

These two flags occupy the previously unnamed final bits of the existing 2912-bit
flag array. An audit found definitions FLAG_UNK_B5E/F but no prior source or script
uses. Save structures, allocation sizes and checksums are not changed. A save from
another hack that uses these flags may conflict; original/prototype saves should
not need conversion. Back up the battery save before testing. Emulator save states
from a different ROM revision are not a supported migration mechanism.

Future C/story integration can call SabrinaCompanion_SetJoined(save, TRUE/FALSE).
It always marks initialized, so deliberate deactivation persists. Existing event
commands can SetFlag 0xB5E then SetFlag/ClearFlag 0xB5F. Clearing only joined before
setting initialized would allow automatic initialization to rejoin. No new event
command or player-facing menu is added. FLAG_HAVE_FOLLOWER is never set: that flag
would change battle and field-move mechanics.

The joined state persists in the normal save flags. Object 252 and its breadcrumb
queue are transient. The save serializer omits only the identified companion,
while leaving ordinary NPCs and the native Pokemon untouched. On field entry,
older prototype companion objects are removed and rebuilt once. Save/load field
coordinates and native Pokemon state continue to use the original engine.

## Movement, collisions and lifecycle

The follow-up gameplay fixes are documented in [GAMEPLAY-VALIDATION.md](GAMEPLAY-VALIDATION.md): ignore settled Pokemon previous coordinates, wait for transient native footprints, and update idle facing after corners.

The field overlay reserves the existing sprite 369/model 163 when preload capacity
allows. Each update requires a joined male player, a visible active native Pokemon,
normal walking, available graphics and no field task or paused Pokemon movement.
The human object never changes the Pokemon identity or native following code.

A bounded 16-tile FIFO records changes to the Pokemon's previous traversed tile,
including while Sabrina finishes her current animation. Adjacent crumbs are
followed with native directional step animations. Idle frames issue no new step.
Overflow, discontinuities, occupied tiles, invalid heights/terrain, failed native
collision probes or a 120-frame stuck movement discard the transient actor/trail.
After an eight-update recovery delay, placement uses a currently checked traversed
tile. Recovery may visibly remove/reintroduce Sabrina; it never blindly teleports
her through walls. North, south, east, west and queued corners have host coverage.

Placement checks current object occupancy and moving NPC previous occupancy,
terrain/height, and player/Pokemon overlap. Directional movement also calls the
native collision query. The native collision scanners and front-interaction lookup
ignore exactly object 252 + sprite 369 + script 0xFFFF. Bit 18 and bit 19 give the
matching native no-obstacle/no-interaction behavior. Other Sabrina NPC objects
retain their original collision and scripts. A foreign use of ID 252 is not deleted.
Dynamic creation sets ID 252 before engine lookup, avoiding accidental reuse of
an unrelated ID-zero actor. Allocation failure safely postpones creation.

During scripts/tasks, cycling, surfing, hidden Pokemon, unsafe occupancy and other
non-walking states the actor is deleted, not merely left hidden as an obstacle.
Full field exit removes it before graphics teardown. Field initialization resets
transient state. A changed map ID/manager invalidates the queue, covering connected
maps as well as warps. The actor returns automatically after eligible safe walking.
Ledges or unusual vertical transitions can cause a temporary disappearance.
This reusable task suppression avoids rewriting individual story cutscenes.

## Battles and Sabrina's Gym

The existing paired male/Sabrina sheets remain byte-for-byte unchanged. Battle
initialization selects them only for an eligible joined male in an ordinary
single battle. This changes presentation only: no partner trainer, extra battler,
turn, Pokemon calculation, Pokeball command or battle-type flag is added.
Existing paired art and protagonist animation resources are reused.

When disabled, in excluded battle modes (including doubles/link/tutorial/frontier),
in Saffron Gym, or against Sabrina trainer 258 or rematch 725, the male uses his
existing solo custom art recovered from bda9631d. Exact copies of the two original
solo resource groups were appended as backpic groups 17/18. All 85 prior archive
members, all other artwork and the female resources are unchanged. The selector
is cleared at battle exit to avoid carrying presentation state to another battle.

Sabrina's companion is suppressed throughout Saffron Gym, and wherever a visible
canonical Sabrina NPC exists (including her rematch location). Her joined flag is
retained. Original Gym battle, loss/whiteout, Marsh Badge, TM and rematch scripts
are unchanged. She resumes after leaving the suppressed area and establishing a
safe walking trail, whether the player won or lost. This is deliberately a small
technical exception, without new dialogue or story scenes.

## Limits requiring gameplay validation

Host stubs test controller decisions, not the DS renderer, engine scheduling or
full story. Compilation and boot are separate evidence. Doors, terrain heights,
ledge animations, long cutscenes, actual battery-save restoration, paired throwing
animation, Gym victory/defeat and Manic EMU compatibility need gameplay testing.
Missing preload capacity safely suppresses Sabrina. Multiplayer/double-battle
companion art is intentionally outside scope. No companion conversation or new
sibling storyline was added. All existing three character designs are preserved;
existing source art fidelity was not re-reviewed or redrawn during this task.
