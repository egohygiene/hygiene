---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-09T11:39:50Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Align the strict repository Pages publisher with one immutable portable Relay review candidate.
  includes:
  - Select Relay 49046d88ef6fe2e31e9a9f443a61157b598efb78 consistently for native validation, generation,
    composition helpers and the consumer exact-generator seal.
  - Retain canonical ADR-only collection, policy-owner selection, source admission and the single consumer deployer.
  - Refresh current publisher guidance while preserving historical source, approval and recovery evidence.
  excludes:
  - ADR-0001 metadata or human disposition, new sources, owner-policy changes and publication authority.
  - Tests, native replay, builds, hosted CI, workflow dispatch, merge, deployment and live verification.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - .github/workflows/publish-pages.yml
  - publication/site.json
  - publication/README.md
  - tools/publication.py
  - .config/egolint/repository-intelligence.toml
  - docs/decisions/POLICY.md
  - docs/decisions/ADR-0002-organization-adr-and-delivery-history.md
  - docs/adr-workflow/CAPTURE.md
  - https://github.com/egohygiene/hygiene/issues/47
  - https://github.com/egohygiene/relay/pull/167
work:
  objective: Propose a consistent immutable Relay selection for the existing strict Hygiene Pages publisher.
  success_conditions:
  - All five current workflow references and publication/site.json bind the same exact public Relay revision.
  - Workflow structure, source gate, permissions, recovery ordering and historical evidence remain unchanged.
  - Review clearly distinguishes prepared source from native execution, source admission and actual publication.
  active_issue:
    provider: github
    id: egohygiene/hygiene#47
    url: https://github.com/egohygiene/hygiene/issues/47
  next:
    kind: action
    id: review-portable-publisher-selection
    description: Review this bounded pin candidate with Relay draft167, then qualify native collection,
      complete bundles and consumer publication in the deferred validation pass. Resolve ADR-0001 authority
      and metadata separately before any source-admitted deployment.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/47
    - https://github.com/egohygiene/relay/pull/167
    - https://github.com/egohygiene/relay/issues/101
    - https://github.com/egohygiene/.github/issues/41
    depends_on: []
state:
  base:
    revision: 92195e49b50778517ef670a7ec97c922dbdf9cec
    ref: refs/heads/main
    verified_at: '2026-11-09T11:37:20Z'
  candidate:
    branch: codex/hygiene-intelligence-portable-upgrade
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-09T11:37:20Z'
    default_branch_revision: 92195e49b50778517ef670a7ec97c922dbdf9cec
    issue_state: open
    pull_request_state: not-applicable
    notes: Live main contains merged release-composition PR93. Issue47 retains the original ADR-0001
      metadata/human-approval and publication gates. Relay draft167 exposes exact review revision
      49046d88ef6fe2e31e9a9f443a61157b598efb78. Existing open drafts75/89/90/91 overlap only CONTINUITY
      within this candidate scope; no publisher/config/helper change was found in their current file lists.
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
  - provider: github
    id: egohygiene/relay#167
    url: https://github.com/egohygiene/relay/pull/167
review:
  status: partial
  reviewed_at: '2026-11-09T11:39:50Z'
  reviewed_by: Codex
  evidence:
  - command: Live repository/issue/open-PR inspection and git ls-remote for Hygiene main and the exact Relay branch
    outcome: passed
    observed_at: '2026-11-09T11:37:20Z'
    notes: Public identity, immutable base/candidate dependency and known overlap were checked; linked
      human approval and production publication remain separate facts.
  - command: Static workflow/config/guidance diff and unchanged source/recovery inventory inspection
    outcome: limited
    observed_at: '2026-11-09T11:39:50Z'
    notes: Five workflow SHA replacements align with site.json. Native owner pins, collect-adrs/policy-owner,
      source admission, job gates, permissions, transport helper and recovery order remain unchanged.
  - command: Data-only JSON/YAML parsing, continuity headings/budget inspection and git diff --check
    outcome: limited
    observed_at: '2026-11-09T11:39:50Z'
    notes: Static syntax and structure only; this is not source conformance or executed publication proof.
  - command: Independent static peer review of the bounded publisher/config/guidance diff
    outcome: limited
    observed_at: '2026-11-09T11:39:50Z'
    notes: No scoped source blocker found. Review confirms pin/config equality and preserved strict
      source inputs, workflow jobs, gates and dated evidence; it does not execute the producer or publisher.
  - command: Tests, native EgoLint/collector replay, full contract/continuity validation, rendering, hosted CI and live verification
    outcome: not-run
    observed_at: '2026-11-09T11:39:50Z'
    notes: Explicitly deferred implementation pass; no install, workflow dispatch, build or deployment was performed.
  environment_limitations:
  - The selected Relay revision is a public draft review candidate, not a qualified release or consumer acceptance result.
  - Original ADR-0001 metadata and actual human architecture approval remain unresolved under issue47;
    the review patch stays unapplied and the strict source gate remains active.
  - Complete generated-bundle equality, route/asset/browser behavior, hosted admission and live recovery remain unexecuted.
  - Earlier audit/schema/qualification gaps remain with tracker76 and the existing peer drafts; no broader conformance is claimed.
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

Record the bounded publisher dependency candidate below user/runtime instructions, scoped guidance, live evidence and canonical sources. This checkpoint supplies no approval or publication authority.

## Resume protocol

Read AGENTS, the publisher workflow/config/runbook, unchanged consumer helper, native owner configuration, issue47 and Relay draft167. Recheck live main and peer drafts before later integration.

## Current objective and success conditions

Align all current validation/generator/composition selections with the exact local seal selection. Preserve strict canonical ADR collection and the repository-owned site/deployment boundary.

## State snapshot

Base main92195e49b50778517ef670a7ec97c922dbdf9cec contains merged PR93. This candidate selects public Relay49046d88ef6fe2e31e9a9f443a61157b598efb78 from draft167; its self-revision and pre-PR reference intentionally remain null. Neither dependency adoption nor source admission is inferred from the draft.

## Completed and material changes

The workflow's five Relay references, publication/site.json and current guidance select one exact candidate. This repairs the prior workflow/config mismatch recorded in issue47 without weakening the exact-generator seal. Relay owns shared portable routes and graph presentation; Hygiene retains its ADR-only source choice, landing, aliases and single publisher. Dated source observations, actual ADRs, approval-null review patches and historical recovery inputs remain unchanged.

## Validation and review evidence

Live source/issue/PR overlap inspection and static data/diff checks are recorded above. The workflow delta is limited to five immutable SHA replacements. No native validator, collector, repository test, site build, CI run or provider publication was executed. Continuity inspection establishes only recorded syntax/structure, not official conformance.

## Blockers, risks, unknowns, and deferred work

Issue47 still requires the original ADR-0001 metadata and real human architecture disposition. Its historical Accepted claim is preserved without new approval; the prepared patch is unapplied. The existing gate can still skip build/deploy. New producer bytes, native compatibility, source admission, public routes/assets, actual deployment and recovery require the deferred qualification pass.

## Next dependency-ready work

Review this dependency-only candidate with Relay draft167, then qualify the pinned pipeline and complete bundle under the existing source gate. Resolve ADR-0001 authority/metadata through its owner before publication. A green advisory run or skipped build is not successful publication.

## Parallel changes and reconciliation

Audit75, presentation89, decision90 and continuity91 remain separate open drafts. Their current changed-file lists overlap this scope only at CONTINUITY.md; reconcile checkpoints semantically on later integration. Parent .github41 and Relay101 coordinate repository-local Intelligence; the central site remains an overview rather than Hygiene's publisher.

## Privacy and redaction

Retain only public source identities, immutable pins and bounded review evidence. No raw provider capture, credentials, private context or local machine path enters the source or checkpoint.

## Handoff update protocol

Refresh after actual review/qualification and before any later handoff. ADR not required: this is a consistent producer selection and exact-seal parity repair under accepted ADR-0002, preserving source, lifecycle and publication authority. The proposed Intelligence/publication designs retain their dispositions.

## Compaction and supersession

Keep the twelve required sections and existing budgets. Git, the publisher runbook and owning issues retain detailed requirements/history; no historical recovery evidence is rewritten by this checkpoint.
