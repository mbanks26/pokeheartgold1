# Stage C — Genuine shiny starters

Only Elm's three starter candidates use GenerateShinyPersonality with the player's
actual original Trainer ID. CreateMon receives that legitimate fixed PID/OT pair;
all other initialization, level 5, random IVs, starting moves, ability, nickname
choice, met information and normal starter event remain native. Unchosen candidates
are discarded normally. No species sprites or shiny palettes were edited.

The ordinary Pokemon factory and wild encounter source are byte-identical to the
protected baseline. A host test compiles the actual native generator/check and
validates 300,000 generated PIDs plus the unchanged 8/65,536 shiny XOR threshold.
One explicit unsigned-shift cast adapts native bit transport for host UBSan only;
the game's existing generator is not changed. All original Trainer records,
including Silver's, remain unchanged; NPC shininess is not forced.

DeSmuME completed each native choice: Chikorita 152 (Overgrow 65, Tackle/Growl),
Cyndaquil 155 (Blaze 66, Tackle/Leer), Totodile 158 (Torrent 67, Scratch/Leer).
All are level 5, retain the actual player OT ID, have valid encrypted checksums,
and yield genuine shiny XOR values 2, 4 and 6. Natural shiny previews and native
Pokemon following appeared. The initial left/right test-directory labels were
corrected after decoding the actual selection: left is Totodile, right Cyndaquil.
Published evidence is labeled by actual species, not those scratch directories.

Each choice was natively saved as counter 3, fully closed and loaded through
Continue in another emulator process. Species, level, moves, ability, PID, OT,
checksum and shiny status remain identical; safe walking recreates exactly one
native Pokemon and one Sabrina. The three compressed native battery saves are
retained as authored fixtures. They contain CPDEX test progress, not user saves.

ROM SHA-1: 333f655dccebb1f753fa6c8346fb88ef9895e76d. Compilation and the
90-assertion companion suite pass. [Pokemon data](stage-c-pokemon-data.json),
[evidence](stage-c-evidence/) and [test patch](stage-c-shiny-starters.bps) are retained.

Shininess is ordinary stored PID/OT data, so native trading/evolution can preserve
it without a permanent cheat flag. Actual evolution, a shiny send-out in battle,
link trading and Manic EMU remain pending further gameplay checks at this checkpoint.
