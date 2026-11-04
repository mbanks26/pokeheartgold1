# Finished NDS download for Manic EMU

The owner-private download page is live:

**https://heartgold-rc1-manic-download.assuredkite.chatgpt.site**

Open it in Safari and sign in with the same ChatGPT account that owns the project.
Keep the page open while it prepares the file, then tap **Save game to Files**.
Import **HeartGold-RC1-Manic.nds** from Files into Manic EMU. No patch application
or original-ROM selection is required. Preserve older games and battery saves.

This delivers the exact existing RC1 build, with all integrated changes already
applied; it does not change game code or claim a new gameplay-validation milestone.
The earlier `/workspace/...` link was not a working ChatGPT download attachment.

| Property | Value |
| --- | --- |
| Filename | HeartGold-RC1-Manic.nds |
| Bytes | 134217728 (128 MiB) |
| SHA-1 | 9670376e2a700d5c910648e18304ca3193c33e9c |
| SHA-256 | 2333089f68a9f29f633fd839b5a6b922a7bf9870ae45e326fb85274ee350c5b7 |
| Game source checkpoint | 507ca40db6d692683746ccf318e910e321eb48d7 |
| Original RC1 archive commit | 232f94c5a78497ad054d6ba92bd711a03e00d912 |
| Private delivery source commit | c546431e23ee6fb91225395f15e22bc89bbd87b6 |

## Recovery and verification

The independent private Site source repository contains only its page and
packaging/verification scripts. Compiled ROM data is generated deployment output
and was **not committed to this GitHub repository or the Site source repository**.
The Site's native deployment reports success. Its transport code was exercised
with Node Web Streams against the actual published archive: all eight compressed
transport parts were verified, the reconstructed ROM matches the exact full
SHA-256 above, and corrupted parts or HTML login responses are rejected.
Transport parts assemble the already finished ROM; they are not ROM patches.

Private Site identity: `appgprj_6aeb0b07b70881918b7c86492f99b451`.
Saved version: `appgprj_6aeb0b07b70881918b7c86492f99b451~appgver_75e620490afc8191bd532b6449f7cc7a`.
Successful deployment: `appgdep_6aeb0c9eb96c81919f8c71353c5fa79d`.
Access was verified as owner-only: one allowed user and no external visitors.
Preserve that audience. Future cloud work can use these exact native Site IDs
to recover source access; no publishing credentials or tokens are stored here.

Actual iPhone browser saving and Manic gameplay still require user-device
testing. The captured native deployment screenshot shows the page preparing the
download; it is not proof of a completed iPhone download. Full campaign and
existing appearance/AI limits remain as documented in [REPORT.md](REPORT.md).
See [delivery validation](evidence/direct-download-validation.json).
