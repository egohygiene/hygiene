---
schema: aether.architecture-document/v1
id: hygiene-system
title: Hygiene System
kind: architecture-document
version: 0.1.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
governed_by:
  - architecture-system
depends_on:
  - hygiene-foundations
  - hygiene-ontology
related:
  - hygiene-purpose
  - hygiene-vision
  - hygiene-principles
  - hygiene-pillars
supersedes: []
---

# Hygiene System

## Purpose and scope

This document identifies Hygiene's logical systems and responsibilities. It answers what the major systems do; [ARCHITECTURE.md](ARCHITECTURE.md) owns their structural organization and dependency rules.

## Canonical control-plane sources

- [Holistic architecture](docs/ecosystem/ARCHITECTURE.md)
- [Repository catalog](docs/ecosystem/REPOSITORY_CATALOG.md)
- [Migration plan](docs/ecosystem/MIGRATION_PLAN.md)
- [Agent context](docs/ecosystem/AGENT_CONTEXT.md)
- [Detailed architecture decisions](docs/decisions/README.md)

These sources supply the data and decisions used by the logical systems below.

## System inventory

| System | State | Responsibility |
| --- | --- | --- |
| Ecosystem architecture | Target | Owns its bounded portion of the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; exposes explicit inputs, outputs, failure states, and evidence. |
| Repository registry | Target | Owns its bounded portion of the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; exposes explicit inputs, outputs, failure states, and evidence. |
| Ontology and schemas | Target | Owns its bounded portion of the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; exposes explicit inputs, outputs, failure states, and evidence. |
| Cross-repository ADRs | Target | Owns its bounded portion of the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; exposes explicit inputs, outputs, failure states, and evidence. |
| Policy catalog | Target | Owns its bounded portion of the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; exposes explicit inputs, outputs, failure states, and evidence. |
| Migration model | Target | Owns its bounded portion of the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; exposes explicit inputs, outputs, failure states, and evidence. |
| Landscape projection | Target | Owns its bounded portion of the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; exposes explicit inputs, outputs, failure states, and evidence. |

## External systems

- every organization repository
- Holon generation
- Pace conformance
- Observatory metrics
- .github public coordination

External systems are integrations, not hidden implementation units. Each requires version, authentication, availability, data, error, and replacement boundaries appropriate to its risk.

## System interactions

Inputs enter through an adapter or validated contract, move through domain systems, produce artifacts and diagnostics, and leave through a stable interface. Evidence flows back to validation, review, and future decisions.

## Failure model

Systems fail closed at destructive, publication, privacy, and security boundaries. Partial results identify coverage and remain distinguishable from complete success.

## Evidence and uncertainty

- **Observed:** The repository README establishes the intended boundary as the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; significant implementation remains incomplete.
- **Decided for this draft:** The repository owns the bounded concern described here and participates through versioned contracts.
- **Proposed:** Target systems and later roadmap phases remain proposals until accepted and implemented.
- **Open question:** Which parts of this draft should become active in the first independently versioned release?
