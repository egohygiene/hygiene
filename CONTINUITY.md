---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:17:11Z'
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
    id: maintainer-review-batch77-79
    description: 'Review drafts #87, #88, then #86; reconcile operational continuity by live evidence
      before merge and carry any unmet acceptance in #76. Select #80–#82 only after the sync.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/77
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    ref: refs/heads/main
    verified_at: '2026-10-30T22:17:11Z'
  candidate:
    branch: fix/77-contract-regression
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#87
      url: https://github.com/egohygiene/hygiene/pull/87
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-30T22:17:11Z'
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
  reviewed_at: '2026-10-30T22:17:11Z'
  reviewed_by: Codex
  evidence:
  - command: Unchanged baseline and stage-one regression replay
    outcome: passed
    observed_at: '2026-10-30T22:17:11Z'
    notes: All 194 baseline tests passed; seven expected missing-entrypoint regression failures were reproduced
      and repaired.
  - command: python3 -I tools/check_contracts.py and independent helper/workflow review
    outcome: passed
    observed_at: '2026-10-30T22:17:11Z'
    notes: The exact reviewed core passed201 tests/25 checks, zero skips. Independent review found no
      blocker; missing executable, zero-exit/no-test and observed-descendant timeout controls passed.
  - command: 'Combined exact-source gate over final #77/#78/#79 implementation files'
    outcome: passed
    observed_at: '2026-10-30T22:17:11Z'
    notes: 228 tests, zero skips/failures/errors, all25 command checks passed. All16 changed non-handoff
      files match their qualified candidates;169 remaining base files are unchanged. Each real branch
      handoff is independently validated.
  - command: Draft202012 schema definitions and canonical instance comparison with formats
    outcome: limited
    observed_at: '2026-10-30T22:17:11Z'
    notes: All18 schema definitions and eight of nine selected canonical instances passed. Agent-Ready
      Web profile has17 schema additional-property diagnostics, byte-identical to unchanged main; this
      existing mismatch is carried in tracker76.
  - command: Pinned continuity schema/formats/composition, workflow preservation and new-file Ruff/format
      checks
    outcome: passed
    observed_at: '2026-10-30T22:17:11Z'
    notes: Exact schema/sections/privacy/budgets, read-only exact-head unfiltered workflow, unchanged
      other jobs and August snapshot, source lint/format and whitespace checks pass.
  environment_limitations:
  - 'Changed-head hosted execution and provider required-check configuration remain unverified. Current
    reference tools do not establish complete schema conformance: the unchanged Agent-Ready Web profile/schema
    mismatch remains in #76. Native ADR/source admission and publication retain independent #47 gates.
    All three PRs remain drafts for review; #80–#85 remain unstarted.'
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

All 194 baseline tests passed; seven expected missing-entrypoint regression failures were reproduced and repaired. The exact reviewed core passed201 tests/25 checks, zero skips. Independent review found no blocker; missing executable, zero-exit/no-test and observed-descendant timeout controls passed. 228 tests, zero skips/failures/errors, all25 command checks passed. All16 changed non-handoff files match their qualified candidates;169 remaining base files are unchanged. Each real branch handoff is independently validated. All18 schema definitions and eight of nine selected canonical instances passed. Agent-Ready Web profile has17 schema additional-property diagnostics, byte-identical to unchanged main; this existing mismatch is carried in tracker76. Exact schema/sections/privacy/budgets, read-only exact-head unfiltered workflow, unchanged other jobs and August snapshot, source lint/format and whitespace checks pass.

## Blockers, risks, unknowns, and deferred work

Changed-head hosted execution and provider required-check configuration remain unverified. Current reference tools do not establish complete schema conformance: the unchanged Agent-Ready Web profile/schema mismatch remains in #76. Native ADR/source admission and publication retain independent #47 gates. All three PRs remain drafts for review; #80–#85 remain unstarted. #47 retains original ADR-0001 human/source-admission/publication acceptance. ADR not required: existing contract/reference behavior and regression wiring are repaired without changing ownership or policy authority.

## Next dependency-ready work

Review drafts #87, #88, then #86; reconcile operational continuity by live evidence before merge and carry any unmet acceptance in #76. Select #80–#82 only after the sync.

## Parallel changes and reconciliation

Issues #78 and #79 are independent candidates from the same main. Reconcile their CONTINUITY snapshots semantically before any future merge. Audit PR #75 remains a separate untouched draft.

## Privacy and redaction

Only public-safe source facts and check summaries are retained. Raw logs, reports, private paths, environment values and credentials remain outside tracked source.

## Handoff update protocol

After domain validation and immediately before PR handoff, refresh exact results, limitations, live source and next action. Check pinned Aether schema, twelve sections and budgets.

## Compaction and supersession

Replace stale current-state prose; preserve detailed history in Git and tracker links. Keep this checkpoint within 240 lines and 16,384 UTF-8 bytes.
