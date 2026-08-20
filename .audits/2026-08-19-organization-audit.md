# Ego Hygiene Organization Audit - 2026-08-19

## Executive summary

Ego Hygiene has crossed the threshold from a collection of experiments into an emerging developer platform and product ecosystem. The immediate risk is no longer lack of ideas; it is architectural state being held in maintainer memory while implementation, migration, and product work proceed in parallel.

The stabilization objective is therefore to externalize that state into durable repository contracts, roadmaps, and dependency-aware GitHub issues until any future work session can begin by selecting the next ready issue rather than reconstructing the organization mentally.

## Observed organization state

The live organization contains 25 repositories. The existing Hygiene ecosystem catalog already assigns target ownership and explicit non-ownership boundaries across architecture/control, developer/runtime, transformation/publishing, knowledge/research, and identity/product concerns.

Observed high-level state:

- Architecture exists and is substantially more mature than implementation in several control-plane repositories.
- Empathy historically incubated capabilities that now have dedicated repository owners.
- A large cross-repository issue portfolio already exists and should be reconciled rather than recreated.
- Observatory exists and has initial visibility/conformance issues.
- Pace exists and has initial fleet-lock and convergence issues.
- Relay, Realm, Egolint, Aether, Holon, Identity, Beacon, Mantle, Flow, and other specialist repositories already have bounded roadmap work.
- Public product work is beginning to become visible through Akashic, OptiFlow, Store, and egohygiene.io.

## Primary organizational problem

The organization has enough moving pieces that repository existence, ownership, readiness, and dependency state can no longer safely depend on human working memory.

The desired operating model is:

```text
intent
  -> Hygiene architecture and ownership
  -> repository v1 roadmap
  -> bounded GitHub issues
  -> implementation / Copilot execution
  -> Relay + Egolint validation
  -> Observatory evidence
  -> Pace convergence
  -> next dependency-ready issue
```

## Accepted architectural direction

### Hygiene

Owns organization architecture, repository catalog, policy vocabulary, cross-repository decisions, lifecycle/maturity semantics, and the contracts that describe what should exist. Hygiene does not implement specialist tooling owned elsewhere.

### .github

Owns organization-facing GitHub defaults, community health, public organization presentation, and fallback issue intake. Reusable CI/release implementation belongs in Relay.

### Empathy

Converges to the strict golden baseline/reference repository template. It should demonstrate integration of organization capabilities without remaining the permanent canonical source for specialist implementations.

### Holon

Owns deterministic template/blueprint resolution and materialization for new repositories or explicitly invoked regeneration. It must preserve user-owned content and expose plan/verify/rollback semantics.

### Pace

Owns later reconciliation and convergence of existing repositories toward versioned organization contracts. It should generate reviewable changes rather than silently mutate repositories.

### Observatory

Owns visibility: inventory, maturity, conformance evidence, dependency health, migration state, and trends. It consumes evidence and must not become the canonical policy source.

## Incubation boundary: Sanctuary

Sanctuary should be reintroduced as an intentionally permissive incubation workspace for experiments, imports, prototypes, and concepts that do not yet have durable ownership.

Rules:

1. Sanctuary is not a second Empathy.
2. Sanctuary is not a canonical organization baseline.
3. Incubated work must carry enough provenance to be evaluated later.
4. Graduation requires an ownership decision.
5. Graduated work moves to an existing holon when one owns the capability.
6. A new repository is created only when the capability has a durable independent boundary.
7. Sanctuary should expose an inventory so abandoned experiments remain understandable rather than becoming invisible debris.

Repository creation is intentionally outside this audit change and should be tracked as an explicit issue.

## Filament and Firmament

`filament` is remembered as a possible repository/concept but is not present in the observed 25-repository inventory. No repository should be created from the name alone. The stabilization campaign should recover its intended capability from prior architecture, notes, issues, or discussions and then decide whether it is:

- already owned by an existing repository;
- a Sanctuary incubation candidate;
- a genuinely missing durable holon; or
- an obsolete name/concept.

`firmament` is a separate, already documented deferred concept for infrastructure-as-code/cloud infrastructure. It should remain deferred until Realm's environment/runtime contracts are stable and the organization can demonstrate secrets, provenance, recovery, and deployment boundaries. Filament and Firmament must not be conflated because their names are similar.

## Stabilization definition of done

The organization planning/control-plane campaign is complete when:

- every active capability has an explicit repository owner or incubation state;
- every repository has a clear purpose and explicit non-ownership boundary;
- every repository has current architecture documentation or an approved equivalent;
- every repository has a holistic v1 roadmap;
- every remaining roadmap unit is represented by a bounded GitHub issue with acceptance criteria;
- cross-repository dependencies are visible;
- stale, duplicated, superseded, and completed issues are reconciled;
- every repository has a release/readiness definition appropriate to its class;
- audits are reproducible and stored under `.audits/` without making generated PDFs the sole source of truth;
- Observatory can report organization state from canonical evidence;
- a maintainer can resume work by selecting a dependency-ready issue without reconstructing the ecosystem from memory.

## Repository audit contract

Each repository stabilization pass must inspect the live repository and existing issue/PR history before proposing work.

Every audit should capture:

### Identity and boundary

- purpose;
- owned capabilities;
- explicit non-goals;
- lifecycle and maturity;
- repository class;
- intended users/consumers.

### Current state

- implemented capabilities;
- architecture/docs state;
- tests and validation;
- CI/release state;
- packaging/distribution state;
- website/docs state where applicable;
- known migrations or staged source;
- existing open issues and PRs.

### Interfaces

- inputs;
- outputs;
- public CLI/library/schema/API contracts;
- upstream producers;
- downstream consumers;
- compatibility/versioning expectations.

### V1 destination

- minimum complete product/platform outcome;
- quality gates;
- security and provenance expectations;
- supported platforms;
- documentation requirements;
- release and rollback expectations;
- observability/conformance evidence.

### Issue reconciliation

Every existing issue should be classified as one of:

- active and correctly scoped;
- delivered;
- superseded;
- duplicate;
- rerouted to another owner;
- blocked by dependency;
- deferred beyond v1.

New issues should be created only for uncovered roadmap units.

### Deliverables

Each stabilized repository should end with:

- `.audits/<date>-<repo>-audit.md` as canonical audit source;
- reproducible PDF generation/output path when useful for review;
- current architecture documentation;
- canonical roadmap document;
- dependency-ordered GitHub issues;
- explicit v1 definition of done.

Existing canonical locations may be retained when moving a document would create duplicate sources of truth.

## Dependency-aware campaign

### Checkpoint 0 - organization

- Hygiene organization audit and roadmap.
- `.github` governance/intake reconciliation.
- Repository catalog reconciliation.
- Sanctuary decision and creation issue.
- Filament recovery/ownership investigation.
- Firmament deferred-boundary confirmation.

### Checkpoint 1 - foundation triangle

1. Hygiene - what should exist.
2. Empathy - what the strict healthy baseline looks like.
3. Holon - how that baseline and profiles are materialized.

### Checkpoint 2 - developer platform

- Aether.
- Realm.
- Mantle.
- Egolint.
- Relay.

### Checkpoint 3 - fleet and platform operation

- Pace.
- Observatory.
- Identity.
- Mindgarden.
- Beacon.

### Checkpoint 4 - media and product infrastructure

- Flow.
- OptiFlow.
- Aniflow.
- Renderflow.
- Reflector.

### Checkpoint 5 - experiences and public products

- Akashic.
- Athena.
- Mindcap.
- Store.
- egohygiene.io.

### Checkpoint 6 - large and special cases

- egohygiene private product.
- organization `.github` final reconciliation.
- Sanctuary.
- Filament or its resolved owner.
- Firmament only if its creation gates have become satisfied.
- any capability discovered by prior audits that lacks ownership.

Batch membership is directional, not rigid. Dependency evidence may move a repository earlier or later.

## Immediate risks

### Architectural drift

Existing documents may describe older ownership, especially Empathy as an incubator. The latest accepted strict-baseline decision should be propagated into Hygiene's catalog and related context after review.

### Duplicate planning

The organization already has a large issue portfolio. Blindly generating a new issue set would increase pressure rather than reduce it. Reconciliation is mandatory before issue creation.

### Premature repository creation

Names and ideas are not sufficient boundaries. Sanctuary is justified by a clear lifecycle role; Filament still requires capability recovery; Firmament remains intentionally gated.

### Control-plane implementation ahead of contracts

Pace and Observatory should consume versioned Hygiene/Holon/Egolint/Relay evidence rather than inventing parallel schemas.

### Visible-product starvation

Infrastructure work should eventually make visible products easier to ship. The campaign should therefore preserve product-facing checkpoints and avoid requiring every control-plane feature to reach theoretical completeness before product sites can launch.

## Success criterion

The organization succeeds at this phase when the architecture stops being something one person must continuously remember and becomes a navigable, versioned execution system encoded in repositories, roadmaps, issues, and evidence.
