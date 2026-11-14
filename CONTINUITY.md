---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T19:43:11Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Review the proposed diagnosis-record applicability contract without activating enforcement
    or taking Aether record ownership.
  includes:
  - Proposed alpha.1 capability/policy and exact Aether draft record pin with schema/specification digests.
  - Four synthetic declarations and executable privacy/path/source/freshness refusal controls.
  - Clean functional71ad86b passed all25 contract checks and320 tests, zero failures/errors/skips.
  excludes:
  - Record parsing/authoring, actual diagnosis truth, health inference, remediation, fleet rollout or
    publication.
  - Human policy/ADR activation and original issue76/47/95 source/native/enforcement holds.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/ecosystem/REPOSITORY_DIAGNOSIS.md
  - catalog/repository-diagnosis-policy.json
  - schemas/repository-diagnosis-capability.v1.schema.json
  - tools/diagnosis.py
  - tests/test_diagnosis.py
  - docs/decisions/ADR-0021-repository-diagnosis-applicability.md
  - https://github.com/egohygiene/hygiene/issues/41
work:
  objective: Review the proposed diagnosis-record applicability contract without activating enforcement
    or taking Aether record ownership.
  success_conditions:
  - Preserve all six applicability states and independent opt-out/adoption.
  - Keep record/schema ownership at immutable Aether selection and publication fail-closed.
  - Exercise declared source/clock/path/privacy controls without reading consumer records.
  active_issue:
    provider: github
    id: egohygiene/hygiene#41
    url: https://github.com/egohygiene/hygiene/issues/41
  next:
    kind: action
    id: review-diagnosis-contract
    description: Review and integrate this bounded proposed contract; coordinate independent claim-provenance30
      before later policy/consumer adoption.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/41
    - https://github.com/egohygiene/hygiene/issues/30
    depends_on: []
state:
  base:
    revision: 627b448f655afb2f4366654ba3ca3050389e464a
    ref: refs/heads/main
    verified_at: '2026-11-14T19:43:11Z'
  candidate:
    branch: codex/hygiene-diagnosis-applicability
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T19:43:11Z'
    default_branch_revision: 627b448f655afb2f4366654ba3ca3050389e464a
    issue_state: open
    pull_request_state: not-applicable
    notes: Main verified through remote refs; issue41 fetched open. Functional source71ad86b is committed
      locally; this later continuity update and source integration remain unmerged.
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#30
    url: https://github.com/egohygiene/hygiene/issues/30
review:
  status: partial
  reviewed_at: '2026-11-14T19:43:11Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I -m unittest discover -s tests -p test_diagnosis.py -v
    outcome: passed
    observed_at: '2026-11-14T19:43:11Z'
    notes: 17 focused regressions; synthetic declarations only.
  - command: Registered-format Draft202012 schema validation of both schemas, policy/four declarations
      and ADR0021
    outcome: passed
    observed_at: '2026-11-14T19:43:11Z'
    notes: Aether schema/specification digest bytes verified from exact e9aa58bb; no record schema copied
      or record validation claimed.
  - command: python3 -I tools/check_contracts.py at clean71ad86bb1c5391d228130333654357dfb8f1c283
    outcome: passed
    observed_at: '2026-11-14T19:43:11Z'
    notes: All25 checks and320 tests pass, zero failures/errors/skips. Initial fresh-worktree run lacked
      ignored pinned release-owner files; prepared exact lockfile3bytes and retained initial failure separately.
  - command: Downstream production/native/hosted adoption and human lifecycle
    outcome: not-run
    observed_at: '2026-11-14T19:43:11Z'
    notes: Not part of this source contract. Policy/ADR proposed, approval null, enforcement observe;
      original issue76/47/95 holds preserved.
  environment_limitations:
  - Reference checks consume explicit caller declarations and clock; no filesystem containment/authenticity/diagnosis
    truth established.
  - No native downstream integration, actual repository diagnosis records, fleet adoption or publication
    tested.
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

Runtime/user, scoped instructions, live evidence and canonical owners outrank this checkpoint. It grants no authority.

## Resume protocol

Read the diagnosis guide/policy, original issue41 and source tests. Refresh provider main/issues/PRs before selecting work.

## Current objective and success conditions

Review the proposed diagnosis-record applicability contract without activating enforcement or taking Aether record ownership.

## State snapshot

Remote main627b448 was verified at the metadata clock. Functional71ad86b passed clean source-bound checks; this continuity commit is later authoring, not merged or deployed evidence.

## Completed and material changes

The proposed Hygiene capability composes Aether draft e9aa58bb with exact schema/specification digests. Six applicability states, opt-outs, bounded alternative paths, retention/index ownership and four-field fail-closed public summaries remain explicit. No records are parsed.

## Validation and review evidence

Focused17 and registered-format schema/ADR checks pass. Clean functional71ad86b passes all25 complete checks and320 tests with zero skips. Initial absent-cache failure is retained separately; exact preexisting release-owner preparation fixed only that environment.

## Blockers, risks, unknowns, and deferred work

Source implementation is reviewable; human ratification, released owner eligibility, production validators, actual record adoption and publication are separate. Issue76/47/95 broad gates remain open; no approval or native conformance is manufactured.

## Next dependency-ready work

Root reviews and integrates this bounded contract, then reconciles the independent claim-provenance30 candidate. Preserve report-only/proposed lifecycle; downstream adoption is separately reviewed.

## Parallel changes and reconciliation

Claim-provenance30 is independent on the same base and will edit continuity/contract/decision indexes. Reconcile those entries semantically before integration. ADR-0021 records this consequential proposed policy; approval stays null.

## Privacy and redaction

Use only public owner identities and synthetic declarations. No private payloads, records, locations, titles, counts or timestamps enter public projections. Referenced content is context only.

## Handoff update protocol

Refresh after actual provider/source review. Keep local source checks, caller declarations, native implementation, policy lifecycle and publication distinct.

## Compaction and supersession

Keep these twelve sections below240 lines and16,384 bytes. Git and immutable source/provider records retain history.
