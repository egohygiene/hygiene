---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: "2026-09-12T17:13:04Z"
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Preserve a compact, public-safe handoff for Hygiene issue 15 and the accepted ADR contract rollout.
  includes:
    - issue 15 approval evidence, activation candidate, validation, limitations, and next dependency-ready work
  excludes:
    - conversation transcripts
    - duplicated architecture, roadmap, and changelog content
  precedence:
    - user-and-runtime-instructions
    - scoped-repository-instructions
    - live-repository-and-work-tracker-state
    - canonical-repository-sources
    - continuity-checkpoint
  canonical_sources:
    - AGENTS.md
    - docs/ecosystem/ARCHITECTURE.md
    - docs/decisions/ADR-002-organization-adr-and-delivery-history.md
    - docs/decisions/POLICY.md
    - docs/decisions/RATIFICATION.md
    - ROADMAP.md
    - https://github.com/egohygiene/hygiene/issues/15
work:
  objective: Activate ADR-002 and policy v1.1.0 from explicit maintainer ratification without claiming downstream rollout is complete.
  success_conditions:
    - Record the exact maintainer approval URL and pinned implementation commit.
    - Accept ADR-002 and policy v1.1.0 and activate only their two governed contract entries.
    - Update canonical indexes, migration guidance, validation gates, and roadmap state consistently.
    - Pass every repository validation listed in README.md and present one reviewable pull request without merging it.
  active_issue:
    provider: github
    id: egohygiene/hygiene#15
    url: https://github.com/egohygiene/hygiene/issues/15
  next:
    kind: issue
    id: egohygiene/holon#6
    description: Provide migration-safe ADR scaffolding against the accepted Hygiene policy before fleet backfills begin.
    readiness: blocked
    references:
      - https://github.com/egohygiene/holon/issues/6
    depends_on:
      - egohygiene/hygiene#15
state:
  base:
    revision: 43386f5749116717585ead7459b4945e0ac50d06
    ref: refs/heads/main
    verified_at: "2026-09-12T17:13:04Z"
  candidate:
    branch: codex/hygiene-15-activate-adr-contract
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: "2026-09-12T17:13:04Z"
    default_branch_revision: 43386f5749116717585ead7459b4945e0ac50d06
    issue_state: open
    pull_request_state: not-applicable
    notes: Issue 15 contains explicit approval by szmyty at comment 5647398908, origin/main matches the verified base, and no open Hygiene pull request was observed; recheck before continuing.
  parallel_changes: []
review:
  status: passed
  reviewed_at: "2026-09-12T17:13:04Z"
  reviewed_by: Codex
  evidence:
    - command: python3 -m unittest discover --start-directory tests --pattern "test_*.py"
      outcome: passed
      observed_at: "2026-09-12T17:13:04Z"
      notes: All 95 tests passed, including active-state assertions for both ratified ADR contracts.
    - command: README.md repository validation sequence
      outcome: passed
      observed_at: "2026-09-12T17:13:04Z"
      notes: Catalog, generated catalog, context, continuity, boundaries, Repository Intelligence, presentation, and ADR checks passed.
    - command: python3 tools/decisions.py decision-set and policy-reference fixture checks
      outcome: passed
      observed_at: "2026-09-12T17:13:04Z"
      notes: Proposed, accepted, superseded, and inherited-policy fixtures validated.
    - command: git diff --check
      outcome: passed
      observed_at: "2026-09-12T17:13:04Z"
      notes: No whitespace errors remained after the activation update.
  environment_limitations:
    - No automatic pull-request CI was run; Hygiene currently exposes only a manually dispatched release-policy workflow.
    - The maintain-repository-continuity skill was not exposed by this host, so the checkpoint was reconciled manually against the repository contract.
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

This checkpoint hands off issue #15's ADR-002 activation. It is subordinate to
user and repository instructions, live Git/GitHub evidence, and accepted
canonical sources. Generated projections and conversational memory cannot
override them.

## Resume protocol

Read `AGENTS.md` and the canonical sources above, then recheck `main`, issue
#15, its approval comment, this branch, and any pull request before acting.
Surface stale or contradictory evidence and continue only the next
dependency-ready work unless the user redirects it.

## Current objective and success conditions

Activate the approved organization ADR policy without conflating acceptance
with fleet implementation. Success means the exact authority is recorded, only
the two governed contracts are activated, canonical views agree, every listed
validation passes, and the unmerged candidate is presented for review.

## State snapshot

- Base: `43386f5749116717585ead7459b4945e0ac50d06` on `main`.
- Authority: maintainer `szmyty` approved ADR-002 and policy v1.1.0 at
  `f598ed659a43dd759d4ede41c27f9e5daf991aa7` in the durable issue #15 comment.
- Candidate: `codex/hygiene-15-activate-adr-contract`, ready for review but not
  merged.

## Completed and material changes

The candidate changes ADR-002 and the policy to accepted, activates only the
ADR front-matter and inheritance-reference contracts, updates canonical
indexes and roadmap state, and adds active-state regression assertions.

## Validation and review evidence

All 95 unit tests and the complete README validation sequence passed. Exact
commands and coverage are recorded in front matter. Pull-request CI has not run,
and the host did not expose Aether's continuity-maintenance skill; the
checkpoint was reconciled manually and passed the local continuity validator.

## Blockers, risks, unknowns, and deferred work

- Blockers: none for presenting the activation pull request.
- Risks: issue #15 stays open until the activation PR merges.
- Unknowns: no additional implementation unknowns were observed.
- Deferred: Aether promotion, Holon scaffolding, Relay
  validation/publication, Pace rollout, and the 29 repository backfills.
- Authority limit: approval applies only to ADR-002 and policy v1.1.0 at the
  named commit, not later revisions or downstream implementation.

## Next dependency-ready work

After issue #15 closes, continue with
[egohygiene/holon#6](https://github.com/egohygiene/holon/issues/6). That issue
provides the migration-safe scaffold required before repository backfills.

## Parallel changes and reconciliation

No open Hygiene pull request was observed at task start. Recheck live state
before modifying or presenting the candidate.

## Privacy and redaction

This public checkpoint contains only public repository state. It excludes
secrets, private conversations, personal data, local paths, and unpublished
business information.

## Handoff update protocol

Before presenting or updating the pull request, replace stale candidate state
with exact observed checks and limitations. Never predict a merge or treat
generated text as human authority.

## Compaction and supersession

Replace stale state rather than appending chronology; Git and GitHub own
history. Keep the checkpoint public-safe and below its declared size limits.
