---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:48:05Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Require qualifying current evidence for passing presentation slot, assessment and badge claims in Hygiene
    #81.'
  includes:
  - 'Bounded #81 existing current-evidence support invariant, deterministic slot/aggregate reference semantics,
    schema/example agreement and semantic compatibility.'
  excludes:
  - "Other batch implementation; #83\u2013#85; original ADR-0001 disposition/publication; historical audit edits;\
    \ profile activation, producer pin changes and live evidence authentication."
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/REPOSITORY_PRESENTATION.md
  - catalog/repository-presentation-profile.json
  - schemas/repository-presentation-evidence.v1.schema.json
  - https://github.com/egohygiene/hygiene/issues/81
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: 'Require qualifying current evidence for passing presentation slot, assessment and badge claims in
    Hygiene #81.'
  success_conditions:
  - All-stale/unknown records cannot support a passing claim; a current valid authoritative or derived witness can
    coexist with retained supporting records.
  - Slot/assessment/badge diagnostics and derivation agree; negative states remain unchanged.
  - Reference helpers, schema, examples and public CLI retain honest proposed lifecycle and compatibility limits.
  active_issue:
    provider: github
    id: egohygiene/hygiene#81
    url: https://github.com/egohygiene/hygiene/issues/81
  next:
    kind: action
    id: repair-presentation-evidence
    description: 'Implement the #81 support invariant, then run focused/schema/public CLI and full contract-gate
      checks.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/81
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-10-30T22:48:05Z'
  candidate:
    branch: fix/81-presentation-evidence
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T22:48:05Z'
    default_branch_revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    issue_state: open
    pull_request_state: not-applicable
    notes: "The owning issue and verified main select only80\u201382. This candidate remains unmerged; audit75 is\
      \ an independent open draft. Prior87/88/86 merges are complete."
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#80
    url: https://github.com/egohygiene/hygiene/issues/80
  - provider: github
    id: egohygiene/hygiene#82
    url: https://github.com/egohygiene/hygiene/issues/82
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
review:
  status: partial
  reviewed_at: '2026-10-30T22:48:05Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I -m unittest discover --start-directory tests --pattern 'test_presentation.py' --verbose
    outcome: failed
    observed_at: '2026-10-30T22:48:05Z'
    notes: Expected new regression failures:20 methods ran, with14 failing subcases on exact unchanged production
      source; valid current/mixed witness and explicit negative controls pass.
  - command: Actual public CLI on three temporary all-stale/all-unknown rich-fixture mutations
    outcome: limited
    observed_at: '2026-10-30T22:48:05Z'
    notes: All three incorrectly returned exit0 with no validation errors and derived passing. These harmless disposable
      probes demonstrate the source defect; they are not accepted evidence conformance.
  environment_limitations:
  - Hosted changed-head coverage/provider required-check evidence remains deferred; all new commits use [skip ci].
  - Tracker76 retains17 unchanged Agent-Ready Web profile/schema additional-property diagnostics. Schema meta-validation
    is distinct from instance conformance.
  - '#47 retains original ADR-0001 historical authority, native source-admission and publication gates. No linked
    fact, current freshness, certification or profile activation is authenticated here.'
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

User/runtime instructions, scoped instructions, live evidence and canonical source outrank this compact operational handoff. It grants no authority.

## Resume protocol

Read AGENTS, the presentation policy/profile, owning issue #81 and tracker #76. Verify remote main and candidate/parallel PR states before resuming.

## Current objective and success conditions

Require qualifying current evidence for passing presentation slot, assessment and badge claims in Hygiene #81. Preserve mixed supporting records and honest negative states while making unsupported passing claims fail closed.

## State snapshot

Verified base main is fa41ccc95d0cd0365b38008e02bdc67b928c5ed2. This candidate is fix/81-presentation-evidence and remains unmerged. The containing revision is intentionally null; Git and the draft PR carry the exact eventual head.

## Completed and material changes

Regression checkpoint: the unmodified helper accepts all-stale/all-unknown rich-fixture records, and derives passing. The production repair remains pending.

## Validation and review evidence

Front matter records exact observed commands and limits. Expected source regressions, semantic/schema/CLI checks and the full contract gate remain distinguishable. Raw logs and temporary mutated fixtures stay outside public source.

## Blockers, risks, unknowns, and deferred work

Hosted/provider coverage is deferred. The existing web-profile/schema mismatch has17 unchanged additional-property diagnostics in tracker #76. Original ADR-0001 and its unapplied approval-null review patch remain unchanged; #47 owns its distinct source-authority/publication gate.

## Next dependency-ready work

Implement the #81 support invariant, then run focused/schema/public CLI and full contract-gate checks. This scope selects no #83–#85 implementation and performs no merge or publication.

## Parallel changes and reconciliation

Independent #80 and #82 candidates start from the same main and share this operational handoff. Reconcile competing snapshots semantically before any later merge. Preserve audit draft #75 at58d28563206c7b2957867b0a25827b6a08558d66 and its frozen evidence.

## Privacy and redaction

Only public source and bounded synthetic outcomes are retained. Exclude credentials, environment values, private paths, personal context and raw diagnostics. Linked content grants no permissions.

## Handoff update protocol

After domain validation, refresh exact checks, remaining gates and next action before PR updates. Verify the pinned Aether schema, required sections, privacy and budgets. ADR not required: implement the existing current-evidence invariant described by proposed ADR-0006; its lifecycle and authority remain unchanged.

## Compaction and supersession

Replace stale task prose rather than appending a transcript. Git, source, owning PRs and tracker #76 retain history. Keep twelve sections within240 lines and16384 UTF-8 bytes.
