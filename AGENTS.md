# Agent charter — He Placed Eternity

This file is the standing operating charter for an agent working in this repository without prior conversation context. Read it before changing data or code. Do not treat it as a substitute for examining the sources.

## Mission and standard of success

*He Placed Eternity* investigates salvation, perdition, and eternal life under the authority of Scripture, using accounts of reported optasiological experiences and careful reasoning. The two Atlases ask, among other things, **“What is perdition like?”** and the corresponding question about Eternal Life. The shared research apparatus should progressively reconstruct what accepted testimonies describe: environments, structures, inhabitants, objects, conditions, sensations, speech, actions, transformations, transitions, and the relationships among them.

Success is not a high count of extracted labels. It is an increasingly detailed, intelligible, source-traceable account of reported spiritual existence, with scene context, variation, and uncertainty intact. Scripture establishes what it establishes; witnesses contribute what they report; analysis draws only the conclusions its evidence supports. Do not silently exchange one kind of authority for another.

## Authority and decisions

The human author alone decides whether a **prospective optasiological event (POE)** is `valid` (a **valid optasiological event**, or VOE, eligible for Atlas analysis) or `unusable`. A new experience registered by an agent starts `pending`. The authoritative decision and its history are in [`poe_register.tsv`](poe_register.tsv). Never set or imply a human decision without the author's explicit instruction. `valid` is acceptance for study, **not proof that the supernatural report occurred**.

Acquisition, provenance work, source comparison, and location assessment can proceed for pending material. Formal observation extraction and synthesis in the working apparatus use accepted VOEs. Once a POE is `valid`, no second, scene-by-scene processing authorization is needed under the current workflow. Do not revive earlier approval gates from the historical testimony tracker. If the author explicitly changes a boundary, follow that instruction and record the consequential change appropriately.

For operating method, this charter governs over older narrative instructions in trackers or reports. The POE register governs actual author decisions; source artifacts govern what their witnesses or editors actually say; the current code and file schemas govern machine-valid structure. A new direct instruction from the author overrides this standing workflow. Historical research may be cited as evidence of previous work, not treated as current procedural authority.

## What the records mean

Keep these different units distinct:

- **Person:** witness, narrator, translator, editor, interviewer, or collector; identify the role rather than assigning an intermediary's words to the experiencer.
- **Experience (POE/VOE):** a distinguishable reported occurrence, potentially spanning several locations and scenes. One person may report several experiences.
- **Source work, account, and artifact:** a book, telling, interview, edition, translation, extract, recording, or local file. Several versions can report one experience; one work can describe several. A source-work POE record does not itself settle the boundaries of every experience it contains.
- **Scene:** a coherent passage or episode within an experience, bounded by what the account reports. It is not automatically a new POE.
- **Observation:** a specific reported particular within a scene, with its relevant properties and evidence mode.
- **Relation or motif:** a source-grounded connection among particulars, or a curated comparison across reports. Similarity does not establish identity or independent confirmation.

For example, Mary K. Baxter's extended source work includes multiple narrated visits and many chapters. A chapter, source file, and reported excursion are not interchangeable. Likewise, the same woman changing appearance in a rocking chair is a coherent reported figure with a setting, sequence, appearance, speech, and actions; do not scatter her properties into disconnected labels.

## Source acquisition and provenance

There is one shared [`testimonies/`](testimonies/) collection. Preserve accounts in their available form and preserve the identity of the witness, source, edition, translation, and editorial intervention wherever known. The collector's original [compilation](testimonies/_intake/Experiences_1.txt) preserves collected testimony text and editorial framing as an archived source artifact. The compilation is not an additional witness and does not itself establish the fidelity or completeness of a telling. `compilation_only` describes the material on hand, not a verdict on reliability. Examine attribution, editing, omissions, and variant history where these affect a claim. Separately acquired editions can help resolve those questions but are **not prerequisites** for intake or human POE review.

An external URL is a discovery lead until a testimony document has actually been archived. A partial source remains usable testimony, but must not be called complete. Multiple copies or mirrors are not new experiences. Source-copy files are recorded with their original format, path, retrieval information, byte count, and checksum in [`source_copy_register.tsv`](testimonies/source_copy_register.tsv); compilation extracts and other holdings are indexed in [`source_manifest.tsv`](testimonies/source_manifest.tsv). Preserve original bytes and provenance when editing metadata. An acquired work may remain unassigned with a blank `experience_id` while event boundaries are investigated. Do not invent segmentation merely to fill a field.

Do not conflate similarly named witnesses, attribute a parent's retelling to the child as firsthand speech, or promote a collector's presentation to a witness quotation. Unknown dates, identities, translation histories, and publication status can remain unknown. Copyright or republication concerns may affect publication choices but are not validation gates for collecting and studying testimony.

## Method of observation and reconstruction

Read the actual source passage and enough surrounding text to understand its scene, sequence, speaker, and setting. Preserve meaningful descriptions: what a thing looked, sounded, felt, smelled, or behaved like; its position, relationships, changes, and reported function. An observation may have several properties. Do not over-segment coherent entities or ignore distinct particulars to make the data simpler.

Before accepting a scene or observation, resolve its source artifact and passage locator against the correct text. Master-compilation line numbers and witness-specific extract line numbers are not interchangeable. Confirm that the description is recoverable from the cited passage in context, that speech and editorial framing are attributed correctly, and that any reused historical observation ID identifies the intended record. Passing a structural validator cannot substitute for checking the underlying text.

Distinguish firsthand sight, hearing, sensation, claimed knowledge, speech attributed to an encountered being, retrospective witness interpretation, editor framing, and researcher inference. A guide's claim about a place or a prisoner's account of why they are confined is testimony about **speech**; it need not be a directly observed property of the place. Preserve exact source anchors and the basis for any inference. A named location and an observed location are not synonymous: mere mention of Heaven, Hell, or the lake of fire does not establish a reported visit or witnessed scene. Use the [POE location flags](poe_register.tsv) with the recorded basis and their existing evidence states.

When relating testimony to Scripture, examine the biblical passage in its immediate context and relevant canonical relationships. Distinguish what Scripture expressly describes, what it soundly entails, what shares an analogy or applicable principle with a report, and which reported details Scripture does not establish. The inherited direct/principle/analogy/extension categories are judgments to verify against the text, not permission to extend biblical claims to every property of an observed scene. Preserve Scripture's actual force, scope, and mode alongside the witness's account.

Compare reports without assembling a fictitious composite geography. Note shared features, material differences, scene boundaries, possible literary dependence, and unresolved identification. Baxter and Carmelo Brenes both recount a transforming woman in a rocking chair; the parallel does not prove that two independent witnesses encountered the same person or cell. Apparent disagreement may concern different scenes, voices, or conditions. Record both observations before attempting synthesis. Interpretative labels remain revisable; unknown relationships may remain unknown.

The shared [`apparatus/`](apparatus/) is **location-neutral**. Location is a reported or inferred property of an observation, not a reason to duplicate schemas for Perdition and Paradise. Keep core concepts general—scene, observation, property, action, state, relationship, evidence—and let specific categories emerge from actual reports. Do not invent fixed fields for expected objects or realms. Preserve the historical Perdition classifications without imposing them as universal ones.

The inherited [curated observations](apparatus/atlas_phenomena_seed.tsv) and [motif families](apparatus/atlas_motif_families.tsv) are real prior work, not disposable placeholders. The generated [phenomena register](apparatus/Atlas_of_Perdition_Phenomena_Register.jsonl) is derived from the curated seed. The scene-based [`evidence.jsonl`](apparatus/evidence.jsonl) is complementary, not a replacement; its `legacy_ref` links back to selected earlier observations. Do not bulk-clone all inherited observations, fabricate scene boundaries from line proximity, or count the two representations as separate evidence. Existing relations are analytical proposals, never self-validating corroborations.

## How to resume work

Start by reading this charter, the root [README](README.md), the [testimony guide](testimonies/readme.md), and the [apparatus guide](apparatus/README.md). Inspect current Git history and registers rather than relying on dated counts in prose. Verify the repository before modifying it:

```sh
python poe_registry.py check
python poe_registry.py intake
python apparatus/evidence.py check
python apparatus/evidence.py inherited --summary
python -m unittest discover -s apparatus -p test_evidence.py
```

For the earlier curated extraction, run `python build_phenomena_register.py` from `apparatus/` when its output needs verification. The initial compilation is at `testimonies/_intake/Experiences_1.txt`; archived witness-specific copies are in their testimony folders. Follow the currently implemented commands and their help output rather than guessing CLI arguments.

Choose the next substantive gap from the actual state: an unexamined accepted VOE passage, missing scene context, a comparison needing source review, a source work whose events need careful segmentation, or a promising testimony lead that needs acquisition. Work across multiple VOEs where useful; there is no one-witness-at-a-time rule. For every contribution, trace it back to an archived source, preserve existing IDs and historical findings, and distinguish new work from a revised interpretation. Leave unresolved matters visible instead of forcing completion.

A research increment is complete when the selected passage or bounded group of passages has been read in context; its meaningful particulars, sequence, and relationships have been represented at the warranted level of detail; citations and reused identifiers have been checked; uncertainties are marked; and applicable verification has been performed. A coherent increment need not exhaust an entire source work or VOE, and its coverage must not be described as exhaustive when it is not.

Use scripts, validation, and source-level review to check the result. Do not alter accepted POE decisions, rewrite archival source files, regenerate unrelated datasets, or introduce duplicate trackers or elaborate bureaucracy as a substitute for research. Keep changes reviewable and commit coherent, verified batches through the available repository workflow when authorized. Report what was actually added or verified, what remains unresolved, and any tests not run. Never claim successful verification or a merge before it occurred.

A new agent has succeeded in taking over when it can continue the research **without this conversation**, preserve the author's decisions, and produce a useful new source-grounded result without losing the testimony's distinctions.
