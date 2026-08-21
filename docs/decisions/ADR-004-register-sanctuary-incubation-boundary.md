---
schema: egohygiene.architecture-decision/v1
id: ADR-004
title: Register Sanctuary as the bounded incubation owner
status: proposed
date: 2026-08-21
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/.github/issues/12
pull_request: null
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/.github
  - egohygiene/empathy
  - egohygiene/holon
  - egohygiene/hygiene
  - egohygiene/pace
  - egohygiene/sanctuary
affected_contracts:
  - egohygiene.repository-context/v1
  - egohygiene.dependency-boundary-register/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/.github/issues/12
    description: Organization intake defining Sanctuary's purpose, minimum baseline, lifecycle evidence, graduation, and control-plane boundaries.
  - type: pull_request
    url: https://github.com/egohygiene/sanctuary/pull/1
    description: Merged bootstrap with Sanctuary's provisional local manifest, lifecycle, provenance, validation, and explicit non-goals.
  - type: pull_request
    url: https://github.com/egohygiene/empathy/pull/66
    description: Merged Empathy decision establishing the strict golden baseline and routing general incubation to Sanctuary.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/9
    description: Organization stabilization audit that proposed Sanctuary while preserving a separate canonical architecture owner.
exceptions: []
approval: null
---

# ADR-004: Register Sanctuary as the bounded incubation owner

## Context

Empathy historically combined the golden repository baseline with general
incubation. Its merged foundation decision now makes Empathy the strict golden
baseline and directs unfinished or ownerless work to Sanctuary. The public
`egohygiene/sanctuary` repository now exists, and its merged bootstrap defines a
provisional local lifecycle, manifest, validator, and trust boundary.

Hygiene's accepted architecture anticipated Sanctuary but still lists Empathy
as a bounded incubator and omits Sanctuary from the observed catalog. The
canonical architecture therefore does not match the live 27-repository
organization or its accepted local ownership split.

## Decision

Register `egohygiene/sanctuary` in the architecture and control plane as the
bounded incubation owner for unfinished or ownerless public work.

Sanctuary owns incubation manifests, source provenance, lifecycle evidence,
explicit baseline exceptions, candidate destinations, and reviewed graduation,
archival, or rejection proposals. It does not own organization-wide policy,
canonical repository templates, stable dependencies, secrets or private data,
generic artifact archives, or durable implementation after graduation.

Empathy remains the strict golden baseline, golden consumer, and integration
testbed. Historical Empathy staging remains migration evidence; it does not
authorize new general incubation there.

The `sanctuary.incubation/v1` schema remains a Sanctuary-local provisional
contract. This decision registers the repository boundary without silently
promoting every local state or field into organization-wide canonical policy.

Stable repositories must not depend on mutable Sanctuary source. Graduation
requires an explicit durable owner, immutable provenance, and consumption from
that owner's versioned contract. `.github` may route ownerless work into
Sanctuary. Holon may later materialize an approved incubator blueprint, and
Pace may propose managed-baseline updates, but neither may silently create,
modify, graduate, archive, or reject an incubation.

## Alternatives considered and rejected

### Keep general incubation in Empathy

Rejected because it conflicts with Empathy's merged strict-baseline decision
and recreates ambiguous ownership.

### Make Sanctuary the canonical template or organization policy owner

Rejected. Empathy owns the strict baseline and Hygiene owns organization
policy. Sanctuary needs local flexibility while the process is proven.

### Create repositories directly for every experiment

Rejected because an implementation location would be chosen before durable
ownership and standalone value are established.

### Treat Sanctuary as a permanent shared-source monorepo

Rejected because graduated implementations need one durable owner and stable,
versioned consumer contracts.

## Consequences and tradeoffs

- The observed catalog grows from 26 to 27 repositories.
- Empathy loses general incubation from its canonical ownership list.
- Sanctuary gains explicit intake and graduation relationships without
  becoming a production dependency.
- Maintainers accept manifest and review overhead in exchange for preserved
  provenance and understandable terminal decisions.
- A later decision may standardize the lifecycle only after real incubation
  evidence demonstrates which fields and states are durable.

## Replacement or exit strategy

If bounded incubation does not justify a permanent repository, active work is
routed through explicit ownership decisions and terminal manifests become a
read-only provenance archive. Hygiene then retires the catalog entry through a
replacement ADR. No implementation may be copied or deleted without preserving
source, license, decision, and recovery evidence.

## Follow-up work

- Prove one small, public, license-compatible incubation end to end.
- Generate Sanctuary's pinned repository context from this reviewed catalog.
- Revisit organization-wide lifecycle standardization only after that evidence
  exists.
