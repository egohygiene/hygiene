# Ego Hygiene roadmap pull-request index

**Snapshot:** 2026-08-24  
**Branch:** `docs/holistic-roadmap-2026-08-24`  
**Status:** 28 draft pull requests created successfully; no default branch was changed  
**Execution graph:** 146 unique quest steps across 28 repositories

## Merge policy

These are truth/reconciliation pull requests, not workflow-adoption pull requests. Keep them draft while `hygiene.roadmap/v1alpha1` and the Egolint validation path are still proposed.

Recommended order:

1. review and accept the Hygiene audit, visual-roadmap specification, rollout plan, and contract direction;
2. release the owner chain: Hygiene, Aether, Egolint, Observatory, Identity, Holon, Relay, then Pace;
3. repair and activate the canonical `egohygiene.io/roadmap/` consumer;
4. prove composed, central, and disabled publication modes;
5. merge remaining repository truth updates in bounded waves;
6. generate duplicate-aware issue plans privately and require explicit approval before any issue writes.

## Pull requests

| Repository | Draft PR | Quest steps | Publication | Current gate |
| --- | ---: | ---: | --- | --- |
| `.github` | [#18](https://github.com/egohygiene/.github/pull/18) | 5 | `central` | Finish the label and routing policy tracked in issue #8, then prove the organization defaults in a consumer repository. |
| `aether` | [#48](https://github.com/egohygiene/aether/pull/48) | 6 | `central` | Repair release workflow run 32672225496, which selected zero jobs, then publish the first immutable bundle release tracked by issue #38. |
| `akashic` | [#56](https://github.com/egohygiene/akashic/pull/56) | 5 | `composed` | Promote issue #34 as the canonical roadmap and deliver stable identifiers and the search work in issue #42. |
| `aniflow` | [#9](https://github.com/egohygiene/aniflow/pull/9) | 5 | `central` | Fix the lowercase-title policy failure, reconcile the claimed v0.3 status, and publish the first verified release. |
| `athena` | [#2](https://github.com/egohygiene/athena/pull/2) | 5 | `central` | Produce a machine-readable inventory and rights/provenance ledger before packaging or encouraging reuse. |
| `beacon` | [#6](https://github.com/egohygiene/beacon/pull/6) | 5 | `central` | Extract a runnable publication CLI and template package before expanding the whitepaper, dossier, magazine, and research formats. |
| `civics` | [#3](https://github.com/egohygiene/civics/pull/3) | 5 | `composed` | Create the missing roadmap and issue backlog, then certify the 2026-09-01 dataset and evidence rules. |
| `egohygiene` | [#414](https://github.com/egohygiene/egohygiene/pull/414) | 5 | `disabled` | Make PR #411 green across Android and iOS by resolving issues #413 and #412, then finish the personal-values loop. |
| `egohygiene.io` | [#6](https://github.com/egohygiene/egohygiene.io/pull/6) | 5 | `canonical` | Fix undefined CI scripts and red CodeQL, correct stale repository metadata, and restore a verified deployment path. |
| `egolint` | [#22](https://github.com/egohygiene/egolint/pull/22) | 6 | `central` | Turn the red self-dogfood run and its 119 findings into an owned, green baseline through issues #20 and #21. |
| `empathy` | [#73](https://github.com/egohygiene/empathy/pull/73) | 5 | `composed` | Restore the security baseline: PR #72 is red and the audit observed 57 high-or-greater OSV findings plus OpenSSF failures. |
| `filament` | [#2](https://github.com/egohygiene/filament/pull/2) | 5 | `central` | Resolve the Filament/Firmament boundary and add a license, issue backlog, and CI foundation. |
| `flow` | [#6](https://github.com/egohygiene/flow/pull/6) | 5 | `central` | Add CI and a minimal executable orchestrator before expanding provider adapters. |
| `holon` | [#21](https://github.com/egohygiene/holon/pull/21) | 6 | `central` | Produce default-branch CI and release evidence, then complete the React/Vite blueprint in issue #14. |
| `hygiene` | [#18](https://github.com/egohygiene/hygiene/pull/18) | 6 | `central` | Accept ADR #15 and add CI before treating the repository catalog and contracts as authoritative. |
| `identity` | [#36](https://github.com/egohygiene/identity/pull/36) | 6 | `central` | Complete voice and approval evidence in issues #13 and #8 before building the renderer and studio. |
| `mantle` | [#22](https://github.com/egohygiene/mantle/pull/22) | 5 | `central` | Make the default branch green and classify ownership and safety expectations for all 73 bin commands. |
| `mindcap` | [#30](https://github.com/egohygiene/mindcap/pull/30) | 5 | `central` | Apply Ruff formatting to the vault catalog and CLI, restore CI, and reconcile stale extraction-era documentation. |
| `mindgarden` | [#4](https://github.com/egohygiene/mindgarden/pull/4) | 5 | `central` | Extract the incubated implementation from Empathy and establish a tested knowledge contract. |
| `observatory` | [#6](https://github.com/egohygiene/observatory/pull/6) | 5 | `central` | Deliver the executable foundation in issue #1 before presenting portfolio status as computed. |
| `optiflow` | [#40](https://github.com/egohygiene/optiflow/pull/40) | 5 | `composed` | Resolve remaining v0.1 contradictions, complete adversarial testing, and publish a signed release. |
| `pace` | [#12](https://github.com/egohygiene/pace/pull/12) | 6 | `central` | Add observed-state capture and a drift report before attempting the reviewable convergence plan tracked by issue #2. |
| `realm` | [#14](https://github.com/egohygiene/realm/pull/14) | 5 | `central` | Pin workflow dependencies, add CI, and prove the contract through a real base-image projection. |
| `reflector` | [#246](https://github.com/egohygiene/reflector/pull/246) | 5 | `composed` | Reconcile the roadmap with completed template extraction and restore commit-policy consistency before the next manuscript checkpoint. |
| `relay` | [#26](https://github.com/egohygiene/relay/pull/26) | 5 | `central` | Reconcile the stale roadmap with shipped v1.0-v1.2 behavior, then define and prove the reusable roadmap build workflow. |
| `renderflow` | [#347](https://github.com/egohygiene/renderflow/pull/347) | 5 | `composed` | Restore the full CI and documentation publication matrix, including pnpm setup ordering and Snapcraft schema compatibility. |
| `sanctuary` | [#2](https://github.com/egohygiene/sanctuary/pull/2) | 5 | `central` | Register the contract in Hygiene and put one real incubation through the currently empty index. |
| `store` | [#14](https://github.com/egohygiene/store/pull/14) | 5 | `central` | Fix the duplicate Black/Small E2E locator and obtain a green replacement for red PR #10 before claiming deploy readiness. |

## Safety record

- All roadmap changes are isolated on review branches.
- Existing strategic roadmap prose was preserved.
- Civics receives the only new root `ROADMAP.md`.
- No issues, labels, releases, workflows, Pages settings, or deployments were changed.
- The private product uses `publication: disabled` and is excluded from public aggregation before evidence collection.
- Public site artifacts exclude the issue-plan payload.

