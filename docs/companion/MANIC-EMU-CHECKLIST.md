# iPhone Manic EMU test checklist

Use a separate test game entry. Back up your normal battery save and keep the old
ROM. Apply the new BPS patch to the matching clean US HeartGold ROM, not to a
previous custom ROM. Start from a new game or copied battery save; avoid loading
save states made with another ROM build. No terminal or desktop editor is needed.

Record the ROM SHA-1 from VALIDATION.json and whether each check passes. A brief
screen recording is helpful for any failure. Include map/location, action, whether
Sabrina disappeared, and whether returning to walking restored her.

- [ ] New male game: custom appearance, freely chosen name and original Oak/Elm sequence.
- [ ] Obtain starter: native lead Pokemon remains itself; Sabrina joins independently.
- [ ] Formation: player, Pokemon, Sabrina; stop, all four turns and repeated corners.
- [ ] Reverse directions and stop near the Pokemon: no permanent overlap or blockage.
- [ ] Enter/leave home, Elm's lab and Pokemon Centers; no duplicate Sabrina.
- [ ] Routes/towns, connected maps, doors and stairs: return on a safe walking tile.
- [ ] Caves, narrow passages and ledges: no wall clipping or trapped player.
- [ ] Cycle, stop, walk: temporary absence is allowed; automatic safe return required.
- [ ] Surf, land, walk: same restoration; native Pokemon follows its original rules.
- [ ] Fishing, special actions and warps: no stuck object; restore after normal walking.
- [ ] Wild Single Battle: paired back art, normal male throwing sequence, one active Pokemon.
- [ ] Trainer Single Battle: same; Sabrina takes no turns and throws no Pokeballs.
- [ ] Return from battle: correct formation, no duplicate human object.
- [ ] Save following in town; fully close game and load battery save: one companion returns.
- [ ] Repeat inside building, after a transition, after cycling and after surfing.
- [ ] Test early Elm, Lyra and Silver encounters: NPCs reach player and scripts finish.
- [ ] Test Gym conversations, Team Rocket, League and Kanto scripts when accessible.
- [ ] Saffron Gym: official Sabrina remains present; no companion duplicate inside.
- [ ] Challenge Sabrina: male solo back art; normal Single Battle and Marsh Badge reward.
- [ ] Win and exit: companion returns outside. Separately lose: normal whiteout/rechallenge and recoverable companion.
- [ ] Sabrina rematch: solo player art against her; return after leaving canonical-NPC area.
- [ ] Check male custom actions/portraits, Sabrina design and white-haired Lyra replacement.

Acceptance: no permanent player blockage, no changed native Pokemon identity,
no progression failures, no duplicate Sabrina, stable save/reload, correct paired
and solo battle presentation. Temporary disappearance during unsafe movement or
scripts is intentional. If restoration fails, preserve the battery save and report
location/action; do not overwrite the normal save with the failed test.
