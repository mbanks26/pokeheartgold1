# Stage B — Sister journey and Eevee

New optional encounters appear near the Pokemon Centers in Violet, Goldenrod,
Ecruteak and Blackthorn. The sister remains an independent traveler. Violet,
Ecruteak and Blackthorn offer one optional Single Battle each; declining keeps
it available, victory records a dedicated story bit, and loss uses native whiteout.
Silver's original battles and all 738 original Trainer records are unchanged.

Her team grows from Marill/Pidgey to Marill/Pidgeotto and Azumarill/Pidgeot.
Eevee joins through a short Goldenrod scene with a Day-Care breeder, a native cry,
and saved story flag B51. Later teams branch on that flag and keep Eevee unevolved.
The player's original Bill gift event is byte-identical to the protected baseline.

Storage: B51 sister's Eevee; B55/B56/B57 sibling victories; B5D hides these new NPCs
on the female-player route. No save structure changes. The five new Trainer rows
are appended at 738-742. Existing female overworld/front assets are reused; only
relevant map preload lists gain the existing sister sprite reference.

The ROM builds separately (SHA-1 69cbc8f225649c927e3e1c5687c2d87a275fc641), and
90 sanitized follower assertions pass, including the female-route guard. All
6,013 baseline graphics and 95 existing back-archive members remain exact.

DeSmuME exercised the Goldenrod acquisition and native save: newest sector counter
2 has B51 set, while the older counter 1 has it clear. Both CRCs pass, and the
player's Bill Eevee gift flag remains clear. Native Pokemon Center exits then
created Violet/Ecruteak/Blackthorn scenes at their real heights (6/6/14). Their
optional battles completed and returned to the field; victory bits and follower
restoration are checked in the evidence traces. The later tests inherit the
actually saved Eevee flag from Goldenrod.

Late-game fixtures use our authored level-100 test Feraligatr to shorten battles.
Ecruteak's fixture marks Bill's prior PC encounter complete to avoid a missing-NPC
cutscene in a relocated save. Fixture setup is not a normal progression playthrough.
Initial outdoor fixtures at an assumed height 2 could not move on those raised
cities; these were corrected by entering through native doors, without changing
runtime code. Manic EMU, normal-level balance and a full journey remain untested.

The final native observations are B55+B51 = 0x22 (Violet), B56+B51 = 0x42
(Ecruteak) and B57+B51 = 0x82 (Blackthorn), with companion bits 0xC0 retained.
One Pokemon and one Sabrina return after a few additional safe walking tiles.
The traces retain exploratory failed expectations made before a new trail formed;
these are not counted as passing assertions.

[Stage B patch](stage-b-sister-journey.bps) and [evidence](stage-b-evidence/) are retained.
