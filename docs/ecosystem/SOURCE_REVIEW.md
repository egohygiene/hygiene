# Source Review and Reconciliation Notes

## Inputs inspected

- The default-branch metadata, root directory, and README for all 25 repositories accessible in the `egohygiene` GitHub organization on 2026-08-17.
- The attached Flow orchestration issue, including its proposed CLI-adapter architecture, versioned JSON contracts, execution state, provenance, diagnostics, and `restore-and-optimize` vertical slice.
- The attached Hygiene visual archive: 73 PNG files, approximately 135 MB.
- Empathy's current root and `.staging` inventory, including recursive summaries for AI/workflow assets and developer-environment material.

No repository was renamed or mutated during this review.

## Live-state observations

- Substantial implementations already exist in Renderflow, Reflector, the private Ego Hygiene app, Empathy, Aether, Mindcap, Aniflow, the Website, Store, Mantle, Akashic, and Optiflow.
- Flow is architecture-first and already documents the intended holon boundaries.
- Egolint is an early implementation.
- `.github` and Athena contain real material but have narrower architectural roles than application repositories.
- Pace, Realm, Identity, Mindgarden, Beacon, Holon, Hygiene, Relay, and Observatory are currently seeds or near-seeds; their roles in this draft are target ownership decisions, not claims of completed functionality.
- The Website repository already contains `apps/egohygiene.io`, strengthening the planned repository rename to `egohygiene.io`.

## Empathy staging observations

The recursive scan found:

- 487 files under staged developer-environment material: 248 workstation files, 215 container files, 11 Realm-related files, 7 Dev Container feature files, and small Dockerfile/Compose groups.
- 1,595 files under staged `.github` material: 1,037 skills, 233 agents, 189 instructions, 53 specs, 39 workflows, plus scripts and references.
- 73 old visual files totaling about 135 MB.
- Smaller groups for OpenCode/Specify commands, templates, Renderflow brand assets, hook configurations, a React template skeleton, and miscellaneous items.

These counts make a bulk “move staging to its matching repo” operation unsafe. The migration plan instead routes individual capabilities and records rejected, archived, or superseded material.

## Ideas retained from the old diagrams

- “Build once, reuse everywhere.”
- A philosophical/document foundation beneath software architecture.
- Local-first, privacy-respecting, portable systems.
- Strong separation of responsibilities and reusable foundations.
- A capture → structure → create → publish value flow.
- Explicit feedback loops, evidence, validation, and iterative evolution.
- Human-readable architecture paired with machine-readable contracts.

## Boundaries intentionally superseded

| Old or ambiguous idea | New decision |
| --- | --- |
| A single Sanctuary-style foundation repo owns all templates, workflows, containers, settings, and tooling | Split by capability: Hygiene, Holon, Pace, Realm, Mantle, Relay, and Egolint |
| Realm contains the shell as an internal subsystem | Mantle is an independent shell/runtime product consumed by Realm |
| Aniflow is the general orchestration layer | Aniflow owns temporal media orchestration; Flow owns cross-holon orchestration |
| Egolint owns reusable GitHub workflow distribution | Egolint owns lint behavior; Relay owns reusable workflow mechanics |
| Empathy is the permanent integration monorepo and component source | Empathy becomes a golden consumer; extracted components release independently |
| Old PNGs are an architecture source of truth | Old visuals are historical references; reviewed text/catalog/diagram source is canonical |
| Website remains the public repo name | Rename to `egohygiene.io`, with redirects and integration repair tracked |
| Nix, Docker, and Dev Containers are one artifact | Realm projects a shared capability model into peer native/Nix/OCI/Dev Container outputs |

## Open decisions before acceptance

1. Approve or revise the five-plane portfolio model.
2. Confirm Hygiene as the canonical ecosystem control-plane repository.
3. Confirm Empathy's final role as golden consumer/integration testbed.
4. Accept the Website → `egohygiene.io` rename and Store's separate deployment boundary.
5. Choose Realm's first toolchain profile after `base`; the architecture deliberately does not lock the full tool list yet.
6. Decide whether the future infrastructure repository should use the working name `firmament` or incubate temporarily elsewhere.
7. Choose which historical diagrams deserve promotion from Athena's archive into Hygiene's approved architecture history.

## Confidence note

The role descriptions for active repositories are grounded in their live READMEs and roots. The role descriptions for seed repositories are proposed target boundaries inferred from their current one-line contracts, the staged source, the user's stated direction, and the need to remove overlap. They should be accepted through one cross-repository architecture decision before parallel implementation begins.
