# RC1 changes relative to the recovered story milestone

Base: `110f4acf4a97c185192467dbc27b1f05ff6d39d0`.
Source checkpoint: `507ca40db6d692683746ccf318e910e321eb48d7`.

## Game-source changes

| File | Purpose |
| --- | --- |
| `files/fielddata/script/scr_seq/scr_seq_0885_T25.s` | Guard the shared Goldenrod interaction for the female route; choose sister response based on Sabrina's joined status. |
| `files/msgdata/msg/msg_0581_T25.json` | Append a sister response without absent Sabrina, and a neutral female-route breeder response. |
| `files/msgdata/msg/msg_0612_T27.json` | Vary four repetitive Ecruteak sister replies around her own training/experiences. |
| `files/msgdata/msg/msg_0629_T30.json` | Vary four repetitive Blackthorn sister replies, with consistent unevolved Eevee. |

No character art, trainer roster, battle calculation, companion movement code,
Pokémon creation code or save structure changed during final QA. The final ROM's
ARM9 is byte-identical to the independently rebuilt baseline. Only NARC script
member 885 and message members 581, 612 and 629 changed; 382/384 resources match.

## QA and packaging files

New/updated tools: `prepare_desmume_save.py`, `release_emulator_session.py`,
`check_release_opening.py`, `check_release_starters.py`,
`check_release_evolution.py`, `check_release_actions.py`,
`check_release_calendar.py`, `check_release_goldenrod.py`,
`check_release_female_route.py`, `check_release_gym.py`,
`check_release_rematch.py`, `check_sabrina_practice_roundtrip.py`,
`audit_release_assets.py`, `audit_release_story.py`, and `make_character_patch.py`.

New save-import regression: `tests/test_desmume_save_import.py`.
Native input traces: `tests/fixtures/story/opening-inputs.json` and
`starter-inputs.json`. Authored fixture provenance/checksums are under
`tests/fixtures/release/`. The test-helper changes improve footer/CRC validation,
menu normalization, cleanup, native save/Continue assertions and diagnostic
messages. They are not game-engine changes.

Documentation and evidence: root `PROJECT.md`, `docs/release/`, compressed
native command/console logs, useful screenshots and small CPDEX battery-save
fixtures. Full commercial ROMs, emulator RAM dumps/states and SDK executables
are excluded. BPS output is new and earlier test patches remain untouched.

For an exact machine-readable file list, compare the source checkpoint against
the base with Git, or inspect its GitHub commit file list. The archive commit
then adds the final documents, manifest and BPS patch.
