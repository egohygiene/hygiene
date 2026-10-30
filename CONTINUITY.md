---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T23:12:11Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Align the decoded ADR reference checker and schema with selected policy in Hygiene #82.'
  includes:
  - Pending/effective supersession, named validation evidence, exact historical reference lookup and canonical
    ID range.
  excludes:
  - 'Actual ADR dispositions/renames, original ADR-0001 approval/backfill, native source admission/publication,
    #83–#85 and unrelated policy changes.'
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/decisions/POLICY.md
  - docs/decisions/VALIDATION.md
  - schemas/architecture-decision.v1.schema.json
  - https://github.com/egohygiene/hygiene/issues/82
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: Repair four bounded decoded ADR reference mismatches while preserving lifecycle authority
    and historical identities.
  success_conditions:
  - Pending proposals require no old mutation; effective supersession remains reciprocal/authorized/acyclic.
  - Verified implementation needs declared named validation evidence; three/four-digit dangling refs have
    equal diagnostics; canonical zero rejects.
  active_issue:
    provider: github
    id: egohygiene/hygiene#82
    url: https://github.com/egohygiene/hygiene/issues/82
  next:
    kind: action
    id: review-three-issue-batch
    description: Independently review draft90 and qualify the combined80–82 batch, then sync with the
      maintainer before any merge or next batch.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-10-30T22:49:21Z'
  candidate:
    branch: fix/82-adr-reference
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#90
      url: https://github.com/egohygiene/hygiene/pull/90
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-30T23:12:11Z'
    default_branch_revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    issue_state: open
    pull_request_state: draft
    notes: Live draft90 is open for82; main staysfa41ccc95d0cd0365b38008e02bdc67b928c5ed2. Audit75 is
      unchanged/open/draft. This candidate is unmerged.
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
  - provider: github
    id: egohygiene/hygiene#80
    url: https://github.com/egohygiene/hygiene/issues/80
  - provider: github
    id: egohygiene/hygiene#81
    url: https://github.com/egohygiene/hygiene/issues/81
review:
  status: partial
  reviewed_at: '2026-10-30T23:12:11Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I tools/check_contracts.py (unchanged base)
    outcome: passed
    observed_at: '2026-10-30T22:49:21Z'
    notes: 228 tests with zero skips/failures/errors and all 25 command checks passed.
  - command: python3 -I -m unittest discover --start-directory tests --pattern test_decisions.py --verbose
    outcome: failed
    observed_at: '2026-10-30T22:49:21Z'
    notes: 'Regression checkpoint: 25 methods ran with twelve expected failing subcases on unchanged reference/schema
      source.'
  - command: Focused ADR suite; complete python3 -I tools/check_contracts.py
    outcome: passed
    observed_at: '2026-10-30T22:55:56Z'
    notes: 27 focused methods; full gate240 tests, zero skips/failures/errors and all25 command checks
      passed.
  - command: Draft202012 schema/meta/formats and targeted per-record parity
    outcome: passed
    observed_at: '2026-10-30T22:55:56Z'
    notes: 25 targeted fixture/ID/evidence cases agree between current schema and reference. This is not
      whole-schema equivalence or cross-record authentication.
  - command: Exact older policy/helper versus current decoded CLI compatibility replay
    outcome: passed
    observed_at: '2026-10-30T22:55:56Z'
    notes: Pinned a05b old helper rejects pending pair; candidate accepts. Pinned1.1 f598 helper accepts
      exact historical3digit pair; current canonical mode rejects those record IDs. Explicit synthetic
      mapped copies pass current mode.
  - command: Optional workspace Ruff baseline comparison
    outcome: limited
    observed_at: '2026-10-30T22:55:56Z'
    notes: Six findings remain identical by path/rule/message to unchanged source; no new finding and
      no Ruff-clean claim.
  - command: Final focused suite and complete python3 -I tools/check_contracts.py
    outcome: passed
    observed_at: '2026-10-30T23:12:11Z'
    notes: Focused27; full240 tests, zero skips/failures/errors and all25 command checks passed on final
      implementation bytes.
  - command: Own-review schema end-anchor reproduction and repair qualification
    outcome: passed
    observed_at: '2026-10-30T23:12:11Z'
    notes: Two newline-suffixed IDs were admitted by the pre-review8ee schema while the helper rejected
      them. Exact8-character schema limits repair both; final schema/meta/formats and27 targeted cases
      plus public CLI controls pass.
  - command: Full scoped diff, pinned continuity schema/formats, privacy/budgets and whitespace
    outcome: passed
    observed_at: '2026-10-30T23:12:11Z'
    notes: Thirteen changed files including synthetic fixtures; all other tracked source, actual ADRs,
      policies/pins, audit and original review patch remain unchanged.
  environment_limitations:
  - 'Exact selected native EgoLint d917ea524962639494e5bb4b3196192238ba57d9 replay is unavailable: no
    cached binary is proven bound to that source. The different cached f14 runtime is not substituted.'
  - 'Hosted changed-head qualification, source admission/publication and original ADR-0001 authority remain
    separate. The unchanged web profile/schema has17 broader diagnostics carried in #76.'
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

# Hygiene continuity

## Purpose and precedence

Live instructions, verified repository/tracker state and canonical policy outrank this operational handoff. It grants no authority.

## Resume protocol

Read AGENTS, policy sections4/9/10, VALIDATION and #82; verify current main and candidate, then inspect #76's three-issue batch.

## Current objective and success conditions

Align pending/effective supersession, named verification evidence, historical reference lookup and canonical ID range with selected policy.

## State snapshot

This independent candidate starts from verified main fa41ccc95d0cd0365b38008e02bdc67b928c5ed2 after accepted #87/#88/#86. The containing revision is null. No new candidate merge is claimed.

## Completed and material changes

tools/decisions.py now distinguishes declared proposal history from effective reciprocal supersession, requires named validation evidence, diagnoses both local reference widths and rejects canonical zero. The schema mirrors the per-record constraints; twelve focused methods and synthetic fixtures cover current and historical compatibility. Malformed lineage arrays remain controlled diagnostics. No authored ADR is changed. ADR-Ref: egohygiene/hygiene#ADR-0002; routine repair of the existing policy implementation requires no duplicate ADR or new disposition.

## Validation and review evidence

The baseline gate passed228 tests/25 checks. Implementation focused27 and complete240 tests/25 checks pass without skips. The earlier focused25/twelve expected failing subcases preserve the stage-one reproduction. Final targeted schema parity27 and four exact older/current CLI compatibility checks pass; optional Ruff retains six unchanged findings. The exact Aether authoring guide and its older-helper warning were inspected at dc8a16851f452763ef4f7fbe4bf057d4500b1921.

## Blockers, risks, unknowns, and deferred work

Author complete-diff review repaired the schema end-anchor mismatch; parent independent and combined-batch review remain pending. Selected native d917 replay is unavailable; a different cached runtime cannot replace it. Source admission/publication and original ADR-0001 historical approval stay #47 work. The17 unchanged broader web-schema diagnostics remain in #76. No source helper/schema result authenticates human approval or actual execution.

## Next dependency-ready work

Independently review draft90 and qualify the combined80–82 batch, then sync with the maintainer before any merge or next batch. Keep #83–#85 unstarted.

## Parallel changes and reconciliation

#80 and #81 are independent peer candidates from the same main. Reconcile shared continuity semantically. Audit draft #75 remains independent at58d28563206c7b2957867b0a25827b6a08558d66; its branch and historical evidence are preserved.

## Privacy and redaction

Only public-safe source facts and synthetic fixtures belong here. Exclude raw logs, private paths, credentials, environment values and conversation text.

## Handoff update protocol

Refresh after domain validation before each draft handoff; verify the pinned b7597301c4d22a9bcd580967b5753138bb368111 continuity schema, twelve sections, privacy and budgets.

## Compaction and supersession

Keep one bounded objective under240 lines/16,384bytes. Git and #76 preserve history and carried acceptance work.
