#!/usr/bin/env python3
"""Review POE status and select accepted experiences for analysis.

Run from any working directory. The source intake and existing research files
remain unchanged. Decisions live only in poe_register.tsv.
"""

import argparse
import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REGISTER = ROOT / "poe_register.tsv"
STATUSES = {"pending", "valid", "unusable"}


def load():
    with REGISTER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fields = reader.fieldnames
        rows = list(reader)
    if not fields or not {"poe_id", "decision_status", "decision_date", "decision_note"}.issubset(fields):
        raise ValueError("POE register has missing required columns")
    ids = [r["poe_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("POE register contains duplicate IDs")
    for row in rows:
        if row["decision_status"] not in STATUSES:
            raise ValueError(f"Invalid decision status for {row['poe_id']}")
    return fields, rows


def show(rows):
    for row in rows:
        print(f"{row['poe_id']}\t{row['decision_status']}\t{row['witness']}\t{row['record_kind']}")


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
    commands.add_parser("check", help="Validate the register")
    args = parser.parse_args()
    fields, rows = load()
    if args.command == "check":
        print(f"Valid register: {len(rows)} records")
    elif args.command == "list":
        show([r for r in rows if not args.status or r["decision_status"] == args.status])
    elif args.command == "eligible":
        show([r for r in rows if r["decision_status"] == "valid"])
    else:
        match = next((r for r in rows if r["poe_id"] == args.poe_id), None)
        if match is None:
            parser.error(f"Unknown POE ID: {args.poe_id}")
        match["decision_status"] = args.status
        match["decision_date"] = date.today().isoformat()
        match["decision_note"] = args.note
        with REGISTER.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print(f"{args.poe_id}: {args.status}")


if __name__ == "__main__":
    main()
