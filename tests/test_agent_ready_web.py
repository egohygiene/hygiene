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
        cls.capability_fixture = agent_ready_web.load_json(
            FIXTURES / "mechanism.capability.valid.json"
        )
        cls.commerce_fixture = agent_ready_web.load_json(
            FIXTURES / "mechanism.commerce.valid.json"
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
        self.assertIn("capabilityPolicy", schema["$defs"])
        self.assertIn("commercePolicy", schema["$defs"])
        self.assertIn("capabilityBinding", schema["$defs"])
        self.assertIn("commerceBinding", schema["$defs"])
        self.assertEqual(
            ["resolution_policy", "representation_policy"],
            schema["allOf"][0]["then"]["required"],
        )
        self.assertEqual(
            [
                "resolution_policy",
                "representation_policy",
                "capability_policy",
                "commerce_policy",
            ],
            schema["allOf"][1]["then"]["required"],
        )
        self.assertIn(
            "browser-capability",
            schema["$defs"]["artifact"]["properties"]["kind"]["enum"],
        )

    def test_checked_in_catalog_is_valid_complete_and_proposed(self) -> None:
        self.assertEqual([], agent_ready_web.validate_profile(self.profile))
        self.assertEqual("proposed", self.profile["status"])
        self.assertEqual("1.0.0-alpha.3", self.profile["version"])
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

    def test_concern_specific_fixtures_prove_guarded_binding_shapes(self) -> None:
        for fixture, binding in (
            (self.capability_fixture, "capability"),
            (self.commerce_fixture, "commerce"),
        ):
            envelope_errors, mechanism_errors = agent_ready_web.validate_fixture(
                fixture
            )
            self.assertEqual([], envelope_errors)
            self.assertEqual([], mechanism_errors)
            self.assertEqual(
                agent_ready_web.MECHANISM_FIELDS | {binding},
                set(fixture["mechanism"]),
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
            "ads-txt": ("commerce", "established"),
            "ai-crawler-guidance": ("readability", "emerging"),
            "ai-oriented-hints": ("readability", "experimental"),
            "app-ads-txt": ("commerce", "established"),
            "canonical-metadata": ("readability", "established"),
            "cats-txt": ("readability", "experimental"),
            "commerce-product-offer-jsonld": ("commerce", "established"),
            "entitymap-html": ("readability", "published_specification"),
            "entitymap-json": ("readability", "published_specification"),
            "llms-full-txt": ("efficiency", "emerging"),
            "llms-txt": ("readability", "emerging"),
            "markdown-alternate": ("efficiency", "emerging"),
            "mcp-b-runtime": ("capability", "experimental"),
            "robots-txt": ("readability", "established"),
            "sitemap-xml": ("readability", "established"),
            "structured-discovery-jsonld": ("readability", "established"),
            "webmcp-tools": ("capability", "experimental"),
        }
        actual = {
            mechanism["id"]: (
                mechanism["concern"],
                mechanism["maturity"]["level"],
            )
            for mechanism in self.profile["mechanisms"]
        }
        self.assertEqual(expected, actual)
        self.assertIn("capability", {value[0] for value in actual.values()})
        self.assertIn("commerce", {value[0] for value in actual.values()})

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

    def test_capability_policy_is_fail_closed_and_human_controlled(self) -> None:
        policy = self.profile["capability_policy"]
        self.assertEqual(
            agent_ready_web.CAPABILITY_POLICY,
            {
                key: value
                for key, value in policy.items()
                if key != "authoritative_references"
            },
        )
        self.assertEqual(
            ["read-only", "state-changing"],
            policy["classification"]["classes"],
        )
        self.assertEqual(
            "fresh-human-confirmation-before-consequential-or-irreversible-effect",
            policy["classification"]["state_changing"]["confirmation"],
        )
        self.assertEqual(
            "secure-exact-origin-and-current-document",
            policy["security"]["origin_binding"],
        )
        self.assertEqual(
            "nonce-or-idempotency-key-bound-to-actor-origin-action-and-expiry",
            policy["execution_evidence"]["replay_protection"],
        )
        self.assertEqual("deny", policy["failure_policy"]["unknown_or_stale_contract"])

    def test_capability_bindings_are_versioned_pinned_and_experimental(self) -> None:
        capabilities = {
            mechanism["id"]: mechanism
            for mechanism in self.profile["mechanisms"]
            if mechanism["concern"] == "capability"
        }
        self.assertEqual({"mcp-b-runtime", "webmcp-tools"}, set(capabilities))
        for mechanism in capabilities.values():
            self.assertEqual("experimental", mechanism["maturity"]["level"])
            self.assertEqual(
                "exact-version-or-immutable-revision",
                mechanism["capability"]["implementation_pin"],
            )
            self.assertEqual(
                "versioned-json-schema-and-runtime-validation-required",
                mechanism["capability"]["input_contract"],
            )
            self.assertEqual(
                "versioned-json-schema-and-runtime-validation-required",
                mechanism["capability"]["output_contract"],
            )

    def test_capability_binding_rejects_missing_or_unpinned_authority(self) -> None:
        missing = copy.deepcopy(self.capability_fixture["mechanism"])
        del missing["capability"]
        self.assertIn(
            "mechanism.capability is required for a capability mechanism",
            agent_ready_web.validate_mechanism(missing),
        )

        unpinned = copy.deepcopy(self.capability_fixture["mechanism"])
        unpinned["capability"]["implementation_pin"] = "floating-latest"
        self.assertIn(
            "mechanism.capability.implementation_pin is invalid",
            agent_ready_web.validate_mechanism(unpinned),
        )

        mismatched = copy.deepcopy(self.capability_fixture["mechanism"])
        mismatched["capability"]["protocol_revision"] = (
            "package-release-or-immutable-repository-revision"
        )
        self.assertIn(
            "mechanism.capability.protocol_revision is invalid for webmcp",
            agent_ready_web.validate_mechanism(mismatched),
        )

    def test_commerce_policy_keeps_metadata_and_actions_separate(self) -> None:
        policy = self.profile["commerce_policy"]
        self.assertEqual(
            agent_ready_web.COMMERCE_POLICY,
            {
                key: value
                for key, value in policy.items()
                if key != "authoritative_references"
            },
        )
        self.assertEqual("egohygiene/store", policy["guarded_actions"]["owner"])
        self.assertEqual("none", policy["guarded_actions"]["metadata_authority"])
        self.assertEqual(
            "do-not-expose-or-invoke",
            policy["guarded_actions"]["missing_contract"],
        )
        self.assertEqual(
            "prohibited",
            policy["advertising"]["invented_relationships"],
        )
        self.assertEqual(
            "forbidden",
            policy["separation"]["offer_to_purchase_authority"],
        )

    def test_commerce_bindings_never_grant_executable_authority(self) -> None:
        commerce = [
            mechanism
            for mechanism in self.profile["mechanisms"]
            if mechanism["concern"] == "commerce"
        ]
        self.assertEqual(3, len(commerce))
        for mechanism in commerce:
            self.assertEqual("none", mechanism["commerce"]["executable_authority"])
            self.assertEqual(
                "store-owned-versioned-contract-required-for-actions",
                mechanism["commerce"]["transaction_contract"],
            )

        candidate = copy.deepcopy(self.commerce_fixture["mechanism"])
        candidate["commerce"]["executable_authority"] = "purchase"
        self.assertIn(
            "mechanism.commerce.executable_authority must be none",
            agent_ready_web.validate_mechanism(candidate),
        )

        candidate = copy.deepcopy(self.commerce_fixture["mechanism"])
        candidate["commerce"]["identity_source"] = (
            "publisher-and-advertising-system-contract-evidence"
        )
        self.assertIn(
            "mechanism.commerce.identity_source is invalid for "
            "descriptive-product-offer",
            agent_ready_web.validate_mechanism(candidate),
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
        self.assertIn("webmcp", descriptions)

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
