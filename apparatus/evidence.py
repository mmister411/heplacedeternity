#!/usr/bin/env python3
"""Source-anchored, location-neutral scene and observation records.

This is a manual curation tool, not an automatic testimony extractor. The
author's POE decision is authoritative. Nothing here changes POE status,
source documents, or the inherited Perdition research.
"""

import argparse
import csv
import json
from pathlib import Path
import re
import sys
from uuid import uuid4


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORE = Path(__file__).resolve().parent / "evidence.jsonl"
MODES = ("seen", "heard", "felt", "attributed_speech", "claimed_knowledge", "interpreted")
ASSESSMENTS = ("reported", "inferred")
KINDS = {"scene": "SCN", "observation": "OBS", "relation": "REL"}
ID_RE = re.compile(r"(SCN|OBS|REL)-[0-9a-f]{32}\Z")


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def poe_index(root):
    records = rows(root / "poe_register.tsv")
    return {record["poe_id"]: record for record in records}


def source_index(root, poes):
    """Index acquired local sources and the POEs they may support."""
    aliases = {poe_id: poe_id for poe_id in poes}
    aliases.update({r["legacy_id"]: p for p, r in poes.items() if r["legacy_id"]})
    found = {}
    paths = {}
    inputs = (
        (root / "testimonies" / "source_copy_register.tsv", "experience_id"),
        (root / "testimonies" / "source_manifest.tsv", "experience_or_work_id"),
    )
    for path, assignment_field in inputs:
        for record in rows(path):
            artifact = record["artifact_id"]
            relative = record["repository_copy"].strip()
            if not relative:
                continue  # Discovered links are not acquired testimony documents.
            candidate = Path(relative)
            if candidate.is_absolute() or ".." in candidate.parts:
                continue
            local = (root / "testimonies" / candidate).resolve()
            if not local.is_relative_to((root / "testimonies").resolve()) or not local.is_file():
                continue
            owners = {aliases[alias] for alias in record[assignment_field].split("|") if alias in aliases}
            if artifact in found:
                # The manifest also indexes source copies already in the copy register.
                if paths[artifact] != local or found[artifact] != owners:
                    raise ValueError(f"Conflicting source artifact ID: {artifact}")
                continue
            paths[artifact] = local
            found[artifact] = owners
    return found


def read_store(path):
    if not path.exists():
        return []
    records = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as error:
                    raise ValueError(f"{path}:{number}: {error.msg}") from error
    return records


def require_text(record, *fields):
    for field in fields:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"{record.get('id', '?')}: {field} must contain text")


def validate(records, root):
    poes = poe_index(root)
    sources = source_index(root, poes)
    by_id = {}
    owners = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each JSONL record must be an object")
        kind, record_id = record.get("type"), record.get("id")
        if kind not in KINDS or not isinstance(record_id, str) or not ID_RE.fullmatch(record_id):
            raise ValueError(f"Unknown record kind or malformed ID: {record_id}")
        if not record_id.startswith(KINDS[kind] + "-") or record_id in by_id:
            raise ValueError(f"Duplicate or mismatched ID: {record_id}")
        by_id[record_id] = record

    # Two passes permit references to records that occur later in the file.
    for record in records:
        kind, record_id = record["type"], record["id"]
        if kind == "scene":
            require_text(record, "poe_id", "source_id", "anchor", "description")
            poe = record["poe_id"]
            if poe not in poes or poes[poe]["decision_status"] != "valid":
                raise ValueError(f"{record_id}: only author-accepted VOEs may be analyzed ({poe})")
            if poe not in sources.get(record["source_id"], set()):
                raise ValueError(f"{record_id}: source is not an acquired copy assigned to {poe}")
            owners[record_id] = poe

    for record in records:
        kind, record_id = record["type"], record["id"]
        if kind == "observation":
            require_text(record, "scene_id", "aspect", "description", "mode", "assessment")
            scene = by_id.get(record["scene_id"])
            if not scene or scene["type"] != "scene":
                raise ValueError(f"{record_id}: observation requires a scene")
            if record["mode"] not in MODES or record["assessment"] not in ASSESSMENTS:
                raise ValueError(f"{record_id}: unknown mode or assessment")
            details = record.get("details", [])
            if not isinstance(details, list) or any(not isinstance(d, str) or not d.strip() for d in details):
                raise ValueError(f"{record_id}: details must be a list of descriptive strings")
            if record["assessment"] == "inferred":
                require_text(record, "basis")
            owners[record_id] = owners[scene["id"]]

    for record in records:
        if record["type"] != "relation":
            continue
        record_id = record["id"]
        require_text(record, "subject", "object", "predicate", "basis", "assessment")
        subject, obj = record["subject"], record["object"]
        if subject not in owners or obj not in owners or subject == obj:
            raise ValueError(f"{record_id}: relation must connect distinct scenes or observations")
        if record["assessment"] not in ASSESSMENTS:
            raise ValueError(f"{record_id}: unknown assessment")
        if owners[subject] != owners[obj] and record["assessment"] != "inferred":
            raise ValueError(f"{record_id}: cross-VOE comparisons are analytical inferences")
    return by_id


def append(store, record, root):
    existing = read_store(store)
    validate(existing + [record], root)
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record["id"]


def new_id(kind):
    return f"{KINDS[kind]}-{uuid4().hex}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE, help="JSONL evidence store")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Validate evidence and author-review/source links")
    listing = commands.add_parser("list", help="Show records, optionally for a POE")
    listing.add_argument("--poe", help="Filter scenes, observations, and relations by POE")
    scene = commands.add_parser("scene", help="Record a coherent scene in an accepted VOE")
    scene.add_argument("--poe", required=True)
    scene.add_argument("--source", required=True, help="Acquired source artifact ID")
    scene.add_argument("--anchor", required=True, help="Passage, page, or time locator")
    scene.add_argument("--description", required=True)
    observation = commands.add_parser("observe", help="Record a particular within a scene")
    observation.add_argument("--scene", required=True)
    observation.add_argument("--aspect", required=True, help="Free text, e.g. place, being, speech")
    observation.add_argument("--description", required=True)
    observation.add_argument("--mode", choices=MODES, required=True)
    observation.add_argument("--assessment", choices=ASSESSMENTS, default="reported")
    observation.add_argument("--basis", help="Required for analyst inference")
    observation.add_argument("--detail", action="append", default=[], help="Preserve a particular property; repeatable")
    observation.add_argument("--anchor", help="Narrower location in the scene's source")
    relation = commands.add_parser("relate", help="Link two particulars without merging them")
    relation.add_argument("--subject", required=True)
    relation.add_argument("--predicate", required=True)
    relation.add_argument("--object", required=True)
    relation.add_argument("--basis", required=True)
    relation.add_argument("--assessment", choices=ASSESSMENTS, default="inferred")
    args = parser.parse_args(argv)

    try:
        if args.command in {"check", "list"}:
            records = read_store(args.store)
            by_id = validate(records, ROOT)
            if args.command == "check":
                print(f"Valid evidence: {len(records)} records")
            else:
                scenes = {r["id"]: r["poe_id"] for r in records if r["type"] == "scene"}
                for record in records:
                    if args.poe:
                        if record["type"] == "scene":
                            related = {record["poe_id"]}
                        elif record["type"] == "observation":
                            related = {scenes[record["scene_id"]]}
                        else:
                            related = {scenes[by_id[i]["scene_id"]] if by_id[i]["type"] == "observation"
                                       else scenes[i] for i in (record["subject"], record["object"])}
                        if args.poe not in related:
                            continue
                    print(json.dumps(record, ensure_ascii=False))
            return 0
        if args.command == "scene":
            record = {"type": "scene", "id": new_id("scene"), "poe_id": args.poe,
                      "source_id": args.source, "anchor": args.anchor, "description": args.description}
        elif args.command == "observe":
            record = {"type": "observation", "id": new_id("observation"),
                      "scene_id": args.scene, "aspect": args.aspect, "description": args.description,
                      "mode": args.mode, "assessment": args.assessment, "details": args.detail}
            if args.basis:
                record["basis"] = args.basis
            if args.anchor:
                record["anchor"] = args.anchor
        else:
            record = {"type": "relation", "id": new_id("relation"),
                      "subject": args.subject, "predicate": args.predicate, "object": args.object,
                      "basis": args.basis, "assessment": args.assessment}
        print(append(args.store, record, ROOT))
        return 0
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
