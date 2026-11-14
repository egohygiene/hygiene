# Synthetic coherence policy qualification

These18 cases contain fictional review identities, dummy revisions/digests and
nonexistent source locators. They do not report a real person's approval or
ratify any architecture. `expected` fields are independently declared outcomes,
not generated golden output copied from the evaluator.

The tests exercise the existing, unchanged Hygiene policy/reference source.
`synthetic_trust_kinds` belongs only to the test harness: trusted test code
constructs an in-memory `TrustedHumanEvidence` after selecting an explicitly
synthetic statement. It is not a governance-source field or production JSON
trust adapter. Passing a similar dictionary to the evaluator grants no trust.

Coverage includes current and expired review, missing/unavailable evidence,
material versus routine change, unknown inventory, deferred and inapplicable
exceptions, revision-required disposition, organization scope and privacy-first
exclusion. The executable tests additionally cover statement binding, forged
claims, invalidation, source clocks, sensitive prose, unsafe evidence URLs,
selected event duplication and protected payload omission.

```bash
python3 -I -m unittest discover -s tests -p test_architecture_coherence.py -v
```

The two standalone valid files provide schema/reference examples. Public
admission intentionally excludes protected or unadmitted members before payload
validation; a filtered fixture is never relabeled as a complete public review.
Provider authentication, actual human decisions, production integration and
policy enforcement remain separate downstream work.
