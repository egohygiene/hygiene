---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T23:20:13Z'
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
    id: review-batch80-82
    description: 'Review draft PRs #91, #89, then #90; reconcile continuity snapshots before a later authorized
      merge and keep all unmet acceptance in #76. Select #83–#85 only after the maintainer sync.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/80
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-10-30T23:20:13Z'
  candidate:
    branch: fix/80-continuity-assessment
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#91
      url: https://github.com/egohygiene/hygiene/pull/91
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-30T23:20:13Z'
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
  reviewed_at: '2026-10-30T23:20:13Z'
  reviewed_by: Codex
  evidence:
  - command: Merged baseline and stage-one focused regressions
    outcome: passed
    observed_at: '2026-10-30T23:20:13Z'
    notes: Merged baseline source passed 228 tests/all 25 checks. Twenty-two focused methods initially
      exposed 17 expected failing subcases and six errors; all are repaired.
  - command: Complete local gate and independent assessment-date review at 67b6afe212166cf540b04bc996beacaa5419a496
    outcome: passed
    observed_at: '2026-10-30T23:20:13Z'
    notes: 236 tests, zero skips/failures/errors and all 25 declared checks pass. Independent review is
      clear; 22 control groups plus six invalid API types cover UTC/TZ behavior, fixed CLI/API repetitions,
      all clock failures, expiry boundaries and nonapproved states.
  - command: 'Combined exact-source gate over #80/#81/#82 candidates'
    outcome: passed
    observed_at: '2026-10-30T23:20:13Z'
    notes: 256 tests, zero skips/failures/errors and all 25 checks passed. All 22 changed non-handoff
      files/Git roles match the qualified candidates; 172 other base files are unchanged. Actual branch
      handoffs are validated separately.
  - command: Date-format/schema and canonical metadata checks
    outcome: limited
    observed_at: '2026-10-30T23:20:13Z'
    notes: Sixteen date/type checks agree with full-date schema validation; 18 schema definitions, seven
      of eight canonical profiles, two presentation fixtures, six ADR fixtures and 13 actual decoded front-matter
      records pass. The unchanged web profile retains 17 schema diagnostics; original ADR-0001 lacks front
      matter. These are structural observations, not native admission or approval authentication.
  - command: Pinned continuity schema/formats/composition and optional Ruff predecessor comparison
    outcome: passed
    observed_at: '2026-10-30T23:20:13Z'
    notes: Exact schema, required sections, privacy and budgets pass. No new optional Ruff diagnostics;
      two predecessor findings remain. Canonical source dates/policy/schema/authority and historical evidence
      bytes are preserved.
  environment_limitations:
  - 'Hosted/ruleset acceptance, baseline web-profile/schema mismatch, duplicate presentation-record mismatch
    and fail-closed ADR reference-newline schema mismatch remain tracked in #76. Exact selected native
    d917 replay is unavailable; #47 retains original ADR-0001/source-admission/publication.'
  - 'All three new PRs remain drafts; no new merge/closure, workflow dispatch, release/tag, deployment
    or publication. #83–#85 remain unstarted.'
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

Merged baseline source passed 228 tests/all 25 checks. Twenty-two focused methods initially exposed 17 expected failing subcases and six errors; all are repaired. 236 tests, zero skips/failures/errors and all 25 declared checks pass. Independent review is clear; 22 control groups plus six invalid API types cover UTC/TZ behavior, fixed CLI/API repetitions, all clock failures, expiry boundaries and nonapproved states. 256 tests, zero skips/failures/errors and all 25 checks passed. All 22 changed non-handoff files/Git roles match the qualified candidates; 172 other base files are unchanged. Actual branch handoffs are validated separately. Sixteen date/type checks agree with full-date schema validation; 18 schema definitions, seven of eight canonical profiles, two presentation fixtures, six ADR fixtures and 13 actual decoded front-matter records pass. The unchanged web profile retains 17 schema diagnostics; original ADR-0001 lacks front matter. These are structural observations, not native admission or approval authentication. Exact schema, required sections, privacy and budgets pass. No new optional Ruff diagnostics; two predecessor findings remain. Canonical source dates/policy/schema/authority and historical evidence bytes are preserved.

## Blockers, risks, unknowns, and deferred work

Hosted/ruleset acceptance, baseline web-profile/schema mismatch, duplicate presentation-record mismatch and fail-closed ADR reference-newline schema mismatch remain tracked in #76. Exact selected native d917 replay is unavailable; #47 retains original ADR-0001/source-admission/publication. All three new PRs remain drafts; no new merge/closure, workflow dispatch, release/tag, deployment or publication. #83–#85 remain unstarted. ADR not required: this repairs the existing as_of resolver seam and clock reporting without changing policy authority or Aether continuity semantics. Canonical profile dates and the absence of real exceptions remain unchanged.

## Next dependency-ready work

Review draft PRs #91, #89, then #90; reconcile continuity snapshots before a later authorized merge and keep all unmet acceptance in #76. Select #83–#85 only after the maintainer sync.

## Parallel changes and reconciliation

Issues #81 and #82 are independent from the same main; reconcile competing operational continuity snapshots before any later merge. Audit #75 remains untouched/open/draft at 58d28563206c7b2957867b0a25827b6a08558d66.

## Privacy and redaction

Only public-safe source and check summaries are retained. Synthetic approved-exception fixture data supplies no actual approval. Raw logs, credentials, environment values and private paths remain outside source.

## Handoff update protocol

After domain validation and before PR presentation, refresh actual results, source and next action. Validate exact pinned schema/formats, required sections, privacy and budgets.

## Compaction and supersession

Replace stale current-state prose; Git and tracker #76 preserve detailed history. Keep twelve sections within 240 lines and 16384 UTF-8 bytes.
