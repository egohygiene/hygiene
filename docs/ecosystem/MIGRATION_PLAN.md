# Migration and Stand-up Plan

This plan favors fast, bounded vertical slices. Workstreams may run in parallel after the architecture registry is accepted, but each extraction finishes with a released artifact and a consuming proof before its staging source is removed.

## 1. Operating model

Create a migration ledger in Hygiene with one record per staged component:

```yaml
id: empathy-staging-devenvironment-workstation-shell
source: egohygiene/empathy:.staging/devenvironment/workstation/shared/shell
target: egohygiene/mantle
classification: candidate
origin: local
license_review: pending
history_strategy: filtered-import
target_pr: null
verification:
  standalone: pending
  consumer: pending
cleanup_pr: null
state: inventoried
```

Allowed states: `inventoried → classified → importing → verified → cleanup-ready → removed`, with `rejected` and `archived` as terminal alternatives. Deletion from Empathy occurs only after target and consumer verification.

## 2. Staging disposition

The GitHub scan found these major staged groups.

| Empathy source | Observed scale | Primary destination | Treatment |
| --- | ---: | --- | --- |
| `.staging/devenvironment` | 487 files | Realm, Mantle, and Filament; Firmament only after a separate future decision | Split environment, shell, reusable IaC, and possible operated-infrastructure material by capability; do not import as one directory |
| `.staging/devenvironment/.devcontainer` | 7 files | Realm | Convert to tested features/templates; remove project-specific assumptions |
| `.staging/devenvironment/workstation` | 248 files | Realm plus Mantle shell subset | Express as declarative host profiles; separate personal/private overlays |
| `.staging/devenvironment/containers` | 215 files | Realm optional runtime profiles; archive/reject obsolete experiments | Keep service images out of Realm `base` and `full` unless capability policy requires them |
| `.staging/.github` | 1,595 files | Aether, Relay, Athena/archive, or reject | Curate by provenance and license; never bulk-promote third-party prompts/skills |
| `.staging/.github/workflows` | 39 files | Relay | Deduplicate, harden permissions, pin actions, then expose small reusable contracts |
| `.staging/.github/agents`, `skills`, `specs`, `instructions` | 1,512+ files | Aether or Athena/archive | First-party stable artifacts go to Aether; references and vendored collections need attribution or archival treatment |
| `.staging/.opencode` and `.staging/.specify` | 28 files | Aether; project scaffolding fragments may go to Holon | Normalize into Aether catalog lifecycle; preserve upstream attribution |
| `.staging/hygiene` | 73 PNG files, ~135 MB | Athena archive; selected canonical sources/renders in Hygiene | Preserve raw references and metadata in Athena; promote only reviewed, reproducible diagrams |
| `.staging/renderflow` | 4 brand files | Renderflow or Identity | Product-specific brand stays local; shared brand tokens/assets move to Identity |
| `.staging/templates` | 20 files | Holon, Beacon, `.github` | Route repo templates to Holon, publication templates to Beacon, org defaults to `.github` |
| `.staging/react-template` | skeletal | Holon or retire | Validate usefulness before importing |
| `.staging/.pre-commit-config.yaml`, `.husky` | hook/config files | Egolint; execution patterns may be exposed by Relay | Consolidate into one local and CI quality entrypoint |
| `.staging/misc` | roadmap and visual | Hygiene and Athena | Read/classify individually; never preserve “misc” as an ownership category |
| Empathy root component directories | `beacon`, `egolint`, `holon`, `identity`, `mantle`, `mindgarden` | Corresponding repositories | Reconcile against target default branch; import only missing canonical work |
| Empathy ecosystem philosophy docs | root Markdown set | Ecosystem versions to Hygiene; repo-local versions remain in Empathy | Separate shared doctrine from the Empathy repository's own purpose |

## 3. Parallel workstreams

### Workstream A — Architecture control plane

Owner target: Hygiene.

1. Import this draft and open the architecture decision.
2. Accept the six planes, ownership table, and one-owner rule.
3. Add repository catalog schema and migration-ledger schema.
4. Rename `website` to `egohygiene.io` and record redirects/link repair as a tracked migration.
5. Add generated local context to seed repositories first, then active repositories.

Exit gate: all 27 repos are cataloged and the architecture release is tagged.

### Workstream B — Mantle standalone

Owner target: Mantle.

1. Diff `empathy/mantle`, staged shell/workstation fragments, and standalone `mantle`.
2. Choose canonical implementations; record discarded duplicates.
3. Test clean installs and idempotent upgrades for Bash, Zsh, and Fish across declared Linux/macOS/Windows compatibility targets.
4. Verify noninteractive behavior, path management, uninstall/rollback, and shell startup latency.
5. Publish a checksummed prerelease.

Exit gate: a clean machine/container can install, activate, test, and remove Mantle without Empathy.

### Workstream C — Realm image family

Owner target: Realm.

1. Define a capability manifest and image dependency graph.
2. Build `base` with a non-root user and pinned Mantle release.
3. Add one representative profile, then `full` as an explicit union.
4. Generate multi-architecture images, SBOMs, provenance, vulnerability results, and smoke tests.
5. Prove use from a minimal Dev Container configuration.
6. Classify workstation and self-hosted service material into native/Nix/container projections.

Exit gate: GHCR publishes immutable `base`, one profile, and `full`; Empathy consumes one by digest.

### Workstream D — CI and quality

Owners: Relay and Egolint.

1. Make Egolint a standalone local CLI/profile system.
2. Extract reusable setup/test/release primitives into Relay.
3. Have Relay invoke Egolint rather than duplicate policy.
4. Add least-privilege permissions, timeouts, immutable action pins, and normalized evidence outputs.
5. Adopt in Empathy and one Rust or web repository.

Exit gate: two unlike repositories consume the same released workflow and quality interfaces.

### Workstream E — Flow suite

Owners: Flow, Aniflow, Optiflow, Renderflow.

1. Freeze each holon's ownership and standalone contract.
2. Version capability discovery and plan/result JSON envelopes.
3. Implement Flow's `restore-and-optimize` or another accepted vertical slice through CLI adapters.
4. Prove resume, provenance, partial failure, and diagnostics.
5. Keep all sibling-holon dependency checks green.

Exit gate: Flow composes at least two released holons without importing their source or creating direct sibling dependencies.

### Workstream F — Knowledge and experience

Owners: Mindcap, Mindgarden, Identity, `egohygiene.io`, Store, Beacon, Akashic, Athena, Reflector, Ego Hygiene app.

1. Stabilize Mindcap's capture manifest and a minimal Mindgarden import.
2. Publish Identity's first token/metadata packages.
3. Complete the website rename and integrate Store through a route/deployment contract.
4. Give Beacon one real derivative and one mock/local publication channel.
5. Inventory Athena and link approved research/visual provenance.

Exit gate: one captured source can become structured knowledge and one branded derivative can be published and surfaced on the web without source copying.

## 4. Critical path

The fastest route to a usable personalized platform is:

1. Hygiene architecture release and catalog.
2. Mantle standalone prerelease.
3. Realm `base` → one profile → `full`.
4. Relay + Egolint adoption in Empathy.
5. Empathy as golden consumer with no relative component imports.
6. Holon creates a fresh fixture and Pace upgrades it.
7. Observatory reports the fixture and the live fleet.

The Flow suite and product/knowledge workstreams can proceed in parallel once ownership is frozen.

## 5. Cleanup rules

- Never clear `.staging` in one bulk commit.
- Remove one verified migration unit at a time and link its destination release/PR.
- Preserve Git history when it materially explains authorship or evolution; otherwise preserve source commit, checksum, and attribution in the ledger.
- Treat secrets, caches, generated outputs, vendored corpora, and machine-specific state as rejection candidates, not migration assets.
- Archive old diagrams with date, source, and “superseded” status; do not silently overwrite them.
- Personal workstation overlays remain private and compose on top of public Realm/Mantle modules.

## 6. Definition of platform-ready

The first platform milestone is reached when a new repository can be created by Holon, opened in a digest-pinned Realm environment with Mantle active, validated by Relay/Egolint, described by local ecosystem context, upgraded through a Pace pull request, and reported by Observatory—without importing Empathy or relying on `.staging`.
