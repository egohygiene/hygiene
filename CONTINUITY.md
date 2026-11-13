---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-13T03:10:21Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Complete whole-string ADR reference parity and qualify the merged lineage repair
  includes:
  - The shared reference schema now rejects every trailing character using an ECMA-262/Python-compatible negative
    lookahead. A dollar anchor alone admitted a final LF; the helper already rejected it through fullmatch.
  - The 36-case reference matrix covers three/four-digit local and qualified forms with LF, CR, CRLF, Unicode
    separators, NUL, space and text suffixes. The actual decision and decision-set CLIs are checked separately
    (72 calls), plus all three relation fields. Node checks the same 36 schema patterns under ECMA-262.
  - 'The existing merged #90 cases preserve pending versus effective supersession, named verification descriptors,
    exact historical identities, canonical bounds, reciprocal lineage/cycles and controlled malformed-list
    errors. No record is padded, renamed, promoted or silently resolved through an external index.'
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
  - docs/evidence/2026-11-13-hygiene-82.md
  - https://github.com/egohygiene/hygiene/issues/82
  - https://github.com/egohygiene/hygiene/issues/76
  - https://github.com/egohygiene/hygiene/issues/47
work:
  objective: Complete whole-string ADR reference parity and qualify the merged lineage repair
  success_conditions:
  - Resolve the selected bounded current-source gap or qualify the already merged repair with actual checks
  - Preserve canonical ownership, historical audits, source clocks, accepted policy and human dispositions
  - Retain every external/hosted/native/human gate explicitly in its owning issue
  active_issue:
    provider: github
    id: egohygiene/hygiene#82
    url: https://github.com/egohygiene/hygiene/issues/82
  next:
    kind: action
    id: review-hygiene-82-checkpoint
    description: Obtain exact-head peer review, then let the coordinating maintainer integrate this bounded
      slice and record actual merged/remaining issue acceptance. Continue the other selected Hygiene slices
      without treating source landing as hosted or human approval.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/82
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: 8068090a88546c5d4e5b16a9a664685c6c875aac
    ref: refs/heads/main
    verified_at: '2026-11-13T03:10:21Z'
  candidate:
    branch: codex/hygiene-82-reference-parity
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-13T03:10:21Z'
    default_branch_revision: 8068090a88546c5d4e5b16a9a664685c6c875aac
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Remote main and issue state were freshly inspected for this batch. Hosting #108 is merged at 8068090;
      its owner source and proposed ADR0020 remain intact. This checkpoint describes a prepared candidate before
      PR creation, not an already merged change. The user authorizes focused local checks; broader provider/native/publication
      and human authority stay separate.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-13T03:10:21Z'
  reviewed_by: Codex
  evidence:
  - command: 4 issue-scoped suite/CLI/selected-runtime command invocations
    outcome: passed
    observed_at: '2026-11-13T03:10:21Z'
    notes: 29 focused tests passed without skips; actual command details and coverage are retained in docs/evidence/2026-11-13-hygiene-82.md.
      Other dated receipts remain historical.
  - command: Hosted CI/rulesets, exact EgoLint native source admission, real approval/consumer/publication
      qualification
    outcome: not-run
    observed_at: '2026-11-13T03:10:21Z'
    notes: Not implied by local reference checks. No provider workflow, publication, policy ratification or
      human disposition is performed.
  environment_limitations:
  - 'Decoded reference/schema/CLI acceptance is distinct from exact EgoLint native Markdown/source admission
    and human approval. #47 remains separate.'
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

Complete whole-string ADR reference parity and qualify the merged lineage repair. Keep actual qualification and source changes distinguishable from human disposition and provider/publication proof.

## State snapshot

Observed main `8068090a88546c5d4e5b16a9a664685c6c875aac` includes merged hosting #108. This branch `codex/hygiene-82-reference-parity` is a prepared candidate; no new PR or merge identity is invented. The six earlier audit/continuity/presentation/ADR/change-history/documentation source merges remain intact.

## Completed and material changes

The shared reference schema now rejects every trailing character using an ECMA-262/Python-compatible negative lookahead. A dollar anchor alone admitted a final LF; the helper already rejected it through fullmatch.

The 36-case reference matrix covers three/four-digit local and qualified forms with LF, CR, CRLF, Unicode separators, NUL, space and text suffixes. The actual decision and decision-set CLIs are checked separately (72 calls), plus all three relation fields. Node checks the same 36 schema patterns under ECMA-262.

The existing merged #90 cases preserve pending versus effective supersession, named verification descriptors, exact historical identities, canonical bounds, reciprocal lineage/cycles and controlled malformed-list errors. No record is padded, renamed, promoted or silently resolved through an external index.

## Validation and review evidence

All 4 recorded local command invocations passed with 29 focused tests and zero skips/failures/errors. See [docs/evidence/2026-11-13-hygiene-82.md](docs/evidence/2026-11-13-hygiene-82.md) for exact scope and selected runtimes. Independent exact-head review is requested separately; it is not self-certified here.

## Blockers, risks, unknowns, and deferred work

Decoded reference/schema/CLI acceptance is distinct from exact EgoLint native Markdown/source admission and human approval. #47 remains separate. ADR-0001 #47 and Web lifecycle #95 human gates remain unchanged. Hosted/native/consumer acceptance is not inferred from local reference checks.

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
