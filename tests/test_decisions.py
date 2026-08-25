from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import decisions  # noqa: E402


FIXTURES = ROOT / "fixtures" / "architecture-decisions"


class DecisionContractTests(unittest.TestCase):
    def load(self, name: str) -> dict[str, object]:
        with (FIXTURES / name).open("r", encoding="utf-8") as stream:
            return json.load(stream)

    def test_valid_decision_lifecycle_fixtures(self) -> None:
        for name in (
            "decision.proposed.valid.json",
            "decision.accepted.valid.json",
            "decision.rejected.valid.json",
            "decision.superseded.valid.json",
            "decision.deprecated.valid.json",
        ):
            with self.subTest(name=name):
                self.assertEqual([], decisions.validate_decision(self.load(name)))

    def test_false_acceptance_is_rejected(self) -> None:
        errors = decisions.validate_decision(
            self.load("decision.accepted-missing-approval.invalid.json")
        )
        self.assertIn("E_APPROVAL approval must be an object", errors)

    def test_lifecycle_disposition_evidence_must_match(self) -> None:
        candidate = copy.deepcopy(self.load("decision.accepted.valid.json"))
        candidate["approval"]["evidence"] = (
            "https://github.com/egohygiene/relay/pull/8#issuecomment-2"
        )
        errors = decisions.validate_decision(candidate)
        self.assertIn(
            "E_APPROVAL_EVIDENCE approval.evidence must match an evidence item "
            "of type approval",
            errors,
        )

    def test_superseded_decision_requires_replacement(self) -> None:
        candidate = copy.deepcopy(self.load("decision.superseded.valid.json"))
        candidate["superseded_by"] = []
        errors = decisions.validate_decision(candidate)
        self.assertIn(
            "E_SUPERSESSION superseded decisions require superseded_by",
            errors,
        )

    def test_bidirectional_supersession_pair_is_valid(self) -> None:
        documents = [
            self.load("decision.superseded.valid.json"),
            self.load("decision.accepted.valid.json"),
        ]
        self.assertEqual([], decisions.validate_decision_set(documents))

    def test_missing_supersession_backlink_is_rejected(self) -> None:
        predecessor = self.load("decision.superseded.valid.json")
        replacement = self.load("decision.accepted.valid.json")
        predecessor["superseded_by"] = []
        errors = decisions.validate_decision_set([predecessor, replacement])
        self.assertTrue(
            any(error.startswith("E_SUPERSESSION_BACKLINK") for error in errors),
            errors,
        )

    def test_supersession_cycle_is_rejected(self) -> None:
        first = self.load("decision.superseded.valid.json")
        second = self.load("decision.accepted.valid.json")
        first["supersedes"] = ["ADR-007"]
        second["status"] = "superseded"
        second["superseded_by"] = ["ADR-006"]
        errors = decisions.validate_decision_set([first, second])
        self.assertTrue(
            any(error.startswith("E_SUPERSESSION_CYCLE") for error in errors),
            errors,
        )

    def test_proposed_replacement_cannot_supersede_history_yet(self) -> None:
        predecessor = self.load("decision.superseded.valid.json")
        replacement = self.load("decision.accepted.valid.json")
        replacement["status"] = "proposed"
        replacement["approval"] = None
        replacement["evidence"] = []
        errors = decisions.validate_decision_set([predecessor, replacement])
        self.assertIn(
            "E_SUPERSESSION_AUTHORITY ADR-006 replacement ADR-007 is not accepted",
            errors,
        )

    def test_unknown_top_level_override_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.load("decision.proposed.valid.json"))
        candidate["local_status"] = "done"
        errors = decisions.validate_decision(candidate)
        self.assertIn("E_OVERRIDE unknown top-level fields: local_status", errors)

    def test_namespaced_extension_payload_is_required(self) -> None:
        candidate = copy.deepcopy(self.load("decision.proposed.valid.json"))
        candidate["extensions"] = {"status": "locally-accepted"}
        errors = decisions.validate_decision(candidate)
        self.assertTrue(any(error.startswith("E_EXTENSION_ID") for error in errors))
        self.assertTrue(any(error.startswith("E_EXTENSION_TYPE") for error in errors))

    def test_valid_policy_reference(self) -> None:
        self.assertEqual(
            [],
            decisions.validate_policy_reference(
                self.load("policy-reference.valid.json")
            ),
        )

    def test_policy_reference_requires_canonical_owner_and_pin(self) -> None:
        errors = decisions.validate_policy_reference(
            self.load("policy-reference-unpinned.invalid.json")
        )
        self.assertIn(
            "E_POLICY_OWNER policy.source.repository must be egohygiene/hygiene",
            errors,
        )
        self.assertIn(
            "E_POLICY_PIN policy.source.revision must be a full commit SHA",
            errors,
        )

    def test_contract_schemas_and_catalog_are_machine_readable(self) -> None:
        for name in (
            "architecture-decision.v1.schema.json",
            "architecture-decision-policy-reference.v1.schema.json",
        ):
            with (ROOT / "schemas" / name).open("r", encoding="utf-8") as stream:
                schema = json.load(stream)
            self.assertEqual(
                "https://json-schema.org/draft/2020-12/schema",
                schema["$schema"],
            )
        with (ROOT / "catalog" / "contracts.yaml").open(
            "r", encoding="utf-8"
        ) as stream:
            catalog = json.load(stream)
        ids = [contract["id"] for contract in catalog["contracts"]]
        self.assertIn(decisions.DECISION_SCHEMA, ids)
        self.assertIn(decisions.POLICY_REFERENCE_SCHEMA, ids)


if __name__ == "__main__":
    unittest.main()
