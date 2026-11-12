---
schema: egohygiene.architecture-decision/v1
id: ADR-0016
title: Keep public repository admission separate from architecture and checkpoint execution
status: proposed
date: "2026-11-09"
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/36
pull_request: null
related:
  - ADR-0002
  - ADR-0005
  - ADR-0008
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/pace
  - egohygiene/observatory
  - egohygiene/relay
affected_contracts:
  - egohygiene.repository-public-catalog/v1
  - egohygiene.repository-public-discovery/v1
  - egohygiene.repository-public-drift/v1
  - egohygiene.organization-checkpoints/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/36
    description: Public-only discovery, canonical catalog reconciliation, freshness, recurrence and checkpoint ownership scope.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/specs/quality/auditor.spec.md
    description: Exact approved portable read-only auditor 2.0.0; Hygiene composes applicability rather than replacing its protocol.
  - type: documentation
    url: https://github.com/egohygiene/antidote/blob/34f7653469002c8f19c9adc87d4bfdcecc0eda33/ARCHITECTURE.md
    description: Owner-declared research workspace and local instrument boundaries.
  - type: documentation
    url: https://github.com/egohygiene/civics/blob/c95596afc206e38b3c5b1f80a3ccbae46326daa8/ARCHITECTURE.md
    description: Owner-declared static civic knowledge graph and public/private evidence boundaries.
exceptions: []
approval: null
---

# ADR-0016: Keep public repository admission separate from architecture and checkpoint execution

## Context

The canonical catalog retains an old observation boundary and the historical
website identity. Public inventory consumers need an explicit reviewed roster,
while full authored role catalogs can contain non-public declarations. A fresh
provider observation establishes identity and visibility; it cannot approve a
role, infer a lifecycle, certify source coverage or authorize publication.

## Decision

Propose a public-only projection of the existing canonical catalog, with stable
provider IDs, declared historical aliases and exact observation provenance.
Filter protected rows before identities, validation, duplicate diagnostics or
digests. Hash only admitted public fields and isolate deterministic catalog
bytes from run receipts and process clocks. Discovery reports drift and never
silently mutates the source registry.

Preserve role declarations and dated first gates independently. Source-backed
owner responsibilities may be reconciled under the existing six-plane model;
undeclared lifecycle or next-gate facts remain unknown. Public identity admission
does not require fabricating those facts.

The proposed organization-checkpoint profile composes Aether auditor 2.0.0 at
its recorded immutable source/digest. It defines a weekly default, event and
on-demand triggers, explicit freshness, retention and baseline requirements,
public privacy boundaries and owner handoffs. It installs no scheduler or
provider authority and retains its proposed lifecycle.

## Alternatives considered and rejected

- Publishing a full role catalog or its raw digest can reveal protected topology.
- Promoting provider activity into architecture/maturity or human acceptance
  conflates distinct evidence questions.
- A second authored public registry would drift from the canonical catalog.
- A fixed organization total would become stale and could expose inferred gaps.

## Consequences and tradeoffs

Downstream consumers gain a reviewed source-admission artifact and deterministic
drift/freshness seam. They must pin the new public schema/helper/artifact together;
historical consumers retain their exact prior schema and producer pins. Unknown
role facets and unavailable checkpoint domains remain useful explicit states.
An archive or missing public identity does not authorize deletion or infer why
a repository disappeared. Execution and retention still need consumer adapters.

## Implementation and evidence links

The canonical catalog, derived public projection, offline inventory adapter,
owner schemas and checkpoint profile implement the bounded source seam. The
public endpoint observation and immutable owner documents supply the dated
evidence. Static schema/syntax and peer review are separate from unexecuted
adapter, regression, native, scheduled, hosted and publication acceptance.

## Replacement or exit strategy

Retain historical names as unambiguous declared aliases. Incompatible identity,
privacy or authority changes require a successor version and reviewed migration.
Revert a faulty catalog/projection change without rewriting prior artifacts,
source observations, ADR dispositions or recovery evidence. Failed collection
never replaces a valid comparison baseline.

## Follow-up work

Review the proposed profile and unknown lifecycle/next-gate source declarations.
Qualify executable parity, privacy/failure cases and consumer intake in the
deferred validation pass. Pace owns reconciliation proposals; Observatory owns
observation/reporting; Relay owns execution/retention. Actual human disposition
and final publication stay with their existing owners.
