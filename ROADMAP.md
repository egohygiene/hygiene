---
schema: aether.architecture-document/v1
id: hygiene-roadmap
title: Hygiene Roadmap
kind: architecture-document
version: 0.2.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
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
- Empathy's strict-baseline role is reflected in organization architecture.
- Sanctuary is defined as an incubation boundary without becoming canonical.
- Filament is investigated before repository creation.
- Firmament remains explicitly deferred until its gates pass.

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

**Scope:** the private egohygiene product, final `.github` reconciliation, Sanctuary, Filament or its resolved owner, Firmament only if its gates pass, and any ownerless capability discovered by earlier audits.

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
