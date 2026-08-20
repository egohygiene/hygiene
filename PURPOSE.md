---
schema: aether.architecture-document/v1
id: hygiene-purpose
title: Hygiene Purpose
kind: architecture-document
version: 0.1.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
governed_by:
  - architecture-purpose
depends_on:
  []
related:
  - hygiene-vision
  - hygiene-principles
  - hygiene-pillars
  - hygiene-manifesto
supersedes: []
---

# Hygiene Purpose

## Purpose statement

Hygiene exists to give the Ego Hygiene organization one coherent source of truth for what exists, who owns it, how it relates, and which rules govern it.

## Need

organization architecture otherwise fragments across repositories, diagrams, conversations, issues, and implementation-specific assumptions.

## Beneficiaries

- organization maintainers
- repository agents
- platform tools
- contributors navigating the ecosystem

## Enduring value

The enduring value is a trustworthy, portable capability that remains useful when its implementation, delivery channel, or surrounding platform changes.

## Scope boundaries

Hygiene owns the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane. It does not absorb neighboring repositories, treat temporary implementation choices as purpose, or claim authority beyond its explicit contracts.

## Evidence and uncertainty

- **Observed:** The repository README establishes the intended boundary as the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; significant implementation remains incomplete.
- **Decided for this draft:** The repository owns the bounded concern described here and participates through versioned contracts.
- **Proposed:** Target systems and later roadmap phases remain proposals until accepted and implemented.
- **Open question:** Which parts of this draft should become active in the first independently versioned release?

## Open questions

- Which beneficiary needs require direct research before this document can become active?
- Which current features are incidental and should remain outside the enduring purpose?
