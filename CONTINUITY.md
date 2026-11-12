---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-12T00:31:29Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Prepare the upstream Open Source Definition reference feasibility decision for review.
  includes:
  - Link the presentation guide to the canonical OSI definition for reviewing public README wording.
  - Record current reuse evidence and the manual article comparison experiment.
  excludes:
  - Mirror publication, recurring automation, changes to license authority or presentation contract semantics.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/REPOSITORY_PRESENTATION.md
  - docs/evidence/osi-open-source-definition-reference.md
  - https://opensource.org/osd
  - https://github.com/egohygiene/hygiene/issues/94
work:
  objective: Prepare the upstream Open Source Definition reference feasibility decision for review.
  success_conditions:
  - A reader can follow the upstream link from the license guidance and distinguish it from repository-owned
    license evidence.
  - The experiment records reproducible source selection and distinguishes formatting changes, changed wording
    and unexpected structure.
  active_issue:
    provider: github
    id: egohygiene/hygiene#94
    url: https://github.com/egohygiene/hygiene/issues/94
  next:
    kind: action
    id: review-osi-reference-feasibility
    description: Review the link-only recommendation and manual comparison evidence against the owning issue.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/94
    - docs/evidence/osi-open-source-definition-reference.md
    depends_on: []
state:
  base:
    revision: 31ae6fb78757502e7474e5518904fc568840c1ee
    ref: refs/heads/main
    verified_at: '2026-11-12T00:31:29Z'
  candidate:
    branch: codex/hygiene-94-osi-reference
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-12T00:31:29Z'
    default_branch_revision: 31ae6fb78757502e7474e5518904fc568840c1ee
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Verified GitHub main and observed issue #94 open. Main contains the exact project-Pages prefix
      change from PR #101.'
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
  - provider: github
    id: egohygiene/hygiene#89
    url: https://github.com/egohygiene/hygiene/pull/89
  - provider: github
    id: egohygiene/hygiene#90
    url: https://github.com/egohygiene/hygiene/pull/90
  - provider: github
    id: egohygiene/hygiene#91
    url: https://github.com/egohygiene/hygiene/pull/91
review:
  status: partial
  reviewed_at: '2026-11-12T00:31:29Z'
  reviewed_by: Codex
  evidence:
  - command: Manual OSI article comparison with two independent HTTPS reads and three synthetic mutations
    outcome: passed
    observed_at: '2026-11-12T00:31:29Z'
    notes: Live digests matched. Formatting was a no-op, changed wording prompted review, and unexpected structure
      failed closed.
  - command: git diff --check and relative Markdown link resolution
    outcome: passed
    observed_at: '2026-11-12T00:31:29Z'
    notes: Whitespace and local reference checks passed.
  - command: python3 tools/continuity.py validate-repository --repository . and pinned Aether schema and section
      checks
    outcome: passed
    observed_at: '2026-11-12T00:31:29Z'
    notes: Local composition, exact schema digest and formats, headings, and byte and line budgets checked.
  - command: Full repository validation, lint, builds and hosted CI
    outcome: not-run
    observed_at: '2026-11-12T00:31:29Z'
    notes: Deferred to the later repository sweep.
  environment_limitations:
  - Repository-wide checks and hosted CI remain deferred.
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

# hygiene continuity

## Purpose and precedence

Read repository instructions and live tracker state before this checkpoint.
The presentation guide owns its license guidance and OSI owns its definition.

## Resume protocol

Refresh main, issue #94, and related open reviews. Read the presentation guide
and its linked feasibility note before selecting any next implementation.

## Current objective and success conditions

Review a canonical OSI reference for public README wording. The evidence
must explain current reuse terms and distinguish changed wording from
formatting noise and unexpected article structure.

## State snapshot

The branch `codex/hygiene-94-osi-reference` was prepared from observed main
`31ae6fb78757502e7474e5518904fc568840c1ee`. Issue #94 was open at review.

## Completed and material changes

The presentation guide points to OSI alongside the repository-owned license
evidence. The feasibility note recommends on-demand review and records the
publisher source, reuse evidence, and normalization experiment. ADR not
required. The link documents an external reference under the existing
presentation guidance.

## Validation and review evidence

Two live reads normalized to the same digest. Synthetic formatting, wording,
and malformed-structure cases returned no-op, review, and manual inspection
respectively. Whitespace, relative links, local handoff composition, and the
pinned Aether schema and section checks passed. Full validation, lint, builds
and hosted CI remain deferred.

## Blockers, risks, unknowns, and deferred work

The recommendation awaits maintainer review. An upstream content-structure
change requires manual inspection before establishing a new digest.

## Next dependency-ready work

Review the link-only recommendation and evidence in
[issue #94](https://github.com/egohygiene/hygiene/issues/94).

## Parallel changes and reconciliation

Open Hygiene drafts #75, #89, #90, and #91 also carry continuity changes.
Reconcile the root handoff against live tracker state before integration.

## Privacy and redaction

Keep the handoff limited to public repository and publisher evidence.

## Handoff update protocol

Record exact live PR and merge observations at the next authorized checkpoint.

## Compaction and supersession

Replace stale current-state prose and rely on Git and owning issues for history.
