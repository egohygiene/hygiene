"""Meaningful reference qualification; fixtures cannot authenticate editorial judgment."""
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
import helpful_content as content


class HelpfulContentTests(unittest.TestCase):
    def setUp(self):
        self.profile = content.load(content.PROFILE)
        self.good = content.load(ROOT / "fixtures/helpful-content/good.json")
        self.as_of = "2026-11-15T00:00:00Z"

    def result(self, value):
        return content.assess(value, self.profile, as_of=self.as_of, public_output=True)

    def rule(self, value, identity):
        return next(rule for rule in self.result(value)["rules"] if rule["rule_id"] == identity)

    def test_proposed_rules_map_actual_sources_and_automation_boundaries(self):
        content.validate_profile(self.profile)
        self.assertEqual("proposed", self.profile["status"])
        self.assertIsNone(self.profile["approval"])
        self.assertEqual(18, len(self.profile["rules"]))
        self.assertEqual({"mechanical", "human"}, {rule["verification"] for rule in self.profile["rules"]})
        self.assertEqual({"all", "current", "archived", "ai-assisted", "high-stakes", "localized"},
                         {rule["applicability"] for rule in self.profile["rules"]})
        sources = {source["id"] for source in self.profile["sources"]}
        for rule in self.profile["rules"]:
            self.assertTrue(set(rule["sources"]) <= sources)
            self.assertTrue(rule["remediation"])
        self.assertEqual("https://github.com/egohygiene/hygiene/issues/17", self.profile["related_policy"])

    def test_independently_expected_good_partial_stale_archive_fixtures(self):
        expected = content.load(ROOT / "fixtures/helpful-content/expectations.json")
        self.assertEqual(7, content.validate_fixtures(self.profile))
        for name, state in expected["cases"].items():
            with self.subTest(case=name):
                result = self.result(content.load(ROOT / f"fixtures/helpful-content/{name}.json"))
                self.assertEqual(state, result["metadata_state"])
                self.assertTrue(result["human_review_required"])
                self.assertEqual("not-supplied", result["publication_decision"])
                self.assertEqual("not-verified", result["source_truth"])
                self.assertFalse(any("score" in key for key in result))

    def test_high_stakes_and_unknown_applicability_do_not_inherit_ordinary_exemptions(self):
        self.assertEqual("not-applicable", self.rule(self.good, "HC-015")["applicability"])
        high = copy.deepcopy(self.good);high["subject"]["risk_profile"] = "high-stakes"
        self.assertEqual("missing", self.rule(high, "HC-015")["metadata_state"])
        self.assertEqual("independent-review-required", self.rule(high, "HC-016")["human_review"])
        unknown = copy.deepcopy(self.good);unknown["subject"]["risk_profile"] = "unknown"
        self.assertEqual("unknown", self.rule(unknown, "HC-015")["metadata_state"])

    def test_ai_provenance_and_reported_reviewer_never_supply_actual_review(self):
        ai = copy.deepcopy(self.good);ai["subject"]["ai_assisted"] = True
        self.assertEqual("missing", self.rule(ai, "HC-008")["metadata_state"])
        ai["evidence"]["ai_provenance"] = {"method": "Synthetic assisted outline", "reference": {
            "reference": "https://example.invalid/provenance", "visibility": "public"},
            "accountable_reviewer": "Synthetic responsible editorial role"}
        result = self.rule(ai, "HC-009")
        self.assertEqual("independent-review-required", result["human_review"])
        self.assertEqual("not-verified", result["review_authenticity"])
        ai["subject"]["ai_assisted"] = None
        self.assertEqual("unknown", self.rule(ai, "HC-008")["metadata_state"])

    def test_exact_content_review_binding_future_dates_and_freshness(self):
        for field, value, expected in (("content_revision", "c" * 64, "blocked"),
                                       ("reviewed_at", "2027-01-01T00:00:00Z", "blocked"),
                                       ("reviewed_at", "2025-01-01T00:00:00Z", "stale")):
            changed = copy.deepcopy(self.good);changed["evidence"]["content_review"][field] = value
            with self.subTest(field=field, value=value):
                self.assertEqual(expected, self.rule(changed, "HC-010")["metadata_state"])
        changed = copy.deepcopy(self.good);changed["evidence"]["source_refs"][0]["observed_at"] = "2027-01-01T00:00:00Z"
        self.assertEqual("blocked", self.rule(changed, "HC-006")["metadata_state"])
        changed = copy.deepcopy(self.good);changed["reviewer_claims"][0]["reviewed_at"] = "2020-01-01T00:00:00Z"
        claim = self.rule(changed, changed["reviewer_claims"][0]["rule_id"])
        self.assertEqual("stale-or-unbound-claim", claim["reported_judgment"])
        self.assertEqual("independent-review-required", claim["human_review"])

    def test_intentional_archive_has_own_gate_and_never_implies_current_freshness(self):
        archived = content.load(ROOT / "fixtures/helpful-content/archived.json")
        self.assertEqual("intentionally-archived", self.result(archived)["metadata_state"])
        self.assertEqual("not-applicable", self.rule(archived, "HC-010")["metadata_state"])
        archived["evidence"]["archive"] = None
        self.assertEqual("missing", self.rule(archived, "HC-012")["metadata_state"])
        self.assertEqual("partial", self.result(archived)["metadata_state"])
        self.assertEqual("not-supplied", self.result(archived)["publication_decision"])
        changed = copy.deepcopy(self.good);changed["evidence"]["last_updated"] = self.as_of
        with self.assertRaises(content.ContentError):self.result(changed)

    def test_correction_and_supersession_history_rejects_duplicates_and_cycles(self):
        changed = copy.deepcopy(self.good)
        event = {"id": "correction-one", "recorded_at": "2026-11-01T00:00:00Z", "reference": {
            "reference": "https://example.invalid/correction", "visibility": "public"}, "supersedes": []}
        changed["evidence"]["corrections"] = [event]
        self.assertEqual("present", self.rule(changed, "HC-011")["metadata_state"])
        changed["subject"]["lifecycle"] = "superseded"
        self.assertEqual("missing", self.rule(changed, "HC-011")["metadata_state"])
        changed["evidence"]["superseded_by"] = {"reference": "https://example.invalid/successor", "visibility": "public"}
        self.assertEqual("present", self.rule(changed, "HC-011")["metadata_state"])
        changed["evidence"]["corrections"].append(copy.deepcopy(event))
        with self.assertRaises(content.ContentError):self.result(changed)
        changed["evidence"]["corrections"] = [{**event, "supersedes": ["correction-one"]}]
        with self.assertRaises(content.ContentError):self.result(changed)

    def test_claimed_human_review_and_search_metrics_cannot_become_quality_pass(self):
        result = self.result(self.good)
        qualitative = [rule for rule in result["rules"] if rule["human_review"] == "independent-review-required"]
        self.assertTrue(qualitative)
        self.assertTrue(all(rule["review_authenticity"] == "not-verified" for rule in qualitative))
        for extra in ("human_approved", "helpfulness_score", "search_ranking"):
            changed = copy.deepcopy(self.good);changed[extra] = 100
            with self.subTest(extra=extra), self.assertRaises(content.ContentError):self.result(changed)
        changed = copy.deepcopy(self.good);changed["reviewer_claims"].append(copy.deepcopy(changed["reviewer_claims"][0]))
        with self.assertRaises(content.ContentError):self.result(changed)

    def test_public_output_refuses_private_evidence_and_unsafe_source_references(self):
        private = copy.deepcopy(self.good);private["visibility"] = "private"
        private["evidence"]["source_refs"][0]["visibility"] = "private"
        result = content.assess(private, self.profile, as_of=self.as_of)
        self.assertEqual("private", result["visibility"])
        with self.assertRaises(content.ContentError):self.result(private)
        private["visibility"] = "public"
        with self.assertRaises(content.ContentError):self.result(private)
        for unsafe in ("/private/synthetic", "../outside", "file:///synthetic", "https://:secret@example.invalid/source"):
            changed = copy.deepcopy(self.good);changed["evidence"]["source_refs"][0]["reference"] = unsafe
            with self.subTest(reference=unsafe), self.assertRaises(content.ContentError):self.result(changed)

    def test_policy_activation_and_duplicate_file_input_are_not_fabricated(self):
        for field, value in (("status", "active"), ("approval", True), ("contract_version", "9.0.0")):
            changed = copy.deepcopy(self.profile);changed[field] = value
            with self.subTest(field=field), self.assertRaises(content.ContentError):content.validate_profile(changed)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"private-fixture":"do-not-echo","private-fixture":"duplicate"}')
            result = subprocess.run([sys.executable, str(ROOT / "tools/helpful_content.py"), "assess",
                                     "--input", str(path), "--as-of", self.as_of],
                                    text=True, capture_output=True, timeout=5)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("do-not-echo", result.stdout + result.stderr)
            link = Path(directory) / "link.json";link.symlink_to(path)
            with self.assertRaises(OSError):content.load(link)


if __name__ == "__main__":
    unittest.main()
