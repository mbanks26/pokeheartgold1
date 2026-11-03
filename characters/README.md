# Character graphics integration

Development branch: `development/character-integration-20261103`.
The separate `recovery/verified-foundation-20261103` branch remains unchanged.

These are newly adapted, hardware-compatible pixel assets based on the user's
reattached references. They are not claims of recovering uncommitted original
sprite files. The indexed PNGs here are the editable source assets.

## Validation and rebuilding

The native overworld BTX0 texture names, order, dimensions, metadata and palette
size are preserved. Texture index 0 is transparent; each texture is 32x32 I4.
Overworld PNG rows are up/back, down/front, left, right, with four frames each.
The trainer NCER/OAM layout and NANR animation timing are preserved, with native
NCGR tile conversion and a lossless pixel roundtrip. Trainer NCBR portraits use
the original game's backward scan encryption, also checked by roundtrip.
All archive members and file sizes outside the listed replacements are preserved.

After graphics changes, use `make rom`, not the stock `make` checksum target:
the stock full-ROM and filesystem hashes must change when graphics are replaced.
Keep the stock ROM separately for the stronger, graphics-only validation below.

```sh
source /workspace/.setup/activate.sh
python3 tools/character_graphics.py apply sabrina
python3 tools/character_graphics.py apply male
python3 tools/character_graphics.py apply female
make rom BUILD=build/recovery-verification
python3 tools/character_graphics.py verify \
  --stock /workspace/pokeheartgold1/build/heartgold.us/pokeheartgold.us.nds \
  --rom build/recovery-verification/pokeheartgold.us.nds \
  --stages sabrina male female --report characters/female/rom-validation.json
```

The converter requires Pillow. It reads the original resource templates from the
verified foundation Git commit, so retain the repository history. The ROM verifier
checks exact allowed archive members and verifies that *every other ROM byte*
equals the stock HeartGold US ROM. This protects game code, events, dialogue,
naming, following Pokemon, filesystem layout and all unrelated assets.

## Stage 1: Sabrina

- 16 overworld walk/idle textures: MMODEL_GSLEADER10, member 163 of a/0/8/1.
- Three trainer battle poses: class 107, members 535 and 536 of a/0/5/8.
- Both encrypted portrait panels: member 539 of a/0/5/8.
- Original character/event IDs and both normal/rematch trainer data retained.
- Conversion and ROM isolation checks passed; see sabrina/rom-validation.json.
- Manic EMU testing pending: Saffron Gym, talking/turning/walking, initial battle
  entrance and psychic gesture animation, rematch, palette/transparency and feet.

## Stage 2: Male protagonist

- Normal walking/running bank: MMODEL_HERO, member 69 of a/0/8/1 (32 textures).
  The run slots reuse the custom directional step artwork at the original timings.
- Front trainer sprite and encrypted portrait: class 0 of a/0/5/8.
- Eight back battle throw poses and encrypted portraits in both ordinary and
  link variants: backpic IDs 0 and 15 of a/0/0/6.
- Original battle OAM layouts and animation sequences retained.
- Conversion, main/sub checksums and graphics-only ROM checks passed; see male/.
- Manic EMU testing pending: choose male, naming, all four walking/running
  directions, first wild battle/Pokeball throw, trainer battle, back animation,
  link-variant display if used, following Pokemon, save/load and map transitions.
- Separate cycling, surfing, HM-use, fishing, watering, ladder, saving/healing,
  Rocket-disguise, Pokeathlon, alternate-avatar and intro/Trainer Card graphics
  remain original. Those require later artwork/integration, not just playtesting.

## Stage 3: Female character replacing Lyra

- Normal walking/running bank: MMODEL_HEROINE, member 70 of a/0/8/1 (32 textures).
  Run slots reuse the custom directional step artwork at original timings.
- Front trainer sprite and encrypted portrait: class 1 of a/0/5/8.
- Eight back battle throw poses and encrypted portraits in ordinary and link
  variants: backpic IDs 1 and 16 of a/0/0/6.
- Fair skin, white hair, red eyes and burgundy clothing adapted from the reference.
- Naming and the original Lyra story role/character IDs are retained.
- Conversion, main/sub checksums and combined graphics-only ROM checks passed;
  see female/conversion.json and female/rom-validation.json.
- Manic EMU testing pending: choose female, naming, all walking/running directions,
  wild/trainer battles and throw animation, following Pokemon, save/load and story
  interactions when she appears as the non-player counterpart.
- The same separate special-state, alternate-avatar, intro and Trainer Card
  graphics listed for the male character remain original and need later artwork.

## Test on an iPhone with Manic EMU

Download `heartgold-characters.bps` from this directory using GitHub's raw-file
download. It contains the graphics changes only, not a full game ROM.
Apply it to a **clean HeartGold US ROM** using a BPS-capable patcher, such as
[Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) in Safari. Save the
resulting `.nds` in Files and import it into Manic EMU as a separate test game.
Keep your existing ROM and save backed up; start a fresh test save for each gender.

- Required source ROM SHA-1: `4fcded0e2713dc03929845de631d0932ea2b5a37`.
- Final graphics ROM SHA-1: `40a353ae2f4973dba725dbf175ea0d6b5d12bc6b`.
- The BPS patch has source/target/patch CRC checks and was applied back to the
  stock source, reproducing the final built ROM byte for byte.
- Patch generation: `python3 tools/make_character_patch.py STOCK.nds CUSTOM.nds characters/heartgold-characters.bps`.

Check transparency, colors, direction order, foot alignment, clipping, battle
animation timing and map transitions. Sabrina needs a save at Saffron Gym or her
rematch. The player back animations retain original timing but use newly adapted
art poses; hand/ball synchronization needs particular attention in gameplay.
These visual checks have **not** been performed in Manic EMU.

## Scope

No dual follower system, gameplay changes, naming changes, story changes or
following-Pokemon changes. No emulator gameplay validation has yet been claimed.

## Extended action graphics checkpoint

Cycling, surfing, fishing and the remaining player action/disguise texture banks
are now integrated; see [actions/README.md](actions/README.md) for IDs and tests.
Earlier lists of original special-state graphics above describe the earlier commits.
Intro, Trainer Card, shared Sabrina battle art and dual-follower logic remain pending.

## Portraits and paired battle art

Intro and Trainer Card portraits for both protagonists are integrated using
the existing custom front artwork resized into native slots. Four intro display
slots share one pose. Trainer Card name/signature/badges remain unchanged.
Sabrina now appears beside the male in all eight normal/link back battle poses;
this is artwork, not a second battle trainer or battle-rule change. The prior
solo back sheet remains in male/battle-back-solo.png.

All conversions and graphics-only ROM isolation checks passed. Every new portrait,
card display, and paired throw needs visual/animation testing in Manic EMU.
Runtime Sabrina-plus-Pokemon movement is a separate implementation stage.
