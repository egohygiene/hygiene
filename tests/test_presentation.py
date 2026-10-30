from __future__ import annotations

import copy
import json
import itertools
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import presentation  # noqa: E402


class RepositoryPresentationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = presentation.load_json(
            ROOT / "catalog" / "repository-presentation-profile.json"
        )
        cls.minimal = presentation.load_json(
            ROOT / "fixtures" / "repository-presentation" / "minimal.valid.json"
        )
        cls.rich = presentation.load_json(
            ROOT / "fixtures" / "repository-presentation" / "rich.valid.json"
        )

    def test_contract_schemas_are_json_schema_documents(self) -> None:
        for name in (
            "repository-presentation-profile.v1.schema.json",
            "repository-presentation-evidence.v1.schema.json",
        ):
            schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
            self.assertEqual(
                "https://json-schema.org/draft/2020-12/schema", schema["$schema"]
            )
            self.assertTrue(schema["$id"].startswith("https://egohygiene.io/"))

    def test_checked_in_profile_is_valid(self) -> None:
        self.assertEqual([], presentation.validate_profile(self.profile))
        self.assertEqual(
            presentation.EXPECTED_SLOT_IDS,
            {slot["id"] for slot in self.profile["slots"]},
        )

    def test_contracts_are_registered_as_proposals(self) -> None:
        contract_index = presentation.load_json(ROOT / "catalog" / "contracts.yaml")
        contracts = {item["id"]: item for item in contract_index["contracts"]}
        for contract_id in (presentation.PROFILE_SCHEMA, presentation.EVIDENCE_SCHEMA):
            self.assertEqual("proposed", contracts[contract_id]["status"])
            self.assertEqual("egohygiene/hygiene", contracts[contract_id]["owner"])

    def test_minimal_and_rich_fixtures_are_valid(self) -> None:
        for fixture in (self.minimal, self.rich):
            self.assertEqual(
                [], presentation.validate_evidence(fixture, self.profile)
            )

    def test_variant_resolution_uses_documented_precedence(self) -> None:
        resolved = presentation.resolve_requirements(
            self.profile, "publication", "private", "archived"
        )
        self.assertEqual("optional", resolved["identity_banner"])
        self.assertEqual("optional", resolved["license"])
        self.assertEqual("not_applicable", resolved["installation"])
        self.assertEqual("not_applicable", resolved["development"])

    def test_required_unknown_state_cannot_render_as_passing(self) -> None:
        candidate = copy.deepcopy(self.rich)
        purpose = next(slot for slot in candidate["slots"] if slot["id"] == "purpose")
        purpose["state"] = "unknown"
        purpose["evidence"] = []
        errors = presentation.validate_evidence(candidate, self.profile)
        self.assertIn("evidence.assessment.state must equal derived state partial", errors)
        self.assertIn("evidence.badge.state must equal derived state partial", errors)

    def test_stale_required_evidence_cannot_render_as_passing(self) -> None:
        candidate = copy.deepcopy(self.rich)
        banner = next(
            slot for slot in candidate["slots"] if slot["id"] == "identity_banner"
        )
        banner["state"] = "stale"
        errors = presentation.validate_evidence(candidate, self.profile)
        self.assertIn("evidence.badge.state must equal derived state stale", errors)

    def test_unsupported_compliance_claim_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.rich)
        candidate["badge"]["message"] = "fully compliant"
        errors = presentation.validate_evidence(candidate, self.profile)
        self.assertIn(
            "evidence.badge.message contains a prohibited claim term", errors
        )

    def test_badge_uses_the_profile_state_message(self) -> None:
        candidate = copy.deepcopy(self.rich)
        candidate["badge"]["message"] = "looks good"
        errors = presentation.validate_evidence(candidate, self.profile)
        self.assertIn(
            "evidence.badge.message must match the profile state message", errors
        )

    def test_not_applicable_requires_profile_resolution_and_reason(self) -> None:
        candidate = copy.deepcopy(self.rich)
        installation = next(
            slot for slot in candidate["slots"] if slot["id"] == "installation"
        )
        installation["state"] = "not_applicable"
        installation["reason"] = None
        errors = presentation.validate_evidence(candidate, self.profile)
        index = candidate["slots"].index(installation)
        self.assertIn(
            f"evidence.slots[{index}].state cannot be not_applicable", errors
        )

    def test_exemption_requires_approval_evidence(self) -> None:
        candidate = copy.deepcopy(self.rich)
        generated = next(
            slot for slot in candidate["slots"] if slot["id"] == "generated_ownership"
        )
        generated["state"] = "exempt"
        errors = presentation.validate_evidence(candidate, self.profile)
        index = candidate["slots"].index(generated)
        self.assertIn(
            f"evidence.slots[{index}].exempt state requires approval evidence", errors
        )

    def test_contract_order_and_diagnostics_are_deterministic(self) -> None:
        candidate = copy.deepcopy(self.rich)
        candidate["slots"][0], candidate["slots"][1] = (
            candidate["slots"][1],
            candidate["slots"][0],
        )
        first = presentation.validate_evidence(candidate, self.profile)
        second = presentation.validate_evidence(copy.deepcopy(candidate), self.profile)
        self.assertEqual(first, second)
        self.assertIn("evidence.slots must use stable id order", first)

    def _run_evidence_cli(self, evidence: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "presentation.json"
            path.write_text(json.dumps(evidence), encoding="utf-8")
            return subprocess.run(
                [sys.executable, "-I", str(ROOT / "tools" / "presentation.py"),
                 "validate-evidence", "--evidence", str(path)],
                cwd=ROOT, capture_output=True, text=True, check=False, timeout=10,
            )

    def _slot(self, evidence: dict, slot_id: str) -> dict:
        return next(slot for slot in evidence["slots"] if slot["id"] == slot_id)

    def _assessment(self, evidence: dict, state: str) -> None:
        evidence["assessment"]["state"] = state
        evidence["badge"]["state"] = state
        evidence["badge"]["message"] = self.profile["claim_policy"]["state_messages"][state]

    def test_passing_claim_rejects_all_stale_or_unknown_records_in_public_cli(self) -> None:
        for mutation, expected in (
            ({"freshness": "stale"}, "stale"),
            ({"assertion": "unknown"}, "partial"),
            ({"freshness": "stale", "assertion": "unknown"}, "stale"),
            ({"freshness": "unknown"}, "partial"),
            ({"freshness": "not_applicable"}, "partial"),
        ):
            with self.subTest(mutation=mutation):
                candidate = copy.deepcopy(self.rich)
                for slot in candidate["slots"]:
                    for record in slot["evidence"]:
                        record.update(mutation)
                self.assertEqual(expected, presentation.derive_state(candidate["slots"]))
                errors = presentation.validate_evidence(candidate, self.profile)
                self.assertTrue(any("passing requires" in error for error in errors))
                self.assertIn(f"evidence.assessment.state must equal derived state {expected}", errors)
                self.assertIn(f"evidence.badge.state must equal derived state {expected}", errors)
                cli = self._run_evidence_cli(candidate)
                self.assertEqual(1, cli.returncode, cli.stdout + cli.stderr)
                self.assertIn("passing requires", cli.stderr)
                self.assertIn(f"derived state {expected}", cli.stderr)
                self.assertNotIn("Traceback", cli.stderr)

    def test_mixed_current_witness_and_supporting_records_preserve_passing(self) -> None:
        for assertion in ("authoritative", "derived"):
            candidate = copy.deepcopy(self.rich)
            purpose = self._slot(candidate, "purpose")
            current = dict(purpose["evidence"][0], assertion=assertion)
            stale = dict(current, freshness="stale")
            unknown = dict(current, assertion="unknown", freshness="unknown")
            for records in itertools.permutations((current, stale, unknown)):
                with self.subTest(assertion=assertion, order=records):
                    purpose["evidence"] = list(copy.deepcopy(records))
                    original = copy.deepcopy(candidate)
                    self.assertEqual("passing", presentation.derive_state(candidate["slots"]))
                    self.assertEqual([], presentation.validate_evidence(candidate, self.profile))
                    self.assertEqual(original, candidate)

    def test_mixed_records_without_current_known_assertion_cannot_support_passing(self) -> None:
        candidate = copy.deepcopy(self.rich)
        purpose = self._slot(candidate, "purpose")
        template = purpose["evidence"][0]
        records = (
            dict(template, freshness="stale"),
            dict(template, assertion="unknown"),
            dict(template, assertion="derived", freshness="unknown"),
        )
        expected_errors = None
        for values in itertools.permutations(records):
            purpose["evidence"] = list(copy.deepcopy(values))
            original = copy.deepcopy(candidate)
            self.assertEqual("partial", presentation.derive_state(candidate["slots"]))
            errors = presentation.validate_evidence(candidate, self.profile)
            self.assertTrue(any("passing requires" in error for error in errors))
            if expected_errors is None:
                expected_errors = errors
            self.assertEqual(expected_errors, errors)
            self.assertEqual(original, candidate)

    def test_recommended_unsupported_passing_slot_derives_advisory(self) -> None:
        candidate = copy.deepcopy(self.rich)
        architecture = self._slot(candidate, "architecture")
        for record in architecture["evidence"]:
            record["freshness"] = "stale"
        self.assertEqual("advisory", presentation.derive_state(candidate["slots"]))
        errors = presentation.validate_evidence(candidate, self.profile)
        self.assertTrue(any("passing requires" in error for error in errors))
        self.assertIn("evidence.assessment.state must equal derived state advisory", errors)
        self.assertIn("evidence.badge.state must equal derived state advisory", errors)

    def test_honest_negative_or_unknown_states_remain_valid_and_unmodified(self) -> None:
        for slot_id, state, aggregate in (
            ("purpose", "stale", "stale"),
            ("purpose", "unknown", "partial"),
            ("architecture", "stale", "advisory"),
            ("architecture", "unknown", "advisory"),
        ):
            with self.subTest(slot=slot_id, state=state):
                candidate = copy.deepcopy(self.rich)
                slot = self._slot(candidate, slot_id)
                slot["state"] = state
                for record in slot["evidence"]:
                    record["freshness"] = "stale" if state == "stale" else "unknown"
                    record["assertion"] = "unknown"
                self._assessment(candidate, aggregate)
                original = copy.deepcopy(candidate)
                self.assertEqual(aggregate, presentation.derive_state(candidate["slots"]))
                self.assertEqual([], presentation.validate_evidence(candidate, self.profile))
                self.assertEqual(0, self._run_evidence_cli(candidate).returncode)
                self.assertEqual(original, candidate)

    def test_current_evidence_never_upgrades_an_explicit_negative_slot(self) -> None:
        for state, aggregate in (("failing", "failing"), ("blocked", "blocked"), ("partial", "partial"), ("stale", "stale")):
            with self.subTest(state=state):
                candidate = copy.deepcopy(self.rich)
                self._slot(candidate, "purpose")["state"] = state
                self._assessment(candidate, aggregate)
                original = copy.deepcopy(candidate)
                self.assertEqual(aggregate, presentation.derive_state(candidate["slots"]))
                self.assertEqual([], presentation.validate_evidence(candidate, self.profile))
                self.assertEqual(original, candidate)

    def test_malformed_current_records_cannot_be_passing_witnesses(self) -> None:
        for field, value in (("location", ""), ("location", " \t"), ("kind", "unsupported"), ("kind", []), ("assertion", {}), ("freshness", []), ("extra", "unexpected")):
            with self.subTest(field=field, value=value):
                candidate = copy.deepcopy(self.rich)
                record = self._slot(candidate, "purpose")["evidence"][0]
                record[field] = value
                self.assertEqual("partial", presentation.derive_state(candidate["slots"]))
                errors = presentation.validate_evidence(candidate, self.profile)
                self.assertTrue(any("passing requires" in error for error in errors))
                self.assertIn("evidence.assessment.state must equal derived state partial", errors)
                cli = self._run_evidence_cli(candidate)
                self.assertEqual(1, cli.returncode, cli.stdout + cli.stderr)
                self.assertNotIn("Traceback", cli.stderr)

    def test_qualifying_witness_does_not_hide_a_malformed_supporting_record(self) -> None:
        candidate = copy.deepcopy(self.rich)
        purpose = self._slot(candidate, "purpose")
        purpose["evidence"].append({"assertion": "unknown", "freshness": "unknown"})
        self.assertEqual("passing", presentation.derive_state(candidate["slots"]))
        errors = presentation.validate_evidence(candidate, self.profile)
        self.assertTrue(any("fields must exactly match" in error for error in errors))
        self.assertFalse(any("passing requires" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
