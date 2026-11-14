"""Executable synthetic declaration/privacy/freshness controls, not record validation."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("diagnosis", ROOT / "tools/diagnosis.py")
diagnosis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagnosis)
AS_OF = "2026-11-14T00:00:00Z"


class DiagnosisTests(unittest.TestCase):
    def fixture(self, name="public-restricted"):
        return json.loads((ROOT / "fixtures/repository-diagnosis" / (name + ".json")).read_text())

    def test_all_synthetic_examples_validate_without_health_inference(self):
        for path in sorted((ROOT / "fixtures/repository-diagnosis").glob("*.json")):
            with self.subTest(path=path.name):
                result = diagnosis.assess(json.loads(path.read_text()), as_of=AS_OF)
                self.assertEqual("unknown", result["health"])
                self.assertEqual("caller-declared-structural-review-only", result["qualification"])

    def test_all_six_applicability_states_remain_distinct(self):
        for state in diagnosis.STATES:
            value = self.fixture()
            value["applicability"]["state"] = state
            self.assertEqual(state, diagnosis.assess(value, as_of=AS_OF)["applicability"])

    def test_absent_recent_unavailable_and_available_never_mean_healthy(self):
        for state in diagnosis.OBSERVATIONS:
            value = self.fixture()
            value["observation"]["state"] = state
            if state in ("not-collected", "unavailable"):
                value["observation"] = {key: state if key == "state" else None for key in value["observation"]}
            result = diagnosis.assess(value, as_of=AS_OF)
            self.assertEqual(state, result["observation"])
            self.assertEqual("unknown", result["health"])

    def test_public_repository_with_restricted_evidence_defaults_to_no_projection(self):
        self.assertIsNone(diagnosis.public_projection(self.fixture(), as_of=AS_OF))

    def test_nonpublic_payload_excluded_before_inspection_including_invalid_clocks(self):
        for visibility in ("private", "internal", "unknown", None):
            with self.subTest(visibility=visibility):
                self.assertIsNone(diagnosis.public_projection({"visibility": visibility, "secret": object()}, as_of="invalid"))

    def test_public_projection_is_exact_allowlist_not_private_metadata(self):
        result = diagnosis.public_projection(self.fixture("public-summary"), as_of=AS_OF)
        self.assertEqual(set(diagnosis.PUBLIC_FIELDS), set(result))
        for prohibited in ("repository", "records_path", "observation", "reason", "source_digest", "health"):
            self.assertNotIn(prohibited, result)

    def test_no_private_or_unknown_visibility_can_request_public_output(self):
        for visibility in ("private", "internal", "unknown"):
            value = self.fixture("public-summary")
            value["visibility"] = visibility
            with self.subTest(visibility=visibility), self.assertRaises(ValueError):
                diagnosis.validate(value)

    def test_forbidden_metadata_or_truthy_wrong_types_cannot_enter_projection(self):
        for fields in (["filenames"], ["counts"], ["timestamps"], ["reason"], [True], ["freshness", "freshness"]):
            value = self.fixture("public-summary")
            value["privacy"]["public_fields"] = fields
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                diagnosis.validate(value)

    def test_upstream_mutable_revision_schema_copy_or_changed_digest_refused(self):
        for field, replacement in (("revision", "main"), ("schema_sha256", "0" * 64), ("lifecycle", "stable")):
            value = self.fixture()
            value["record_contract"][field] = replacement
            with self.subTest(field=field), self.assertRaises(ValueError):
                diagnosis.validate(value)

    def test_literal_paths_allow_existing_directory_but_refuse_escape_discovery(self):
        for path in ("docs/diagnostics", "docs/Diagnostic Notes", "docs/診断"):
            self.assertEqual(path, diagnosis.safe_path(path))
        for path in ("/private", "../records", "docs/../records", "docs//records", "docs/", "C:/records", "docs\\records", ".GIT/objects", "docs/%2e%2e", "docs/**", "docs/records\n"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                diagnosis.safe_path(path)

    def test_alternative_path_needs_explicit_reason(self):
        value = self.fixture()
        value["records_path"] = "docs/diagnostics"
        with self.assertRaises(ValueError):
            diagnosis.validate(value)
        value["alternative_path_reason"] = "Synthetic explicitly selected bounded legacy directory."
        diagnosis.validate(value)

    def test_observation_age_not_new_index_build_controls_freshness(self):
        value = self.fixture()
        value["observation"]["observed_at"] = "2026-10-01T00:00:00Z"
        value["observation"]["index_generated_at"] = AS_OF
        result = diagnosis.assess(value, as_of=AS_OF)
        self.assertEqual("stale", result["freshness"])
        self.assertIn("INDEX_STALE", result["diagnostics"])

    def test_source_mismatch_is_not_fresh(self):
        value = self.fixture()
        value["observation"]["source_revision"] = "b" * 40
        self.assertEqual("source-mismatch", diagnosis.assess(value, as_of=AS_OF)["freshness"])

    def test_future_clock_invalid_date_or_index_before_observation_refused(self):
        for observed, generated in (("2026-11-15T00:00:00Z", "2026-11-15T01:00:00Z"), ("2026-02-30T00:00:00Z", AS_OF), ("2026-11-13T00:00:00Z", "2026-11-12T00:00:00Z")):
            value = self.fixture()
            value["observation"]["observed_at"] = observed
            value["observation"]["index_generated_at"] = generated
            with self.subTest(observed=observed), self.assertRaises(ValueError):
                diagnosis.assess(value, as_of=AS_OF)

    def test_required_opt_out_remains_visible_review_gap(self):
        value = self.fixture("opted-out")
        value["applicability"]["state"] = "required"
        self.assertEqual(["REQUIRED_ADOPTION_REVIEW"], diagnosis.assess(value, as_of=AS_OF)["diagnostics"])

    def test_declaration_never_causes_consumer_path_reads(self):
        original = Path.read_bytes
        def allowed(path):
            self.assertEqual(ROOT / "catalog/repository-diagnosis-policy.json", path)
            return original(path)
        value = self.fixture()
        with patch.object(Path, "read_bytes", allowed):
            diagnosis.assess(value, as_of=AS_OF)

    def test_closed_envelope_retention_types_and_duplicate_json_fail(self):
        value = self.fixture()
        value["record_body"] = "Not a Hygiene capability field."
        with self.assertRaises(ValueError):
            diagnosis.validate(value)
        for days in (True, 0, -1, "90"):
            value = self.fixture()
            value["retention"]["days"] = days
            with self.subTest(days=days), self.assertRaises(ValueError):
                diagnosis.validate(value)
        for content in (b'{"visibility":"public","visibility":"private"}', b'{"x":NaN}', b'{"x":1e999}', b'[' * 1000 + b'0' + b']' * 1000):
            with self.subTest(content=content[:40]), self.assertRaises((ValueError, RecursionError)):
                diagnosis.parse(content)


if __name__ == "__main__":
    unittest.main()
