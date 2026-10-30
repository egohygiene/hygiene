---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:02:46Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Complete Hygiene issue #77 contract regression checks independently from native ADR admission
    and publication.'
  includes:
  - tools/check_contracts.py composes full unittest discovery and 24 deterministic reference/generated
    checks, reports actual counts and failures, and retains bounded diagnostics.
  - The Pages checks job runs that entrypoint at the exact PR head without path filters, with read-only
    permissions and diagnostic upload. Native/admission/build/deployment definitions remain unchanged.
  - 'README, Task check and the current HYG-Q03 note identify the same gate; the August roadmap snapshot
    is byte-preserved. Tracker #76 owns carried follow-ups.'
  excludes:
  - 'Issues #80–#85, historical audit PR #75, original ADR-0001 disposition, producer upgrades and publication.'
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - README.md
  - docs/decisions/POLICY.md
  - https://github.com/egohygiene/hygiene/issues/77
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: 'Complete Hygiene issue #77 contract regression checks independently from native ADR admission
    and publication.'
  success_conditions:
  - All current test families and deterministic source/generated checks execute together with attributable
    failures.
  - Read-only PR coverage has no path filters and remains separate from native admission and publication.
  active_issue:
    provider: github
    id: egohygiene/hygiene#77
    url: https://github.com/egohygiene/hygiene/issues/77
  next:
    kind: action
    id: review-contract-gate
    description: 'Complete independent source review and combined #77–#79 qualification, then keep the
      three drafts open for maintainer sync; do not start #80–#85.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/77
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    ref: refs/heads/main
    verified_at: '2026-10-30T22:02:46Z'
  candidate:
    branch: fix/77-contract-regression
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#87
      url: https://github.com/egohygiene/hygiene/pull/87
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T22:02:46Z'
    default_branch_revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    issue_state: open
    pull_request_state: draft
    notes: 'Observed main and active issues are unchanged; tracker #76 records the three-issue batch.
      This candidate is not merged.'
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
  - provider: github
    id: egohygiene/hygiene#78
    url: https://github.com/egohygiene/hygiene/issues/78
  - provider: github
    id: egohygiene/hygiene#79
    url: https://github.com/egohygiene/hygiene/issues/79
review:
  status: partial
  reviewed_at: '2026-10-30T22:02:46Z'
  reviewed_by: Codex
  evidence:
  - command: Unchanged baseline full unittest discovery
    outcome: passed
    observed_at: '2026-10-30T22:02:46Z'
    notes: 194 baseline tests passed with no skips.
  - command: Stage-one actual-gate regression suite
    outcome: failed
    observed_at: '2026-10-30T22:02:46Z'
    notes: Seven expected failures exposed the absent entrypoint; later implementation controls pass.
  - command: python3 -I tools/check_contracts.py
    outcome: passed
    observed_at: '2026-10-30T22:02:46Z'
    notes: 201 tests across all thirteen current modules passed with zero skips; all 25 planned command
      checks passed. Actual copied-source controls reject invalid catalog/profile, stale output, failed/empty
      discovery and preserve explicit skip counts.
  - command: Workflow structural comparison, new-file Ruff check/format, pinned continuity schema/composition
      and git diff --check
    outcome: passed
    observed_at: '2026-10-30T22:02:46Z'
    notes: Exact-head/read-only/unfiltered wiring is checked; every other workflow job/event and the historical
      roadmap block remain unchanged. New source lint/format and continuity constraints pass.
  environment_limitations:
  - Independent final review and combined batch qualification remain pending. Hosted changed-head execution
    and provider required-check configuration are unverified; no dispatch was performed. Native source
    authority and publication retain independent gates.
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

User/runtime instructions, scoped instructions, live evidence and canonical sources outrank this checkpoint. It grants no authority.

## Resume protocol

Read AGENTS and canonical policy, verify current main and PR state, then inspect #77 and tracker #76. The prior #73 adoption handoff is historical; #74 is already merged.

## Current objective and success conditions

Complete Hygiene issue #77 contract regression checks independently from native ADR admission and publication.

## State snapshot

Independent base is aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d. Candidate fix/77-contract-regression remains open/draft in PR #87. The containing revision is intentionally null.

## Completed and material changes

tools/check_contracts.py composes full unittest discovery and 24 deterministic reference/generated checks, reports actual counts and failures, and retains bounded diagnostics. The Pages checks job runs that entrypoint at the exact PR head without path filters, with read-only permissions and diagnostic upload. Native/admission/build/deployment definitions remain unchanged. README, Task check and the current HYG-Q03 note identify the same gate; the August roadmap snapshot is byte-preserved. Tracker #76 owns carried follow-ups.

## Validation and review evidence

194 baseline tests passed with no skips. Seven expected failures exposed the absent entrypoint; later implementation controls pass. 201 tests across all thirteen current modules passed with zero skips; all 25 planned command checks passed. Actual copied-source controls reject invalid catalog/profile, stale output, failed/empty discovery and preserve explicit skip counts. Exact-head/read-only/unfiltered wiring is checked; every other workflow job/event and the historical roadmap block remain unchanged. New source lint/format and continuity constraints pass.

## Blockers, risks, unknowns, and deferred work

Independent final review and combined batch qualification remain pending. Hosted changed-head execution and provider required-check configuration are unverified; no dispatch was performed. Native source authority and publication retain independent gates. #47 retains original ADR-0001 human/source-admission/publication acceptance. ADR not required: existing contract/reference behavior and regression wiring are repaired without changing ownership or policy authority.

## Next dependency-ready work

Complete independent source review and combined #77–#79 qualification, then keep the three drafts open for maintainer sync; do not start #80–#85.

## Parallel changes and reconciliation

Issues #78 and #79 are independent candidates from the same main. Reconcile their CONTINUITY snapshots semantically before any future merge. Audit PR #75 remains a separate untouched draft.

## Privacy and redaction

Only public-safe source facts and check summaries are retained. Raw logs, reports, private paths, environment values and credentials remain outside tracked source.

## Handoff update protocol

After domain validation and immediately before PR handoff, refresh exact results, limitations, live source and next action. Check pinned Aether schema, twelve sections and budgets.

## Compaction and supersession

Replace stale current-state prose; preserve detailed history in Git and tracker links. Keep this checkpoint within 240 lines and 16,384 UTF-8 bytes.
