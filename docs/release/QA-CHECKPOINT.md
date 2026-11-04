# Validated source checkpoint — 4 November 2026

Final test ROM: SHA-1 `9670376e2a700d5c910648e18304ca3193c33e9c`.
The following archive commit will attach the reproducible BPS patch and final
player-facing report. This checkpoint contains all source and test tools for it.

Four game-source files changed after the recovered story/partner milestone:
Goldenrod's shared sister/breeder script and message bank, plus the Ecruteak and
Blackthorn sister message banks. The fixes prevent Sabrina speaking while
deactivated, prevent female-route breeder interactions from awarding male-story
Eevee progression, and vary repetitive sister replies. All three custom designs,
battle engine, companion engine, trainer rosters and save structures are preserved.

All six final host regression suites pass. A new-directory build completed
9,670 steps; the final script/text rebuild completed 2,135 steps. Actual-ROM
comparison proves unchanged ARM9 and 382/384 resource files; only script member
885 and message members 581, 612 and 629 differ from the rebuilt baseline.

The evidence archive records eighteen scenario groups with each tested ROM hash
and authored prerequisites. It includes genuine shiny choices and native
save/cold load for all three starters, native evolutions and final-ROM evolved
save loading, simultaneous followers, cycling/Surf/fishing restoration,
corners/ledge/held-B movement, native Trainer Cards, daily callbacks, Gym
win/loss, a Dojo rematch, late AI partner victory/save/cold load, and the female
Goldenrod fix. An independently replayed fresh male game reaches Cherrygrove's
Guide Gent; this is not a full campaign playthrough.

Known appearance limitations remain: stock 3D Bag models and reused Sabrina
partner front/profile poses. Full Johto/Kanto/Mount Silver, natural rematch phone
scheduling, exhaustive partner AI edge cases and actual Manic EMU remain
unverified. No known critical or major regression was established in the tested
scenarios; untested progression is not certified.

See [native evidence index](evidence/native-index.json),
[final host results](evidence/final-host-regressions.json),
[asset audit](evidence/final-assets.json), and
[source/ROM equivalence](evidence/final-equivalence.json).
