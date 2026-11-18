# Testimony Tracker

This tracker connects people, reported optasiological experiences, accounts, source artifacts, scenes, and the phenomena described within them. It also records decisions about material proposed for the *Atlas of Perdition*.

The [matching-edition register](edition_match_register.md) identifies published wording close to the archived compilation. The [source discovery register](source_discovery_register.tsv) holds initial leads, including the collector's 59-name list. Person folders contain collected texts and other source material. A discovery ID (PROS-001, etc.) identifies a lead; it does not necessarily identify a distinct witness or experience.

## Record model

| Record | What it identifies | Example or reference |
|---|---|---|
| Person | A witness, narrator, interviewer, translator, editor, collector, or other participant. Record each role in relation to an account. | [Angelica Zambrano](angelica-zambrano/readme.md) |
| Experience | One reported occurrence, which may include several settings or encounters. Use a stable ID; do not create a new event for each retelling. | AZ-01 through AZ-04 |
| Account | A particular telling, interview, translation, transcription, or edition of one or more experiences. | AZ-01/A1 |
| Source artifact | An identifiable file, page, recording, image, or manuscript carrying an account. | AZ-01 transcript file |
| Working corpus unit | A bounded section of an existing compilation, sometimes containing more than one experience or account. | DAN, BAX, AZ1, FER, etc. |
| Scene or passage | A bounded portion of an account, identified by page, paragraph, line, or timestamp. | Assign a segment ID when indexed |
| Reported feature | A being, place, structure, implement, action, condition, sensory quality, speech, transition, or other feature within one account scene. | Assign a source-local observation ID |
| Motif or type | A recurring feature category used to connect observations across accounts without treating them as the same occurrence. | Link related observations by motif ID |
| Relation | A source-anchored connection among records or described elements. | A scene describes a passageway leading to a chamber |
| Processing authorization | The author's permission to perform specified analysis on identified collected material. | Record scope, date, and reference when granted |
| Atlas decision | The author's decision concerning specified passages, scenes, or phenomena, including the exact approved scope. | Assign a decision ID when made |

These record types connect in several directions:

- A person may report several experiences. Several people may testify about one event.
- An experience may have several accounts. One account may discuss more than one experience.
- An account may appear in several source artifacts, including translations and revisions.
- A working corpus unit records a segment of a compiled text; it does not necessarily represent one distinct experience.
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
| Atlas locus | Infernal proper; threshold/transit; operationally adjacent; non-infernal; undetermined |

Reported modes, settings, and subjects are separate classifications. A heavenly scene in a mixed account remains heavenly; a threshold scene receives its own locus. More specific categories can be added as the accounts require.

A source-anchored relation should identify its speaker or mediator and distinguish what the account says from an editor's wording or a later analytical connection. Cross-witness similarities may be linked without treating repeated publications of one account as independent testimonies.

## Relationship ledger

Each relation can be recorded as a separate link with five parts: **subject ID, predicate, object ID or value, source anchor, and attribution**. Source metadata can anchor links such as *translation of* or *recounts*. Passage references anchor reported locations, actions, sequence, containment, speech, and other relations within an experience.

| Subject | Predicate | Object or value | Source anchor | Attribution |
|---|---|---|---|---|
| AZ-01/A1 | recounts | AZ-01 | [English edited account](angelica-zambrano/experience-01/transcript.en.edited.md) | Published account attributed to Angelica Zambrano |

New predicates may be added without changing the record classes. Distinguish a relation stated within testimony from one supplied by translation, editorial framing, or later analysis.

## Previously processed corpus units

The [Corpus Survey](../apparatus/Atlas_of_Perdition_Corpus_Survey.md) identifies 16 working text units from 13 named witnesses. The [phenomena seed](../apparatus/atlas_phenomena_seed.tsv) contains 426 records indexed to those units. The line ranges refer to the working compilation `Pasted text(20261116-025409).txt`, which is not stored in this repository.

| Unit ID | Witness or account | Compilation lines | Phenomena | Experience boundary | Collection record or archived text |
|---|---|---|---:|---|---|
| DAN | Daniel Ekechukwu | 306–349 | 14 | Shorter mediated telling DA2 is linked | [DAN source register](daniel-ekechukwu/experience-01/sources.md) · [Compilation copy](daniel-ekechukwu/experience-01/compilation-extract.en.txt) |
| BAX | Mary K. Baxter, *A Divine Revelation of Hell* | 350–2008 | 112 | 26 chapters; event boundaries remain source-specific | [BAX source register](mary-k-baxter/experience-01/sources.md) · [Compilation copy](mary-k-baxter/experience-01/compilation-extract.en.txt) |
| MEL | Bryan Melvin | 2009–2042 | 35 |  | [MEL source register](bryan-melvin/experience-01/sources.md) · [Compilation copy](bryan-melvin/experience-01/compilation-extract.en.txt) |
| PER | Jennifer Perez | 2043–2145 | 17 |  | [PER source register](jennifer-perez/experience-01/sources.md) · [Compilation copy](jennifer-perez/experience-01/compilation-extract.en.txt) |
| ALB | Aline Baxley, *I Walked in Hell* | 2226–2281 | 12 |  | [ALB source register](aline-baxley/experience-01/sources.md) · [Compilation copy](aline-baxley/experience-01/compilation-extract.en.txt) |
| AZ1 | Angelica Zambrano, first experience | 2338–2813 | 29 | [AZ-01](angelica-zambrano/experience-01/readme.md) | [Edited English text](angelica-zambrano/experience-01/transcript.en.edited.md) · [Compilation copy](angelica-zambrano/experience-01/compilation-extract.en.txt) |
| AZ2 | Angelica Zambrano, second experience | 2814–3034 | 20 | [AZ-02](angelica-zambrano/experience-02/readme.md) | [English text](angelica-zambrano/experience-02/transcript.en.published.md) · [Compilation copy](angelica-zambrano/experience-02/compilation-extract.en.txt) |
| AZ3 | Angelica Zambrano, third experience | 3035–3383 | 23 | [AZ-03](angelica-zambrano/experience-03/readme.md) | [English text](angelica-zambrano/experience-03/transcript.en.published.md) · [Compilation copy](angelica-zambrano/experience-03/compilation-extract.en.txt) |
| AZ4 | Angelica Zambrano, fourth experience | 3384–3545 | 8 | [AZ-04](angelica-zambrano/experience-04/readme.md) | [Partial English text](angelica-zambrano/experience-04/transcript.en.partial.md) · [Compilation copy](angelica-zambrano/experience-04/compilation-extract.en.txt) |
| BRE | Carmelo Brenes, *Rescued from Hell* | 3546–3617 | 35 |  | [BRE source register](carmelo-brenes/experience-01/sources.md) · [Compilation copy](carmelo-brenes/experience-01/compilation-extract.en.txt) |
| PAR | Young Moon Park | 3618–3671 | 14 |  | [PAR source register](young-moon-park/experience-01/sources.md) · [Compilation copy](young-moon-park/experience-01/compilation-extract.en.txt) |
| APY | Athet Pyan Shinthaw Paulu | 3676–3775 | 14 |  | [APY source register](athet-pyan-shinthaw-paulu/experience-01/sources.md) · [Compilation copy](athet-pyan-shinthaw-paulu/experience-01/compilation-extract.en.txt) |
| FER | Bernarda Fernández | 3780–3851 | 13 | Two journeys within this source unit | [FER source register](bernarda-fernandez/sources.md) · [Compilation copy](bernarda-fernandez/compilation-extract.en.txt) |
| WIE | Bill Wiese, *23 Minutes in Hell* | 3856–4194 | 36 |  | [WIE source register](bill-wiese/experience-01/sources.md) · [Compilation copy](bill-wiese/experience-01/compilation-extract.en.txt) |
| KNI | Carl Knighton | 4195–4248 | 7 |  | [KNI source register](carl-knighton/experience-01/sources.md) · [Compilation copy](carl-knighton/experience-01/compilation-extract.en.txt) |
| PUR | Aaron Purser, *A Visit to Hell* | 4304–4474 | 37 |  | [PUR source register](aaron-purser/experience-01/sources.md) · [Compilation copy](aaron-purser/experience-01/compilation-extract.en.txt) |
| **Total** | **13 named witnesses; 16 units** | | **426** | | |

This table records existing apparatus work. The four separately archived Zambrano English texts are related published accounts; they have not been matched line by line to the compilation versions. The historical compilation is now preserved in full, divided into 16 principal source units and five related companion extracts. Each witness folder holds a byte-exact copy of its complete compilation section and links to external editions. The compilation copies have not yet been collated line by line against the external editions.

## Collected experiences and accounts

| Experience | Person | Collected account | Source condition | Collection state |
|---|---|---|---|---|
| [AZ-01](angelica-zambrano/experience-01/readme.md) | Angelica Zambrano | [AZ-01/A1: English edited text](angelica-zambrano/experience-01/transcript.en.edited.md) | Publisher identifies it as edited and minimally abridged | Archived |
| [AZ-02](angelica-zambrano/experience-02/readme.md) | Angelica Zambrano | [AZ-02/A1: English published text](angelica-zambrano/experience-02/transcript.en.published.md) | English text from HeavenVisit | Archived |
| [AZ-03](angelica-zambrano/experience-03/readme.md) | Angelica Zambrano | [AZ-03/A1: English published text](angelica-zambrano/experience-03/transcript.en.published.md) | English text from HeavenVisit | Archived |
| [AZ-04](angelica-zambrano/experience-04/readme.md) | Angelica Zambrano | [AZ-04/A1: English partial text](angelica-zambrano/experience-04/transcript.en.partial.md) | Published telling covers part of the fourth experience | Archived |
| [DAN-01](daniel-ekechukwu/readme.md) | Daniel Ekechukwu | [3 source links](daniel-ekechukwu/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [BAX-W01](mary-k-baxter/readme.md) | Mary K. Baxter | [4 source links](mary-k-baxter/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [MEL-01](bryan-melvin/readme.md) | Bryan Melvin | [3 source links](bryan-melvin/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [PER-01](jennifer-perez/readme.md) | Jennifer Perez | [3 source links](jennifer-perez/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [ALB-01](aline-baxley/readme.md) | Aline Baxley | [2 source links](aline-baxley/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [BRE-01](carmelo-brenes/readme.md) | Carmelo Brenes | [3 source links](carmelo-brenes/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [PAR-01](young-moon-park/readme.md) | Young Moon Park | [3 source links](young-moon-park/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [APY-01](athet-pyan-shinthaw-paulu/readme.md) | Athet Pyan Shinthaw Paulu | [3 source links](athet-pyan-shinthaw-paulu/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [FER-01 / FER-02](bernarda-fernandez/readme.md) | Bernarda Fernández | [4 source links](bernarda-fernandez/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [WIE-01](bill-wiese/readme.md) | Bill Wiese | [4 source links](bill-wiese/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [KNI-01](carl-knighton/readme.md) | Carl Knighton | [3 source links](carl-knighton/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |
| [PUR-01](aaron-purser/readme.md) | Aaron Purser | [1 source link](aaron-purser/experience-01/sources.md) | External full texts, interviews, and/or documents; see source record | Full compilation section archived; external versions linked |

Each experience folder records the witness, historical corpus anchor, full compilation extract, account versions, and source links. The four Zambrano folders also hold separately archived published English texts and account outlines. New tellings of an existing experience are added as accounts under the same experience ID. Scene, observation, and motif records are created as their source passages are indexed.

## Collection and processing

Collection is open to potential valid optasiological events (VOEs), including dreams, visions, near-death accounts, reports of resuscitation or resurrection, recorded prophecy, and other encounters. Collection includes locating sources, preserving permitted copies, identifying witnesses and account versions, and recording provenance. Collection requires no processing authorization.

**Processing requires the Atlas author's approval for a named scope.** Processing means close reading, scene segmentation, formal claim or phenomenon extraction, AIM assessment, motif mapping, cross-witness synthesis, or adding material to the analytical apparatus. Approval can cover one passage, account, experience, person, or another clearly stated selection. A collected transcript does not enter processing automatically.

| Processing authorization ID | Material and version(s) covered | Decision | Authorized operations | Author instruction / date |
|---|---|---|---|---|

The 16 corpus units above were processed previously. This tracker begins recording new processing authorizations as they occur.

## POE review and subsequent extraction

The root [POE register](../../poe_register.tsv) identifies reported experiences and records the author's decisions: `pending`, `valid`, or `unusable`. The collection retains source copies and versions separately. Accepted VOEs may be examined for reported phenomena, speech, conditions, and relationships, retaining source anchors and distinctions among witnesses and accounts.

The discovery register and historical extraction identifiers remain available for provenance. Their legacy assessment and approval fields describe the earlier research procedure; they do not supersede POE status or require a second admission decision.
