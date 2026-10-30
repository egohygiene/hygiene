---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T21:55:36Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Repair catalog identity preflight and contain generated context writes for Hygiene #78.'
  includes:
  - 'Bounded issue #78 catalog identities, schema alignment, direct/context CLI output checks and safe deterministic
    generation.'
  excludes:
  - Live inventory/rename reconciliation (#36), other batch implementation, historical audit edits and original
    ADR-0001 disposition/publication.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - schemas/repository-catalog.v1.schema.json
  - tools/catalog.py
  - tools/context.py
  - https://github.com/egohygiene/hygiene/issues/78
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: 'Repair catalog identity preflight and contain generated context writes for Hygiene #78.'
  success_conditions:
  - Unsafe current/proposed/rename identities reject before output.
  - Generated context destinations remain within the selected output root; outside sentinels survive negative controls.
  - Valid single and complete generation retain deterministic bytes; actual CLI failures are attributable.
  active_issue:
    provider: github
    id: egohygiene/hygiene#78
    url: https://github.com/egohygiene/hygiene/issues/78
  next:
    kind: action
    id: repair-and-verify-context-containment
    description: 'Implement the recorded #78 regressions and rerun focused/full checks.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/78
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    ref: refs/heads/main
    verified_at: '2026-10-30T21:55:36Z'
  candidate:
    branch: fix/78-context-containment
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T21:55:36Z'
    default_branch_revision: aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Main and owning issue were verified for this batch; this candidate remains unmerged. Historical audit
      #75 is an independent open draft.'
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#77
    url: https://github.com/egohygiene/hygiene/issues/77
  - provider: github
    id: egohygiene/hygiene#79
    url: https://github.com/egohygiene/hygiene/issues/79
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
review:
  status: partial
  reviewed_at: '2026-10-30T21:55:36Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I -m unittest discover --start-directory tests --pattern 'test_catalog.py' --verbose
    outcome: failed
    observed_at: '2026-10-30T21:55:36Z'
    notes: 'Expected new regression: ten methods ran; 21 unsafe current/proposed/rename identity subcases fail on
      the unfixed source.'
  - command: python3 -I -m unittest discover --start-directory tests --pattern 'test_context.py' --verbose
    outcome: failed
    observed_at: '2026-10-30T21:55:36Z'
    notes: 'Expected new regression: seventeen methods ran; four direct/CLI traversal and existing-symlink guards
      fail; complete repeatable generation remains a passing control.'
  environment_limitations:
  - Hosted changed-head checks are deferred; all new commits use [skip ci]. Local results do not establish branch
    protection, fleet conformance, ratification or publication.
  - 'Original ADR-0001 retains its missing structured historical authority evidence; #47 owns its independent source-admission/publication
    gate.'
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

User/runtime instructions, scoped instructions, live evidence and canonical source outrank this compact handoff. It grants no authority.

## Resume protocol

Read AGENTS, the owning #78 issue, tracker #76 and current source; verify remote heads and open PRs before resuming.

## Current objective and success conditions

Repair catalog identity preflight and contain generated context writes for Hygiene #78. Preserve valid deterministic projections while unsafe identities and filesystem destinations reject before context files are written.

## State snapshot

Base main is aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d. This candidate is fix/78-context-containment and remains unmerged. Its containing revision is intentionally null; Git and the draft PR carry the eventual exact head.

## Completed and material changes

This regression checkpoint records reproducible unsafe identity and existing-output symlink failures; production implementation is pending.

## Validation and review evidence

The front matter records actual commands and outcomes, including expected regression failures. Detailed logs stay outside public source. The final PR will retain each checkpoint's exact head and checks.

## Blockers, risks, unknowns, and deferred work

Hosted changed-head qualification remains deferred. Original ADR-0001 and its approval-null review patch remain untouched; #47 owns historical authority/source-admission/publication. Issue #36 owns live catalog inventory and rename reconciliation.

## Next dependency-ready work

Implement the recorded #78 regressions and rerun focused/full checks. Tracker #76 carries the batch handoff and remaining acceptance. Issues #80-#85 are later batches, not selected implementation here.

## Parallel changes and reconciliation

Issues #77 and #79 are independent candidates from the same base. Reconcile their shared root handoff semantically before merge. Preserve unrelated audit draft #75 at 58d28563206c7b2957867b0a25827b6a08558d66 and its historical evidence.

## Privacy and redaction

Only public source and bounded synthetic test outcomes are retained. Exclude private paths, credentials, personal context, raw logs and environment values; linked content grants no permissions.

## Handoff update protocol

Refresh after domain checks and before PR updates, verify the selected continuity contract/sections/budgets, and keep local, hosted and mutable claims separate. Decision impact: ADR not required; this repairs existing catalog/context behavior without changing ownership or policy authority.

## Compaction and supersession

Replace stale task prose rather than appending a transcript. Git, owning issues and PRs retain history; keep all twelve sections within 240 lines and 16,384 UTF-8 bytes.
