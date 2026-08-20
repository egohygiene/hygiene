---
schema: aether.architecture-document/v1
id: hygiene-meta
title: Hygiene Meta
kind: architecture-document
version: 0.1.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
governed_by:
  - architecture-meta
depends_on:
  - hygiene-epistemology
  - hygiene-ai-constitution
related:
  - hygiene-purpose
  - hygiene-vision
  - hygiene-principles
  - hygiene-pillars
supersedes: []
---

# Hygiene Meta Architecture

## Architecture-system overview

Hygiene's architecture is an 18-document graph materialized from the Aether architecture specifications. Each document owns one bounded concern. This index maps ownership and relationships without replacing the documents themselves.

## Document inventory

| Artifact | Path | Category | Status | Governing specification | Upstream dependencies |
| --- | --- | --- | --- | --- | --- |
| hygiene-purpose | [PURPOSE.md](PURPOSE.md) | Identity | provisional | architecture-purpose | — |
| hygiene-vision | [VISION.md](VISION.md) | Identity | provisional | architecture-vision | hygiene-purpose |
| hygiene-principles | [PRINCIPLES.md](PRINCIPLES.md) | Identity | provisional | architecture-principles | hygiene-purpose, hygiene-vision |
| hygiene-pillars | [PILLARS.md](PILLARS.md) | Identity | provisional | architecture-pillars | hygiene-purpose, hygiene-vision, hygiene-principles |
| hygiene-manifesto | [MANIFESTO.md](MANIFESTO.md) | Identity | provisional | architecture-manifesto | hygiene-purpose, hygiene-vision, hygiene-principles, hygiene-pillars |
| hygiene-epistemology | [EPISTEMOLOGY.md](EPISTEMOLOGY.md) | Meta | provisional | architecture-epistemology | hygiene-purpose, hygiene-principles |
| hygiene-ai-constitution | [AI_CONSTITUTION.md](AI_CONSTITUTION.md) | Meta | provisional | architecture-ai-constitution | hygiene-purpose, hygiene-vision, hygiene-principles, hygiene-epistemology |
| hygiene-ontology | [ONTOLOGY.md](ONTOLOGY.md) | Domain | provisional | architecture-ontology | hygiene-purpose, hygiene-vision, hygiene-principles, hygiene-epistemology |
| hygiene-personal-model | [PERSONAL_MODEL.md](PERSONAL_MODEL.md) | Domain | provisional | architecture-personal-model | hygiene-purpose, hygiene-vision, hygiene-principles, hygiene-epistemology, hygiene-ontology |
| hygiene-foundations | [FOUNDATIONS.md](FOUNDATIONS.md) | Foundation | provisional | architecture-foundations | hygiene-purpose, hygiene-principles, hygiene-epistemology |
| hygiene-system | [SYSTEM.md](SYSTEM.md) | Foundation | provisional | architecture-system | hygiene-foundations, hygiene-ontology |
| hygiene-architecture | [ARCHITECTURE.md](ARCHITECTURE.md) | Foundation | provisional | architecture-architecture | hygiene-foundations, hygiene-system |
| hygiene-methodology | [METHODOLOGY.md](METHODOLOGY.md) | Foundation | provisional | architecture-methodology | hygiene-principles, hygiene-epistemology, hygiene-ai-constitution, hygiene-foundations, hygiene-architecture |
| hygiene-design | [DESIGN.md](DESIGN.md) | Experience | provisional | architecture-design | hygiene-purpose, hygiene-vision, hygiene-principles, hygiene-personal-model |
| hygiene-design-system | [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) | Experience | provisional | architecture-design-system | hygiene-personal-model, hygiene-design |
| hygiene-decisions | [DECISIONS.md](DECISIONS.md) | Governance | provisional | architecture-decisions | hygiene-principles, hygiene-epistemology, hygiene-foundations, hygiene-system, hygiene-architecture |
| hygiene-roadmap | [ROADMAP.md](ROADMAP.md) | Foundation | provisional | architecture-roadmap | hygiene-vision, hygiene-pillars, hygiene-architecture, hygiene-decisions |
| hygiene-meta | [META.md](META.md) | Meta | provisional | architecture-meta | hygiene-epistemology, hygiene-ai-constitution |

## Relationship graph

```mermaid
flowchart TD
  PURPOSE --> VISION --> PRINCIPLES --> PILLARS --> MANIFESTO
  PURPOSE --> EPISTEMOLOGY --> AI[AI Constitution]
  PRINCIPLES --> EPISTEMOLOGY
  EPISTEMOLOGY --> ONTOLOGY --> PERSONAL[Personal Model]
  PRINCIPLES --> FOUNDATIONS
  EPISTEMOLOGY --> FOUNDATIONS
  FOUNDATIONS --> SYSTEM --> ARCHITECTURE --> METHODOLOGY
  PERSONAL --> DESIGN --> DS[Design System]
  ARCHITECTURE --> DECISIONS --> ROADMAP
  PILLARS --> ROADMAP
  AI --> META
  EPISTEMOLOGY --> META
```

## Ownership map

- Identity documents own why the repository exists, its desired future, decision heuristics, strategic capabilities, and public commitments.
- Meta documents own knowledge integrity, AI authority, and navigation of this document system.
- Domain documents own canonical concepts and bounded human assumptions.
- Foundation documents own invariants, logical systems, structure, working method, and strategic evolution.
- Experience documents own intended experience and reusable semantic design language.
- Governance owns accepted architectural decisions and historical lineage.

## Reading order

1. PURPOSE, VISION, and PRINCIPLES.
2. EPISTEMOLOGY and ONTOLOGY.
3. FOUNDATIONS, SYSTEM, and ARCHITECTURE.
4. PERSONAL_MODEL, DESIGN, and DESIGN_SYSTEM when evaluating human-facing surfaces.
5. AI_CONSTITUTION before delegating consequential work.
6. DECISIONS and ROADMAP for accepted constraints and evolution.

## Authoring order

Follow the dependency graph from purpose through identity and evidence, then domain and foundations, experience, governance, roadmap, and finally this META index.

## Lifecycle and validation

All documents begin as provisional and require human review before becoming active. Validation covers frontmatter, stable identifiers, links, graph acyclicity, ownership boundaries, evidence labels, Markdown structure, and agreement with repository reality.

## Change propagation

A material upstream change triggers review of every downstream node. Implementation changes first update the owning specification or decision when they alter durable behavior; META changes whenever inventory or relationships change.

## Gaps and omissions

- No document in this set is intentionally omitted because Hygiene has repository, automation, human, AI, and public or documentation surfaces that justify the complete reference set.
- Target systems remain provisional where implementation evidence is absent.
- Repository-local schemas and automated graph validation should be added or connected to Aether in a later conformance pass.

## Evidence and uncertainty

- **Observed:** The repository README establishes the intended boundary as the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; significant implementation remains incomplete.
- **Decided for this draft:** The repository owns the bounded concern described here and participates through versioned contracts.
- **Proposed:** Target systems and later roadmap phases remain proposals until accepted and implemented.
- **Open question:** Which parts of this draft should become active in the first independently versioned release?
