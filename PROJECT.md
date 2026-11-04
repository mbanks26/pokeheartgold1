# Custom HeartGold — current project state

Current release: [RC1 report and downloads](docs/release/README.md), 4 November
2026. This is the current overview; the numbered Stage A–F and character-stage
documents are historical records of those earlier builds.

## Repository and canon

The recovered project is **mbanks26/pokeheartgold1**, branch
`development/release-candidate-20261104`. The separate mbanks26/pokeheartgold
repository does not contain this development history. Recovery branches and
master are preserved. Do not reset, force-push or merge into master during QA.

The male protagonist retains selectable naming, brown skin, black dreadlocks
with gold accents, amber-brown eyes, red/white jacket, black shirt, dark cargo
pants and matching shoes/accessories. Sabrina retains long black-green hair,
green eyes, burgundy clothing/boots and black leggings. She is his established
partner and Saffron's official Gym Leader; their families and his sister knew
one another before this adventure. She should sound reserved, perceptive and
capable of dry humor and affection, rather than repeatedly explaining this history.

The redesigned Lyra character is his independently traveling **sister, not
twin**: fair skin, silver-white hair, red eyes, burgundy/black clothing, ribbon
and gold accessories. She is competitive and playful without replacing Silver.
Her encounters occur in Violet, Goldenrod, Ecruteak and Blackthorn. A breeder
explains her Eevee, later dialogue catches up a missed acquisition, and later
teams retain unevolved Eevee. Bill's separate Eevee gift is unchanged.

The female player keeps native progression, selectable naming and custom female
art. Added male-route sibling/companion events are disabled. Native required
Lyra/Ethan events remain; a complete alternate sibling story is not implemented.
Goldenrod's shared breeder interaction is explicitly neutral on this route.

Editable graphics: [male](characters/male/), [Sabrina](characters/sabrina/),
[female](characters/female/), [special actions](characters/actions/).
Existing 2D action, intro and Trainer Card art is integrated. Stock **3D Bag
models** remain, and the separate partner presentation reuses Sabrina's existing
front/profile artwork. No graphics were recreated during final QA.

## Companion and battle architecture

`src/field/sabrina_companion.inc` manages independent human object **252**, sprite
369, script FFFF. Native following Pokémon **253** and player **255** retain their
identities. A 16-entry trail records the Pokémon's vacated tiles. Terrain,
height and occupancy checks precede spawning/movement. An eight-frame cooldown,
120-frame timeout and fresh-trail recovery handle invalid trails and blocked
movement. Only the exact companion identity is non-solid; unrelated NPCs are
not made passable. Human position is excluded from ordinary map-object save
serialization, preventing restoration of duplicate stale objects.

Formation is player → Pokémon → Sabrina. Tasks, incompatible avatar states,
canonical Sabrina scenes and special actions suppress her temporarily. Walking
on a valid fresh trail restores her; joined status is independent of visibility.
This design preserves the original Pokémon follower rather than replacing it.

Ordinary eligible male Single Battles use existing combined back artwork in
slots 0/15. Solo slots 17/18 are selected for unjoined/official Sabrina battles;
partner backpic 19 uses recovered Sabrina poses. Gym trainers 258 and 725 remain
enemies in ordinary Singles, with native rosters/rewards. Joined state survives
Gym suppression, victory and loss.

Three scripted native AI Multi Battles use battle type **0x4B**, separate Sabrina
teams 743–745, and new opponents where needed (746–749). They occur at the
Slowpoke Well, Radio Tower Petrel event and optional post-Marsh Saffron practice.
The player controls only their own Pokémon; the existing battle AI controls
Sabrina. Native battle/AI source is unchanged. Do not promise optimal AI or
unverified switching/fainting behavior. Original 738 trainer records remain.

## Starters, flags and save compatibility

Elm's Chikorita/Cyndaquil/Totodile are genuinely shiny using the actual player's
OT and native shiny-PID generation in `src/choose_starter.c`. Level 5, starter
selection, normal moves/ability and ordinary creation rules remain. The global
wild shiny threshold is still 8/65,536. Existing non-shiny Pokémon are not changed.

No save-size/layout changes were made. Existing flag/variable slots are used:

| Slot | Meaning |
| --- | --- |
| B50 | Opening introduction completed/actors hidden |
| B51 | Sister Eevee acquisition recorded |
| B52 / B53 / B54 | Well / Tower / practice partner victories |
| B55 / B56 / B57 | Optional Violet / Ecruteak / Blackthorn sister victories |
| B5D | Female-route story guard |
| B5E / B5F | Companion explicitly initialized / joined |
| 416F | Introduction completion repair |
| 416E | Selected companion conversation message |

`ClearDailyFlags` preserves B50–B57 and the upper three bits of the B58 byte;
ordinary daily bits B58–B5C still clear. See [save compatibility](docs/story/RTC-PERSISTENCE.md).
Already-erased flags from older buggy builds cannot be inferred reliably; retain
older saves/backups or use the existing catch-up event where supported.

Scripts can set B5E and B5F to join, or set B5E and clear B5F to deactivate.
`SabrinaCompanion_SetJoined` provides the C equivalent. Keep B5E initialized when
deactivated so the temporary starter fallback cannot silently re-enable her.
On foot with Sabrina present, **Select** requests a progress-dependent conversation;
native A/menu/phone/warp controls have priority. There is no added town-entry
conversation popup. Original tutorials and some phone wording remain stock.

Native battery saves are compatible across these builds. Emulator save states
depend on the exact ROM and should not be transferred between versions. The QA
fixtures are CPDEX test progress with documented authored prerequisites, never
proof of completing all earlier story events.

## Rebuild and verification for a future cloud workspace

Use the toolchain/setup described in [INSTALL.md](INSTALL.md), the existing
Metrowerks SDK wrappers and the preserved Git history. The successful environment
uses Metrowerks ARM via qemu-i386, GCC 14.2, Meson 1.12 and Ninja 1.12. Its shell
activation is `/workspace/.setup/activate.sh`. The existing configured directory
is `build/release-candidate`; use the explicit `pokeheartgold.us.nds` target.
Generic Ninja `all` includes unrelated host SDK utilities with a known wrapper
problem. A new build directory completed all 9,670 ROM build tasks in this audit.

For the verified configuration, use `make rom BUILD=build/new-rc` or run Ninja's
explicit ROM target in an already configured directory. Keep the stock US ROM
separate. Source checkpoint and expected hashes are in the release manifest.
To preserve space after final QA, generated object caches were losslessly gzipped;
restore those `.o.gz` caches or allow Ninja to regenerate missing objects. Source,
installed toolchain, symbols and immutable ROM snapshots remain preserved.

Run the six `tests/test_{sabrina_stabilization,sabrina_dialogue,shiny_starters,
sabrina_partner,story_daily_persistence,desmume_save_import}.py` scripts and the
two `tools/audit_release_{assets,story}.py` audits. These distinguish host stubs
from actual-ROM/static checks. Native drivers under `tools/check_release_*.py`
accept `--core`, immutable `--rom`, matching `--symbols` and a new `--output`
directory; see each `--help`. Evolution additionally consumes the starter
driver's saved outputs. Never link a mutable build target as an immutable test ROM.

Use `tools/prepare_desmume_save.py` for valid raw-save/DSV conversion; simply
renaming SAV to DSV can boot an empty game. Preserve native sector generations
and CRCs when authoring fixtures. Test failures caused by fixture import or
automation assumptions must not be recorded as production bugs.

`tools/make_character_patch.py` emits BPS, validates the exact base SHA-1, performs
a complete byte roundtrip, and refuses to overwrite an existing output. Its
`--metadata` option records the release scope. NARC member matching avoids
embedding unchanged resources when archive sizes change. Independent Rom Patcher
JS validation and all checksums are archived in the release evidence.

The iPhone user does not need a terminal or desktop editing software. All build,
source, patch and emulator work is performed in the cloud; only ordinary Manic
gameplay review remains on the phone.
