# Final regression and playable test release

The final patch is [stage-e-release.bps](stage-e-release.bps), pushed with implementation
commit 6181ce5c on development/story-partner-integration-20261103 in
mbanks26/pokeheartgold1. Final ROM SHA-1:
4f4e203c2b52967d2739c762360ed0065b458d59. The protected master branch and earlier
commits, patches and working ROMs have not been reset, force-pushed or merged.

## Implemented scope

The New Bark lab approach establishes the player, his independently traveling sister
and Sabrina as an existing couple familiar to the family. The sister walks away;
Elm's original selection, player naming and native early progression are retained.
Selected encounters in Violet, Goldenrod, Ecruteak and Blackthorn provide optional
battles and a growing Marill/Pidgey-based team. A Day-Care breeder explains her Eevee
acquisition; later catch-up dialogue handles a missed scene. Eevee remains unevolved,
and the player's original Bill gift is untouched.

All three fresh Elm starter choices are genuinely shiny through native PID/OT rules.
Twenty-eight Sabrina conversations and selective Mother/Elm/Silver/Gym Leader/Rocket
acknowledgments respond to location and milestones. Stand still on foot and press
Select while Sabrina is present. Three selected native AI Multi Battles use separate
Sabrina teams; normal battles remain Singles. Her official Saffron Gym and rematch
teams, original Marsh Badge/Skill Swap rewards and Lance's battle remain intact.

The independent human follows the native Pokemon's vacated-tile history, with terrain,
height and occupancy checks. She hides during tasks and special actions, then returns
from a fresh valid walking trail. Joined status persists independently of her current
visibility, and the companion cannot permanently obstruct player/NPC movement. No
new save fields or Pokemon follower identity changes were introduced. The recovered
flags' daily-reset bug was fixed and documented in [RTC-PERSISTENCE.md](RTC-PERSISTENCE.md).

## Evidence and limits of each check

| Area | Evidence |
| --- | --- |
| Compilation | Verified ROM target builds; final and regression build logs retained. |
| Host controller checks | 90 assertions on real controller/queue/save/presentation code with engine stubs. |
| Conversation/input checks | 27 assertions and pagination/original common-text preservation. |
| Native shiny calculation | 300,000 PID generations; ordinary threshold remains 8/65,536. |
| Calendar persistence | 8,192 reset cases; native elapsed-day fixture clears B49 and retains B51/B5F. |
| Partner data | All 44 explicit moves legal by actual learnsets/TMs; separate native parties and 0x4B setup decoded in all three encounters. |
| New game and starters | Native opening/Mother/Elm scene and each original choice; all three saved and cold-loaded as genuine shinies. See Stages A/C. |
| Sister journey | Native Eevee event/save and three optional victories in authored location fixtures. Bill gift script unchanged. See Stage B. |
| Ordinary battles | Captured combined male/Sabrina back art in a normal wild Single; original battle calculations unchanged. |
| AI partner control | In the Well fixture the player used only non-damaging Screech; Kadabra defeated the opponents. Native victories set B52/B53/B54; original Well transition and Basement Key occur. |
| Partner restoration | Well/Tower corrected fixtures restore protagonist -> native Pokemon -> Sabrina. The final-release Saffron driver wins, restores formation, saves, fully closes, cold Continues and restores exactly one of each follower. Native save counter 5 and CRC pass. |
| Official Sabrina Gym | Native Trainer Single type 0x1, trainer 258, Espeon 53/Mr. Mime 53/Alakazam 55. Combined art disabled; Marsh Badge and TM48 quantity 1 awarded. |
| Gym defeat | Authored 1HP/zero-PP player fixture loses normally; no Marsh Badge or defeated-trainer flag is set. Joined status remains; native WhiteOut completes and both followers return. |
| Retry availability | Original loss/challenge script is byte-identical; native eligibility flags remain clear. The full return journey from the fixture's New Bark respawn to Saffron has not been replayed. |
| Save/load status | Native joined save retains Eevee progress; disabled save cold Continues with no Sabrina. Final release cold-loads the disabled status correctly. |
| Shiny animation/evolution | Genuine shiny Chikorita sparkle captured. A level/experience setup using original IVs/EVs/nature reaches native level 16 in a wild Hoothoot battle, evolves into shiny Bayleef, saves and cold-loads on the final release. PID 878592113, OT 3484597151, shiny XOR 2 remain unchanged. |
| Graphics preservation | All 6,013 pre-existing graphics files, first 95 back-archive members and original 738 trainer records preserved. Conversion for appended partner backpic 19 passes pixel roundtrip. |
| Patch | Own roundtrip and independent RomPatcherJS source/target CRC and output SHA-1 checks pass. |

Full battle scenarios and Gym win/loss ran on c794f957edb5656e7298b50548afcaf4a5497c25.
The release then corrected one Azalea conversation predicate to use the original Well
completion flag even when Sabrina was absent. All game-resource files and battle/AI
overlays remain identical; [equivalence details](release-regression-equivalence.json)
record linker relocations. Final-release native checks cover that dialogue, evolved
shiny loading, deactivated loading, and the full Saffron practice/save/Continue case.

These are headless DeSmuME 0.9.12 libretro JIT/HLE scenarios with captured screenshots,
not actual iPhone gameplay or a complete campaign. High-level parties, late-game
prerequisites, relocation and the defeat/evolution setup were authored test fixtures.
Exploratory logs retain failed placement/cycling expectations; corrected release
scenarios pass independently. The native-UI practice driver writes no battle results
or Pokemon data: it commands only the player's Crunch and lets Sabrina's AI act.

## Remaining gameplay review

- Test in Manic EMU: complete Johto/Kanto progression, all cutscenes, long running,
  narrow passages, cycling/surfing restoration, map connections and NPC traffic.
- Review partner art: the new slot reuses existing front/profile psychic poses.
  A dedicated newly drawn rear/throwing sheet is absent. All original art is retained.
- Native AI is not guaranteed optimal. Full switching/faint/target edge cases and
  all rematches have not been exhaustively played.
- Actual link trading is untested (headless Wi-Fi is disabled). Cyndaquil/Totodile
  evolution has not been played; all three choices and their save/load data were tested.
- Original required Lyra tutorials and much phone dialogue remain stock; broader
  sibling wording and story pacing need campaign review.

Use [the iPhone checklist](MANIC-CHECKLIST.md). The new-game opening and shiny guarantee
apply at fresh starter selection; existing saves keep their Pokemon and original
progress. Native battery saves transfer across versions; emulator save states require
the exact ROM. Earlier flags already erased by an old daily reset need a backup or
the sister's catch-up encounter, as explained in the compatibility report.

See [changed source/assets](CHANGED-FILES.md), [flags and control API](FLAGS.md),
[AI implementation](STAGE-E.md), [graphics references](partner-graphics.json),
[preservation](final-preservation.json), [patch checks](independent-patch-checks.json)
and [regression evidence](stage-f-evidence/). Authored small save fixtures and their
checksums are in tests/fixtures/story/regression-manifest.json; they are CPDEX test
progress, not user playthrough saves.

## Reproduction for a future cloud workspace

Use the verified pokeheartgold.us.nds target with the existing toolchain; generic
Ninja 'all' also includes unrelated host SDK utilities with a known wrapper issue.
No additional gameplay source changes were made during this final regression stage.
The native UI driver tools/check_sabrina_practice_roundtrip.py accepts the core, ROM,
matching symbols and isolated output directory. Its practice-input fixture supplies
only authored prerequisites; the driver wins through native controls, checks a real
battery save, closes the core and uses a new process for Continue. Full RAM/ROM states
are kept in the workspace, not committed. Previous working ROMs are preserved, and
older generated symbol/RAM captures have verified lossless gzip archives.
