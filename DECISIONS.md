---
schema: aether.architecture-document/v1
id: hygiene-decisions
title: Hygiene Decisions
kind: architecture-document
version: 0.1.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
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
supersedes: []
---

# Hygiene Decisions

## Purpose

This root file is the canonical decision index for Hygiene. Detailed cross-repository
records live under [docs/decisions/](docs/decisions/README.md), with one detailed
record per decision. The index does not duplicate their full rationale.

## Decision index

| ID | Decision | Status | Record |
| --- | --- | --- | --- |
| ADR-0001 | Accept holistic organization architecture v0.1 | Accepted | [Detailed record](docs/decisions/ADR-0001-holistic-architecture-v0.1.md) |

## Governance

New significant organization decisions receive a stable identifier, explicit
status, evidence, alternatives, consequences, review triggers, and a detailed
record. Superseding records preserve links to the decisions they replace.

GitHub issues coordinate implementation. Proposals remain proposals until an ADR
is accepted. Historical context is preserved rather than rewritten to match later
understanding.

## Pending decisions

- Organization ontology schema and nested repository ontology contract.
- Architecture-corpus activation and conformance policy after Aether stabilizes.
- Managed and self-hosted boundaries for the organization compiler.
- Firmament creation gate and infrastructure ownership.
- Public landscape publication and synchronization ownership.

## Evidence and uncertainty

- **Observed:** ADR-0001 and the ecosystem architecture are present on the default branch.
- **Proposed:** Later decisions listed above remain unaccepted.
- **Open question:** Which review gate promotes organization architecture documents from draft to active?

## Validation

The index must resolve every detailed record, use each decision identifier once,
and remain consistent with the repository catalog and holistic architecture.
