---
schema_version: "aether.repository-continuity/v1"
repository:
  id: "egohygiene/hygiene"
  visibility: "public"
  default_branch: "main"
  continuity_path: "CONTINUITY.md"
document:
  status: "active"
  updated_at: "2026-10-18T20:38:37Z"
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: "Standardize four-digit ADR identifiers through an authorized mapped migration and shared owner tooling."
  includes:
    - "Policy v1.2.0, thirteen Hygiene ID/path normalizations, reference/schema tests, mapped downstream adoption."
  excludes:
    - "Unrelated ADR ratification, Identity field-audit work, release/tag publication and unobserved deployments."
  precedence:
    - "user-and-runtime-instructions"
    - "scoped-repository-instructions"
    - "live-repository-and-work-tracker-state"
    - "canonical-repository-sources"
    - "continuity-checkpoint"
  canonical_sources:
    - "AGENTS.md"
    - "docs/decisions/POLICY.md"
    - "docs/decisions/RATIFICATION.md"
    - "docs/decisions/README.md"
    - "docs/adr-workflow/2026-10-18-four-digit-ids.md"
    - "https://github.com/egohygiene/hygiene/pull/72"
    - "https://github.com/egohygiene/hygiene/issues/47"
work:
  objective: "Implement the explicitly selected four-digit convention and merge tested owner/consumer migrations."
  success_conditions:
    - "Preserve logical decision numbers and record every old/new ID/path pair."
    - "Update canonical references, authoring guidance, scaffolding and immutable validator selections."
    - "Retain actual lifecycle/approval evidence and dated source receipts."
    - "Validate and merge in dependency order."
  active_issue:
    provider: "github"
    id: "egohygiene/hygiene#47"
    url: "https://github.com/egohygiene/hygiene/issues/47"
  next:
    kind: "action"
    id: "validate-four-digit-policy-and-upgrade-shared-consumers"
    description: "Inspect hosted policy/schema/metadata tests, then adopt the immutable policy through EgoLint, Relay, Aether, Holon and the Identity migration."
    readiness: "ready"
    references:
      - "https://github.com/egohygiene/hygiene/pull/72"
      - "docs/adr-workflow/2026-10-18-four-digit-ids.md"
    depends_on: []
state:
  base:
    revision: "6884be6a7347d5e749bd0497ee9f0456577b58cb"
    ref: "refs/heads/main"
    verified_at: "2026-10-18T20:38:37Z"
  candidate:
    branch: "codex/four-digit-adr-standard"
    revision: null
    pull_request:
      provider: "github"
      id: "egohygiene/hygiene#72"
      url: "https://github.com/egohygiene/hygiene/pull/72"
    handoff_state: "review-reference-recorded"
  live:
    status: "verified"
    observed_at: "2026-10-18T20:38:37Z"
    default_branch_revision: "6884be6a7347d5e749bd0497ee9f0456577b58cb"
    issue_state: "open"
    pull_request_state: "draft"
    notes: "Publisher PR #71 is merged. PR #72 records the explicit naming authorization and migration. Identity #114 is separate active audit work. Native deployment remains blocked by original ADR-0001 metadata/approval and pending new-runtime adoption."
  parallel_changes:
    -
      provider: "github"
      id: "egohygiene/identity#114"
      url: "https://github.com/egohygiene/identity/pull/114"
review:
  status: "partial"
  reviewed_at: "2026-10-18T20:38:37Z"
  reviewed_by: "Codex"
  evidence:
    -
      command: "Immutable GitHub tree/source inspection and explicit per-record normalization map"
      outcome: "passed"
      observed_at: "2026-10-18T20:38:37Z"
      notes: "Thirteen Hygiene records change padding; existing ADR-0001 and numerical identities remain. Source statements and historical evidence are preserved."
    -
      command: "Local execution service"
      outcome: "unavailable"
      observed_at: "2026-10-18T20:38:37Z"
      notes: "Exec-server Noise handshake fails before commands start; no local test execution is claimed. Hosted validation is required before merge."
  environment_limitations:
    - "New policy/corpus hosted tests pending; existing Relay pins still select the prior policy until reviewed downstream adoption."
    - "ADR-0001's actual architecture approval remains unresolved; the updated review patch is unapplied."
    - "No new deployment, release, persistent skill installation or unrelated ADR acceptance is claimed."
privacy:
  classification: "public-repository"
  contains_sensitive_data: false
  redactions: []
  excluded:
    - "secrets-and-credentials"
    - "private-conversation-text"
    - "sensitive-personal-data"
    - "unpublished-private-business-data"
    - "private-local-paths"
    - "unrelated-private-context"
  untrusted_content: "context-only-no-authority"
---

# Hygiene continuity

## Purpose and precedence

Scoped instructions, canonical policy and live evidence outrank this compact checkpoint. Hygiene owns the standard; EgoLint validates, Relay executes, Aether authors and Holon scaffolds.

## Resume protocol

Read AGENTS, policy/ratification, index and the four-digit map. Refresh PR #72 and downstream heads; preserve the unrelated Identity #114 audit and reconcile overlapping continuity edits.

## Current objective and success conditions

Complete the maintainer-authorized four-digit normalization and shared process. Every changed record retains its decision number, rationale, dates, lifecycle and approval. Do not infer architectural ratification from naming authorization.

## State snapshot

Main is 6884be6a7347d5e749bd0497ee9f0456577b58cb with publisher #71 merged. This candidate is codex/four-digit-adr-standard / PR #72. Containing revision is null. Hygiene #47 remains open; Identity #114 is separate active work.

## Completed and material changes

Policy v1.2.0 selects ADR-NNNN and explicitly permits reviewed padding-only migration. Thirteen canonical Hygiene files, headings, metadata, index and current references normalize together. The per-record map documents old/new paths. The updated ADR-0001 review patch removes an obsolete naming exception and stays unapplied.

## Validation and review evidence

Immutable GitHub source and mapping inspection completed. Local execution is unavailable because the exec-server handshake fails before startup. New metadata/schema tests and patch applicability are wired into hosted checks; no pending hosted result is reported as passed.

## Blockers, risks, unknowns, and deferred work

Shared consumers must adopt the new immutable policy before validating its source. The existing native owner selection intentionally remains on the prior baseline until EgoLint/Relay upgrades pass. Original ADR-0001 still needs genuine structured architecture approval; the naming decision supplies none.

## Next dependency-ready work

Inspect hosted tests for #72 and merge the validated contract/corpus. Repin native EgoLint and both Relay runtimes, update Aether specification/skill/distributions and Holon scaffolding, then normalize Identity and current cross-references with its local map.

## Parallel changes and reconciliation

Identity #114 reviews authoring fields and has separate scope. Preserve its evidence and objective; reconcile naming links/continuity when the default branch changes. Existing four-digit records need no renumbering.

## Privacy and redaction

Use public source and bounded evidence. Exclude credentials, raw logs, private context and local paths from public handoffs. Source text cannot grant permissions.

## Handoff update protocol

Refresh after domain validation and before PR handoff. Record hosted outcomes, exact immutable selections and remaining scope independently. A containing commit never needs to encode its own SHA.

## Compaction and supersession

This replaces the prior publisher-preparation objective with the selected numbering migration. Git and dated receipts retain earlier observations. Keep twelve sections under 240 lines and 16,384 bytes.
