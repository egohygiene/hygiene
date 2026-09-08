from __future__ import annotations

import copy
import json
import sys
import tomllib
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import continuity  # noqa: E402


class RepositoryContinuityPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = continuity.load_json(
            ROOT / "catalog" / "repository-continuity-policy.json"
        )

    def test_policy_schema_is_a_json_schema_document(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository-continuity-policy.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
        self.assertEqual(
            "https://egohygiene.io/schemas/hygiene/repository-continuity-policy.v1.schema.json",
            schema["$id"],
        )

    def test_checked_in_profile_is_valid_and_truthful_about_upstream(self) -> None:
        self.assertEqual([], continuity.validate_profile(self.profile))
        upstream = self.profile["upstream"]
        self.assertEqual(continuity.AETHER_REVISION, upstream["revision"])
        self.assertEqual("draft", upstream["lifecycle"])
        self.assertFalse(upstream["release_included"])
        self.assertEqual("observe", self.profile["rollout"]["current_stage"])

    def test_upstream_artifacts_are_immutable_without_a_local_protocol_fork(self) -> None:
        artifacts = {item["id"]: item for item in self.profile["upstream"]["artifacts"]}
        self.assertEqual(set(continuity.EXPECTED_UPSTREAM_ARTIFACTS), set(artifacts))
        for artifact in artifacts.values():
            self.assertRegex(artifact["sha256_utf8_lf"], r"^[0-9a-f]{64}$")
            self.assertNotIn("/main/", artifact["path"])
        self.assertEqual(
            [],
            list(ROOT.rglob("aether.repository-continuity.v1.schema.json")),
            "Hygiene must reference, not vendor, Aether's continuity schema",
        )

    def test_mutable_or_wrong_upstream_pin_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.profile)
        candidate["upstream"]["revision"] = "a" * 40
        self.assertIn(
            "profile.upstream.revision must pin the Aether #80 merge commit",
            continuity.validate_profile(candidate),
        )

    def test_initial_scope_names_all_29_active_repositories_without_exceptions(self) -> None:
        initial = self.profile["applicability"]["initial_scope"]
        self.assertEqual(29, initial["active_repository_count"])
        self.assertEqual(continuity.INITIAL_REPOSITORIES, set(initial["repositories"]))
        self.assertEqual([], self.profile["exceptions"]["records"])

    def test_applicability_covers_lifecycle_kind_and_visibility(self) -> None:
        required = continuity.resolve_applicability(
            self.profile, "egohygiene/hygiene", "active", "standard", "public"
        )
        self.assertEqual("required", required["requirement"])
        private = continuity.resolve_applicability(
            self.profile, "egohygiene/egohygiene", "active", "standard", "private"
        )
        self.assertEqual("required", private["requirement"])
        dormant = continuity.resolve_applicability(
            self.profile, "egohygiene/example", "dormant", "standard", "public"
        )
        self.assertEqual("advisory", dormant["requirement"])
        archived = continuity.resolve_applicability(
            self.profile, "egohygiene/example", "archived", "standard", "public"
        )
        self.assertEqual("not-applicable", archived["requirement"])
        mirror = continuity.resolve_applicability(
            self.profile, "egohygiene/example", "active", "mirror", "public"
        )
        self.assertEqual("not-applicable", mirror["requirement"])
        generated = continuity.resolve_applicability(
            self.profile, "egohygiene/example", "active", "generated-only", "internal"
        )
        self.assertEqual("advisory", generated["requirement"])
        template = continuity.resolve_applicability(
            self.profile, "egohygiene/example", "active", "template", "public"
        )
        self.assertEqual("required", template["requirement"])

    def test_only_reviewed_unexpired_exception_changes_applicability(self) -> None:
        candidate = copy.deepcopy(self.profile)
        candidate["exceptions"]["records"] = [
            {
                "repository": "egohygiene/hygiene",
                "owner": "egohygiene/hygiene",
                "reason": "Bounded migration dependency is unavailable.",
                "approval": "https://github.com/egohygiene/hygiene/issues/45#issuecomment-1",
                "expires_on": "2026-12-31",
                "review_trigger": "Recheck when the dependency publishes a stable release.",
                "validation_state": "approved",
                "exit_criteria": "Adopt the pinned stable contract and remove this record.",
            }
        ]
        self.assertEqual([], continuity.validate_profile(candidate))
        resolved = continuity.resolve_applicability(
            candidate,
            "egohygiene/hygiene",
            "active",
            "standard",
            "public",
            as_of=date(2026, 9, 8),
        )
        self.assertEqual("exempt", resolved["requirement"])
        self.assertIsNotNone(resolved["exception"])

    def test_approved_expired_exception_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.profile)
        candidate["exceptions"]["records"] = [
            {
                "repository": "egohygiene/hygiene",
                "owner": "egohygiene/hygiene",
                "reason": "Expired migration window.",
                "approval": "https://github.com/egohygiene/hygiene/issues/45#issuecomment-1",
                "expires_on": "2026-09-08",
                "review_trigger": "Expiry date reached.",
                "validation_state": "approved",
                "exit_criteria": "Remove the exception.",
            }
        ]
        self.assertIn(
            "profile.exceptions.records[0] approved exception is already expired",
            continuity.validate_profile(candidate),
        )

    def test_rollout_order_and_rollback_are_explicit(self) -> None:
        stages = self.profile["rollout"]["stages"]
        self.assertEqual(["observe", "ratchet", "enforce"], [item["id"] for item in stages])
        self.assertEqual(
            ["visible-non-blocking", "block-new-regressions", "block-nonconformance"],
            [item["finding_behavior"] for item in stages],
        )
        self.assertTrue(all(item["rollback"] for item in stages))

    def test_precedence_and_information_safety_are_normative(self) -> None:
        self.assertEqual(continuity.SOURCE_PRECEDENCE, self.profile["source_precedence"])
        safety = self.profile["information_safety"]
        self.assertTrue(safety["minimum_necessary"])
        self.assertTrue(safety["git_history_owns_chronology"])
        self.assertIn("private-conversation-text", safety["public_excluded"])
        self.assertIn("credentials-and-secrets", safety["public_excluded"])
        self.assertIn("exclude-credentials-and-secrets", safety["private_rules"])

    def test_breaking_context_successor_preserves_v1_artifact(self) -> None:
        compatibility = self.profile["compatibility"]
        self.assertEqual("breaking", compatibility["impact"])
        self.assertEqual("1.0.0", compatibility["previous_contract"]["version"])
        self.assertEqual("deprecated", compatibility["previous_contract"]["status"])
        self.assertEqual("2.0.0", compatibility["successor_contract"]["version"])
        self.assertTrue((ROOT / compatibility["previous_contract"]["artifact"]).is_file())
        self.assertTrue((ROOT / compatibility["successor_contract"]["artifact"]).is_file())

    def test_context_v2_contract_uses_correct_file_ownership(self) -> None:
        contract = tomllib.loads(
            (ROOT / "contracts" / "repository-context.toml").read_text(encoding="utf-8")
        )
        requirements = {item["id"]: item for item in contract["requirements"]}
        self.assertEqual("2.0.0", contract["version"])
        self.assertTrue(contract["provisional"])
        self.assertEqual("repository-owned", requirements["agent-instructions"]["ownership"])
        self.assertEqual("repository-owned", requirements["continuity-checkpoint"]["ownership"])
        self.assertEqual("generated", requirements["ecosystem-context"]["ownership"])

    def test_contract_catalog_and_downstream_boundaries_are_complete(self) -> None:
        contracts = continuity.load_json(ROOT / "catalog" / "contracts.yaml")["contracts"]
        registered = {item["id"]: item for item in contracts}
        self.assertEqual("deprecated", registered["egohygiene.repository-context/v1"]["status"])
        self.assertEqual("proposed", registered["egohygiene.repository-context/v2"]["status"])
        self.assertEqual("proposed", registered[continuity.POLICY_SCHEMA]["status"])
        downstream = {item["repository"]: item["issue"] for item in self.profile["downstream"]}
        self.assertEqual(continuity.DOWNSTREAM_ISSUES, downstream)

    def test_hygiene_dogfood_files_and_managed_block_are_valid(self) -> None:
        self.assertEqual([], continuity.validate_repository(ROOT, self.profile))
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(1, agents.count("<!-- BEGIN AETHER REPOSITORY-CONTINUITY -->"))
        self.assertIn("Before architecture-changing work", agents)
        checkpoint = (ROOT / "CONTINUITY.md").read_text(encoding="utf-8")
        self.assertNotIn("This template is intentionally invalid", checkpoint)
        self.assertLessEqual(len(checkpoint.encode("utf-8")), 16_384)
        self.assertLessEqual(len(checkpoint.splitlines()), 240)


if __name__ == "__main__":
    unittest.main()
