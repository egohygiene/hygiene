---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:37:51Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Integrate the approved context identity/output repair with the accepted complete regression
    gate.
  includes:
  - Catalog schema/reference validation rejects unsafe current/proposed/rename identities. The context
    writer preflights all direct-child destinations, rejects links/nonregular output, and replaces same-directory
    entries without writing through outside hard links. Stable caller-owned ancestors and nontransactional
    batch limits remain documented.
  - Reviewed source 84f193d523cb990ea90bb6a615d59f33bf925bd9 integrates with accepted main 949cd4ae45b48bfdbdfac3edcfbd08ff330652a1;
    qualified non-handoff bytes are preserved.
  excludes:
  - 'Audit PR #75 and original ADR-0001 disposition; unrelated policy changes, hosted dispatch, releases
    and publication.'
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/decisions/POLICY.md
  - https://github.com/egohygiene/hygiene/issues/76
  - https://github.com/egohygiene/hygiene/issues/78
work:
  objective: Integrate the approved context identity/output repair with the accepted complete regression
    gate.
  success_conditions:
  - Preserve reviewed implementation and canonical source while integrating accepted predecessor work.
  - Pass the complete merged-source gate and exact continuity schema, then execute the authorized ordered
    merge.
  active_issue:
    provider: github
    id: egohygiene/hygiene#78
    url: https://github.com/egohygiene/hygiene/issues/78
  next:
    kind: action
    id: finish-context-merge
    description: Finish the merged-source checks and authorized merge88, then integrate86. Consolidate77–79
      into tracker76 and start the requested80–82 batch only from verified final main.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/76
    - https://github.com/egohygiene/hygiene/pull/88
    depends_on: []
state:
  base:
    revision: 949cd4ae45b48bfdbdfac3edcfbd08ff330652a1
    ref: refs/heads/main
    verified_at: '2026-10-30T22:37:51Z'
  candidate:
    branch: fix/78-context-containment
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#88
      url: https://github.com/egohygiene/hygiene/pull/88
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-30T22:37:51Z'
    default_branch_revision: 949cd4ae45b48bfdbdfac3edcfbd08ff330652a1
    issue_state: open
    pull_request_state: draft
    notes: PR87 is merged at949cd4a; PR88 remains open/draft and source-preserving reconciliation is in
      progress. PR86 and audit75 remain open/draft.
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#86
    url: https://github.com/egohygiene/hygiene/pull/86
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
review:
  status: partial
  reviewed_at: '2026-10-30T22:37:51Z'
  reviewed_by: Codex
  evidence:
  - command: Reviewed source and main/API/tree comparison
    outcome: passed
    observed_at: '2026-10-30T22:37:51Z'
    notes: PR87 merged949cd4ae45b48bfdbdfac3edcfbd08ff330652a1 from reviewed e22e31f; main tree matched
      that checked candidate. This integration preserves original78 source84f193d and all qualified gate
      bytes. Only operational continuity needs manual reconciliation.
  - command: python3 -I tools/check_contracts.py (merged source)
    outcome: passed
    observed_at: '2026-10-30T22:37:51Z'
    notes: Fresh merged-source gate passed 217 tests with zero skips and all 25 declared command checks;
      qualified implementation bytes and Git executable roles match the reviewed source.
  - command: Pinned continuity schema/formats, section/privacy/budget and whitespace checks
    outcome: passed
    observed_at: '2026-10-30T22:37:51Z'
    notes: Exact upstream schema and local composition are verified before this checkpoint is committed.
  - command: Additional canonical Agent-Ready Web schema consistency
    outcome: limited
    observed_at: '2026-10-30T22:37:51Z'
    notes: The unchanged predecessor profile/schema pair still has17 additional-property diagnostics.
      Tracker76 retains this failed broader consistency check; no whole-repository conformance is claimed.
  environment_limitations:
  - 'Hosted changed-head execution and provider required-check evidence remain deferred. Native source
    admission/publication and original ADR-0001 approval remain separate under #47.'
  - All new commits use [skip ci]. This accepted source merge creates no tag/release, workflow dispatch,
    deployment or publication.
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

User/runtime instructions, scoped instructions, live evidence and canonical sources outrank this compact operational handoff. It grants no authority.

## Resume protocol

Read AGENTS and canonical policy, verify current main and PR state, then inspect tracker #76 and the owning PR before resuming.

## Current objective and success conditions

Integrate the approved context identity/output repair with the accepted complete regression gate.

## State snapshot

Observed main is 949cd4ae45b48bfdbdfac3edcfbd08ff330652a1. Candidate fix/78-context-containment integrates reviewed source 84f193d523cb990ea90bb6a615d59f33bf925bd9 in open draft PR #88; it is not yet merged. The containing revision remains null.

## Completed and material changes

Catalog schema/reference validation rejects unsafe current/proposed/rename identities. The context writer preflights all direct-child destinations, rejects links/nonregular output, and replaces same-directory entries without writing through outside hard links. Stable caller-owned ancestors and nontransactional batch limits remain documented. PR87 merged949cd4ae45b48bfdbdfac3edcfbd08ff330652a1 from reviewed e22e31f; main tree matched that checked candidate. This integration preserves original78 source84f193d and all qualified gate bytes. Only operational continuity needs manual reconciliation.

## Validation and review evidence

Fresh merged-source gate passed 217 tests with zero skips and all 25 declared command checks; qualified implementation bytes and Git executable roles match the reviewed source. Independent source review and earlier actual CLI/negative controls remain attributed to their exact inputs in the PR. Final continuity schema/formats and budgets are checked separately.

## Blockers, risks, unknowns, and deferred work

Hosted/ruleset evidence is unavailable/deferred. The additional web-profile schema check remains failed with17 unchanged predecessor diagnostics and is carried in #76. #47 retains original ADR-0001 approval, native source-admission and publication gates. ADR not required: source-preserving integration and operational handoff reconciliation implement already reviewed repairs.

## Next dependency-ready work

Finish the merged-source checks and authorized merge88, then integrate86. Consolidate77–79 into tracker76 and start the requested80–82 batch only from verified final main.

## Parallel changes and reconciliation

Known open work is linked above. Audit PR #75 remains untouched/open/draft at58d28563206c7b2957867b0a25827b6a08558d66. Reconcile remaining continuity snapshots semantically before merging.

## Privacy and redaction

Only public-safe source facts and result summaries are retained. Raw logs, reports, credentials, environment values and private machine paths remain outside source.

## Handoff update protocol

After domain validation and before PR presentation, refresh exact source/checks and next action. Validate the exact pinned Aether schema, all required sections, privacy and budgets.

## Compaction and supersession

Replace stale state; Git and tracker76 retain detailed history. Keep twelve sections within240 lines and16384 UTF-8 bytes.
