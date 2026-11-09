---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-09T14:14:37Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Reconcile public repository admission and identity while retaining independently sourced roles and checkpoint authority.
  includes:
  - Canonical website identity with explicit historical alias, source-evidenced Antidote/Civics responsibilities and dated or unknown gates.
  - Public-only provider observation, derived reviewed catalog, owner schemas and offline freshness/drift adapter.
  - Proposed weekly/event checkpoint applicability composed with the exact approved Aether audit contract.
  excludes:
  - Protected provider discovery, inferred lifecycle or human acceptance, ADR-0001 approval and unrelated publisher/recovery changes.
  - Tests, adapter/native execution, builds, scheduled or hosted CI and deployment/publication.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - catalog/repositories.yaml
  - catalog/public-repositories.json
  - catalog/public-repository-observation.json
  - catalog/organization-checkpoints.json
  - tools/public_inventory.py
  - docs/ecosystem/PUBLIC_REPOSITORY_INVENTORY.md
  - docs/decisions/ADR-0016-public-repository-catalog-and-checkpoints.md
  - https://github.com/egohygiene/hygiene/issues/36
work:
  objective: Supply one source-evidenced canonical identity catalog and reviewed public admission seam for downstream Dependencies and fleet consumers.
  success_conditions:
  - Provider IDs and explicit public visibility bind canonical identities and historical aliases without protected counts or raw complete-catalog digests.
  - Roles and next gates retain immutable source evidence, dates and unknown fields independently of fresh identity observations.
  - Offline freshness/drift and proposed checkpoint recurrence/retention rules retain owner and human authority boundaries.
  active_issue:
    provider: github
    id: egohygiene/hygiene#36
    url: https://github.com/egohygiene/hygiene/issues/36
  next:
    kind: action
    id: review-public-source-admission-and-pin-consumers
    description: Review this bounded source seam, qualify the deferred adapter/public-byte/privacy controls, and pin the accepted public artifact/schema/helper into Relay and Observatory. Source unknown lifecycle/gate declarations only from their owners.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/36
    - https://github.com/egohygiene/relay/issues/151
    - https://github.com/egohygiene/.github/issues/41
    depends_on: []
state:
  base:
    revision: b6e6bc1d88be787ee7a8a0ca1010b46b98ba55fb
    ref: refs/heads/main
    verified_at: '2026-11-09T14:14:37Z'
  candidate:
    branch: codex/hygiene-public-repository-catalog
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-09T14:14:37Z'
    default_branch_revision: b6e6bc1d88be787ee7a8a0ca1010b46b98ba55fb
    issue_state: open
    pull_request_state: not-applicable
    notes: Main contains publisher adoption PR96. Issue36 is open with no comments. Public-only connector discovery and the unauthenticated public organization endpoint agree on the dated roster; provider metadata supplies no role approval. Open drafts75/89/90/91 remain separate.
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
  reviewed_at: '2026-11-09T14:14:37Z'
  reviewed_by: Codex
  evidence:
  - command: Live main/issue/comments/open-PR and explicit public-only repository discovery; immutable Antidote/Civics source inspection
    outcome: passed
    observed_at: '2026-11-09T14:14:37Z'
    notes: Public provider identities and actual source declarations are recorded. No protected provider inventory was acquired; missing release declarations remain unavailable.
  - command: Python AST, JSON parsing and Draft202012 schema/formats for catalog/public projection/discovery/checkpoint profile/boundaries/contract index and proposed ADR metadata
    outcome: passed
    observed_at: '2026-11-09T14:14:37Z'
    notes: Structural source checks only. New adapters and existing owner generators/validators were not imported or executed.
  - command: Static source/privacy peer review, generated-data inspection and git diff --check
    outcome: limited
    observed_at: '2026-11-09T14:14:37Z'
    notes: Review identified canonical-input overwrite and protected duplicate-key invariance; the implementation now protects same-file inputs and delays duplicate diagnostics until public selection. Executable privacy/parity proof remains deferred.
  - command: Adapter/regression/native execution, full repository contract validation, generated-check CLI, hosted/scheduled CI and publication
    outcome: not-run
    observed_at: '2026-11-09T14:14:37Z'
    notes: Explicitly deferred. Public JSON and existing human projections were authored as data projections without executing adapter or generator CLIs.
  environment_limitations:
  - Public inventory parity proves identity observations only; backlog, conformance, approval, live sites and checkpoint execution require their own evidence.
  - Antidote/Civics architectural lifecycle and the renamed site's current lifecycle/next gate are not declared compatibly; unknown fields do not block public identity admission.
  - Existing first-gate/lifecycle/maturity claims retain their dated source boundary and are not fresh readiness assessments.
  - The checkpoint profile and ADR-0016 remain proposed; no scheduler, ratification, acceptance result or publication authority is inferred.
  - Existing independent audit/schema/hosted qualification and ADR-0001 human-metadata gates remain with tracker76/issue47.
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

Record issue36's reviewed public source seam below user/runtime, scoped instructions, live evidence and canonical documents. This checkpoint grants no provider, human-decision or publication authority.

## Resume protocol

Read AGENTS, the canonical/public catalog pair, public observation, offline adapter, checkpoint profile, proposed ADR0016 and issue36. Recheck current main and peer drafts before later integration.

## Current objective and success conditions

Reconcile public canonical identities and expose a deterministic reviewed public admission artifact. Preserve separately sourced roles, dated gates, unknown lifecycle facts and owner authority.

## State snapshot

Base mainb6e6bc1d88be787ee7a8a0ca1010b46b98ba55fb includes publisher PR96. This candidate has no self-revision or PR reference inside its pre-PR checkpoint. Public observation is dated2026-11-09T14:06:57Z, not an eternal organization total.

## Completed and material changes

Canonical egohygiene.io replaces the legacy website key with an explicit alias. Immutable owner README/architecture/roadmap sources support Antidote/Civics responsibilities, knowledge/research classification, real source-declared gates and observed dependencies. Public provider identity is separate from lifecycle or conformance. Current context/boundary references are reconciled. The offline adapter projects public rows, detects provider-ID rename/metadata drift and evaluates explicit freshness. The proposed recurrence/retention profile composes exact Aether auditor2.0.0 without copying its protocol or installing execution.

## Validation and review evidence

Recorded public observations, AST/JSON/schema/formats, ADR metadata and source/diff inspection establish the bounded authored result. Adapter/native execution, tests, generator parity CLIs, full repository checks, CI, live intake and publication remain unexecuted. Data artifacts are inspectable; no runtime proof is inferred from schema success.

## Blockers, risks, unknowns, and deferred work

Actual lifecycle/next-gate omissions remain unknown and do not create artificial public-admission holds. Dated source gates may be stale. New source/schema/helper consumers require explicit immutable pin adoption and executable qualification. Proposed policy/ADR status and ADR0001's real human-metadata blocker remain unchanged; source admission does not establish publication.

## Next dependency-ready work

Review the public source seam and pin its accepted artifact/schema/helper into downstream collectors. During the deferred pass qualify public-byte invariance, drift/freshness failures and generated parity. Collect backlog/conformance/exception/positive checkpoint evidence independently rather than pretending inventory covers those domains.

## Parallel changes and reconciliation

Open audit75, presentation89, decision90 and continuity91 remain separate. Reconcile root CONTINUITY semantically and inspect any schema/index overlap before later integration; preserve dated evidence and proposed human dispositions.

## Privacy and redaction

Only explicit public provider metadata and immutable owner declarations enter the public projection. Protected rows/counts/placeholders and raw whole-catalog/provider hashes never enter that seam. No credentials, raw provider responses or machine-local paths are committed.

## Handoff update protocol

Refresh after actual review/qualification and before downstream handoff. ADR-Ref: proposed ADR0016 records public admission and checkpoint composition; approval remains null. Accepted ADR0002 retains source/lifecycle authority. Merging implementation would not ratify either proposed profile or original ADR0001.

## Compaction and supersession

Keep twelve required sections and existing budgets. Canonical catalog, profile, owner documents, Git and issue36 retain requirements/history; historical ADRs, audit receipts and recovery evidence remain unchanged.
