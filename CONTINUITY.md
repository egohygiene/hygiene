---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-13T03:16:33Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify exact release-owner composition and repair the real Task handoff parse
  includes:
  - The current implementation composes the immutable Aether 8a2a3d08f3aa9da3847bd5277843506ab855192e validator/schema/runtime
    lock. The isolated selected dependencies are jsonschema 4.10.3, PyYAML 6.0.1, attrs 22.2.0 and pyrsistent
    0.20.0; no weaker optional fallback supplies success.
  - 'Actual Task 3.54.0 initially rejected .tasks/release.yml: the unquoted Handoff only: echo was parsed as
    a YAML command mapping. A block scalar preserves the exact shell handoff text. A regression checks shipped
    command shapes so colons cannot silently become mapping keys.'
  - The actual release:plan, release:prepare and release:verify Task entries passed with the pinned source/runtime.
    Plan/prepare/verify use version 1.0.0-alpha.1 solely as a read-only candidate argument. The fourth entry
    delegates to release:verify and prints a manual handoff; it is inspected but deliberately not invoked.
  - Positive declaration evidence names the exact executed owner and engines. Negative cases cover wrong tasks,
    empty authority, unknown/duplicate JSON, altered/missing owner source and weaker fallback. Structural YAML
    controls cover block/inline/quoted/comment/manual and forbidden automatic/duplicate triggers.
  excludes:
  - Human policy/ADR disposition, exception approval, source-hold waiver, consumer rollout and publication
  - Hosted CI/ruleset proof and broad provider/production/native qualification
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
  - docs/evidence/2026-11-13-hygiene-84.md
  - https://github.com/egohygiene/hygiene/issues/84
  - https://github.com/egohygiene/hygiene/issues/76
  - https://github.com/egohygiene/hygiene/issues/47
work:
  objective: Qualify exact release-owner composition and repair the real Task handoff parse
  success_conditions:
  - Resolve the selected bounded current-source gap or qualify the already merged repair with actual checks
  - Preserve canonical ownership, historical audits, source clocks, accepted policy and human dispositions
  - Retain every external/hosted/native/human gate explicitly in its owning issue
  active_issue:
    provider: github
    id: egohygiene/hygiene#84
    url: https://github.com/egohygiene/hygiene/issues/84
  next:
    kind: action
    id: review-hygiene-84-checkpoint
    description: Obtain exact-head peer review, then let the coordinating maintainer integrate this bounded
      slice and record actual merged/remaining issue acceptance. Continue the other selected Hygiene slices
      without treating source landing as hosted or human approval.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/84
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: 2eb965989603d4da922f34a27d66c113c1f5358f
    ref: refs/heads/main
    verified_at: '2026-11-13T03:16:33Z'
  candidate:
    branch: codex/hygiene-84-qualification
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-13T03:16:33Z'
    default_branch_revision: 2eb965989603d4da922f34a27d66c113c1f5358f
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Remote main and issue state were freshly inspected for this batch. Hosting #108 and duplicate-record
      checkpoint #109 are merged at the observed base; its owner source and proposed ADR0020 remain intact.
      This checkpoint describes a prepared candidate before PR creation, not an already merged change. The
      user authorizes focused local checks; broader provider/native/publication and human authority stay separate.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-13T03:16:33Z'
  reviewed_by: Codex
  evidence:
  - command: 7 issue-scoped suite/CLI/selected-runtime command invocations
    outcome: passed
    observed_at: '2026-11-13T03:16:33Z'
    notes: 16 focused tests passed without skips; actual command details and coverage are retained in docs/evidence/2026-11-13-hygiene-84.md.
      Other dated receipts remain historical.
  - command: Hosted CI/rulesets, exact EgoLint native source admission, real approval/consumer/publication
      qualification
    outcome: not-run
    observed_at: '2026-11-13T03:16:33Z'
    notes: Not implied by local reference checks. No provider workflow, publication, policy ratification or
      human disposition is performed.
  environment_limitations:
  - 'No release:publish, tag, release, workflow dispatch, deployment, credential action or immutable artifact
    overwrite was performed. Proposed policy and ADR-0015 retain their dispositions; later successor policy
    #65 is separate.'
  - 'The broader gate at merged #109 source failed (295 tests, 14 failures/7 errors; four of 25 checks failed)
    because hosting inputs lack three context dependency mappings and one context test expects an old index.
    Health owns the bounded follow-up; no full-gate pass is claimed.'
  - 'ADR-0001 historical source and human approval/publication hold remains #47; Agent-Ready Web lifecycle
    review remains #95.'
  - 'The parent #76 retains hosted/ruleset and exact native replay carryovers; unrelated organization census/rollout
    is not claimed.'
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

User/runtime, scoped instructions, live evidence and canonical sources outrank this compact handoff. It grants no human approval or publication authority.

## Resume protocol

Read AGENTS, ROADMAP, accepted policy/ratification, the architecture authority map and issue #76. Refresh exact source and PR state before further edits or integration.

## Current objective and success conditions

Qualify exact release-owner composition and repair the real Task handoff parse. Keep actual qualification and source changes distinguishable from human disposition and provider/publication proof.

## State snapshot

Observed main `2eb965989603d4da922f34a27d66c113c1f5358f` includes merged hosting #108 and duplicate-record checkpoint #109. This branch `codex/hygiene-84-qualification` is a prepared candidate; no new PR or merge identity is invented. The six earlier audit/continuity/presentation/ADR/change-history/documentation source merges remain intact.

## Completed and material changes

The current implementation composes the immutable Aether 8a2a3d08f3aa9da3847bd5277843506ab855192e validator/schema/runtime lock. The isolated selected dependencies are jsonschema 4.10.3, PyYAML 6.0.1, attrs 22.2.0 and pyrsistent 0.20.0; no weaker optional fallback supplies success.

Actual Task 3.54.0 initially rejected .tasks/release.yml: the unquoted Handoff only: echo was parsed as a YAML command mapping. A block scalar preserves the exact shell handoff text. A regression checks shipped command shapes so colons cannot silently become mapping keys.

The actual release:plan, release:prepare and release:verify Task entries passed with the pinned source/runtime. Plan/prepare/verify use version 1.0.0-alpha.1 solely as a read-only candidate argument. The fourth entry delegates to release:verify and prints a manual handoff; it is inspected but deliberately not invoked.

Positive declaration evidence names the exact executed owner and engines. Negative cases cover wrong tasks, empty authority, unknown/duplicate JSON, altered/missing owner source and weaker fallback. Structural YAML controls cover block/inline/quoted/comment/manual and forbidden automatic/duplicate triggers.

## Validation and review evidence

All 7 recorded local command invocations passed with 16 focused tests and zero skips/failures/errors. See [docs/evidence/2026-11-13-hygiene-84.md](docs/evidence/2026-11-13-hygiene-84.md) for exact scope and selected runtimes. Independent exact-head review is requested separately; it is not self-certified here.

## Blockers, risks, unknowns, and deferred work

No release:publish, tag, release, workflow dispatch, deployment, credential action or immutable artifact overwrite was performed. Proposed policy and ADR-0015 retain their dispositions; later successor policy #65 is separate. The separate full gate on merged #109 failed on missing hosting/context mappings and a stale context test index; Health owns that repair. No full-gate pass is claimed.  ADR-0001 #47 and Web lifecycle #95 human gates remain unchanged. Hosted/native/consumer acceptance is not inferred from local reference checks.

## Next dependency-ready work

Obtain exact-head peer review, then let the coordinating maintainer integrate this bounded slice and record actual merged/remaining issue acceptance. Continue the other selected Hygiene slices without treating source landing as hosted or human approval.

## Parallel changes and reconciliation

Other selected issues #76/#80/#81/#82/#83/#84 proceed in separate slices. Reconcile shared continuity/roadmap semantically at integration. Hosting #108 owner files, all dated audit bytes, frozen pins and accepted human dispositions are preserved. ADR not required: routine repair/qualification under ADR-0002 and existing proposed profiles; no new policy choice.

## Privacy and redaction

Only public source, synthetic controls and bounded check results are retained. Exclude credentials, private identities, raw private paths and unrelated context. No live URL capability is executed by these syntax tests.

## Handoff update protocol

Refresh exact head, remote main, PR/review observations and check scope at integration. A future merge does not retroactively qualify a later tree or alter a historical report.

## Compaction and supersession

Git, immutable audits and owning issues retain history. Replace stale current prose; keep these twelve sections within 240 lines and 16,384 UTF-8 bytes.
