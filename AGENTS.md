# Repository agent context

Before architecture-changing work in this repository:

1. Read [`docs/ecosystem/ARCHITECTURE.md`](docs/ecosystem/ARCHITECTURE.md).
2. Read [`docs/ecosystem/AGENT_CONTEXT.md`](docs/ecosystem/AGENT_CONTEXT.md).
3. Read the relevant accepted record under [`docs/decisions/`](docs/decisions/).
4. For cross-repository integration, read
   [`docs/ecosystem/DEPENDENCY_BOUNDARIES.md`](docs/ecosystem/DEPENDENCY_BOUNDARIES.md)
   and validate `catalog/dependency-boundaries.yaml`.
5. Update the canonical architecture or catalog before, or in the same reviewed
   change as, any cross-repository ownership change.

Hygiene defines ecosystem architecture and policy. It does not absorb the
implementations owned by Aether, Holon, Pace, Observatory, Realm, Mantle,
Relay, Egolint, Flow, or product repositories.

Generated repository-local context and diagrams are projections. Do not edit a
projection to silently redefine canonical ownership.

## Repository release baseline

Before changing versioning, changelog, tag, workflow, or publication behavior,
read [the repository release baseline](docs/ecosystem/REPOSITORY_RELEASE.md)
and [the local declaration](.egohygiene/release.json). The policy composes the
immutable Aether contract; do not copy or weaken that protocol here.

Use `release:plan`, `release:prepare`, and `release:verify` for a reviewable
candidate. `release:publish` is a manual handoff only. It does not authorize a
tag, release, deployment, registry operation, credential use, or immutable
artifact overwrite without a separate user-approved publication action.
