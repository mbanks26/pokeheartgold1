# RC1 milestone coverage

This report separates **new independent testing** from inherited Codex reports.
No complete campaign or actual Manic EMU playthrough was performed. A forced
late-game test save is evidence for the isolated event only.

## Evidence levels and tested versions

- **Fresh native**: DeSmuME inputs from a blank battery save, no runtime progress writes.
- **Isolated native**: actual emulator/UI/game logic, with prerequisites authored
  in a documented CPDEX test save. Does not validate the preceding journey.
- **Inherited native**: earlier captured scenario, inspected but not replayed in
  this assignment. Retained in `docs/story/`; not credited as a new pass.
- **Static/host**: source, data, actual packaged resources or host tests with engine
  stubs. Cannot prove that a scene is reachable or a route is softlock-free.
- **Not run**: no adequate gameplay evidence for the specified sequence.

| ROM | SHA-1 | New tests |
| --- | --- | --- |
| Clean-directory custom baseline | 4f4e203c2b52967d2739c762360ed0065b458d59 | Both openings, male progression to Cherrygrove, three starter choices/save/cold, Gym win/loss, actions/cards, daily callbacks |
| First dialogue candidate | 7e4e21c5945a4f7eaab887adebc21a9042b9d840 | All three native evolutions, Dojo rematch, joined/disabled Goldenrod dialogue |
| Final RC1 | 9670376e2a700d5c910648e18304ca3193c33e9c | Fresh female/save/cold, female Goldenrod guard, joined/disabled Goldenrod/save/cold, all three evolved save loads, ledge, held-B movement, complete late partner victory/save/cold |

Actual-ROM comparison proves ARM9 byte-identical across baseline and final, with
382/384 resource files unchanged. Only script member 885 and messages 581/612/629
changed. Thus the earlier scenarios exercise the same graphics, engine, battle
and trainer resources; they are still labeled with the ROM actually tested.

## Opening, Johto and League

| Milestone | Independent evidence and remaining gap |
| --- | --- |
| Oak introduction / male selection / selectable name | Fresh native baseline; custom art and CPDEX name entered normally. |
| Female selection / selectable name | Fresh native baseline and final; custom art, native progression guard. |
| Mother / Marill / lab approach / sister and Sabrina / Elm | Fresh native both genders, female added actors suppressed; male relationship opening completes. |
| Each shiny starter | Isolated native selection, save and new-process Continue for all three; genuine shiny PID/OT, ordinary level/moves/ability. |
| First Pokémon and Sabrina followers | Fresh male native one each; fresh female native Pokémon only. |
| Early sister encounter / Pokégear / Elm phone / Route 29 | Fresh male continuous native inputs; original events complete. |
| Wild battles / level-up / move learning | Fresh male native wins; Chikorita level 6 learns Razor Leaf. |
| Cherrygrove Guide Gent | Fresh male continuous native tour, save, complete close and cold Continue; both followers return. |
| Mr. Pokémon / Pokédex / Egg delivery | Static preservation; **not played from fresh save**. |
| Early Silver battle / rival naming | Custom acknowledgment/source reviewed; **not freshly played**. |
| Catching tutorial / required counterpart events | Native dispatch/event entries retained; **not freshly played**. |
| Sprout Tower | Static only; no end-to-end navigation/boss test. |
| Falkner / Zephyr Badge | Static native progression and custom greeting reviewed; no new gameplay test. |
| Slowpoke Well / Bugsy | Earlier isolated partner victory and native Well transition inherited; Bugsy progression not newly played. |
| Ilex Forest / Farfetch'd / Cut | Static only. |
| Goldenrod / Whitney | Isolated final sister/breeder interaction tested; Gym and city progression not played. |
| Burned Tower / Morty | Static dialogue/progression reviewed; no new gameplay test. |
| Ecruteak sister | Dialogue reviewed/formatted; earlier optional battle inherited; final new replies not all visually played. |
| Olivine Lighthouse / Jasmine | Static only. |
| Cianwood / Chuck | Static only. |
| Whirl Islands / legendary sequence | Static only. |
| Lake of Rage / Rocket Hideout / Pryce | Static only; no complete Rocket sequence test. |
| Radio Tower / Petrel partner event | Earlier isolated AI victory, Basement Key and restoration inherited; no complete Tower takeover replay. |
| Ice Path / Blackthorn sister / Clair | Static source/team/dialogue review; earlier optional sister battle inherited; no full Ice Path/Gym test. |
| Dragon's Den | Static only. |
| Routes to League / Victory Road / Silver | Static only. |
| Will / Koga / Bruno / Karen | Static only; no new League battles. |
| Champion Lance / Hall of Fame | Original Lance script protected byte-for-byte; **not played**. Authored GameClear is only a reset-persistence test. |

## Kanto and postgame

| Milestone | Independent evidence and remaining gap |
| --- | --- |
| S.S. Aqua / arrival in Kanto | Static only. |
| Lt. Surge / Thunder Badge | Static only. |
| Erika / Rainbow Badge | Static only. |
| Janine / Soul Badge | Static only. |
| Sabrina / Marsh Badge | Isolated native Gym door/teleporter puzzle, original trainer 258 Single, win/reward and loss/whiteout. Authored high-level party/location and four subtrainer flags. Not natural Kanto arrival. |
| Sabrina loss retry | Native loss retains joined status and no badge/TM; script remains retryable. Complete return journey and second challenge not played. |
| Sabrina Dojo rematch | Isolated native trainer 725 Single, six original Pokémon, win, appointment clear, restore/save/cold. Appointment/location authored; natural phone acquisition/weekly timing not tested. |
| Misty / Cascade Badge / Cerulean | Static only. |
| Power Plant / Machine Part / Radio Card | Static only. |
| Brock / Boulder Badge | Static only. |
| Blaine / Volcano Badge | Static only. |
| Blue / Earth Badge | Static only. |
| All badges / Mount Silver access | Original gates retained; actual acquisition/access not played. Setting all badges in a reset fixture is not this test. |
| Red | Static only; encounter and victory not played. |
| Other Gym rematches / optional activities | Original entries retained; not exhaustively played. |

## Cross-cutting feature checks

| Area | Independently tested | Remaining gaps |
| --- | --- | --- |
| Companion trail | Corners/stops, eight repeated loops, native ledge, held-B movement, early route connection, doors, Gym/Dojo transitions, post-battle restoration; host controller terrain/timeout/object lifecycle cases. | All narrow passages, bridge heights, NPC traffic, stairs/caves and prolonged running not exhaustive. Held-B test does not measure speed/FPS. |
| Special movement | Native cycle/dismount, Surf/land, rod cast/close; Sabrina suppresses/restores and native Pokémon remains independent. | Fly/teleport/HM/puzzle permutations, actual fishing catch and all disguises/special animations not played. |
| Cutscenes | Fresh opening, Mother/Elm/sister, Guide Gent; native task suppression and host guards. | Full Rocket/League/Kanto approaches, every scripted player/NPC movement not played. |
| Ordinary battles | Fresh male wild wins and level-up; isolated official Sabrina/rematch Singles, late Multi victory. | Every battle type, link, Frontier, general Double battles and all combined-art poses not visually exhausted. |
| Partner AI | Final native late practice uses only player Crunch; Sabrina acts independently; legal 44 moves/seven records and native AI routing pass host/static checks. Earlier Well Screech-only AI victory/Tower evidence inherited. | Fainting/switch/target/status/ability/EXP/reward/loss edges not exhaustive. Native retargeting may waste a Ghost move on a Normal immunity. |
| Shiny evolution | All three first evolutions via native Rare Candy UI, original PID/OT retained, native save/cold; final ROM cold-loads all three. | Final-stage evolutions, link trading and every shiny animation not played. |
| Saves | Real saves, full core close/new-process Continue, joined/disabled state, female guard, Eevee flag, evolved data, partner victory, Gym outcomes/rematch; native CRCs. | Cold loading while still cycling/Surfing or mid-script was not specifically tested. Arbitrary old user saves and repeated real hardware clock transitions not exhaustive. |
| Daily/weekly reset | 1/8 elapsed-day callbacks with stored clock authored; B49 clears, B50–B57 and B5D/E/F persist; native save/cold. 8,192 host reset cases. | Actual week-long play, daylight-saving/time rollback and all native weekly content not tested. |
| Character assets | 6,013 preserved source graphics; packaged custom pixels/palettes/metadata, archives, eight intro slots; native openings/cards/selected battles and field actions captured. | Stock 3D Bag models remain. Not every action/frame/palette visually checked. Native idle cells can share addresses. |
| Female route | Final fresh opening/save/cold and Goldenrod native door/breeder/neutral dialogue/save/cold, no sister 240 or human 252 and no false Eevee flag. | Entire female campaign and all original phone/tutorial counterpart wording not played. |
| Performance | Representative native scenarios completed without a measured stall. | Paired clean/custom benchmark was incomplete after disk exhaustion; no comparative FPS or Manic performance claim. |

The available automation drives native inputs and isolated save fixtures; there
is no verified end-to-end campaign navigator. A bounded fresh run reached the
Cherrygrove tour. No naturally completed compatible late-game save was recovered;
late fixtures therefore state their authored prerequisites explicitly. Disk
pressure also prevented completing the optional paired performance benchmark.
These are specific limits, not passes or evidence that unplayed content is broken.

See [evidence index](evidence/native-index.json), [host results](evidence/final-host-regressions.json),
[static story audit](evidence/final-story-audit.json), and the [Manic checklist](MANIC-CHECKLIST.md).
