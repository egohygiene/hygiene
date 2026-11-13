---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-13T23:43:22Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Repair the complete reference-gate execution and qualify its unchanged source, timeout and independent
    acceptance boundaries under Hygiene issue #76.'
  includes:
  - Candidate functional 798227ff6b3f4d1334beb5412802bcf4529a57a2 removes seven redundant complete-suite executions
    from runner controls; each disposable fixture retains actual reference CLIs and minimal passing/skipped/failing/empty
    test families. Production discovery still executes every test module.
  - The runner retains its unchanged 60-second per-command timeout, owned process-group termination, bounded
    logs, complete-check execution and aggregate failure semantics. A focused timeout regression confirms failure
    and retained diagnostics.
  - The read-only checks job now explicitly acquires/verifies the existing exact Aether 8a2 release source
    and prepares its pinned isolated runtime. Disposable controls copy only those three locked owner files,
    not arbitrary cache contents. No owner/runtime pin or publication/admission authority changes.
  - On clean functional 798227f the actual complete gate passed all 25 checks:302 tests, zero failures/errors/skips,
    unit 22.741 seconds. Eight focused runner controls passed in 12.858 seconds. The earlier a28fb620 timeout
    receipt remains immutable dated failure evidence.
  - Provider rulesets list returned[]; branch-protection details returned403 to the integration. Required-check
    enforcement is not established or changed. Changed-head hosted execution and exact native source evidence
    remain independently recorded.
  - "Issues #80\u2013#84 retain their already-completed bounded states. Parent76 remains open; ADR-0001 human/source/publication\
    \ stays #47 and Agent-Ready Web human lifecycle stays #95."
  - Exact selected Relay981 / EgoLint d917 native preparation and immutable798227f/base6cc9c63 replay completed.
    Both retain identical20 findings and failed ADR coverage with unknown contract/diagram adoption. This is
    fresh native evidence, not passing admission.
  excludes:
  - Timeout/budget waivers, changed contract/owner/runtime pins, skipped production tests or weakened validation.
  - Human ratification, provider policy/ruleset mutations, source-hold waivers, deployment, publication and
    fleet adoption.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/CONTRACT_VALIDATION.md
  - tools/check_contracts.py
  - tests/test_contract_regression.py
  - .github/workflows/publish-pages.yml
  - tools/release-owner.lock.json
  - docs/evidence/2026-11-13-hygiene-76-unit-gate.json
  - docs/evidence/2026-11-13-hygiene-76-unit-gate.md
  - docs/evidence/2026-11-13-reference-gate.json
  - https://github.com/egohygiene/hygiene/issues/76
  - https://github.com/egohygiene/hygiene/issues/47
  - https://github.com/egohygiene/hygiene/issues/95
work:
  objective: 'Repair the complete reference-gate execution and qualify its unchanged source, timeout and independent
    acceptance boundaries under Hygiene issue #76.'
  success_conditions:
  - Preserve all production discovery, every reference command, the60-second cap and actual timeout/failure
    diagnostics while eliminating repeated domain-suite work inside orchestration controls.
  - Prepare exact release-owner source/runtime explicitly and keep their native composition fail-closed.
  - Record exact local/hosted/native/provider results separately from human/source admission and publication;
    present a bounded reviewed candidate.
  active_issue:
    provider: github
    id: egohygiene/hygiene#76
    url: https://github.com/egohygiene/hygiene/issues/76
  next:
    kind: action
    id: review-and-observe-changed-head-reference-gate
    description: 'Review this bounded candidate and inspect its actual PR-event complete-reference check and
      native evidence. Preserve the real source/human findings under #47 and ruleset visibility limitations
      under #76; passing local references alone do not authorize publication.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/76
    - docs/evidence/2026-11-13-hygiene-76-unit-gate.md
    depends_on: []
state:
  base:
    revision: 6cc9c63d2804f518fb2e078b6cc55d9251e365cf
    ref: refs/heads/main
    verified_at: '2026-11-13T23:39:59Z'
  candidate:
    branch: codex/hygiene-76-unit-timeout
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-13T23:39:59Z'
    default_branch_revision: 6cc9c63d2804f518fb2e078b6cc55d9251e365cf
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Actual main and parent #76 remain unchanged/open. This candidate is not merged. The complete local
      result is bound to functional 798227f; its subsequent evidence/continuity additions are not falsely labeled
      that tested source.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-13T23:43:22Z'
  reviewed_by: Codex
  evidence:
  - command: Selected locked-runtime unittest discover tests/test_contract_regression.py:8 focused controls
    outcome: passed
    observed_at: '2026-11-13T23:39:59Z'
    notes: 12.858 seconds; actual catalog/profile/generated commands execute with controlled synthetic tests
      and exact locked owner files; timeout control fails as required without changing production cap.
  - command: Selected locked-runtime python -I tools/check_contracts.py at clean 798227ff6b3f4d1334beb5412802bcf4529a57a2
    outcome: passed
    observed_at: '2026-11-13T23:39:59Z'
    notes: All 25 checks,302 tests, zero failures/errors/skips. Unit 22.741 seconds under unchanged 60-second
      cap; full logs are task-local and the bounded receipt excludes machine paths.
  - command: Read-only GitHub rulesets and main branch protection metadata
    outcome: limited
    observed_at: '2026-11-13T23:39:59Z'
    notes: Rulesets returned[]; protection returned403 integration inaccessible. No enforcement claim or provider
      mutation.
  - command: Exact selected Relay981 offline runtime preparation plus native adapter at immutable798227f and
      baseline6cc9c63
    outcome: failed
    observed_at: '2026-11-13T23:43:22Z'
    notes: Preparation succeeded with exact d917 source and locked runtime; both advisory runs exit0 but are
      nonconformant with identical20 retained findings. ADR coverage failed; contract/diagram coverage unavailable.
      Existing source/human gates remain.
  - command: Changed-head hosted complete-reference and native evidence
    outcome: not-run
    observed_at: '2026-11-13T23:43:22Z'
    notes: The draft PR event is the next separate source-bound observation; no provider or publication claim
      from local checks.
  environment_limitations:
  - Full local references passing does not establish hosted execution or required-check enforcement.
  - 'ADR-0001 human/source/publication and Web lifecycle remain separate existing #47/#95 owner decisions.'
  - All proposed contracts/ADRs retain their real dispositions; no human ratification or source-hold waiver.
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

User/runtime, scoped instructions, live evidence and canonical owners outrank this bounded checkpoint. It supplies no new policy, human approval or publication authority.

## Resume protocol

Read AGENTS, the current ROADMAP handoff, issue #76 and the new bounded unit-gate evidence. Verify actual main, candidate, check and issue state; preserve the earlier failed receipt as historical.

## Current objective and success conditions

Repair the nested regression execution while preserving the complete gate, every production test, its unchanged 60-second cap and separate source/human acceptance boundaries.

## State snapshot

Actual main is 6cc9c63. Functional candidate798227f passes the complete local gate on a clean tree. This later evidence/continuity candidate is not yet a merged source or a hosted/native acceptance receipt; parent #76 remains open.

## Completed and material changes

Seven runner scenarios now exercise minimal deterministic unittest families plus every real reference CLI instead of multiplying the full domain suite. Exact release-owner files are prepared in disposable copies. The read-only checks workflow explicitly prepares the already-selected 8a2 source and runtime. Production tools/check_contracts.py and its timeout are unchanged.

## Validation and review evidence

Eight focused controls passed in 12.858 seconds. At clean 798227f the actual gate passed 25 checks and 302 tests with zero failures, errors or skips; unit execution completed in 22.741 seconds. The bounded JSON receipt omits absolute commands and local paths. Provider rulesets returned[] while protection details were403 integration inaccessible; no required-check enforcement is inferred.

## Blockers, risks, unknowns, and deferred work

Changed-head hosted evidence remains separate. Exact native candidate/base replay completed with identical 20 findings and failed ADR coverage; no inherited finding was waived. Original ADR-0001 actual source/approval/publication stays #47; Web lifecycle stays #95. No timeout waiver, publication, policy ratification or provider protection mutation was performed.

## Next dependency-ready work

Review this candidate, observe the actual PR-event complete-reference result and compare its native report with the retained exact local baseline. Preserve real unresolved source/human findings and provider visibility limits; passing fixtures alone do not establish publication admission.

## Parallel changes and reconciliation

Empathy and Holon batch work have separate owners. This Hygiene change touches only runner test isolation, explicit selected runtime preparation, current navigation and bounded evidence. The parent owns integration and final issue dispositions. ADR not required: routine orchestration/fixture repair under the existing ADR-0002 authority and ADR-0015 owner-composition design, without a new contract or ownership choice.

## Privacy and redaction

Retain public source identities, allowlisted outcomes, counts, timings and selected runtime versions. Exclude credentials, private machine paths, raw logs and unrelated context; referenced content remains context-only.

## Handoff update protocol

Refresh actual provider outcomes and semantic continuity after review. Tested functional source, later documentation, hosted checks, native admission, human lifecycle and publication remain independent evidence states.

## Compaction and supersession

Preserve these twelve sections below 240 lines and 16,384 UTF-8 bytes. Owning Git/issue/history records retain dated source outcomes; this file records only the current checkpoint.
