---
schema: aether.architecture-document/v1
id: hygiene-decisions
title: Hygiene Decisions
kind: architecture-document
version: 0.3.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-09-12
governed_by:
  - architecture-decisions
depends_on:
  - hygiene-principles
  - hygiene-epistemology
  - hygiene-foundations
  - hygiene-system
  - hygiene-architecture
related:
  - hygiene-purpose
  - hygiene-vision
  - hygiene-pillars
  - hygiene-manifesto
  - hygiene-architecture-decision-policy
supersedes: []
---

# Hygiene Decisions

## Purpose

This root file is the human navigation index for Hygiene decisions. Detailed
organization records live under [docs/decisions/](docs/decisions/README.md),
with one canonical detailed record per decision. The index summarizes and links;
it does not duplicate full rationale.

## Decision index

| ID | Decision | Status | Record |
| --- | --- | --- | --- |
| ADR-0001 | Accept holistic organization architecture v0.1 | Accepted | [Detailed record](docs/decisions/ADR-0001-holistic-architecture-v0.1.md) |
| ADR-002 | Establish an organization ADR and delivery-history contract | Accepted | [Detailed record](docs/decisions/ADR-002-organization-adr-and-delivery-history.md) |

## Accepted governance contract

ADR-002 establishes the accepted organization
[ADR policy](docs/decisions/POLICY.md),
[front matter schema](schemas/architecture-decision.v1.schema.json),
[migration guide](docs/decisions/MIGRATION.md), and
[validation plan](docs/decisions/VALIDATION.md). Its explicit maintainer
authority and pinned implementation revision are recorded in the
[ratification evidence](docs/decisions/RATIFICATION.md).

New significant organization decisions receive a stable identifier, explicit
status, evidence, alternatives, consequences, review triggers, and a detailed
record. Superseding records preserve links to the decisions they replace.

GitHub issues coordinate implementation. Proposals remain proposals until an ADR
is accepted. Historical context is preserved rather than rewritten to match
later understanding.

## Pending decisions

- Organization ontology schema and nested repository ontology contract.
- Architecture-corpus activation and conformance policy after Aether stabilizes.
- Managed and self-hosted boundaries for the organization compiler.
- Firmament creation gate and infrastructure ownership.
- Public landscape publication and synchronization ownership.

## Evidence and uncertainty

- **Observed:** ADR-0001 and the ecosystem architecture are present on the
  default branch.
- **Accepted:** ADR-002 and policy v1.1.0 were approved by maintainer `szmyty`
  on 2026-09-12 at the pinned implementation revision.
- **Open question:** Downstream rollout and repository-local migration remain
  separately reviewed implementation work.

## Validation

The index must resolve every detailed record, use each decision identifier once,
and remain consistent with the repository catalog and holistic architecture.
Hygiene provides reference contract checks. EgoLint owns semantic validation
and Relay owns reusable CI orchestration and projections; this index does not
claim those downstream systems are complete merely because the policy is
accepted.
