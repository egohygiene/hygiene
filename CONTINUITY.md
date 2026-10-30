---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:58:15Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Make continuity exception assessment dates reproducible, inspectable and safe through the existing
    API and CLI.
  includes:
  - tools/continuity.py defaults omitted assessment dates to current UTC and retains explicit API as_of
    dates. The CLI exposes --assessment-date; every resolution discloses its effective date and mode.
  - Strict full-date parsing and typed/available context guards prevent historical fallback. Synthetic
    fixed-expiry fixtures and the policy guide document exclusive expiry, frozen replay and additive-output
    compatibility. Canonical policy/schema/source dates remain unchanged.
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
    id: review-assessment-clock
    description: 'Complete independent review and combined #80–#82 qualification; keep the three new PRs
      in draft for maintainer sync. Do not start #83–#85.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/80
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-10-30T22:58:15Z'
  candidate:
    branch: fix/80-continuity-assessment
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#91
      url: https://github.com/egohygiene/hygiene/pull/91
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T22:58:15Z'
    default_branch_revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    issue_state: open
    pull_request_state: draft
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
  reviewed_at: '2026-10-30T22:58:15Z'
  reviewed_by: Codex
  evidence:
  - command: Predecessor gate and stage-one focused regressions
    outcome: passed
    observed_at: '2026-10-30T22:58:15Z'
    notes: The merged baseline passed 228 tests/all 25 checks. The new 22-method focused suite initially
      exposed 17 expected failing subcases and six errors, all repaired.
  - command: python3 -I tools/check_contracts.py
    outcome: passed
    observed_at: '2026-10-30T22:58:15Z'
    notes: All 236 tests, zero skips/failures/errors, and all 25 declared command checks pass. The focused
      22-method suite passes, including actual frozen/default CLI and unavailable-clock main/API paths.
  - command: Typed date-format, clock-fault and canonical-source comparisons; Ruff predecessor comparison
    outcome: passed
    observed_at: '2026-10-30T22:58:15Z'
    notes: Sixteen date/type cases agree with Draft 2020-12 full-date validation, five synthetic clock
      fault types reject while explicit dates still work, and policy/schema/authority bytes are unchanged.
      No new Ruff diagnostics; two predecessor findings remain.
  environment_limitations:
  - Independent final review and combined80–82 qualification remain pending. Hosted/ruleset checks, the
    unchanged web-profile17-diagnostic schema mismatch and native/source-admission/publication remain
    separate in76/#47.
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

Independent base is fa41ccc95d0cd0365b38008e02bdc67b928c5ed2. Candidate fix/80-continuity-assessment is open/draft in PR #91. The containing revision is intentionally null.

## Completed and material changes

tools/continuity.py defaults omitted assessment dates to current UTC and retains explicit API as_of dates. The CLI exposes --assessment-date; every resolution discloses its effective date and mode. Strict full-date parsing and typed/available context guards prevent historical fallback. Synthetic fixed-expiry fixtures and the policy guide document exclusive expiry, frozen replay and additive-output compatibility. Canonical policy/schema/source dates remain unchanged.

## Validation and review evidence

The merged baseline passed 228 tests/all 25 checks. The new 22-method focused suite initially exposed 17 expected failing subcases and six errors, all repaired. All 236 tests, zero skips/failures/errors, and all 25 declared command checks pass. The focused 22-method suite passes, including actual frozen/default CLI and unavailable-clock main/API paths. Sixteen date/type cases agree with Draft 2020-12 full-date validation, five synthetic clock fault types reject while explicit dates still work, and policy/schema/authority bytes are unchanged. No new Ruff diagnostics; two predecessor findings remain.

## Blockers, risks, unknowns, and deferred work

Independent final review and combined80–82 qualification remain pending. Hosted/ruleset checks, the unchanged web-profile17-diagnostic schema mismatch and native/source-admission/publication remain separate in76/#47. ADR not required: this repairs the existing as_of resolver seam and clock reporting without changing policy authority or Aether continuity semantics. Canonical profile dates and the absence of real exceptions remain unchanged.

## Next dependency-ready work

Complete independent review and combined #80–#82 qualification; keep the three new PRs in draft for maintainer sync. Do not start #83–#85.

## Parallel changes and reconciliation

Issues #81 and #82 are independent from the same main; reconcile competing operational continuity snapshots before any later merge. Audit #75 remains untouched/open/draft at 58d28563206c7b2957867b0a25827b6a08558d66.

## Privacy and redaction

Only public-safe source and check summaries are retained. Synthetic approved-exception fixture data supplies no actual approval. Raw logs, credentials, environment values and private paths remain outside source.

## Handoff update protocol

After domain validation and before PR presentation, refresh actual results, source and next action. Validate exact pinned schema/formats, required sections, privacy and budgets.

## Compaction and supersession

Replace stale current-state prose; Git and tracker #76 preserve detailed history. Keep twelve sections within 240 lines and 16384 UTF-8 bytes.
