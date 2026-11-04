# Stage E — Sabrina's native AI partner battles

Three selected encounters use HeartGold's existing Trainer + Doubles + Multi + AI
format (0x4B), with a separate Sabrina party in BATTLER_PLAYER2. The player commands
one of their own Pokemon. Sabrina uses the native trainer AI, configured with flags
7 plus the engine's automatic doubles logic. No scripted move sequence, player
control of Sabrina's moves, battle calculation changes or Pokemon identity swaps
were introduced. Ordinary battles remain Singles, and Lance's event is unchanged.

Encounters and separate teams:

| Encounter | Sabrina | Opponents |
| --- | --- | --- |
| Slowpoke Well | Kadabra 16 | Original Proton team + Grunt's Rattata 11 |
| Radio Tower fake Director | Alakazam 32, Mr. Mime 30 | Original Petrel team + Grunt's Raticate 27 |
| Optional post-Marsh Saffron practice | Alakazam 50, Mr. Mime 48 | Psychic students Rei and Nori, two Pokemon each |

The students stand beside the Gym approach at 1331/1332,209. Talk from the road
beside the flower pots. Practice requires Sabrina joined and the Marsh Badge;
declining is supported, and victory is recorded once. Sabrina's official Gym and
rematch teams remain unchanged. When Sabrina is disabled, Well/Tower retain their
original Single Battles and original loss/progression branches.

All 44 specified moves pass checks against the actual level-up and TM/HM data.
Abilities use native selection, trainer difficulty is 100, and no battle-only stat
advantages were added. The three native runtime setups were decoded to verify
0x4B, distinct trainer IDs, separate parties and one Pokemon in the authored player
fixture. During the Well check the player used only Screech (PP 40 to 37; all
other move PP unchanged), while Sabrina's Kadabra defeated the opponents. This
verifies independent AI actions rather than merely displaying a second sprite.
Native AI can still make imperfect choices or lose an intended target when the
player knocks it out first; smarter prediction has not been added.

Native victories set B52/B53/B54. Well preserves the original Kurt-house transition;
Tower awards the original Basement Key (quantity 1). Corrected fixtures verify the
three-member formation after Well and Tower. The general controller hides Sabrina
during battle/script tasks and recreates her from a fresh safe Pokemon trail.
Additional save/load, defeat and final field regressions are recorded in Stage F.

For the partner presentation, backpic 19 appends five members to the archive. All
95 previous members, including combined ordinary-battle art and solo male art,
remain byte-identical. The new layout repeats Sabrina's existing three front/profile
psychic poses; it does not redraw or replace any existing character PNG. Conversion
and NCGR/OAM pixel roundtrip pass. A dedicated newly drawn rear/throwing sheet is
still absent, so partner presentation needs visual approval in Manic EMU.

Compilation passes. Full battle scenarios ran on ROM
c794f957edb5656e7298b50548afcaf4a5497c25. The final release is
4f4e203c2b52967d2739c762360ed0065b458d59: its only subsequent source adjustment
uses the native Slowpoke Well milestone for Azalea dialogue, including saves where
Sabrina was absent from that battle. All game-resource files and battle/AI overlays
are identical between these ROMs; other overlay changes are linker relocations.
Release-native checks verify that dialogue condition, evolved shiny battery-save
loading, and persistent deactivated companion loading.

Host checks pass 90 companion assertions, 27 conversation/input assertions, 300,000
native shiny-PID cases, 8,192 daily reset cases, and partner legality/architecture
checks. All 6,013 existing graphics and original 738 trainer records are preserved.
Evidence logs include exploratory position/cycling assumptions; those failed
expectations are retained and are not counted as successful gameplay checks.
Late-game locations and high-level player teams were authored test fixtures,
not a complete ordinary campaign playthrough.

Use [the final patch](stage-e-release.bps) with your own clean US HeartGold ROM
(SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37). See the [iPhone checklist](MANIC-CHECKLIST.md),
[RTC/save compatibility fix](RTC-PERSISTENCE.md), [native parties](native-partner-parties.json),
[victory flags/reward](native-partner-completion.json), [graphics conversion](partner-graphics.json)
and [preservation audit](stage-e-preservation.json). Actual Manic EMU, link trading,
full campaign pacing, all cutscenes and every AI switch/target situation remain unverified.
