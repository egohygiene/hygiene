---
schema: egohygiene.architecture-decision/v1
id: ADR-005
title: Unify repository intelligence as a provenance-aware graph projection
status: proposed
date: 2026-08-25
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/19
pull_request: https://github.com/egohygiene/hygiene/pull/20
related:
  - ADR-002
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/*
affected_contracts:
  - egohygiene.repository-intelligence/v1
  - egohygiene.repository-intelligence-vocabulary/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/19
    description: Approved implementation scope for the proposed Repository Intelligence contract.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/20
    description: Review surface for the proposed contract, vocabulary, fixture, validator, and tests.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/main/docs/ecosystem/visual-roadmap-system.md
    description: Reviewed visual-roadmap ownership, evidence, privacy, and publication design.
exceptions: []
approval: null
---

# ADR-005: Unify repository intelligence as a provenance-aware graph projection

## Context

The proposed organization ADR foundation describes generated decision and
activity data, while the visual-roadmap design describes a separate roadmap
manifest and evidence snapshot. Planned Repository Intelligence views also need
issues, pull requests, commits, checks, releases, and deployments to connect to
the same intent and decision records.

Separate hand-built payloads for each page would duplicate entity identity,
provenance, privacy, freshness, and relationship semantics. A roadmap node,
decision, or commit could then appear authoritative in one view and inferred or
stale in another. Live browser queries would also require tokens, make builds
nondeterministic, and weaken the repository-owned publication boundary.

The organization needs a common interchange contract without turning that
projection into a second source of truth or moving implementation ownership
into Hygiene.

## Decision

Propose `egohygiene.repository-intelligence/v1` as the normalized,
repository-scoped graph projection for Repository Intelligence. The first
contract release is `1.0.0-alpha.1` and remains proposed until this ADR receives
explicit human approval.

The projection contains:

- stable entities for repositories, roadmap steps, architecture decisions,
  issues, pull requests, commits, checks, releases, and deployments;
- a versioned directed-relationship vocabulary with explicit endpoint kinds
  and cardinality;
- normalized lifecycle events with occurrence time, recording time, actor
  attribution when publication policy permits it, changes, and provenance;
- source records that distinguish authoritative, inferred, and unknown claims
  from current, stale, unknown, and not-applicable freshness; and
- explicit visibility, redaction, represented-commit, and generator metadata.

Canonical facts remain in their owners: `ROADMAP.md`, ADR Markdown, Git, GitHub,
check providers, release records, and deployment providers. The graph is a
deterministic, disposable projection of explicitly pinned inputs.

Specialized `decisions.json`, `activity.json`, roadmap manifests, and page view
models may remain narrower projections or compatibility adapters. They must use
the shared identity, provenance, visibility, and relationship semantics when
they claim compatibility with Repository Intelligence v1.

Hygiene owns the contract and vocabulary. Aether owns authoring guidance;
Egolint owns semantic lint rules; Observatory owns normalized evidence queries
and fleet snapshots; Holon owns reusable visualization components; Relay owns
collection, validation orchestration, static generation, and publication
workflows; Pace owns reviewable fleet adoption. Repository owners retain intent,
local decisions, and final site composition authority.

## Alternatives considered and rejected

### Keep one unrelated contract per page

Rejected because every page would redefine identifiers, provenance, freshness,
privacy, and links. Small page-specific view models remain appropriate only as
derived adapters over one normalized contract.

### Make Observatory the contract owner

Rejected because Observatory consumes and queries evidence. The organization
vocabulary and cross-repository policy belong to Hygiene; Observatory should not
silently redefine them while aggregating data.

### Query GitHub directly from the public site

Rejected because browser-side collection would expose credentials or depend on
unauthenticated rate limits, produce different answers over time, and make
privacy filtering harder to review.

### Treat Git history as the complete source of intent

Rejected because commits show delivery activity, not why work was chosen,
whether a decision was approved, whether exit criteria passed, or whether a
roadmap step remains blocked.

### Require commit trailers for all historical linkage

Rejected because adoption must not rewrite history. Trailers improve future
precision but explicit roadmap, ADR, issue, and pull-request links remain valid
sources.

## Consequences and tradeoffs

- Every Repository Intelligence view can resolve the same entity and evidence
  chain from intent through deployment.
- Consumers can show uncertainty and staleness without converting absence into
  false success.
- A richer graph contract costs more authoring and validation work than a page-
  specific payload.
- Alpha consumers must pin an exact contract version and tolerate review-driven
  change before v1 activation.
- Stable identifiers and source links make migration safer, but generators must
  reject collisions and dangling references.
- Public projections reveal less data by default because unknown visibility and
  unapproved actor metadata fail closed.

## Implementation and evidence links

The schema, vocabulary, complete-quest fixture, reference validator, and tests
are implemented in the pull request that resolves issue #19. This proposed ADR
does not claim that Relay collection, Observatory aggregation, Holon rendering,
or Pace adoption is complete.

## Replacement or exit strategy

Additive optional fields and new namespaced extensions may remain compatible
within v1. A change to identity, required fields, authority, visibility,
relationship direction, or event meaning requires a new major contract and a
proposed superseding ADR.

Alpha versions may change through reviewed increments. Consumers must pin the
exact pre-release version. Once v1 is active, migrations must publish old-to-new
identifier rules, compatibility fixtures, and an overlap window before removing
the previous contract.

Because canonical sources remain independent, the projection can be regenerated
or replaced without rewriting roadmap, ADR, Git, GitHub, release, or deployment
history.

## Follow-up work

1. Obtain explicit human review for ADR-002, ADR-005, and their policy boundary.
2. Add the decision-impact hook in Aether and semantic checks in Egolint.
3. Implement Observatory's normalized graph/read model against the complete
   quest fixture.
4. Implement Holon's accessible Roadmap, Decisions, and Journey components.
5. Implement Relay collection, generation, and consumer-owned publication.
6. Use Pace to pilot and then reconcile adoption across eligible repositories.
