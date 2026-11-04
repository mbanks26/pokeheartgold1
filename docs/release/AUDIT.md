# Release-candidate audit — 2026-11-04

Working repository: **mbanks26/pokeheartgold1**. GitHub was checked again at the
start of this assignment. mbanks26/pokeheartgold has only master 8cbb4a19;
the recovered project and every requested milestone live in pokeheartgold1.

New protected development branch: **development/release-candidate-20261104**,
created remotely and locally from **110f4acf4a97c185192467dbc27b1f05ff6d39d0**.
No merge into master, reset, force-push, branch deletion, or old patch replacement.

## Recovered history

| Development branch | GitHub head at audit |
| --- | --- |
| character-integration-20261103 | cfea70fd53da81e741cacc65b250ffdd48de7739 |
| sabrina-companion-20261103 | 4ea2dc8a603cb58df6b64f8057cae436a0c7f5ac |
| sabrina-stabilization-20261103 | 2acac1673d5a59cc5364d6551b3d85196a3a93fd |
| sabrina-gameplay-validation-20261103 | bcf2f8fd9377e001c36d67308dc0c2402c4f2505 |
| story-partner-integration-20261103 | 110f4acf4a97c185192467dbc27b1f05ff6d39d0 |
| master | 3fea383f5a229391d12ef3429f8095177638a44d |

Recovery branches pre-companion, pre-story and verified-foundation remain on GitHub.
The latter is a28e2a56981b20b8d27b4c86539942fadbd62688; the local recovery ref
was older, so the remote list rather than that stale ref was used for this audit.
Sabrina afd4151f, male bda9631d, female 2c669251, prototype 4ea2dc8a and the
recovery checkpoint are verified ancestors of the selected development head.

The latest state includes the New Bark opening, sister encounters and Eevee,
genuine shiny starters, milestone conversations, three native AI Multi Battles,
and the daily-reset fix bf7dde2a. No feature recreation was needed.

## Newly rerun evidence

- The existing ROM target rebuilds byte-identically to the prior final ROM:
  SHA-1 4f4e203c2b52967d2739c762360ed0065b458d59.
- All five existing host suites pass again: 90 controller assertions, 27
  dialogue assertions, 300,000 shiny PID cases, all 44 explicit partner/opponent
  moves and seven trainer records, and 8,192 native daily-reset cases.
- A new preservation audit verifies all 6,013 existing graphics files, original
  95 back-archive members, original 738 trainer records, Bill's Eevee gift,
  Lance's battle, official Sabrina Gym script and save structures.
- Native input replay from a blank battery save reaches a genuinely shiny
  Chikorita for both genders. Player-selected name CPDEX is entered normally.
  Male: one Sabrina and one native Pokemon; female: one Pokemon, no Sabrina,
  and the female story guard is set. Neither run writes progress into RAM.
- The native Saffron practice battle/save/close/Continue scenario passes again
  after repairing fixture import. Player commands only Crunch; Sabrina uses
  the native AI. Native save counter 5 and CRC pass, both persistent flags
  remain set, and exactly one object for each follower returns.

These are independently rerun checks for this assignment. Earlier Well/Tower,
Gym win/loss, evolution and elapsed-day evidence remains in docs/story; it is
not relabeled as new testing. A separate clean-directory build and broader QA
are in progress. This audit checkpoint is not a campaign-completion claim.

## Evidence-based issue list at audit

| Severity | Finding | Action/status |
| --- | --- | --- |
| Test infrastructure | Raw SAV renamed to DSV may boot an empty game; practice driver then raised KeyError instead of a useful diagnostic. | Fixed: validate native CRCs and create the actual DeSmuME footer; refuse overwrite, add regression, improve error/cleanup; native rerun passes. |
| Minor graphics | Original Ethan/Lyra **3D Bag models** remain. They are separate from the custom 2D walking/action/intro/card resources. | Confirmed in unchanged Bag asset/code and inherited screenshot; do not claim every alternate appearance is customized. |
| Cosmetic presentation | Partner backpic 19 reuses existing Sabrina front/profile poses. | Preserve established artwork; dedicated rear/throw artwork remains absent. |
| Verification gap | No full Johto–Kanto–Mount Silver playthrough or actual Manic EMU test. | Attempt fresh progression; publish explicit milestone coverage and remaining gaps. |
| Verification gap | All original phone/tutorial text has not been reconciled to the sister relationship. | Review chronology and dialogue; retain required native events. |

No new critical or major gameplay defect has been established by the checks above.
That is not evidence that untested progression is clear of defects.

The supported base header is NTR-IPKE-USA, revision byte 0, 134,217,728 bytes,
SHA-1 4fcded0e2713dc03929845de631d0932ea2b5a37. Commercial ROM data and RAM/ROM
save states are not committed. Earlier ROMs and patches remain intact; disposable
old generated build objects/resources and RAM captures were losslessly gzipped,
hash-verified, with restoration manifests retained in the workspace.

See [evidence](evidence/) and the prior [project report](../story/STAGE-F.md).
