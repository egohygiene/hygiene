---
schema: egohygiene.architecture-decision/v1
id: ADR-002
title: Establish an organization ADR and delivery-history contract
status: proposed
date: 2026-08-20
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: null
pull_request: null
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/*
affected_contracts:
  - egohygiene.architecture-decision/v1
  - egohygiene.organization-contract-index/v1
implementation_status: not_started
evidence:
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/main/docs/ecosystem/ARCHITECTURE.md
    description: Accepted ecosystem ownership and generated-context boundaries.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/main/library/organization/specs/architecture/governance/decisions.spec.md
    description: Existing draft decision specification requiring ownership reconciliation.
  - type: implementation
    url: https://github.com/egohygiene/relay/tree/main/actions/repository-intelligence
    description: Existing reusable static intelligence action and public projection boundary.
exceptions: []
approval: null
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

Propose a Hygiene-owned organization ADR policy and versioned front matter
schema. New local ADRs use `docs/decisions/ADR-NNN-short-slug.md`, begin as
`proposed`, retain local ownership, and link approval, implementation evidence,
affected contracts, affected repositories, and supersession lineage.

Decision status and implementation status remain independent. Only explicit
human approval evidence may transition a proposal to `accepted`.

Relay will later validate ADRs and generate deterministic repository
`decisions.json` and privacy-safe `activity.json` contracts. Observatory will
later aggregate those contracts. Repository sites retain final static-site
composition and deployment authority under `/intelligence`, with `/adr`
redirecting to `/intelligence/decisions`.

This proposal defines contracts and migration rules only. It does not claim the
validator, generators, routes, redirect, dashboard views, or aggregation are
implemented.

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
- Aether's current draft specification and default-accepted template require a
  migration after this policy is approved.
- Relay and Observatory gain explicit boundaries, but their schemas and
  implementations remain follow-up work.
- Front matter and lineage add authoring overhead only for consequential
  decisions; routine implementation remains outside the ADR requirement.
- Privacy-safe activity views expose less detail for private repositories by
  design.

## Implementation and evidence links

Current evidence is limited to the audited repository state and the existing
Relay intelligence action linked in front matter. No implementation or
validation run is claimed.

The pull request for this proposal must be added to `pull_request` after it is
opened. Human approval, if granted, must be recorded separately in `approval`
before the status changes.

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

1. After human approval and merge, update Aether and Holon with pinned reusable
   guidance and managed/scaffold/validate artifacts.
2. Implement Relay validators and deterministic `decisions.json` and
   `activity.json` generation with privacy and legacy fixtures.
3. Implement Observatory aggregation and the first organization dashboard.
4. Pilot Identity with a provenance-preserving migration map.
5. Roll out grouped, reviewable repository pull requests.
