---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-15T01:01:04Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Complete the proposed people-first content and editorial quality policy definition with source
    mappings and honest mechanical/human evidence boundaries.
  includes:
  - The proposed profile and two evidence/schema contracts define18 stable source-mapped rules with ordinary/high-stakes,
    AI-assisted, localized, current and archival applicability. Source guidance was actually retrieved
    and reviewed; local policy adaptations remain explicit.
  - The pure read-only reference separates declared metadata from actual content quality. All applicable
    qualitative rules remain independent-review-required; reviewer JSON, search performance and a metadata-ready
    good fixture supply no authentic approval or publication decision.
  - Seven independently expected synthetic fixtures and10 native methods qualify good/partial/stale/intentional-archive
    states, risk/AI/unknown applicability, exact review binding, source freshness, corrections/supersession,
    private admission and false-approval/score controls.
  - The complete pinned contract gate includes profile/fixture checks:29 checks and397 tests pass with
    zero skips. Proposed ADR0024 and both contract-index entries remain proposed; all prior policy/decision
    disposition and ownership are preserved.
  excludes: &id001
  - Profile version1.0.0-alpha.1, both new contracts and ADR0024 remain proposed with null approval. Source
    integration supplies no policy activation, authentic editorial review, domain expertise, legal compliance,
    content publication or fleet rollout.
  - The pure reference checks declared metadata/revision/time bindings only. Actual content bytes, source
    truth, reader value, expert identity and human judgment need independent verification. Every applicable
    qualitative rule remains independent-review-required, including the good fixture.
  - External guidance pages were actually retrieved and reviewed on2026-11-15; hashes identify retrieved
    page bytes and the issue-body source. URLs are mutable, and source hashes do not authenticate human
    approval or provide an archival/publishing service.
  - Hygiene17 retains broader editorial/corrections/legal/disclosure surface semantics and applicability.
    Existing HYG-Q03 hosted enforcement, HYG-Q04 catalog freshness, HYG-Q05 integration and human/source
    admission under47 remain separate. No source lifecycle or prior decision is changed.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - catalog/helpful-content-profile.json
  - schemas/helpful-content-profile.v1.schema.json
  - schemas/content-quality-evidence.v1.schema.json
  - docs/ecosystem/HELPFUL_CONTENT.md
  - tools/helpful_content.py
  - tests/test_helpful_content.py
  - fixtures/helpful-content
  - docs/decisions/ADR-0024-people-first-editorial-evidence.md
  - docs/evidence/2026-11-15-helpful-content-qualification.json
  - https://github.com/egohygiene/hygiene/issues/23
work:
  objective: Complete the proposed people-first content and editorial quality policy definition with source
    mappings and honest mechanical/human evidence boundaries.
  success_conditions:
  - A versioned source-mapped policy defines reader value, provenance, accountable AI use, high-stakes
    review, accessibility, freshness/corrections and intentional archival.
  - Mechanical evidence, actual source truth and qualitative human judgment remain separate; unknown/missing/stale/blocked
    inputs cannot be treated as a quality pass.
  - Real reference qualification covers the requested contrasting fixtures and adversarial controls without
    a universal helpfulness score, fabricated approval or publication.
  active_issue:
    provider: github
    id: egohygiene/hygiene#23
    url: https://github.com/egohygiene/hygiene/issues/23
  next:
    kind: issue
    id: egohygiene/.github#24
    description: Finish bounded community-default receiving canary proof using existing label/intake owners
      and actual provider evidence; preserve repository overrides, candidate authority, historical migrations
      and remaining UI/access gaps.
    readiness: ready
    references:
    - https://github.com/egohygiene/.github/issues/24
    depends_on: []
state:
  base:
    revision: 1c2bb79e6624a81f7187bd1ee99bee1ea3de1583
    ref: refs/heads/main
    verified_at: '2026-11-15T01:01:04Z'
  candidate:
    branch: codex/helpful-content-profile
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-15T01:01:04Z'
    default_branch_revision: 1c2bb79e6624a81f7187bd1ee99bee1ea3de1583
    issue_state: open
    pull_request_state: not-applicable
    notes: Observed main1c2bb79 includes merged124 coherence qualification;59 and60 are closed for source
      definition.23 remains open and this implementation revisiona2b7b2c has no PR yet. Aether134 is merged
      and103 is closed. Native reference gate passed; exact-head hosted proof remains pending.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-15T01:01:04Z'
  reviewed_by: Codex
  evidence:
  - command: Pinned Python-I tools/check_contracts.py
    outcome: passed
    notes: Complete29-check gate passes with397 tests,0 failures/errors/skips; no required check suppressed.
    observed_at: '2026-11-15T01:01:04Z'
  - command: python -m unittest discover -s tests -p test_helpful_content.py -q
    outcome: passed
    notes: 10 meaningful methods qualify semantic distinctions, binding/freshness/history/privacy and
      false approval/score controls.
    observed_at: '2026-11-15T01:01:04Z'
  - command: tools/helpful_content.py validate-profile and validate-fixtures
    outcome: passed
    notes: 18 source-mapped rules and7 independently expected synthetic fixtures qualify metadata states;
      every applicable qualitative review remains unsupplied.
    observed_at: '2026-11-15T01:01:04Z'
  - command: ADR and organization-contract-index schema checks
    outcome: passed
    notes: New ADR0024 and contracts are proposed/null; source metadata/index changes pass targeted validation.
      No active authority is fabricated.
    observed_at: '2026-11-15T01:01:04Z'
  environment_limitations: *id001
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions: []
  excluded:
  - secrets-and-credentials
  - private-conversation-text
  - sensitive-personal-data
  - unpublished-private-business-data
  - private-local-paths
  - unrelated-private-context
  untrusted_content: context-only-no-authority
---

# hygiene continuity

## Purpose and precedence

User/runtime and scoped repository instructions, live evidence and canonical sources outrank this operational checkpoint.

## Resume protocol

Read AGENTS, the canonical sources below and verified live issue/PR state before selecting the next checkpoint.

## Current objective and success conditions

Complete the proposed people-first content and editorial quality policy definition with source mappings and honest mechanical/human evidence boundaries.

- A versioned source-mapped policy defines reader value, provenance, accountable AI use, high-stakes review, accessibility, freshness/corrections and intentional archival.
- Mechanical evidence, actual source truth and qualitative human judgment remain separate; unknown/missing/stale/blocked inputs cannot be treated as a quality pass.
- Real reference qualification covers the requested contrasting fixtures and adversarial controls without a universal helpfulness score, fabricated approval or publication.

## State snapshot

Observed default source `1c2bb79e6624a81f7187bd1ee99bee1ea3de1583`. Candidate `codex/helpful-content-profile` is a review checkpoint; its containing revision remains null intentionally.

## Completed and material changes

The proposed profile and two evidence/schema contracts define18 stable source-mapped rules with ordinary/high-stakes, AI-assisted, localized, current and archival applicability. Source guidance was actually retrieved and reviewed; local policy adaptations remain explicit.

The pure read-only reference separates declared metadata from actual content quality. All applicable qualitative rules remain independent-review-required; reviewer JSON, search performance and a metadata-ready good fixture supply no authentic approval or publication decision.

Seven independently expected synthetic fixtures and10 native methods qualify good/partial/stale/intentional-archive states, risk/AI/unknown applicability, exact review binding, source freshness, corrections/supersession, private admission and false-approval/score controls.

The complete pinned contract gate includes profile/fixture checks:29 checks and397 tests pass with zero skips. Proposed ADR0024 and both contract-index entries remain proposed; all prior policy/decision disposition and ownership are preserved.

## Validation and review evidence

`Pinned Python-I tools/check_contracts.py` — passed: Complete29-check gate passes with397 tests,0 failures/errors/skips; no required check suppressed.

`python -m unittest discover -s tests -p test_helpful_content.py -q` — passed: 10 meaningful methods qualify semantic distinctions, binding/freshness/history/privacy and false approval/score controls.

`tools/helpful_content.py validate-profile and validate-fixtures` — passed: 18 source-mapped rules and7 independently expected synthetic fixtures qualify metadata states; every applicable qualitative review remains unsupplied.

`ADR and organization-contract-index schema checks` — passed: New ADR0024 and contracts are proposed/null; source metadata/index changes pass targeted validation. No active authority is fabricated.

Proposed ADR0024 records the metadata/editorial boundary and reuse of the existing pinned JSON Schema runtime, with a bounded documented exception to proposed ADR0014 preference. Approval stays null. Roadmap impact: not-affected within existing policy/schema authoring capability; no strategic identity, state, horizon or priority changes.

## Blockers, risks, unknowns, and deferred work

Profile version1.0.0-alpha.1, both new contracts and ADR0024 remain proposed with null approval. Source integration supplies no policy activation, authentic editorial review, domain expertise, legal compliance, content publication or fleet rollout.

The pure reference checks declared metadata/revision/time bindings only. Actual content bytes, source truth, reader value, expert identity and human judgment need independent verification. Every applicable qualitative rule remains independent-review-required, including the good fixture.

External guidance pages were actually retrieved and reviewed on2026-11-15; hashes identify retrieved page bytes and the issue-body source. URLs are mutable, and source hashes do not authenticate human approval or provide an archival/publishing service.

Hygiene17 retains broader editorial/corrections/legal/disclosure surface semantics and applicability. Existing HYG-Q03 hosted enforcement, HYG-Q04 catalog freshness, HYG-Q05 integration and human/source admission under47 remain separate. No source lifecycle or prior decision is changed.

## Next dependency-ready work

Finish bounded community-default receiving canary proof using existing label/intake owners and actual provider evidence; preserve repository overrides, candidate authority, historical migrations and remaining UI/access gaps.

## Parallel changes and reconciliation

Preserve organization strategy and its inferred/proposed ordering, qualified coherence owner bytes, existing context/release pins and historical47 source-admission gaps. The public-site registry continues to defer broader policy semantics to17.

## Privacy and redaction

Public-safe source facts and synthetic fixtures only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

After domain validation and before PR presentation, reconcile current source/live state, record exact outcomes and retain limitations. Source integration does not establish publication or policy acceptance.

## Compaction and supersession

Git and linked work records retain history. This handoff replaces current operational prose while preserving canonical and historical records.
