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


class AgentReadyWebCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = agent_ready_web.load_json(
            ROOT / "catalog" / "agent-ready-web-profile.json"
        )
        cls.valid_fixture = agent_ready_web.load_json(
            FIXTURES / "mechanism.valid.json"
        )
        cls.policy_fixture = agent_ready_web.load_json(
            FIXTURES / "mechanism.discovery-policy.valid.json"
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
        self.assertIn("catalogMechanism", schema["$defs"])
        self.assertEqual(
            ["resolution_policy", "representation_policy"],
            schema["allOf"][0]["then"]["required"],
        )

    def test_checked_in_catalog_is_valid_complete_and_proposed(self) -> None:
        self.assertEqual([], agent_ready_web.validate_profile(self.profile))
        self.assertEqual("proposed", self.profile["status"])
        self.assertEqual("1.0.0-alpha.2", self.profile["version"])
        self.assertEqual(
            agent_ready_web.SCOPED_MECHANISM_IDS,
            [item["id"] for item in self.profile["mechanisms"]],
        )

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

    def test_checkpoint_one_mechanism_shape_remains_compatible(self) -> None:
        self.assertEqual(
            agent_ready_web.MECHANISM_BASE_FIELDS,
            set(self.valid_fixture["mechanism"]),
        )
        self.assertEqual(
            [],
            agent_ready_web.validate_mechanism(self.valid_fixture["mechanism"]),
        )

    def test_enriched_policy_fixture_proves_catalog_record_shape(self) -> None:
        envelope_errors, mechanism_errors = agent_ready_web.validate_fixture(
            self.policy_fixture
        )
        self.assertEqual([], envelope_errors)
        self.assertEqual([], mechanism_errors)
        self.assertEqual(
            agent_ready_web.MECHANISM_FIELDS,
            set(self.policy_fixture["mechanism"]),
        )

    def test_applicability_and_truthful_absence_policy_is_exact(self) -> None:
        self.assertEqual(
            agent_ready_web.RESOLUTION_POLICY,
            self.profile["resolution_policy"],
        )
        self.assertTrue(
            self.profile["resolution_policy"]["applicability_precedes_strength"]
        )
        self.assertEqual(
            "prohibited",
            self.profile["resolution_policy"]["fabricated_placeholder"],
        )
        for mechanism in self.profile["mechanisms"]:
            self.assertEqual(
                "before-requirement-strength",
                mechanism["applicability"]["evaluation"],
            )
            self.assertEqual(
                "valid-absent",
                mechanism["applicability"]["inapplicable_result"],
            )

    def test_every_mechanism_resolves_every_site_class(self) -> None:
        for mechanism in self.profile["mechanisms"]:
            self.assertEqual(
                agent_ready_web.SITE_CLASSES,
                [
                    rule["site_class"]
                    for rule in mechanism["requirements"]["site_class_overrides"]
                ],
            )

    def test_mechanism_classification_and_concern_scope_are_explicit(self) -> None:
        expected = {
            "ai-crawler-guidance": ("readability", "emerging"),
            "ai-oriented-hints": ("readability", "experimental"),
            "canonical-metadata": ("readability", "established"),
            "cats-txt": ("readability", "experimental"),
            "entitymap-html": ("readability", "published_specification"),
            "entitymap-json": ("readability", "published_specification"),
            "llms-full-txt": ("efficiency", "emerging"),
            "llms-txt": ("readability", "emerging"),
            "markdown-alternate": ("efficiency", "emerging"),
            "robots-txt": ("readability", "established"),
            "sitemap-xml": ("readability", "established"),
            "structured-discovery-jsonld": ("readability", "established"),
        }
        actual = {
            mechanism["id"]: (
                mechanism["concern"],
                mechanism["maturity"]["level"],
            )
            for mechanism in self.profile["mechanisms"]
        }
        self.assertEqual(expected, actual)
        self.assertNotIn("capability", {value[0] for value in actual.values()})
        self.assertNotIn("commerce", {value[0] for value in actual.values()})

    def test_emerging_and_experimental_mechanisms_are_non_blocking(self) -> None:
        for mechanism in self.profile["mechanisms"]:
            if mechanism["maturity"]["level"] not in {
                "emerging",
                "experimental",
            }:
                continue
            rules = [mechanism["requirements"]["default"]]
            rules.extend(mechanism["requirements"]["site_class_overrides"])
            self.assertNotIn("required", {rule["strength"] for rule in rules})

        candidate = copy.deepcopy(self.policy_fixture["mechanism"])
        candidate["requirements"]["default"]["strength"] = "required"
        errors = agent_ready_web.validate_mechanism(candidate)
        self.assertIn(
            "mechanism emerging or experimental mechanisms must remain "
            "non-blocking by default",
            errors,
        )

    def test_representation_integrity_and_negotiation_are_deterministic(self) -> None:
        policy = self.profile["representation_policy"]
        self.assertEqual(
            agent_ready_web.REPRESENTATION_INTEGRITY,
            policy["integrity"],
        )
        self.assertEqual(
            agent_ready_web.CONTENT_NEGOTIATION_POLICY,
            policy["content_negotiation"],
        )
        self.assertEqual(
            agent_ready_web.ALTERNATE_DISCOVERY_POLICY,
            policy["alternate_discovery"],
        )
        self.assertEqual(
            "prohibited",
            policy["content_negotiation"]["user_agent_selection"],
        )
        self.assertEqual(
            "same-or-stricter-than-canonical",
            policy["integrity"]["access_control"],
        )

    def test_catalog_rules_include_privacy_and_scope_boundaries(self) -> None:
        descriptions = " ".join(
            rule["description"]
            for mechanism in self.profile["mechanisms"]
            for rule in mechanism["content_rules"] + mechanism["validation_rules"]
        ).lower()
        self.assertIn("private", descriptions)
        self.assertIn("canonical", descriptions)
        self.assertIn("commerce", descriptions)
        self.assertIn("authorization", descriptions)
        self.assertNotIn("webmcp", descriptions)

    def test_every_maturity_assessment_cites_a_primary_reference(self) -> None:
        for mechanism in self.profile["mechanisms"]:
            authorities = {
                reference["id"]: reference["authority"]
                for reference in mechanism["authoritative_references"]
            }
            self.assertTrue(
                any(
                    authorities.get(reference_id) == "primary"
                    for reference_id in mechanism["maturity"]["reference_ids"]
                )
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
