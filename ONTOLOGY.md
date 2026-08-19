---
schema: aether.architecture-document/v1
id: hygiene-ontology
title: Hygiene Ontology
kind: architecture-document
version: 0.1.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
governed_by:
  - architecture-ontology
depends_on:
  - hygiene-purpose
  - hygiene-vision
  - hygiene-principles
  - hygiene-epistemology
related:
  - hygiene-pillars
  - hygiene-manifesto
  - hygiene-ai-constitution
  - hygiene-personal-model
supersedes: []
---

# Hygiene Ontology

## Domain scope

Hygiene models the concepts needed for give the Ego Hygiene organization one coherent source of truth for what exists, who owns it, how it relates, and which rules govern it. The ontology names conceptual entities and relationships; it is not a source-code class model, API schema, or database design.

## Canonical concepts

| Concept | Meaning |
| --- | --- |
| Organization | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Plane | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Repository | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Capability | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Ownership | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Policy | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Contract | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Dependency | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Lifecycle | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |
| Conformance | A canonical concept in the Hygiene domain whose exact fields belong to specifications or schemas, not this ontology. |

## Core relationships

- A repository or person provides source context to one or more domain artifacts.
- A specification constrains how an artifact is interpreted or produced.
- A plan separates proposed action from execution.
- Evidence supports a claim; a decision authorizes a durable direction.
- Provenance connects derived artifacts to their inputs and processing context.
- A consumer integrates through an explicit interface rather than internal structure.

## Boundaries

- Conceptual identity is distinct from filesystem path, database identifier, or display label.
- Observed state is distinct from desired state.
- Proposed relationships are not accepted facts.
- Neighboring repositories retain ownership of their domain concepts.

## Evidence and uncertainty

- **Observed:** The repository README establishes the intended boundary as the canonical ecosystem architecture, ontology, repository registry, cross-repository decisions, and platform-policy control plane; significant implementation remains incomplete.
- **Decided for this draft:** The repository owns the bounded concern described here and participates through versioned contracts.
- **Proposed:** Target systems and later roadmap phases remain proposals until accepted and implemented.
- **Open question:** Which parts of this draft should become active in the first independently versioned release?
