# Changed files

Compared with prototype 4ea2dc8a.

## Runtime/source and resource changes

- `asm/include/unk_0205FD20.inc`
- `asm/unk_0205FD20.s`
- `files/a/0/0/6`
- `include/map_object.h`
- `include/sabrina_companion.h`
- `include/sabrina_companion_trail.h`
- `src/battle/battle_022378C0.c`
- `src/field/fieldmap.c`
- `src/field/sabrina_companion.inc`
- `src/map_object.c`
- `src/pokemon.c`

## Validation/tools

- `tests/test_sabrina_companion.py`
- `tests/test_sabrina_stabilization.py`
- `tools/append_sabrina_solo.py`
- `tools/audit_sabrina_preservation.py`

Documentation, preservation manifests, validation results, emulator evidence and the new BPS patch are in `docs/companion/`. No story script or other character asset was changed.

## Gameplay-validation follow-up

Compared with stabilization commit 2acac167, runtime changes are confined to
`src/field/sabrina_companion.inc`; regression assertions update
`tests/test_sabrina_stabilization.py`. New recovery tooling:

- `tools/companion_emulator_runner.py`
- `tools/make_companion_test_fixture.py`
- `tests/scenarios/companion_smoke.jsonl`
- `tests/scenarios/companion_ledge.jsonl`
- `tests/fixtures/companion/` (two compressed authored saves, layout, manifest)

Updated reports, reproduction instructions, screenshots, traces and the new BPS
are in `docs/companion/`. Earlier reports/patches remain recoverable. No graphics
or story scripts change in this follow-up.
