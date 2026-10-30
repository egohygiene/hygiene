from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
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
        first["supersedes"] = ["ADR-0007"]
        second["status"] = "superseded"
        second["superseded_by"] = ["ADR-0006"]
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
            "E_SUPERSESSION_AUTHORITY ADR-0006 replacement ADR-0007 is not accepted",
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
        contracts = {
            contract["id"]: contract for contract in catalog["contracts"]
        }
        self.assertEqual("active", contracts[decisions.DECISION_SCHEMA]["status"])
        self.assertEqual(
            "active", contracts[decisions.POLICY_REFERENCE_SCHEMA]["status"]
        )


class FourDigitIdentifierTests(unittest.TestCase):
    def test_three_digit_canonical_id_requires_normalization(self):
        candidate = json.loads((FIXTURES / "decision.proposed.valid.json").read_text())
        candidate["id"] = "ADR-001"
        self.assertIn("E_ID id must match four-digit ADR-NNNN", decisions.validate_decision(candidate))

    def test_four_digit_range_and_oversized_id(self):
        for identifier in ("ADR-0001", "ADR-9999"):
            candidate = json.loads((FIXTURES / "decision.proposed.valid.json").read_text())
            candidate["id"] = identifier
            self.assertEqual([], decisions.validate_decision(candidate))
        candidate["id"] = "ADR-10000"
        self.assertIn(
            "E_ID id must match four-digit ADR-NNNN",
            decisions.validate_decision(candidate),
        )


class DecisionAlignmentTests(unittest.TestCase):
    load = DecisionContractTests.load

    def cli(
        self, documents: list[dict], *, command: str = "decision-set"
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            arguments = [
                sys.executable,
                "-I",
                str(ROOT / "tools/decisions.py"),
                command,
            ]
            for index, document in enumerate(documents):
                path = Path(directory) / f"decision-{index}.json"
                path.write_text(json.dumps(document), encoding="utf-8")
                arguments.extend(["--input", str(path)])
            return subprocess.run(
                arguments,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )

    def test_pending_proposal_preserves_accepted_predecessor_and_has_no_backlink(
        self,
    ) -> None:
        documents = [
            self.load("decision.pending-predecessor.valid.json"),
            self.load("decision.pending-replacement.valid.json"),
        ]
        before = copy.deepcopy(documents)
        self.assertEqual([], decisions.validate_decision_set(documents))
        self.assertEqual(before, documents)
        result = self.cli(documents)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_declined_proposal_history_does_not_require_effective_backlinks(
        self,
    ) -> None:
        for status in ("rejected", "deprecated"):
            predecessor = self.load("decision.pending-predecessor.valid.json")
            replacement = self.load("decision.accepted.valid.json")
            replacement["status"] = status
            with self.subTest(status=status):
                self.assertEqual(
                    [], decisions.validate_decision_set([predecessor, replacement])
                )
                predecessor["status"] = "superseded"
                predecessor["superseded_by"] = [replacement["id"]]
                errors = decisions.validate_decision_set([predecessor, replacement])
                self.assertTrue(
                    any(
                        error.startswith("E_SUPERSESSION_AUTHORITY") for error in errors
                    ),
                    errors,
                )

    def test_effective_supersession_requires_old_disposition_and_reciprocal_links(
        self,
    ) -> None:
        predecessor = self.load("decision.pending-predecessor.valid.json")
        replacement = self.load("decision.accepted.valid.json")
        predecessor["superseded_by"] = [replacement["id"]]
        self.assertTrue(
            any(
                "E_SUPERSESSION" in error
                for error in decisions.validate_decision_set([predecessor, replacement])
            )
        )
        predecessor["status"] = "superseded"
        self.assertEqual(
            [], decisions.validate_decision_set([predecessor, replacement])
        )
        replacement["supersedes"] = []
        self.assertTrue(
            any(
                error.startswith("E_SUPERSESSION_FORWARD")
                for error in decisions.validate_decision_set([predecessor, replacement])
            )
        )

    def test_verified_approval_only_is_rejected_by_both_public_commands(self) -> None:
        candidate = self.load("decision.verified-approval-only.invalid.json")
        self.assertTrue(
            any(
                error.startswith("E_VERIFICATION")
                for error in decisions.validate_decision(candidate)
            )
        )
        for command in ("decision", "decision-set"):
            with self.subTest(command=command):
                result = self.cli([candidate], command=command)
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertIn("E_VERIFICATION", result.stderr)

    def test_named_validation_descriptor_is_structural_and_not_execution(self) -> None:
        candidate = self.load("decision.verified.valid.json")
        self.assertEqual([], decisions.validate_decision(candidate))
        self.assertEqual(0, self.cli([candidate], command="decision").returncode)
        candidate["evidence"][0]["description"] = " \t"
        self.assertTrue(
            any(
                error.startswith("E_VERIFICATION")
                for error in decisions.validate_decision(candidate)
            )
        )
        candidate["evidence"][0]["description"] = "Synthetic named validation"
        candidate["evidence"][0]["url"] = "not-a-uri"
        self.assertTrue(
            any(
                error.startswith("E_URI")
                for error in decisions.validate_decision(candidate)
            )
        )

    def test_dangling_legacy_and_canonical_local_refs_receive_same_diagnostics(
        self,
    ) -> None:
        for field in ("related", "supersedes", "superseded_by"):
            for reference in ("ADR-999", "ADR-0999"):
                candidate = (
                    self.load("decision.superseded.valid.json")
                    if field == "superseded_by"
                    else self.load("decision.proposed.valid.json")
                )
                candidate[field] = [reference]
                with self.subTest(field=field, reference=reference):
                    expected = (
                        f"E_DANGLING_REFERENCE {candidate['id']}.{field} -> {reference}"
                    )
                    self.assertIn(
                        expected, decisions.validate_decision_set([candidate])
                    )
                    result = self.cli([candidate])
                    self.assertEqual(1, result.returncode)
                    self.assertIn(expected, result.stderr)

    def test_legacy_reference_does_not_silently_alias_a_padded_identity(self) -> None:
        first = self.load("decision.pending-predecessor.valid.json")
        second = self.load("decision.proposed.valid.json")
        second["related"] = ["ADR-006"]
        self.assertIn(
            "E_DANGLING_REFERENCE ADR-0007.related -> ADR-006",
            decisions.validate_decision_set([first, second]),
        )
        self.assertEqual(["ADR-006"], second["related"])

    def test_historical_fixture_lookup_preserves_identity_but_requires_older_pin(
        self,
    ) -> None:
        documents = [
            self.load("historical/policy-1.1.0/decision.previous.json"),
            self.load("historical/policy-1.1.0/decision.replacement.json"),
        ]
        before = copy.deepcopy(documents)
        errors = decisions.validate_decision_set(documents)
        self.assertTrue(any("E_ID" in error for error in errors), errors)
        self.assertFalse(
            any(
                "E_DANGLING_REFERENCE" in error or "E_SUPERSESSION_" in error
                for error in errors
            ),
            errors,
        )
        self.assertEqual(before, documents)

    def test_explicit_synthetic_padding_map_preserves_disposition_and_resolves(
        self,
    ) -> None:
        documents = [
            self.load("historical/policy-1.1.0/decision.previous.json"),
            self.load("historical/policy-1.1.0/decision.replacement.json"),
        ]
        originals = copy.deepcopy(documents)
        mapping = {"ADR-006": "ADR-0006", "ADR-007": "ADR-0007"}
        for document in documents:
            document["id"] = mapping[document["id"]]
            for field in ("related", "supersedes", "superseded_by"):
                document[field] = [
                    mapping.get(reference, reference) for reference in document[field]
                ]
        self.assertEqual([], decisions.validate_decision_set(documents))
        for before, after in zip(originals, documents):
            for key in set(before) - {"id", "related", "supersedes", "superseded_by"}:
                self.assertEqual(before[key], after[key])

    def test_zero_id_is_rejected_and_valid_canonical_bounds_remain_valid(self) -> None:
        candidate = self.load("decision.zero-id.invalid.json")
        for command in ("decision", "decision-set"):
            with self.subTest(command=command):
                result = self.cli([candidate], command=command)
                self.assertEqual(1, result.returncode, result.stdout)
                self.assertIn("E_ID", result.stderr)
        for identifier in ("ADR-0001", "ADR-9999"):
            candidate["id"] = identifier
            self.assertEqual([], decisions.validate_decision(candidate))

    def test_pending_declarations_still_reject_cycles_and_self_links(self) -> None:
        predecessor = self.load("decision.pending-predecessor.valid.json")
        replacement = self.load("decision.pending-replacement.valid.json")
        predecessor["supersedes"] = [replacement["id"]]
        errors = decisions.validate_decision_set([predecessor, replacement])
        self.assertTrue(
            any(error.startswith("E_SUPERSESSION_CYCLE") for error in errors), errors
        )
        replacement["supersedes"] = [replacement["id"]]
        self.assertTrue(
            any(
                error.startswith("E_SELF_REFERENCE")
                for error in decisions.validate_decision_set([replacement])
            )
        )

    def test_malformed_lineage_is_diagnosed_without_graph_lookup_crashes(self) -> None:
        for field in ("related", "supersedes", "superseded_by"):
            for invalid in (None, {}, [{}]):
                candidate = self.load("decision.superseded.valid.json")
                candidate[field] = invalid
                with self.subTest(field=field, invalid=invalid):
                    errors = decisions.validate_decision_set([candidate])
                    self.assertTrue(any("E_TYPE" in error for error in errors), errors)
                    result = self.cli([candidate])
                    self.assertEqual(1, result.returncode, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
