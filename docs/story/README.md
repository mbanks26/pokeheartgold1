# Story and partner integration

Use [the latest stable story/partner patch](stage-e-release.bps),
[implementation](STAGE-E.md), [final regression report](STAGE-F.md), [RTC persistence correction](RTC-PERSISTENCE.md)
and [iPhone gameplay checklist](MANIC-CHECKLIST.md).

Development branch: development/story-partner-integration-20261103 in
mbanks26/pokeheartgold1, the repository containing the validated recovered build.
Master and all prior commits/builds remain preserved.

On iPhone, download the patch and apply it to your own clean US HeartGold ROM
(SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37) with Safari's
[Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/). Import the resulting
.nds as a separate Manic EMU test entry. Back up your normal battery save first.
Use native battery saves across versions. Emulator save states require their exact
ROM. A new game exercises the revised opening and guaranteed shiny starter choice;
existing saves retain their Pokemon and skip the new opening safely.

Historical checkpoints remain available: [audit](AUDIT.md), [request](REQUEST.md),
[Stage A](STAGE-A.md), [Stage B](STAGE-B.md), [Stage C](STAGE-C.md) and [Stage D](STAGE-D.md).
Their patches are archival; the latest patch includes the daily-reset persistence fix.
