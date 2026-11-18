#!/usr/bin/env python3
"""Review POE status and select accepted experiences for analysis.

Run from any working directory. The source intake and existing research files
remain unchanged. Decisions live only in poe_register.tsv.

Location flags concern the reported experience, not its files. "reported" means
a location is explicitly identified in a witnessed scene; "inferred" means its
identity follows from the described setting; "possible" marks a weaker clue.
"not_reported" means no sufficient indication in the reviewed source;
"unassessed" means the location has not been evaluated. Keep a short basis for
inferred or possible identifications. Locations may overlap or nest.
"""

import argparse
import csv
from datetime import date
import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
REGISTER = ROOT / "poe_register.tsv"
SOURCE_COPY_REGISTER = ROOT / "atlasofperdition" / "testimonies" / "source_copy_register.tsv"
TESTIMONY_ROOT = SOURCE_COPY_REGISTER.parent
SOURCE_MANIFEST = TESTIMONY_ROOT / "source_manifest.tsv"
STATUSES = {"pending", "valid", "unusable"}
FEATURES = (
    "heaven", "hell", "lake_of_fire", "celestial_city", "new_jerusalem",
    "new_earth", "outer_darkness", "sheol", "paradise",
)
# These states describe location evidence, independent of the human POE decision.
FEATURE_STATES = {"unassessed", "reported", "inferred", "possible", "not_reported"}
ID_PATTERN = re.compile(r"POE-([0-9]{6})$")
FIELDS = [
    "poe_id", "legacy_id", "witness", "title", "summary", "record_kind",
    *FEATURES, "location_basis", "decision_status", "decision_date", "decision_note",
]


def load():
    with REGISTER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fields = reader.fieldnames
        rows = list(reader)
    if fields != FIELDS:
        raise ValueError("POE register columns do not match the expected schema")
    ids = [r["poe_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("POE register contains duplicate IDs")
    if any(not ID_PATTERN.fullmatch(value) for value in ids):
        raise ValueError("POE IDs must have the form POE-000001")
    legacy = [r["legacy_id"] for r in rows if r["legacy_id"]]
    if len(legacy) != len(set(legacy)):
        raise ValueError("POE register contains duplicate legacy IDs")
    for row in rows:
        if row["decision_status"] not in STATUSES:
            raise ValueError(f"Invalid decision status for {row['poe_id']}")
        for feature in FEATURES:
            if row[feature] not in FEATURE_STATES:
                raise ValueError(f"Invalid {feature} value for {row['poe_id']}")
        if not row["witness"].strip() or not row["title"].strip():
            raise ValueError(f"Witness and title are required for {row['poe_id']}")
    return fields, rows


def show(rows):
    for row in rows:
        locations = ",".join(
            f"{f}:{row[f]}" for f in FEATURES if row[f] in {"reported", "inferred", "possible"}
        ) or "-"
        print(f"{row['poe_id']}\t{row['decision_status']}\t{row['witness']}\t{row['title']}\t{locations}")


def verified_copy(artifact, relative_name, expected_sha, errors, expected_bytes=None):
    relative = Path(relative_name)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        errors.append(f"Unsafe source path: {artifact}")
        return False
    path = TESTIMONY_ROOT / relative
    if not path.resolve().is_relative_to(TESTIMONY_ROOT.resolve()):
        errors.append(f"Source path leaves testimony collection: {artifact}")
        return False
    if not path.is_file():
        errors.append(f"Missing source file: {artifact}")
        return False
    data = path.read_bytes()
    if (expected_bytes is not None and str(len(data)) != expected_bytes) or hashlib.sha256(data).hexdigest() != expected_sha:
        errors.append(f"Source size or checksum mismatch: {artifact}")
        return False
    return True


def audit_intake(rows):
    """Audit acquired documents; source extent and human review remain separate."""
    by_id = {r["poe_id"]: r["poe_id"] for r in rows}
    by_id.update({r["legacy_id"]: r["poe_id"] for r in rows if r["legacy_id"]})
    copies = {r["poe_id"]: [] for r in rows}
    compilations = {r["poe_id"]: [] for r in rows}
    errors = []
    with SOURCE_COPY_REGISTER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        required = {"artifact_id", "experience_id", "repository_copy", "bytes", "sha256"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Source-copy register lacks required columns")
        seen_artifacts = set()
        for source in reader:
            artifact = source["artifact_id"]
            if artifact in seen_artifacts:
                errors.append(f"Duplicate source artifact: {artifact}")
            seen_artifacts.add(artifact)
            if not verified_copy(artifact, source["repository_copy"], source["sha256"], errors, source["bytes"]):
                continue
            for experience_id in source["experience_id"].split("|"):
                poe_id = by_id.get(experience_id)
                if poe_id is None:
                    errors.append(f"Unmatched source experience: {artifact} / {experience_id}")
                else:
                    copies[poe_id].append(artifact)

    # The collector's original intake compilation is a testimony document too.
    # Its distinct excerpts are indexed in the source manifest, not the copy register.
    with SOURCE_MANIFEST.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        required = {"artifact_id", "experience_or_work_id", "repository_copy", "collection_state", "source_note"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Source manifest lacks required columns")
        for source in reader:
            if source["collection_state"] != "compilation_extract":
                continue
            artifact = source["artifact_id"]
            match = re.search(r"sha256=([0-9a-f]{64})", source["source_note"])
            if not match:
                errors.append(f"Missing compilation checksum: {artifact}")
                continue
            if not verified_copy(artifact, source["repository_copy"], match.group(1), errors):
                continue
            if "editorial-" in Path(source["repository_copy"]).name:
                continue
            for experience_id in source["experience_or_work_id"].split("|"):
                poe_id = by_id.get(experience_id)
                if poe_id:
                    compilations[poe_id].append(artifact)

    print("poe_id\tintake_evidence\tsource_copies\tcompilation_units\twitness")
    for row in rows:
        found = copies[row["poe_id"]]
        compiled = compilations[row["poe_id"]]
        status = "source_copy_acquired" if found else "compilation_only" if compiled else "incomplete_no_document"
        print(f"{row['poe_id']}\t{status}\t{len(found)}\t{len(compiled)}\t{row['witness']}")
    with_copies = sum(bool(found) for found in copies.values())
    compiled_only = sum(not copies[key] and bool(compilations[key]) for key in copies)
    missing = len(rows) - with_copies - compiled_only
    print(f"Intake: {with_copies} source-copy, {compiled_only} compilation-only, {missing} without documents; {len(errors)} source errors")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        raise ValueError("Source-copy intake audit failed")


def save(fields, rows):
    with REGISTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="List POEs, optionally by status")
    listing.add_argument("--status", choices=sorted(STATUSES))
    commands.add_parser("eligible", help="List valid VOEs eligible for analysis")
    commands.add_parser("intake", help="Audit acquired testimony copies per POE")
    change = commands.add_parser("set", help="Record an explicit human decision")
    change.add_argument("poe_id")
    change.add_argument("status", choices=sorted(STATUSES))
    change.add_argument("--note", default="")
    mark = commands.add_parser("set-feature", help="Record a top-level location assessment")
    mark.add_argument("poe_id")
    mark.add_argument("feature", choices=FEATURES)
    mark.add_argument("state", choices=sorted(FEATURE_STATES))
    create = commands.add_parser("add", help="Register a new prospective experience")
    create.add_argument("--witness", required=True)
    create.add_argument("--title", required=True)
    create.add_argument("--summary", default="")
    create.add_argument("--kind", choices=["experience", "source_work"], default="experience")
    commands.add_parser("check", help="Validate the register")
    args = parser.parse_args()
    fields, rows = load()
    if args.command == "check":
        print(f"Valid register: {len(rows)} records")
    elif args.command == "list":
        show([r for r in rows if not args.status or r["decision_status"] == args.status])
    elif args.command == "eligible":
        show([r for r in rows if r["decision_status"] == "valid"])
    elif args.command == "intake":
        audit_intake(rows)
    elif args.command == "add":
        if not args.witness.strip() or not args.title.strip():
            parser.error("Witness and title cannot be empty")
        next_number = max((int(ID_PATTERN.fullmatch(r["poe_id"]).group(1)) for r in rows), default=0) + 1
        if next_number > 999999:
            parser.error("POE ID range exhausted")
        new_id = f"POE-{next_number:06d}"
        rows.append(dict.fromkeys(FIELDS, "") | {
            "poe_id": new_id, "witness": args.witness.strip(), "title": args.title.strip(),
            "summary": args.summary, "record_kind": args.kind, "decision_status": "pending",
            **{feature: "unassessed" for feature in FEATURES},
        })
        save(fields, rows)
        print(f"Registered {new_id}: pending")
    elif args.command in {"set", "set-feature"}:
        match = next((r for r in rows if args.poe_id in {r["poe_id"], r["legacy_id"]}), None)
        if match is None:
            parser.error(f"Unknown POE ID: {args.poe_id}")
        if args.command == "set-feature":
            match[args.feature] = args.state
            save(fields, rows)
            print(f"{match['poe_id']} {args.feature}: {args.state}")
        else:
            match["decision_status"] = args.status
            match["decision_date"] = date.today().isoformat()
            match["decision_note"] = args.note
            save(fields, rows)
            print(f"{match['poe_id']}: {args.status}")


if __name__ == "__main__":
    main()
