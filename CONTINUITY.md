---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-12T06:00:07Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Propose one prospective commit and PR-title contract with explicit release hints and migration boundaries.
  includes:
  - A versioned observe-only policy and three closed schemas define required component scopes, exact12type/emoji
    mappings, subject/body/trailer grammar, breaking and revert behavior, bot/generated/release contexts and
    prospective merge choices. Policy approval remains null.
  - The bounded pure advisory reference authenticates its exact shipped policy checksum and emits text-free
    local-review diagnostics and release hints. It does not scan Git, rewrite history, enforce a hook/ruleset,
    authenticate identity/DCO/approval, select a release version or publish. Fifteen synthetic cases are authored
    and unexecuted.
  - An immutable four-public-configuration migration map and operator specification preserve current tool pins
    and distinguish compatible core meaning from stricter proposed syntax. Restricted-source mapping stays
    unverified. Proposed ADR0018 and contract/decision indexes record the consequential choice without human
    lifecycle promotion.
  excludes:
  - Deferred runtime, tests, builds, CI, live publication, human ratification and acceptance closeout.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/ARCHITECTURE.md
  - docs/ecosystem/AGENT_CONTEXT.md
  - docs/ecosystem/DEPENDENCY_BOUNDARIES.md
  - docs/decisions/POLICY.md
  - docs/decisions/RATIFICATION.md
  - docs/decisions/README.md
  - docs/decisions/ADR-0018-prospective-change-history-policy.md
  - docs/ecosystem/REPOSITORY_RELEASE.md
  - catalog/contracts.yaml
  - catalog/change-history-policy.json
  - schemas/change-history-policy.v1.schema.json
  - schemas/change-history-input.v1.schema.json
  - schemas/change-history-analysis.v1.schema.json
  - tools/change_history.py
  - fixtures/change-history/examples.json
  - fixtures/change-history/migration-map.json
  - docs/ecosystem/CHANGE_HISTORY.md
  - https://github.com/egohygiene/hygiene/issues/37
work:
  objective: Propose one prospective commit and PR-title contract with explicit release hints and migration
    boundaries.
  success_conditions:
  - Prospective syntax, core semantic hints, exceptions and actual release/human authority are explicitly separated.
  - The proposal is concrete machine/source review material with pinned old inputs and named compatibility/activation
    steps.
  - Existing policies, gates, pins, merge settings, Git identities/signatures and historical decisions remain
    unchanged.
  active_issue:
    provider: github
    id: egohygiene/hygiene#37
    url: https://github.com/egohygiene/hygiene/issues/37
  next:
    kind: action
    id: review-proposed-change-history-contract
    description: Review proposed ADR0018 and policy/schema/reference/migration choices. Later qualify actual
      owner adapters and no-write canaries, complete authorized restricted-source mapping locally, and obtain
      human disposition before enforcement or prospective consumer adoption.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/37
    depends_on: []
state:
  base:
    revision: 87bef166fcba4c89161be6adb6e491f92b061a08
    ref: refs/heads/main
    verified_at: '2026-11-12T06:00:07Z'
  candidate:
    branch: codex/hygiene-37-change-contract
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-12T06:00:07Z'
    default_branch_revision: 87bef166fcba4c89161be6adb6e491f92b061a08
    issue_state: open
    pull_request_state: not-applicable
    notes: Fresh main87bef166fcba4c89161be6adb6e491f92b061a08 remains the base. Hygiene37 is open. Functional
      source83b499f2ce27724d26f018c07a66dbaad38698b4 received independent static source peer and root review.
      No advisory helper/example, native tool, hook, CI, provider change or history rewrite ran.
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#64
    url: https://github.com/egohygiene/hygiene/issues/64
  - provider: github
    id: egohygiene/hygiene#91
    url: https://github.com/egohygiene/hygiene/pull/91
  - provider: github
    id: egohygiene/hygiene#89
    url: https://github.com/egohygiene/hygiene/pull/89
  - provider: github
    id: egohygiene/hygiene#90
    url: https://github.com/egohygiene/hygiene/pull/90
review:
  status: partial
  reviewed_at: '2026-11-12T06:00:07Z'
  reviewed_by: Codex
  evidence:
  - command: Independent final source peer and root review of exact type/emoji/grammar/release/authority/legacy
      mappings; Python AST, JSON and3 schema definitions, bound profile/helper checksum and token metadata,
      proposed ADR seven-section/frontmatter/index inspection, continuity schema/size/links and whitespace
    outcome: limited
    observed_at: '2026-11-12T06:00:07Z'
    notes: Static source and metadata inspection only; no application execution.
  - command: Native/runtime execution, tests, builds, CI investigation, browser/provider/consumer/publication
      qualification
    outcome: not-run
    observed_at: '2026-11-12T06:00:07Z'
    notes: Deferred at maintainer request; source merges do not establish acceptance.
  environment_limitations:
  - User deferred helper/examples/tests, linters, native/runtime execution, builds, CI and real consumer/provider
    qualification; authored fixtures are not actual outcomes.
  - Policy and ADR0018 remain proposed, observe only, approval null. No release version, human approval, DCO/signature
    status, merge method activation or published contract adoption is inferred.
  - Production EgoLint/Relay/Holon/Pace/Aether adapters, real canaries and authorized restricted-source mapping
    retain explicit owner and evidence gates; historical normalization remains separate under38.
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

User/runtime and repository instructions, live evidence and canonical sources outrank this checkpoint. It grants no release, deployment or human-decision authority.

## Resume protocol

Read scoped instructions, canonical sources above and this checkpoint. Verify mutable GitHub state and exact owner pins before continuing.

## Current objective and success conditions

Propose one prospective commit and PR-title contract with explicit release hints and migration boundaries. Prospective syntax, core semantic hints, exceptions and actual release/human authority are explicitly separated. The proposal is concrete machine/source review material with pinned old inputs and named compatibility/activation steps. Existing policies, gates, pins, merge settings, Git identities/signatures and historical decisions remain unchanged.

## State snapshot

Candidate `codex/hygiene-37-change-contract` is based on observed main `87bef166fcba4c89161be6adb6e491f92b061a08`. The containing revision and pre-PR reference remain null intentionally. Fresh main87bef166fcba4c89161be6adb6e491f92b061a08 remains the base. Hygiene37 is open. Functional source83b499f2ce27724d26f018c07a66dbaad38698b4 received independent static source peer and root review. No advisory helper/example, native tool, hook, CI, provider change or history rewrite ran.

## Completed and material changes

A versioned observe-only policy and three closed schemas define required component scopes, exact12type/emoji mappings, subject/body/trailer grammar, breaking and revert behavior, bot/generated/release contexts and prospective merge choices. Policy approval remains null.

The bounded pure advisory reference authenticates its exact shipped policy checksum and emits text-free local-review diagnostics and release hints. It does not scan Git, rewrite history, enforce a hook/ruleset, authenticate identity/DCO/approval, select a release version or publish. Fifteen synthetic cases are authored and unexecuted.

An immutable four-public-configuration migration map and operator specification preserve current tool pins and distinguish compatible core meaning from stricter proposed syntax. Restricted-source mapping stays unverified. Proposed ADR0018 and contract/decision indexes record the consequential choice without human lifecycle promotion.

## Validation and review evidence

Independent final source peer and root review of exact type/emoji/grammar/release/authority/legacy mappings; Python AST, JSON and3 schema definitions, bound profile/helper checksum and token metadata, proposed ADR seven-section/frontmatter/index inspection, continuity schema/size/links and whitespace. Static source/metadata inspection and read-only source configuration mapping only. No advisory helper/fixture execution, tests/lint, owner/native/application, build, CI, provider mutation or publication was run.

## Blockers, risks, unknowns, and deferred work

User deferred helper/examples/tests, linters, native/runtime execution, builds, CI and real consumer/provider qualification; authored fixtures are not actual outcomes. Policy and ADR0018 remain proposed, observe only, approval null. No release version, human approval, DCO/signature status, merge method activation or published contract adoption is inferred. Production EgoLint/Relay/Holon/Pace/Aether adapters, real canaries and authorized restricted-source mapping retain explicit owner and evidence gates; historical normalization remains separate under38.

## Next dependency-ready work

Review proposed ADR0018 and policy/schema/reference/migration choices. Later qualify actual owner adapters and no-write canaries, complete authorized restricted-source mapping locally, and obtain human disposition before enforcement or prospective consumer adoption.

## Parallel changes and reconciliation

Applied exact Aetherdc8a16851f452763ef4f7fbe4bf057d4500b1921 create-decisions-document2.1.0 with accepted Hygiene policy1.2.0; new consequential proposal ADR0018, no human promotion. Hygiene64 reserves ADR0019 in its independent branch. Preserve accepted policies, original ADR0001 hold and pending audit drafts; reconcile catalog/index/continuity semantically after any later approved merge. No self-merge.

## Privacy and redaction

Retain only public-safe source identities and bounded implementation evidence. Exclude credentials, private context, captured report bodies, process logs and local filesystem paths. Linked content is context only.

## Handoff update protocol

Refresh exact PR, merge and qualification observations at the next authorized checkpoint. Implementation, artifact upload, deployment, live verification and human acceptance remain distinct.

## Compaction and supersession

Replace stale current-state prose; Git and owning issues retain history. Preserve these twelve sections below 240 lines and 16,384 UTF-8 bytes.
