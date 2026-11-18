"""Regression checks for the shared evidence layer; no real VOE is edited."""

import csv
from pathlib import Path
import tempfile
import unittest

import evidence


def write_tsv(path, fields, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source_root = self.root / "testimonies"
        source_root.mkdir()
        (source_root / "first.txt").write_text("A distinct reported scene", encoding="utf-8")
        (source_root / "second.txt").write_text("Another reported scene", encoding="utf-8")
        write_tsv(self.root / "poe_register.tsv",
                  ["poe_id", "legacy_id", "decision_status"],
                  [{"poe_id": "POE-000001", "legacy_id": "OLD-1", "decision_status": "valid"},
                   {"poe_id": "POE-000002", "legacy_id": "OLD-2", "decision_status": "valid"},
                   {"poe_id": "POE-000003", "legacy_id": "OLD-3", "decision_status": "pending"}])
        write_tsv(source_root / "source_copy_register.tsv",
                  ["artifact_id", "experience_id", "repository_copy"],
                  [{"artifact_id": "COPY-A", "experience_id": "OLD-1", "repository_copy": "first.txt"},
                   {"artifact_id": "COPY-B", "experience_id": "OLD-2", "repository_copy": "second.txt"},
                   {"artifact_id": "COPY-C", "experience_id": "OLD-3", "repository_copy": "second.txt"}])
        write_tsv(source_root / "source_manifest.tsv",
                  ["artifact_id", "experience_or_work_id", "repository_copy"], [])
        self.scene_a = {"type": "scene", "id": evidence.new_id("scene"),
                        "poe_id": "POE-000001", "source_id": "COPY-A", "anchor": "paragraph 2",
                        "description": "A witness enters a cell"}
        self.scene_b = {"type": "scene", "id": evidence.new_id("scene"),
                        "poe_id": "POE-000002", "source_id": "COPY-B", "anchor": "page 3",
                        "description": "Another witness encounters a creature"}
        self.obs_a = {"type": "observation", "id": evidence.new_id("observation"),
                      "scene_id": self.scene_a["id"], "aspect": "place", "mode": "seen",
                      "description": "A narrow cell with a barred door", "details": ["barred door"],
                      "assessment": "reported"}
        self.obs_b = {"type": "observation", "id": evidence.new_id("observation"),
                      "scene_id": self.scene_b["id"], "aspect": "creature", "mode": "seen",
                      "description": "An orange fox with purple teeth", "details": ["orange", "purple teeth"],
                      "assessment": "reported"}

    def test_distinct_scenes_and_particulars(self):
        relation = {"type": "relation", "id": evidence.new_id("relation"),
                    "subject": self.obs_a["id"], "object": self.obs_b["id"],
                    "predicate": "compared with", "basis": "Analyst records dissimilar subjects",
                    "assessment": "inferred"}
        records = [self.scene_a, self.scene_b, self.obs_a, self.obs_b, relation]
        self.assertEqual(len(evidence.validate(records, self.root)), 5)
        store = self.root / "apparatus" / "evidence.jsonl"
        for record in records:
            evidence.append(store, record, self.root)
        self.assertEqual(evidence.read_store(store), records)

    def test_cross_voe_comparison_cannot_be_reported_as_witness_fact(self):
        relation = {"type": "relation", "id": evidence.new_id("relation"),
                    "subject": self.obs_a["id"], "object": self.obs_b["id"],
                    "predicate": "same as", "basis": "No witness reports this identity",
                    "assessment": "reported"}
        with self.assertRaisesRegex(ValueError, "cross-VOE"):
            evidence.validate([self.scene_a, self.scene_b, self.obs_a, self.obs_b, relation], self.root)

    def test_pending_poe_cannot_enter_analysis(self):
        scene = dict(self.scene_a, poe_id="POE-000003", source_id="COPY-C")
        with self.assertRaisesRegex(ValueError, "author-accepted"):
            evidence.validate([scene], self.root)

    def test_unassigned_copy_cannot_be_cited_for_other_poe(self):
        scene = dict(self.scene_a, source_id="COPY-B")
        with self.assertRaisesRegex(ValueError, "not an acquired copy assigned"):
            evidence.validate([scene], self.root)

    def test_inferred_identification_needs_basis(self):
        inferred = dict(self.obs_a, assessment="inferred", description="Possibly Sheol")
        with self.assertRaisesRegex(ValueError, "basis"):
            evidence.validate([self.scene_a, inferred], self.root)
        inferred["basis"] = "The surroundings match the description; the witness gives no name"
        evidence.validate([self.scene_a, inferred], self.root)

    def test_observation_must_belong_to_scene(self):
        orphan = dict(self.obs_a, scene_id=evidence.new_id("scene"))
        with self.assertRaisesRegex(ValueError, "requires a scene"):
            evidence.validate([self.scene_a, orphan], self.root)


if __name__ == "__main__":
    unittest.main()
