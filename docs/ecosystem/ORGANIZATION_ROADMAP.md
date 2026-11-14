# Organization roadmap and repository composition

Proposed contract: `egohygiene.organization-roadmap/v1`, version
`1.0.0-alpha.1`. Tracking: [#60](https://github.com/egohygiene/hygiene/issues/60).
Decision: [ADR-0023](../decisions/ADR-0023-organization-roadmap-composition.md),
proposed with null approval. This proposal defines strategy records and reference
checks; implementation and merge do not ratify priority or activate enforcement.

## Canonical source and ownership

The canonical organization strategy source is
[`organization/roadmap.v1.json`](../../organization/roadmap.v1.json).
[`organization/ROADMAP.md`](../../organization/ROADMAP.md) is its deterministic
human view, separately located from [Hygiene's own roadmap](../../ROADMAP.md).
Edit the JSON and regenerate the view in the same change. The
[schema](../../schemas/organization-roadmap.v1.schema.json) defines its versioned
shape; the reference checker adds identity, provenance and graph invariants.

| Concern | Canonical owner |
| --- | --- |
| Organization initiatives, strategic horizon, composition and policy | Hygiene, this source |
| Repository capability strategy and local roadmap IDs | Each repository's `ROADMAP.md` |
| Executable work, acceptance, delivery dependencies | GitHub issues/PRs in their owning repository |
| Consequential rationale and human disposition | Repository and organization ADRs |
| Current Now/Next/Later/Parked focus proposals | [Pace #25](https://github.com/egohygiene/pace/issues/25) |
| Portable authoring guidance | Aether |
| Reusable collection, validation orchestration and projection mechanics | Relay |
| Conformance semantics and normalized reports | EgoLint |
| Organization observations and reporting | Observatory |
| New-repository materialization and reviewed existing-fleet adoption | Holon and Pace, respectively |
| Organization UI/export composition and final hosting | Website and selected `.github` publisher, respectively |

This contract neither creates a second repository registry nor transfers any
execution, credentials, publication or adoption authority. Strategic reference
links to immutable source or navigational `main` URLs are not runtime dependencies.

## Stable initiative identity and composition

`ORG-I001` and subsequent `ORG-I` numeric IDs belong to organization strategy;
they never replace repository IDs such as `HYG-Q03` or `AET-Q07`. IDs are
permanent and are not renumbered when priority changes. Each record carries an
owner, outcome, horizon, declared state, assertion, freshness and provenance.

`repository_nodes` compose only repository identity, stable local key,
applicability and provenance. They copy no repository outcome, issue body or ADR
rationale. One initiative can reference many nodes; a node can contribute to
several initiatives. Repository-only work needs no organization initiative, and
an undecomposed initiative may have an empty node list. Absence is not a claim
that a repository is inactive or that collection is complete.

`active`, `archived` and `not_applicable` participation describe the explicitly
referenced node. They do not change canonical repository lifecycle. Archived or
inapplicable references remain navigable history and cannot grant readiness.

`depends_on` points from dependent to prerequisite initiative. Independent
branches of that acyclic graph may proceed concurrently within their own
acceptance gates; a horizon is not an execution lock. `supersedes` and
`superseded_by` are reciprocal, acyclic links. A superseded record remains in
source with its original identity. `--previous` additionally rejects lost IDs
and authoritative changes without a new review reference.

## Intent, evidence and human review

Horizons are `now`, `next`, `later` and `maybe`. States are `proposed`, `planned`,
`ready`, `active`, `blocked`, `paused`, `completed`, `deferred`, `superseded`,
`optional` and `unknown`. Freshness is independent: `current`, `stale`, `unknown`
or `not_applicable`. A stale observation never becomes fresh because a renderer
ran. Completed implementation does not automatically change strategic intent.

Assertions reuse Repository Intelligence's `authoritative`, `inferred` and
`unknown` vocabulary. The initial organization source is entirely **inferred**:
its horizons and dependencies are reviewable suggestions grounded in current
repository strategy and this implementation task. They are not newly accepted
organization priorities.

An authoritative initiative requires an explicit `manual` provenance source
linking a durable maintainer review comment, included in the record's provenance
and `review` reference. Authoritative completion also requires a linked check,
release or deployment source. These structural checks do **not** authenticate
the account, review contents or actual delivery. The responsible human must
review the exact diff and evidence before authoritative admission. Agents may
suggest edits, mark observed freshness and reconcile evidence; they must never
manufacture human review or promote inferred relationships on their own.

Governed fields, including horizon, owner, composition, dependencies and state,
need renewed review when changed authoritatively. A source observation, commit
count, successful test or focus-queue ranking does not supply that review. A
new proposal can clear the review and return its assertion to `inferred` while
retaining lineage. Contract lifecycle remains proposed/null approval here.

## Repository Intelligence compatibility

The schema references the existing alpha.2 Intelligence **source** and **event**
definitions rather than introducing a second provenance dialect. Sources retain
their owner, full immutable revision or explicit null, URL, original observation
clock, visibility, assertion and freshness. `links` reuse `tracks`, `informs`,
`evidences` and `releases`; dependencies and supersession use the existing
`depends-on` and `supersedes` relationship semantics.

An organization initiative maps to the existing roadmap entity identity
`ri:egohygiene/hygiene:roadmap-step:ORG-I001`, with organization scope in
`extensions.egohygiene.organization-roadmap`. Referenced repository steps retain
their own `ri:<repository>:roadmap-step:<key>` identity. Repository-to-initiative
contribution uses `implements`; issue, ADR, release and evidence sources remain
references to their canonical owners. Do not invent new entity kinds in an old
Intelligence schema or fill uncollected source domains with empty success.

`events` reuse `roadmap_step.created` and `roadmap_step.status_changed`, original
occurrence and recording clocks, subject identity and provenance. This bounded
reference accepts proposed/unknown events with null actors and no inferred
field-change claims. Actual authoritative history belongs in the established
Intelligence collector. The initial source emits no invented historical events.

Rich strategic state remains in the namespaced extension during projection:
`completed` maps to `complete`, `proposed` to `planned`, and `paused`, `optional`
and `unknown` must not be strengthened into current readiness. A future collector
must preserve original state and freshness; it cannot derive initiative
acceptance from related issue/PR activity. Production graph integration remains
owned by Relay/Observatory and the organization `/roadmap/` consumer.

## Privacy before projection

Public canonical source contains public facts only. A restricted source may be
processed within its authorized boundary, but a public view is filtered **before**
rendering: remove restricted sources, participation, links and events; remove
restricted initiatives and any initiative whose dependency/supersession closure
would disclose them. Recompute source reachability after filtering. Publish no
restricted names, keys, repository paths, locators, placeholder counts or actor
identities. A view never claims an exhaustive organization inventory.

Mixed synthetic fixtures exercise private participation; they are labeled
synthetic and contain no actual private topology. Visibility declarations still
require content review: no parser can establish that prose was correctly
classified, or sanitize an author deliberately putting private facts in a public
title. Never feed restricted output into a public artifact before review.

## Validation, rollout and recovery

```bash
python3 tools/organization_roadmap.py validate
python3 tools/organization_roadmap.py public
python3 tools/organization_roadmap.py render > organization/ROADMAP.md
python3 tools/organization_roadmap.py check-generated
python3 -I -m unittest discover -s tests -p test_organization_roadmap.py -v
python3 -I tools/check_contracts.py
```

For a reviewed change, additionally pass `--previous` with its actual immutable
base source. The pure helper reads bounded explicit files only, performs no
network request, changes no strategy and prints generic refusal diagnostics.
It does not discover missing repository IDs or independently prove the source
revision contains them; initial bindings were checked against the exact source
roadmaps. Downstream collection must repeat that owner check.

Start in observe mode with the proposed source, review initiative placement and
representative consumer mappings, then select a compatible version in each
consumer. No fleet activation, package publication or platform deployment is
part of this source change. Roll back the selected contract/view together while
retaining initiative IDs, prior review evidence and supersession history.
