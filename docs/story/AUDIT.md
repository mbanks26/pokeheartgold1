# Protected story-integration foundation

The actual recovered project is mbanks26/pokeheartgold1. The similarly named
pokeheartgold has only its unrelated master branch. Remote branches were inspected
on 2026-11-03: the newest validated development head remains bcf2f8fd9377e001c36d67308dc0c2402c4f2505.

Sabrina afd4151f, male bda9631d, female 2c669251 and companion prototype 4ea2dc8a
are ancestors of that head. The recovered graphics, action variants, combined
battle art and the three later native walking fixes are together on this history.
The explicit ROM target builds without work; 88 sanitized controller assertions pass.
All 6,013 baseline graphics files (including earlier evidence screenshots) match and the verified ROM retains SHA-1
5cbf4223b6b1a02ccee28fd276e86281fff61291.

A remote recovery/pre-story-partner-20261103 checkpoint and separate
 development/story-partner-integration-20261103 branch were created at that head.
A full local pre-edit Git bundle is also retained. Master and all previous
branches, ROMs and BPS patches are preserved. Development uses the separate
build/story-integration directory. Only our disposable emulator RAM/state captures
were losslessly archived to recover disk space; their hashes and compressed
contents are retained, and no working ROM or battery save was removed.

The project already has a native MultiBattle script command. With a nonzero
partner and two distinct opponents it selects TRAINER|DOUBLES|MULTI|AI and creates
an independent BATTLER_PLAYER2 party. Lance's existing event will remain intact.
New partner-team records must be separate from Sabrina's Gym/rematch data.

Existing save flags B50-B5D and variables 416E-416F have no source/event references
except their unnamed declarations before this work. Reserved story aliases use
that existing storage; the save structure is not resized. B5E/B5F retain their
previous companion-initialized/joined meaning. The original auto-join fallback
remains for existing starter saves; new male games set those bits in the story scene.
