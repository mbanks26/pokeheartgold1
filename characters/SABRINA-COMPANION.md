# Experimental Sabrina + Pokemon companion

Branch: development/sabrina-companion-20261103.
The graphics-only branch development/character-integration-20261103 remains intact.

This prototype is enabled for the male protagonist when a following Pokemon is
active. Sabrina occupies a separate dynamic map object (ID 252), following the
Pokemon's previous tile. She first appears after a valid trail tile is available,
usually after walking a couple of steps with the starter. The Pokemon remains
the game's original follower. No save-layout change or HAVE_FOLLOWER flag is used.
The latter would change wild battle rules and restrict field moves.

She uses the custom Sabrina overworld art and is already visible beside the male
in his normal/link back battle poses. Those paired poses do not add another
battler, Pokemon, AI partner, or double-battle rule.

Implemented guards: female/no-active-follower exclusion, reserved-ID collision
check, full object allocation failure handling, texture preload reservation,
script/menu/task and movement-pause gates, adjacent trail movement, safe-tile
catch-up, hide/restore and cleanup. No canonical gym NPC is replaced or edited.
She has no new talk script. Existing naming, trainers, events and party data are
unchanged. Save compatibility and actual runtime behavior still require testing.

## Current limitations

- Walking companion only. Sabrina hides during cycling, surfing and other
  player action states, then returns to the trail when walking resumes.
- Maps with no spare preload slot suppress her rather than overflowing resources.
- There can be a second Sabrina in scenes containing the canonical gym NPC;
  that NPC is retained to preserve its original events.
- Catch-up can snap to the Pokemon's previously traversed tile.
- Intro display slots reuse one custom pose. Intro/card portraits and battle
  poses need visual testing, especially paired throw overlap/timing.
- The updated intro portraits are Oak's player-selection artwork; character
  artwork in the animated opening movie remains original.
- The prototype is not claimed gameplay-verified or release-ready.

## Validation

Native ROM build passed. `python3 tests/test_sabrina_companion.py` passed host
checks on the actual companion decision code with engine stubs. These cover
eligibility, allocation failure, duplicate prevention, a reserved-ID collision,
pause/busy handling, hidden-state restoration, adjacent movement, catch-up and
cleanup. Stubs do not test engine rendering, collision, heights or save behavior.
All filesystem asset payloads and ARM7 bytes match the graphics checkpoint.
ARM9/overlay code and related linker metadata change for the runtime feature.
The 1.6 MB BPS patch uses source-copy operations for relocated unchanged data and
was independently applied with Rom Patcher JS, reproducing the built ROM hash.

## iPhone / Manic EMU test

Download `sabrina-companion-experimental.bps` from this directory. Apply it to a
clean HeartGold US ROM (SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37) with a
BPS patcher in Safari, then import the result as a separate game in Manic EMU.
Keep the previous game and save backed up. Start a fresh male test save.

1. Get the starter and walk: verify player, Pokemon and Sabrina are all visible.
2. Turn, reverse, run, use narrow paths and stairs; check overlap/collision/heights.
3. Enter/exit buildings and doors, warp, save/reload, and start/finish a battle.
4. Open menus, talk to NPCs and trigger story scenes; verify Sabrina pauses.
5. Cycle/surf/fish and return to walking; verify correct hiding/restoration and
   original Pokemon behavior. These action graphics are integrated for players.
6. Choose female and verify there is no additional Sabrina follower.
7. Check Saffron Gym/rematch scripts and the male's paired battle animation.

The latest binary hash and machine-check results are in
`sabrina-companion-validation.json`. No Manic EMU testing has been performed here.
