---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T21:55:18Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Complete Hygiene issue #77 contract regression checks independently from native ADR admission
    and publication.'
  includes:
  - 'The candidate adds seven actual-gate regression controls covering new test discovery/skips, invalid
    catalog/profile, stale generated output, failed/empty suites and bounded retained diagnostics. The
    shared tracker #76 now owns carried follow-ups; no original closes before review/merge.'
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
    id: implement-contract-regression
    description: Implement the complete read-only local/PR regression gate, then run actual positive/negative
      controls before review.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/77
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    ref: refs/heads/main
    verified_at: '2026-10-30T21:55:18Z'
  candidate:
    branch: fix/77-contract-regression
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T21:55:18Z'
    default_branch_revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    issue_state: open
    pull_request_state: not-applicable
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
  reviewed_at: '2026-10-30T21:55:18Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I -m unittest discover --start-directory tests --pattern test_*.py --verbose (unchanged
      baseline)
    outcome: passed
    observed_at: '2026-10-30T21:55:18Z'
    notes: All 194 baseline tests passed with no skips.
  - command: python3 -I -m unittest discover --start-directory tests --pattern test_contract_regression.py
      --verbose
    outcome: failed
    observed_at: '2026-10-30T21:55:18Z'
    notes: All seven new tests fail as expected because the complete gate entrypoint is absent.
  environment_limitations:
  - Implementation and changed-source validation are pending. Hosted changed-head execution and provider
    branch protection remain unverified. Native source authority and publication stay independently gated.
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

Independent base is aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d. Candidate fix/77-contract-regression remains in progress before PR creation. The containing revision is intentionally null.

## Completed and material changes

The candidate adds seven actual-gate regression controls covering new test discovery/skips, invalid catalog/profile, stale generated output, failed/empty suites and bounded retained diagnostics. The shared tracker #76 now owns carried follow-ups; no original closes before review/merge.

## Validation and review evidence

All 194 baseline tests passed with no skips. All seven new tests fail as expected because the complete gate entrypoint is absent.

## Blockers, risks, unknowns, and deferred work

Implementation and changed-source validation are pending. Hosted changed-head execution and provider branch protection remain unverified. Native source authority and publication stay independently gated. #47 retains original ADR-0001 human/source-admission/publication acceptance. ADR not required: existing contract/reference behavior and regression wiring are repaired without changing ownership or policy authority.

## Next dependency-ready work

Implement the complete read-only local/PR regression gate, then run actual positive/negative controls before review.

## Parallel changes and reconciliation

Issues #78 and #79 are independent candidates from the same main. Reconcile their CONTINUITY snapshots semantically before any future merge. Audit PR #75 remains a separate untouched draft.

## Privacy and redaction

Only public-safe source facts and check summaries are retained. Raw logs, reports, private paths, environment values and credentials remain outside tracked source.

## Handoff update protocol

After domain validation and immediately before PR handoff, refresh exact results, limitations, live source and next action. Check pinned Aether schema, twelve sections and budgets.

## Compaction and supersession

Replace stale current-state prose; preserve detailed history in Git and tracker links. Keep this checkpoint within 240 lines and 16,384 UTF-8 bytes.
