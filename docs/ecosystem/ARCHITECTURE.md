# Ego Hygiene Holistic Architecture

Status: **accepted v0.1**  
Canonical target: `egohygiene/hygiene`  
Last reconciled: **2026-08-18**

## 1. Intent

Ego Hygiene is a portfolio of independently useful products, tools, platform capabilities, and knowledge systems that work together through versioned artifacts and explicit contracts. It is not a monorepo split across many GitHub repositories, and no repository is a dumping ground for shared code.

The target system optimizes for one person moving very quickly without turning temporary convenience into permanent ambiguity:

- one canonical owner for every capability;
- independent releases and standalone usefulness;
- composition through packages, OCI images, CLIs, and versioned data contracts;
- generated repository context instead of copied architecture;
- local-first operation with optional cloud deployment;
- automation that proposes pull requests and preserves reviewable provenance;
- incubation is allowed, but every staged artifact has an owner, state, and exit condition.

## 2. The six planes

### 2.1 Architecture and control plane

This plane defines the ecosystem, creates and evolves repositories, distributes reusable AI artifacts, reconciles the fleet, and makes maturity visible.

- **hygiene** — canonical ecosystem architecture, repository registry, platform policies, cross-repository decisions, adoption model, and staging ledger.
- **.github** — organization profile, public defaults, funding, and default community-health files.
- **aether** — canonical first-party AI specifications, skills, agents, catalogs, validators, and release projections.
- **holon** — architecture-driven bootstrapper that creates new organizations and repositories from versioned blueprints.
- **pace** — fleet reconciler for adoption, migrations, and synchronization; it proposes bounded pull requests to existing repositories.
- **observatory** — read-oriented portfolio inventory, maturity tracking, dependency visibility, conformance evidence, and platform telemetry.
- **sanctuary** — bounded incubation workspace for unfinished or ownerless
  public work, with provisional manifests, provenance, lifecycle evidence, and
  reviewed graduation proposals.

The distinction between Holon and Pace is deliberate: **Holon creates; Pace converges**. Observatory reports; it does not silently remediate. Hygiene defines policy; it does not contain the implementations of every policy.

Sanctuary incubates; it does not own a capability after graduation. Its local
lifecycle schema remains provisional until a separate Hygiene decision makes
those semantics organization-wide canonical. Stable repositories must consume
graduated work from its durable owner rather than depend on Sanctuary source.

### 2.2 Developer and runtime platform

This plane makes every repository reproducible on a workstation, in a Dev Container, and in CI.

- **realm** — environment artifact factory: layered OCI images, Dev Container templates/features, Nix flake/modules, workstation profiles, and optional self-hosted service profiles.
- **mantle** — portable shell runtime and developer-tooling framework for Bash, Zsh, Fish, Linux, macOS, and Windows compatibility environments.
- **relay** — reusable GitHub Actions, composite actions, and release/CI workflow orchestration.
- **egolint** — lint policy, profiles, CLI behavior, report normalization, autofix boundaries, and quality evidence.
- **empathy** — strict golden baseline, golden consumer, and integration testbed
  for the complete repository foundation; historical staging is migration
  evidence, not ongoing general incubation.

Realm consumes a released Mantle artifact. Relay invokes Egolint. Empathy proves that the assembled platform works without becoming the canonical source for its components.

### 2.3 Content transformation and publishing plane

This plane turns source media and documents into verified, distributable artifacts.

- **flow** — suite facade and cross-holon orchestration: planning, compatibility, execution state, provenance, recovery, progress, and diagnostics.
- **aniflow** — time-based video decomposition, ordered frame/audio/video processing, reconstruction, temporal validation, and resumable run evidence.
- **optiflow** — safe local inventory, evidence-backed media relationships, immutable optimization plans, and collection normalization.
- **renderflow** — spec-driven transform graphs and publication-ready document, image, and audio derivatives.
- **beacon** — multi-channel release assembly, validation, packaging, publication, and distribution.

Flow wraps the other engines without absorbing them. Aniflow, Optiflow, and Renderflow remain standalone libraries and CLIs and must not depend directly on one another. Flow composes them through stable public library interfaces or versioned CLI/JSON contracts. Beacon may invoke Renderflow or Flow but owns release and distribution policy, not transformation engines.

### 2.4 Knowledge and research plane

This plane captures evidence, builds usable knowledge, preserves source material, and publishes research.

- **mindcap** — capture connectors, verified source archives, canonical ingestion inputs, and provenance.
- **mindgarden** — versioned semantic knowledge model, relationships, query, curation, and second-brain workflows.
- **akashic** — curated public knowledge constellations and focused Awesome lists.
- **athena** — preserved assets, raw references, external resources, and large archival collections.
- **reflector** — research and tooling for reflective synchronization and governable recursive AI-assisted engineering.

Athena is the reservoir; Akashic is an opinionated public collection; Mindcap is acquisition; Mindgarden is the living knowledge system; Reflector is a research product. Raw archives must not become runtime dependencies.

### 2.5 Identity, product, and experience plane

This plane exposes the ecosystem to people.

- **identity** — brand systems, design tokens, voice, public metadata, and generated creative-asset packages.
- **egohygiene** — the private, local-first Flutter cognition and reflection product.
- **egohygiene.io** — the renamed `website` repository and canonical public website, documentation, playground, and shared web packages.
- **store** — provider-neutral storefront and commerce adapter deployed at `egohygiene.io/store`.

Identity publishes versioned brand artifacts that products consume. The website and store retain separate release boundaries even when they share a domain. The Ego Hygiene app is a product, not the platform-control repository.

### 2.6 Infrastructure and deployment plane

This plane publishes reusable infrastructure definitions without taking
ownership of every environment built from them.

- **filament** — reusable infrastructure-as-code modules, stack contracts,
  schemas, provider and engine adapters, examples, tests, and validation
  semantics.

Filament consumers retain deployment intent, credentials, budgets, approvals,
environment-specific topology, and production state. Relay may execute
Filament validation and release workflows, while Realm supplies development
environments and tools; neither owns Filament's infrastructure semantics.

## 3. Foundational document architecture

The earlier “Engineering Universe” diagrams remain useful, but they describe a documentation and reasoning system rather than repository topology. The new architecture preserves that system inside Hygiene as a governance plane:

- **Purpose and identity:** `VISION`, `PURPOSE`, `MANIFESTO`, `PRINCIPLES`, `PILLARS`.
- **Method and system:** `METHODOLOGY`, `FOUNDATIONS`, `SYSTEM`, `ROADMAP`, `ARCHITECTURE`.
- **Meta and AI governance:** `META`, `EPISTEMOLOGY`, `AI_CONSTITUTION`.
- **Domain model:** `ONTOLOGY`, `PERSONAL_MODEL`.
- **Experience:** `DESIGN`, `DESIGN_SYSTEM`.
- **Oversight:** `DECISIONS` and cross-repository ADRs.

Ecosystem-level versions of these documents belong in `hygiene/docs/foundation/`. Product- or repository-specific versions remain local and link back to the canonical ecosystem context. A file with the same name is not automatically the same bounded context.

## 4. Composition and dependency rules

### 4.1 Allowed integration mechanisms

Repositories compose through one or more of these versioned surfaces:

1. OCI images and Dev Container features from GHCR.
2. GitHub Releases and checksummed standalone binaries or bundles.
3. Ecosystem-native packages such as crates, npm packages, Python packages, or Nix inputs.
4. Reusable workflows and actions pinned to immutable references.
5. Versioned JSON schemas and CLI contracts.
6. Pull-request projections generated from a canonical catalog or template.
7. HTTP APIs only where a running service is genuinely required.

### 4.2 Forbidden coupling

- No copying a sibling repository's source tree to “integrate” it.
- No direct dependency between Aniflow, Optiflow, and Renderflow.
- No permanent component source in `empathy` after extraction.
- No unversioned dependency on another repository's default branch in production.
- No circular build dependencies.
- No giant universal base image containing every optional tool.
- No raw Athena archive as a runtime or build dependency.
- No infrastructure secrets, workstation secrets, or private identity data in images or templates.

### 4.3 Contract ownership

Contracts live with the capability that owns their semantics. Flow owns suite orchestration schemas; Aether owns AI artifact catalogs; Hygiene owns the repository registry and conformance model; Identity owns brand package schemas; each product owns its domain contracts. A generic “shared contracts” repository is intentionally avoided.

## 5. Realm artifact architecture

Realm should emit multiple targets from a shared, tested definition rather than treat one Docker image as the whole workstation system.

### 5.1 OCI image family

Recommended initial tags:

- `ghcr.io/egohygiene/realm:base` — minimal supported developer substrate, non-root user, certificates, common transport/archive tools, shell prerequisites, labels, and health metadata.
- `ghcr.io/egohygiene/realm:<profile>` — independently useful toolchain profiles extending `base`, such as `rust`, `python`, `node`, `flutter`, `media`, or `cloud` after the exact list is accepted.
- `ghcr.io/egohygiene/realm:full` — the union intended for the primary all-capabilities workstation and integration tests.
- immutable release and digest tags alongside moving convenience tags.

Every variant must extend the same released base, support the declared architectures, produce an SBOM and provenance attestation, run a profile smoke test, and stay free of credentials and personal state.

### 5.2 Mantle in Realm

Mantle should be installed from a pinned release artifact and configured for the non-root developer user. Realm owns the installation decision and image integration; Mantle owns the shell behavior and portable installer.

Docker's `SHELL` instruction is **not** the correct way to make Mantle the interactive shell. `SHELL` changes the interpreter used by later shell-form Dockerfile instructions (and shell-form command instructions); it does not change the user's login shell. Mantle is currently a framework layered over supported shells, not a replacement POSIX shell executable.

Use a conventional build shell such as:

```dockerfile
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
```

Then install Mantle, select Bash/Zsh/Fish as the actual user shell, and source Mantle through the appropriate login/interactive startup integration. Dev Container settings may select the terminal profile, but the image must also behave correctly without VS Code.

### 5.3 Workstation and runtime outputs

Realm may additionally publish:

- a Nix flake with reusable modules and host profiles;
- Dev Container templates and features;
- native bootstrap manifests for supported hosts;
- optional Compose/service profiles for local self-hosting;
- a machine-readable capability manifest shared by all outputs.

Nix, Dev Containers, and OCI are peer projections of the same capability model. Nix should not be forced to “consume a Docker image” when a native host module is the correct artifact.

### 5.4 Infrastructure definitions and future operation boundary

Reusable multi-cloud and local infrastructure definitions are separate from
the developer environment. Filament owns those versioned modules, stack
contracts, provider adapters, and validation semantics without owning consumer
credentials or state.

The working-name **firmament** remains a separate deferred possibility for
organization-operated infrastructure compositions, networking, clusters,
deployment environments, and operational state. It is not part of the current
26-repository inventory. It must not duplicate Filament modules and should be
created only after Realm and Filament artifact contracts are stable and a
separate decision proves a durable operational need.

## 6. Repository context distribution

Hygiene will publish an architecture release containing:

- `catalog/repositories.yaml` — machine-readable repository registry;
- this ecosystem architecture;
- cross-repository ADRs and contract indexes;
- diagram sources and approved rendered diagrams;
- a staging migration ledger.

Each repository should contain a generated `docs/ecosystem/CONTEXT.md` with:

- the pinned Hygiene architecture release;
- its portfolio, purpose, ownership, and non-responsibilities;
- upstream inputs and published outputs;
- local maturity and immediate migration gate;
- links to canonical diagrams and decisions.

Each repository's `AGENTS.md` should require agents to read that local context before architecture-changing work. Pace later opens update PRs when the canonical architecture changes. Repository-local docs may add detail but may not silently redefine cross-repository ownership.

## 7. Control loops

### 7.1 Create and adopt

1. Hygiene defines a versioned repository class and policy.
2. Holon creates a new repository from that class.
3. Aether supplies appropriate agent/skill projections.
4. Realm supplies the development environment.
5. Relay runs CI and Egolint validates quality.
6. Observatory records evidence and maturity.
7. Pace proposes upgrades as the platform evolves.

### 7.2 Capture to publication

1. Mindcap captures and verifies source material.
2. Mindgarden structures and relates knowledge.
3. Akashic curates public knowledge where appropriate.
4. Flow coordinates selected media/document operations.
5. Specialized work runs in Aniflow, Optiflow, or Renderflow.
6. Beacon assembles and distributes releases.
7. Identity supplies brand packages.
8. `egohygiene.io`, Store, and the Ego Hygiene app present experiences.

These are capability flows, not a requirement that every repository imports every predecessor.

## 8. Success criteria

The architecture is operating—not merely documented—when:

- all 27 repositories have one explicit owner boundary and generated local context;
- no production component exists only under `empathy/.staging`;
- Mantle is independently tested across its supported shells/platforms;
- Realm publishes a tested base image, at least one profile, and `full` with SBOM/provenance;
- Empathy consumes released platform artifacts and passes an end-to-end golden-repository test;
- Relay and Egolint replace copied workflow/lint implementations;
- Flow can plan and execute at least one cross-holon pipeline without sibling engine dependencies;
- Observatory can report versions, conformance, and maturity across the fleet;
- selected diagrams are generated from reviewed sources and old visuals are archived with provenance.
