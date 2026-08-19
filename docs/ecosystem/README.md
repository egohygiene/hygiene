# Ego Hygiene Ecosystem Architecture

Status: **accepted v0.1**  
Architecture date: **2026-08-18**  
Scope: the 25 repositories currently visible in the `egohygiene` GitHub organization, plus one explicitly deferred infrastructure boundary.

This package defines the target repository architecture before any new infographic is produced. It reconciles the live repositories, the current Flow orchestration proposal, the contents staged in `empathy`, and the earlier ecosystem diagrams.

## Start here

1. Read [`ARCHITECTURE.md`](ARCHITECTURE.md) for the target system and ownership rules.
2. Use [`REPOSITORY_CATALOG.md`](REPOSITORY_CATALOG.md) for the role and current state of every repository.
3. Review [`SOURCE_REVIEW.md`](SOURCE_REVIEW.md) for what was inspected, retained, and superseded.
4. Follow [`MIGRATION_PLAN.md`](MIGRATION_PLAN.md) to extract staged work without losing provenance.
5. Give [`AGENT_CONTEXT.md`](AGENT_CONTEXT.md) to every repository agent.
6. Use the canonical `catalog/repositories.yaml` introduced by [issue #2](https://github.com/egohygiene/hygiene/issues/2) as the machine-readable source for generated context and automation.
7. Review the equivalent Mermaid, PlantUML, and Excalidraw sources in [`diagrams/`](diagrams/README.md).

## Architectural decision

`hygiene` becomes the canonical ecosystem architecture and platform-control repository. Other repositories receive a small, generated local context document that states their own boundary and pins an architecture release. They do **not** receive independent copies of the entire ecosystem specification. `pace` will eventually reconcile those projections through pull requests.

This prevents 25 copies of the architecture from drifting while still giving every human and agent enough local context to work safely.

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

The acceptance record is
[`ADR-0001`](../decisions/ADR-0001-holistic-architecture-v0.1.md). The intended
first release tag is `architecture-v0.1.0`.
