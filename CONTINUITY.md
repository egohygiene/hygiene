---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:50:42Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Make continuity exception assessment dates reproducible, inspectable and safe through the existing
    API and CLI.
  includes:
  - Eight new assessment methods and a clearly synthetic fixed-expiry fixture expose the historical implicit
    clock, absent CLI date path/reporting and invalid-context fallbacks. No production implementation
    has changed yet.
  excludes:
  - Policy/update/approval/expiry source-date rewriting, Aether protocol changes, policy promotion, unrelated81/82
    implementation and83–85.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/REPOSITORY_CONTINUITY.md
  - catalog/repository-continuity-policy.json
  - https://github.com/egohygiene/hygiene/issues/80
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: Make continuity exception assessment dates reproducible, inspectable and safe through the
    existing API and CLI.
  success_conditions:
  - Fixed before/at/after expiry API and CLI assessments agree and disclose the represented date.
  - Current UTC and explicit frozen date paths reject invalid/unavailable context without granting an
    expired or unapproved exemption.
  active_issue:
    provider: github
    id: egohygiene/hygiene#80
    url: https://github.com/egohygiene/hygiene/issues/80
  next:
    kind: action
    id: implement-assessment-clock
    description: Implement the current-UTC/default and explicit frozen-date path, strict date/context
      diagnostics and visible result metadata, then qualify before review.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/80
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-10-30T22:50:42Z'
  candidate:
    branch: fix/80-continuity-assessment
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T22:50:42Z'
    default_branch_revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    issue_state: open
    pull_request_state: not-applicable
    notes: Main is verified after the ordered87/88/86 merges. Original77–79 issues are consolidated into76.
      This new80 candidate is not merged;81/82 are independent peers.
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
  - provider: github
    id: egohygiene/hygiene#81
    url: https://github.com/egohygiene/hygiene/issues/81
  - provider: github
    id: egohygiene/hygiene#82
    url: https://github.com/egohygiene/hygiene/issues/82
review:
  status: partial
  reviewed_at: '2026-10-30T22:50:42Z'
  reviewed_by: Codex
  evidence:
  - command: Merged predecessor full gate and exact main-tree preservation
    outcome: passed
    observed_at: '2026-10-30T22:50:42Z'
    notes: Merged baseline source passed228 tests/all25 command checks with zero skips; source is verified
      atfa41ccc95d0cd0365b38008e02bdc67b928c5ed2.
  - command: python3 -I -m unittest discover --start-directory tests --pattern test_continuity.py --verbose
    outcome: failed
    observed_at: '2026-10-30T22:50:42Z'
    notes: The focused suite ran22 methods. Seventeen failing subcases and six errors are expected on
      the unfixed clock/reporting/CLI path; predecessor controls remain passing.
  environment_limitations:
  - 'Implementation and changed-source qualification are pending. Hosted/ruleset acceptance and the unchanged17-diagnostic
    web-profile schema mismatch remain in76; #47 retains native/source-admission/publication.'
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

Read AGENTS and the continuity policy; verify current main, issue80, the PR and tracker76 before resuming. The prior87/88/86 implementation batch is merged.

## Current objective and success conditions

Make continuity exception assessment dates reproducible, inspectable and safe through the existing API and CLI.

## State snapshot

Independent base isfa41ccc95d0cd0365b38008e02bdc67b928c5ed2. Candidate fix/80-continuity-assessment is in progress before PR creation. The containing revision is intentionally null.

## Completed and material changes

Eight new assessment methods and a clearly synthetic fixed-expiry fixture expose the historical implicit clock, absent CLI date path/reporting and invalid-context fallbacks. No production implementation has changed yet.

## Validation and review evidence

Merged baseline source passed228 tests/all25 command checks with zero skips; source is verified atfa41ccc95d0cd0365b38008e02bdc67b928c5ed2. The focused suite ran22 methods. Seventeen failing subcases and six errors are expected on the unfixed clock/reporting/CLI path; predecessor controls remain passing.

## Blockers, risks, unknowns, and deferred work

Implementation and changed-source qualification are pending. Hosted/ruleset acceptance and the unchanged17-diagnostic web-profile schema mismatch remain in76; #47 retains native/source-admission/publication. ADR not required: this repairs the existing as_of resolver seam and clock reporting without changing policy authority or Aether continuity semantics. Canonical profile dates and the absence of real exceptions remain unchanged.

## Next dependency-ready work

Implement the current-UTC/default and explicit frozen-date path, strict date/context diagnostics and visible result metadata, then qualify before review.

## Parallel changes and reconciliation

Issues81 and82 are independent from the same main; reconcile competing operational continuity snapshots before any later merge. Audit75 remains untouched/open/draft at58d28563206c7b2957867b0a25827b6a08558d66.

## Privacy and redaction

Only public-safe source and check summaries are retained. Synthetic approved-exception fixture data supplies no actual approval. Raw logs, credentials, environment values and private paths remain outside source.

## Handoff update protocol

After domain validation and before PR presentation, refresh actual results, source and next action. Validate exact pinned schema/formats, required sections, privacy and budgets.

## Compaction and supersession

Replace stale current-state prose; Git and tracker76 preserve detailed history. Keep twelve sections within240 lines and16384 UTF-8 bytes.
