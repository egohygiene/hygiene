from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "agent-ready-web"
sys.path.insert(0, str(ROOT / "tools"))

import agent_ready_web  # noqa: E402


class AgentReadyWebFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = agent_ready_web.load_json(
            ROOT / "catalog" / "agent-ready-web-profile.json"
        )
        cls.valid_fixture = agent_ready_web.load_json(
            FIXTURES / "mechanism.valid.json"
        )

    def test_contract_schema_is_a_json_schema_document(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "agent-ready-web-profile.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema",
            schema["$schema"],
        )
        self.assertEqual(
            "https://egohygiene.io/schemas/hygiene/"
            "agent-ready-web-profile.v1.schema.json",
            schema["$id"],
        )
        self.assertFalse(schema["additionalProperties"])

    def test_checked_in_foundation_is_valid_proposed_and_catalog_empty(self) -> None:
        self.assertEqual([], agent_ready_web.validate_profile(self.profile))
        self.assertEqual("proposed", self.profile["status"])
        self.assertEqual([], self.profile["mechanisms"])

    def test_four_concerns_are_distinct_and_exactly_one_is_required(self) -> None:
        self.assertEqual(
            agent_ready_web.CONCERNS,
            [item["id"] for item in self.profile["concerns"]],
        )
        self.assertEqual(
            {
                "primary_concern_cardinality": "exactly-one",
                "independent_requirement_resolution": True,
                "cross_concern_inference": "forbidden",
            },
            self.profile["concern_policy"],
        )

    def test_site_requirement_and_maturity_vocabularies_are_stable(self) -> None:
        self.assertEqual(
            agent_ready_web.SITE_CLASSES,
            [item["id"] for item in self.profile["site_classes"]],
        )
        self.assertEqual(
            agent_ready_web.REQUIREMENT_STRENGTHS,
            [item["id"] for item in self.profile["requirement_strengths"]],
        )
        self.assertEqual(
            agent_ready_web.MATURITY_LEVELS,
            [item["id"] for item in self.profile["maturity_levels"]],
        )

    def test_profile_is_registered_as_a_proposed_hygiene_contract(self) -> None:
        contracts = agent_ready_web.load_json(
            ROOT / "catalog" / "contracts.yaml"
        )["contracts"]
        registered = {contract["id"]: contract for contract in contracts}
        contract = registered[agent_ready_web.PROFILE_SCHEMA]
        self.assertEqual("proposed", contract["status"])
        self.assertEqual("egohygiene/hygiene", contract["owner"])
        self.assertEqual(
            "schemas/agent-ready-web-profile.v1.schema.json",
            contract["source"],
        )

    def test_synthetic_mechanism_proves_the_registration_shape(self) -> None:
        envelope_errors, mechanism_errors = agent_ready_web.validate_fixture(
            self.valid_fixture
        )
        self.assertEqual([], envelope_errors)
        self.assertEqual([], mechanism_errors)
        self.assertEqual("readability", self.valid_fixture["mechanism"]["concern"])
        self.assertEqual(
            "mechanism-registration-only",
            self.profile["mechanism_contract"]["evidence_scope"],
        )

    def test_ambiguous_concern_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.valid_fixture["mechanism"])
        candidate["concern"] = ["readability", "efficiency"]
        errors = agent_ready_web.validate_mechanism(candidate)
        self.assertIn(
            "mechanism.concern must identify exactly one canonical concern",
            errors,
        )

    def test_conditional_requirement_needs_an_explicit_condition(self) -> None:
        candidate = copy.deepcopy(self.valid_fixture["mechanism"])
        candidate["requirements"]["site_class_overrides"][0]["condition"] = None
        errors = agent_ready_web.validate_mechanism(candidate)
        self.assertIn(
            "mechanism.requirements.site_class_overrides[0].condition is required "
            "when strength is conditional",
            errors,
        )

    def test_primary_reference_and_registration_evidence_are_required(self) -> None:
        candidate = copy.deepcopy(self.valid_fixture["mechanism"])
        candidate["authoritative_references"][0]["authority"] = "supporting"
        candidate["registration_evidence"] = []
        errors = agent_ready_web.validate_mechanism(candidate)
        self.assertIn(
            "mechanism.authoritative_references must include at least one primary "
            "authoritative reference",
            errors,
        )
        self.assertIn(
            "mechanism.registration_evidence must be a non-empty array",
            errors,
        )

    def test_reference_locations_reject_parent_traversal(self) -> None:
        candidate = copy.deepcopy(self.valid_fixture["mechanism"])
        candidate["authoritative_references"][0]["location"] = "../specification"
        errors = agent_ready_web.validate_mechanism(candidate)
        self.assertIn(
            "mechanism.authoritative_references[0].location must be an HTTPS URL "
            "or safe repository-relative path",
            errors,
        )

    def test_compatibility_fixtures_cover_valid_and_invalid_records(self) -> None:
        self.assertEqual(
            [],
            agent_ready_web.validate_fixture_directory(FIXTURES),
        )

    def test_compatibility_identifies_additions_and_breakage(self) -> None:
        compatibility = self.profile["compatibility"]
        self.assertTrue(
            any(
                "reviewed minor version" in item
                for item in compatibility["additive_changes"]
            )
        )
        self.assertTrue(
            any(
                "remove or rename" in item
                for item in compatibility["breaking_changes"]
            )
        )
        self.assertEqual("fail-closed", compatibility["unknown_core_values"])

    def test_ownership_boundary_is_complete_and_does_not_claim_adoption(self) -> None:
        self.assertEqual(agent_ready_web.OWNERS, set(self.profile["ownership"]))
        self.assertIn("guarded commerce", self.profile["ownership"]["store"]["owns"])
        self.assertIn(
            "automatic adoption",
            self.profile["ownership"]["pace"]["excludes"],
        )


if __name__ == "__main__":
    unittest.main()
