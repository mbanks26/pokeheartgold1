# Emulator gameplay validation checkpoint — 2026-11-03

Development continues on `development/sabrina-gameplay-validation-20261103`, from
protected checkpoint `2acac167`. The prior branch, ROM and patch are retained.
This is an in-progress validation report, not full-game or iPhone certification.

## Bugs found by actual gameplay and fixed

1. Native Pokemon previous coordinates reset to its current occupied tile when
   it stops. The controller now records only truly vacated tiles, retaining the
   last validated trail tile for safe placement. Sabrina no longer disappears
   simply because the player stops.
2. Native movement reserves the Pokemon's previous footprint until its animation
   finishes. Sabrina now waits for that footprint to clear instead of dropping
   and respawning at ordinary corners. A 120-update bound retains safe recovery.
3. When a corner ends without another human step, idle facing now points toward
   the adjacent lead Pokemon rather than retaining the previous walk direction.

Only the controller and its meaningful regression tests change at runtime. All
5,980 existing graphics files, original adventure scripts and battle rules remain
unchanged. There are now **88 sanitized host assertions**; these complement, rather
than substitute for, the emulator runs.

## Evidence collected so far

- A fresh game completed Oak's introduction, player-entered naming, the home
  introduction, starter selection and early Lyra encounter.
- Both custom character selection designs, male field graphics and the custom
  white-haired Lyra NPC are visible in captured gameplay.
- Independent actor IDs 255 (player), 253 (native Pokemon) and 252 (Sabrina) form
  the expected trail. No Pokemon identity substitution is used.
- Walking, stopping, corners, reversals and all four directions have native-engine
  position and object-count checks. On the corner-fix intermediate ROM, Sabrina
  remained present for all 48 sampled frames of the corner, and all 32 sampled
  frames of a subsequent westward section. The final ROM additionally fixes idle
  facing; further final-ROM regression runs continue.
- The lab aide and post-starter Lyra scripts suppress Sabrina and complete, with
  automatic companion recovery afterward. Full-building exit and outdoor height
  changes have been exercised.
- Battery save loading in a building preserves joined status; only one native
  Pokemon object is restored, and Sabrina returns after safe walking.
- On the final ROM, an isolated action fixture verifies native bicycle state 1
  suppresses Sabrina, and dismount plus safe walking restores state 0 and one
  Sabrina object alongside the Pokemon.
- On the final ROM, a late-game fixture enters Saffron Gym through its real door,
  loads the official Sabrina NPC, suppresses the companion and traverses native
  Gym teleporters. Battle outcomes are still being checked.

The action/Gym fixture is derived from our own fresh starter save. It supplies
location, a bicycle, Old Rod, Fog Badge and a level-100 Feraligatr with test stats
and Surf, solely to reach late-game scenarios. Fixture setup is not evidence of
normal progression. Gameplay ROM/source code and story scripts are unchanged by
these authored save fixtures. No user save is modified.

## Current build and remaining checks

- ROM build: PASS; separate `build/sabrina-gameplay-validation` directory.
- ROM SHA-1: `5cbf4223b6b1a02ccee28fd276e86281fff61291`.
- ARM7 stock checksum: PASS.
- [New BPS candidate](sabrina-companion-gameplay-tested.bps): generator roundtrip
  and independent RomPatcherJS CRC/apply checks PASS.
- Required clean US source SHA-1: `4fcded0e2713dc03929845de631d0932ea2b5a37`.

Surf/fishing restoration, wild/trainer battle presentation, Sabrina victory/loss,
more save/reload scenarios, caves/ledges and full story coverage remain pending at
this checkpoint. Manic EMU on the user's iPhone has not been accessed or tested.
Evidence snapshots and machine-readable checkpoint data are in
[gameplay-20261103](gameplay-20261103/).
