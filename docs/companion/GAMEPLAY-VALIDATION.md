# Sabrina companion gameplay validation — 2026-11-03

Previously unverified actions have now been exercised in a real headless DeSmuME
libretro emulator. Three movement bugs were found and fixed. This is a tested
development candidate; Manic EMU and full-game certification remain pending.

Branch: `development/sabrina-gameplay-validation-20261103` in
`mbanks26/pokeheartgold1`. Runtime fixes: `bc2f6a1e`. Master, recovery branches,
the stabilization branch, earlier ROMs and patches remain preserved.

## Build and automated checks

- ROM compilation PASS in separate `build/sabrina-gameplay-validation` directory.
- ROM SHA-1: `5cbf4223b6b1a02ccee28fd276e86281fff61291`; 134,217,728 bytes.
- Native ARM7 checksum PASS. Modified ARM9/full-ROM stock checksums do not apply.
- **88 sanitized host assertions PASS** on actual controller, trail, persistence,
  battle policy and serializer code. Engine calls are stubbed in those tests.
- Preservation audit: **5,980 existing graphics unchanged**, all original story
  scripts unchanged; 85 existing back-archive members remain identical. The
  stabilization work appended ten already recovered solo resources.
- [BPS test patch](sabrina-companion-gameplay-tested.bps): generator roundtrip and
  independent RomPatcherJS CRC/apply verification PASS. Required clean US ROM
  SHA-1: `4fcded0e2713dc03929845de631d0932ea2b5a37`.
- Final-ROM cold-boot smoke: **18 commands, seven assertion groups, zero errors,
  process exit 0**. Actor counts, exact positions and facing pass in all directions.
  All three actors stay present across 48 southward, 32 westward and 32 northward
  motion frames; all stay stationary throughout 180 sampled idle frames.

## Actual emulator gameplay

Evidence is in [gameplay-20261103](gameplay-20261103/). The table uses the final ROM
above except where an earlier fresh-game run is explicitly identified. Actor IDs
are player 255, original Pokemon 253 and independent Sabrina 252.

| Check | Result and evidence |
| --- | --- |
| Walking, corners, stopping, facing | PASS, ordered adjacent actors; `smoke-commands.jsonl`, motion/idle traces and `smoke-*.png`; ordinary starter save |
| Genuine town save and cold load | PASS; emulator closed, native Continue used, joined flag retained, one Sabrina returns after walking; `town-cold-load-pass.png`, `town-cold-reload-walk-pass.png` |
| Indoor save load | PASS; native lab starter save loads on final ROM, human returns after a safe trail |
| Native doors and buildings | PASS for home/lab, Union Cave and Saffron Gym routes exercised; `cave-walk-after-transition.png`, `gym-entry-check.png` |
| Map connection and script recovery | PASS Route 29 to New Bark; native Pokegear gate finishes, walking restores formation; `connection-clear-walking-pass.png`; fixture supplies missing prerequisite |
| Cave and restricted approach | PASS Union Cave entry/exit and short interior walking trail, original NPCs retained; `cave-walk-after-transition.png`; not every cave/passage |
| Native ledge | PASS Route 29 east-facing ledge crossing; human may disappear during unsafe jump trail and returns in order after walking; `ledge-mid.png`, `ledge-after.png`, `ledge-commands.jsonl`; isolated save with native Repel counter |
| Cycling | PASS; state 1 hides Sabrina, dismount/walking restores state 0 and one of each follower; `cycle-hide-final.png`, `cycle-restore-final.png` |
| Surfing | PASS native Surf question/action, state 2, no companion; landing/walking restores formation; `surfing-pass.png`, `surf-and-battle-recovery-pass.png` |
| Fishing | PASS native Old Rod action suppresses human, finishing/walking restores her; `fishing-action.png`, `fishing-restoration-pass.png` |
| Wild Single Battle | PASS Tentacool encounter during Surf, paired back art, one active Pokemon, victory and walking recovery; `wild-intro-120.png`, `surf-and-battle-recovery-pass.png` |
| Trainer Single Battle | PASS Bird Keeper Peter, paired art, normal battle and victory, walking recovery; `ordinary-trainer-intro.png`, `ordinary-trainer-recovery-pass.png` |
| Saffron Gym and teleporters | PASS official Sabrina NPC present, companion suppressed, native teleport-pad sequence; `gym-entry-check.png`, `sabrina-win-field.png` |
| Sabrina challenge art | PASS male solo art against Sabrina; no companion beside player; `gym-battle120.png` plus battle-policy observation |
| Sabrina victory | PASS original three-Pokemon battle/dialogue, Marsh Badge bit 0x20, companion resumes outside; `sabrina-win-field.png`, `sabrina-resumes-after-victory.png` |
| Sabrina loss | PASS normal home whiteout, badge byte 0x00 and defeated-trainer bit clear, joined flag retained, companion restored; `sabrina-loss-recovery.png`, `loss-companion-rejoined.png`; challenge remains available by original flag/script logic |
| Early scripted NPCs | Lab aide and post-starter Lyra scripts finish; suppression/recovery observed; final-ROM lab exit/Lyra run plus earlier captures |
| Fresh game, naming, starter, designs | Oak/home/Elm introduction, player-entered name, starter, male field art, both selection designs and white-haired Lyra visually checked on prior stabilization ROM; subsequent runtime changes affect companion walking only, with art preservation verified |

Battle art remains presentation only: Sabrina takes no turns, and the native
Pokemon retains its identity. No battle calculations or Gym reward scripts were
changed. Existing combined and solo art is reused; no art was recreated.

## Bugs found and corrected

1. Record only vacated Pokemon tiles: its native previous coordinates reset to
   its occupied tile when it stops, which previously made Sabrina disappear.
2. Wait for transient native Pokemon footprint reservations instead of dropping
   and respawning at ordinary corners. A bounded timeout preserves safe recovery.
3. At an idle corner, face the adjacent Pokemon without requiring another step.

Only `src/field/sabrina_companion.inc` changes runtime behavior in this follow-up.
Host regressions exercise these observed failures.

## Setup, persistence evidence and limits

Late-game scenarios use our own authored CPDEX starter-save fixtures. These supply
location, Bicycle, Old Rod, Fog Badge, fast text and optionally a level-100
Feraligatr with test stats and Crunch/Surf. Loss setup uses HP 1 and depleted PP.
A native Repel counter avoids random battles during the ledge case.
Rod registration and the Pokegear prerequisite were supplied only in isolated
fixtures. These establish test preconditions, not proof of normal full-game
progression. No user save, ROM rule or story script was modified for fixture setup.

The newest town battery sector has counter 2, valid CRC and joined status, with
active saved IDs `[255,253,0,1,2,5]`. Its older lab backup has counter 1 and IDs
`[255,0,2,253]`. Both omit transient Sabrina 252 as intended. Native Continue loads
the battery save; the controller recreates one human once a safe trail exists.

The clean smoke run has no failed assertions. Exploratory logs are also retained,
including failed expectations while scripts/menus were active, movement was
blocked, transitions had not completed or insufficient walking had occurred.
Those attempts were investigated and rerun with valid preconditions; they are
not counted as passes. Union Cave transitions required additional wait frames.

Still unverified: Manic EMU on iPhone; exhaustive ledges/stairs/narrow geometry;
all special actions/disguises; every save/action combination; Sabrina rematch
in gameplay; all Silver/Rocket/League/Kanto cutscenes; full-duration progression.
Safe temporary hiding remains intentional. Sampled maps cannot establish universal
clipping or softlock prevention.

`VALIDATION.json` and `gameplay-20261103/checkpoint.json` are historical checkpoints.
Use [GAMEPLAY-VALIDATION.json](GAMEPLAY-VALIDATION.json) for this candidate,
[REPRODUCING.md](REPRODUCING.md) for automation recovery and
[MANIC-EMU-CHECKLIST.md](MANIC-EMU-CHECKLIST.md) for remaining device checks.
