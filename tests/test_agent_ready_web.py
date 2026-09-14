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
        cls.application_fixture = agent_ready_web.load_json(
            FIXTURES / "site.application.valid.json"
        )
        cls.content_fixture = agent_ready_web.load_json(
            FIXTURES / "site.content.valid.json"
        )

    def refresh_conformance(self, candidate: dict) -> None:
        summary, diagnostics = agent_ready_web.derive_conformance(
            candidate,
            self.profile,
        )
        candidate["summary"] = summary
        candidate["diagnostics"] = diagnostics

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
        self.assertIn("integrationPolicy", schema["$defs"])
        self.assertIn("conformancePolicy", schema["$defs"])
        self.assertIn("consumerResolution", schema["$defs"])
        self.assertIn("referenceReview", schema["$defs"])
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
        self.assertEqual(
            [
                "resolution_policy",
                "representation_policy",
                "capability_policy",
                "commerce_policy",
                "integration_policy",
                "conformance_policy",
                "reference_review",
            ],
            schema["allOf"][2]["then"]["required"],
        )
        self.assertIn(
            "browser-capability",
            schema["$defs"]["artifact"]["properties"]["kind"]["enum"],
        )

    def test_checked_in_catalog_is_valid_complete_and_proposed(self) -> None:
        self.assertEqual([], agent_ready_web.validate_profile(self.profile))
        self.assertEqual("proposed", self.profile["status"])
        self.assertEqual("1.0.0-alpha.4", self.profile["version"])
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

    def test_integration_policy_preserves_cross_layer_authority_boundaries(self) -> None:
        self.assertEqual(
            agent_ready_web.INTEGRATION_POLICY,
            self.profile["integration_policy"],
        )
        invariants = self.profile["integration_policy"]["cross_layer_invariants"]
        self.assertEqual(
            [
                "discovery",
                "structured-metadata",
                "advertising-declaration",
                "maturity-classification",
            ],
            invariants["non_authoritative_inputs"],
        )
        self.assertEqual(
            ["capability", "consent", "authorization", "transaction-authority"],
            invariants["cannot_grant"],
        )
        candidate = copy.deepcopy(self.profile)
        candidate["integration_policy"]["cross_layer_invariants"][
            "capability_source"
        ] = "metadata"
        self.assertIn(
            "profile.integration_policy must preserve independent concerns and "
            "authority boundaries",
            agent_ready_web.validate_profile(candidate),
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
        evidence_contract = registered[agent_ready_web.CONFORMANCE_SCHEMA]
        self.assertEqual("proposed", evidence_contract["status"])
        self.assertEqual("egohygiene/hygiene", evidence_contract["owner"])
        self.assertEqual(
            "schemas/agent-ready-web-conformance.v1.schema.json",
            evidence_contract["source"],
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
            agent_ready_web.validate_fixture_directory(FIXTURES, self.profile),
        )

    def test_whole_profile_fixtures_cover_every_site_class(self) -> None:
        fixtures = [
            agent_ready_web.load_json(path)
            for path in sorted(FIXTURES.glob("site.*.valid.json"))
        ]
        self.assertEqual(
            agent_ready_web.SITE_CLASSES,
            sorted(fixture["site_class"] for fixture in fixtures),
        )
        for fixture in fixtures:
            envelope_errors, conformance_errors = (
                agent_ready_web.validate_conformance_fixture(fixture, self.profile)
            )
            self.assertEqual([], envelope_errors)
            self.assertEqual([], conformance_errors)
            self.assertTrue(fixture["synthetic"])
            self.assertTrue(fixture["conformance"]["synthetic"])
            self.assertEqual(
                agent_ready_web.SCOPED_MECHANISM_IDS,
                [item["id"] for item in fixture["conformance"]["mechanisms"]],
            )

    def test_conformance_schema_denies_cross_layer_authority(self) -> None:
        schema = agent_ready_web.load_json(
            ROOT / "schemas" / "agent-ready-web-conformance.v1.schema.json"
        )
        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema",
            schema["$schema"],
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            agent_ready_web.AUTHORITY_ASSERTIONS,
            schema["properties"]["authority_assertions"]["const"],
        )
        self.assertIn(
            "profile",
            schema["required"],
        )
        self.assertIn(
            "resolved_revision",
            schema["$defs"]["pin"]["required"],
        )

    def test_requirement_resolution_covers_every_normative_state(self) -> None:
        mechanism = copy.deepcopy(self.profile["mechanisms"][0])
        rule = mechanism["requirements"]["site_class_overrides"][0]
        for strength in ("required", "recommended", "optional", "prohibited"):
            rule["strength"] = strength
            rule["condition"] = None
            self.assertEqual(
                (strength, strength),
                agent_ready_web.resolve_requirement(
                    mechanism,
                    "application",
                    "applicable",
                    None,
                ),
            )
        rule["strength"] = "conditional"
        rule["condition"] = "synthetic-condition"
        self.assertEqual(
            ("conditional", "required"),
            agent_ready_web.resolve_requirement(
                mechanism, "application", "applicable", "met"
            ),
        )
        self.assertEqual(
            ("conditional", "inapplicable"),
            agent_ready_web.resolve_requirement(
                mechanism, "application", "applicable", "not-met"
            ),
        )
        self.assertEqual(
            ("conditional", "unresolved"),
            agent_ready_web.resolve_requirement(
                mechanism, "application", "applicable", "unknown"
            ),
        )
        self.assertEqual(
            ("conditional", "inapplicable"),
            agent_ready_web.resolve_requirement(
                mechanism, "application", "not-applicable", None
            ),
        )
        self.assertEqual(
            ("conditional", "unresolved"),
            agent_ready_web.resolve_requirement(
                mechanism, "application", "unknown", None
            ),
        )

    def test_conformance_diagnostics_and_levels_are_deterministic(self) -> None:
        application = self.application_fixture["conformance"]
        self.assertEqual([], agent_ready_web.validate_conformance(application, self.profile))
        self.assertEqual("recommended", application["summary"]["level"])
        self.assertEqual(["ARW-EXP-001"], [item["code"] for item in application["diagnostics"]])

        content = self.content_fixture["conformance"]
        self.assertEqual([], agent_ready_web.validate_conformance(content, self.profile))
        self.assertEqual("baseline", content["summary"]["level"])
        self.assertEqual(["ARW-REC-001"], [item["code"] for item in content["diagnostics"]])

        missing_required = copy.deepcopy(application)
        assessment = missing_required["mechanisms"][4]
        assessment["presence"] = "absent"
        assessment["validation"] = "not-run"
        assessment["evidence_ids"] = []
        self.refresh_conformance(missing_required)
        self.assertEqual("nonconformant", missing_required["summary"]["level"])
        self.assertIn(
            "ARW-REQ-001",
            [item["code"] for item in missing_required["diagnostics"]],
        )
        self.assertEqual(
            [],
            agent_ready_web.validate_conformance(missing_required, self.profile),
        )

    def test_every_failure_diagnostic_path_is_exercised(self) -> None:
        unknown = copy.deepcopy(self.application_fixture["conformance"])
        unknown_assessment = unknown["mechanisms"][1]
        unknown_assessment["applicability"] = "unknown"
        unknown_assessment["resolved_strength"] = "unresolved"
        self.refresh_conformance(unknown)
        self.assertIn("ARW-APP-001", [item["code"] for item in unknown["diagnostics"]])

        inapplicable_present = copy.deepcopy(
            self.application_fixture["conformance"]
        )
        inapplicable_assessment = inapplicable_present["mechanisms"][16]
        inapplicable_assessment["presence"] = "present"
        inapplicable_assessment["validation"] = "passed"
        inapplicable_assessment["evidence_ids"] = ["artifact-snapshot"]
        self.refresh_conformance(inapplicable_present)
        self.assertIn(
            "ARW-APP-002",
            [item["code"] for item in inapplicable_present["diagnostics"]],
        )

        failed_present = copy.deepcopy(self.application_fixture["conformance"])
        failed_assessment = failed_present["mechanisms"][4]
        failed_assessment["validation"] = "failed"
        failed_assessment["evidence_ids"] = []
        self.refresh_conformance(failed_present)
        self.assertEqual(
            ["ARW-EVD-001", "ARW-VAL-001"],
            [
                item["code"]
                for item in failed_present["diagnostics"]
                if item["mechanism_id"] == "canonical-metadata"
            ],
        )

        conditional_profile = copy.deepcopy(self.profile)
        conditional_rule = conditional_profile["mechanisms"][1]["requirements"][
            "site_class_overrides"
        ][0]
        conditional_rule["strength"] = "conditional"
        conditional_rule["condition"] = "synthetic-condition"
        conditional = copy.deepcopy(self.application_fixture["conformance"])
        conditional_assessment = conditional["mechanisms"][1]
        conditional_assessment["declared_strength"] = "conditional"
        conditional_assessment["requirement_condition"] = "unknown"
        conditional_assessment["resolved_strength"] = "unresolved"
        _, conditional_diagnostics = agent_ready_web.derive_conformance(
            conditional,
            conditional_profile,
        )
        self.assertIn(
            "ARW-CND-001",
            [item["code"] for item in conditional_diagnostics],
        )

        prohibited_profile = copy.deepcopy(self.profile)
        prohibited_rule = prohibited_profile["mechanisms"][1]["requirements"][
            "site_class_overrides"
        ][0]
        prohibited_rule["strength"] = "prohibited"
        prohibited_rule["condition"] = None
        prohibited = copy.deepcopy(self.application_fixture["conformance"])
        prohibited_assessment = prohibited["mechanisms"][1]
        prohibited_assessment["declared_strength"] = "prohibited"
        prohibited_assessment["resolved_strength"] = "prohibited"
        prohibited_assessment["presence"] = "present"
        prohibited_assessment["validation"] = "passed"
        prohibited_assessment["evidence_ids"] = ["artifact-snapshot"]
        _, prohibited_diagnostics = agent_ready_web.derive_conformance(
            prohibited,
            prohibited_profile,
        )
        self.assertIn(
            "ARW-PRO-001",
            [item["code"] for item in prohibited_diagnostics],
        )

    def test_narrow_exemption_is_distinct_and_never_passing(self) -> None:
        candidate = copy.deepcopy(self.application_fixture["conformance"])
        candidate["evidence"].insert(
            1,
            {
                "id": "approval-record",
                "kind": "approval",
                "location": "fixtures/agent-ready-web/site.application.valid.json",
                "observed_at": "2026-09-14T16:00:00Z",
                "subject_revision": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "description": "Synthetic time-bounded approval for compatibility testing only.",
                "sha256": None,
            },
        )
        assessment = candidate["mechanisms"][4]
        assessment["presence"] = "absent"
        assessment["validation"] = "not-run"
        assessment["evidence_ids"] = []
        assessment["exemption"] = {
            "id": "synthetic-canonical-exemption",
            "scope": "required-absence",
            "owner": "Synthetic site owner",
            "reason": "Compatibility exercise",
            "approved_by": "Synthetic reviewer",
            "approval_evidence_id": "approval-record",
            "approved_on": "2026-09-14",
            "expires_on": "2026-09-15",
        }
        self.refresh_conformance(candidate)
        self.assertEqual("exempt", candidate["summary"]["level"])
        self.assertEqual(1, candidate["summary"]["exemptions"])
        self.assertIn("ARW-EXM-001", [item["code"] for item in candidate["diagnostics"]])
        self.assertEqual([], agent_ready_web.validate_conformance(candidate, self.profile))

    def test_conformance_rejects_authority_inference_and_unbound_evidence(self) -> None:
        authority = copy.deepcopy(self.application_fixture["conformance"])
        authority["authority_assertions"]["structured_metadata_grants_capability"] = True
        self.assertIn(
            "conformance.authority_assertions must deny cross-layer authority inference",
            agent_ready_web.validate_conformance(authority, self.profile),
        )

        unbound = copy.deepcopy(self.application_fixture["conformance"])
        unbound["mechanisms"][4]["evidence_ids"] = ["missing-evidence"]
        self.assertIn(
            "conformance.mechanisms[4].evidence_ids contains unknown evidence ids: "
            "missing-evidence",
            agent_ready_web.validate_conformance(unbound, self.profile),
        )

        future = copy.deepcopy(self.application_fixture["conformance"])
        future["evidence"][0]["observed_at"] = "2026-09-14T16:00:01Z"
        self.assertIn(
            "conformance.evidence[0].observed_at must not follow the assessment",
            agent_ready_web.validate_conformance(future, self.profile),
        )

        not_an_origin = copy.deepcopy(self.application_fixture["conformance"])
        not_an_origin["subject"]["origin"] = "https://example.invalid/path"
        self.assertIn(
            "conformance.subject.origin must be an HTTPS origin",
            agent_ready_web.validate_conformance(not_an_origin, self.profile),
        )

    def test_profile_pin_and_derived_output_cannot_float_or_be_fabricated(self) -> None:
        candidate = copy.deepcopy(self.application_fixture["conformance"])
        candidate["profile"]["pin"]["value"] = "floating-main"
        self.assertIn(
            "conformance.profile.pin.value must equal the resolved immutable revision",
            agent_ready_web.validate_conformance(candidate, self.profile),
        )

        candidate = copy.deepcopy(self.application_fixture["conformance"])
        candidate["profile"]["pin"]["sha256"] = "sha256:" + ("0" * 64)
        self.assertIn(
            "conformance.profile.pin.sha256 must match the loaded canonical profile",
            agent_ready_web.validate_conformance(candidate, self.profile),
        )

        candidate = copy.deepcopy(self.application_fixture["conformance"])
        candidate["profile"]["version"] = "1.0.0-alpha.99"
        self.assertIn(
            "conformance.profile.version must match the loaded profile",
            agent_ready_web.validate_conformance(candidate, self.profile),
        )

        candidate = copy.deepcopy(self.application_fixture["conformance"])
        candidate["profile"]["pin"]["kind"] = "released-version"
        candidate["profile"]["pin"]["value"] = self.profile["version"]
        self.assertIn(
            "conformance.profile.pin.kind released-version requires a non-proposed "
            "profile",
            agent_ready_web.validate_conformance(candidate, self.profile),
        )

        candidate = copy.deepcopy(self.application_fixture["conformance"])
        candidate["summary"]["level"] = "baseline"
        self.assertIn(
            "conformance.summary must equal the deterministic derived summary",
            agent_ready_web.validate_conformance(candidate, self.profile),
        )

    def test_reference_review_covers_the_complete_catalog(self) -> None:
        review = self.profile["reference_review"]
        self.assertEqual(
            agent_ready_web.SCOPED_MECHANISM_IDS,
            review["mechanism_ids"],
        )
        self.assertEqual(agent_ready_web.REFERENCE_REVIEW_CHECKS, review["checks"])
        for mechanism in self.profile["mechanisms"]:
            self.assertIn(
                "primary",
                {
                    reference["authority"]
                    for reference in mechanism["authoritative_references"]
                },
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
        self.assertEqual(
            agent_ready_web.CONSUMER_RESOLUTION_POLICY,
            compatibility["consumer_resolution"],
        )
        self.assertEqual(
            "review-and-compatibility-testing-only",
            compatibility["consumer_resolution"]["proposed_profile_use"],
        )
        candidate = copy.deepcopy(self.profile)
        candidate["compatibility"]["consumer_resolution"]["upgrade"] = (
            "follow-floating-main"
        )
        self.assertIn(
            "profile.compatibility.consumer_resolution is invalid",
            agent_ready_web.validate_profile(candidate),
        )

    def test_ownership_boundary_is_complete_and_does_not_claim_adoption(self) -> None:
        self.assertEqual(agent_ready_web.OWNERS, set(self.profile["ownership"]))
        self.assertIn(
            "Transaction-domain capability",
            self.profile["ownership"]["store"]["owns"],
        )
        self.assertIn(
            "automatic adoption",
            self.profile["ownership"]["pace"]["excludes"],
        )
        self.assertIn(
            "final publication authority",
            self.profile["ownership"]["sites"]["owns"],
        )


if __name__ == "__main__":
    unittest.main()
