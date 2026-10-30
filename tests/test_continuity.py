from __future__ import annotations

import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

import tomllib

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


class ContinuityAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = continuity.load_json(
            ROOT / "catalog/repository-continuity-policy.json"
        )
        cls.fixture = continuity.load_json(
            ROOT / "fixtures/repository-continuity/expiry-assessments.json"
        )

    def sample(self) -> dict:
        value = copy.deepcopy(self.profile)
        self.assertEqual(self.fixture["profile_updated"], value["updated"])
        value["exceptions"]["records"] = [copy.deepcopy(self.fixture["exception"])]
        return value

    def resolve(self, profile: dict, **options) -> dict:
        return continuity.resolve_applicability(
            profile, "egohygiene/hygiene", "active", "standard", "public", **options
        )

    def cli(
        self, profile: dict, assessment_date: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text(json.dumps(profile), encoding="utf-8")
            before = path.read_bytes()
            arguments = [
                sys.executable,
                "-I",
                str(ROOT / "tools/continuity.py"),
                "--profile",
                str(path),
                "resolve",
                "--repository",
                "egohygiene/hygiene",
                "--lifecycle",
                "active",
                "--repository-kind",
                "standard",
                "--visibility",
                "public",
            ]
            if assessment_date is not None:
                arguments.extend(["--assessment-date", assessment_date])
            result = subprocess.run(
                arguments,
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            self.assertEqual(before, path.read_bytes())
            return result

    def test_fixed_before_at_after_expiry_and_visible_date(self) -> None:
        sample = self.sample()
        before = copy.deepcopy(sample)
        for case in self.fixture["cases"]:
            with self.subTest(date=case["assessment_date"]):
                actual = self.resolve(
                    sample, as_of=date.fromisoformat(case["assessment_date"])
                )
                self.assertEqual(case["requirement"], actual["requirement"])
                self.assertEqual(case["reason"], actual["reason"])
                self.assertEqual(case["assessment_date"], actual["assessment_date"])
                self.assertEqual("explicit", actual["assessment_mode"])
                if case["requirement"] != "exempt":
                    self.assertIsNone(actual["exception"])
        self.assertEqual(before, sample)

    def test_default_uses_current_utc_not_the_profile_update_date(self) -> None:
        with mock.patch.object(continuity, "datetime", create=True) as clock:
            clock.now.return_value = datetime(2026, 10, 20, 18, tzinfo=timezone.utc)
            actual = self.resolve(self.sample())
        self.assertEqual("required", actual["requirement"])
        self.assertEqual("2026-10-20", actual["assessment_date"])
        self.assertEqual("current-utc", actual["assessment_mode"])

    def test_actual_cli_matches_frozen_api_and_repeats_exactly(self) -> None:
        for case in self.fixture["cases"]:
            with self.subTest(date=case["assessment_date"]):
                expected = self.resolve(
                    self.sample(), as_of=date.fromisoformat(case["assessment_date"])
                )
                first = self.cli(self.sample(), case["assessment_date"])
                second = self.cli(self.sample(), case["assessment_date"])
                self.assertEqual(0, first.returncode, first.stderr)
                self.assertEqual(0, second.returncode, second.stderr)
                self.assertEqual(expected, json.loads(first.stdout))
                self.assertEqual(first.stdout, second.stdout)

    def test_actual_default_cli_discloses_current_utc_assessment(self) -> None:
        before = datetime.now(timezone.utc).date()
        result = self.cli(self.sample())
        after = datetime.now(timezone.utc).date()
        self.assertEqual(0, result.returncode, result.stderr)
        actual = json.loads(result.stdout)
        self.assertIn(
            actual["assessment_date"], {before.isoformat(), after.isoformat()}
        )
        self.assertEqual("current-utc", actual["assessment_mode"])
        effective = date.fromisoformat(actual["assessment_date"])
        expected = (
            "exempt"
            if effective < date.fromisoformat(self.fixture["exception"]["expires_on"])
            else "required"
        )
        self.assertEqual(expected, actual["requirement"])

    def test_invalid_api_dates_never_fall_back_to_a_historical_clock(self) -> None:
        for invalid in (
            False,
            0,
            "2026-09-30",
            datetime(2026, 9, 30, tzinfo=timezone.utc),
            {},
            [],
        ):
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                self.resolve(self.sample(), as_of=invalid)

    def test_invalid_cli_dates_have_controlled_attributable_errors(self) -> None:
        for invalid in (
            "20261001",
            "2026-W40-4",
            "2026-1-01",
            "2026-02-30",
            "0000-01-01",
            "2026-10-01\n",
            "",
        ):
            with self.subTest(value=invalid):
                result = self.cli(self.sample(), invalid)
                self.assertEqual(2, result.returncode)
                self.assertIn("assessment date must be YYYY-MM-DD", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_unapproved_or_invalid_records_never_gain_exemption(self) -> None:
        for state in ("proposed", "expired", "revoked"):
            with self.subTest(state=state):
                sample = self.sample()
                sample["exceptions"]["records"][0]["validation_state"] = state
                self.assertEqual(
                    "required",
                    self.resolve(sample, as_of=date(2026, 9, 30))["requirement"],
                )
        for field, value in (
            ("validation_state", "unsupported"),
            ("approval", None),
            ("expires_on", "20261001"),
        ):
            with self.subTest(field=field), self.assertRaises(ValueError):
                sample = self.sample()
                sample["exceptions"]["records"][0][field] = value
                self.resolve(sample, as_of=date(2026, 9, 30))

    def test_missing_clock_fails_and_explicit_date_still_works(self) -> None:
        with mock.patch.object(continuity, "datetime", create=True) as clock:
            clock.now.side_effect = OSError("synthetic unavailable clock")
            with self.assertRaisesRegex(
                ValueError, "current UTC assessment date is unavailable"
            ):
                self.resolve(self.sample())
            actual = self.resolve(self.sample(), as_of=date(2026, 9, 30))
        self.assertEqual("exempt", actual["requirement"])
        self.assertEqual("2026-09-30", actual["assessment_date"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text(json.dumps(self.sample()), encoding="utf-8")
            errors = io.StringIO()
            with mock.patch.object(continuity, "datetime", create=True) as clock:
                clock.now.side_effect = OSError("synthetic unavailable clock")
                with redirect_stderr(errors):
                    status = continuity.main(
                        [
                            "--profile",
                            str(path),
                            "resolve",
                            "--repository",
                            "egohygiene/hygiene",
                            "--lifecycle",
                            "active",
                            "--repository-kind",
                            "standard",
                            "--visibility",
                            "public",
                        ]
                    )
            self.assertEqual(2, status)
            self.assertIn(
                "current UTC assessment date is unavailable", errors.getvalue()
            )
            self.assertNotIn("Traceback", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
