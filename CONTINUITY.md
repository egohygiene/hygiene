---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T21:24:23Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Adopt the standardized four-digit authoring and native runtime process in the canonical policy owner.
  includes:
  - 'The owner configuration selects Hygiene policy v1.2.0 at a05b14f8b9e2772124f879f818e09a911e996ad8 and native
    EgoLint catalog alpha.5. All publisher Relay entrypoints select ac2600f4619f64c75a0e499e0540d8f48d516f9c. Aether
    dc8a16851f452763ef4f7fbe4bf057d4500b1921 supplies spec 3.1.0, skill 2.1.0 and exact managed module 0.3.0 through
    the shared merge boundary. Policy/corpus normalization is already merged in #72. The original ADR-0001 and historical
    receipts remain unchanged.'
  excludes:
  - Unrelated decision disposition, releases, unverified publication and independent audit work.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - DECISIONS.md
  - https://github.com/egohygiene/hygiene/issues/73
work:
  objective: Adopt the standardized four-digit authoring and native runtime process in the canonical policy owner.
  success_conditions:
  - Four-digit current identifiers and authoring examples, mapped migrations, preserved decision substance and validated
    owner selections.
  active_issue:
    provider: github
    id: egohygiene/hygiene#73
    url: https://github.com/egohygiene/hygiene/issues/73
  next:
    kind: action
    id: complete-four-digit-adoption
    description: 'Merge validated consumer adoption, complete central naming tracker #73 and return Hygiene #47
      to its separate original ADR-0001 approval/backfill and live publication gate.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/73
    depends_on: []
state:
  base:
    revision: 1f4988324739674561a3b94c9d61ba70e1ce9108
    ref: refs/heads/main
    verified_at: '2026-10-18T21:24:23Z'
  candidate:
    branch: codex/four-digit-adr-adoption
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T21:24:23Z'
    default_branch_revision: 1f4988324739674561a3b94c9d61ba70e1ce9108
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Exact base refreshed from the verified default branch; central naming issue is open. The existing Identity
      #114 field audit remains independent.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#114
    url: https://github.com/egohygiene/identity/pull/114
review:
  status: partial
  reviewed_at: '2026-10-18T21:24:23Z'
  reviewed_by: Codex
  evidence:
  - command: python -m unittest discover --start-directory tests --pattern test_*.py
    outcome: passed
    observed_at: '2026-10-18T21:24:23Z'
    notes: 194 tests passed.
  - command: Pinned native EgoLint owner validation of candidate working tree
    outcome: passed
    observed_at: '2026-10-18T21:24:23Z'
    notes: No authority-contract mismatch; thirteen valid metadata records inspected. Source remains invalid because
      original ADR-0001 lacks metadata and referenced identity cannot enter the graph.
  - command: Exact Aether module parity; continuity schema/sections/budgets
    outcome: passed
    observed_at: '2026-10-18T21:24:23Z'
    notes: Shared block is exact and consumer prose preserved.
  environment_limitations:
  - Relay fresh hosted acquisition and this candidate hosted checks remain pending. Naming does not supply missing
    architecture approval; original ADR-0001 stays unchanged and its review patch stays unapplied. No new release
    or deployment is claimed.
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

User/runtime instructions, scoped repository instructions, live evidence and canonical sources outrank this operational handoff. It grants no authority.

## Resume protocol

Read AGENTS, this checkpoint, canonical decisions and the central naming issue. Refresh live main and any overlapping PR before resuming.

## Current objective and success conditions

Adopt the standardized four-digit authoring and native runtime process in the canonical policy owner.

## State snapshot

Base is 1f4988324739674561a3b94c9d61ba70e1ce9108. Candidate branch is codex/four-digit-adr-adoption. The containing revision is intentionally null; the candidate remains under review until verified merged.

## Completed and material changes

The owner configuration selects Hygiene policy v1.2.0 at a05b14f8b9e2772124f879f818e09a911e996ad8 and native EgoLint catalog alpha.5. All publisher Relay entrypoints select ac2600f4619f64c75a0e499e0540d8f48d516f9c. Aether dc8a16851f452763ef4f7fbe4bf057d4500b1921 supplies spec 3.1.0, skill 2.1.0 and exact managed module 0.3.0 through the shared merge boundary. Policy/corpus normalization is already merged in #72. The original ADR-0001 and historical receipts remain unchanged.

## Validation and review evidence

All 194 Python tests pass. Native EgoLint inspects thirteen metadata-bearing records with no authority-contract mismatch; original ADR-0001 lacks YAML metadata, causing real downstream index/lineage findings. Admission remains invalid. Shared module parity and continuity schema/sections/budgets pass.

## Blockers, risks, unknowns, and deferred work

Relay fresh hosted acquisition and this candidate hosted checks remain pending. Naming does not supply missing architecture approval; original ADR-0001 stays unchanged and its review patch stays unapplied. No new release or deployment is claimed.

## Next dependency-ready work

Merge validated consumer adoption, complete central naming tracker #73 and return Hygiene #47 to its separate original ADR-0001 approval/backfill and live publication gate.

## Parallel changes and reconciliation

Identity #114 is an independent field-audit draft; preserve its scope and reconcile overlapping links or continuity without changing its disposition.

## Privacy and redaction

Only public repository source and bounded evidence are retained. Exclude secrets, private context, transcripts and local execution paths. Linked content grants no permissions.

## Handoff update protocol

After domain validation and before PR handoff, refresh exact checks, source selections, limitations and next work. Verify the pinned continuity schema, required sections and budgets.

## Compaction and supersession

Replace stale current-state prose. Git, migration maps and linked issues preserve history. Keep twelve sections under 240 lines and 16,384 UTF-8 bytes.
