# ADR-0001: Adopt the holistic ecosystem architecture v0.1

- Status: Accepted
- Accepted: 2026-08-18
- Owners: `egohygiene`
- Scope: organization repository topology, ownership, and dependency direction
- Issue: <https://github.com/egohygiene/hygiene/issues/1>

## Context

Ego Hygiene has 25 repositories at different maturity levels and substantial
temporary incubation under `empathy`. Rapid development requires a stable map
so that temporary colocation does not become permanent ownership ambiguity.

The reviewed architecture package reconciles the live repository inventory,
the Flow suite boundary, Realm and Mantle, staged Empathy material, public web
surfaces, and older architecture references.

## Decision

Adopt the architecture under `docs/ecosystem/` as the accepted v0.1 ecosystem
model.

### Accepted

- Use the five-plane portfolio model.
- Make `hygiene` the canonical owner of ecosystem architecture, the repository
  catalog, platform policy, and cross-repository ADRs.
- Keep `.github` as the public organization inbox, organization profile,
  defaults, community-health fallback, and coordination surface.
- Treat Empathy as the golden consumer, integration testbed, and bounded
  incubator while specialist capabilities are extracted.
- Preserve standalone tools and compose them through versioned artifacts and
  contracts.
- Generate compact repository-local ecosystem context from the canonical
  architecture instead of copying the complete specification into every repo.

### Amended during acceptance

- Organization-level work may begin in `.github` as a practical fallback. Its
  implementation issues must move to owning repositories, while lasting
  architectural decisions and catalog state remain in Hygiene.
- The machine-readable catalog is promoted in a separate contract change so
  its schema, validator, fixtures, and generated documentation are reviewed
  together.

### Deferred

- The proposed `firmament` infrastructure repository remains uncreated until
  Realm's artifact, provenance, secrets, lock, and recovery contracts are
  proven.
- Realm's first stable language profile and exact `full` contents remain
  separate evidence-based decisions after the capability model is accepted.
- Historical PNG diagrams remain references until selected assets are reviewed
  for provenance and archived explicitly.

### Rejected

- A giant universal base image containing every optional tool or service.
- Copying sibling repository source as an integration mechanism.
- Mutable production dependencies on another repository's default branch.
- Credentials, signing material, workstation secrets, or private identity data
  in repositories, images, templates, diagrams, or generated context.
- Treating raw archives or old diagrams as the canonical architecture.

## Consequences

- Architecture-changing work updates Hygiene first or in the same reviewed
  change set.
- Holon creates repositories, Pace converges existing repositories, and
  Observatory reports evidence without silently remediating it.
- Realm consumes released Mantle artifacts; Relay invokes Egolint; Empathy
  proves the assembled platform through released boundaries.
- Flow composes Aniflow, Optiflow, and Renderflow without absorbing their
  implementations or allowing direct sibling dependencies.
- The accepted release is prepared as `architecture-v0.1.0`; release mechanics
  and the canonical catalog are completed by follow-on work.

## Verification

- The required narrative, migration, agent, source-review, and catalog-view
  documents are present under `docs/ecosystem/`.
- Mermaid, PlantUML, and Excalidraw sources describe the same five planes and
  repository topology.
- Regenerating `ecosystem.excalidraw` from its source script produces no diff.
- The versioned dependency-boundary register and local reference validator make
  the accepted integration direction, forbidden media-engine couplings,
  immutable pinning policy, and expiring exception requirements executable.
