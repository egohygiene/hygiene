---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: "2026-11-12T00:32:36Z"
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Reconcile current navigation and topology evidence for Hygiene issue 85.
  includes:
    - Current roadmap, authority map, topology diagrams and operational checkpoint.
    - Historical architecture decisions, approval evidence and source admission references.
  excludes:
    - Organization ratification, source-admission repair and hosted publication.
    - Catalog policy, repository roles and dependency changes.
  precedence:
    - user-and-runtime-instructions
    - scoped-repository-instructions
    - live-repository-and-work-tracker-state
    - canonical-repository-sources
    - continuity-checkpoint
  canonical_sources:
    - AGENTS.md
    - ROADMAP.md
    - docs/decisions/README.md
    - docs/ecosystem/ARCHITECTURE.md
    - publication/README.md
    - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: Make the next audit review and exact architecture and publication authority clear to a fresh session.
  success_conditions:
    - The current handoff identifies the next open review and preserves the historical roadmap and stable HYG-Q IDs.
    - The architecture and diagrams identify proposed amendments and link observed local implementations separately.
    - The publisher pin, admission requirements and unresolved ADR-0001 evidence remain traceable.
  active_issue:
    provider: github
    id: egohygiene/hygiene#85
    url: https://github.com/egohygiene/hygiene/issues/85
  next:
    kind: action
    id: review-audit-repair-drafts
    description: Review the continuity, presentation and ADR draft repairs in the order recorded by issue 76.
    readiness: ready
    references:
      - https://github.com/egohygiene/hygiene/issues/76
      - https://github.com/egohygiene/hygiene/pull/91
      - https://github.com/egohygiene/hygiene/pull/89
      - https://github.com/egohygiene/hygiene/pull/90
    depends_on: []
state:
  base:
    revision: 31ae6fb78757502e7474e5518904fc568840c1ee
    ref: refs/heads/main
    verified_at: "2026-11-12T00:32:36Z"
  candidate:
    branch: codex/hygiene-85-authority-navigation
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: "2026-11-12T00:32:36Z"
    default_branch_revision: 31ae6fb78757502e7474e5518904fc568840c1ee
    issue_state: open
    pull_request_state: not-applicable
    notes: Main includes merged PRs 92, 93 and 101. PRs 89 through 91 remain open for review.
  parallel_changes:
    - provider: github
      id: egohygiene/hygiene#89
      url: https://github.com/egohygiene/hygiene/pull/89
    - provider: github
      id: egohygiene/hygiene#90
      url: https://github.com/egohygiene/hygiene/pull/90
    - provider: github
      id: egohygiene/hygiene#91
      url: https://github.com/egohygiene/hygiene/pull/91
    - provider: github
      id: egohygiene/hygiene#103
      url: https://github.com/egohygiene/hygiene/pull/103
    - provider: github
      id: egohygiene/hygiene#102
      url: https://github.com/egohygiene/hygiene/issues/102
review:
  status: partial
  reviewed_at: "2026-11-12T00:32:36Z"
  reviewed_by: Codex
  evidence:
    - command: >-
        python3 tools/boundaries.py validate and
        python3 tools/catalog.py --catalog catalog/repositories.yaml validate
      outcome: passed
      observed_at: "2026-11-12T00:32:36Z"
      notes: Existing register and catalog validate.
    - command: >-
        python3 -m unittest discover --start-directory tests
        --pattern "test_catalog.py"
      outcome: failed
      observed_at: "2026-11-12T00:32:36Z"
      notes: >-
        Both the candidate and clean base have the same two failures in ten
        tests. One expects 27 catalog rows and one expects the older
        unknown-plane diagnostic.
    - command: >-
        python3 -m unittest discover --start-directory tests
        --pattern "test_continuity.py"
      outcome: passed
      observed_at: "2026-11-12T00:32:36Z"
      notes: All 14 focused continuity tests pass.
    - command: >-
        Diagram regeneration and parity, navigation links and pinned
        continuity schema validation
      outcome: passed
      observed_at: "2026-11-12T00:32:36Z"
      notes: Local source and handoff checks.
    - command: Complete regression gate, hosted CI, native admission and deployment
      outcome: not-run
      observed_at: "2026-11-12T00:32:36Z"
      notes: Deferred. Publication remains subject to the separate repository runbook.
  environment_limitations:
    - Whole-repository and hosted validation were deferred.
    - Mermaid and PlantUML renderers were not run.
    - Native ADR-0001 approval evidence and source admission remain tracked by issue 47.
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

Follow repository instructions and verify the current Git and GitHub state.
The roadmap, decisions and publisher sources govern the claims they own.

## Resume protocol

Start at [README](README.md), follow [AGENTS](AGENTS.md) and the
[current roadmap handoff](ROADMAP.md#current-work-and-publication-handoff),
then compare the review links below with live evidence.

## Current objective and success conditions

Make the active audit review and the scope of historical, approved, proposed
and implemented architecture decisions traceable from the main entry points.

## State snapshot

The navigation candidate is based on observed main
`31ae6fb78757502e7474e5518904fc568840c1ee`. Its pre-PR metadata leaves the
candidate revision and PR reference null.

## Completed and material changes

The roadmap identifies the next review and the repository-owned Intelligence
publisher. The architecture authority map and diagrams distinguish the
historical baseline from the Filament and Sanctuary/Empathy proposals, and the
decision index links the accepted ADR policy. Original ADR records, the
unapplied review patch and the dated execution snapshot are preserved.

## Validation and review evidence

Repository catalog and boundary references, diagram regeneration and parity,
navigation links and pinned continuity checks were examined locally. The two
catalog-test failures match clean main. Full regression, CI, native admission
and deployment checks are deferred.

## Blockers, risks, unknowns, and deferred work

[Issue 47](https://github.com/egohygiene/hygiene/issues/47) owns ADR-0001's
missing structured metadata and approval evidence. The
[publisher runbook](publication/README.md) requires passing exact-revision
native ADR coverage before build and deployment.

## Next dependency-ready work

Review drafts [#91](https://github.com/egohygiene/hygiene/pull/91),
[#89](https://github.com/egohygiene/hygiene/pull/89), then
[#90](https://github.com/egohygiene/hygiene/pull/90) under
[#76](https://github.com/egohygiene/hygiene/issues/76).

## Parallel changes and reconciliation

The three audit drafts, feasibility draft #103 and separate work on issue 102
carry their own handoff edits. Reconcile this file with the resulting main state before
integrating overlapping candidates.

## Privacy and redaction

Retain public source identities and bounded operational evidence.

## Handoff update protocol

Refresh exact review, merge and validation evidence at the next authorized
checkpoint.

## Compaction and supersession

Replace superseded operational details. Git and the owning issues retain
history.
