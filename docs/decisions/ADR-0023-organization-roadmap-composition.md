---
schema: egohygiene.architecture-decision/v1
id: ADR-0023
title: Compose organization strategy by stable repository roadmap references
status: proposed
date: "2026-11-14"
decision_scope: organization
visibility: public
owners: [egohygiene/hygiene]
issue: https://github.com/egohygiene/hygiene/issues/60
pull_request: null
related: [ADR-0002, ADR-0005, ADR-0016, ADR-0017]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/hygiene, egohygiene/aether, egohygiene/holon, egohygiene/empathy, egohygiene/.github, egohygiene/relay, egohygiene/pace, egohygiene/observatory]
affected_contracts: [egohygiene.organization-roadmap/v1]
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/60
    description: Organization strategy ownership, reference composition and privacy acceptance.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/ea2768d49a5953d7f710374fbf13bff880f44f91/docs/ecosystem/ARCHITECTURE.md
    description: Existing standalone, versioned-contract and control-plane owner boundaries.
exceptions: []
approval: null
---

# ADR-0023: Compose organization strategy by stable repository roadmap references

## Context

Repository roadmaps and execution queues already exist, but they do not supply
one canonical organization strategy source. Copying all issues into a shared
roadmap would duplicate tactical ownership and convert experiments into apparent
commitments. Activity-derived priority would also confuse evidence with intent.

## Proposed decision

Keep organization strategy in Hygiene's `organization/roadmap.v1.json` with a
deterministic `organization/ROADMAP.md` view. Version stable initiative IDs,
horizons, state, provenance and composition links to repository-owned roadmap
nodes. Separate declared intent, freshness, inferred relationships and human
review; keep the initial initiative ordering proposed and inferred.

Reuse existing Intelligence source/event vocabulary and entity identities.
Preserve private participation only in authorized source and filter its complete
dependency closure before public rendering. Keep source, tactical work, ADRs,
Pace focus and UI publication in their existing owners.

## Alternatives and consequences

Putting the whole fleet into Hygiene's repository roadmap conflates policy-owner
evolution with organization strategy. A `.github` issue list alone supplies an
execution queue, but no durable strategic model. A second repository registry or
new incompatible Intelligence entity kind would duplicate existing authority.

Reference composition needs owner-ID verification and explicit stale/private
handling. A pure schema/helper proves structure and deterministic privacy
filtering, not account authenticity, complete collection, delivery or ratified
priority. Production graph collection and consumer adoption remain downstream.

## Validation, rollout and rollback

Synthetic scenarios exercise cross-repository and independent work, shared node
participation, dependencies, blocked/optional/stale state, lineage and private
participation. Adversarial controls reject cycles, dangling references,
fabricated authoritative placement and lost IDs. The existing complete contract
gate includes the new source and generated-view checks.

Human review of the exact strategy proposal precedes authoritative placement.
No enforcement or deployment is activated here. Restore the prior selected
source/view for rollback while preserving IDs and review history. This ADR stays
proposed with null approval regardless of implementation or merge state.
