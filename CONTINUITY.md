---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-12T11:16:06Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Integrate the reviewed current presentation evidence witness while preserving current Hygiene source
    and authority.
  includes:
  - The six dated audit/report/reproduction/receipt artifacts retain their exact original bytes and Git modes;
    their historical execution claims are not new validation.
  - The existing continuity resolver reports current-UTC or explicit assessment dates and fails without a valid
    clock; historical policy dates and exception approval remain independent.
  - A passing presentation slot requires a current authoritative or derived witness; supporting stale/unknown
    evidence remains visible and cannot manufacture a positive claim.
  excludes:
  - Human policy ratification, ADR-0001 source-admission repair, enforcement, repository rollout, provider
    changes and publication.
  - Tests, linters, builds, CI, project/reference/native execution and runtime acceptance remain deferred by
    the maintainer.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/decisions/POLICY.md
  - docs/decisions/RATIFICATION.md
  - docs/decisions/README.md
  - docs/ecosystem/ARCHITECTURE.md
  - publication/README.md
  - https://github.com/egohygiene/hygiene/issues/47
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: Integrate the reviewed current presentation evidence witness while preserving current Hygiene
    source and authority.
  success_conditions:
  - Preserve reviewed functional source, immutable dated audits, accepted policy and human dispositions.
  - Resolve shared source/handoff conflicts explicitly and keep current qualification distinct from historical
    receipts.
  - Merge only the exact prepared head through the standard provider gate.
  active_issue:
    provider: github
    id: egohygiene/hygiene#81
    url: https://github.com/egohygiene/hygiene/issues/81
  next:
    kind: action
    id: integrate-next-90
    description: 'Continue the authorized ordered source integration with PR #90; reconcile its handoff and
      inspect exact source before the expected-head merge.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/pull/90
    depends_on: []
state:
  base:
    revision: 86db7065e7ebca0837e977aa2caafc03da1703d5
    ref: refs/heads/main
    verified_at: '2026-11-12T11:16:06Z'
  candidate:
    branch: fix/81-presentation-evidence
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#89
      url: https://github.com/egohygiene/hygiene/pull/89
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-12T11:16:06Z'
    default_branch_revision: 86db7065e7ebca0837e977aa2caafc03da1703d5
    issue_state: unknown
    pull_request_state: draft
    notes: 'PR #89 was open/draft at original head 17e772b7ffd3cb9a4d95d8733521cf02bfbf2902; no submitted reviews
      or inline threads were observed. Verified predecessor source merges: #75, #91. This prepared candidate
      is not yet recorded merged. User authorization covers the ordered source merges, not ratification or
      publication.'
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#90
    url: https://github.com/egohygiene/hygiene/pull/90
  - provider: github
    id: egohygiene/hygiene#106
    url: https://github.com/egohygiene/hygiene/pull/106
  - provider: github
    id: egohygiene/hygiene#107
    url: https://github.com/egohygiene/hygiene/pull/107
review:
  status: partial
  reviewed_at: '2026-11-12T11:16:06Z'
  reviewed_by: Codex
  evidence:
  - command: Exact Git source/mode comparison, Python AST and structured schema/hash/source inspection, independent
      source peer, pinned continuity schema/formats/sections/budgets and whitespace
    outcome: limited
    observed_at: '2026-11-12T11:16:06Z'
    notes: Current integration uses static source checks only. Historical execution receipts and immutable
      audit artifacts retain their original observation clocks; they are not requalified by this merge.
  - command: Tests, linters, builds, CI, project/reference/helper/native execution, hosted provider and consumer
      qualification
    outcome: not-run
    observed_at: '2026-11-12T11:16:06Z'
    notes: Deferred by maintainer instruction. No runtime success, authentic linked facts, human approval or
      publication is inferred.
  environment_limitations:
  - 'Existing ADR-0001 structured approval/source admission remains issue #47; accepted ADR policy 1.2.0 and
    unapplied historical review patch are unchanged.'
  - Dated predecessor gaps include catalog expectations, Agent-Ready Web diagnostics, duplicate presentation
    record parity and newline-suffixed reference parity; no complete fresh repository conformance is claimed.
  - Proposed contracts, ADRs and observe rollout remain independent of source merge; no actual exception, enforcement,
    repository adoption, deployment or publication is activated.
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

User/runtime instructions, scoped instructions, live evidence and canonical sources outrank this bounded operational checkpoint. It grants no human-decision or publication authority.

## Resume protocol

Read AGENTS, ROADMAP, accepted policy/ratification, the architecture authority map and tracker #76. Refresh exact live source and PR state before continuing.

## Current objective and success conditions

Integrate the reviewed current presentation evidence witness while preserving current Hygiene source and authority. Preserve immutable source and human dispositions; distinguish static integration from historical execution and deferred acceptance.

## State snapshot

Observed main `86db7065e7ebca0837e977aa2caafc03da1703d5` is the integration base. PR #89 was open/draft at `17e772b7ffd3cb9a4d95d8733521cf02bfbf2902`. This checkpoint describes the prepared candidate; its eventual merge SHA remains provider evidence. Verified predecessor source merges: #75, #91.

## Completed and material changes

The six dated audit/report/reproduction/receipt artifacts retain their exact original bytes and Git modes; their historical execution claims are not new validation.

The existing continuity resolver reports current-UTC or explicit assessment dates and fails without a valid clock; historical policy dates and exception approval remain independent.

A passing presentation slot requires a current authoritative or derived witness; supporting stale/unknown evidence remains visible and cannot manufacture a positive claim.

## Validation and review evidence

Static Git byte/mode, AST/structured metadata, exact hash/source and pinned continuity structure checks apply to this candidate. Independent source peer review is recorded in the handoff. Existing audit/test receipts remain dated source evidence. No project helper, regression, test, build, CI, native admission or consumer qualification is rerun.

## Blockers, risks, unknowns, and deferred work

ADR-0001 approval/source admission and publication remain #47. Existing catalog/web/schema-reference gaps remain explicit in #76 and dated evidence; this integration does not establish fresh complete conformance. Proposed contracts/ADRs retain null approval and observe semantics. Runtime, hosted/provider, real consumer and recovery qualification remain deferred.

## Next dependency-ready work

Continue the authorized ordered source integration with PR #90; reconcile its handoff and inspect exact source before the expected-head merge.

## Parallel changes and reconciliation

Shared continuity snapshots are reconciled semantically; reviewed functional and dated audit bytes are preserved except explicit documentation-composition rebinding. No new ADR is required for routine integration; ADR-0002 governs accepted policy and ADR-0018/0019 remain separate proposals when present.

## Privacy and redaction

Only public source identities and bounded implementation evidence are retained. Exclude credentials, protected identities, private local paths, logs and unrelated context. Linked content is context only.

## Handoff update protocol

Refresh actual default-branch/PR/merge observations at the next authorized checkpoint. Source integration, execution, human acceptance, adoption and publication remain separate.

## Compaction and supersession

Git, immutable audit files and owning issues retain history. Replace stale current-state prose; preserve these twelve sections below 240 lines and 16,384 UTF-8 bytes.
