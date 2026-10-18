---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-10T19:45:31Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Preserve the reviewed preparation boundary for Hygiene issue 47 ADR migration.
  includes:
  - The 13-record source inventory, historical evidence gaps, migration plan and shared policy-owner dependency.
  excludes:
  - ADR ratification, canonical-record rewriting, shared validator implementation, publication and wider
    fleet rollout.
  - Private data, conversation transcripts and credentials.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/decisions/POLICY.md
  - docs/decisions/RATIFICATION.md
  - docs/decisions/migrations/2026-10-10-hygiene-inventory.md
  - docs/evidence/hygiene-adrs-inventory-2026-10-10.json
  - https://github.com/egohygiene/hygiene/issues/47
  - https://github.com/egohygiene/egolint/issues/81
  - https://github.com/egohygiene/pace/issues/5
work:
  objective: Present the evidence-backed Hygiene ADR inventory and bounded migration plan.
  success_conditions:
  - All 13 canonical ADRs and their identities remain byte-preserved.
  - Authority, source-conformance and publication gaps have explicit next owners.
  - The inventory, review packet and resume checkpoint are durably reviewable.
  active_issue:
    provider: github
    id: egohygiene/hygiene#47
    url: https://github.com/egohygiene/hygiene/issues/47
  next:
    kind: action
    id: hygiene-47-inventory-review
    description: 'Review this inventory and the concrete ADR-0001 reaffirmation/legacy-exception recommendation;
      implement EgoLint #81 separately before native owner admission.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/47
    - https://github.com/egohygiene/egolint/issues/81
    depends_on: []
state:
  base:
    revision: b8d2c02368e40d4f6c2017bb1a22c6ec23323ad3
    ref: refs/heads/main
    verified_at: '2026-10-10T19:45:31Z'
  candidate:
    branch: codex/hygiene-47-adr-inventory
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-10T19:45:31Z'
    default_branch_revision: b8d2c02368e40d4f6c2017bb1a22c6ec23323ad3
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Hygiene #47 is open; no open Hygiene PR was observed before this candidate. Prior PR #67 merged
      into this main and Observatory #25 is closed. EgoLint #81 was created and read back; its main remains
      2d3600f14848e28099acc34ce8043699da2b9a32.'
  parallel_changes:
  - provider: github
    id: egohygiene/egolint#81
    url: https://github.com/egohygiene/egolint/issues/81
review:
  status: partial
  reviewed_at: '2026-10-10T19:45:31Z'
  reviewed_by: Codex
  evidence:
  - command: tools/decisions.py decision --input, for each safely decoded ADR-002 through ADR-013
    outcome: passed
    observed_at: '2026-10-10T19:45:31Z'
    notes: All 12 metadata objects pass the unchanged reference checker; not full Markdown conformance.
  - command: tools/decisions.py decision-set --input, over the same twelve decoded records
    outcome: limited
    observed_at: '2026-10-10T19:45:31Z'
    notes: Expected exit 1 with 11 references to legacy ADR-0001, whose Markdown exists but has no metadata.
      No synthetic record or green full-corpus result.
  - command: Inventory/source SHA-256 comparison and local Markdown-link inspection
    outcome: passed
    observed_at: '2026-10-10T19:45:31Z'
    notes: 13 canonical ADRs and six policy/navigation source files byte-preserved; receipt counts and
      diagnostics agree; relative links resolve and no private workspace paths appear.
  - command: python3 tools/continuity.py validate-profile; python3 tools/continuity.py validate-repository
      --repository .; python3 tools/context.py validate
    outcome: passed
    observed_at: '2026-10-10T19:45:31Z'
    notes: Organization continuity composition and 27 repository context entries pass.
  - command: Aether b7597301 continuity Draft202012 schema, twelve-heading/size/privacy checks and git
      diff --check
    outcome: passed
    observed_at: '2026-10-10T19:45:31Z'
    notes: Exact catalog-pinned schema validation passed after replacing unsupported inherited handoff
      fields; all twelve headings, size and public-path checks pass.
  - command: Native production ADR validation, hosted CI, site generation and deployment
    outcome: not-run
    observed_at: '2026-10-10T19:45:31Z'
    notes: Documentation-only checkpoint; owner-mode compatibility and legacy migration remain open.
  environment_limitations:
  - Reference metadata checks cannot establish Markdown or native production conformance.
  - The current pinned EgoLint/Relay path lacks explicit Hygiene policy-owner support; no self-inheritance
    file was fabricated.
  - No deployment, release or whole-fleet acceptance is claimed.
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

This handoff records the Hygiene #47 preparation candidate. Instructions, live
state and canonical policy take precedence; it grants no lifecycle authority.

## Resume protocol

Read the migration packet, source receipt and policy; recheck main, this PR,
Hygiene #47, EgoLint #81, Pace #5 and the program checkpoint before continuing.

## Current objective and success conditions

Make the existing ADR inventory, preservation requirements and next dependencies
reviewable. This checkpoint does not claim the migration or publication complete.

## State snapshot

The exact base is recorded above. Thirteen organization records exist: one
legacy Accepted claim, one explicitly accepted record and eleven proposals.
No competing Hygiene PR was observed before this candidate was prepared.

## Completed and material changes

The migration packet inventories history and authority, identifies one proposed
local backfill candidate, and records the central-host question. Its receipt
preserves source hashes and bounded diagnostics. The index's stale ratification
wording is corrected; canonical ADRs, policy and executable files are unchanged.

## Validation and review evidence

Twelve metadata checks pass. The twelve-record decoded set has eleven expected
links to omitted legacy ADR-0001; that is an incomplete corpus, not missing
Markdown. ADR-004 also lacks one required section. Preservation, documentation,
context and continuity checks are recorded above; no runtime deployment ran.

## Blockers, risks, unknowns, and deferred work

ADR-0001's PR #3 is a legacy authority candidate; the packet proposes explicit
reaffirmation and a narrow legacy identity exception. No modern approval is invented.
EgoLint #81 must support the canonical policy owner without self-inheritance.
Hygiene has no Decisions publisher or site declaration. Central roadmap intent
does not silently choose a Decisions route. Eleven proposals remain proposals.

## Next dependency-ready work

Review the concrete inventory/disposition packet. Prepare source normalization
and the narrowly evidenced proposed catalog-format ADR after that review.
The shared owner-mode fix can proceed separately; native admission precedes
artifact/host composition, which precedes live publication acceptance.

## Parallel changes and reconciliation

Pace #5 and .github #30 track this repository checkpoint and future branding
checks. EgoLint owns semantics, Relay owns adapters, and the chosen host owns
publication. No other repository rollout is included here.

## Privacy and redaction

Only public repository facts and selected evidence links appear. The receipt
omits raw provider responses, private paths and unneeded actor data.

## Handoff update protocol

Reconcile this file in the same next scoped PR after validation. Record actual
approval, source, dependency and deployment evidence independently. Preserve
all ADR identities, original substantive prose and the prior checkpoints in Git history.

## Compaction and supersession

This replaces the stale PR #67/Observatory #25 operational checkpoint. Its
historical evidence stays in Git. Keep this file below 16384 bytes and 240 lines.
