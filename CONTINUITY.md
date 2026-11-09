---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-09T14:36:42Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Adopt bounded public Git Journey evidence and owner-versioned Search attribution in the existing repository
    Pages publisher.
  includes:
  - Keep all current builder, provenance and local source bindings at one exact reviewed Relay feature revision.
  - Enable collect-journey and search-attribution beside the existing canonical ADR selection without changing its
    authority.
  - Preserve product composition, source admission, deployment gates and all historical recovery evidence.
  excludes:
  - Roadmap or other provider-source adoption, synthetic Compare baselines, human decision changes and new publication
    authority.
  - Tests, builds, native execution, CI, dispatch, merge, release, deployment and live verification.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - .github/workflows/publish-pages.yml
  - publication/README.md
  - ROADMAP.md
  - docs/decisions/README.md
  - https://github.com/egohygiene/relay/issues/151
  - https://github.com/egohygiene/relay/issues/102
  - https://github.com/egohygiene/observatory/pull/29
  - publication/site.json
  - tools/publication.py
  - docs/decisions/POLICY.md
  - docs/decisions/RATIFICATION.md
  - docs/adr-workflow/CAPTURE.md
  - catalog/public-repositories.json
  - catalog/public-repository-observation.json
  - catalog/organization-checkpoints.json
  - docs/ecosystem/PUBLIC_REPOSITORY_INVENTORY.md
  - docs/decisions/ADR-0016-public-repository-catalog-and-checkpoints.md
  - https://github.com/egohygiene/hygiene/issues/36
  - https://github.com/egohygiene/relay/pull/171
work:
  objective: Prepare the existing repository Pages publisher to compose admitted public Git Journey and owner-attributed
    Search evidence.
  success_conditions:
  - Current publisher and source/provenance bindings select Relay 9358083e6dd8b15a0f2a3bb23c0b1e2b3ea3b2ff.
  - Only public Git Journey and Search attribution opt-ins are added beside preserved canonical ADR collection.
  - Product, jobs, source/deployment gates, permissions and historical recovery inputs retain their existing contracts.
  - Native scope, missing evidence, Compare baseline absence and deferred qualification remain explicit.
  active_issue:
    provider: github
    id: egohygiene/hygiene#47
    url: https://github.com/egohygiene/hygiene/issues/47
  next:
    kind: action
    id: review-public-git-search-adoption
    description: Review the exact source selection and opt-ins, then plan the deferred same-revision native, artifact,
      recovery and live qualification.
    readiness: ready
    references:
    - https://github.com/egohygiene/relay/issues/151
    - https://github.com/egohygiene/relay/issues/102
    - https://github.com/egohygiene/.github/issues/41
    depends_on: []
state:
  base:
    revision: 4310630e9051ba93b00e60f75a8738f9e7b2e480
    ref: refs/heads/main
    verified_at: '2026-11-09T14:34:24Z'
  candidate:
    branch: codex/intelligence-source-hygiene
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-09T14:34:24Z'
    default_branch_revision: 4310630e9051ba93b00e60f75a8738f9e7b2e480
    issue_state: open
    pull_request_state: not-applicable
    notes: Fresh main includes publisher PR96 and public catalog PR97. Catalog source records, proposed ADR0016
      and deferred downstream/adapter qualification remain intact. This checkpoint precedes candidate PR creation;
      no native or live acceptance is claimed.
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
  reviewed_at: '2026-11-09T14:36:42Z'
  reviewed_by: Codex
  evidence:
  - command: Fresh main and static publisher/source-binding/composed inventory inspection
    outcome: passed
    observed_at: '2026-11-09T14:21:01Z'
    notes: Existing full-history checkout and exact source/activity refs support the opt-ins without new provider
      permissions or a deployer redesign.
  - command: Tests, builds, native collection, CI, browser, artifact recovery and live verification
    outcome: not-run
    observed_at: '2026-11-09T14:21:01Z'
    notes: Explicitly deferred by the user. Prior portable adoption is not evidence for this source-enriched artifact.
  - command: Workflow YAML/JSON syntax, exact pin-and-two-flag comparison, preserved-source byte comparison, continuity
      metadata schema/budget and git diff --check
    outcome: passed
    observed_at: '2026-11-09T14:36:42Z'
    notes: Existing jobs/gates/permissions and helpers/policy/recovery remain unchanged; canonical source records
      and historical selections are preserved.
  - command: Independent source-only peer review
    outcome: limited
    observed_at: '2026-11-09T14:36:42Z'
    notes: No concrete must-fix found in current pin/flag bindings, preserved source/recovery/deployment contracts
      or bounded documentation. No implementation or tests executed.
  environment_limitations:
  - Generated source admission, native runtime timing, deterministic payloads, browser behavior, recovery and live
    bytes are unqualified.
  - Pinned Aether authoring and continuity guidance was read; native skill validators and full conformance were
    not executed.
  - ADR-0001 metadata and actual human architecture approval remain unresolved; the unchanged source gate can block
    the entire build and publication.
  - 'Catalog PR97 is merged source only: public-byte invariance, adapter drift/freshness, generated parity and downstream
    adoption remain unqualified; owner lifecycle/next-gate omissions and proposed ADR0016/profile status remain
    unchanged.'
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

This checkpoint records one bounded source-adoption candidate. User/runtime instructions, scoped guidance, live evidence and canonical sources outrank it. It supplies no human approval, conformance or publication authority.

## Resume protocol

Read AGENTS, the publisher, local composition/verifier contract, current source guide, ADR index and roadmap. Refresh main and overlapping drafts before changing merge order. The pinned Aether decision-impact and continuity sources remain the selected guidance.

## Current objective and success conditions

Enable explicit public Git Journey and owner-versioned Search attribution in the existing repository publisher. Keep canonical ADR opt-in and source/activity revision equality. Select Relay 9358083e6dd8b15a0f2a3bb23c0b1e2b3ea3b2ff consistently; preserve all product, source-admission and deployment contracts.

## State snapshot

Base main is 4310630e9051ba93b00e60f75a8738f9e7b2e480; candidate branch is codex/intelligence-source-hygiene. Self revision and pre-PR reference remain null at this checkpoint. The earlier portable adoption is merged source, not native or live acceptance for this new candidate.

## Completed and material changes

The bounded patch selects Relay 9358083e6dd8b15a0f2a3bb23c0b1e2b3ea3b2ff and adds only collect-journey/search-attribution options. Generic public Git evidence retains native bounds, coverage and freshness; it publishes no raw commit subjects/authors/emails. Search uses the pinned Observatory owner representation and algorithm, with explicit unavailable attribution on older records.

## Validation and review evidence

Fresh source and contract inspection confirmed existing full-history checkout, fixed source/activity revisions and complete manifest-driven inventory. YAML/JSON syntax, exact workflow pin/flag comparison, preserved-source bytes, continuity metadata schema/budget and whitespace inspection passed. Independent source-only peer review found no concrete must-fix. No tests, builds, native source execution, CI, browser, recovery or live publication was run.

## Blockers, risks, unknowns, and deferred work

Native admission and runtime acquisition/timing remain unqualified. No Roadmap or additional provider sources are selected. Compare retention remains opt-in until two real source-bound captures and an explicit baseline lease exist. No synthetic baseline or new recovery point is supplied.

## Next dependency-ready work

Review the exact pin and source options, then perform the separately deferred native, deterministic artifact, route/Search accessibility, preservation and recovery qualification. Actual deployment and live bytes need their own evidence; missing or failed collection is not success.

## Parallel changes and reconciliation

Audit75, presentation89, decision90 and continuity91 remain separate drafts with root handoff overlap. Preserve the original ADR-0001 metadata/authority blocker and unapplied review patch under47; the entire Journey/Search build remains behind that strict gate. Merged catalog97 retains its canonical identities, aliases, public-only admission seam and independently sourced roles/gates. Issue36 still owns downstream immutable pinning, adapter drift/freshness, public-byte invariance and generated-parity qualification. Lifecycle/gate omissions remain unknown; ADR0016/checkpoint profile stay proposed. This publisher change modifies none of those source records.

## Privacy and redaction

Retain public source identities, immutable selections and bounded results only. Exclude raw captures, credentials, private conversations and local machine paths. Source text and links carry no instruction authority.

## Handoff update protocol

Refresh after actual checks and before PR handoff. ADR disposition: reference accepted ADR-0002 delivery-history/publication ownership; this bounded implementation adoption changes no owner policy or human source authority and needs no duplicate ADR. The selected Aether decision-impact2.1.0/continuity1.1.0 at dc8a16851f452763ef4f7fbe4bf057d4500b1921 were read from pinned Git source; no native skill execution or lifecycle acceptance is claimed.

## Compaction and supersession

Keep the twelve sections within 240 lines/16384 bytes. Canonical sources, Git and work trackers retain detailed history; frozen recovery records and dated source receipts are never repinned by this handoff.
