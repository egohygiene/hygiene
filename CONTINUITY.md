---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-03T06:00:58Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Compose the exact selected Aether release validator with structural Hygiene handoff/trigger
    checks and explicit native evidence.
  includes: &id001
  - Verify selected owner validator/schema/runtime-lock bytes and execute full normative validation; unavailable/fallback
    inputs cannot pass.
  - Validate actual Task definitions and only workflow_dispatch events across supported YAML forms; reject
    duplicate/unknown declaration data.
  - Keep preparation read-only, emit deterministic source/runtime/declaration evidence and leave policy/ADR
    approval and publication separate.
  excludes:
  - Implicit downloads/installations inside the checker, tag/release/deployment/credential actions and
    policy activation.
  - Regression suites, actual Task/manual-workflow execution, hosted CI and issue closure.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - tools/releases.py
  - tools/release-owner.lock.json
  - .egohygiene/release.json
  - .tasks/release.yml
  - .github/workflows/release-policy.yml
  - docs/ecosystem/REPOSITORY_RELEASE.md
  - docs/decisions/ADR-0015-compose-pinned-release-validation.md
  - tests/test_release_policy.py
  - catalog/repository-release-policy.json
  - https://github.com/egohygiene/hygiene/issues/84
work:
  objective: Compose the exact selected Aether release validator with structural Hygiene handoff/trigger
    checks and explicit native evidence.
  success_conditions: *id001
  active_issue:
    provider: github
    id: egohygiene/hygiene#84
    url: https://github.com/egohygiene/hygiene/issues/84
  next:
    kind: action
    id: review-draft-and-qualify
    description: Review the composed validator and proposed ADR-0015; qualify negative/native/Task/workflow
      cases during the deferred checks pass, preserving existing peer drafts and the selected immutable
      owner pin.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/84
    depends_on: []
state:
  base:
    revision: 09783cb411445248c9184c3a03a3a87f97d1d375
    ref: refs/heads/main
    verified_at: '2026-11-03T06:00:58Z'
  candidate:
    branch: codex/84-release-contract-composition
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-03T06:00:58Z'
    default_branch_revision: 09783cb411445248c9184c3a03a3a87f97d1d375
    issue_state: open
    pull_request_state: not-applicable
    notes: Main09783cb contains merged URL/origin PR92. Issue84 and tracker76 are open; peer audit75/presentation89/decision90/continuity91
      remain open and unchanged. This candidate performs no merge or publication and does not accept ADR-0015.
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
  reviewed_at: '2026-11-03T06:00:58Z'
  reviewed_by: Codex
  evidence:
  - command: python3 tools/releases.py validate-profile
    outcome: passed
    observed_at: '2026-11-03T06:00:58Z'
    notes: The existing proposed policy profile validates; its pin/version/status and catalog/schema bytes
      are unchanged.
  - command: python3 tools/releases.py verify-owner --aether-source .cache/release/aether
    outcome: passed
    observed_at: '2026-11-03T06:00:58Z'
    notes: Selected Aether8a2a3d08f3aa9da3847bd5277843506ab855192e validator/schema/runtime-lock bytes
      match their recorded SHA-256 values. Source verification alone is not declaration validation.
  - command: python3 tools/releases.py validate-declaration --repository . --format json
    outcome: passed
    observed_at: '2026-11-03T06:00:58Z'
    notes: The actual pinned native entrypoint and full Draft202012Validator execute, followed by structural
      local checks. Receipt status passed; declaration digest5c0fcf3190cde8165585de9cdcbfde3367d44c8fd15975f0fb9a672578dceb32.
      Observed jsonschema4.26.0/PyYAML6.0.3; policy remains proposed.
  - command: Two Python AST parses; new ADR metadata/schema; local documentation targets and git diff
      --check
    outcome: passed
    observed_at: '2026-11-03T06:00:58Z'
    notes: Sources parse and seven new regression methods are authored but unexecuted. ADR-0015 is structurally
      valid, proposed with null approval. The manual-only workflow and Task definitions were parsed but
      not executed.
  - command: Pinned continuity metadata/schema/formats, twelve headings, size and privacy inspection
    outcome: passed
    observed_at: '2026-11-03T06:00:58Z'
    notes: One bounded source handoff meets structural/privacy/budget checks; official EgoLint conformance
      is unexecuted.
  - command: Regression suites, Task dispatch, manual workflow runtime, owner-lock dependency installation
      and hosted CI
    outcome: not-run
    observed_at: '2026-11-03T06:00:58Z'
    notes: No test or workflow executes and no dependency install occurs. Existing available runtime establishes
      only the recorded positive declaration proof.
  environment_limitations:
  - Seven new regressions, actual Task dispatch and the changed manual workflow remain unexecuted; issue84
    stays open.
  - Current positive proof uses jsonschema4.26.0/PyYAML6.0.3. The future manual workflow selects the owner
    lock with jsonschema4.10.3/PyYAML6.0.1; that runtime path was not executed.
  - Prepared selected owner source and full dependencies are required for composed declaration checks;
    unavailable or weaker fallback validation fails explicitly. Profile/resolve remain standard-library-only.
  - ADR-0015 and the existing release policy remain proposed; no approval, adoption, tag, release or deployment
    is inferred.
  - Tracker76 retains independent audit/schema consistency and qualification work.
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

Record the bounded issue84 composition repair below user/runtime, scoped instructions, live evidence and canonical sources. It grants no publication authority.

## Resume protocol

Read AGENTS, release guidance, owner lock, native Aether pin, proposed ADR-0015 and issue84/tracker76. Main already contains merged92; preserve peer drafts75/89/90/91.

## Current objective and success conditions

Execute exact selected native validation with full schema support, then prove actual Task identity and manual-only trigger structure without copying the producer protocol or publishing anything.

## State snapshot

Base main09783cb411445248c9184c3a03a3a87f97d1d375 includes merged92. Issue84 and existing peers are open. Candidate codex/84-release-contract-composition has null self-revision/PR before creation.

## Completed and material changes

The checker locks selected owner bytes, runs the native full validator, rejects unavailable/fallback inputs and records declaration/source/runtime evidence. YAML checks cover actual task definitions and manual-only triggers, including quoted/flow/comment forms and duplicates. Task/manual-workflow wiring shares the same prepared source/checker. ADR-0015 proposes the bounded runtime choice without changing catalog formats or approval.

## Validation and review evidence

Profile/source verification and the actual composed declaration CLI exit0. Receipt identifies immutable owner8a2a3d0, full jsonschema4.26.0/PyYAML6.0.3 and the unchanged declaration digest. Python/ADR metadata/local links/whitespace and continuity checks pass. No regression case or Task/workflow executes.

## Blockers, risks, unknowns, and deferred work

New and existing suites, real Task/manual workflow and official EgoLint/hosted CI remain unexecuted. The future owner-lock dependency versions differ from the observed current positive runtime and are unqualified here. ADR-0015/policy stay proposed; no publication or issue closure occurs.

## Next dependency-ready work

Review the source/ADR proposal and qualify native negative cases plus real handoffs in the deferred pass. Preserve the current owner pin and explicit unavailable behavior; do not treat a plan as approval to publish.

## Parallel changes and reconciliation

Existing audit75, presentation89, decision90 and continuity91 remain separate. Root checkpoint and decision-index changes may need semantic reconciliation during later integration; preserve proposed states, owner contracts and their source evidence.

## Privacy and redaction

Retain only public scoped source facts, immutable owner hashes and synthetic fixtures. No private workbook data, personal context, credentials or machine-local paths are committed.

## Handoff update protocol

Refresh after actual checks/review. ADR-Ref: ADR-0015 proposes exact native composition and conditional full runtimes; it remains proposed with null approval. Existing accepted policy and proposed release/catalog records retain their statuses. No merge or lifecycle promotion is claimed.

## Compaction and supersession

Keep twelve required sections and existing size budgets. Canonical release guidance, lock, owner source, Git and issue84 retain detailed requirements/history.
