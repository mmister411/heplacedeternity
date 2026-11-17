# Testimony Tracker

This tracker connects people, reported optasiological experiences, accounts, source artifacts, scenes, and the phenomena described within them. It also records decisions about material proposed for the *Atlas of Perdition*.

The [source discovery register](source_discovery_register.tsv) holds initial leads, including the collector's 59-name list. Person folders contain collected texts and other source material. A discovery ID (PROS-001, etc.) identifies a lead; it does not necessarily identify a distinct witness or experience.

## Record model

| Record | What it identifies | Example or reference |
|---|---|---|
| Person | A witness, narrator, interviewer, translator, editor, collector, or other participant. Record each role in relation to an account. | [Angelica Zambrano](angelica-zambrano/readme.md) |
| Experience | One reported occurrence, which may include several settings or encounters. Use a stable ID; do not create a new event for each retelling. | AZ-01 through AZ-04 |
| Account | A particular telling, interview, translation, transcription, or edition of one or more experiences. | AZ-01/A1 |
| Source artifact | An identifiable file, page, recording, image, or manuscript carrying an account. | AZ-01 transcript file |
| Scene or passage | A bounded portion of an account, identified by page, paragraph, line, or timestamp. | Assign a segment ID when indexed |
| Reported feature | A being, place, structure, implement, action, condition, sensory quality, speech, transition, or other feature within one account scene. | Assign a source-local observation ID |
| Motif or type | A recurring feature category used to connect observations across accounts without treating them as the same occurrence. | Link related observations by motif ID |
| Relation | A source-anchored connection among records or described elements. | A scene describes a passageway leading to a chamber |
| Atlas decision | The author's decision concerning specified passages, scenes, or phenomena, including the exact approved scope. | Assign a decision ID when made |

These record types connect in several directions:

- A person may report several experiences. Several people may testify about one event.
- An experience may have several accounts. One account may discuss more than one experience.
- An account may appear in several source artifacts, including translations and revisions.
- A scene may describe several features. Similar features from different witnesses may share a motif without being treated as the same observed instance.
- A reported relationship, such as containment, movement, sequence, agency, or location, must retain its source passage.
- An Atlas decision attaches to the material actually considered, not automatically to an entire person or every account from that person.

Existing identifiers stay fixed. Keep AZ-01 through AZ-04 as experience IDs and AZ-01/A1 through AZ-04/A1 as account IDs. Scene IDs can extend an account ID (for example AZ-01/A1/S01); source-local observations and shared motifs receive their own IDs. Preserve links when names or classifications change.

## Optasiological classification

Classification follows the reported content, with multiple values where necessary.

| Dimension | Initial values and distinctions |
|---|---|
| Reported mode | Dream; vision; trance; near-death experience; return from reported death; prophetic disclosure; interpreted tongues; other; undetermined |
| Person's role | Experiencer; eyewitness to surrounding events; narrator; interviewer; intermediary; translator; editor; compiler |
| Reported setting | Heaven; Perdition; earthly setting; passage or threshold; other; undetermined. Mixed accounts retain each setting. |
| Described element | Place or region; boundary or passage; being or person; object or implement; event or operation; bodily condition; sensory quality; speech or communication; other |
| Relation | Within; adjacent to; leads to; precedes; follows; acts upon; causes; restrains; contains; resembles; refers to; other |
| Evidence and attribution | Who states it, which account carries it, the passage anchor, and the established O/F/H/K/S/I knowledge mode when assigned |
| Atlas locus | Infernal proper; threshold/transit; operationally adjacent; non-infernal; undetermined, as defined by the [Atlas Inclusion Measure](../apparatus/Atlas_of_Perdition_Inclusion_Criteria.md) |

Reported modes, settings, and subjects are separate classifications. A heavenly scene in a mixed account remains heavenly; a threshold scene receives its own locus. More specific categories can be added as the accounts require.

A source-anchored relation should identify its speaker or mediator and distinguish what the account says from an editor's wording or a later analytical connection. Cross-witness similarities may be linked without treating repeated publications of one account as independent testimonies.

## Relationship ledger

Each relation can be recorded as a separate link with five parts: **subject ID, predicate, object ID or value, source anchor, and attribution**. Source metadata can anchor links such as *translation of* or *recounts*. Passage references anchor reported locations, actions, sequence, containment, speech, and other relations within an experience.

| Subject | Predicate | Object or value | Source anchor | Attribution |
|---|---|---|---|---|
| AZ-01/A1 | recounts | AZ-01 | [English edited account](angelica-zambrano/experience-01/transcript.en.edited.md) | Published account attributed to Angelica Zambrano |

New predicates may be added without changing the record classes. Distinguish a relation stated within testimony from one supplied by translation, editorial framing, or later analysis.

## Collected experiences and accounts

| Experience | Person | Collected account | Source condition | Collection state |
|---|---|---|---|---|
| [AZ-01](angelica-zambrano/experience-01/readme.md) | Angelica Zambrano | [AZ-01/A1: English edited text](angelica-zambrano/experience-01/transcript.en.edited.md) | Publisher identifies it as edited and minimally abridged | Archived |
| [AZ-02](angelica-zambrano/experience-02/readme.md) | Angelica Zambrano | [AZ-02/A1: English published text](angelica-zambrano/experience-02/transcript.en.published.md) | English text from HeavenVisit | Archived |
| [AZ-03](angelica-zambrano/experience-03/readme.md) | Angelica Zambrano | [AZ-03/A1: English published text](angelica-zambrano/experience-03/transcript.en.published.md) | English text from HeavenVisit | Archived |
| [AZ-04](angelica-zambrano/experience-04/readme.md) | Angelica Zambrano | [AZ-04/A1: English partial text](angelica-zambrano/experience-04/transcript.en.partial.md) | Published telling covers part of the fourth experience | Archived |

Each experience folder maintains its source links, textual history, and account outline. New tellings of an existing experience are added as accounts under the same experience ID. Scene, observation, and motif records are created as their source passages are indexed.

## Assessment and Atlas disposition

The [Atlas Inclusion Measure](../apparatus/Atlas_of_Perdition_Inclusion_Criteria.md) scores the descriptive yield of each passage or scene on U or 0–4. Record its infernal locus and source anchor separately.

The author approves Atlas inclusion for a **specified scope**. A proposal can be made during analysis; approval, approval with conditions, deferral, or rejection is recorded only from the Atlas author's decision. A blank decision field means no decision has been recorded.

| Decision ID | Proposed passage(s) or phenomena | Account and source anchor | AIM / locus | Decision | Author's decision reference and date | Approved scope / Atlas location |
|---|---|---|---|---|---|---|

No new inclusion decisions are recorded for AZ-01 through AZ-04.

The discovery register also identifies Mary K. Baxter (PROS-032) and Park Young Moon (PROS-042) as represented in the existing Atlas corpus. Their historic records remain in the apparatus; passage-specific decisions can be entered here when examined.

## Adding records

1. Identify the person and the distinct reported experience. Reuse an existing experience ID for another account of the same occurrence.
2. Link the account to a source artifact. Record language, translation, editing, completeness, and source dates where known; distinguish event date from recording or publication date.
3. Anchor scenes and statements to passages or timestamps. Classify reported modes, settings, described elements, and relationships as the material establishes them.
4. Record AIM findings against passages or scenes and link proposals to their exact source anchors.
5. Record author decisions in the disposition table with date, reference, and scope. If a decision changes, add a new entry referring to the earlier decision.

The tables can be split into separate machine-readable registers as the collection grows, retaining the same IDs and relations. The tracker remains the index for current disposition decisions; the source discovery register retains the original first-pass research statuses.
