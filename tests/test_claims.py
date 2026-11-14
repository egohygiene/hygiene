"""Synthetic provenance qualification, privacy, state and temporal refusal controls."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("claims", ROOT / "tools/claims.py")
claims = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(claims)
AS_OF = "2026-11-14T00:00:00Z"
PUBLIC = ("example/public-fixture",)


class ClaimTests(unittest.TestCase):
    def fixture(self, name="benchmark"):
        return json.loads((ROOT / "fixtures/claims" / (name + ".json")).read_text())

    def test_six_pilot_fixtures_have_actual_bounded_dispositions(self):
        for name, state in (("benchmark", "measured"), ("compatibility", "verified"),
                            ("provider-reported", "provider-reported"), ("estimated", "estimated"),
                            ("stale", "stale"), ("blocked", "blocked")):
            with self.subTest(name=name):
                result = claims.assess(self.fixture(name), as_of=AS_OF)
                self.assertEqual(state, result["effective_state"])
                self.assertEqual(state in ("measured", "verified"), result["positive_evidence_label_eligible"])
                self.assertEqual("provenance-structure-only-not-independent-verification", result["qualification"])

    def test_eleven_states_remain_distinct_and_neutral_states_never_green(self):
        for state in claims.STATES:
            value = self.fixture("compatibility" if state == "verified" else "benchmark")
            value["state"] = state
            result = claims.assess(value, as_of=AS_OF)
            with self.subTest(state=state):
                self.assertEqual(state, result["effective_state"])
                self.assertEqual(state in ("measured", "verified"), result["positive_evidence_label_eligible"])

    def test_missing_provenance_downgrades_strong_claim_without_fabricating_evidence(self):
        for field in ("revision", "digest", "verification-clock", "responsible", "expiry", "runtime", "configuration", "fixture", "evidence"):
            value = self.fixture()
            if field == "revision": value["subject"]["revision"] = None
            elif field == "digest": value["evidence"][0]["sha256"] = None
            elif field == "verification-clock":
                value["verification"]["at"] = None
                value["valid_until"] = None
            elif field == "responsible": value["verification"]["responsible"] = None
            elif field == "expiry": value["valid_until"] = None
            elif field == "runtime": value["environment"]["runtime"]["version"] = "unknown"
            elif field in ("configuration", "fixture"): value["procedure"][field] = None
            else:
                value["evidence"] = []
                value["verification"]["evidence_ids"] = []
            result = claims.assess(value, as_of=AS_OF)
            with self.subTest(field=field):
                self.assertEqual("measured", result["declared_state"])
                self.assertEqual("unverified", result["effective_state"])
                self.assertFalse(result["positive_evidence_label_eligible"])
                self.assertIn("PROVENANCE_INCOMPLETE", result["diagnostics"])

    def test_no_verified_benchmark_by_renaming_measurement(self):
        value = self.fixture()
        value["state"] = "verified"
        with self.assertRaises(ValueError):
            claims.assess(value, as_of=AS_OF)

    def test_unknown_subject_method_material_version_and_empty_command_cannot_qualify(self):
        for field in ("component", "method", "configuration", "dependency", "command"):
            value = self.fixture()
            if field == "component": value["subject"]["component"] = "unknown"
            elif field == "method": value["procedure"]["id"] = "unknown"
            elif field == "configuration": value["procedure"]["configuration"]["version"] = "unknown"
            elif field == "dependency": value["environment"]["dependencies"][0]["version"] = "unknown"
            else: value["procedure"]["command"] = []
            with self.subTest(field=field):
                self.assertEqual("unverified", claims.assess(value, as_of=AS_OF)["effective_state"])

    def test_wrong_verification_method_cannot_upgrade_provider_or_estimate(self):
        for name in ("provider-reported", "estimated"):
            value = self.fixture(name)
            value["state"] = "measured"
            self.assertEqual("unverified", claims.assess(value, as_of=AS_OF)["effective_state"])

    def version_field(self, value, field, version):
        if field == "runtime": value["environment"]["runtime"]["version"] = version
        elif field == "dependency": value["environment"]["dependencies"][0]["version"] = version
        elif field == "procedure": value["procedure"]["version"] = version
        elif field in ("tag", "released_version"): value["subject"][field] = version
        else:
            value["procedure"][field] = {"id": "fixture-" + field, "version": version, "sha256": "f" * 64}

    def test_case_insensitive_unknown_material_versions_never_qualify(self):
        for version in ("unknown", "UNKNOWN", "UnKnOwN", "unavailable", "UNAVAILABLE", "Unspecified", "NOT-RECORDED", "NOT-COLLECTED"):
            for field in ("runtime", "dependency", "procedure", "configuration", "fixture", "task", "dataset", "tag", "released_version"):
                value = self.fixture()
                self.version_field(value, field, version)
                result = claims.assess(value, as_of=AS_OF)
                with self.subTest(version=version, field=field):
                    self.assertEqual("unverified", result["effective_state"])
                    self.assertFalse(result["positive_evidence_label_eligible"])

    def test_mutable_channels_refused_case_insensitively_in_every_version_field(self):
        for channel in sorted(claims.MUTABLE_CHANNELS):
            for version in (channel, channel.upper(), channel.title()):
                for field in ("runtime", "dependency", "procedure", "configuration", "fixture", "task", "dataset", "tag", "released_version"):
                    value = self.fixture()
                    self.version_field(value, field, version)
                    with self.subTest(version=version, field=field), self.assertRaises(ValueError):
                        claims.assess(value, as_of=AS_OF)

    def test_immutable_release_prerelease_build_and_digest_versions_stay_supported(self):
        for version in ("1.2.3", "v1.2.3", "1.2.3-alpha.1+build.7", "a" * 40):
            for field in ("runtime", "dependency", "procedure", "configuration", "fixture", "task", "dataset", "tag", "released_version"):
                value = self.fixture()
                self.version_field(value, field, version)
                with self.subTest(version=version, field=field):
                    self.assertEqual("measured", claims.assess(value, as_of=AS_OF)["effective_state"])

    def test_freshness_boundary_and_original_state_preserved(self):
        value = self.fixture("compatibility")
        self.assertEqual("verified", claims.assess(value, as_of="2026-11-30T23:59:59Z")["effective_state"])
        result = claims.assess(value, as_of=value["valid_until"])
        self.assertEqual("stale", result["effective_state"])
        self.assertEqual("verified", result["declared_state"])
        self.assertIn("EXPIRED", result["diagnostics"])
        self.assertEqual("2026-11-13T01:00:00Z", value["verification"]["at"])

    def test_raw_retention_expiry_limits_otherwise_current_evidence(self):
        value = self.fixture()
        value["evidence"][0]["retained_until"] = AS_OF
        result = claims.assess(value, as_of=AS_OF)
        self.assertEqual("stale", result["effective_state"])
        self.assertIn("EVIDENCE_RETENTION_EXPIRED", result["diagnostics"])

    def test_supersession_does_not_delete_history_or_self_reference(self):
        value = self.fixture()
        value["superseded_by"] = "benchmark.successor"
        self.assertEqual("stale", claims.assess(value, as_of=AS_OF)["effective_state"])
        self.assertEqual("measured", value["state"])
        value["superseded_by"] = value["id"]
        with self.assertRaises(ValueError): claims.validate(value)

    def test_future_inverted_or_invalid_dates_refused(self):
        for change in ("future-verification", "future-capture", "capture-after-verification", "retention-before-capture", "invalid-date", "expiry-before-verification"):
            value = self.fixture()
            if change == "future-verification": value["verification"]["at"] = "2026-11-15T00:00:00Z"
            elif change == "future-capture": value["evidence"][0]["captured_at"] = "2026-11-15T00:00:00Z"
            elif change == "capture-after-verification": value["evidence"][0]["captured_at"] = "2026-11-13T02:00:00Z"
            elif change == "retention-before-capture": value["evidence"][0]["retained_until"] = "2026-11-12T00:00:00Z"
            elif change == "invalid-date": value["verification"]["at"] = "2026-02-30T00:00:00Z"
            else: value["valid_until"] = "2026-11-13T00:00:00Z"
            with self.subTest(change=change), self.assertRaises(ValueError): claims.assess(value, as_of=AS_OF)

    def test_unknown_visibility_and_unadmitted_repositories_excluded_before_payload(self):
        for visibility in ("restricted", "internal", "unknown", None):
            self.assertIsNone(claims.project_public({"visibility": visibility, "private": object()}, as_of="invalid", public_repositories=PUBLIC))
        value = self.fixture()
        self.assertIsNone(claims.project_public(value, as_of=AS_OF))
        value["subject"]["repository"] = "example/unadmitted"
        self.assertIsNone(claims.project_public(value, as_of="invalid", public_repositories=PUBLIC))

    def test_public_projection_does_not_echo_untrusted_prose_command_or_private_location(self):
        value = self.fixture()
        value["statement"] = "UNTRUSTED-STATEMENT"
        value["procedure"]["command"] = ["UNTRUSTED-COMMAND"]
        value["limitations"] = ["UNTRUSTED-LIMITATION"]
        result = claims.project_public(value, as_of=AS_OF, public_repositories=PUBLIC)
        serialized = json.dumps(result)
        for field in ("UNTRUSTED-STATEMENT", "UNTRUSTED-COMMAND", "UNTRUSTED-LIMITATION"):
            self.assertNotIn(field, serialized)
        self.assertEqual(["evidence:synthetic-benchmark-raw"], result["evidence_references"])

    def test_human_projection_links_raw_or_safe_evidence_with_current_qualifier(self):
        for name in ("benchmark", "provider-reported", "stale", "blocked"):
            value = self.fixture(name)
            rendered = claims.render_public(value, as_of=AS_OF, public_repositories=PUBLIC)
            self.assertIn("**" + claims.assess(value, as_of=AS_OF)["effective_state"] + "**", rendered)
            self.assertIn(value["subject"]["revision"], rendered)
            for evidence in value["evidence"]: self.assertIn(evidence["reference"]["locator"], rendered)
        rendered = claims.render_public(self.fixture("provider-reported"), as_of=AS_OF, public_repositories=PUBLIC)
        self.assertIn("](https://github.com/egohygiene/hygiene/issues/30)", rendered)

    def test_restricted_evidence_has_only_opaque_handles(self):
        for locator in ("/private/logs", "https://internal.example/evidence", "evidence:private title", "file:///tmp/logs"):
            value = self.fixture()
            value["evidence"][0]["reference"]["locator"] = locator
            with self.subTest(locator=locator), self.assertRaises(ValueError): claims.validate(value)

    def test_public_evidence_rejects_credentials_queries_fragments_and_markdown_injection(self):
        for locator in ("http://example.com/a", "https://user@example.com/a", "https://example.com/a?token=secret", "https://example.com/a#secret", "https://example.com/a%20b", "https://example.com/[x]", "https://example.com/(x)"):
            value = self.fixture("provider-reported")
            value["evidence"][0]["reference"]["locator"] = locator
            with self.subTest(locator=locator), self.assertRaises(ValueError): claims.validate(value)

    def test_duplicate_dangling_evidence_and_ambiguous_json_refused(self):
        value = self.fixture()
        value["evidence"].append(copy.deepcopy(value["evidence"][0]))
        with self.assertRaises(ValueError): claims.validate(value)
        value = self.fixture()
        value["verification"]["evidence_ids"] = ["missing"]
        with self.assertRaises(ValueError): claims.validate(value)
        for raw in (b'{"state":"measured","state":"blocked"}', b'{"x":NaN}', b'{"x":1e999}', b'[' * 1000 + b'0' + b']' * 1000):
            with self.subTest(raw=raw[:40]), self.assertRaises((ValueError, RecursionError)): claims.parse(raw)

    def test_boolean_nonfinite_numbers_counts_and_mutable_versions_refused(self):
        for field, replacement in (("sample_count", True), ("sample_count", 0), ("value", True), ("value", float("inf")), ("value", 10**1000)):
            value = self.fixture()
            value["measurement"][field] = replacement
            with self.subTest(field=field), self.assertRaises(ValueError): claims.validate(value)
        for version in ("main", "latest", "^1.0.0", "1.*", "HEAD"):
            value = self.fixture()
            value["environment"]["runtime"]["version"] = version
            with self.subTest(version=version), self.assertRaises(ValueError): claims.validate(value)

    def test_proposed_policy_composes_real_local_owner_bytes_and_all_state_rules(self):
        policy = json.loads((ROOT / "catalog/claim-provenance-policy.json").read_text())
        self.assertEqual("proposed", policy["status"])
        self.assertIsNone(policy["approval"])
        self.assertEqual("observe", policy["enforcement"])
        self.assertEqual(list(claims.STATES), policy["states"])
        for item in policy["composes"]:
            if item["repository"] == "egohygiene/hygiene" and "path" in item:
                self.assertEqual(item["sha256"], hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest())
        self.assertEqual(set(claims.STATES), {row["state"] for row in policy["presentation"]})
        self.assertEqual(sorted(claims.MUTABLE_CHANNELS), policy["version_admission"]["mutable_channels_refused"])
        self.assertEqual(sorted(claims.UNKNOWN_VALUES), policy["version_admission"]["unknown_values_never_strong"])


if __name__ == "__main__":
    unittest.main()
