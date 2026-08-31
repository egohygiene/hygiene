---
schema: egohygiene.architecture-decision/v1
id: ADR-007
title: Define an inheritable repository release-convention baseline
status: proposed
date: 2026-08-31
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/27
pull_request: null
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/*
affected_contracts:
  - egohygiene.repository-release-policy/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/27
    description: Approved scope for the inheritable release-convention baseline and its downstream consumers.
  - type: external
    url: https://github.com/egohygiene/aether/pull/62
    description: Merged immutable Aether release-declaration contract consumed by this policy without copying its protocol.
exceptions: []
approval: null
---

# ADR-007: Define an inheritable repository release-convention baseline

## Context

The organization needs a consistent way to plan, review, version, document,
and recover releases across contracts, packages, tools, images, sites,
publications, workspaces, private repositories, and archived history. Aether
now owns the formal repository release declaration, but an owner is still
needed for applicability, migration status, legacy exceptions, and the
cross-repository consumer boundary.

Copying Aether's schema into every repository would create competing protocol
sources. Conversely, making Relay workflows or Egolint diagnostics define the
policy would conflate execution or checking with organizational governance.

## Decision

Propose `egohygiene.repository-release-policy/v1` at `1.0.0-alpha.1` as the
Hygiene-owned composition profile. It pins Aether
`egohygiene.repository-release/v1` version `1.0.0` to merge commit
`8a2a3d08f3aa9da3847bd5277843506ab855192e` and requires an explicit future
policy update to move that pin.

The baseline requires a root changelog, Aether declaration, one component
version authority, bounded Taskfile handoffs, a manually dispatched workflow,
release/rollback guidance, and an `AGENTS.md` pointer for applicable
repositories. It uses required, advisory, not-applicable, and temporary
exempt adoption states, preserving legacy tags and changelog history without
rewriting or fabricating it.

Repository release facts remain in `.egohygiene/release.json`; Hygiene does
not require an external release registry. Hygiene dogfoods the profile as an
active contract repository with its own versioned policy artifact.

## Alternatives considered and rejected

### Copy the Aether declaration into a Hygiene schema

Rejected because Aether owns the release protocol. A copied schema would drift
and force downstream consumers to choose between two authorities.

### Make a Relay workflow the organization policy

Rejected because reusable execution cannot represent every package, container,
site, publication, internal, or historical delivery adapter. Relay consumes a
stable policy; it does not define release applicability.

### Require one hosted release registry

Rejected because provider publication is repository-owned, may be private or
external, and should not become a second source of truth for local release
facts.

### Rewrite legacy tags and changelogs into a uniform history

Rejected because that destroys provenance and invents evidence. The baseline
governs future release decisions while recording existing history honestly.

## Consequences and tradeoffs

- Every repository class gets one visible semantic release baseline without
  assuming identical build or delivery mechanics.
- New and active repositories have clear required files and handoffs; an
  incubating repository may remain advisory until a durable release boundary
  exists.
- Consumers must carry a version and immutable Aether pin, which adds a small
  review step but prevents branch-based protocol drift.
- Relay #47 and Egolint #29 receive a bounded policy input; Pace can later
  propose migration pull requests instead of direct mutations.
- The alpha policy remains proposed and makes no claim that the full fleet is
  already conformant.

## Implementation and evidence links

Issue #27 implements the machine profile, JSON Schema, deterministic
validator, representative examples, migration guide, contract index,
dependency register, formal decision record, and Hygiene dogfood declaration.
The Aether dependency is the immutable merged contract linked above.

## Replacement or exit strategy

An additive policy change remains within v1 only when it preserves valid local
declarations and explicit migration behavior. A change to slot meaning,
applicability precedence, adoption-state semantics, Aether contract identity,
or migration/exception requirements requires a proposed major successor and
fixtures that preserve historical release evidence.

A later accepted policy may replace this proposal without rewriting legacy
tags, release assets, or changelog entries.

## Follow-up work

1. Obtain maintainer approval and publish a versioned Hygiene policy release.
2. Implement Relay #47 against the approved immutable policy pin.
3. Implement Egolint #29 diagnostics against the same pin and fixtures.
4. Pilot representative repositories before Pace proposes grouped migrations.
5. Aggregate only released evidence in Observatory after consumer contracts
   stabilize.
