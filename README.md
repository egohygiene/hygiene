# hygiene

The canonical ecosystem architecture and platform-control repository for the
Ego Hygiene organization.

Hygiene owns the repository registry, cross-repository architecture decisions,
platform policy, adoption model, and migration context. It does not own the
implementations of every policy or product capability.

## Ecosystem architecture

- [Holistic architecture](docs/ecosystem/ARCHITECTURE.md)
- [Repository catalog](docs/ecosystem/REPOSITORY_CATALOG.md)
- [Migration plan](docs/ecosystem/MIGRATION_PLAN.md)
- [Agent context](docs/ecosystem/AGENT_CONTEXT.md)
- [Diagram sources](docs/ecosystem/diagrams/README.md)
- [Architecture acceptance decision](docs/decisions/ADR-0001-holistic-architecture-v0.1.md)

The accepted written architecture and versioned machine-readable catalog are
authoritative. Rendered diagrams, local repository context, and future
landscape sites are projections of those sources.

## Control-plane boundary

The public organization repository, `egohygiene/.github`, remains the
organization-facing inbox, profile, public defaults, and fallback coordination
surface. Hygiene is the canonical long-term home for ecosystem architecture,
the repository catalog, and cross-repository ADRs.

See [issue #1](https://github.com/egohygiene/hygiene/issues/1) for the initial
architecture import and [issue #2](https://github.com/egohygiene/hygiene/issues/2)
for the validated catalog contract.
