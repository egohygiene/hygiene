---
schema: egohygiene.architecture-decision/v1
id: ADR-009
title: Define the Agent-Ready Web profile foundation
status: proposed
date: 2026-09-14
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/50
pull_request: https://github.com/egohygiene/hygiene/pull/54
related:
  - ADR-0001
  - ADR-002
  - ADR-006
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/holon
  - egohygiene/relay
  - egohygiene/pace
  - egohygiene/store
  - egohygiene/observatory
affected_contracts:
  - egohygiene.agent-ready-web-profile/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/50
    description: Reviewed checkpoint scope, exclusions, acceptance criteria, and branch boundary.
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/16
    description: Parent roadmap and ordered four-checkpoint dependency boundary.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/54
    description: Focused review surface for the proposed checkpoint 1 foundation.
exceptions: []
approval: null
---

# ADR-009: Define the Agent-Ready Web profile foundation

## Context

Issue #16 proposes an organization publication profile for websites that stay
excellent for people while providing explicit interfaces for crawlers,
retrieval systems, and browser agents. Its complete scope spans discovery,
alternate representations, interactive capabilities, efficiency, commercial
metadata, safety, generators, rollout, and evidence. Defining all of that in
one change would make maturity, ownership, and compatibility difficult to
review independently.

The first checkpoint needs stable language before it can classify concrete
mechanisms. In particular, a discovery representation must not silently grant
an action, a lower-overhead representation must not weaken provenance or
access control, and commercial metadata must not imply permission to transact.
Every later mechanism also needs primary references and evidence supporting
its registration and maturity rather than being treated as a standard because
it appeared in backlog prose.

## Decision

Propose `egohygiene.agent-ready-web-profile/v1` at `1.0.0-alpha.1` with Hygiene
as its canonical policy owner. The foundation defines four independent primary
concerns—readability, capability, efficiency, and commerce—and requires each
future mechanism to belong to exactly one. Cross-concern inference is
forbidden, and dependencies between concerns must be explicit.

The profile defines stable application, commerce, content, documentation, and
hybrid site classes; required, recommended, optional, conditional, and
prohibited requirement strengths; and the four maturity levels approved by
issue #50. Maturity and requirement strength remain independent.

Each future mechanism must declare site-class-aware requirements, a dated
maturity rationale, at least one primary authoritative reference, registration
evidence, and isolated namespaced extensions. The canonical mechanism registry
is empty in this checkpoint so discovery artifacts, browser-agent protocol
details, advertising files, and commerce actions remain later decisions.

The contract uses semantic versioning and exact-version or immutable-revision
consumer pins. Unknown core values fail closed. Unknown validly namespaced
extensions may be preserved as uninterpreted data but cannot affect core
conformance or grant authority.

Hygiene owns policy and reference validation; Holon owns future new-site
generation; Relay owns reusable workflow execution and evidence transport;
Pace owns reviewable existing-site convergence; Store owns later guarded
commerce-domain contracts; and Observatory owns read-only evidence and metrics.
This proposal implements none of those downstream capabilities.

## Alternatives considered and rejected

### Define one undifferentiated agent-ready checklist

Rejected because metadata, actions, transport efficiency, and commerce have
different security and ownership implications. A single checklist would allow
one concern to imply another and make safe requirement resolution ambiguous.

### Populate the complete mechanism catalog in the foundation

Rejected because issue #50 deliberately precedes discovery and capability
catalog review. Empty canonical mechanisms plus synthetic fixtures prove the
contract without pre-deciding checkpoints #51 or #52.

### Put policy and generation together in Holon

Rejected because Hygiene owns organization policy while Holon materializes
accepted, versioned inputs. Combining them would let generator behavior become
an accidental policy source.

### Permit unstructured references and maturity notes

Rejected because consumers could not distinguish a primary specification from
supporting commentary or determine when a maturity assessment was made.

## Consequences and tradeoffs

- Later checkpoints gain stable site, requirement, maturity, reference,
  evidence, extension, and ownership vocabulary.
- Exactly-one concern assignment prevents descriptive metadata from becoming
  implicit capability or transaction authority.
- The empty mechanism registry keeps the PR reviewable but means the profile
  cannot yet drive useful site generation or conformance assessment.
- Exact pins and fail-closed unknown core values prevent silent semantic drift,
  while requiring reviewed consumer upgrades for additive revisions.
- Synthetic compatibility fixtures demonstrate the registration shape without
  claiming external standards, adoption, or downstream implementation.
- The profile stays proposed until explicit maintainer authority permits a
  lifecycle transition.

## Implementation and evidence links

The proposal is implemented by the canonical
[`agent-ready-web-profile.json`](../../catalog/agent-ready-web-profile.json),
its [JSON Schema](../../schemas/agent-ready-web-profile.v1.schema.json), the
[human policy](../ecosystem/AGENT_READY_WEB.md), synthetic
[compatibility fixtures](../../fixtures/agent-ready-web), a dependency-free
reference validator, and focused tests. Issue #50 is the review authority for
this bounded checkpoint; [PR #54](https://github.com/egohygiene/hygiene/pull/54)
merged its implementation. The decision lifecycle remains proposed.

## Replacement or exit strategy

Clarifications and optional registrations may evolve additively under an exact
reviewed version pin. Removing or renaming core vocabulary, changing meaning,
weakening prohibited behavior, changing reference/evidence shape, or moving an
ownership boundary requires a proposed major-version successor and migration
fixtures.

If the proposal is declined, consumers must not infer policy from the fixture
or documentation. The proposed contract and ADR remain historical review
evidence, and no downstream rollout or publication state needs to be undone
because this checkpoint authorizes neither.

## Follow-up work

PR #54, PR #55, and PR #56 merged the first three ordered implementation
checkpoints without activating the proposed profile. ADR-012 and issue #53 own
final integration and conformance evidence. Lifecycle promotion, releases, and
all downstream implementation or adoption remain separate work requiring their
own authority.
