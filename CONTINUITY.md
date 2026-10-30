---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T21:54:14Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Repair bounded GitHub Actions uses detection for Hygiene #79.'
  includes:
  - Literal quoted/plain Action values, structural workflow/composite locations, deterministic locations
    and public CLI controls.
  excludes:
  - "Issues #80\u2013#85, policy authority changes, historical audit edits, original ADR-0001 approval/backfill\
    \ and publication."
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/DEPENDENCY_BOUNDARIES.md
  - catalog/dependency-boundaries.yaml
  - https://github.com/egohygiene/hygiene/issues/79
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: Recognize equivalent quoted mutable Action references without classifying unrelated text
    as executable dependencies.
  success_conditions:
  - Literal scalar parity, public CLI path/line/exit controls, immutable/versioned positives and documented
    supported subset.
  active_issue:
    provider: github
    id: egohygiene/hygiene#79
    url: https://github.com/egohygiene/hygiene/issues/79
  next:
    kind: action
    id: implement-quoted-uses-detection
    description: Implement the bounded scanner repair, then rerun focused and complete checks before review.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/79
    depends_on: []
state:
  base:
    revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    ref: refs/heads/main
    verified_at: '2026-10-30T21:54:14Z'
  candidate:
    branch: fix/79-quoted-action-refs
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T21:54:14Z'
    default_branch_revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Live issue #79 is open without comments; parent verified unchanged main and audit draft #75.
      This candidate has not merged.'
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
  - provider: github
    id: egohygiene/hygiene#77
    url: https://github.com/egohygiene/hygiene/issues/77
  - provider: github
    id: egohygiene/hygiene#78
    url: https://github.com/egohygiene/hygiene/issues/78
review:
  status: partial
  reviewed_at: '2026-10-30T21:54:14Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I -m unittest discover --start-directory tests --pattern test_boundaries.py --verbose
    outcome: failed
    observed_at: '2026-10-30T21:54:14Z'
    notes: 'Regression checkpoint: 24 methods ran; thirteen expected failing subcases expose missing quotes/escapes
      and unrelated-text matches. No scanner implementation changed yet.'
  environment_limitations:
  - Hosted changed-head qualification remains deferred; regression failures are deliberately retained
    before the repair.
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

Live instructions, canonical contracts and verified tracker state outrank this compact handoff. It grants no authority.

## Resume protocol

Read AGENTS, the boundary guide/register and #79, then verify main, this candidate and the three-issue batch in #76.

## Current objective and success conditions

Repair equivalent quoted Action references with correct executable locations and unchanged rule identity, paths and lines.

## State snapshot

This regression candidate starts from verified main aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d. Its containing revision is intentionally null. The previous #73/#74 continuity objective was already merged; this snapshot replaces that stale task state.

## Completed and material changes

Eight focused methods add quoted/plain, reusable workflow/composite, public CLI, pinned-reference and unrelated-text controls. Two old inline fixtures now use actual workflow nesting. tools/boundaries.py and its owning policy remain unchanged at this checkpoint. ADR not required: this is a repair of the existing BOUNDARY-002 reference implementation, preserving ownership, dependency rules and authority.

## Validation and review evidence

The focused command ran 24 methods and retained thirteen expected failing subcases. The failures are the stage-one reproduction, not acceptance. Full unchanged-base coverage is recorded by the batch coordinator. No hosted result is inferred.

## Blockers, risks, unknowns, and deferred work

The scanner repair is pending. General YAML features, fleet/native enforcement and source originality remain outside this bounded parser. Original ADR-0001 authority and actual publication remain #47 work. Preserve its original body and review patch, all accepted/proposed policy states and immutable audit evidence.

## Next dependency-ready work

Implement #79, pass the focused and complete checks, then prepare its draft for the batch review. Do not start #80–#85.

## Parallel changes and reconciliation

#77 and #78 are independent candidates from the same main. Reconcile shared continuity semantically at review/merge time. Audit draft #75 stays independent at head 58d28563206c7b2957867b0a25827b6a08558d66.

## Privacy and redaction

Only public-safe source facts and synthetic fixtures are retained. No raw logs, credentials, environment values, private paths or conversation transcript belong here.

## Handoff update protocol

Refresh after domain checks before each draft handoff, verify schema/sections/budgets and retain actual failed, limited and deferred outcomes.

## Compaction and supersession

Keep one current objective and twelve sections below 240 lines and 16,384 UTF-8 bytes. Git and #76 retain history and carried follow-ups.
