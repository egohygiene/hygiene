---
schema: egohygiene.architecture-decision/v1
id: ADR-0019
title: Compose canonical documentation locations with existing presentation and continuity
status: proposed
date: "2026-11-12"
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/64
pull_request: null
related:
  - ADR-0002
  - ADR-0006
  - ADR-0008
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/aether
  - egohygiene/empathy
  - egohygiene/holon
  - egohygiene/identity
  - egohygiene/egolint
  - egohygiene/relay
  - egohygiene/observatory
  - egohygiene/pace
affected_contracts:
  - egohygiene.repository-documentation-profile/v1
  - egohygiene.repository-documentation-inventory/v1
  - egohygiene.repository-documentation-assessment/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/64
    description: Original documentation-location requirements and October 17 architecture/agent checkpoint; no policy activation.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/ae4e4c1399aeed3b82c97959c82741892c230fbf/catalog/repository-presentation-profile.json
    description: Unchanged proposed presentation slots, applicability, claims and ownership.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/ae4e4c1399aeed3b82c97959c82741892c230fbf/catalog/repository-continuity-policy.json
    description: Existing observe-only applicability and draft Aether continuity composition.
  - type: documentation
    url: https://github.com/egohygiene/empathy/blob/058d92a0f8c970f98a58d446408716936e593c99/foundation/catalog.json
    description: Actual catalog 2.0 root architecture and selected agent-context surface; CONTINUITY/CLAUDE catalog gap remains.
  - type: documentation
    url: https://github.com/egohygiene/holon/blob/c91565ce1d58b0882b77d3d01ab46f15b457e573/blueprints/repository-presentation/blueprint.json
    description: Existing versioned generated README region and immutable owner inputs remain unchanged.
exceptions: []
approval: null
---

# ADR-0019: Compose canonical documentation locations with existing presentation and continuity

## Context

Hygiene #64 asks for predictable durable documentation and useful entry points
without wholesale relocation or competing README, agent or architecture policy.
Existing repositories have useful canonical root and nested locations. Empathy's
current catalog is 2.0.0, not the issue's historical 1.1.0, and its current
required-file selection does not yet implement the whole proposed continuity
composition. Holon already owns a non-destructive generated presentation region.
Presentation and continuity remain proposed; accepted ADR policy does not
ratify either. Aether owns document/continuity semantics and authoring.

## Decision

Propose a versioned Hygiene location/navigation profile composing exact existing
presentation and continuity bytes and pure applicability resolvers. Explicitly
selected architecture normally uses `docs/architecture/` with root navigation;
declared legacy root sources and repository-owned exception path maps preserve
established locations. No universal 18-file corpus or arbitrary README word
limit is selected. A regular optional Claude compatibility file imports shared
`AGENTS.md`; it does not eagerly import the architecture corpus.

Expose closed observation and local assessment contracts plus a small optional
standard-library reference. Declared inventory is not actual filesystem,
public-source, link, content, human-approval or enforcement proof. Existing owners
retain production validation, scaffolding, orchestration and reviewed adoption.
Keep the profile proposed/observe and approval null; source implementation does
not activate it. A later Aether reconciliation and one Empathy pilot precede
broader migration.

## Alternatives considered and rejected

- Requiring every document or moving the fleet during policy authoring would
  erase class applicability, historical links and review boundaries.
- Treating root and nested copies as coequal authority would permit drift;
  navigation must point to one selected canonical identity instead.
- A new README template or continuity protocol would duplicate existing owners;
  compose their exact contracts and preserve their lifecycle instead.
- Turning long agent transcripts into README/CONTINUITY would mix disposable
  notes, durable proof and current state, with avoidable privacy exposure.
- Enforcing ASCII-only canonical paths would require unjustified renames of
  existing space/Unicode filenames; retain safe literal relative names.

## Consequences and tradeoffs

Maintainers can distinguish entry points, canonical details, generated views,
current handoffs, retained evidence and disposable scratch. The explicit path
map and separate lifecycle vocabularies cost some inventory work, but prevent
silent upgrades and invented applicability. A local reference can review
observations without acquiring or publishing consumer content; real production
discovery/content checks and exceptions still need owner evidence.

## Implementation and evidence links

The [policy](../ecosystem/REPOSITORY_DOCUMENTATION.md), versioned profile, three
schemas, synthetic examples and reference adapter implement the bounded source
seam. The [migration map](../migration/2026-11-12-documentation-layout.md) records
current immutable inputs and downstream obligations. Aether authoring 2.1.0 at
`dc8a16851f452763ef4f7fbe4bf057d4500b1921` and accepted Hygiene policy 1.2.0
were read before drafting. Synthetic cases and regression scenarios are authored
but unexecuted. Runtime, helper/test/build/CI, content/link and consumer-pilot
qualification are deferred; no passing or historical count is invented.

The merge integration selects exact corrected merged Hygiene owner source
`ae4e4c1399aeed3b82c97959c82741892c230fbf`, including #91's explicit/current
assessment clock and #89's current-evidence witness repair. The machine profile,
reference and closed output schema bind those exact bytes and retain the
owner-returned assessment date/mode. Presentation composition remains
requirements-only; it does not validate a passing witness or promote any
policy, ADR or consumer lifecycle.

## Replacement or exit strategy

Consumers remain on existing paths/pins until a reviewed compatible selection.
A successor changes the profile/schema/helper together, retains stable source
identities and historical citations, and documents aliases plus rollback. A
rollback restores prior reviewed paths, bytes and ownership state while
preserving later local edits. It cannot delete historical decisions, infer
approval, rewrite history or waive Hygiene #47's separate source-admission hold.

## Follow-up work

Hygiene #64 retains the Aether reconciliation and Empathy pilot phases. Inventory
actual specs/skills, catalog artifacts, blueprint state, validators, collectors,
renderers, site maps and links before any move. Reuse existing Holon #24,
Identity #54 and Pace adoption concerns as scoped in the migration map. Human
review of this proposal, separate upstream stability/continuity promotion,
required owner qualification and reviewed consumer adoption remain outstanding.
