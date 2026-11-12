# Documentation-location compatibility and migration map

Date: 2026-11-12. Scope: Hygiene [#64](https://github.com/egohygiene/hygiene/issues/64),
proposal [ADR-0019](../decisions/ADR-0019-repository-documentation-locations.md).
This is a source-backed preview, not an executed pilot or permission to move
files. [The policy](../ecosystem/REPOSITORY_DOCUMENTATION.md) and machine profile
remain proposed/observe. Existing canonical paths and all current pins remain.

## Reverified source checkpoints

| Source | Exact observation | Compatibility obligation |
| --- | --- | --- |
| Hygiene presentation | `ae4e4c1399aeed3b82c97959c82741892c230fbf`, profile alpha.1 SHA-256 `94132769e6cb9d4bc68abd6314bbe797ce6ab9abaad3bb424775d1157367d573` | Reuse slots, override order, evidence labels, Identity composition and local prose preservation. It remains proposed. |
| Hygiene continuity | Same revision, policy alpha.1 SHA-256 `2f694682df641f9c9741d79c7d23bca2ae5bd0d1e3aa6ca00cb31db17e0e2e2c` | Reuse pure applicability resolver and draft Aether pin `b7597301c4d22a9bcd580967b5753138bb368111`; observe does not become enforce. |
| Empathy foundation | `058d92a0f8c970f98a58d446408716936e593c99`, `foundation/catalog.json`, catalog `2.0.0` / schema `1.1.0` | Root `ARCHITECTURE.md` remains required/repository-owned; `AGENTS.md` is selected through `agent-context`; no CONTINUITY or CLAUDE artifact is currently in that catalog. The issue's historical `1.1.0` catalog observation is not current. |
| Holon presentation blueprint | `c91565ce1d58b0882b77d3d01ab46f15b457e573`, blueprint `1.0.0` | Pins Hygiene `cb2ed63425d29abada2d2bbb43a3b3e59d11aeb8` with historical `44e088…` profile bytes; Identity `3c2fd3141371b355628e81f66f63159f19d63338`; EgoLint `4efe92a2609b3384fcf3b5cda343a4f64d108824`. No implicit repin or blueprint upgrade. |
| Aether authoring | `dc8a16851f452763ef4f7fbe4bf057d4500b1921`, `create-decisions-document` `2.1.0`, architecture-decisions `3.1.0` | Draft authoring composes accepted Hygiene ADR policy `1.2.0` at `a05b14f8b9e2772124f879f818e09a911e996ad8`; four-digit IDs and human disposition remain unchanged. |

These statements come from immutable source inspection, not helper/scenario
execution. Consumer profile support, actual filesystem contents, deployment and
current live links are not established by a source pin. Hygiene ADR-0001's
separate metadata/approval/source-admission hold under #47 remains unchanged.

The Hygiene composition above deliberately selects the corrected merged owner
source after #91's assessment-clock and #89's presentation-witness fixes.
The machine profile binds both profile and helper SHA-256 values from that
exact revision. Original consumer selections, including Holon's historical
`44e088…` presentation bytes, remain independent and are not silently repinned.
The reference retains the continuity owner's explicit assessment date/mode and
selects presentation requirements without validating a passing evidence witness.
Schemas and synthetic expected outputs follow the selected interface; no helper,
example, regression or consumer was executed during this integration.

## Source-to-destination preview

Select canonical identities before considering a path move. A row is a possible
mapping, not a rename command. Keep established locations where they work.

| Current source class | Proposed destination or preserved compatibility | Required preservation |
| --- | --- | --- |
| Detailed root `ARCHITECTURE.md` | Preserve as canonical in `legacy-root`, or explicitly map to selected `docs/architecture/ARCHITECTURE.md` | Source bytes, stable ID, front matter, dependencies, citations; root becomes navigation only after all consumers are reconciled. |
| Root purpose/mission material | Retain the existing selected PURPOSE concern, or map its identity into the selected architecture corpus | Mission/scope/limits/change-admission meaning; no competing MISSION authority. |
| Existing `docs/ecosystem/**` / `docs/foundation/**` | Preserve by declared repository exception unless an owner-reviewed move is justified | Hygiene ownership, current links, diagrams, architecture metadata, source identity and historical evidence. This proposal moves none. |
| Root `AGENTS.md` | Keep exact root entry | Repository-authored instructions and each pinned managed region; never replace with generic new instructions. |
| Root `CONTINUITY.md` | Keep exact compact root handoff | Aether continuity semantics and privacy; historical transcripts stay outside the checkpoint. |
| Selected Claude compatibility | Regular root `CLAUDE.md` importing `@AGENTS.md` | Preserve justified provider instructions through reviewed change; no symlink or eager corpus import. |
| Existing ADR corpus/index | Keep `docs/decisions/` | Numbered records, accepted decisions, approval evidence, lineage, dated original citations and local extensions. No renumbering or lifecycle changes. |
| Long implementation explanation/evidence | Existing evidence/development location or deliberately selected durable path | Source scope, actual validation limits and relevant rationale; README links to it. |
| Ignored temporary working notes | Remain outside versioned source unless useful content is promoted | Durable requirements, decisions and proof must be reviewed into their proper source first; no private transcript publication. |
| Spaces/Unicode in existing filenames | Preserve literal names | Update links deliberately if a later move is approved; no reference-profile-induced rename. |

Each real map must list old/new paths, source IDs, source and proposed output
digests, owning/generated regions, inbound/outbound references, retained aliases,
actual unknowns, and an exact rollback selection. Inventory handles are not new
architecture IDs. Conflicting canonical identities require maintainer selection.

## Required consumer inventory and next owner

| Consumer | Bounded next checkpoint | Existing coordination |
| --- | --- | --- |
| Aether | Review architecture-set/document specs, authoring skills, source-discovery precedence and managed agent projections against the selected map; patch only real gaps and regenerate owned projections together. Existing continuity behavior stays composed. | Hygiene #64 phase 2; existing Aether continuity sources from #81/#82 remain draft. A new implementation issue has not been created here. |
| Empathy | One opt-in pilot reconciles the catalog/profile, root navigation, index, selected corpus, inventory and generated ownership. Add AGENTS/CONTINUITY applicability explicitly through the existing continuity composition; do not pretend catalog 2.0 already declares them universally. | Hygiene #64 phase 3, foundation owner Empathy, organization file walkthrough [.github #32](https://github.com/egohygiene/.github/issues/32). |
| Holon / Identity | Inspect README blueprint mappings, generated-region markers, source digests, merge conflict checks and rollback. Consume only reviewed Identity assets; preserve outside-region local prose byte-for-byte. | [Holon #24](https://github.com/egohygiene/holon/issues/24), [Identity #54](https://github.com/egohygiene/identity/issues/54). |
| EgoLint | Review exact path/discovery and link/content semantics using admitted sources, including canonical-versus-navigation duplicates, scoped applicability and unsupported cases. This optional reference is not a new production linter. | Existing presentation/continuity ownership; [EgoLint #55](https://github.com/egohygiene/egolint/issues/55) carries continuity validation. |
| Relay / Observatory | Inspect collectors, rendering paths, source receipts, search/graph links and normalized references against the actual map; preserve clocks and evidence semantics. | [Relay #60](https://github.com/egohygiene/relay/issues/60), [Observatory #18](https://github.com/egohygiene/observatory/issues/18) are existing continuity boundaries, not proof of layout adoption. |
| Repository publishers | Inspect site configuration, route/link maps, redirects and artifact provenance before any path change. No new publisher, hosting or build is selected here. | Each repository owns facts and final publication. |
| Pace | Preview reviewed adoption only after compatible owner inputs and a qualified pilot exist; retain exceptions, pins and rollback state. | [Pace #14](https://github.com/egohygiene/pace/issues/14), [#26](https://github.com/egohygiene/pace/issues/26). |

Links identify existing concerns; this source-only checkpoint does not update
their state, post messages, create downstream issues or claim completion.

## Pilot, qualification and rollback

1. Review the proposed layout/ADR and actual source-owner gaps. Preserve the
   presentation and continuity policies' independent human activation gates.
2. Build the complete consumer/path inventory, then select one Empathy pilot
   without broad file moves or specialist-source absorption.
3. Preview canonical identities, metadata/dependencies, generated ownership,
   local text, root/index navigation, provider compatibility and aliases.
4. Update all affected owner inputs/consumers for that map together; production
   selection uses exact immutable revisions and matching byte digests.
5. In the deferred qualification pass, run schemas and regression cases, actual
   Aether discovery/content checks, production EgoLint/link validation, Holon
   plan/verify/rollback and consumer rendering checks with real owner inputs.
6. Review actual outputs and exclusions before any optional publication or Pace
   adoption. Merge/source presence never supplies ratification or live evidence.

Rollback restores the prior reviewed path/pin/source-byte and generated ownership
selection through a reviewed change. Keep legacy navigation or redirects where
needed; preserve edits made after the pilot rather than overwriting them.
Rollback does not rewrite history, delete ADR/evidence originals, revoke human
disposition, weaken admission, or automatically deploy anything. No pilot or
recovery was executed for this proposal; all those outcomes remain unknown.
