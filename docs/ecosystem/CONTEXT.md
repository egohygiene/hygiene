<!-- egohygiene-context: repository-context/v1 -->
---
schema-version: "1.0.0"
context-version: "1.0.0"
architecture-release: "architecture-v0.1.0"
repository: "egohygiene/hygiene"
source-repository: "egohygiene/hygiene"
source-revision: "f8303f1522e220bbc9b41191c635b0f236b1bf00"
generated-by: "egohygiene/hygiene:repository-context@1.0.0"
---

# Ecosystem context for `egohygiene/hygiene`

> Generated from the pinned Hygiene catalog. Do not edit this projection by hand.

## Identity

- Plane: `architecture-control`
- Visibility: `public`
- Lifecycle: `seed`
- Maturity: `seed`

## Ownership

### Owns

- ecosystem architecture
- repository registry
- platform policy
- cross-repository ADRs
- maturity model
- migration ledger

### Does not own

- tool implementations
- reusable workflows
- product domain logic

### Publishes

- architecture releases
- repository context projections
- policy schemas

## Dependencies

### Repository inputs

- None declared.

### Consumed contracts and artifacts

- None declared.

## Neighbors

### Upstream

- None declared.

### Downstream

- egohygiene/filament
- egohygiene/holon
- egohygiene/observatory
- egohygiene/pace

## Constraints

- Integrate sibling capabilities through released, immutable artifacts instead of copied source.
- Preserve repository-owned content and generated-file provenance.
- Do not place credentials, private identity data, or secret material in repository projections.
- Treat this context as a generated projection; change ecosystem ownership in Hygiene instead.
- Do not absorb or claim ownership of tool implementations.
- Do not absorb or claim ownership of reusable workflows.
- Do not absorb or claim ownership of product domain logic.

## Canonical links

- [Agent Context](https://github.com/egohygiene/hygiene/blob/f8303f1522e220bbc9b41191c635b0f236b1bf00/docs/ecosystem/AGENT_CONTEXT.md)
- [Architecture](https://github.com/egohygiene/hygiene/blob/f8303f1522e220bbc9b41191c635b0f236b1bf00/docs/ecosystem/ARCHITECTURE.md)
- [Catalog](https://github.com/egohygiene/hygiene/blob/f8303f1522e220bbc9b41191c635b0f236b1bf00/catalog/repositories.yaml)
- [Decisions](https://github.com/egohygiene/hygiene/blob/f8303f1522e220bbc9b41191c635b0f236b1bf00/docs/decisions/README.md)
- [Migration](https://github.com/egohygiene/hygiene/blob/f8303f1522e220bbc9b41191c635b0f236b1bf00/docs/ecosystem/MIGRATION_PLAN.md)
- [Repository](https://github.com/egohygiene/hygiene)

## Upgrade and stale-context behavior

- Compare `architecture_release` with the selected Hygiene release.
- On mismatch: `fail`.
- Upgrade owner: `egohygiene/pace`.
- Action: Regenerate from the pinned Hygiene release and review the resulting pull request.
