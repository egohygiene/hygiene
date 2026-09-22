---
schema: egohygiene.architecture-decision/v1
id: ADR-013
title: Define the canonical public-site surface and route registry
status: proposed
date: 2026-09-21
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/25
pull_request: null
related:
  - ADR-0001
  - ADR-002
  - ADR-005
  - ADR-006
  - ADR-009
  - ADR-012
  - egohygiene/identity#ADR-017
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/holon
  - egohygiene/identity
  - egohygiene/observatory
  - egohygiene/pace
  - egohygiene/relay
  - egohygiene/renderflow
  - egohygiene/website
affected_contracts:
  - egohygiene.public-site-surface-registry/v1
  - egohygiene.public-site-surface-declaration/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/25
    description: Authoritative scope and acceptance criteria for the canonical surface registry and repository declaration contract.
  - type: issue
    url: https://github.com/egohygiene/.github/issues/30
    description: Cross-repository roadmap that sequences this contract before reusable validation, rendering, adoption, and observability work.
  - type: documentation
    url: https://github.com/egohygiene/relay/blob/4fa92e187a6a980fea202c8309749a204a1ccae5/README.md
    description: Relay evidence for the deployed Repository Intelligence namespace and nested module routes.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/f9ba4ca9c8938b76e2564dc112455ad3b3e25cc2/docs/decisions/ADR-017-zensical-launchkit-publication-architecture.md
    description: Accepted Identity evidence preserving the product experience at the organization /identity/ route.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/c589587395750cd1c79c6fa0bef010189c547249/docs/ecosystem/visual-roadmap-system.md
    description: Existing organization and repository roadmap routes that require scope-specific bindings rather than one global path.
  - type: issue
    url: https://github.com/egohygiene/.github/issues/37
    description: Organization Identity module request whose /identity/ route conflicts with the accepted Identity product route and requires reconciliation.
exceptions: []
approval: null
---

# ADR-013: Define the canonical public-site surface and route registry

## Context

The organization roadmap names public mini-apps and supporting surfaces such as
documentation, Repository Intelligence, Identity, magazine, presentation,
garden, activity, roadmap, decisions, status, feeds, accessibility, privacy,
trust, community, support, and donation. Until now, those names have appeared
across issues, site proposals, repository documentation, and generated output
without one versioned route and state contract.

That ambiguity creates two kinds of drift. A consumer can interpret a friendly
name such as `roadmap` as either `/roadmap/` or the deployed Repository
Intelligence route `/intelligence/roadmap/`. A repository can also say a
surface is absent without distinguishing not applicable, missing, planned,
blocked, private, unpublished, withdrawn, or stale. Aggregators and generators
then have to guess.

Existing boundaries constrain the answer. Relay documents the Repository
Intelligence bundle under `/intelligence/` and nested module routes. Identity's
accepted ADR-017 preserves its product experience under `/identity/`. Agent-
Ready Web already owns discovery, representation, guarded capability,
commerce, and conformance policy. Repository presentation owns README and
orientation semantics. The later System Status contract must own incident and
operational semantics. Hygiene should connect those contracts without copying
their implementations or moving their authority.

## Decision

Propose two related v1 contracts at version `1.0.0-alpha.1`:

- `egohygiene.public-site-surface-registry/v1` is the Hygiene-owned catalog of
  stable surface IDs, canonical routes, redirect aliases, applicability,
  default semantic owner, source-artifact kind, renderer contract,
  dependencies, compatibility, composition, and ownership boundaries.
- `egohygiene.public-site-surface-declaration/v1` is a repository-owned,
  complete declaration of the resolved requirement, disposition, semantic and
  publication owners, source artifact, renderer, dependencies, publication
  state, visibility, freshness, assertion, revision, and evidence for every
  registered surface.

The initial registry contains 36 surfaces and two route profiles. The
`repository` profile preserves Relay's shipped Repository Intelligence bundle
under `/intelligence/`. The `organization` profile gives first-class control-
plane modules canonical top-level routes, including `/roadmap/`, `/decisions/`,
`/dependencies/`, and `/health/`. Modules kept local to Intelligence or a
repository detail—Now, Journey, Compare, Work, Diagnostics, and the legacy
Dashboard—remain nested in both profiles. Declarations select exactly one
profile; aliases redirect and cannot publish duplicate canonical content.

Separate an HTTPS host origin from a normalized `base_path` so GitHub project
Pages, product mounts, and versioned docs resolve without changing logical
route identity. Separate the subject repository (`site.id`) from the
publication repository so a central host can publish a subject's truthful
declaration without taking semantic ownership.

Preserve `/identity/` for the Identity product experience established by
Identity ADR-017. Keep the Repository Intelligence identity/adoption view as
the distinct `identity_intelligence` surface at `/intelligence/identity/`.
`.github#37` must reconcile its conflicting request for organization
`/identity/` before publication; the registry does not collapse incompatible
source, renderer, dependency, and ownership contracts.
The Identity Intelligence module depends on the Intelligence shell, not a
published Identity product surface, so it can report missing, inapplicable, or
stale adoption without creating a circular publication gate.

Reserve `/status/` as the stable `status` surface route, but do not define
incident, component, health, severity, uptime, or operational evidence
semantics here. Hygiene #62 owns that separately reviewed contract.

Routes are absolute and normalized. Directory routes end in `/`; file
endpoints such as `/feed.xml` do not. Query, fragment, encoded, wildcard, empty
segment, alias-chain, alias-cycle, and route-collision forms are invalid.

Keep policy and observed state independent:

- applicability: `applicable`, `not_applicable`, `unknown`, with separate
  evidence, freshness, assertion, reason, revision, and observation;
- requirement: `required`, `recommended`, `optional`;
- disposition: `owned`, `inherited`, `omitted`;
- implementation: `unknown`, `missing`, `planned`, `blocked`, `implemented`,
  `unsupported`, `not_applicable`;
- publication: `unknown`, `unpublished`, `preview`, `published`, `withdrawn`,
  `not_applicable`;
- visibility: `public`, `internal`, `private`;
- freshness: `current`, `stale`, `unknown`, `not_applicable`; and
- assertion: `authoritative`, `inferred`, `unknown`.

Applicability resolves before strength. Landing is always applicable; other
surfaces are site-declared, allowing a recommended status or privacy-choice
surface to be truthfully not applicable when its condition does not hold.
Applicable, not-applicable, and unresolved-unknown applicability results
require complete current-or-stale assessment evidence unless private visibility
requires redaction. Unknown records an evidence-backed unresolved review and
still forces delivery state to remain unknown rather than becoming fabricated
absence. Not-applicable synchronizes disposition and delivery axes. Blocked
state requires named blockers or the private redaction marker.

Published state requires a source, exact-version or full-SHA renderer pin,
canonical URL resolved from origin, base path, and route binding, evidence URL,
full represented commit SHA, observation time, and current-or-stale freshness.
A current surface revision equals the site revision; a stale revision differs
from it. Private state retains only safe state and reason while redacting
applicability, source, renderer, URL, revision, observation, evidence, and
dependency-topology details.

Declarations cover the entire registry in registry order and bind the registry
schema, exact version, canonical path, full revision, and canonical JSON
SHA-256. Non-synthetic validation additionally requires an externally resolved
registry revision so matching bytes cannot prove an arbitrary commit claim.
Consumers accept an exact version with resolved immutable revision and digest,
or an immutable revision with digest. Unknown surface IDs and pin or digest
mismatches fail closed. Because declarations have complete coverage, adding,
removing, or renaming any surface ID is breaking. Changing a route profile,
canonical route, alias meaning, state or evidence semantics, required field, or
privacy and provenance guarantee is also breaking.

Surface dependencies are route-profile-specific publication prerequisites. A
published surface can depend only on surfaces that are implemented and
published in the selected profile. Repository-profile Intelligence modules
depend on the Intelligence shell, while first-class organization routes such
as `/roadmap/`, `/decisions/`, and `/health/` publish independently. System
Status is not a prerequisite of Health in either profile; their semantics
remain independently owned until a later composition contract explicitly
relates them.

Ownership remains separated:

- Hygiene owns the registry, schemas, route identity, state vocabulary,
  compatibility, and privacy boundary.
- Each subject repository owns its facts, resolved applicability, represented
  revision, and surfaces whose registry authority is `repository`. A globally
  named authority owns that surface's semantics and source artifacts. The
  declared publication repository retains final host and deploy authority.
- Identity owns the `/identity/` product semantics and versioned inputs;
  Renderflow owns versioned renderer inputs. Neither owns consuming-site facts,
  route composition, or deployment authority.
- Holon may scaffold declarations for new repositories from eligible immutable
  pins without inventing facts or evidence.
- Relay may provide reusable validation, rendering, redirects, and publication
  workflows without redefining policy or publishing without repository
  authority.
- Observatory may aggregate privacy-safe declarations and freshness without
  disclosing private topology or silently remediating.
- Pace may propose reviewed adoption and reconciliation for existing
  repositories without direct default-branch mutation.
- The organization site may compose the resulting routes while consuming the
  same canonical contracts and organization-owned facts.

Agent-Ready Web resources remain in that profile and are referenced rather
than duplicated as surface entries. Repository Intelligence pages remain
projections; they never replace canonical roadmap, ADR, Git, GitHub, release,
deployment, or provider sources.

## Alternatives considered and rejected

### Use one global canonical route per surface

Rejected because organization routes and Relay's repository bundle have
different, already documented topology. Making either set globally canonical
would contradict the other. Explicit route profiles preserve both while every
declaration still selects exactly one canonical binding.

### Move Identity under Repository Intelligence

Rejected because Identity ADR-017 already assigns `/identity/` to a product
experience with its own nested documentation and legal surfaces. The
intelligence/adoption view receives a distinct ID and scoped route.

### Treat activity and journey as separate surfaces

Rejected because both names describe one history view. Separate canonical
pages would duplicate content and create divergent evidence; `journey` is the
surface and activity paths are aliases.

### Put implementation and publication in one status enum

Rejected because implemented-but-private, implemented-but-unpublished,
published-but-stale, blocked, missing, and not-applicable states carry
different operational and privacy meaning.

### Fold not-applicable into requirement strength

Rejected because applicability is conditional and must resolve before
strength. A recommended mechanism can truthfully be not applicable without
changing the registry's recommended strength, and unknown applicability must
remain visible.

### Let declarations include only present surfaces

Rejected because absence would become ambiguous and an older consumer could
silently ignore newly registered policy. Complete declarations make every
omission inspectable.

### Copy renderer or neighboring policy into Hygiene

Rejected because it would violate repository boundaries and let a registry
redefine implementations owned by Identity, Relay, Renderflow, or later System
Status work.

## Consequences and tradeoffs

- Generators, renderers, aggregators, and rollout tooling receive one stable
  vocabulary and no longer need route-name heuristics.
- Complete declarations are intentionally verbose, but their explicit absence
  and privacy states prevent false readiness claims.
- Existing friendly paths remain available through profile-specific redirects
  while each declaration has one canonical content location.
- Base-path and publication-owner fields add declaration detail but cover
  project Pages and centrally hosted subjects without route heuristics.
- Exact pins and digests make upgrades deliberate and reviewable, at the cost
  of updating declarations when the registry changes.
- Reserving `/status/` allows routing work to proceed without prematurely
  deciding incident semantics.
- A proposed registry and synthetic fixtures establish no live site,
  deployment, adoption, conformance, or publication claim.

## Implementation and evidence links

The proposal is represented by the canonical
[`public-site-surface-registry.json`](../../catalog/public-site-surface-registry.json),
the [registry schema](../../schemas/public-site-surface-registry.v1.schema.json),
the [declaration schema](../../schemas/public-site-surface-declaration.v1.schema.json),
the [human specification](../ecosystem/PUBLIC_SITE_SURFACES.md), the dependency-
free validator, complete synthetic [fixtures](../../fixtures/public-site-surfaces),
and focused tests. The organization contract index, dependency-boundary
register and generated view, architecture documents, README, roadmap,
changelog, and continuity checkpoint link to those canonical sources without
copying the contract.

Issue #25 is the proposal and review authority. No automatic pull-request CI,
acceptance, release, or downstream implementation is assumed.

## Replacement or exit strategy

Consumers retain an existing valid immutable pin until a reviewed upgrade.
Compatible revisions may add optional metadata while preserving every existing
surface ID, route meaning, state rule, and privacy guarantee. Adding even an
optional surface is breaking because complete declarations must add an explicit
record. Breaking changes require a documented migration and deliberate pin
update.

If the proposal is rejected, repositories keep their existing routes and no
fixture or proposed declaration may be treated as adoption evidence. If a
future contract supersedes this one, this ADR and contract-index entries remain
discoverable and link to the replacement rather than being rewritten.

## Follow-up work

Maintainers review this focused proposal. After acceptance, Relay can implement
reusable validation, redirect, rendering, and publication workflows;
Observatory can normalize privacy-safe state; Pace can plan reviewed adoption;
Holon can scaffold new declarations; and individual repositories can declare
their surfaces. Hygiene #62 remains the authority for System Status semantics.
Those changes are separate review surfaces and are not implemented or claimed
here.
