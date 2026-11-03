POKÉMON HEARTGOLD — COMPLETE STORY INTEGRATION AND PARTNER BATTLE DEVELOPMENT

PROJECT OVERVIEW

Game: Pokémon HeartGold (Nintendo DS)

Repository: mbanks26/pokeheartgold

Development: Codex Cloud

Testing: DeSmuME and Manic EMU on iPhone

You are continuing development of my customized Pokémon HeartGold ROM hack.

The game already has custom character graphics and a preliminary dual-follower system. Preserve all completed modifications.

Our goal is to keep the original HeartGold adventure largely intact while adding:

1. A customized male protagonist.
2. Sabrina as his established romantic partner and permanent traveling companion.
3. His redesigned sister as a competitive, independent Pokémon Trainer.
4. More natural, context-aware character dialogue.
5. Occasional scripted partner battles with Sabrina.
6. Genuine shiny starter Pokémon.
7. Eevee joining the sister’s team during her journey.
8. Expanded character acknowledgment throughout Johto and Kanto.

Implement the changes directly in the repository. Do not merely produce design notes or example code.

⸻

PHASE 1 — PROTECT EXISTING DEVELOPMENT

Before modifying anything:

* Inspect the repository, development branches, and recent commits.
* Locate the latest validated HeartGold development branch.
* Preserve all three customized character designs.
* Preserve Sabrina’s dual-follower implementation.
* Preserve the existing combined battle artwork.
* Confirm the current ROM builds successfully.
* Create a recoverable checkpoint.
* Preserve earlier test patches and working ROM builds.
* Do not reset or force-push existing branches.
* Do not merge unfinished changes into master.

The previous follower validation reported:

Commit: bcf2f8fd

Branch: development/sabrina-gameplay-validation-20261103

Verify the actual Git history rather than assuming that commit contains every later modification.

Previous Codex testing reported 88 passing automated assertions and successful DeSmuME tests for follower movement, map transitions, save/load, and Sabrina’s Gym battle.

Preserve this functionality.

⸻

PHASE 2 — CHARACTER CANON

Male protagonist

He replaces Ethan’s visual appearance.

His established design includes:

* Medium-dark brown skin.
* Black dreadlocks.
* Amber-brown eyes.
* Red-and-white jacket.
* Black shirt.
* Dark cargo pants.
* Red-and-white sneakers.

Preserve his existing character graphics, battle animations, and portraits.

His name must remain player-selectable.

Do not hardcode a character name.

He begins his Pokémon journey in New Bark Town.

He is dedicated to training, enjoys competition, and has a close relationship with his sister.

Do not excessively dictate his personality through NPC dialogue.

Sabrina

Sabrina is the official Saffron City Psychic-type Gym Leader.

Her existing redesigned appearance includes:

* Long black-green hair.
* Green eyes.
* Burgundy outfit.
* Black leggings.
* Burgundy boots.

Preserve all completed sprite and portrait work.

Established relationship

Sabrina and the protagonist have known each other since childhood.

Their fathers knew each other, and the protagonist’s father previously lived in Saffron City.

The families’ connection allowed Sabrina and the protagonist to spend considerable time together growing up.

He became familiar with Sabrina’s Psychic abilities and reserved personality.

Their relationship eventually became romantic.

They are already romantically involved at the beginning of HeartGold.

His immediate family knows about their relationship.

Sabrina does not need to introduce herself to his mother or sister.

Sabrina’s personality

Preserve Sabrina’s recognizable Pokémon characterization:

* Reserved.
* Intelligent.
* Perceptive.
* Confident.
* Disciplined.
* Sometimes intimidating.
* Exceptionally talented with Psychic Pokémon.

However, Sabrina is not a robot.

Take into account her anime characterization following her encounter with Ash, when she demonstrates laughter and a more emotionally expressive side.

Around trusted people, especially the protagonist and his sister, she can:

* Smile or laugh.
* Make dry jokes.
* Tease occasionally.
* Express affection.
* Become irritated.
* Disagree with decisions.
* Show concern.
* Enjoy ordinary experiences.

Do not make her excessively cheerful or emotionally detached.

She should behave naturally while retaining her reserved personality.

Protagonist’s sister

The character replacing Lyra’s NPC appearance is the protagonist’s sister.

They are not twins.

Her exact age difference is not established.

Her appearance includes:

* Fair skin.
* Long white hair.
* Red eyes.
* Burgundy-and-black feminine clothing.
* Burgundy ribbon.
* Gold hair accessories.

Preserve her completed character graphics.

Personality

She is competitive, confident, outgoing, witty, playful, and occasionally mischievous.

She frequently teases her brother.

Her teasing should feel affectionate rather than cruel.

She is proud of her progress as a Pokémon Trainer and enjoys comparing achievements with him.

She occasionally teases Sabrina as well.

However, she also has a serious side and can express genuine concern, encouragement, and maturity.

Her rivalry with her brother should feel different from Silver’s.

Silver remains the primary antagonistic rival of the original story.

Relationship with Sabrina

The sister has known Sabrina since childhood.

She initially thought Sabrina was strange because of her Psychic abilities and unusual behavior.

Over time, she grew to understand and like Sabrina.

They are now comfortable acquaintances with a long shared history.

They can joke, disagree, and discuss subjects unrelated to the protagonist.

She already knows Sabrina and her brother are romantically involved.

⸻

PHASE 3 — NATURAL DIALOGUE WRITING

One of the major weaknesses of our earlier FireRed hack was dialogue that sounded overly formal, repetitive, or robotic.

This HeartGold implementation must improve significantly.

General writing rules

* Characters must speak naturally.
* Avoid excessive exposition.
* Do not repeatedly explain established relationships.
* Vary conversation length.
* Allow natural humor.
* Allow disagreement.
* Keep each character’s personality distinct.
* Avoid repetitive compliments.
* Avoid excessive romantic declarations.
* Preserve the conversational atmosphere of Pokémon HeartGold.
* Keep dialogue within Nintendo DS text-box limitations.

Sabrina’s dialogue

Sabrina should not simply describe locations like a travel guide.

Bad example:

“This is Goldenrod City. It is a large city with a Department Store.”

Better example:

Sabrina: “I forgot how crowded Goldenrod gets.”

Sister: “You don’t sound happy about it.”

Sabrina: “I’m considering teleporting us somewhere quieter.”

Sister: “You wouldn’t.”

Sabrina: “Probably not.”

Use this style of natural interaction.

The exact dialogue may vary.

Sabrina should respond to events, people, environments, her own memories, and the protagonist’s choices.

She may occasionally have nothing important to say.

Sister’s dialogue

The sister should have her own sense of humor and competitiveness.

She should occasionally boast, challenge her brother, become frustrated after losing, or acknowledge when he’s done something impressive.

Do not make every interaction about Sabrina and the protagonist’s relationship.

Romantic dialogue

The protagonist and Sabrina are already in an established relationship.

Show this through familiarity, trust, subtle affection, humor, and occasional disagreements.

Avoid treating every conversation like a dramatic romantic confession.

Their relationship should feel comfortable and lived-in.

⸻

PHASE 4 — NEW BARK TOWN INTRODUCTION

Implement a revised opening sequence outside Professor Elm’s laboratory.

Opening scene

When the protagonist approaches Professor Elm’s laboratory, his sister is standing outside speaking with Sabrina.

Both recognize him immediately.

The sister teases him about taking so long to get ready.

Sabrina responds with her usual reserved humor.

Nobody formally introduces themselves.

The scene establishes their familiarity naturally.

Sister’s journey

The sister is preparing to begin her own Pokémon journey at approximately the same time as her brother.

She is competitive and excited to begin training.

She wants to see which sibling becomes the stronger trainer.

She does not have a significant head start or existing Gym Badges.

She may already have arrangements for receiving her first Pokémon, provided these fit the established story.

Preserve Professor Elm’s original starter selection and introductory events.

Departure

The sister leaves to begin her journey.

Use proper NPC movement rather than making her vanish abruptly.

She will reappear at selected points throughout Johto.

Sabrina remains with the protagonist.

Activate Sabrina’s existing human follower system through a persistent story flag.

The lead Pokémon must continue following normally through HeartGold’s native follower mechanics.

Critical compatibility

Preserve:

* Professor Elm’s laboratory.
* Original starter selection.
* Silver’s introductory appearances.
* The Pokémon Egg storyline.
* The Pokédex.
* The protagonist’s mother.
* Lyra’s required tutorial functions.
* Early game progression.

Do not break the original story to accommodate the new introduction.

⸻

PHASE 5 — GUARANTEED SHINY STARTER POKÉMON

I want the protagonist’s selected starter to be genuinely shiny.

HeartGold’s original starter choices must remain:

* Chikorita
* Cyndaquil
* Totodile

All three options should be shiny-capable by design, meaning whichever one the player chooses is guaranteed to be shiny.

Requirements

1. Preserve the three original starter choices.
2. Preserve their starting levels.
3. Preserve normal starter moves and abilities.
4. Preserve Professor Elm’s starter selection event.
5. Ensure the chosen Pokémon is genuinely shiny according to the game’s Pokémon data.
6. Do not merely recolor the Pokémon sprite.
7. Preserve normal Trainer ID, personality, and shiny calculation rules wherever possible.
8. Do not globally increase wild Pokémon shiny odds.
9. Do not make every NPC Pokémon shiny.
10. Do not automatically force Silver’s Pokémon to be shiny.
11. Ensure the Pokémon remains shiny after saving, loading, trading, and evolving.

The guaranteed shiny behavior should apply specifically to the protagonist’s initial starter.

Use the smallest reliable implementation appropriate to HeartGold’s existing Pokémon creation system.

If guaranteeing a shiny starter requires generating a suitable personality value, implement that carefully while preserving the Pokémon’s other legitimate attributes.

Testing

Automate tests for each of the three starter choices.

Verify actual shiny status, not just graphics.

If technically feasible, verify the shiny animation during the first battle.

Do not alter the base shiny probability elsewhere.

⸻

PHASE 6 — SISTER RECEIVES EEVEE

During her journey, the sister receives an Eevee.

This must be incorporated into her story rather than appearing without explanation.

Requirements

* She begins her journey around the same time as the protagonist.
* Eevee joins her team during the adventure.
* Introduce the acquisition through a short scripted encounter or believable dialogue.
* Give her a natural reaction to receiving Eevee.
* Maintain consistency during later encounters.
* Eevee should become a recognizable part of her Pokémon team.

I prefer that Eevee joins her during the early or middle portion of Johto, rather than beginning with an unexplained fully developed team.

Suggested story opportunity

Goldenrod City would be a suitable place because Eevee is already associated with Bill’s family in the Johto games.

Investigate the existing Bill/Eevee events and determine whether her acquisition can fit naturally without depriving the player of the original obtainable Eevee.

Do not remove or interfere with the player’s existing Eevee gift event.

If Goldenrod is unsuitable, choose another story-consistent location.

Future evolution

Do not choose Eevee’s final evolution yet.

Keep that decision open for a future development task.

Do not automatically reuse Leaf’s Vaporeon storyline from our separate FireRed hack.

The sister should have a sensible gradually developing team that matches her competitive personality.

Avoid legendary Pokémon or excessive early-game power.

⸻

PHASE 7 — SISTER’S INDEPENDENT JOURNEY

Expand selected original Lyra appearances.

She should travel independently rather than constantly following her brother.

Possible encounters include:

* New Bark Town.
* Cherrygrove City.
* Violet City.
* Goldenrod City.
* Ecruteak City.
* Olivine City.
* Blackthorn City.
* Pokémon League or late Johto.

Do not force her into every area.

Her encounters should have different purposes.

Some can be friendly conversations.

Others may involve competitive teasing or short battles.

She may discuss:

* Pokémon she has caught.
* Her Eevee.
* Training experiences.
* Gym challenges.
* Her brother’s progress.
* Sabrina.
* Their mother.
* Interesting things she has discovered.

Sibling battles

Implement a small number of optional or story-appropriate battles against the sister if they fit the original progression.

Use gradually developing Pokémon teams.

Avoid excessive difficulty spikes.

Do not replace Silver’s original rival battles.

⸻

PHASE 8 — SABRINA’S CONTEXT-AWARE DIALOGUE

Add meaningful dialogue throughout Johto and Kanto.

Important locations include:

* New Bark Town.
* Cherrygrove City.
* Violet City.
* Azalea Town.
* Goldenrod City.
* Ecruteak City.
* Olivine City.
* Mahogany Town.
* Blackthorn City.
* Pokémon League.
* Major Kanto locations.

Sabrina should know where she is, but she should not mechanically announce location facts.

Instead, let her respond naturally to circumstances.

For example:

Violet City

Sabrina might take an interest in the discipline of Sprout Tower’s monks.

Goldenrod City

She might react to the noise and crowds.

Ecruteak City

She might be interested in the city’s spiritual traditions.

Olivine City

She may express concern for the sick Ampharos.

Mahogany Town

She should recognize suspicious activities and react to Team Rocket’s involvement.

Blackthorn City

She may reflect on how much the protagonist has improved.

Pokémon League

Her dialogue should acknowledge the journey they have shared.

These are thematic guidelines, not mandatory lines.

Dialogue progression

Use established story flags to change conversations after:

* Gym victories.
* Important rival encounters.
* Team Rocket events.
* Major Pokémon discoveries.
* Significant story milestones.

Avoid spoilers and dialogue appearing before relevant events occur.

Do not repeat the same congratulatory lines after every badge.

⸻

PHASE 9 — OTHER CHARACTERS ACKNOWLEDGE SABRINA

Sabrina must not be invisible to the game world.

Relevant NPCs should recognize or react to her presence.

Protagonist’s mother

She already knows Sabrina and the relationship.

She recognizes the protagonist’s sister as her daughter.

Preserve all existing mother-related functions.

Professor Elm

He recognizes Sabrina as the Saffron City Gym Leader.

He may comment on her traveling through Johto, but should not behave as though she’s a complete stranger.

Sister

The sister talks naturally with Sabrina and the protagonist.

Their shared childhood history should be reflected through familiarity rather than exposition.

Silver

Silver initially may be suspicious or dismissive of Sabrina’s presence.

Over time, he may acknowledge her strength.

Preserve his original character development.

Gym Leaders

Relevant Gym Leaders may recognize Sabrina personally or by reputation.

Their reactions should vary.

Team Rocket

Certain Rocket members may recognize Sabrina because of her status and Team Rocket’s history in Kanto.

Sabrina’s presence should affect occasional dialogue, but she must not automatically solve the conflict.

The protagonist remains responsible for major story victories.

Other characters

Use selective acknowledgment from characters who have a legitimate reason to notice or recognize Sabrina.

Avoid excessive references.

⸻

PHASE 10 — SABRINA AS AN AI-CONTROLLED PARTNER IN MULTI BATTLES

NEW MAJOR FEATURE

HeartGold already supports Double Battles and certain partner-trainer mechanics.

I want Sabrina to participate in selected story battles as a genuine partner trainer.

This should not replace ordinary battles.

Battle structure

Most wild encounters and normal trainer battles remain Single Battles.

During selected scripted encounters, Sabrina joins the protagonist in a Multi Battle.

The protagonist controls one Pokémon.

Sabrina controls her own Pokémon independently.

Two opposing Pokémon participate according to the existing Multi Battle mechanics.

Sabrina must control her own Pokémon

This is essential.

Sabrina is an experienced Gym Leader.

Her Pokémon and actions must be controlled by the game’s AI, not by the player.

The player must not select Sabrina’s moves or command her Pokémon.

Sabrina should independently choose:

* Which move to use.
* Which opponent to target.
* When to use defensive or supportive moves.
* When to switch Pokémon, if supported by the selected battle format.
* How to respond to changing battle conditions.

Use an AI implementation consistent with her status as an experienced Psychic-type Gym Leader.

Prefer existing trainer-partner battle systems where feasible.

Do not create an entirely new battle engine if the game already supports the necessary mechanics.

Sabrina’s Pokémon

Use Sabrina’s canonical Psychic-type Pokémon identity as a foundation.

Her available Pokémon should be appropriate to the point in the story.

A reasonable progression might use:

* Abra/Kadabra during earlier encounters, where appropriate.
* Alakazam during more significant later battles.
* Other Pokémon consistent with her existing HeartGold Gym team.

However, do not arbitrarily weaken her official Gym Leader team or overwrite her actual Gym battle data.

Keep partner-battle team data separate from her Gym Leader team where necessary.

Battle AI

Sabrina should make reasonably intelligent decisions.

Her AI should:

* Select effective moves.
* Avoid obviously wasteful actions when possible.
* Consider type effectiveness.
* Use status moves appropriately.
* Avoid repeatedly attacking ineffective targets without reason.
* Preserve normal Pokémon battle rules.
* Avoid unnecessary friendly fire.
* Use appropriate targeting logic for partner battles.

Do not hardcode a scripted move sequence for every turn.

Her behavior should respond to actual battle conditions.

Important limitation

Do not give Sabrina illegal moves, impossible abilities, excessive stats, or unfair battle-only advantages simply to make her appear intelligent.

Use legitimate Pokémon data and a sensible AI configuration.

⸻

PHASE 11 — WHERE SABRINA PARTICIPATES IN PARTNER BATTLES

Select a small number of meaningful story encounters.

Potential events include:

Team Rocket — Slowpoke Well

Sabrina and the protagonist might confront two Team Rocket members.

Sabrina uses one Psychic Pokémon while the player uses their own lead Pokémon.

Preserve the original story’s outcome and required progression.

Goldenrod Radio Tower

Introduce an important partner battle during the Team Rocket takeover, if a suitable encounter can be adapted safely.

Sabrina should have relevant reactions to Team Rocket’s actions.

Mahogany Town — Rocket Hideout

Consider a partner battle against Team Rocket members during the hideout storyline.

Preserve Lance’s existing scripted role and original battle events.

Do not remove Lance or replace his established partner involvement.

Kanto

Include an additional partner battle if a natural opportunity exists during the postgame.

Encounter limits

Do not add partner battles indiscriminately.

Aim for approximately three or four meaningful scripted Sabrina battles across the complete adventure.

The exact selection should depend on existing script compatibility and gameplay pacing.

If a proposed event cannot safely support a Multi Battle, choose a more suitable encounter.

Dialogue before and after battles

Sabrina should speak naturally.

She might briefly suggest working together, comment on an opponent’s behavior, or express concern.

After the battle, she should react according to what happened.

Avoid repetitive victory speeches.

⸻

PHASE 12 — PARTNER BATTLE PRESENTATION

During normal Single Battles:

* Preserve the existing combined protagonist-and-Sabrina artwork where appropriate.
* Sabrina remains a visual companion.
* She does not participate in combat.

During Sabrina partner battles:

* Use a suitable partner-trainer presentation.
* Sabrina sends out her own Pokémon.
* The protagonist sends out one of their Pokémon.
* The player controls only their own Pokémon.
* Sabrina’s choices are handled independently by AI.
* Preserve appropriate battle animations and text.

Use compatible trainer sprites and battle messages.

Ensure Sabrina’s Pokémon is visually and mechanically distinct from the player’s Pokémon.

Avoid duplicated sprites or contradictory battle artwork.

After battle

Restore the normal traveling formation.

Sabrina must return to following the protagonist and their lead Pokémon.

Preserve all battle results, experience, money, and story flags according to HeartGold’s mechanics.

Handle victory, defeat, and interruptions safely.

⸻

PHASE 13 — SABRINA’S SAFFRON GYM BATTLE

Sabrina remains the official Gym Leader of Saffron City.

When the protagonist reaches her Gym:

1. She temporarily leaves the traveling formation.
2. Her companion state remains saved.
3. She resumes her official Gym Leader position.
4. She battles the protagonist herself.
5. Her own Pokémon are controlled by the opposing-trainer AI.
6. The protagonist battles her normally.
7. Preserve the original Gym battle structure.
8. Preserve the Marsh Badge.
9. Preserve the original Gym rewards.
10. Sabrina must not appear beside the player during her own Gym battle.
11. After victory, she returns to the protagonist’s side.
12. If the protagonist loses, allow a normal retry.
13. Preserve existing rematch compatibility.

Story characterization

Sabrina will not give the protagonist special treatment.

She has accompanied him through his journey and knows how much he has improved.

Her dialogue should reflect familiarity and professional respect.

Avoid overly dramatic speeches.

The Gym battle should remain a meaningful challenge.

⸻

PHASE 14 — FOLLOWER AND STORY EVENT COMPATIBILITY

Preserve the existing dual-follower arrangement:

Protagonist → Lead Pokémon → Sabrina

Sabrina must remain an independent human follower.

Do not replace the lead Pokémon’s existing following mechanic.

During scripted conversations, Gym events, and partner battles:

* Safely manage Sabrina’s object.
* Prevent duplicate companions.
* Avoid NPC collisions.
* Restore her after battle.
* Preserve save/load behavior.
* Handle map transitions.
* Prevent broken cutscenes.
* Preserve all original story flags.

Use existing follower utilities wherever possible.

⸻

PHASE 15 — DEVELOPMENT AND TESTING ORDER

Implement this assignment incrementally.

Stage A — Opening and relationships

* New Bark Town introduction.
* Sister’s departure.
* Sabrina’s companion activation.
* Mother and Elm dialogue.

Build and test.

Stage B — Sister’s journey

* Recurring encounters.
* Competitive dialogue.
* Eevee acquisition.
* Basic team progression.

Build and test.

Stage C — Shiny starters

* Guarantee the selected starter is genuinely shiny.
* Test Chikorita, Cyndaquil, and Totodile.
* Preserve wild shiny odds and all unrelated Pokémon.

Build and test.

Stage D — Sabrina dialogue

* Location-aware conversations.
* Story-dependent responses.
* Other NPCs acknowledging Sabrina.
* Dialogue quality review.

Build and test.

Stage E — Partner battles

* Audit existing Multi Battle architecture.
* Implement Sabrina as an AI-controlled partner.
* Add an initial controlled test battle.
* Verify her independent move selection.
* Expand to a small number of story encounters.
* Test battle completion and companion restoration.

Build and test.

Stage F — Saffron Gym and regression testing

* Verify Sabrina’s Gym battle.
* Verify victory/loss paths.
* Verify companion restoration.
* Verify story progression.
* Verify save/load.
* Verify character graphics remain unchanged.

⸻

PHASE 16 — REQUIRED VALIDATION

Run automated tests and available emulator scenarios.

Required areas include:

1. New game initialization.
2. Correct protagonist graphics.
3. Sister’s introduction and departure.
4. Normal starter selection.
5. Genuine shiny starter status.
6. Normal wild shiny probability.
7. Sabrina’s introduction and follower activation.
8. Native following Pokémon behavior.
9. Mother and Professor Elm dialogue.
10. Silver’s original story events.
11. Sister’s recurring appearances.
12. Eevee acquisition.
13. Preservation of the player’s original Eevee gift.
14. Sabrina’s dialogue progression.
15. Other NPC acknowledgment.
16. Standard Single Battles.
17. Sabrina AI-controlled Multi Battles.
18. Sabrina’s independent move selection.
19. Battle victory and defeat handling.
20. Companion restoration after partner battles.
21. Sabrina’s Saffron Gym challenge.
22. Marsh Badge award.
23. Sabrina’s solo opponent presentation.
24. Save/load persistence.
25. Preservation of all custom graphics.
26. Existing follower regression tests.

Use DeSmuME for emulator testing where possible.

Clearly distinguish static tests, successful compilation, automated emulator scenarios, and actual visual testing.

Do not claim the full game is stable without appropriate verification.

⸻

PHASE 17 — DELIVERABLES

Provide:

1. Implemented New Bark Town introduction.
2. New sister dialogue and recurring encounters.
3. Sister’s Eevee acquisition event.
4. Guaranteed shiny starter functionality.
5. Updated Sabrina dialogue throughout Johto and Kanto.
6. NPC recognition of Sabrina.
7. AI-controlled Sabrina partner battles.
8. Appropriate Sabrina partner Pokémon data.
9. Working Saffron Gym battle integration.
10. List of modified source and asset files.
11. New story flags and their meanings.
12. Successful HeartGold ROM build.
13. Automated and emulator testing results.
14. Known limitations.
15. A playable .nds test build or suitable patch.
16. iPhone-compatible testing instructions.
17. A recoverable Git commit pushed to the appropriate development branch.

Commit and push completed, tested work after each major stage.

Do not overwrite the previous stable ROM.

Do not force-push or merge into master without explicit approval.

⸻

FINAL INSTRUCTIONS

I am developing entirely from an iPhone using Codex Cloud.

Handle source editing, event scripting, graphics integration, battle AI integration, compilation, and automated testing autonomously.

Prioritize reliability, preservation of the original HeartGold storyline, and natural character writing.

Sabrina must remain an established romantic partner, a recognizable character with genuine emotional range, and an experienced Psychic Gym Leader.

The sister must remain competitive, playful, independent, and affectionate toward her brother.

The protagonist should retain his player-selected name and original gameplay role.

Begin by auditing the current repository and protecting completed work. Then implement the revised New Bark Town introduction, the sister’s journey and Eevee acquisition, shiny starters, natural dialogue, and Sabrina’s independently controlled partner battles in validated stages.

If a requested feature cannot be implemented safely, preserve the current playable build, explain the technical blocker, and complete the remaining independent features.