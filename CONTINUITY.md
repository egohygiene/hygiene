---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:49:21Z'
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
    id: implement-adr-reference-alignment
    description: 'Repair #82 reference/schema semantics, verify compatibility controls and prepare the
      bounded draft for review.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/82
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-10-30T22:49:21Z'
  candidate:
    branch: fix/82-adr-reference
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T22:49:21Z'
    default_branch_revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Current main is verified; #82 is open without comments. The previous three implementation
      candidates are merged. This is a new independent regression candidate.'
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
  reviewed_at: '2026-10-30T22:49:21Z'
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

Ten regression methods and synthetic decoded fixtures reproduce the four mismatches. Historical compatibility fixtures preserve three-digit identities; a synthetic explicit padding map preserves their decision substance. Reference/schema source is unchanged at this checkpoint. ADR-Ref: egohygiene/hygiene#ADR-0002; routine repair of the existing policy implementation requires no duplicate ADR or new disposition.

## Validation and review evidence

The unchanged complete gate passed228 tests and25 checks. Focused25 methods retain twelve expected failing subcases before the repair. These failures are reproduction evidence, not acceptance. The exact Aether authoring guide and its older-helper warning were inspected at dc8a16851f452763ef4f7fbe4bf057d4500b1921.

## Blockers, risks, unknowns, and deferred work

Implementation is pending. Selected native d917 replay is unavailable; a different cached runtime cannot replace it. Source admission/publication and original ADR-0001 historical approval stay #47 work. The17 unchanged broader web-schema diagnostics remain in #76. No source helper/schema result authenticates human approval or actual execution.

## Next dependency-ready work

Implement #82, run focused/public CLI/schema/compatibility and complete gate checks, then review this three-issue batch. Keep #83–#85 unstarted.

## Parallel changes and reconciliation

#80 and #81 are independent peer candidates from the same main. Reconcile shared continuity semantically. Audit draft #75 remains independent at58d28563206c7b2957867b0a25827b6a08558d66; its branch and historical evidence are preserved.

## Privacy and redaction

Only public-safe source facts and synthetic fixtures belong here. Exclude raw logs, private paths, credentials, environment values and conversation text.

## Handoff update protocol

Refresh after domain validation before each draft handoff; verify the pinned b7597301c4d22a9bcd580967b5753138bb368111 continuity schema, twelve sections, privacy and budgets.

## Compaction and supersession

Keep one bounded objective under240 lines/16,384bytes. Git and #76 preserve history and carried acceptance work.
