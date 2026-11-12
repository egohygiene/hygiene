# Ego Hygiene Ecosystem Architecture

This package describes the current repository architecture. The
[authority map](ARCHITECTURE.md#authority-and-evidence) identifies the
historical v0.1 baseline, proposed amendments and observed owner implementations.
Use the [reviewed public inventory](PUBLIC_REPOSITORY_INVENTORY.md) for
catalog scope and freshness.

## Start here

1. Read [`ARCHITECTURE.md`](ARCHITECTURE.md) for the target system and ownership rules.
2. Use the [machine-readable catalog](../../catalog/repositories.yaml) for
   current identities and [`REPOSITORY_CATALOG.md`](REPOSITORY_CATALOG.md) for
   the historical role and first-gate snapshot.
3. Review [`SOURCE_REVIEW.md`](SOURCE_REVIEW.md) for what was inspected, retained, and superseded.
4. Follow [`MIGRATION_PLAN.md`](MIGRATION_PLAN.md) to extract staged work without losing provenance.
5. Give [`AGENT_CONTEXT.md`](AGENT_CONTEXT.md) to every repository agent.
6. Use the canonical `catalog/repositories.yaml` introduced by [issue #2](https://github.com/egohygiene/hygiene/issues/2) as the machine-readable source for generated context and automation.
7. Use [`DEPENDENCY_BOUNDARIES.md`](DEPENDENCY_BOUNDARIES.md) and
   `catalog/dependency-boundaries.yaml` for cross-repository integration
   direction, interface requirements, and exceptions.
8. Review [`REPOSITORY_INTELLIGENCE.md`](REPOSITORY_INTELLIGENCE.md) for the
   proposed graph, event, provenance, linkage, privacy, and compatibility
   contract used by repository intelligence projections.
9. Review [`REPOSITORY_PRESENTATION.md`](REPOSITORY_PRESENTATION.md) for the
   proposed README slots, applicability, evidence-badge states, generated
   boundaries, and rollout ownership.
10. Review [`REPOSITORY_RELEASE.md`](REPOSITORY_RELEASE.md) for the proposed
    release-convention baseline, immutable Aether pin, migration states, and
    repository-owned release boundary.
11. Review [`REPOSITORY_CONTINUITY.md`](REPOSITORY_CONTINUITY.md) for the
    proposed root checkpoint requirement, immutable Aether pin, source
    precedence, privacy, staged rollout, exceptions, and v2 migration.
12. Review [`AGENT_READY_WEB.md`](AGENT_READY_WEB.md) for the proposed
    human-first and machine-readable web profile, discovery and efficient-
    representation catalog, guarded capability publication, descriptive
    commerce and advertising policy, deterministic conformance evidence,
    cross-layer authority denials, compatibility, and ownership boundaries.
13. Review [`PUBLIC_SITE_SURFACES.md`](PUBLIC_SITE_SURFACES.md) for the proposed
    public-site surface identities, scope-specific routes, applicability,
    delivery states, ownership, composition, and downstream handoffs.
14. Review the equivalent Mermaid, PlantUML, and Excalidraw sources in [`diagrams/`](diagrams/README.md).

## Architectural decision

`hygiene` becomes the canonical ecosystem architecture and platform-control repository. Other repositories receive a small, generated local context document that states their own boundary and pins an architecture release. They do **not** receive independent copies of the entire ecosystem specification. `pace` will eventually reconcile those projections through pull requests.

Generated context keeps repository-local guidance tied to its selected source.

## What this package does not do

- It does not mutate or rename any GitHub repository.
- It does not move files out of `empathy/.staging`.
- It does not declare old diagrams authoritative.
- It intentionally defers the polished infographic until this written model is accepted.

## Canonical home

This package is canonical under `egohygiene/hygiene/docs/ecosystem/`. The
machine-readable repository registry is promoted separately at the repository
root by issue #2 so that its schema, validator, fixtures, and generated views
can be reviewed as one contract.

[`ADR-0001`](../decisions/ADR-0001-holistic-architecture-v0.1.md) records the
historical five-plane baseline. The current six-plane view includes the
proposed amendments listed in the [authority map](ARCHITECTURE.md#authority-and-evidence).
