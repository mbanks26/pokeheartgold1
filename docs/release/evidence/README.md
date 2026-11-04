# Reading the evidence

`native-index.json` identifies every newly tested scenario group, its actual
ROM SHA-1, authored prerequisites and selected result/image files. `native/`
contains complete useful input traces and console logs compressed with gzip;
these are sufficient to distinguish native input from authored save setup.
Full emulator RAM dumps/states are excluded because they contain game data.

The baseline files at this directory's top level were saved in checkpoint
66a6be90. The `final-*` host/static reports were rerun against the final source.
The clean build and subsequent two text/script build logs are compressed here.
`final-equivalence.json` describes exactly what changed between tested ROMs.
`patch-validation.json` records a complete independent BPS decode and checksums.

Some native scenarios began as scratch scripts and were subsequently consolidated
into the portable CLI tools. The captured traces/results describe the runs
actually performed; this is not a claim that every consolidated CLI was rerun
against every ROM. Native input, host stubs, static checks and inherited historical
evidence have distinct coverage levels in the report.

Exploratory fixture/automation failures are not relabeled as ROM bugs. Corrected
successful cases are retained here: valid DSV import and native sector counters,
actual Medicine-pocket selection, native Gym badge semantics and correct
subtrainer IDs. Earlier exploratory logs remain in the workspace.

Screenshots are headless DeSmuME captures. None is an actual Manic EMU or iPhone
capture. No full campaign completion, exhaustive AI behavior, comparative FPS
or arbitrary old-save compatibility is implied.
