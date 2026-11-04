# HeartGold RC1 — player-test download

**RC1 is ready for a comprehensive player test, with coverage limits.** It is
not a verified complete Johto–Kanto–Mount Silver playthrough. Actual Manic EMU
compatibility has not been tested. The final report identifies every remaining
gap and the known minor appearance/dialogue limitations.

- [Download heartgold-rc1.bps](heartgold-rc1.bps) — 3,957,611 bytes.
- [Twenty-item final report](REPORT.md).
- [Milestone coverage](COVERAGE.md).
- [Manic gameplay checklist](MANIC-CHECKLIST.md).
- [Three-character sprite and gameplay gallery](GRAPHICS.md).
- [Checksums and independent patch validation](evidence/patch-validation.json).
- [Current project and engineering guide](../../PROJECT.md).
- [Native screenshots, results and input traces](evidence/native-index.json).

Source checkpoint: `507ca40db6d692683746ccf318e910e321eb48d7`, on
`mbanks26/pokeheartgold1:development/release-candidate-20261104`.
The Git commit enclosing this release document is the archive checkpoint; the
source checkpoint identifies the exact game source used for the ROM.

## Apply on iPhone

1. Keep your existing ROM and export/back up its battery save in Manic before
   adding a new build. Keep older patches and emulator save states separately.
2. Save `heartgold-rc1.bps` to Files. On GitHub's file page, use its download/raw
   control rather than saving the HTML page.
3. In Safari open [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/).
   Choose your own clean **Pokémon HeartGold USA, revision 0** ROM as the ROM
   file and the RC1 BPS as the patch. The required clean ROM is 134,217,728 bytes,
   SHA-1 `4fcded0e2713dc03929845de631d0932ea2b5a37`. BPS checks the base CRC;
   an existing patched ROM, trimmed file, different region or revision is rejected.
4. Apply the patch and save the result under a new name, for example
   `HeartGold-RC1.nds`. Expected SHA-1:
   `9670376e2a700d5c910648e18304ca3193c33e9c`.
5. Import that new NDS into Manic as a separate test game. Start a fresh save
   for the opening/story test. If testing an existing battery save, import a
   copy using Manic's save-import controls and check the displayed player/progress.
   Do not load an old-version emulator save state into the new ROM.
6. Begin with the [priority checklist](MANIC-CHECKLIST.md). The male route includes
   the sister/Sabrina storyline; the female route retains native progression with
   custom female graphics and deliberately omits those added relationship events.

No commercial ROM is included in GitHub. The BPS alone is insufficient to play;
it must be applied to the matching clean ROM. No source edits or terminal work
are required on the iPhone.

## Known presentation limits

Stock Ethan/Lyra **3D Bag models** remain. The custom 2D protagonist, action,
intro and Trainer Card resources are integrated; not every action has received
native visual gameplay review. Sabrina's separate partner art uses existing
front/profile poses rather than a newly drawn rear/throw sheet. Some native
tutorial/phone dialogue still uses original counterpart wording.

Earlier character/Stage A–F documents describe their own builds. RC1's source,
hashes, tests and remaining limitations are recorded here; those historical files
have not been replaced.
