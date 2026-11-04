# HeartGold RC1 — final integration and QA report

**Result: reproducible experimental candidate for a comprehensive player test.**
Three minor route/dialogue defects are fixed. All final automated checks pass,
the ROM builds, and the new BPS reproduces it exactly in two decoders. No known
critical or major regression remains in the tested scenarios. A complete
Johto–Kanto–Mount Silver playthrough and actual Manic EMU test were not completed;
RC1 is not certified as a fully tested campaign.

## 1. Repository and branch

The actual recovered project is **mbanks26/pokeheartgold1**, branch
`development/release-candidate-20261104`. Both repositories and all available
remote branches were inspected. The separate pokeheartgold repository has only
master 8cbb4a19 and lacks the custom project. The latest feature head recovered
was 110f4acf4a97c185192467dbc27b1f05ff6d39d0, after bcf2f8fd. Sabrina afd4151f,
male bda9631d, female 2c669251 and prototype 4ea2dc8a are verified ancestors.
No feature needed recreation or a speculative merge. See [branch audit](AUDIT.md).

## 2. Commit and recovery checkpoints

Initial independently validated QA checkpoint:
`66a6be90c36449248b1fd5826a31f09cbd96fb77`.
Final game-source/test checkpoint: **`507ca40db6d692683746ccf318e910e321eb48d7`**.
The Git commit enclosing this document, manifest and BPS is the final archive
commit; its exact SHA is shown in the GitHub commit page and delivery message.
This avoids placing an impossible self-referential commit hash inside its tree.
All checkpoints are fast-forward history on the development branch. Master stays
at 3fea383f5a229391d12ef3429f8095177638a44d; no reset, force-push or master merge.

## 3. Features confirmed in source

Custom graphics; New Bark family/companion opening; selectable player naming;
male-route sister encounters and Eevee; genuine shiny starter creation; separate
human companion plus native following Pokémon; 28 opt-in contextual Sabrina
conversations and selective NPC acknowledgments; three native AI partner
encounters; official Sabrina Gym/rematch role; saved activation and repaired
daily flags. Female route retains native progression with added relationship
events disabled. Presence in source is separate from gameplay reachability.
Current architecture, canon and flags are in [PROJECT.md](../../PROJECT.md).

## 4. Character graphics verification

All **6,013** existing graphics files and 95 back-archive members from milestone
bcf2f8fd are preserved; five subsequently appended back members and prior partner assets
remain. Actual-ROM audit checks 384 FAT files, 308 NARCs and 56,728 members,
custom texture pixels/palettes/native metadata, compiled battle/card archives
and eight custom intro slots. Native openings, both Trainer Cards, battle and
selected movement screenshots provide visual evidence. No art was recreated.

Editable previews: [male](../../characters/male/overworld.png),
[Sabrina](../../characters/sabrina/overworld.png),
[sister/female](../../characters/female/overworld.png). The designs remain the
brown-skinned dreadlocked red/white protagonist, black-green-haired burgundy
Sabrina and silver-white-haired red-eyed burgundy/black sister.

Limits: original Ethan/Lyra **3D Bag models remain**; partner backpic 19 reuses
Sabrina front/profile poses. Walking/run slots reuse established custom step
art. Some native idle texture cells share addresses, so conversion uses the
original effective last-write mapping rather than unique ROM cells for every
PNG cell. Special-action resources are integrated but not all frames/actions
have been visually played. See [asset audit](evidence/final-assets.json).

## 5. Story and dialogue audit

The static audit verifies all 965 original script-dispatch prefixes and 491
original event-collection prefixes, protected Bill/Lance/Gym/Dojo scripts and
32 native battle/AI files. It checks 69 changed/added English messages against
two-line/32-character page rules; this is not pixel-font or reachability proof.
Custom text was reviewed for relationship continuity, reserved warmth/dry humor,
chronology and repetition. Eight repetitive Ecruteak/Blackthorn sister replies
were varied. Goldenrod no longer gives absent Sabrina a speaking line.

Mother/Elm/Silver/select Gym Leaders/Rockets acknowledge her selectively. Native
required counterpart tutorials and much phone dialogue remain stock; a complete
sibling-language rewrite and all NPC scene staging were not attempted. No new
major story, reward, difficulty or gameplay system was introduced.

## 6. Sister and Eevee progression

Violet/Goldenrod/Ecruteak/Blackthorn encounters and optional battle guards exist.
Her team grows independently and retains unevolved Eevee; no Vaporeon was added.
Bill's separate gift is byte-identical. Earlier native acquisition/optional
battle evidence is retained as **inherited**, not a new full journey test.
New final-ROM Goldenrod joined/disabled interactions save/cold-load without
changing the acquired-Eevee flag, Bill flag or player Pokémon; no repeat reward.
The female-route shared breeder now uses neutral text without setting B51, and
native door entry/save/cold confirms no added sister/Sabrina objects.

## 7. All three shiny starters

Native selection/save/cold Continue passed independently for Chikorita, Cyndaquil
and Totodile. Native data is valid level 5 with normal species, moves and abilities:

| Choice | Native PID | Shiny XOR | First evolution tested |
| --- | --- | --- | --- |
| Chikorita | 1681199130 | 2 | Bayleef, level 16 |
| Cyndaquil | 1261846302 | 5 | Quilava, level 14 |
| Totodile | 884359323 | 0 | Croconaw, level 18 |

All share the actual CPDEX fixture OT 3484597151. Authored legal pre-evolution
level/EXP/stats and one Rare Candy supplied prerequisites; native item use,
evolution, real saves and new-process Continue preserved PID/OT/shininess for
all three. Final ROM cold-loads all evolved saves. Three previews were captured.
The 300,000-case native PID host test passes; ordinary wild threshold remains
8/65,536 and original trainer records, including Silver, are unchanged. No
global shiny forcing or cosmetic-only recolor. Final-stage evolutions and every
shiny animation are untested; existing saves' Pokémon are not retroactively changed.

## 8. Sabrina follower tests

Fresh male gameplay creates one Pokémon 253 and one Sabrina 252. Native tests
cover turns/stops, eight corner loops, ledge and held-B movement, early route
connection, several doors, Gym/Dojo warps, cycle/dismount, Surf/land, rod cast,
ordinary/partner battle restoration, save and cold Continue. Final ledge formation
is player 655 → Pokémon 654 → Sabrina 653 on the same row. Host checks exercise
terrain/occupancy, blocked timeout, lifecycle, suppression and exact-identity
non-solid behavior. No duplicate object was observed in successful scenarios.
Exhaustive narrow paths, bridge heights, all cutscenes/warps and prolonged play
remain unverified; temporary hiding must not be mistaken for loss of joined state.

## 9. Partner-battle AI

All three 0x4B Multi setups, seven separate trainer records and 44 legal moves
pass static/host checks; native AI source remains unchanged. The **final ROM**
late Saffron practice independently wins while the player commands only their
own Crunch, then saves, closes and cold-loads both followers and B54/B5F.
Earlier Well/Tower independent-AI victories and progression rewards are inherited
evidence, not rerun here. Native targeting is not guaranteed optimal; immunity
retargeting can waste a move. Status/ability/switch/faint/loss/reward permutations
and general Doubles are not exhaustive. No battle-engine rewrite was introduced.

## 10. Official Saffron Gym and rematch

New isolated native Gym tests enter through the door and teleporter puzzle,
challenge original trainer 258 in Single type 0x1, use solo player artwork,
win the Marsh Badge and one TM48, restore both followers and save. Separate
1HP/zero-PP prerequisites lose natively; no badge/TM, joined status survives
whiteout and both followers return. Four subtrainer victories/location/high-level
party were authored; no leader result or badge was injected. The original Gym
uses its badge rather than setting trainer flag 258; a false test assumption
was corrected without changing game logic.

A new isolated Dojo test loads the native Gym-victory save, authors only location
and a phone appointment, enters natively, finds one canonical Sabrina and no
human follower, fights original trainer 725 with six native Pokémon, wins,
clears the appointment, restores/saves and cold-loads both followers. Natural
phone acquisition/weekly scheduling, full loss-return-retry travel and all
rematch defeat permutations are not tested. Original Gym/Dojo scripts remain intact.

## 11. Johto coverage

Continuous fresh male gameplay reaches Cherrygrove's Guide Gent after original
Mother/Pokégear/Elm/Route 29 events, real wild wins and native level-up/Razor Leaf.
It saves and cold-loads there. **The eight Johto Gyms, full Rocket plot, League
and Champion were not played end-to-end.** Static preservation and inherited
isolated events are explicitly listed in [milestone coverage](COVERAGE.md).

## 12. Kanto coverage

Saffron Gym win/loss and an isolated Dojo rematch were independently played.
Arrival, other seven Gyms, Power Plant/Cerulean, all-badge acquisition, Mount
Silver and Red were **not played**. Original gates/scripts are preserved, which
does not prove full progression. See the Kanto coverage table.

## 13. Saves, reloads and daily reset

Six final host suites pass, including **8,192** native daily-reset cases. Native
1/8 elapsed-day fixtures clear ordinary B49 while B50–B57 and B5D/E/F persist;
joined/disabled state, authored all-badge/GameClear state and native save/cold
survive. This exercises native callbacks with a stored clock moved into the
past, not a real week of campaign play. Real save/cold checks also cover fresh
female, all starters/evolutions, Eevee, partner victory, Gym aftermath/rematch.
No save-format change. Native CRC validation/import replaces unsafe SAV-renaming.
Old already-erased story bits need a backup or supported catch-up; arbitrary old
user saves, clock rollback and every weekly event remain unverified.

## 14. Build, patch and checksums

A new-directory ROM build completed **9,670/9,670** tasks and matched the prior
release byte-for-byte. Final text/script rebuild completed **2,135/2,135** tasks.
The explicit HeartGold ROM target succeeds; generic host SDK `all` is not the
release target. Logs are archived in `evidence/`.

| Artifact | Size | SHA-1 |
| --- | --- | --- |
| Required USA rev 0 clean ROM | 134,217,728 | 4fcded0e2713dc03929845de631d0932ea2b5a37 |
| Final patched RC1 ROM | 134,217,728 | 9670376e2a700d5c910648e18304ca3193c33e9c |
| heartgold-rc1.bps | 3,957,611 | 4076fcf197034ab6ceda0cbae9595fb642644343 |

Patch SHA-256: `f61448b75042e8d17d77d5ed0d55e23163fcf8091d1a01ad764bc8652f6b0d90`.
ROM SHA-256: `2333089f68a9f29f633fd839b5a6b922a7bf9870ae45e326fb85274ee350c5b7`.
BPS CRC32 source/target/patch: `c180a0e9` / `f353ed65` / `e489726f`.
Own full byte roundtrip and independent Rom Patcher JS v20240821 produce the
identical ROM; incorrect base and corrupt patch are rejected. Full hashes and
metadata are in [patch validation](evidence/patch-validation.json).

## 15. Bugs found and fixed

1. Goldenrod could give Sabrina a line while deactivated: joined-status branch
   now selects a sister-only response; native final test passes both cases.
2. The female-route generic breeder shared the male sister/Eevee entry: a B5D
   guard now routes to neutral dialogue without rewards/flags; final native test passes.
3. Repeated sister replies across towns: eight lines now reflect her own training
   and experiences while retaining event/team logic and page limits.

Test-infrastructure fixes include proper DSV footer/CRC/no-overwrite import,
save-menu normalization and clearer cleanup/diagnostics. Failed exploratory
tests from wrong item-pocket selection, Gym-flag assumptions or fabricated
backup sectors were corrected as test issues, not production-game bugs.
See [changed files](CHANGED-FILES.md) for all game-source changes.

## 16. Remaining unverified behavior and blockers

No verified automated campaign navigator or naturally completed compatible
late-game save was available. A bounded fresh-input run reached Cherrygrove;
advanced fixtures author prerequisites explicitly. Full campaign, every special
action/cutscene, natural rematch scheduling and exhaustive AI edges remain gaps.
Disk exhaustion interrupted the optional paired performance comparison; verified
generated object caches and private RAM captures were losslessly compressed to
finish packaging. No comparative FPS claim. Actual Manic/iPhone gameplay was
not accessible from this cloud environment. See [coverage](COVERAGE.md).

## 17. Known issues by severity

| Severity | Issue/status |
| --- | --- |
| Critical | None established by successful tests; unplayed progression is not certified. |
| Major | None established by successful tests; same coverage qualification. |
| Minor appearance | Stock 3D Bag models can display Ethan/Lyra despite custom 2D art. Requires separate 3D artwork work; preserved here. |
| Minor dialogue | Some original required counterpart tutorials/phone wording remains stock rather than fully sibling-aware; campaign context review needed. |
| Minor tactics | Existing native AI retargeting can waste an immune move; no optimal-play guarantee. |
| Cosmetic | Sabrina's separate partner presentation reuses front/profile poses; dedicated rear/throw artwork absent. |

Coverage gaps are not counted as confirmed bugs. No core feature was removed to
improve a benchmark, and no new large quality-of-life system was added.

## 18. Downloadable patch

[heartgold-rc1.bps](heartgold-rc1.bps). It validates the exact clean USA revision 0
base and creates the tested 128 MiB ROM. Commercial ROM data, emulator full RAM
states and SDK binaries are not included in Git. Prior ROMs/patches are preserved.

## 19. iPhone installation and gameplay testing

Use the [Safari patch/import instructions](README.md#apply-on-iphone) and
[Manic checklist](MANIC-CHECKLIST.md). Download the BPS to Files, apply it to the
matching clean ROM using Rom Patcher JS, save under a new name and import into
Manic separately. Prefer a fresh save for story review; battery-save copies may
be imported, while old-version emulator save states must remain separate. No
terminal or desktop editing is required. Manic compatibility is not yet verified.

## 20. GitHub preservation

The source checkpoint and enclosing release archive commit are published on
`development/release-candidate-20261104` in **mbanks26/pokeheartgold1**. Source,
test drivers, fixture provenance, complete useful compressed traces, screenshots,
results, manifest, documentation and BPS are preserved there. Remote branch head
and unchanged master are checked at delivery. No prior commits/branches/patches
were overwritten and nothing was merged into master.
