# Helpful-content reference fixtures

All content, roles, source URLs and review claims are synthetic. None asserts a
real site's quality, actual expert credentials, human approval or publication.

`expectations.json` independently declares seven expected metadata states at a
fixed supplied time: good, partial, stale, intentionally archived, missing
high-stakes review, missing AI provenance and unknown applicability. The good
fixture is metadata-ready and still requires independent editorial review.
Archived means intentionally historical, never current or freshly endorsed.

Run `tools/helpful_content.py validate-fixtures` and
`python3 -m unittest discover -s tests -p test_helpful_content.py`. Runtime tests
separately cover adversarial binding, future/stale review, correction/supersession,
approval/score injection, duplicate input, privacy and unsafe references. No
skipped or absent human/provider check is treated as passing.
