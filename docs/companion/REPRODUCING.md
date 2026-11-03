# Recovering the headless gameplay checks

These instructions are for a future Codex workspace. The iPhone user does not
need a terminal. The playable deliverable is the BPS patch linked in README.md.

## Protected inputs

- Current source branch: `development/sabrina-gameplay-validation-20261103`.
- Runtime fixes: `bc2f6a1e`; prior stabilization: `2acac167`.
- Build a separate directory with the existing managed toolchain, HEARTGOLD,
  `meson/cross_unix.ini`, `meson/native.ini`, wrap-mode nopromote. Consult INSTALL.md
  and existing recovery setup instructions when provisioning a replacement machine.
- Activate `/workspace/.setup/activate.sh`, then build the explicit
  `ninja -C build/sabrina-gameplay-validation pokeheartgold.us.nds` target.
  The generic all-target route also selects an unrelated host SDK assembly target
  and fails on `-wrap:sdk`; it is not the verified ROM build route.
- Expected ROM SHA-1: `5cbf4223b6b1a02ccee28fd276e86281fff61291`.
- Never use another build's emulator state. Use native battery saves instead.

## Emulator and frontend

The tested core is [libretro/desmume](https://github.com/libretro/desmume), commit
`95b4d798731caa809125b6c3c11d17cc332ff6ef`, built from its GitHub source archive.
Archive SHA-256: `279d6f75852f406c3af24f9323944deb51ea7a7d5438f8108a62ce2951aed80c`.
The locally built core SHA-256 was
`554e67b3f5ba12f83fbe2bac2189c94c9224b85dbd82d14f00fba8303bd7ed08`;
compiler/platform differences may produce another core binary hash.

The core reports DeSmuME 0.9.12, x64 JIT. Build in
`desmume/src/frontend/libretro` with `make -j4 platform=unix`. This environment
needed local libpcap development headers and links to libGL/libpcap/pthread;
packages were extracted into work directories without replacing the existing
system/toolchain. No downloaded Nintendo BIOS or firmware is required: the test
uses the core's HLE firmware/BIOS and software rasterizer.

`tools/companion_emulator_runner.py` is a small libretro ctypes frontend requiring
Python, numpy and Pillow. It supplies deterministic frame-counted buttons/touch,
captures screenshots, reads actor/flag RAM using the matching `main.nef.xMAP`,
checks expectations and exits nonzero on any failed command. It logs core/ROM
hashes. Raw RAM writes are disabled unless `--allow-fixture-writes` is explicit.
Save states have ROM-hash sidecars; cross-ROM state loads are refused.
It has no GUI, audio timing or Manic EMU coverage.

## Reproducible ordinary-save smoke

Create a new isolated directory. Decompress
`tests/fixtures/companion/town-after-following.sav.gz` to `smoke.sav` there, and
copy/hardlink the matching test ROM to `smoke.nds`. Do not share `.dsv` or `.sav`
paths with a user's game. The core auto-imports the raw `.sav` on first boot.
Run the frontend with these arguments and JSONL stdin:

```
python3 tools/companion_emulator_runner.py \
  --core /path/to/desmume_libretro.so \
  --rom /isolated/test/smoke.nds \
  --symbols build/sabrina-gameplay-validation/main.nef.xMAP \
  --output /isolated/test \
  < tests/scenarios/companion_smoke.jsonl
```

Supply LD_LIBRARY_PATH if the extracted core dependencies require it. The checked
run has 18 commands, seven assertion groups and exit 0. It boots through native
Continue, creates one independent human after walking, verifies exact formation
and facing east/south/west/north, samples motion and 180 stationary frames, then
tests same-ROM state restore. Published traces are under gameplay-20261103/.

The fixture manifest records SHA-256 of each decompressed 512 KiB save. These
are authored CPDEX test saves from our own new game, not user progress or ROM
assets. The lab fixture is a genuinely saved starter game; the town fixture
contains a genuinely saved later counter and the earlier lab backup.

## Late-game scenarios

`tools/make_companion_test_fixture.py` creates a new, isolated save from a
decompressed starter fixture and refuses to overwrite its source or output.
The checked save layout comes from native SaveData array headers. The generator
validates source CRC, relocates player/native Pokemon, removes stale NPC records,
supplies action prerequisites, re-encrypts Pokemon data where requested and
updates save checksums. It emits a setup/hash manifest beside its output.

Example: `python3 tools/make_companion_test_fixture.py starter.sav actions.sav
--map 60 --x 698 --z 400 --battle-ready`. Use a single shell line when executing.
Map 60 is New Bark, 59 Saffron, 33 Route 29 and 36 Route 32. Native entry into
Saffron Gym and Union Cave is used after fixture placement outside. These saves
shorten access to scenarios; they do not prove normal progression to those maps.

Controls are JSON lines such as `{"frames":48,"buttons":["RIGHT"]}` and
`{"frames":120,"inspect":true,"shot":"result.png","expect":{"counts":{"252":1,"253":1}}}`.
Touch coordinates are bottom-screen native 256x192 coordinates. `talk` presses
A with release intervals while a field task remains active. Wait for transitions
to finish before asserting. A blocked player cannot establish a fresh trail.

For loss testing, the isolated party was set to HP 1 and zero move PP using the
same native checksum/encryption scheme; native Struggle/whiteout then ran without
ROM modifications. Fishing registration and a Route 29 Pokegear prerequisite
were fixture-only RAM changes. Original gameplay scripts were untouched.

The compressed exploratory logs preserve failed expectations as well as successful
reruns. They are diagnostic sessions, not a zero-failure automated regression suite.
The separate clean smoke trace is the reproducible zero-failure automated run.
No ROM, RAM dump or emulator state is committed to GitHub.

## Native ledge regression

Create a new fixture using map 33, x 650, z 404 and `--repel-steps 250` (omit
`--battle-ready`); place it as `ledge.sav` beside a separate `ledge.nds` copy.
Run `tests/scenarios/companion_ledge.jsonl` with the frontend. The tested run has
12 commands, one final actor-count assertion group, zero errors and exit 0.
The player's native east-facing ledge jump is followed by a short grass walk;
formation finishes at player (655,2,404), Pokemon (654,2,404), Sabrina (653,2,404).
Temporary absence during the unsafe trail is accepted. The original scout without
Repel encountered a wild Pokemon before its final walking assertion; its failed
expectation is retained as an exploratory log, not reported as a ledge failure.
