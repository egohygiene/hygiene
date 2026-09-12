---
schema: egohygiene.architecture-decision/v1
id: ADR-002
title: Establish an organization ADR and delivery-history contract
status: accepted
date: 2026-08-20
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/15
pull_request: https://github.com/egohygiene/hygiene/pull/10
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/*
affected_contracts:
  - egohygiene.architecture-decision/v1
  - egohygiene.architecture-decision-policy-reference/v1
  - egohygiene.organization-contract-index/v1
implementation_status: verified
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/15
    description: Ratification scope and acceptance criteria for the organization ADR contract.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/10
    description: Merged foundation for this proposed decision and its first canonical contracts.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/main/docs/ecosystem/ARCHITECTURE.md
    description: Accepted ecosystem ownership and generated-context boundaries.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/main/library/organization/specs/architecture/governance/decisions.spec.md
    description: Legacy Aether draft retained as migration evidence rather than canonical policy.
  - type: implementation
    url: https://github.com/egohygiene/aether/pull/50
    description: Draft decision-impact agent hook pinned to the proposed Hygiene policy boundary.
  - type: implementation
    url: https://github.com/egohygiene/relay/tree/main/actions/repository-intelligence
    description: Existing reusable static intelligence action and public projection boundary.
  - type: validation
    url: https://github.com/egohygiene/hygiene/issues/15#issuecomment-5647360172
    description: Ratification packet recording 95 passing tests and focused lifecycle and inheritance checks.
  - type: approval
    url: https://github.com/egohygiene/hygiene/issues/15#issuecomment-5647398908
    description: Explicit maintainer approval of ADR-002 and policy v1.1.0 at the pinned implementation commit.
exceptions: []
approval:
  date: 2026-09-12
  by: szmyty
  evidence: https://github.com/egohygiene/hygiene/issues/15#issuecomment-5647398908
---

# ADR-002: Establish an organization ADR and delivery-history contract

## Context

Ego Hygiene repositories already contain architecture documents, inline
decision logs, detailed ADRs, agent instructions, and a reusable repository
intelligence dashboard. Their conventions differ in location, identifier width,
status vocabulary, metadata, approval evidence, and source authority.

The read-only audit found four-digit and three-digit ADRs, an alternate `OFD`
prefix, inline and detailed storage, missing machine-readable metadata, and one
repository-local ID collision. Some reconstructed records claim acceptance
without durable approval evidence. No repository currently contains the planned
generated `docs/ecosystem/CONTEXT.md`.

Without a canonical contract, humans and coding agents can duplicate decisions,
confuse acceptance with implementation, or build dashboards that become a
second source of truth. The organization also needs a chronological delivery
view without copying protected GitHub content into public output.

## Decision

Adopt a Hygiene-owned organization ADR policy, versioned front matter schema,
and repository inheritance-reference schema. New local ADRs use
`docs/decisions/ADR-NNN-short-slug.md`, begin as `proposed`, retain local
ownership, and link human disposition, implementation evidence, affected
contracts, affected repositories, and supersession lineage. Repository-local
policy pins the Hygiene version and commit instead of copying global prose.

Decision status and implementation status remain independent. Only explicit
human approval evidence may assign a non-proposed lifecycle disposition.
Repository-specific metadata is permitted only through registered namespaced
extension contracts; global lifecycle, identity, ownership, and privacy rules
cannot be overridden locally.

Egolint will later own ADR lint semantics. Relay will orchestrate those checks
and generate deterministic repository `decisions.json` and privacy-safe
`activity.json` contracts. Observatory will later aggregate those contracts.
Repository sites retain final static-site composition and deployment authority
under `/intelligence`, with `/adr` redirecting to `/intelligence/decisions`.

This decision defines contracts, compatibility fixtures, reference contract
checks, and migration rules. It does not claim fleet validation, generators,
routes, redirect, dashboard views, or aggregation are implemented.

## Alternatives considered and rejected

### Make Aether the policy owner

Rejected because Aether owns reusable agent guidance and templates, while
organization policy, cross-repository conventions, and contract indexing belong
to Hygiene. Aether should pin and project the approved contract.

### Put the canonical system in `.github`

Rejected because `.github` is the public intake and fallback layer. Making it
the control plane would duplicate Hygiene's accepted ownership.

### Centralize every ADR in Hygiene

Rejected because product and tool repositories own their local decisions and
implementation evidence. Hygiene owns only organization decisions and shared
conventions.

### Hand-author dashboard data

Rejected because manually maintained JSON or pages would drift from ADRs and
GitHub metadata. Generated projections preserve one source of truth.

### Mechanically rewrite existing decision history

Rejected because IDs, rationale, approval claims, and blame context carry
provenance. Migration must validate first and preserve ambiguity until a human
resolves it.

## Consequences and tradeoffs

- Humans and agents gain a consistent significance test, lifecycle, and
  cross-repository reference key.
- Approval, implementation, and verification can no longer be conflated.
- Existing repositories require different validate-first or scaffold-first
  migrations rather than one bulk replacement.
- Aether's decision-impact hook demonstrates a pinned consumer and may now be
  promoted through its own reviewed release and repository-adoption workflow.
- Egolint, Relay, and Observatory gain explicit boundaries, but their fleet
  implementations remain follow-up work.
- Front matter and lineage add authoring overhead only for consequential
  decisions; routine implementation remains outside the ADR requirement.
- Privacy-safe activity views expose less detail for private repositories by
  design.

## Implementation and evidence links

Current evidence includes the audited repository state, canonical Hygiene
schemas and fixtures, Aether's pinned decision-impact hook, the existing Relay
intelligence action, the ratification validation packet, and explicit
maintainer approval linked in front matter. Together they verify this contract
package without claiming that fleet rollout, repository publication, or every
downstream consumer is complete.

## Replacement or exit strategy

The policy and schemas are versioned contracts. A breaking change requires a
new schema version and a proposed organization ADR with migration guidance.
Aether packages, Holon projections, Relay generators, and Observatory inputs
must pin a supported version so implementations can be replaced without
rewriting canonical ADR content.

If the system creates excessive friction, the significance test or generated
projection contract can be superseded while retaining decision history. Local
Markdown remains portable even if Relay or Observatory is replaced.

## Follow-up work

1. Promote and release Aether's pinned instruction module against the accepted
   policy revision.
2. Complete Holon's migration-safe scaffold and Relay's reusable conformance
   validation.
3. Complete deterministic Relay generation and `/decisions/` publication with
   privacy and legacy fixtures.
4. Pilot Identity with a provenance-preserving migration map.
5. Use Pace to roll out grouped, reviewable repository pull requests.
