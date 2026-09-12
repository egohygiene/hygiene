---
schema: aether.architecture-document/v1
id: hygiene-roadmap
title: Hygiene Roadmap
kind: architecture-document
version: 0.5.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-09-12
governed_by:
  - architecture-roadmap
depends_on:
  - hygiene-vision
  - hygiene-pillars
  - hygiene-architecture
  - hygiene-decisions
related:
  - hygiene-purpose
  - hygiene-principles
  - hygiene-manifesto
  - hygiene-epistemology
supersedes: []
---

# Hygiene Roadmap

<!-- BEGIN ROADMAP EXECUTION SNAPSHOT -->
<!-- roadmap-manifest
schema: hygiene.roadmap/v1alpha1
repository: egohygiene/hygiene
visibility: public
publication: central
route: /roadmap/hygiene/
updated: 2026-08-25
-->
## 2026-08-24 execution snapshot

> This evidence-reconciled snapshot is the issue-generation and visual-roadmap handoff. The longer-horizon strategy below remains canonical context; generated HTML, JSON, progress, issue plans, and commit lists are projections.

**Lifecycle:** seed, architecture-first control plane  
**Current gate:** Merge the ADR-002 activation change, then add CI against the accepted organization contracts.

**North-star outcome:** The canonical, machine-readable definition of the organization, its repositories, boundaries, and lifecycle contracts.

### Visual roadmap publication

**Mode:** `central`  
**Route:** `/roadmap/hygiene/`  
**Current publication evidence:** Machine-readable source catalog; no CI or Pages publication observed.

Publish the public-safe projection through egohygiene.io at /roadmap/hygiene/. This repository owns intent and acceptance evidence; it does not add a second site deployment.

### Quest line

<!-- roadmap-step
id: HYG-Q01
status: complete
depends_on: []
issues: []
-->
#### HYG-Q01 — Establish schemas and governance tools

**State:** `complete`
**Depends on:** None

**Outcome:** Initial schemas, tools, tests, and incubation boundaries exist.

**Exit criteria:**

- [x] Core schemas and tools are present with test coverage.
- [x] The Sanctuary registration boundary is represented.

**Current evidence:**

- The audit found 5 schemas, 3 tools, and 3 tests.
- PR #12 merged at 3452af8cd24b and PR #14 at 51edefe29f8e.

<!-- roadmap-step
id: HYG-Q02
status: complete
depends_on: [HYG-Q01]
issues: [15]
-->
#### HYG-Q02 — Ratify the organization ADR standard

**State:** `complete`
**Depends on:** `HYG-Q01`

**Outcome:** ADR-002, tracked by issue #15, defines what Hygiene owns and how repositories inherit its versioned ADR contract without copying policy.

**Exit criteria:**

- [x] ADR-002 is explicitly accepted with named human authority and durable evidence.
- [x] The front matter and repository policy-reference contracts are activated.
- [x] Conflicting local policy sources are deprecated or clearly marked non-canonical.

**Current evidence:**

- PR #10 merged the proposed foundation and PR #21 hardened its inheritance and extension contract.
- Aether PR #50 provides a pinned consumer without claiming policy authority.
- Maintainer `szmyty` explicitly approved ADR-002 and policy v1.1.0 at
  `f598ed659a43dd759d4ede41c27f9e5daf991aa7` in issue #15 on 2026-09-12.

<!-- roadmap-step
id: HYG-Q03
status: ready
depends_on: [HYG-Q02]
issues: []
-->
#### HYG-Q03 — Activate contract validation

**State:** `ready`
**Depends on:** `HYG-Q02`

**Outcome:** Every catalog and schema change is validated before merge.

**Exit criteria:**

- [ ] Schema, tool, and fixture tests run in CI.
- [ ] An invalid catalog fixture is rejected.

**Current evidence:**

- No CI workflow was observed.

<!-- roadmap-step
id: HYG-Q04
status: ready
depends_on: [HYG-Q02]
issues: []
-->
#### HYG-Q04 — Refresh the 28-repository catalog

**State:** `ready`  
**Depends on:** `HYG-Q02`

**Outcome:** The catalog accurately represents the live organization and publication names.

**Exit criteria:**

- [ ] All 28 audited repositories, including Civics, are represented.
- [ ] The website rename and lifecycle fields are reconciled.

**Current evidence:**

- The current catalog lists 27 repositories, omits Civics, and has a pending website rename.

<!-- roadmap-step
id: HYG-Q05
status: planned
depends_on: [HYG-Q03, HYG-Q04]
issues: [19, 22, 45]
-->
#### HYG-Q05 — Version and integrate the organization contract

**State:** `planned`  
**Depends on:** `HYG-Q03`, `HYG-Q04`

**Outcome:** Egolint validates, Observatory reads, Holon renders, and Pace rolls out one versioned contract.

**Exit criteria:**

- [ ] A tagged schema release is consumed by the four control-plane tools.
- [ ] Compatibility and migration rules are documented.

**Current evidence:**

- PR #20 merged the proposed Repository Intelligence schema, vocabulary,
  complete delivery-chain fixture, and reference validator. Cross-tool
  integration remains unproven.
- Issue #22 defines the proposed repository-presentation profile and evidence
  boundary before Identity, Holon, Egolint, and Pace implementations.
- Issue #45 defines the proposed repository-continuity applicability profile,
  breaking repository-context v2 transition, and observe-first downstream
  boundary. Stable Aether release evidence and ADR-008 acceptance remain gates
  before ratchet or enforcement.

<!-- roadmap-step
id: HYG-Q06
status: planned
depends_on: [HYG-Q05]
issues: []
-->
#### HYG-Q06 — Publish the roadmap contract

**State:** `planned`  
**Depends on:** `HYG-Q05`

**Outcome:** Hygiene publishes hygiene.roadmap/v1alpha1 as the canonical contract for stable quest IDs, states, dependencies, evidence, visibility, and supersession.

**Exit criteria:**

- [ ] The schema, compatibility rules, public/private policy, and fixtures are versioned and validated in CI.
- [ ] The contract explicitly keeps ROADMAP.md canonical and generated issue/site data derivative.

**Current evidence:**

- The contract is specified in the 2026-08-24 visual-roadmap design but is not yet released.

### Roadmap-to-issue handoff

- A step is complete only when its exit criteria and required evidence are satisfied; commit count never determines progress.
- Ready steps without an issue are candidates for the private, duplicate-aware roadmap.issue-plan.json dry run. Planned steps remain preview-only unless a reviewer explicitly opts them in with issue_policy: propose.
- Issue creation or reconciliation requires human approval or an explicitly authorized Pace operation and returns issue references through a reviewable roadmap pull request.
- Pull requests and commits should include Roadmap-Step: <ID>; historical evidence may be linked through existing issue and pull-request relationships.
- Public rendering uses only allowlisted build-time evidence and never places a GitHub token or private issue plan in the browser artifact.

<!-- END ROADMAP EXECUTION SNAPSHOT -->

## Strategic context

Hygiene is the organization control-plane source for architecture, ownership, lifecycle, repository catalog, policy vocabulary, and cross-repository decisions. This roadmap describes capability evolution rather than promised dates.

The immediate organization priority is stabilization: externalize architecture and v1 execution state so future work can be selected from a dependency-aware issue graph rather than reconstructed from maintainer memory.

The detailed current-state audit is maintained at `.audits/2026-08-19-organization-audit.md`.

## Operating loop

```text
Architecture -> Audit -> Roadmap -> Issues -> Implement -> Validate -> Observe -> Converge
```

Hygiene defines what should exist. Repository audits define current state and v1 destination. GitHub issues are the execution layer. Relay and Egolint provide reusable validation. Observatory reports evidence. Pace proposes reviewable fleet convergence.

## Phase 1: Accept and reconcile the holistic architecture

**Outcome:** Organization ownership, dependency direction, lifecycle state, and accepted/proposed boundaries are explicit and internally consistent.

**Exit signals:**

- The architecture corpus is accepted and internally linked.
- The live repository inventory is reconciled with the canonical catalog.
- Empathy's strict-baseline role is reflected in organization architecture and
  no longer includes general incubation.
- Sanctuary is registered as the bounded incubation owner while its local
  lifecycle schema remains provisional rather than organization-wide canonical.
- Filament is routed as the reusable infrastructure-as-code contract owner and
  reconciled with the live repository catalog.
- Firmament remains a separate, explicitly deferred deployment boundary until
  Realm and Filament artifact contracts are stable and a non-overlapping need
  is approved.

## Phase 2: Stabilize the repository catalog and audit contract

**Outcome:** Every repository can be audited through one repeatable contract and represented through versioned organization metadata.

**Exit signals:**

- The repository catalog has a versioned machine-readable schema.
- Repository purpose, non-ownership, lifecycle, dependencies, and maturity are validated.
- A reusable audit contract covers current state, interfaces, v1 destination, issue reconciliation, and definition of done.
- Audit sources live under `.audits/` or an approved existing canonical location.
- Generated PDF review artifacts are reproducible and never the only canonical source.

## Phase 3: Complete the foundation triangle

**Outcome:** Hygiene, Empathy, and Holon provide a coherent organization definition -> golden baseline -> materialization path.

**Exit signals:**

- Hygiene defines the canonical organization contracts.
- Empathy demonstrates the strict healthy baseline without owning specialist implementations.
- Holon can plan, render, verify, and roll back repository materialization.
- Existing issues across the three repositories are reconciled into dependency-ready v1 queues.

## Phase 4: Stabilize the developer platform

**Scope:** Aether, Realm, Mantle, Egolint, and Relay.

**Outcome:** Repositories consume versioned AI artifacts, environments, shell tooling, quality rules, and automation rather than copied sibling source.

**Exit signals:**

- Stable public contracts exist for the required v1 surfaces.
- At least one non-Empathy repository consumes released surfaces.
- Security, provenance, release, rollback, and compatibility behavior are explicit.

## Phase 5: Stabilize fleet and platform operation

**Scope:** Pace, Observatory, Identity, Mindgarden, and Beacon.

**Outcome:** Fleet drift, evidence, identity, knowledge, and publication can be represented through versioned contracts without generated surfaces becoming canonical state.

**Exit signals:**

- Observatory can report unknown/stale state rather than guessing.
- Pace can produce dry-run convergence plans and reviewable changes.
- Identity, Mindgarden, and Beacon publish independently consumable contracts.

## Phase 6: Stabilize media and product infrastructure

**Scope:** Flow, OptiFlow, Aniflow, Renderflow, and Reflector.

**Outcome:** Independent tools expose stable contracts and composed workflows prove orchestration without source duplication.

## Phase 7: Stabilize experiences and public products

**Scope:** Akashic, Athena, Mindcap, Store, and egohygiene.io.

**Outcome:** Public surfaces ship through shared platform capabilities while retaining independent product ownership and accessible standalone behavior.

## Phase 8: Resolve large and special cases

**Scope:** the private egohygiene product, final `.github` reconciliation,
Sanctuary's first real bounded incubation, Filament's first bounded
infrastructure contract, Firmament only if its gates pass, and any ownerless
capability discovered by earlier audits.

## Per-repository planning completion contract

A repository is planning-complete for this campaign when:

- its purpose and non-ownership boundary are current;
- its architecture is current;
- its audit records current state and v1 gaps;
- its v1 roadmap is dependency ordered;
- existing issues are reconciled;
- uncovered roadmap work has bounded issues with acceptance criteria;
- release, security, testing, documentation, and site requirements are explicit for its repository class;
- upstream/downstream contracts are versioned or explicitly provisional;
- its v1 definition of done is measurable;
- a future work session can select the next ready issue without reconstructing repository context.

## Prioritization rule

Within each phase:

1. resolve P0 correctness/security blockers;
2. resolve contracts required by multiple downstream repositories;
3. ship the smallest golden-path vertical slice;
4. establish release and evidence paths;
5. add fleet automation only after underlying contracts stabilize;
6. defer speculative breadth not required for v1.

## Drift rule

When architecture, audit, roadmap, issues, and implementation disagree:

1. record the discrepancy;
2. identify the current accepted decision;
3. update the canonical owner first;
4. reroute or supersede stale issues;
5. update projections and consumers afterward;
6. preserve historical decisions rather than silently rewriting why a change occurred.

## Cross-cutting tracks

- Security, privacy, accessibility, licensing, and provenance.
- Documentation, architecture portals, examples, and onboarding.
- Packaging, release, compatibility, and self-hosting.
- Organization integration through explicit contracts.
- Observatory evidence and Pace conformance.

## Deferred direction

Optional managed services, enterprise controls, marketplaces, and the conversational organization compiler remain later architecture work. Current choices should preserve portability and avoid foreclosing them.
