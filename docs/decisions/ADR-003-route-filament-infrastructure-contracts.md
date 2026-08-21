---
schema: egohygiene.architecture-decision/v1
id: ADR-003
title: Route reusable infrastructure contracts to Filament
status: proposed
date: 2026-08-21
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/.github/issues/13
pull_request: null
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/.github
  - egohygiene/filament
  - egohygiene/hygiene
affected_contracts:
  - egohygiene.repository-context/v1
  - egohygiene.dependency-boundary-register/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/.github/issues/13
    description: Organization intake requiring evidence recovery, owner comparison, and exactly one routing decision.
  - type: pull_request
    url: https://github.com/egohygiene/filament/pull/1
    description: Merged initialization that records the clarified reusable infrastructure-as-code boundary.
  - type: documentation
    url: https://github.com/egohygiene/filament/blob/main/ARCHITECTURE.md
    description: Filament-owned boundary, relationships, consumer responsibilities, and Firmament reconciliation note.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/9
    description: Earlier stabilization audit that kept Filament unresolved and Firmament separately deferred.
exceptions: []
approval: null
---

# ADR-003: Route reusable infrastructure contracts to Filament

## Context

The organization intake in `egohygiene/.github#13` remembered a `filament`
concept but predated the live Filament repository. The intake required explicit
reference recovery, comparison with every plausible owner, a distinction from
the similarly named deferred Firmament boundary, and exactly one outcome.

The evidence now establishes that `egohygiene/filament` exists and its merged
architecture assigns it reusable infrastructure-as-code modules, stack
contracts, schemas, provider and engine adapters, examples, tests, validation,
and versioned releases. This matches the recovered maintainer intent. Consumers
retain why and where infrastructure is deployed, along with credentials,
budgets, approvals, environment-specific topology, and production state.

Hygiene's accepted v0.1 architecture predates this clarification. It lists 25
current repositories, treats Filament as unresolved in the stabilization
roadmap, and preserves Firmament as a deferred future infrastructure boundary.
The catalog therefore needs reconciliation with observed organization state.

## Decision

Recommend **Route**: route reusable infrastructure-as-code implementation
contracts to the existing `egohygiene/filament` repository. Do not create
another repository and do not incubate a duplicate in Sanctuary.

Filament owns reusable modules, stack contracts, metadata and schemas, provider
and engine adapters, test fixtures, examples, validation semantics, and their
versioned release evidence. It is represented in the infrastructure and
deployment plane and publishes immutable or versioned contracts to consumers.

Firmament remains independently deferred. If a later organization-operated
infrastructure boundary is needed, Firmament may be reconsidered for deployed
compositions, shared networking or clusters, deployment environments, and
operational state. It must consume rather than duplicate Filament contracts,
and its creation still requires stable Realm and Filament artifacts plus a
separate approved decision.

This proposed record grants no authority to provision infrastructure, create
Firmament, select a universal IaC engine, hold credentials centrally, or move
consumer-owned production state into Filament.

## Alternatives considered and rejected

### Route to Realm

Rejected. Realm owns developer environments, images, Dev Containers, Nix, and
workstation projections. It may provide IaC tooling but does not own reusable
cloud or resource definitions.

### Route to Relay

Rejected. Relay owns reusable CI, release, and publication mechanics. It may
execute Filament validation, plan, test, and release commands but does not own
their IaC semantics.

### Route to Holon

Rejected. Holon materializes repositories and organizations from blueprints;
it does not own ongoing infrastructure modules or deployed state.

### Route to product repositories

Rejected as the canonical answer. Consumers keep deployment intent and state,
but independently copying reusable module implementations would violate the
accepted dependency boundary.

### Incubate in Sanctuary

Rejected. The concept has a live repository, a coherent architecture, explicit
non-ownership, and a bounded v1 path. Sanctuary would create a duplicate source
of truth rather than reduce uncertainty.

### Merge Filament into Firmament or create another repository

Rejected. Naming similarity is not an ownership contract. Filament is already
the reusable definition layer; Firmament remains a deferred possible operated
deployment boundary. No additional repository is needed.

### Retire or leave unresolved

Rejected. The merged Filament architecture and maintainer clarification provide
sufficient evidence for a distinct, reusable capability.

## Consequences and tradeoffs

- The live repository catalog grows from 25 to 26 repositories and gains an
  infrastructure and deployment plane.
- Filament must prove one narrow vertical slice before broad provider or engine
  expansion.
- Consumers gain reusable, pinned infrastructure contracts while retaining
  sensitive deployment authority and state.
- Relay and Realm can support Filament without absorbing its semantics.
- Firmament becomes easier to evaluate later, but its remaining operational
  boundary is intentionally unimplemented and may ultimately be retired.

## Implementation and evidence links

This change updates the Hygiene catalog, narrative architecture, roadmap,
dependency-boundary register, generated views, and diagram sources. Filament's
repository architecture remains the implementation-level source for its local
boundary. No infrastructure resources, credentials, provider selection, or
production state are introduced.

## Replacement or exit strategy

If real consumers show that reusable IaC does not sustain an independent
release boundary, a later accepted ADR may route individual contracts to their
durable owners and deprecate Filament. That migration must preserve versioned
consumer compatibility and state ownership; it must not copy source silently.

## Follow-up work

- Open a bounded Filament implementation issue for the first independently
  testable module or stack contract after this routing decision is approved.
- Require any future Firmament proposal to demonstrate a non-overlapping
  operated-infrastructure need and explicit secret, state, cost, rollback, and
  lifecycle boundaries.
- Project the updated catalog through Pace only after the architecture change
  is accepted and released.
