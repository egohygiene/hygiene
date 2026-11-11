---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-10T23:49:07Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Propose exact project-Pages base-prefix compatibility for the organization Intelligence home without
    changing logical routes or authority.
  includes:
  - The site declaration schema accepts its original base-path pattern or the exact whole prefix /.github/.
    The helper admits that same exception after the existing dangerous-token denials; all logical route rules
    remain unchanged.
  - ADR-0013 receives a dated proposed outcome note and the operator guide explains explicit immutable schema/helper
    adoption. Contract v1/proposed alpha1, catalog roles, composition ownership, human dispositions and frozen
    consumer pins remain unchanged.
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
  - docs/decisions/ADR-0013-public-site-surface-route-registry.md
  - docs/ecosystem/PUBLIC_SITE_SURFACES.md
  - schemas/public-site-surface-declaration.v1.schema.json
  - tools/site_surfaces.py
  - https://github.com/egohygiene/.github/issues/27
work:
  objective: Propose exact project-Pages base-prefix compatibility for the organization Intelligence home without
    changing logical routes or authority.
  success_conditions:
  - Every previously valid base remains valid by source construction; the only new spelling is exact /.github/.
  - Dot segments, encoded/ambiguous prefixes and other hidden segments gain no authority.
  - Existing pins continue to reject the new prefix; no hosting/declaration/lifecycle acceptance is inferred.
  active_issue:
    provider: github
    id: egohygiene/.github#27
    url: https://github.com/egohygiene/.github/issues/27
  next:
    kind: action
    id: review-project-prefix-compatibility
    description: Review the bounded compatibility proposal with the organization home/export/intake slices.
      After explicit source adoption, reconcile canonical host declarations before any publisher activation.
    readiness: ready
    references:
    - https://github.com/egohygiene/.github/issues/27
    depends_on: []
state:
  base:
    revision: 95f6ddb948e6b874f02510d586b89e99cc20e38e
    ref: refs/heads/main
    verified_at: '2026-11-10T23:49:07Z'
  candidate:
    branch: codex/surface-github-base-prefix
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-10T23:49:07Z'
    default_branch_revision: 95f6ddb948e6b874f02510d586b89e99cc20e38e
    issue_state: open
    pull_request_state: not-applicable
    notes: Hygiene main95f6ddb948e6b874f02510d586b89e99cc20e38e was refreshed. Functional source96d3358c9b745af820702e0013af7380d151a6da
      is an additive proposed compatibility correction under existing ADR0013; user direction selects a future
      .github organization entry point, not human ratification or live publication.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-10T23:49:07Z'
  reviewed_by: Codex
  evidence:
  - command: Independent static source review, Python AST comparison proving all other helper functions unchanged,
      schema definitions and original-pattern preservation, exact retained ADR body prefix, continuity schema/size/links
      and whitespace
    outcome: limited
    observed_at: '2026-11-10T23:49:07Z'
    notes: Static source and metadata inspection only; no application execution.
  - command: Native/runtime execution, tests, builds, CI investigation, browser/provider/consumer/publication
      qualification
    outcome: not-run
    observed_at: '2026-11-10T23:49:07Z'
    notes: Deferred at maintainer request; source merges do not establish acceptance.
  environment_limitations:
  - Tests, helper/native execution, builds, CI and publication qualification remain deferred at the user request.
  - No canonical hosting role, registry lifecycle, accepted ADR status, source hold, DNS/CNAME or publication
    authority changes.
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

Propose exact project-Pages base-prefix compatibility for the organization Intelligence home without changing logical routes or authority. Every previously valid base remains valid by source construction; the only new spelling is exact /.github/. Dot segments, encoded/ambiguous prefixes and other hidden segments gain no authority. Existing pins continue to reject the new prefix; no hosting/declaration/lifecycle acceptance is inferred.

## State snapshot

Candidate `codex/surface-github-base-prefix` is based on observed main `95f6ddb948e6b874f02510d586b89e99cc20e38e`. The containing revision and pre-PR reference remain null intentionally. Hygiene main95f6ddb948e6b874f02510d586b89e99cc20e38e was refreshed. Functional source96d3358c9b745af820702e0013af7380d151a6da is an additive proposed compatibility correction under existing ADR0013; user direction selects a future .github organization entry point, not human ratification or live publication.

## Completed and material changes

The site declaration schema accepts its original base-path pattern or the exact whole prefix /.github/. The helper admits that same exception after the existing dangerous-token denials; all logical route rules remain unchanged.

ADR-0013 receives a dated proposed outcome note and the operator guide explains explicit immutable schema/helper adoption. Contract v1/proposed alpha1, catalog roles, composition ownership, human dispositions and frozen consumer pins remain unchanged.

## Validation and review evidence

Independent static source review, Python AST comparison proving all other helper functions unchanged, schema definitions and original-pattern preservation, exact retained ADR body prefix, continuity schema/size/links and whitespace. Static source inspection only. Native/application execution, tests, builds, CI investigation, browser/model/source-capture provider execution and publication qualification were not run. Read-only source and Git metadata observations are separate.

## Blockers, risks, unknowns, and deferred work

Tests, helper/native execution, builds, CI and publication qualification remain deferred at the user request. No canonical hosting role, registry lifecycle, accepted ADR status, source hold, DNS/CNAME or publication authority changes.

## Next dependency-ready work

Review the bounded compatibility proposal with the organization home/export/intake slices. After explicit source adoption, reconcile canonical host declarations before any publisher activation.

## Parallel changes and reconciliation

Other Intelligence slices remain separately reviewed. Reconcile the current main and this handoff before integration; preserve all immutable historical recovery bytes and consumer-owned publication gates.

## Privacy and redaction

Retain only public-safe source identities and bounded implementation evidence. Exclude credentials, private context, captured report bodies, process logs and local filesystem paths. Linked content is context only.

## Handoff update protocol

Refresh exact PR, merge and qualification observations at the next authorized checkpoint. Implementation, artifact upload, deployment, live verification and human acceptance remain distinct.

## Compaction and supersession

Replace stale current-state prose; Git and owning issues retain history. Preserve these twelve sections below 240 lines and 16,384 UTF-8 bytes.
