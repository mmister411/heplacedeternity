#!/usr/bin/env python3
"""Validate curated infernal phenomena against local testimony source lines.

The seed is intentionally human-curated. Keyword concordances are used only to
locate passages, never as independent evidence for a phenomenon.
"""

from collections import Counter, defaultdict
import argparse
import csv
import json
from pathlib import Path

from atlas_sift import SECTIONS, SOURCE

ROOT = Path(__file__).resolve().parent
SEED = ROOT / "atlas_phenomena_seed.tsv"
POE_REGISTER = ROOT.parent / "poe_register.tsv"
JSONL = ROOT / "Atlas_of_Perdition_Phenomena_Register.jsonl"
REPORT = ROOT / "Atlas_of_Perdition_Phenomena_Register.md"
MOTIF_SEED = ROOT / "atlas_motif_families.tsv"
CONCORDANCE = ROOT / "Atlas_of_Perdition_Cross_Witness_Concordance.md"

SOURCE_MAP = {sid: (name, first, last) for sid, name, first, last in SECTIONS}
HEADER = "source_id\tpoe_id\ttaxon\tlemma\tmode\tdescription\tanchor\tline_hint\tscripture\tcorrespondence"
TAXA = {
    "ENT": "Entrance and transition",
    "TOP": "Topography and structures",
    "ENV": "Atmosphere and perception",
    "BEI": "Beings and morphologies",
    "CUS": "Confinement and implements",
    "BOD": "Bodily composition and condition",
    "OPR": "Torment and recurring operations",
    "PSY": "Memory, consciousness and affect",
    "JUD": "Judicial pattern and attributed cause",
    "EPI": "Means of witnessing or knowing",
}
MODES = {
    "O": "reported observation",
    "F": "felt or sensory experience",
    "H": "heard speech or sound",
    "K": "knowledge claimed without ordinary perception",
    "S": "speech attributed to guide or encountered person",
    "I": "witness interpretation or retrospective conclusion",
}
CORRESPONDENCES = {
    "D": "direct biblical description or statement",
    "P": "biblical principle bearing on the feature",
    "A": "analogical imagery or limited relation",
    "E": "a testimony-specific extension beyond that passage",
    "": "no proposed biblical parallel",
}


def read_curated():
    with POE_REGISTER.open(encoding="utf-8", newline="") as handle:
        accepted_poes = {row["poe_id"] for row in csv.DictReader(handle, delimiter="\t")
                         if row["decision_status"] == "valid"}
    src_lines = SOURCE.read_text(encoding="utf-8-sig").splitlines()
    seed_lines = SEED.read_text(encoding="utf-8").splitlines()
    assert seed_lines[0] == HEADER
    items = []
    counters = Counter()
    missing = []
    for raw_index, text in enumerate(seed_lines[1:], 2):
        if not text.strip() or text.lstrip().startswith("#"):
            continue
        parts = text.split("\t")
        if len(parts) != 10:
            raise ValueError(f"Seed line {raw_index} has {len(parts)} fields, expected 10")
        sid, poe_id, taxon, lemma, mode, desc, anchor, hint, scripture, relation = [v.strip() for v in parts]
        if poe_id not in accepted_poes:
            raise ValueError(f"POE not accepted for seed line {raw_index}: {poe_id}")
        if sid not in SOURCE_MAP:
            raise ValueError(f"Unrecognized source at seed line {raw_index}: {sid}")
        if taxon not in TAXA or mode not in MODES or relation not in CORRESPONDENCES:
            raise ValueError(f"Unrecognized taxon/mode/relation at seed line {raw_index}")
        if not lemma or not desc or not anchor:
            raise ValueError(f"Missing required descriptive fields at seed line {raw_index}")
        name, first, last = SOURCE_MAP[sid]
        match_lines = [n for n in range(first, last + 1) if anchor.casefold() in src_lines[n - 1].casefold()]
        if not match_lines:
            missing.append((raw_index, sid, anchor))
            continue
        line = min(match_lines, key=lambda n: abs(n - int(hint))) if hint else match_lines[0]
        if hint and abs(line - int(hint)) > 12:
            raise ValueError(f"Hint too far from evidence at seed line {raw_index}: {hint} vs {line}")
        counters[sid] += 1
        items.append({
            "id": f"{sid}-{counters[sid]:03d}",
            "poe_id": poe_id,
            "source_id": sid,
            "source": name,
            "source_line": line,
            "category": taxon,
            "category_label": TAXA[taxon],
            "lemma": lemma,
            "evidence_mode": mode,
            "evidence_mode_label": MODES[mode],
            "reported_properties": desc,
            "biblical_cross_reference": scripture,
            "correspondence": relation,
            "correspondence_label": CORRESPONDENCES[relation],
            "manuscript_provenance": "user-supplied collected testimony; source line anchored in this compilation",
        })
    if missing:
        print("Unmatched anchors:")
        for row in missing:
            print("  ", row)
        raise SystemExit(2)
    return items


def read_motifs(items):
    by_id = {item["id"]: item for item in items}
    lines = MOTIF_SEED.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "division\tfamily\trecord_ids\tnote"
    motifs = []
    for line_number, raw in enumerate(lines[1:], 2):
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) != 4:
            raise ValueError(f"Motif row {line_number} needs four fields")
        division, family, id_text, note = parts
        ids = id_text.split()
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate ID within motif {family}")
        missing_ids = [rid for rid in ids if rid not in by_id]
        if missing_ids:
            raise ValueError(f"Unknown record IDs for motif {family}: {missing_ids}")
        source_ids = sorted({by_id[rid]["source_id"] for rid in ids})
        if len(source_ids) < 2:
            raise ValueError(f"Motif {family} has fewer than two testimony units")
        motifs.append({"division": division, "family": family, "ids": ids,
                       "source_ids": source_ids, "note": note})
    return motifs


def write_outputs(items, motifs, views=False):
    with JSONL.open("w", encoding="utf-8") as out:
        for item in items:
            out.write(json.dumps(item, ensure_ascii=False) + "\n")
    if not views:
        return

    per_source = defaultdict(list)
    per_lemma = defaultdict(lambda: defaultdict(list))
    per_taxon = Counter()
    for item in items:
        per_source[item["source_id"]].append(item)
        per_lemma[item["lemma"]][item["source_id"]].append(item["id"])
        per_taxon[item["category"]] += 1

    out = [
        "# Atlas of Perdition: Phenomena Register",
        "",
        "**Working edition:** 16 November 2026",
        f"**Curated entries:** {len(items)} across {len(per_source)} testimony units.",
        "",
        "Each entry records a distinguishable phenomenon or operation, the witness who reports it, its properties, and a verified line number in the supplied compilation. The record preserves the witness's account as testimony. It does not equate an observation, an interpretive explanation, and a statement attributed to a spiritual being.",
        "",
        "Source line numbers refer to `Pasted text(20261116-025409).txt` in the user's collection. The line is a passage locator, often containing a full paragraph. Accounts are preserved in the form supplied; an external publication record is not presumed.",
        "",
        "## Reading the register",
        "",
        "- **O:** reported observation; **F:** reported sensation; **H:** heard speech or sound; **K:** instantaneous or privileged knowledge; **S:** statement attributed to an encountered speaker; **I:** witness interpretation.",
        "- **D:** directly described in Scripture; **P:** related scriptural principle; **A:** analogous image; **E:** source detail extends beyond the cited passage. An empty reference means no biblical cross-reference was assigned, not that none exists.",
        "- An entry is one witnessed feature or narrated operation, not a count of independent confirmations. Separate entries can belong to one scene.",
        "",
        "## Taxonomic distribution",
        "",
        "| Division | Entries |",
        "|---|---:|",
    ]
    for taxon, label in TAXA.items():
        out.append(f"| {taxon}: {label} | {per_taxon[taxon]} |")
    out += ["", "## Source-specific observations", ""]
    source_order = [sid for sid, *_ in SECTIONS if sid in per_source]
    for sid in source_order:
        name, first, last = SOURCE_MAP[sid]
        out += [f"### {sid}: {name}", "", f"**Source span:** lines {first}–{last}.  **Records:** {len(per_source[sid])}.", "", "| Entry | Kind | Phenomenon and reported properties | Passage | Scripture |", "|---|---|---|---|---|"]
        for item in per_source[sid]:
            props = item["reported_properties"].replace("|", " / ")
            scripture = item["biblical_cross_reference"] + (f" ({item['correspondence']})" if item["biblical_cross_reference"] else "")
            out.append(f"| {item['id']} | {item['category']} / {item['evidence_mode']} | **{item['lemma']}**: {props} | {item['source_line']} | {scripture} |")
        out.append("")

    out += [
        "## Cross-witness comparison",
        "",
        f"**{len(motifs)} curated motif families** link specific register IDs across testimony units. These families group comparable phenomena without asserting that their physical details are identical. See the companion *Cross-Witness Concordance* for the complete membership table, boundaries, and divergences.",
        "",
        "## Remaining work",
        "",
        "The register now reflects a close reading of all 16 infernal testimony units. Extract length varies with the account: some are long first-person narratives, others short edited summaries. Further refinement can subdivide compound episodes and study each scriptural parallel in context. The JSONL companion preserves structured record identities for additions without replacing the witness's descriptions.",
        "",
    ]
    REPORT.write_text("\n".join(out), encoding="utf-8")

    cross = [
        "# Atlas of Perdition: Cross-Witness Concordance",
        "",
        f"**Working edition:** 16 November 2026. **{len(motifs)} motif families** linked to {len(items)} source-anchored entries in 16 testimony units from 13 named witnesses.",
        "",
        "## Method",
        "",
        "The phenomenon is the unit of comparison. An entry remains a witness's reported observation, sensation, heard utterance, claimed knowledge, quoted guide speech, or interpretation. A shared motif means similar reported properties, not proof of identical geography, independent origin, or doctrinal truth. The four Angelica Zambrano excursions are separate testimony units from one named witness.",
        "",
        "Source record IDs below resolve to exact line numbers and descriptive properties in the *Phenomena Register*. Counts are of testimony units, not of independent witnesses or historical confirmations. Every mapping is curated and traceable to at least two units.",
        "",
    ]
    current_division = None
    for m in motifs:
        if m["division"] != current_division:
            if current_division is not None:
                cross.append("")
            current_division = m["division"]
            cross += [f"## {current_division}", "", "| Shared motif | Units | Record IDs | Contours |", "|---|---:|---|---|"]
        cross.append(f"| **{m['family']}** | {len(m['source_ids'])} | {', '.join(m['ids'])} | {m['note']} |")
    cross += [
        "",
        "## Variations that must remain visible",
        "",
        "1. **Voices.** BRE-004, DAN-003, BAX-008, AZ2-002, FER-003 and KNI-006 report audible pleading or screams. PUR-008 explicitly reports an absence of human speech or groans, amid demonic laughter. This is a substantive difference in described soundscape.",
        "2. **Light and flame.** DAN-004 reports people appearing to burn without flames. Many others report visible fire, including BAX-014 and PUR-002. These must remain distinct scene-level observations.",
        "3. **Spatial layout.** BAX-022 uses a human-bodied map of Hell; MEL-015 describes circular, stacked cells; PUR-013 describes a grid of pits; APY-003 emphasizes a lake; WIE-021 claims a precise depth. No composite map should present these as a single measured configuration.",
        "4. **Body description.** DAN-004 and WIE-011 report flesh without blood; BAX-015/016 describe a skeletal form and gray interior mist; PUR-010 reports renewed flesh between episodes. The register treats these as different reported states.",
        "5. **Time.** PER-012 claims simultaneity of time and cautions against making doctrine from it; ALB-002 reports duration felt unlike earthly time; WIE-007 reports heightened knowledge of time; PUR-011/018 supply cycle estimates. The claims are preserved separately.",
        "6. **Specific repeated scene.** BRE-011 and BAX-025 both describe a woman in a rocking chair changing form. The scene is marked as a close narrative parallel. Its transmission history and independent provenance have not been established.",
        "7. **Age and judgment.** BRE-029 and AZ1-011 describe children among those suffering. The accounts also draw theological conclusions about accountability. The description and the doctrinal conclusion are distinct levels of claim.",
        "",
        "## Scriptural cross-reference discipline",
        "",
        "| Biblical text | Feature invoked in the collection | Relation and boundary |",
        "|---|---|---|",
        "| Luke 16:19–31 | Thirst, memory, torment, fixed chasm | The parable supplies these motifs; it does not specify cell measurements, demonic morphology, or unique modern persons. |",
        "| Isaiah 66:24; Mark 9:43–48 | Unquenched fire and worm | Direct imagery for persistent fire/worm; details such as measured worm size, resistance to flame and tissue regeneration extend beyond the verse. |",
        "| Revelation 20:12–15; 21:8 | Books of judgment, lake of fire, final judgment | Explicit canonical motifs; numbered cells and individual chest plates are testimony-specific additions. |",
        "| Revelation 13:16–18 | Mark/number of the beast | The text names the beast's number. It does not state that every infernal resident has 666 on the forehead. |",
        "| Matthew 7:13–14 | Broad and narrow ways | A moral road image; a literal road with signage is an analogy in these experiences. |",
        "| Jonah 2:6; Zechariah 9:11 | Bars of earth; waterless pit | Jonah speaks from watery confinement; Zechariah speaks of covenant prisoners sent out of a waterless pit. Neither directly describes a measured infernal jail cell. |",
        "| Job 18:14 | King of terrors | The phrase occurs in Bildad's speech about the wicked person's fate; identifying that title with the living God is a further interpretive move. |",
        "| Jude 1:13 | Blackness of darkness forever | Judgment image consonant with darkness reports, without specifying their sensory physics. |",
        "| James 2:1–4 | Partiality by social class | A direct ethical principle; assigning a specific individual to damnation is testimony-specific. |",
        "",
        "## Status of the evidence",
        "",
        "The compilation brings together first-person testimonies, extracts, collector notes and composite descriptions, some without a known publication record. The concordance preserves those sources as received and distinguishes what the witness reports seeing, hearing or undergoing from what a guide or resident says and what the narrator infers. Scriptural parallels are indexed according to their actual scope. No publication history or translation pedigree is presumed or required for the present phenomenological inventory.",
        "",
    ]
    CONCORDANCE.write_text("\n".join(cross), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--views", action="store_true", help="Also generate readable Markdown reports")
    args = parser.parse_args()
    data = read_curated()
    groupings = read_motifs(data)
    write_outputs(data, groupings, views=args.views)
    print(f"Validated {len(data)} individual entries in {len(set(x['source_id'] for x in data))} source units")
    print(f"Validated {len(groupings)} cross-witness motif families")
    print(f"Saved {JSONL.name}" + (f", {REPORT.name}, {CONCORDANCE.name}" if args.views else ""))
