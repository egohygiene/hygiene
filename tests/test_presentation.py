from __future__ import annotations

import copy
import json
import sys
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


if __name__ == "__main__":
    unittest.main()
