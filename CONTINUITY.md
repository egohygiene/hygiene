---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-12T00:33:32Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Propose JournalList trust.txt as an optional Agent-Ready Web discovery
    mechanism.
  includes:
  - Register the proposed trust-txt mechanism, source and evidence rules, compatibility
    behavior, and synthetic examples.
  - Document the conflict between JournalList v1.5 and its deployment FAQ. Select
    the FAQ direction.
  excludes:
  - First consumer selection, live observations, lifecycle activation, rollout, and
    public publication.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - catalog/agent-ready-web-profile.json
  - docs/ecosystem/AGENT_READY_WEB.md
  - docs/decisions/ADR-0010-agent-ready-web-discovery-representations.md
  - https://github.com/egohygiene/hygiene/issues/102
work:
  objective: Propose JournalList trust.txt as an optional Agent-Ready Web discovery
    mechanism.
  success_conditions:
  - The exact HTTPS well-known route returns text/plain, and the root route redirects
    to it.
  - The profile keeps publication optional and differentiates applicable absence,
    evidenced non-applicability, and unknown.
  - The profile and synthetic evidence validate. Reviewed source ownership and immutable
    consumer pins remain explicit.
  active_issue:
    provider: github
    id: egohygiene/hygiene#102
    url: https://github.com/egohygiene/hygiene/issues/102
  next:
    kind: action
    id: review-trust-txt-proposal
    description: 'Review the proposed alpha.5 addition and its placement decision
      on issue #102.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/102
    depends_on: []
state:
  base:
    revision: 31ae6fb78757502e7474e5518904fc568840c1ee
    ref: refs/heads/main
    verified_at: '2026-11-12T00:33:32Z'
  candidate:
    branch: codex/hygiene-102-trust-txt
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-12T00:33:32Z'
    default_branch_revision: 31ae6fb78757502e7474e5518904fc568840c1ee
    issue_state: open
    pull_request_state: not-applicable
    notes: 'GitHub showed issue #102 open and no corresponding open pull request at
      the pre-PR observation.'
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
  - provider: github
    id: egohygiene/hygiene#103
    url: https://github.com/egohygiene/hygiene/pull/103
  - provider: github
    id: egohygiene/hygiene#85
    url: https://github.com/egohygiene/hygiene/issues/85
review:
  status: partial
  reviewed_at: '2026-11-12T00:33:32Z'
  reviewed_by: Codex
  evidence:
  - command: python3 tools/agent_ready_web.py validate-profile
    outcome: passed
    observed_at: '2026-11-12T00:33:32Z'
    notes: Proposed alpha.5 catalog passes the reference checker.
  - command: python3 tools/agent_ready_web.py validate-fixtures
    outcome: passed
    observed_at: '2026-11-12T00:33:32Z'
    notes: All 15 compatibility fixtures validate.
  - command: python3 -m unittest discover --start-directory tests --pattern test_agent_ready_web.py
    outcome: passed
    observed_at: '2026-11-12T00:33:32Z'
    notes: 44 focused tests pass.
  - command: Draft 2020-12 validation with format checks
    outcome: passed
    observed_at: '2026-11-12T00:33:32Z'
    notes: The profile and all five whole-profile evidence fixtures pass. Two invalid
      Trust profile mutations reject.
  - command: Full regression, hosted CI, and live site validation
    outcome: not-run
    observed_at: '2026-11-12T00:33:32Z'
    notes: Full regression and CI are deferred. HTTP and source observations are synthetic.
  environment_limitations:
  - Full regression and CI are deferred. Live serving, source authenticity, and a
    real consumer were not checked.
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

This checkpoint records the proposed trust.txt change. User and repository instructions, live GitHub evidence, and canonical sources take precedence.

## Resume protocol

Read AGENTS.md, issue #102, the profile guide, and ADR-0010. Verify the live issue and candidate before relying on this snapshot.

## Current objective and success conditions

Propose JournalList trust.txt as an optional Agent-Ready Web discovery mechanism. Validate the exact origin-root placement and source-review rules without changing existing mechanism meanings or enabling publication.

## State snapshot

Candidate `codex/hygiene-102-trust-txt` is based on observed main `31ae6fb78757502e7474e5518904fc568840c1ee`. Issue #102 was open at the pre-PR observation. Candidate revision and pull request are null in this pre-PR checkpoint.

## Completed and material changes

Proposed alpha.5 registers the optional mechanism, records primary and supporting sources, binds the route and media type in the schema and reference checker, and replays whole-profile evidence across all five site classes. The guide explains the JournalList redirect discrepancy and the selected FAQ direction.

## Validation and review evidence

The profile command, 15 fixtures, 44 focused tests, and Draft 2020-12 profile and site fixture checks passed. Invalid placement and strength mutations reject. Full regression, hosted CI, and live observations were deferred.

## Blockers, risks, unknowns, and deferred work

The profile remains proposed and exact older consumer pins retain their earlier checker. Site relationships, public contacts, training policy, and HTTP behavior require actual owner review and consumer evidence before a publication claim.

## Next dependency-ready work

Review the proposed alpha.5 addition and its placement decision on issue #102. Select a first consumer separately after lifecycle and eligibility review.

## Parallel changes and reconciliation

Open drafts #75, #89–#91, and #103 carry their own continuity snapshots. Issue #85 has parallel navigation work. Reconcile the active handoff before integrating parallel changes.

## Privacy and redaction

The only example contact uses a reserved domain. Review evidence and any publication facts belong to their proper owners.

## Handoff update protocol

Verify the draft and main again at the next authorized checkpoint. Refresh the observed state when evidence changes.

## Compaction and supersession

Retain current validation evidence and the next action here. Git and issue #102 retain the history.
