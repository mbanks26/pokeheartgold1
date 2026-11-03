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
make rom BUILD=build/recovery-verification
python3 tools/character_graphics.py verify \
  --stock /workspace/pokeheartgold1/build/heartgold.us/pokeheartgold.us.nds \
  --rom build/recovery-verification/pokeheartgold.us.nds \
  --stages sabrina --report characters/sabrina/rom-validation.json
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

## Scope

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

No dual follower system, gameplay changes, naming changes, story changes or
following-Pokemon changes. No emulator gameplay validation has yet been claimed.
