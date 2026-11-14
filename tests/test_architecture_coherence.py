"""Qualify existing policy/reference bytes; no live human approval is created."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import architecture_coherence as coherence


class ArchitectureCoherenceTests(unittest.TestCase):
    def setUp(self):
        directory = ROOT / "fixtures/architecture-coherence"
        self.base = json.loads((directory / "governance.valid.json").read_text())
        self.change = json.loads((directory / "material-change.valid.json").read_text())
        self.cases = json.loads((directory / "examples.json").read_text())["cases"]
        self.roster = ["egohygiene/hygiene", "egohygiene/aether"]
        self.context = dict(as_of="2026-11-14T12:00:00Z", public_repositories=self.roster,
                            change_inventory="complete", availability="present")

    def evidence(self, source=None, kind="decision"):
        # This is trusted TEST CODE over explicitly synthetic data. Production
        # JSON cannot construct this context and no human source is contacted.
        statement = coherence.human_statement(source or self.base, kind=kind, public_repositories=self.roster)
        return coherence.TrustedHumanEvidence(coherence.statement_sha256(statement), "d" * 64)

    def test_all_eighteen_cases_match_independently_declared_expected_states(self):
        self.assertEqual(18, len(self.cases))
        self.assertEqual(18, len({case["id"] for case in self.cases}))
        for case in self.cases:
            with self.subTest(case=case["id"]):
                evidence = [self.evidence(case["governance"], kind) for kind in case["synthetic_trust_kinds"]]
                source = copy.deepcopy(case["governance"])
                result = coherence.evaluate(source, **case["context"], trusted_human_evidence=evidence)
                self.assertEqual(case["expected"], {key: result[key] for key in case["expected"]})
                self.assertEqual(source, case["governance"])
                self.assertEqual(result, coherence.evaluate(source, **case["context"], trusted_human_evidence=evidence))
                self.assertNotIn("d" * 64, json.dumps(result))

    def test_raw_json_actor_or_digest_fields_cannot_supply_human_trust(self):
        forged = {"statement_sha256": self.evidence().statement_sha256, "capture_sha256": "d" * 64}
        result = coherence.evaluate(self.base, **self.context, trusted_human_evidence=[forged])
        self.assertIsNone(result["human_disposition"])
        self.assertEqual("unverified", result["human_evidence"])
        for mutation in ("scope", "assessment", "revision", "expiry", "notes"):
            source = copy.deepcopy(self.base)
            if mutation == "scope":
                source["scope"].update(kind="subsystem", key="egohygiene/hygiene:synthetic")
                source["human_decision"]["scope_key"] = source["scope"]["key"]
            elif mutation == "assessment":
                source["review_ref"]["assessment_sha256"] = "c" * 64
                source["human_decision"]["assessment_sha256"] = "c" * 64
            elif mutation == "revision":
                source["represented_revisions"][0]["revision"] = "c" * 40
                source["human_decision"]["represented_revisions"][0]["revision"] = "c" * 40
            elif mutation == "expiry": source["valid_until"] = "2026-12-01T00:00:00Z"
            else: source["human_decision"]["notes"] = ["Synthetic changed caveat"]
            with self.subTest(mutation=mutation):
                result = coherence.evaluate(source, **self.context, trusted_human_evidence=[self.evidence()])
                self.assertIsNone(result["human_disposition"])

    def test_typed_test_context_is_immutable_and_capture_is_never_emitted(self):
        evidence = self.evidence()
        with self.assertRaises(AttributeError): evidence.statement_sha256 = "0" * 64
        result = coherence.evaluate(self.base, **self.context, trusted_human_evidence=[evidence])
        self.assertEqual("ratified", result["state"])
        self.assertNotIn("capture", json.dumps(result))

    def test_all_dispositions_preserve_source_claim_versus_synthetic_verified_state(self):
        for disposition in coherence.DISPOSITIONS:
            source = copy.deepcopy(self.base)
            source["human_decision"]["disposition"] = disposition
            if disposition == "ratified-with-notes": source["human_decision"]["notes"] = ["Synthetic caveat"]
            unverified = coherence.evaluate(source, **self.context)
            self.assertIsNone(unverified["human_disposition"])
            verified = coherence.evaluate(source, **self.context, trusted_human_evidence=[self.evidence(source)])
            self.assertEqual(disposition, verified["human_disposition"])
            self.assertEqual(disposition, verified["state"])

    def test_source_binding_errors_and_incomplete_reviews_fail(self):
        for field in ("review_id", "assessment_sha256", "scope_key", "represented_revisions"):
            source = copy.deepcopy(self.base)
            source["human_decision"][field] = [] if field == "represented_revisions" else "different"
            with self.subTest(field=field), self.assertRaises(coherence.CoherenceError):
                coherence.admit_governance(source, public_repositories=self.roster)
        source = copy.deepcopy(self.base); source["progress"] = "in-progress"
        with self.assertRaises(coherence.CoherenceError): coherence.admit_governance(source, public_repositories=self.roster)

    def test_each_explicit_material_trigger_stales_without_rewriting_ratification(self):
        for kind in set(coherence.MATERIAL_KINDS) - {"explicit-human-invalidation"}:
            change = copy.deepcopy(self.change); change["kind"] = kind
            result = coherence.evaluate(self.base, **self.context, material_changes=[change],
                                         trusted_human_evidence=[self.evidence()])
            self.assertEqual(("stale", "ratified"), (result["state"], result["human_disposition"]))
            self.assertEqual("ratified", self.base["human_decision"]["disposition"])

    def test_routine_revision_difference_is_not_a_material_trigger(self):
        change = copy.deepcopy(self.change); change["kind"] = "routine-implementation"
        result = coherence.evaluate(self.base, **self.context, material_changes=[change],
            current_revisions=[dict(repository="egohygiene/hygiene", revision="c" * 40)],
            trusted_human_evidence=[self.evidence()])
        self.assertEqual(("ratified", "current", "different"), (result["state"], result["freshness"], result["revision_match"]))

    def test_invalidation_needs_its_own_exact_synthetic_human_context(self):
        change = copy.deepcopy(self.change)
        change.update(kind="explicit-human-invalidation", authority=copy.deepcopy(self.base["human_decision"]["authority"]))
        result = coherence.evaluate(self.base, **self.context, material_changes=[change],
                                     trusted_human_evidence=[self.evidence()])
        self.assertEqual("unknown", result["freshness"])
        self.assertEqual([change["id"]], result["unverified_change_ids"])
        subject = coherence.material_change_statement(change, public_repositories=self.roster)
        evidence = coherence.TrustedHumanEvidence(coherence.statement_sha256(subject), "e" * 64)
        result = coherence.evaluate(self.base, **self.context, material_changes=[change],
                                     trusted_human_evidence=[self.evidence(), evidence])
        self.assertEqual("stale", result["state"])

    def test_partial_unknown_or_unavailable_inventory_never_establishes_freshness(self):
        for inventory in ("partial", "unknown", "unavailable"):
            context = {**self.context, "change_inventory": inventory}
            result = coherence.evaluate(self.base, **context, trusted_human_evidence=[self.evidence()])
            self.assertEqual(("unavailable", "unknown", "ratified"),
                             (result["state"], result["freshness"], result["human_disposition"]))
            result = coherence.evaluate(self.base, **context, material_changes=[self.change],
                                         trusted_human_evidence=[self.evidence()])
            self.assertEqual("stale", result["state"])

    def test_expiry_boundary_future_source_and_calendar_refusals(self):
        source = copy.deepcopy(self.base); source["valid_until"] = self.context["as_of"]
        current = coherence.evaluate(source, **self.context, trusted_human_evidence=[self.evidence(source)])
        self.assertEqual("current", current["freshness"])
        expired = coherence.evaluate(source, **{**self.context, "as_of": "2026-11-14T12:00:01Z"},
                                      trusted_human_evidence=[self.evidence(source)])
        self.assertEqual("stale", expired["state"])
        for invalid in ("2026-02-30T12:00:00Z", "2026-11-14T12:00:00+00:00", "2026-11-14T12:00:00"):
            with self.assertRaises(coherence.CoherenceError): coherence.evaluate(self.base, **{**self.context, "as_of": invalid})
        future = copy.deepcopy(self.change); future["observed_at"] = "2026-12-01T00:00:00Z"
        with self.assertRaises(coherence.CoherenceError): coherence.evaluate(self.base, **self.context, material_changes=[future])

    def test_deferral_expires_and_material_event_invalidates_exception(self):
        source = next(case["governance"] for case in self.cases if case["id"] == "deferred-synthetic-trusted")
        evidence = self.evidence(source, "applicability")
        expired = coherence.evaluate(source, **{**self.context, "as_of": "2026-12-02T00:00:00Z"}, trusted_human_evidence=[evidence])
        self.assertEqual("review-due", expired["state"])
        change = copy.deepcopy(self.change); change["review_id"] = None
        result = coherence.evaluate(source, **self.context, material_changes=[change], trusted_human_evidence=[evidence])
        self.assertEqual(("review-due", "unknown", "deferred"),
                         (result["state"], result["applicability"], result["claimed_applicability"]))

    def test_before_assessment_and_unrelated_events_are_not_reinterpreted(self):
        change = copy.deepcopy(self.change); change["observed_at"] = "2026-10-01T00:00:00Z"
        result = coherence.evaluate(self.base, **self.context, material_changes=[change], trusted_human_evidence=[self.evidence()])
        self.assertEqual("current", result["freshness"])
        change["review_id"] = "OTHER-SYNTHETIC-REVIEW"
        change["private_untrusted_payload"] = object()
        result = coherence.evaluate(self.base, **self.context, material_changes=[change], trusted_human_evidence=[self.evidence()])
        self.assertEqual([], result["material_change_ids"])

    def test_public_admission_precedes_payload_validation_and_no_topology_escapes(self):
        for mutation in ("visibility", "member"):
            source = copy.deepcopy(self.base)
            source["private_untrusted_payload"] = object()
            if mutation == "visibility": source["visibility"] = "private"
            else: source["scope"]["repositories"].append("egohygiene/synthetic-protected")
            self.assertIsNone(coherence.admit_governance(source, public_repositories=self.roster))
            result = coherence.evaluate(source, **{**self.context, "availability": "missing"})
            self.assertEqual("unavailable", result["state"])
            self.assertNotIn("synthetic-protected", json.dumps(result))
            self.assertNotIn("count", json.dumps(result))

    def test_public_payload_sensitive_prose_and_unsafe_urls_fail_with_closed_diagnostics(self):
        for value in ("/workspace/synthetic-private/file", "synthetic@example.invalid", "password=synthetic-only"):
            source = copy.deepcopy(self.base); source["human_decision"]["notes"] = [value]
            with self.assertRaises(coherence.CoherenceError) as failure:
                coherence.admit_governance(source, public_repositories=self.roster)
            self.assertNotIn(value, str(failure.exception))
        for value in ("http://github.com/egohygiene/hygiene/issues/1", "https://github.com/egohygiene/hygiene/../aether",
                      "https://github.com/egohygiene/hygiene/issues/1?token=synthetic", "https://github.com/egohygiene/synthetic-protected/issues/1"):
            source = copy.deepcopy(self.base); source["applicability"]["evidence"] = [value]
            with self.assertRaises(coherence.CoherenceError): coherence.admit_governance(source, public_repositories=self.roster)

    def test_duplicate_selected_events_and_invalid_scope_revisions_fail(self):
        with self.assertRaises(coherence.CoherenceError):
            coherence.evaluate(self.base, **self.context, material_changes=[self.change, self.change])
        source = copy.deepcopy(self.base)
        source["represented_revisions"].append(copy.deepcopy(source["represented_revisions"][0]))
        with self.assertRaises(coherence.CoherenceError): coherence.admit_governance(source, public_repositories=self.roster)
        for extra in ("verified_human", "score", "ci_status"):
            source = copy.deepcopy(self.base); source[extra] = True
            with self.assertRaises(coherence.CoherenceError): coherence.admit_governance(source, public_repositories=self.roster)


if __name__ == "__main__":
    unittest.main()
