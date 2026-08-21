<!-- egohygiene-context: repository-context/v1 -->
---
schema-version: "1.0.0"
context-version: "1.0.0"
architecture-release: "architecture-v0.1.0"
repository: "egohygiene/sanctuary"
source-repository: "egohygiene/hygiene"
source-revision: "e44856439ebb9bf8df7a6b3afce473574f4fbfad"
generated-by: "egohygiene/hygiene:repository-context@1.0.0"
---

# Ecosystem context for `egohygiene/sanctuary`

> Generated from the pinned Hygiene catalog. Do not edit this projection by hand.

## Identity

- Plane: `architecture-control`
- Visibility: `public`
- Lifecycle: `incubating`
- Maturity: `provisional-contract`

## Ownership

### Owns

- bounded incubation of unfinished or ownerless public work
- incubation provenance and lifecycle evidence
- graduation, archival, and rejection proposals

### Does not own

- canonical repository templates
- organization-wide policy and canonical lifecycle semantics
- durable specialist implementations after ownership decisions
- stable repository dependencies
- credentials, private data, production state, and generic artifact archives

### Publishes

- provisional incubation manifests
- provenance and lifecycle records
- reviewed ownership-decision evidence

## Dependencies

### Repository inputs

- egohygiene/.github
- egohygiene/hygiene

### Consumed contracts and artifacts

- hygiene architecture release
- organization issue intake

## Neighbors

### Upstream

- egohygiene/.github
- egohygiene/hygiene

### Downstream

- None declared.

## Constraints

- Integrate sibling capabilities through released, immutable artifacts instead of copied source.
- Preserve repository-owned content and generated-file provenance.
- Do not place credentials, private identity data, or secret material in repository projections.
- Treat this context as a generated projection; change ecosystem ownership in Hygiene instead.
- Do not absorb or claim ownership of canonical repository templates.
- Do not absorb or claim ownership of organization-wide policy and canonical lifecycle semantics.
- Do not absorb or claim ownership of durable specialist implementations after ownership decisions.
- Do not absorb or claim ownership of stable repository dependencies.
- Do not absorb or claim ownership of credentials, private data, production state, and generic artifact archives.

## Canonical links

- [Agent Context](https://github.com/egohygiene/hygiene/blob/e44856439ebb9bf8df7a6b3afce473574f4fbfad/docs/ecosystem/AGENT_CONTEXT.md)
- [Architecture](https://github.com/egohygiene/hygiene/blob/e44856439ebb9bf8df7a6b3afce473574f4fbfad/docs/ecosystem/ARCHITECTURE.md)
- [Catalog](https://github.com/egohygiene/hygiene/blob/e44856439ebb9bf8df7a6b3afce473574f4fbfad/catalog/repositories.yaml)
- [Decisions](https://github.com/egohygiene/hygiene/blob/e44856439ebb9bf8df7a6b3afce473574f4fbfad/docs/decisions/README.md)
- [Migration](https://github.com/egohygiene/hygiene/blob/e44856439ebb9bf8df7a6b3afce473574f4fbfad/docs/ecosystem/MIGRATION_PLAN.md)
- [Repository](https://github.com/egohygiene/sanctuary)

## Upgrade and stale-context behavior

- Compare `architecture_release` with the selected Hygiene release.
- On mismatch: `fail`.
- Upgrade owner: `egohygiene/pace`.
- Action: Regenerate from the pinned Hygiene release and review the resulting pull request.
