# Sabrina companion stabilization candidate

**Newer gameplay work:** [emulator findings and current candidate](GAMEPLAY-VALIDATION.md) on `development/sabrina-gameplay-validation-20261103`. The original report and patch below are retained as a historical checkpoint.

The recovered custom graphics and prototype are together in **mbanks26/pokeheartgold1**,
not the similarly named pokeheartgold repository. This work continues from
4ea2dc8a on **development/sabrina-stabilization-20261103**. The recovery checkpoint,
graphics/prototype branches, master and previous ROM builds are retained.

This candidate adds persistent joined status, a bounded walking trail, safe
removal/recreation, nonblocking collision behavior, map/task cleanup and conditional
paired/solo battle art. Original Pokemon following and story scripts are preserved.
Compilation and automated host checks do not establish full gameplay reliability.

- [Pre-edit history/prototype audit](AUDIT.md)
- [Implementation, flags, save compatibility and limitations](ARCHITECTURE.md)
- [Exact validation results and ROM/patch hashes](VALIDATION.json)
- [Existing art preservation](art-audit.json)
- [Recovered solo graphics references](graphics-preservation.json)
- [Manic EMU checklist](MANIC-EMU-CHECKLIST.md)
- [Changed files](CHANGED-FILES.md)
- [Download BPS test patch](sabrina-companion-stabilized.bps)

## On your iPhone

1. Keep your previous game and back up its battery save.
2. Download the BPS patch above using GitHub's **Raw/Download** control.
3. In Safari, open [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/).
   Select your own clean US HeartGold ROM and the BPS patch. The expected clean
   SHA-1 is `4fcded0e2713dc03929845de631d0932ea2b5a37`.
4. Apply the patch and save the resulting `.nds` in Files. Import it into Manic
   EMU as a separate test entry. Do not patch an already modified ROM.
5. Start fresh or use a backed-up battery save. Follow the checklist; do not load
   old emulator save states into the new ROM.

The patch enforces source and target checksums. It is the distributable test build;
the full copyrighted ROM is not committed to GitHub. No desktop tools are needed.

## Recovery/build notes for Codex

The existing managed environment is activated with `/workspace/.setup/activate.sh`.
The separate build directory is `build/sabrina-stabilization`, configured with
`meson/cross_unix.ini`, `meson/native.ini`, HEARTGOLD and wrap-mode nopromote.
Build the explicit **pokeheartgold.us.nds** target. The generic default-all target
also selects an unrelated native SDK assembly target using GCC and fails on
`-wrap:sdk`; this is not the ROM build route. Existing build setup is preserved.
For a new workspace, follow INSTALL.md and the repository's existing recovery/setup
instructions to provision the toolchain before configuring a separate build dir.

Validation commands used by Codex:

```
python3 tests/test_sabrina_stabilization.py
python3 tools/audit_sabrina_preservation.py
ninja -C build/sabrina-stabilization pokeheartgold.us.nds
python3 subprojects/meson-1.12.0/meson.py test -C build/sabrina-stabilization --no-rebuild 'HEARTGOLD Sub Checksums'
```

The explicit target was built with existing toolchain wrappers, preserving the
prototype ROM in build/recovery-verification and the separate pre-edit copy.
Patch generation uses tools/make_character_patch.py and is additionally checked
with the independent RomPatcherJS BPS decoder. There is no stock ARM9/full-ROM
checksum claim: source and art deliberately differ from stock.
