# Extended player action graphics

Both protagonists now have new native texture sources for cycling (71/72),
surfing (73/74), HM use (75/76), watering (77/78), fishing (79/80), ladders
(81/82), device/Pokemon gestures (85/86), saving (87/88), healing (89/90),
Rocket walking/running (95/96), Rocket healing (97/98), Pokeathlon (99/100),
tree shaking (207/208), alternate avatar (213/214), and Rocket saving (248/249).
Rocket uniforms remain black with the red R; the custom identities are retained.
Alternate-avatar run slots reuse the normal custom walking/step artwork.

Each numbered PNG is a 4-column sheet of 32x32 frames, in numeric texture order.
The conversion tool preserves file size, texture names/order, dimensions, format,
and all metadata, replacing only texture pixels and the 16-color RGB555 palette.
Every replacement passes indexed-pixel roundtrip checks. No game logic changes
are included in this graphics checkpoint. The ROM validation report lists the
precise changed members and checks all other ROM bytes against the original.

Reapply: `python3 tools/extended_character_graphics.py ID [ID ...]`, then `make rom`.
Run the usual graphics-only ROM verifier after all desired sources are applied.

Manic EMU tests are still required for every action, including all directions,
bike mount/dismount, fishing rod alignment/casting, water transitions, ladders,
watering and healing gestures, Rocket disguise story scenes, and Pokeathlon.
Generation and palette conversion are not proof of correct gameplay animation.

The additional requested intro artwork, Trainer Card artwork, Sabrina/male shared
battle poses, and actual Sabrina-plus-Pokemon companion behavior are not included
in this checkpoint. The agreed companion behavior is male-only, from the start
once the player has a Pokemon, without the old HAVE_FOLLOWER flag that changes
battle rules and restricts field moves. Sabrina's existing gym role remains.
