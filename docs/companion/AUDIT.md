# Pre-edit audit: permanent Sabrina companion

## Recovered history and protection

The live custom work is in mbanks26/pokeheartgold1. mbanks26/pokeheartgold has only
the unrelated upstream master 8cbb4a19. In pokeheartgold1, all of afd4151f (Sabrina),
bda9631d (male), 2c669251 (female), cfea70fd (extended graphics) are ancestors of
4ea2dc8a (prototype). The prototype already contains the graphics; no merge or
recreation is needed. The initial working tree was clean. A remote checkpoint
recovery/pre-companion-stabilization-20261103 points to 4ea2dc8a; a full local
Git bundle and separate prototype ROM copy were made before edits. Development
continues on development/sabrina-stabilization-20261103. Existing branches and
ROMs are retained. The existing Ninja graph reported no work and the prototype
ROM matched recorded SHA-1 544e5b9a59dab0656ab1c3fe28f0e4fe8f4fd8db.

## Actual prototype architecture

src/field/sabrina_companion.inc is included by fieldmap.c. Its per-frame hook
looks up object 252, requires male avatar/active visible following Pokemon and
a preloaded Sabrina texture. It uses SPRITE_GSLEADER10 (369), native model 163.
It creates an independent ordinary human object, never substitutes the Pokemon.
Its only history is the native Pokemon object's previous coordinate, not a
queue. It starts a run-step for adjacent targets and teleports to others.
The preload list reserves the existing Sabrina sprite when capacity permits.

There is no joined flag or save initialization. Reappearance after reload is an
eligibility effect, not explicit persistence. The object is non-KEEP with no
custom talk script. There are no explicit map-entry/exit trail lifecycle hooks.
Scripts pause new commands but leave the object present as a potential obstacle.
Placement checks only player/Pokemon current positions; no generic NPC occupancy
or terrain check is made. There is no timeout for a stuck held movement.

## Confirmed defects and missing behavior

1. Native MapObject_SetVisible(TRUE) sets bit 9, which actually hides an object.
   FollowMon_IsVisible explicitly negates MapObject_CheckVisible. Door-transition
   code corroborates this. Prototype hide/restore logic and its host stub used
   the opposite interpretation, so prior host success does not validate rendering.
2. The original clearing of flags 7/8 is not proof of non-collision. Native
   collision scanning sub_02060BFC excludes bit 18. Interaction filtering uses
   bit 19. These need intentional handling, plus removal during task/cutscenes.
3. Sampling only the newest previous coordinate can skip intermediate turns.
4. Unchecked teleport targets can be occupied. No validated breadcrumb recovery,
   map epoch, held-step timeout, or duplicate-save cleanup is implemented.
5. Player-side male battle art is always the combined sheet in backpic 0/15;
   TrainerClassToBackpicID has no companion/Gym condition. Thus Sabrina can appear
   beside the player against herself or while disabled. Existing solo artwork
   remains recoverable from bda9631d and must be reused without redrawing.
6. Gym/rematch scripts are intact, including battle, loss/whiteout, Marsh Badge,
   TM48 and post-battle rewards. A presentation exception should avoid rewriting
   these progression scripts. Companion suppression in her Gym prevents duplicates;
   join state should survive victory/loss and resume after leaving the Gym.

## Implementation boundaries

Preserve all existing custom artwork bytes. Add copies of existing solo battle
resources only if runtime selection needs extra archive slots. Reserve two
previously unnamed tail flags within the existing 2912-bit array, after auditing
their direct source/script references; do not alter save block size. Document
compatibility and the existing SetFlag/ClearFlag event interface. Do not use
FLAG_HAVE_FOLLOWER, which changes battle rules and restricts field moves.

Keep field history transient, map-scoped, bounded, and derived only from native
Pokemon traversed tiles. Hide/remove on unsafe scripts, actions, occupancy and
discontinuities. Validate native collisions before steps. Treat compilation,
host model tests, emulator boot/scenarios and actual Manic EMU testing as distinct
evidence. No previous emulator gameplay verification is available.
