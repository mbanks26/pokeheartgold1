# Stage A — New Bark opening and relationships

The original home/Marill sequence remains. Two additional existing-art NPCs wait
outside Elm's lab. Approaching the lab's only normal doorway starts their scene.
The sister walks down the path toward Route 29 before her object is hidden.
Sabrina steps aside and waits while the player visits Elm. The scene writes the
existing initialized/joined companion bits; native Pokemon following still begins
through Elm's unchanged starter event. Existing starter saves skip the opening.

Mother recognizes her daughter and Sabrina. Elm recognizes Sabrina and refers to
the sister's Marill. The post-starter tutorial retains its required behavior and
uses sibling dialogue. The protagonist's name is always the native player buffer.
New text is formatted for two-row message pages using the game's supported glyphs.

New storage: B50 opening complete (also hides its scene NPCs on future loads),
416F coordinate-trigger completion. B5E/B5F keep their previous meaning. No save
structure changes. Other reserved story bits are named for later stages but unused.

The runtime ROM code is unchanged in this stage. The separate ROM compiles; all
88 sanitized follower assertions pass. A new game was played through Oak's intro,
player-entered CPDEX name, Mother, native Marill scene, new opening, sister exit,
joined flag activation and Elm's introduction in DeSmuME. Lab access remains usable.
Normal Chikorita selection, nickname choice and native follower creation were
then completed. After safe walking, actor counts are one Pokemon and one Sabrina;
joined/initialized status remains true. The native pre-starter battery save has
valid sectors with counters 1 and 2 and is retained as a compressed test fixture.
Manic EMU is not tested.

ROM SHA-1: 805e990425d5a89b0bb3a5096a6c2cb9d74d03b6. The ROM ARM9 bytes match
the prior validated build exactly. This stage changes story resources only.
[Stage A patch](stage-a-opening.bps) and [emulator evidence](stage-a-evidence/) are retained.
