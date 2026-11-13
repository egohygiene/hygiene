---
schema: egohygiene.architecture-decision/v1
id: ADR-0020
title: Separate organization Intelligence export composition from its Pages publisher
status: proposed
date: "2026-11-13"
decision_scope: organization
visibility: public
owners: [egohygiene/hygiene]
issue: https://github.com/egohygiene/.github/issues/41
pull_request: null
related: [ADR-0002, ADR-0005, ADR-0013]
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/.github
  - egohygiene/egohygiene.io
  - egohygiene/relay
affected_contracts:
  - egohygiene.public-site-surface-registry/v1
  - egohygiene.public-site-surface-declaration/v2
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/.github/issues/41
    description: Existing organization Intelligence coordination and reconciliation of its historical website hosting criterion.
  - type: documentation
    url: https://github.com/egohygiene/.github/blob/58e1e6b336c3350bb31ceb4286d660860c992207/docs/reviews/2026-11-13-real-report-proof.md
    description: Actual sealed export and review artifact canary, with original partial and historical evidence retained separately from publication.
  - type: documentation
    url: https://github.com/egohygiene/.github/blob/58e1e6b336c3350bb31ceb4286d660860c992207/docs/decisions/ADR-0006-organization-intelligence-entrypoint.md
    description: Independent proposed organization entry-point record, whose approval remains null.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/31ae6fb78757502e7474e5518904fc568840c1ee/docs/ecosystem/PUBLIC_SITE_SURFACES.md
    description: Existing route profiles, literal project mount compatibility and distinct semantic/source/renderer/publication owners.
exceptions: []
approval: null
---

# ADR-0020: Separate organization Intelligence export composition from its Pages publisher

## Context

The maintainer selected `.github` as the primary organization Intelligence
entry point and explicitly authorized work toward live project Pages. The
website already owns the organization UI and a sealed Intelligence-only export;
the actual review canary retains one partial historical audit and unavailable
Core/Sanity inputs. Review receipts expressly supply no deploy authority.

The v1 surface contract separates subject and publication repositories but
fixes Relay-compatible renderers to Relay and the landing renderer to the site.
That cannot truthfully name the actual website exporter for this composition.
The older registry ownership sentence also combines website composition and
hosting. Neither a false Relay label nor silent owner reassignment is valid.

## Decision

Propose a narrowly scoped v2 declaration dialect over the same v1 route
registry. It selects only the public `.github` organization profile at
`https://egohygiene.github.io/.github/`. Landing and the 19 existing Intelligence
surfaces name the website exporter and one exact producer revision explicitly.
All other renderer rules and every existing route, source, state, privacy,
evidence and dependency invariant remain unchanged.

The website owns UI/source composition and its independent company site;
`.github` owns selected composition references, final organization publication
and recovery. Hygiene retains policy, Observatory retains normalized models,
and each repository keeps its own dashboard and publisher. Current registry,
architecture and repository ownership descriptions reflect that separation
without promoting maturity, lifecycle or human disposition.

A small owner facade validates the new binding, then privately projects it
into the old validation vocabulary to reuse the unchanged v1 semantics. The
original v2 declaration is the only retained/hash-bound statement. No new
registry, model assembler, renderer copy or provider adapter is introduced.

## Alternatives considered and rejected

- Calling the website renderer Relay or `.github` would make ownership false.
- Treating a review receipt as permission would erase its original boundary.
- Relaxing all renderer owners or redefining repository profiles would weaken
  valid existing consumers without a justified need.
- Copying the entire website would import company/store routes and duplicate
  the compositor. Publishing the sealed Intelligence-only export preserves it.

## Consequences and tradeoffs

The explicit dialect needs reviewed consumer adoption; older validators do
not gain v2 support. Existing v1 helper/schema bytes and historical pins remain
valid. Current registry ownership metadata changes its canonical digest, so
current fixture references rebind together without rewriting their facts.
The organization publisher must still match the declaration to the actual
producer, artifact, model clocks, origin/base, routes and complete file hashes.

An implemented unavailable page does not become a successful audit, status
monitor or ratified architecture. Before deployment the declaration remains
unpublished; actual deployment/live/recovery evidence is recorded separately.
Explicit task authorization supplies no ADR acceptance and no policy activation.

## Implementation and evidence links

The [hosting compatibility guide](../ecosystem/ORGANIZATION_INTELLIGENCE_HOSTING.md),
v2 declaration schema, owner facade and focused positive/negative tests are
the bounded owner implementation. The current publisher candidate remains
owned by `.github`. This record stays proposed with null approval; the selected
Aether decision-authoring reference is `dc8a16851f452763ef4f7fbe4bf057d4500b1921`
and Hygiene ADR policy remains accepted v1.2.0. No older record is ratified,
superseded or reclassified by this source change.

## Replacement or exit strategy

Keep all valid v1 consumers and immutable pins. A rejected or replaced hosting
proposal does not erase prior source or receipts. The publication repository
owns rollback to its reviewed prior source/artifact, while the website retains
its independent publisher and routes. Broader renderer or hosting profiles
need a separate explicit contract change rather than extending this exception.

## Follow-up work

Peer and select the exact owner resources in the existing organization
publisher, then qualify the separately authorized Pages deployment and live
routes/recovery. Reconcile historical organization acceptance text against
actual evidence. Native EgoLint/Observatory v2 adoption, organization-wide
assessments and human ADR ratification remain independent owner work.
