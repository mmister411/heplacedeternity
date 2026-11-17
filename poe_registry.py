#!/usr/bin/env python3
"""Review POE status and select accepted experiences for analysis.

Run from any working directory. The source intake and existing research files
remain unchanged. Decisions live only in poe_register.tsv.
"""

import argparse
import csv
from datetime import date
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
REGISTER = ROOT / "poe_register.tsv"
STATUSES = {"pending", "valid", "unusable"}
ID_PATTERN = re.compile(r"POE-([0-9]{6})$")
FIELDS = ["poe_id", "legacy_id", "witness", "title", "summary", "record_kind", "decision_status", "decision_date", "decision_note"]


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
        if not row["witness"].strip() or not row["title"].strip():
            raise ValueError(f"Witness and title are required for {row['poe_id']}")
    return fields, rows


def show(rows):
    for row in rows:
        print(f"{row['poe_id']}\t{row['decision_status']}\t{row['witness']}\t{row['title']}")


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
    change = commands.add_parser("set", help="Record an explicit human decision")
    change.add_argument("poe_id")
    change.add_argument("status", choices=sorted(STATUSES))
    change.add_argument("--note", default="")
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
        })
        save(fields, rows)
        print(f"Registered {new_id}: pending")
    elif args.command == "set":
        match = next((r for r in rows if args.poe_id in {r["poe_id"], r["legacy_id"]}), None)
        if match is None:
            parser.error(f"Unknown POE ID: {args.poe_id}")
        match["decision_status"] = args.status
        match["decision_date"] = date.today().isoformat()
        match["decision_note"] = args.note
        save(fields, rows)
        print(f"{match['poe_id']}: {args.status}")


if __name__ == "__main__":
    main()
