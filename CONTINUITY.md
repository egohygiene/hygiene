---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T22:27:30Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Define proposed organization strategy and repository-roadmap composition separately from repository
    strategy and tactical execution.
  includes:
  - Canonical organization/roadmap.v1.json and its deterministic organization/ROADMAP.md define five stable
    proposed initiatives, horizons and dependencies; all placement remains inferred with no human review
    fabricated.
  - A versioned proposed schema references the existing Intelligence source/event definitions. The pure
    reference checker preserves repository IDs, provenance, freshness, supersession and review boundaries;
    public filtering removes protected participation and dependency closure before rendering.
  - Twelve then thirteen meaningful synthetic controls cover cross-repository/shared and independent work,
    blocked/optional/stale state, inferred versus reviewed declarations, complete private filtering, cycles,
    lineage, event clocks and actual CLI refusal. The complete gate now includes source and generated-view
    checks.
  excludes: &id001
  - ADR-0023 and the organization roadmap contract remain proposed with null approval; this source does
    not ratify strategy, authenticate review comments, reprioritize work or activate fleet enforcement.
  - Initial node keys were inspected against exact public repository roadmap revisions. The helper does
    not perform live owner discovery or establish exhaustive collection; production graph/UI integration
    remains with existing Relay, Observatory and publisher owners.
  - No package publication, external service configuration, deployment, restricted-product inventory or
    live human-review operation occurred. The public synthetic protected example contains no real private
    topology.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - organization/roadmap.v1.json
  - organization/ROADMAP.md
  - docs/ecosystem/ORGANIZATION_ROADMAP.md
  - schemas/organization-roadmap.v1.schema.json
  - tools/organization_roadmap.py
  - tests/test_organization_roadmap.py
  - docs/decisions/ADR-0023-organization-roadmap-composition.md
  - https://github.com/egohygiene/hygiene/issues/60
work:
  objective: Define proposed organization strategy and repository-roadmap composition separately from
    repository strategy and tactical execution.
  success_conditions:
  - Organization initiatives compose repository strategy by stable references and retain explicit dependency,
    optionality, freshness and review semantics.
  - Proposed placement never becomes authoritative through activity, CI success or source merge; existing
    canonical owners remain separate.
  - Public projection contains no protected identity, URL, node key, event, count or dependency topology
    from the synthetic restricted source.
  active_issue:
    provider: github
    id: egohygiene/hygiene#60
    url: https://github.com/egohygiene/hygiene/issues/60
  next:
    kind: issue
    id: egohygiene/aether#88
    description: After reviewing this source checkpoint, compose roadmap-impact reconciliation through
      the existing Aether agent/instruction system; local signals must preserve Hygiene strategy ownership
      and human review.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/88
    - https://github.com/egohygiene/hygiene/issues/60
    depends_on: []
state:
  base:
    revision: ea2768d49a5953d7f710374fbf13bff880f44f91
    ref: refs/heads/main
    verified_at: '2026-11-14T22:27:30Z'
  candidate:
    branch: codex/organization-roadmap
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T22:27:30Z'
    default_branch_revision: ea2768d49a5953d7f710374fbf13bff880f44f91
    issue_state: open
    pull_request_state: not-applicable
    notes: Observed main ea2768d retains prior source qualifications. Issue60 is open; this local candidate
      has no PR yet. Separate five-repository intake snapshot has137 open issues and no open PRs after
      Aether129 merged. Recheck mutable source and tracker state before integration.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-14T22:27:30Z'
  reviewed_by: Codex
  evidence:
  - command: python -I -m unittest discover -s tests -p test_organization_roadmap.py -v
    outcome: passed
    notes: 13 synthetic controls pass, including partial and completely restricted public projection and
      idempotent repeat.
    observed_at: '2026-11-14T22:27:30Z'
  - command: Draft202012Validator with local schema registry and FormatChecker; Hygiene decision reference
      check
    outcome: passed
    notes: Canonical and mixed synthetic roadmap inputs and proposed ADR-0023 metadata pass schema/formats;
      selected Intelligence source/event definitions are reused by reference.
    observed_at: '2026-11-14T22:27:30Z'
  - command: python -I tools/check_contracts.py
    outcome: passed
    notes: All27 reference checks and372 tests pass with zero failures/errors/skips. Exact locked Aether
      release-owner files were provided in the ignored local cache; no release was created.
    observed_at: '2026-11-14T22:27:30Z'
  environment_limitations: *id001
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

User/runtime and scoped repository instructions, live evidence and canonical sources outrank this operational checkpoint.

## Resume protocol

Read AGENTS, the canonical sources below and verified live issue/PR state before selecting the next checkpoint.

## Current objective and success conditions

Define proposed organization strategy and repository-roadmap composition separately from repository strategy and tactical execution.

- Organization initiatives compose repository strategy by stable references and retain explicit dependency, optionality, freshness and review semantics.
- Proposed placement never becomes authoritative through activity, CI success or source merge; existing canonical owners remain separate.
- Public projection contains no protected identity, URL, node key, event, count or dependency topology from the synthetic restricted source.

## State snapshot

Observed default source `ea2768d49a5953d7f710374fbf13bff880f44f91`. Candidate `codex/organization-roadmap` is a review checkpoint; its containing revision remains null intentionally.

## Completed and material changes

Canonical organization/roadmap.v1.json and its deterministic organization/ROADMAP.md define five stable proposed initiatives, horizons and dependencies; all placement remains inferred with no human review fabricated.

A versioned proposed schema references the existing Intelligence source/event definitions. The pure reference checker preserves repository IDs, provenance, freshness, supersession and review boundaries; public filtering removes protected participation and dependency closure before rendering.

Twelve then thirteen meaningful synthetic controls cover cross-repository/shared and independent work, blocked/optional/stale state, inferred versus reviewed declarations, complete private filtering, cycles, lineage, event clocks and actual CLI refusal. The complete gate now includes source and generated-view checks.

## Validation and review evidence

`python -I -m unittest discover -s tests -p test_organization_roadmap.py -v` — passed: 13 synthetic controls pass, including partial and completely restricted public projection and idempotent repeat.

`Draft202012Validator with local schema registry and FormatChecker; Hygiene decision reference check` — passed: Canonical and mixed synthetic roadmap inputs and proposed ADR-0023 metadata pass schema/formats; selected Intelligence source/event definitions are reused by reference.

`python -I tools/check_contracts.py` — passed: All27 reference checks and372 tests pass with zero failures/errors/skips. Exact locked Aether release-owner files were provided in the ignored local cache; no release was created.

ADR-Ref: ADR-0002 governs human disposition. ADR-0023 proposes the new organization source/composition format and retains null approval. Existing proposed architecture, Intelligence, coherence and release decisions keep their dispositions.

## Blockers, risks, unknowns, and deferred work

ADR-0023 and the organization roadmap contract remain proposed with null approval; this source does not ratify strategy, authenticate review comments, reprioritize work or activate fleet enforcement.

Initial node keys were inspected against exact public repository roadmap revisions. The helper does not perform live owner discovery or establish exhaustive collection; production graph/UI integration remains with existing Relay, Observatory and publisher owners.

No package publication, external service configuration, deployment, restricted-product inventory or live human-review operation occurred. The public synthetic protected example contains no real private topology.

## Next dependency-ready work

After reviewing this source checkpoint, compose roadmap-impact reconciliation through the existing Aether agent/instruction system; local signals must preserve Hygiene strategy ownership and human review.

## Parallel changes and reconciliation

Preserve prior change-history, claim-provenance, diagnosis and website-owner evidence. Concurrent remote integrations in Aether, Empathy, Holon and .github were observed independently; selected roadmap references remain immutable facts, not exhaustive fleet adoption.

## Privacy and redaction

Public-safe source facts and synthetic fixtures only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

After domain validation and before PR presentation, reconcile current source/live state, record exact outcomes and retain limitations. Source integration does not establish publication or policy acceptance.

## Compaction and supersession

Git and linked work records retain history. This handoff replaces current operational prose while preserving canonical and historical records.
