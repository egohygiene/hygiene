---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-03T22:52:43Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Preserve the Hygiene-owned collection-coverage dependency for Observatory issue 25.
  includes:
  - Proposed Repository Intelligence alpha.2 coverage semantics, schema, reference validation, fixtures and compatibility migration.
  excludes:
  - Provider collection, rendering, deployment, downstream adoption and lifecycle ratification.
  - Private data, conversation transcripts and credentials.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/REPOSITORY_INTELLIGENCE_COVERAGE.md
  - docs/decisions/ADR-005-unify-repository-intelligence-projection.md
  - schemas/repository-intelligence.alpha2.schema.json
  - catalog/contracts.yaml
  - https://github.com/egohygiene/observatory/issues/25
work:
  objective: Present a bounded input-contract dependency for honest per-domain collection coverage.
  success_conditions:
  - Explicit collection and freshness states for nine domains.
  - Legacy alpha.1 artifacts retained; exact alpha.2 migration documented.
  - Privacy-safe fixtures and reference validation pass.
  active_issue:
    provider: github
    id: egohygiene/observatory#25
    url: https://github.com/egohygiene/observatory/issues/25
  next:
    kind: pull-request-review
    id: collection-coverage-contract-review
    description: Review this Hygiene candidate before merging the dependent Observatory implementation; production EgoLint/Relay repinning follows separately.
    readiness: ready-for-review
    references:
    - https://github.com/egohygiene/observatory/issues/25
    depends_on: []
state:
  base:
    revision: 63d313b1ddf8669808e897853b74928505494da0
    ref: refs/heads/main
    verified_at: '2026-10-03T22:52:43Z'
  candidate:
    branch: codex/observatory-25-domain-coverage
    revision: null
    revision_role: working-tree-candidate
    pull_request: null
    handoff_state: ready-for-review
    finalization: The commit containing this checkpoint and its pull request are the authoritative review candidate.
  live:
    status: verified
    observed_at: '2026-10-03T22:52:43Z'
    default_branch_revision: 63d313b1ddf8669808e897853b74928505494da0
    issue_state: open
    pull_request_state: not-created
    notes: Observatory issue 25 is open. Hygiene PR 63 merged at this base; its previous checkpoint is superseded by this task. No competing Hygiene PR was open at inspection.
  parallel_changes:
  - The dependent Observatory coverage candidate is prepared separately; no Identity repository changes are part of this task.
review:
  status: passed
  reviewed_at: '2026-10-03T22:52:43Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover --start-directory tests --pattern "test_*.py"
    outcome: passed
    observed_at: '2026-10-03T22:52:43Z'
    notes: 184 tests, including eight new coverage contract tests.
  - command: README.md complete validation sequence
    outcome: passed
    observed_at: '2026-10-03T22:52:43Z'
    notes: Catalog, generated views, context, continuity, profiles, boundaries, fixtures and ADR reference checks passed.
  - command: Draft202012Validator with RFC3339 FormatChecker against alpha.2 schema and coverage mutations
    outcome: passed
    observed_at: '2026-10-03T22:52:43Z'
    notes: Eight fixture documents and 256 malformed coverage schema/reference parity cases passed.
  environment_limitations:
  - No automatic Hygiene pull-request CI workflow exists. Local reference validation is not a claim of production EgoLint alpha.2 support.
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

This operational checkpoint is subordinate to instructions, live state and
canonical sources. It grants no merge, publication or deployment authority.

## Current objective and success conditions

Provide the input-contract dependency for Observatory #25: empty arrays never
stand in for collection completeness or applicability.

## State snapshot

The candidate branches from main at the exact revision in front matter.
The former PR #63 checkpoint was stale: that PR is merged. This candidate
remains unmerged until live GitHub evidence establishes otherwise.

## Material result

The proposed alpha.2 schema requires nine explicit domain claims. The reference
validator, eight synthetic fixtures, catalog pointer and ADR-005 amendment
retain Hygiene ownership and exact alpha.1 compatibility artifacts.

## Validation and limitations

184 tests and the complete README checks pass. Schema/format validation and
256 malformed coverage parity cases pass. No automatic hosted CI is available.

## Next dependency-ready work

Review this owner contract and the dependent Observatory consumer together.
EgoLint production validation and Relay collection/rendering require a separate
compatible repin before publication. No provider collection is implemented here.

## Handoff update protocol

Before changing the candidate, verify live main, competing PRs and Observatory
issue 25. Preserve proposed lifecycle and exact immutable consumer pins.

## Compaction and supersession

Keep the checkpoint below 16384 bytes and 240 lines. Git retains prior history.
