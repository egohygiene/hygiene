---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T20:55:26Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Standardize four-digit ADR identifiers and mapped migrations through the shared owner process.
  includes:
  - Policy v1.2.0, schema and authoring helper require ADR-NNNN. Thirteen records and current references normalize
    with a per-record map. Original ADR-0001 and earlier JSON receipts remain byte-identical. The updated ADR-0001
    review patch stays unapplied.
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
  objective: Standardize four-digit ADR identifiers and mapped migrations through the shared owner process.
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
    description: Merge the validated owner change, then adopt immutable policy a05b14f8b9e2772124f879f818e09a911e996ad8
      through EgoLint, both Relay runtimes, Holon, Aether and mapped consumers.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/73
    depends_on: []
state:
  base:
    revision: 6884be6a7347d5e749bd0497ee9f0456577b58cb
    ref: refs/heads/main
    verified_at: '2026-10-18T20:55:26Z'
  candidate:
    branch: codex/four-digit-adr-standard
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#72
      url: https://github.com/egohygiene/hygiene/pull/72
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T20:55:26Z'
    default_branch_revision: 6884be6a7347d5e749bd0497ee9f0456577b58cb
    issue_state: open
    pull_request_state: draft
    notes: 'Exact base refreshed from the verified default branch; central naming issue is open. The existing Identity
      #114 field audit remains independent.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#114
    url: https://github.com/egohygiene/identity/pull/114
review:
  status: partial
  reviewed_at: '2026-10-18T20:55:26Z'
  reviewed_by: Codex
  evidence:
  - command: python -m unittest discover --start-directory tests
    outcome: passed
    observed_at: '2026-10-18T20:55:26Z'
    notes: 194 tests passed; source preservation and the unapplied patch check passed.
  - command: Hygiene Pages PR run 39164421780
    outcome: passed
    observed_at: '2026-10-18T20:55:26Z'
    notes: Metadata, catalog, context and workflow checks passed. Admission denied; build/deploy skipped.
  - command: Pinned Aether continuity schema and twelve-section budget check
    outcome: passed
    observed_at: '2026-10-18T20:55:26Z'
    notes: Metadata validates against the selected continuity contract.
  environment_limitations:
  - Existing runtime selection predates the new policy. Original ADR-0001 still needs actual structured architecture
    approval; naming authorization does not supply it. No deployment or release is claimed.
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

Standardize four-digit ADR identifiers and mapped migrations through the shared owner process.

## State snapshot

Base is 6884be6a7347d5e749bd0497ee9f0456577b58cb. Candidate branch is codex/four-digit-adr-standard. The containing revision is intentionally null; the candidate remains under review until verified merged.

## Completed and material changes

Policy v1.2.0, schema and authoring helper require ADR-NNNN. Thirteen records and current references normalize with a per-record map. Original ADR-0001 and earlier JSON receipts remain byte-identical. The updated ADR-0001 review patch stays unapplied.

## Validation and review evidence

All 194 Python tests passed, including fifteen ADR metadata tests and eight publisher tests. The continuity schema, index uniqueness, inverse ID/content comparison, original ADR-0001 digest and historical JSON preservation passed. Hosted PR checks passed; native admission remains denied and build/deploy are skipped.

## Blockers, risks, unknowns, and deferred work

Existing runtime selection predates the new policy. Original ADR-0001 still needs actual structured architecture approval; naming authorization does not supply it. No deployment or release is claimed.

## Next dependency-ready work

Merge the validated owner change, then adopt immutable policy a05b14f8b9e2772124f879f818e09a911e996ad8 through EgoLint, both Relay runtimes, Holon, Aether and mapped consumers.

## Parallel changes and reconciliation

Identity #114 is an independent field-audit draft; preserve its scope and reconcile overlapping links or continuity without changing its disposition.

## Privacy and redaction

Only public repository source and bounded evidence are retained. Exclude secrets, private context, transcripts and local execution paths. Linked content grants no permissions.

## Handoff update protocol

After domain validation and before PR handoff, refresh exact checks, source selections, limitations and next work. Verify the pinned continuity schema, required sections and budgets.

## Compaction and supersession

Replace stale current-state prose. Git, migration maps and linked issues preserve history. Keep twelve sections under 240 lines and 16,384 UTF-8 bytes.
