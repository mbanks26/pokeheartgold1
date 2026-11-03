# HeartGold recovery — November 3, 2026

## Foundation

Use mbanks26/pokeheartgold1 at source commit 3fea383f5a229391d12ef3429f8095177638a44d.
This is the repository for which the replacement cloud environment supplied a clean checkout, tools, a built ROM, and successful prior build logs.
A separate local development copy is at /workspace/work/recovery/pokeheartgold1 on recovery/verified-foundation-20261103.
The original /workspace/pokeheartgold1 checkout was left unchanged.
No existing GitHub branch was moved, reset, overwritten, deleted, or merged.

## GitHub inspection

At the start of recovery, both repositories exposed only refs/heads/master, no tags, and no pull requests, releases, or GitHub Actions runs.

| Repository | master | Upstream |
| --- | --- | --- |
| mbanks26/pokeheartgold | 8cbb4a19ab781611ff1767035dcaea6b47baeded | ctrl-cheeb-del/pokeheartgold |
| mbanks26/pokeheartgold1 | 3fea383f5a229391d12ef3429f8095177638a44d | pret/pokeheartgold |

GitHub comparisons against these exact commits in the corresponding upstream repositories returned identical, zero commits ahead, and zero changed files.
Thus both exposed histories are upstream histories; neither contains a custom project commit beyond those upstream commits.
The first fork's recent work concerns field-effect pointers, union-room/link types, and other decompilation changes.
The second fork's latest commit is the upstream overlay_57 merge, following upstream nitroarc and compression changes.
These should not be mistaken for your custom character work.

The cloud checkout was clean and matched pokeheartgold1/master exactly.
Its full Git history passed git fsck; a verified complete-history Git bundle is saved locally as /workspace/work/recovery/pokeheartgold1-foundation.bundle.
The ordinary asset search found no separately attached design images in library-files, shared/downloads, or scratch.
This does not establish what existed in the deleted workspace; that workspace's uncommitted files cannot be recovered through GitHub.

## Character work

| Requested design | Recovery result |
| --- | --- |
| Black male protagonist, dreadlocks, red-and-white jacket | No custom design or integration recovered from the available GitHub refs or current attachments |
| Sabrina, long black-green hair, classic burgundy outfit | No custom design or integration recovered; stock Sabrina references are upstream content |
| Lyra replacement, fair skin, white hair, red eyes, feminine burgundy clothing | No custom design or integration recovered; stock Ethan/Lyra source references are upstream content |

Reattach original approved images/sprite sheets from the previous chat or iPhone Files/Photos if available.
Include separate overworld sheets, battle sprites, portraits, palettes, or 3D textures/models if those were completed.
Missing assets need recreation only after checking those originals.
Descriptions above are preserved specifications, not recovered artwork.
No new character artwork or additional features were implemented during recovery.

## Recovered cloud setup

cloud-install-recovered.sh is the exact setup script found at /workspace/.setup/install.sh.
It was not previously committed to either master branch.
It targets a Debian cloud workspace at /workspace/pokeheartgold1 and /workspace/.setup, installs dependencies into the workspace, and uses qemu-i386 plus patched 32-bit compiler loaders.
It is a recovered setup record, not a universal installer, and was not rerun during recovery.
Use it only in a fresh compatible cloud workspace after reviewing its hard-coded paths.
The existing original checkout and /workspace/.setup remain dependencies of the copied compiler wrappers in this recovered environment; do not remove them.
The repository's INSTALL.md remains the standard setup guide.

Current environment verification command:
```sh
cd /workspace/work/recovery/pokeheartgold1
source /workspace/.setup/activate.sh
make BUILD=build/recovery-verification
```
This command configured a new build directory instead of reusing previous compiled output.
The log is /workspace/work/recovery/fresh-build.log.

Git shell network access failed because the configured proxy was unreachable; connected GitHub tools successfully supplied the repository inspection and recovery branch operations.
No desktop or iPhone terminal is needed to review this recovery branch.

## Fresh build verification — PASSED

The fresh build completed with exit code 0. All four Meson tests passed: Main Checksums, Sub Checksums, Filesystem Checksums, and ROM Checksum (4 passed, 0 failed).
The newly generated pokeheartgold.us.nds is 134217728 bytes (128 MiB), SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37, matching the upstream HeartGold US reference ROM.
This verifies a complete original-ROM build, including filesystem bytes; the custom character designs are not integrated into it.
No emulator gameplay test was performed. No additional features were started.

Continue development from the source on this recovery branch. Only recovery documentation and the preserved setup script were added; the game's source and assets remain at the verified foundation commit.
