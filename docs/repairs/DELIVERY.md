# RC2 delivery and recovery

Game source, repair tests, approved master artwork, screenshots and BPS checkpoint:
**969ea00d1d443e3440d50bb4208811592438be0c**.

Repository: https://github.com/mbanks26/pokeheartgold1
Branch: `development/manic-repairs-20261104`.

Full pre-applied game: https://heartgold-rc1-manic-download.assuredkite.chatgpt.site
The retained URL contains `rc1`, but the updated page and downloaded filename say
**HeartGold-RC2-Manic.nds**. No base-ROM selection or patching is required there.
Use Safari and the same ChatGPT account. Wait for preparation, tap Save game to
Files, then import the `.nds` in Manic. Keep RC1 and a backup of its battery save.
Cold boot with the battery save and choose Continue; do not resume an RC1 emulator
save state. The native prior-build battery-save test passed; this new ROM has not
yet been played in Manic.

[Complete repair report, screenshots, known issues and checklist](REPORT.md).
[Optional recovery BPS](heartgold-manic-repairs-rc2.bps).
[Independent patch/checksum validation](patch-validation.json).
[Browser transport/assembly validation](evidence/download-validation.json).
[Complete Select/menu/direct-A/save/cold test](evidence/complete-interaction-result.json).

Required resulting ROM: 134217728 bytes, SHA-256
`a32a6b09a3895996f37bf05d1acbd2a7bf3712e56f46af43a017dfa6b44f72db`.

The source/patch checkpoint above contains all game changes. This document and
its adjacent additional test evidence are archival follow-ups; their containing
commit does not change game bytes. Original RC1 ROM SHA-256 remains
`2333089f68a9f29f633fd839b5a6b922a7bf9870ae45e326fb85274ee350c5b7`.

Private delivery-page source: `22e74d13d976562b559a4ec84451f4f41093ce67`.
Its Git contains the page and reproducible packaging recipe, no commercial ROM.
The private generated deployment assembles eight verified transport parts into
one finished ROM. Node Web Streams tests verify all parts and exact final bytes,
and reject corrupted parts and login HTML. This is transport validation, not an
independent iPhone browser or Manic gameplay test.

Native private publication succeeded on 4 November 2026:

* Deployment: `appgdep_6aeb755ce17c8191a4330a1d5ec33768`
* Saved version: `appgprj_6aeb0b07b70881918b7c86492f99b451~appgver_d50bb0ad35048191aa69fe02d6608afb`
* Owner-only audience preserved. Prior RC1 source, local ROM and saved Site version
  remain recoverable. The previous version was not overwritten.
* [Native deployment proof](evidence/private-deployment.json).

Known unresolved presentation: brief throwing-arm/Sabrina-hair overlap; see
REPORT.md for the graphics-service rejection and exact testing limitations.
No full Johto/Kanto campaign or new Manic playthrough is claimed.
