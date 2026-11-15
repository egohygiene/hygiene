# People-first content and editorial quality profile

Status: **proposed**, `1.0.0-alpha.1`; human activation is not supplied.
Canonical source: [profile](../../catalog/helpful-content-profile.json).
Contracts: [profile schema](../../schemas/helpful-content-profile.v1.schema.json)
and [content evidence](../../schemas/content-quality-evidence.v1.schema.json).

This profile defines reviewable expectations for useful, trustworthy content.
It does not estimate ranking, promise indexing, certify quality or give content
a universal helpfulness score. Search traffic and ranking cannot substitute for
reader value, accurate evidence or accountable editorial judgment.

## Sources and local policy decisions

The profile maps each stable rule to reviewed source IDs and an applicability
class. The [Google people-first guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
provides editorial self-assessment, original value, experience/expertise,
accurate promises, and who/how/why framing. It is guidance, not Google endorsement
of this profile or a claim that E-E-A-T is one mechanical ranking factor.
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplies technical accessibility and
equivalent-information context; legal applicability remains separate.

Both pages were retrieved successfully on 2026-11-15. Exact observation times
and page-byte SHA-256 values are in the source catalog. These identify retrieved
snapshots; the public URLs are mutable and the hashes do not authenticate an
organization approval. The profile contains original requirements and links,
not redistributed copies of those pages.

Hygiene23 supplies explicitly proposed local requirements for source provenance,
AI workflow accountability, revision-bound review, freshness, corrections,
archival and domain review. They are recorded as local policy adaptations rather
than falsely attributed as universal Google mandates. Selecting a review interval
requires appropriate editorial/domain judgment; the checker invents no cadence.

## Rules and applicability

| ID | Requirement | Applicability | Mechanical / human boundary |
| --- | --- | --- | --- |
| HC-001 | Audience, purpose and user need | All | Metadata presence; relevance still needs judgment |
| HC-002 | Original reader value | All | Human editorial review |
| HC-003 | Supported experience/expertise claims | All | Human source/domain review |
| HC-004 | Accountable authorship/editor | All | Role metadata; identity/authenticity separately verified |
| HC-005 | Accurate titles, summaries and promises | All | Human comparison with actual content |
| HC-006 | Source references, dates and available digests | All | Shape/freshness of declared evidence; no source fetching |
| HC-007 | Limitations, uncertainty and applicability | All | Evidence reference plus human risk review |
| HC-008 | AI method/provenance and accountable reviewer | AI-assisted | Metadata required; disclose to readers where applicable |
| HC-009 | AI-assisted accuracy, originality and oversight | AI-assisted | Human review; scale/automation is not value |
| HC-010 | Last substantive review bound to content revision | Current content | Declared revision/date/interval; actual review independently verified |
| HC-011 | Corrections and supersession | All | Stable dated source links; no silent history rewrite |
| HC-012 | Intentional archive status | Archived | Reason/date/banner reference; no fake freshness |
| HC-013 | Locale and accessibility/equivalent evidence | All | Metadata; actual accessibility remains unproven |
| HC-014 | Meaningful accessible/localized equivalents | All | Human review of actual information |
| HC-015 | Qualified specialist review evidence | High-stakes | Revision-bound record; credentials/review independently verified |
| HC-016 | Expert accuracy and appropriate consensus | High-stakes | Qualified human/domain review |
| HC-017 | No fabricated expertise or search-first low-value output | All | Human editorial judgment; no ranking proxy |
| HC-018 | Reviewed equivalent localized content | Localized | Reference metadata; linguistic quality separately reviewed |

Unknown AI assistance, risk or localization makes conditional applicability
**unknown**, not exempt. Ordinary content does not inherit service-specific or
high-stakes requirements; health, legal, financial, safety and research content
requires appropriate specialist review. A reviewer label alone proves neither
qualification nor authentic approval.

## Evidence and review semantics

The subject identifies an exact declared SHA-256 content revision. Callers verify
that it represents actual content bytes. Review records bind that revision,
recorded UTC time, explicit interval and evidence source. A cosmetic updated
timestamp does not renew last substantive review. Future or revision-mismatched
records are blocked; overdue records are stale. Missing fields stay missing.

Authorship/editorial roles identify responsibility without inventing credentials.
Sources retain visibility, observation time and digest when known; unavailable
provenance remains partial. Limitations and actual domain evidence must be
reviewed in the content, not inferred from the presence of a URL.

Corrections preserve stable IDs, time, source and supersession links; duplicate,
missing or cyclic correction references are rejected. A superseded subject needs
a successor reference. Keep the old source accessible with appropriate historical
context rather than silently editing the claim's history. An empty corrections
list means none recorded in supplied evidence, not proof that no correction is
needed.

Intentional archival needs its own reason, date and visible historical-status
reference. It is **intentionally-archived**, not current/fresh/passing. An archive
label alone cannot bypass its evidence gate. Domain risk and qualitative review
remain visible; archival does not endorse the old claims.

Reviewer JSON records are attributed **claims**. A matching revision, role string,
supported judgment or schema-valid object cannot authenticate human review.
The reference tool always leaves applicable qualitative rules at
`independent-review-required`, even in the good fixture. Production consumers
must independently verify identity, scope, actual content and source evidence;
they must preserve this boundary in their own review workflow.

## Reference evaluation

```sh
python3 tools/helpful_content.py validate-profile
python3 tools/helpful_content.py validate-fixtures
python3 tools/helpful_content.py assess \
  --input fixtures/helpful-content/good.json \
  --as-of 2026-11-15T00:00:00Z --public-output
```

Use the existing pinned JSON Schema runtime prepared for the [complete contract gate](../CONTRACT_VALIDATION.md); the commands assume that runtime is selected on PATH. No new dependency or installation step is added.

The read-only helper uses caller-supplied time, performs no network/clock reads,
and emits a reference view bound to this proposed profile, not a second normalized
lint-report contract. It checks metadata/local source bindings only. It never
fetches content, verifies reviewer identity, measures usefulness, publishes or
activates policy. Diagnostics withhold rejected content.

The [seven synthetic fixtures](../../fixtures/helpful-content) independently
expect metadata-ready, partial, stale, intentionally-archived and unknown states,
plus missing high-stakes/AI evidence. Metadata-ready means declared mechanical
fields are present; human review and publication decisions remain unsupplied.
Every fixture keeps qualitative review explicit. Adversarial tests cover false
approval/score claims, changed revisions, future dates, stale review claims,
correction cycles, private admission and unsafe references.

## Privacy, integration and adoption

Public evidence cannot contain declared private/internal sources. A restricted
assessment cannot be emitted through the public-output path. Classification
still needs content review: a label cannot detect hidden sensitive prose or
declassify a private source. No private transcript or actual sensitive data is
used in fixtures.

Hygiene owns this proposed publication policy. Aether may author/review content;
EgoLint owns production conformance semantics and normalized diagnostics; Relay
orchestrates validation without owning editorial policy; Observatory reports
evidence/freshness without inventing a usefulness score. Content repositories
own sources, review, corrections, publication and final claims; Pace owns any
reviewed rollout proposals. Holon may scaffold selected metadata without creating
reviewed policy text or overwriting consumer content.

[Hygiene17](https://github.com/egohygiene/hygiene/issues/17) retains editorial,
corrections, legal/disclosure surface semantics and applicability. This profile
references those surfaces without assigning routes or completing that broader
issue. Jurisdiction, legal review, regulatory claims and actual accessibility
conformance remain separate. Neither templates nor CI establish legal compliance.

Keep the profile/ADR proposed with null approval until the owning human activation
process supplies a disposition. No enforcement, content publication, source-rights
clearance, Google endorsement or fleet rollout is activated by source integration.
