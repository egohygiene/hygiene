from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import organization_roadmap as roadmap


class OrganizationRoadmapTests(unittest.TestCase):
    def setUp(self):
        self.source = roadmap.load(roadmap.DEFAULT)
        self.fixture = roadmap.load(ROOT / "fixtures/organization-roadmap/composition.valid.json")

    def test_canonical_proposal_and_cross_repository_synthetic_fixture(self):
        roadmap.validate(self.source)
        roadmap.validate(self.fixture)
        self.assertEqual(5, len(self.source["initiatives"]))
        self.assertTrue(all(row["assertion"] == "inferred" and row["review"] is None
                            for row in self.source["initiatives"]))
        states = {row["state"] for row in self.fixture["initiatives"]}
        self.assertTrue({"active", "blocked", "optional", "paused"} <= states)
        self.assertIn("stale", {row["freshness"] for row in self.fixture["initiatives"]})

    def test_compose_shared_nodes_and_independent_work_without_copying_prose(self):
        first, second = self.source["initiatives"][:2]
        second["repository_nodes"].append(copy.deepcopy(first["repository_nodes"][0]))
        roadmap.validate(self.source)
        independent = self.source["initiatives"][-1]
        self.assertEqual([], independent["depends_on"])
        self.assertEqual([], independent["repository_nodes"])
        for row in self.source["initiatives"]:
            for node in row["repository_nodes"]:
                self.assertNotIn("outcome", node)

    def test_dependency_cycles_missing_references_and_duplicate_identity_fail(self):
        for mutation in ("cycle", "dangling", "duplicate", "self"):
            candidate = copy.deepcopy(self.source)
            if mutation == "cycle": candidate["initiatives"][0]["depends_on"] = ["ORG-I002"]
            elif mutation == "dangling": candidate["initiatives"][0]["depends_on"] = ["ORG-I999"]
            elif mutation == "self": candidate["initiatives"][0]["depends_on"] = ["ORG-I001"]
            else: candidate["initiatives"].append(copy.deepcopy(candidate["initiatives"][0]))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): roadmap.validate(candidate)

    def test_inferred_placement_cannot_become_authoritative_without_review(self):
        row = self.source["initiatives"][0]
        row["assertion"] = "authoritative"
        with self.assertRaises(ValueError): roadmap.validate(self.source)
        row["review"] = "source:roadmap-contract"
        with self.assertRaises(ValueError): roadmap.validate(self.source)

    def test_declared_review_completion_and_renewed_review_are_distinct(self):
        row = self.source["initiatives"][0]
        review = copy.deepcopy(self.source["sources"][0])
        review.update(id="source:synthetic-review", kind="manual", repository="egohygiene/hygiene",
                      revision=None, url="https://github.com/egohygiene/hygiene/issues/60#issuecomment-1")
        self.source["sources"].append(review)
        row.update(assertion="authoritative", review=review["id"])
        row["provenance"].append(review["id"])
        roadmap.validate(self.source)  # Structural declaration, not live authentication.
        changed = copy.deepcopy(self.source)
        changed["initiatives"][0]["horizon"] = "later"
        with self.assertRaises(ValueError): roadmap.validate_transition(self.source, changed)
        row["state"] = "completed"
        with self.assertRaises(ValueError): roadmap.validate(self.source)
        evidence = copy.deepcopy(review)
        evidence.update(id="source:synthetic-check", kind="check_provider",
                        url="https://github.com/egohygiene/hygiene/actions/runs/1")
        self.source["sources"].append(evidence)
        row["links"].append(dict(type="evidences", source=evidence["id"]))
        roadmap.validate(self.source)
        self.source["visibility"] = "private"
        evidence["visibility"] = "private"
        with self.assertRaises(ValueError): roadmap.validate(self.source)

    def test_supersession_keeps_ids_and_requires_reciprocal_lineage(self):
        old = copy.deepcopy(self.source)
        self.source["initiatives"][0].update(state="superseded", superseded_by=["ORG-I002"])
        with self.assertRaises(ValueError): roadmap.validate(self.source)
        self.source["initiatives"][1]["supersedes"] = ["ORG-I001"]
        roadmap.validate_transition(old, self.source)
        self.source["initiatives"].pop()
        with self.assertRaises(ValueError): roadmap.validate_transition(old, self.source)

    def test_unknown_stale_optional_and_archive_state_do_not_auto_promote(self):
        for state in roadmap.STATES - {"superseded"}:
            self.source["initiatives"][0].update(state=state, freshness="stale")
            roadmap.validate(self.source)
            projected = roadmap.public_projection(self.source)["initiatives"][0]
            self.assertEqual((state, "stale"), (projected["state"], projected["freshness"]))
        for applicability in ("archived", "not_applicable"):
            self.source["initiatives"][0]["repository_nodes"][0]["applicability"] = applicability
            roadmap.validate(self.source)

    def test_public_projection_removes_private_participation_and_dependency_closure(self):
        projected = roadmap.public_projection(self.fixture)
        roadmap.validate(projected)
        serialized = roadmap.encoded(projected)
        for private in ("synthetic-protected", "SYNTHETIC-PROTECTED", "ORG-I900", "PRIVATE-Q01", "ORG-I004"):
            self.assertNotIn(private, serialized)
        self.assertNotIn('"count"', serialized)
        self.assertEqual([], projected["events"])
        self.assertEqual("active", projected["initiatives"][0]["state"])
        self.assertEqual("stale", projected["initiatives"][2]["freshness"])
        self.assertEqual(projected, roadmap.public_projection(projected))

    def test_public_provenance_cannot_claim_restricted_source(self):
        self.fixture["initiatives"][0]["provenance"].append("source:synthetic-protected")
        with self.assertRaises(ValueError): roadmap.validate(self.fixture)

    def test_completely_restricted_view_is_empty_without_topology_placeholders(self):
        candidate = copy.deepcopy(self.source)
        candidate["visibility"] = "private"
        for row in candidate["initiatives"]:
            row["visibility"] = "private"
        projected = roadmap.public_projection(candidate)
        roadmap.validate(projected)
        self.assertEqual([], projected["initiatives"])
        self.assertEqual([], projected["sources"])
        self.assertEqual([], projected["events"])

    def test_events_preserve_clocks_and_do_not_create_authoritative_history(self):
        event = self.fixture["events"][0]
        event["recorded_at"] = "2026-01-01T00:00:00Z"
        with self.assertRaises(ValueError): roadmap.validate(self.fixture)
        event["recorded_at"] = self.fixture["updated_at"]
        event["assertion"] = "authoritative"
        with self.assertRaises(ValueError): roadmap.validate(self.fixture)

    def test_cli_and_ambiguous_input_fail_without_echoing_private_details(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text('{"schema":"PRIVATE-SENTINEL","schema":"duplicate"}')
            result = subprocess.run([sys.executable, str(ROOT / "tools/organization_roadmap.py"),
                                     "validate", "--input", str(path)], text=True, capture_output=True, check=False)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("PRIVATE-SENTINEL", result.stdout + result.stderr)
            path.write_text(roadmap.encoded(self.fixture))
            result = subprocess.run([sys.executable, str(ROOT / "tools/organization_roadmap.py"),
                                     "public", "--input", str(path)], text=True, capture_output=True, check=False)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn("synthetic-protected", result.stdout)

    def test_generated_view_and_registered_proposal_are_current(self):
        self.assertEqual((ROOT / "organization/ROADMAP.md").read_text(), roadmap.render(self.source))
        catalog = json.loads((ROOT / "catalog/contracts.yaml").read_text())
        contract = next(row for row in catalog["contracts"] if row["id"] == roadmap.SCHEMA)
        self.assertEqual("proposed", contract["status"])
        schema = json.loads((ROOT / contract["source"]).read_text())
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
        self.assertEqual("repository-intelligence.alpha2.schema.json#/$defs/source",
                         schema["properties"]["sources"]["items"]["$ref"])


if __name__ == "__main__":
    unittest.main()
