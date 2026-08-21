# Repository Catalog

Observed on GitHub: **2026-08-21**
Inventory: **27 repositories**
Status labels describe the observed implementation state, not product quality.

## Architecture and control plane

| Repository | Target ownership | Explicitly does not own | Observed state | First gate |
| --- | --- | --- | --- | --- |
| `hygiene` | Canonical ecosystem architecture, repo registry, platform policy, cross-repo ADRs, maturity model, migration ledger | Tool implementations, reusable workflows, product domain logic | Seed | Import and approve this architecture package |
| `.github` | Organization profile, funding, public defaults, default community-health files | Reusable CI/release workflow implementations | Light foundation | Reduce to org-facing defaults; delegate automation to Relay |
| `aether` | First-party AI specs, skills, agents, catalog/provenance schemas, validators, release projections | General repository policy, environments, CI, linting, release orchestration | Active | Curate staged AI assets with provenance and lifecycle state |
| `holon` | Versioned blueprints and bootstrap engine for new repos/orgs | Ongoing synchronization of existing repos | Seed | Define one repository-class schema and generate a disposable fixture |
| `pace` | Fleet adoption, migration, reconciliation, synchronization, PR generation | Product CI primitives or direct unreviewed mutation of default branches | Seed | Read Hygiene catalog and produce a dry-run projection diff |
| `observatory` | Inventory, maturity, dependency visibility, conformance evidence, telemetry | Policy definition or silent remediation | Seed | Ingest the repository catalog and Relay/Egolint evidence |
| `sanctuary` | Bounded incubation, provenance, lifecycle evidence, and reviewed ownership-decision proposals for unfinished or ownerless public work | Canonical templates/policy, stable dependencies, permanent specialist source, secrets/private data, generic artifact archives | Provisional local contract | Prove one real incubation without broadening the local lifecycle into organization policy |

## Developer and runtime platform

| Repository | Target ownership | Explicitly does not own | Observed state | First gate |
| --- | --- | --- | --- | --- |
| `realm` | Layered OCI images, Dev Containers, Nix modules/profiles, native workstation projections, optional local runtime profiles | Shell semantics, CI workflows, cloud resource provisioning | Seed with substantial source staged in Empathy | Publish `base`, one profile, and `full`; install pinned Mantle |
| `mantle` | Portable shell framework, startup integration, environment management, tool installers, cross-platform shell tests | OS image lifecycle, Dev Container metadata, cloud infrastructure | Active implementation | Reconcile Empathy copy, prove standalone install matrix, tag release |
| `relay` | Reusable workflows, composite actions, CI/release orchestration | Lint policy, repo architecture, product release semantics | Seed | Extract one reusable test workflow and one release primitive |
| `egolint` | Universal lint CLI/profiles, rules, MegaLinter integration, report normalization, safe autofix policy | Workflow fleet distribution or unrelated repository templates | Early implementation | Make the CLI standalone and invoke it from Relay |
| `empathy` | Strict golden baseline, golden consumer, integration testbed, humane repository reference | Permanent source of Mantle/Realm/Holon/etc.; untracked staging; general incubation | Transition monorepo | Add migration ledger; consume released Mantle and Realm artifacts |

## Infrastructure and deployment

| Repository | Target ownership | Explicitly does not own | Observed state | First gate |
| --- | --- | --- | --- | --- |
| `filament` | Reusable IaC modules, stack contracts, schemas, provider/engine adapters, examples, tests, and validation semantics | Consumer deployment intent, credentials, budgets, approvals, production state, developer environments, CI orchestration | Provisional architecture | Select one bounded vertical slice and publish a stable contract with a disposable consumer fixture |

## Content transformation and publishing

| Repository | Target ownership | Explicitly does not own | Observed state | First gate |
| --- | --- | --- | --- | --- |
| `flow` | Cross-holon plans, compatibility, execution state, provenance, validation, recovery, suite UX | Reimplementation of specialized engines | Architecture-first | Accept contracts and implement one vertical slice |
| `aniflow` | Temporal video decomposition, ordered processors, reconstruction, checkpoints, temporal validation | Collection optimization, document transforms, suite-wide orchestration | Active implementation | Stabilize versioned CLI/library contract for Flow |
| `optiflow` | Read-safe inventory, evidence-backed relationships, immutable optimization plans, collection normalization | Temporal video reconstruction, transform graphs, suite-wide orchestration | Active implementation; read-only v0.1 | Stabilize plan/schema contract before mutation features |
| `renderflow` | Spec-driven transform graphs and publication-ready document/image/audio derivatives | Collection policy, temporal orchestration, distribution policy | Active product | Publish stable Flow-facing contract and retain standalone UX |
| `beacon` | Release assembly, validation, packaging, channel adapters, publication and distribution | Rendering engines or knowledge storage | Seed | Publish one artifact through a local/mock channel using Renderflow output |

## Knowledge and research

| Repository | Target ownership | Explicitly does not own | Observed state | First gate |
| --- | --- | --- | --- | --- |
| `mindcap` | Capture plugins, verified archives, canonical ingestion records and provenance | Semantic knowledge model or publishing | Active implementation | Define stable capture manifest consumed by Mindgarden |
| `mindgarden` | Versioned semantic knowledge, relationships, query, curation, second-brain workflows | Source capture mechanics or raw archival storage | Seed | Define minimal local-first storage and import Mindcap manifest fixture |
| `akashic` | Curated public knowledge lists and exploration site | Raw dump/archive or private personal knowledge | Active product | Define optional export/import relationship with Mindgarden |
| `athena` | Preserved assets, references, large source collections and archival provenance | Canonical architecture or runtime dependencies | Active collection | Add inventory/licensing metadata and absorb raw visual archive |
| `reflector` | Research manuscript, reflective synchronization CLI, publication evidence, recursive-engineering research | Generic fleet controller or canonical platform policy | Active research product | Publish its research contracts and report evidence to Observatory |

## Identity, product, and experience

| Repository | Target ownership | Explicitly does not own | Observed state | First gate |
| --- | --- | --- | --- | --- |
| `identity` | Brand system, design tokens, voice, public metadata, generated asset packages | Product UI implementation or raw asset archive | Seed | Publish versioned token and metadata packages |
| `egohygiene` | Private Flutter cognition/reflection product and its domain model | Ecosystem control plane or generic repo foundation | Active private product | Consume released Identity/Realm/Relay surfaces incrementally |
| `egohygiene.io` | Public site, docs, playground, web design-system packages; renamed from `website` | Store commerce logic or generic publishing engine | Active implementation; rename pending | Rename repo and repair links, packages, deployment, and badges |
| `store` | Provider-neutral storefront and commerce port/adapters at `egohygiene.io/store` | Main-site content platform, manufacturing, fulfillment, hosted checkout | Active implementation | Formalize integration contract and independent deployment with site |

## Cross-repository adjacency

The following relationships are intentional and should be contract-tested:

| Producer | Consumer | Artifact/contract |
| --- | --- | --- |
| Hygiene | every repo | architecture release, repository registry, context projection |
| Aether | repo agents and Holon/Pace | versioned AI artifacts and catalogs |
| Holon | new repositories | generated bootstrap tree plus provenance manifest |
| Pace | existing repositories | pull-request projections and migration diffs |
| Realm | every implementation repo | OCI/Dev Container/Nix/workstation environment artifacts |
| Mantle | Realm and native workstations | versioned installer/runtime bundle |
| Relay | every implementation repo | pinned reusable workflows/actions |
| Egolint | Relay and local developers | CLI, profiles, normalized reports/SARIF |
| Relay/Egolint | Observatory | conformance and run evidence |
| Aniflow/Optiflow/Renderflow | Flow | stable library or versioned CLI/JSON contract |
| Renderflow/Flow | Beacon | artifact manifests and validated derivatives |
| Mindcap | Mindgarden | capture/archive manifest with provenance |
| Identity | products, site, store, Beacon | tokens, assets, voice and metadata packages |
| Store | `egohygiene.io` | route/deployment/analytics contract, not source inclusion |
| Filament | infrastructure consumers | versioned modules, stack contracts, schemas, provider adapters, validation evidence |
| `.github` | Sanctuary | routed ownerless-work intake and ownership questions |
| Sanctuary | durable capability owners | immutable graduation provenance and reviewed ownership-decision evidence |

## Deferred repository

`firmament` remains a proposed future boundary for organization-operated
infrastructure compositions, networking, clusters, deployment environments,
and operational state. It is not in the current inventory and must not duplicate
Filament's reusable IaC contracts. It should not be created until Realm and
Filament publish stable artifact contracts and a separate decision proves a
non-overlapping operational need.
