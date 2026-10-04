"""Collection completeness is a claim, never inferred from empty graph arrays."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import intelligence


class CoverageContractTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = {p.stem: json.loads(p.read_text()) for p in
                         (ROOT / 'fixtures/repository-intelligence/coverage').glob('*.json')}
        self.vocabulary = json.loads((ROOT / 'catalog/repository-intelligence-vocabulary.json').read_text())

    def test_all_synthetic_coverage_fixtures_validate(self):
        for name, fixture in self.fixtures.items():
            with self.subTest(name=name):
                self.assertEqual([], intelligence.validate_snapshot(fixture, self.vocabulary))

    def test_every_domain_is_required_and_unknown_domains_are_rejected(self):
        for domain in intelligence.COVERAGE_DOMAINS:
            candidate = deepcopy(self.fixtures['full'])
            del candidate['collection_coverage'][domain]
            self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))
        candidate['collection_coverage']['protected/hidden'] = {'count': 37}
        errors = intelligence.validate_snapshot(candidate, self.vocabulary)
        self.assertTrue(errors)
        self.assertNotIn('protected/hidden', ' '.join(errors))
        self.assertNotIn('37', ' '.join(errors))

    def test_denied_coverage_cannot_carry_provider_identity_counts_or_messages(self):
        for key in ('repository', 'count', 'url', 'message', 'extensions'):
            candidate = deepcopy(self.fixtures['provider-denied'])
            candidate['collection_coverage']['issues'][key] = 'protected/hidden'
            errors = intelligence.validate_snapshot(candidate, self.vocabulary)
            self.assertTrue(errors)
            self.assertNotIn('protected/hidden', ' '.join(errors))

    def test_false_empty_and_false_observed_claims_are_rejected(self):
        for state in ('observed_empty', 'not_applicable', 'unavailable', 'failed', 'uncollected'):
            candidate = deepcopy(self.fixtures['full'])
            candidate['collection_coverage']['issues']['collection'] = state
            self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))
        candidate = deepcopy(self.fixtures['observed-empty'])
        candidate['collection_coverage']['issues']['collection'] = 'observed'
        self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))

    def test_filtered_and_truncated_results_remain_partial_even_when_empty(self):
        for reason in ('filtered', 'truncated', 'incomplete'):
            candidate = deepcopy(self.fixtures['partial'])
            candidate['collection_coverage']['issues']['reason'] = reason
            self.assertEqual([], intelligence.validate_snapshot(candidate, self.vocabulary))
            candidate['collection_coverage']['issues']['collection'] = 'observed_empty'
            self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))

    def test_legacy_input_cannot_silently_attach_new_coverage(self):
        candidate = deepcopy(self.fixtures['full'])
        candidate['contract_version'] = '1.0.0-alpha.1'
        self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))
        del candidate['collection_coverage']
        self.assertEqual([], intelligence.validate_snapshot(candidate, self.vocabulary))

    def test_freshness_and_time_cannot_upgrade_uncollected_data(self):
        for key, value in [('freshness','current'), ('observed_at','2026-10-03T00:00:00Z'),
                           ('reason','complete')]:
            candidate = deepcopy(self.fixtures['roadmap-only'])
            candidate['collection_coverage']['issues'][key] = value
            self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))
        candidate = deepcopy(self.fixtures['full'])
        candidate['collection_coverage']['issues']['observed_at'] = '2099-01-01T00:00:00Z'
        self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))

    def test_malformed_coverage_diagnostics_never_crash(self):
        for value in (None, [], {}, 42, True, 'protected/hidden'):
            candidate = deepcopy(self.fixtures['full'])
            candidate['collection_coverage'] = value
            self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))
            for key in ('collection', 'freshness', 'reason', 'observed_at'):
                candidate = deepcopy(self.fixtures['full'])
                candidate['collection_coverage']['issues'][key] = value
                self.assertTrue(intelligence.validate_snapshot(candidate, self.vocabulary))


if __name__ == '__main__':
    unittest.main()
