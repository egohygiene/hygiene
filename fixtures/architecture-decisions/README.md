# ADR compatibility fixtures

These are synthetic decoded JSON records for reference/schema tests. Their
status and evidence descriptors assert no actual human decision or test run.

- `decision.pending-predecessor.valid.json` and
  `decision.pending-replacement.valid.json` represent an accepted predecessor
  and a proposed replacement. The old record has no effective backlink.
- `decision.accepted.valid.json` and `decision.superseded.valid.json` retain
  the effective reciprocal pair. The tests also reject unapproved/declined
  replacements, missing backlinks, self-links and cycles.
- `decision.verified.valid.json` declares named validation evidence structurally;
  `decision.verified-approval-only.invalid.json` is the approval-only negative.
  `decision.zero-id.invalid.json` rejects canonical `ADR-0000`; valid bounds are
  `ADR-0001` and `ADR-9999`.

## Historical identity compatibility

`historical/policy-1.1.0/decision.previous.json` and `decision.replacement.json`
preserve the exact synthetic `ADR-006`/`ADR-007` pair. Their selected older
Hygiene helper/policy source is
`f598ed659a43dd759d4ede41c27f9e5daf991aa7`. Use a separately inspected trusted
copy of that exact `tools/decisions.py`; no current command implicitly fetches
or falls back to historical source:

```sh
python3 "$LEGACY_ADR_REFERENCE" decision-set \
  --input fixtures/architecture-decisions/historical/policy-1.1.0/decision.previous.json \
  --input fixtures/architecture-decisions/historical/policy-1.1.0/decision.replacement.json
```

The current v1.2.0 canonical mode rejects three-digit record IDs. Its set checker
still resolves exact locally supplied identities and reports dangling references
equally for the accepted three-/four-digit reference grammar. There is no implicit
padding alias. A test-only explicit map `ADR-006 -> ADR-0006`,
`ADR-007 -> ADR-0007` shows number/disposition-preserving migration on copies;
no historical source, authored ADR, lifecycle authority or consumer pin changes.

The fixtures and per-record schema cannot prove evidence authentication, actual
execution, external-index resolution or native Markdown/source admission. See
the [validation guide](../../docs/decisions/VALIDATION.md) for the exact current
reference versus pinned Aether/native boundaries.
