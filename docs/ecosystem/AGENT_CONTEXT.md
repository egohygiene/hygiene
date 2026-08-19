# Ecosystem Context for Repository Agents

This document is designed to be referenced by every Ego Hygiene repository agent. The canonical copy should live in `egohygiene/hygiene`; a small generated projection should live at `docs/ecosystem/CONTEXT.md` in each repository.

## Required reading order

1. The repository's local `AGENTS.md` and repository-local architecture.
2. Its entry in the pinned `catalog/repositories.yaml` projection.
3. This ecosystem context.
4. Any contract or ADR directly named by the task.

## System rules

1. **One owner per capability.** If a change appears to move a boundary, stop and propose an ecosystem ADR.
2. **Standalone first.** A tool remains independently buildable, testable, documented, and releasable even when Flow, Beacon, Realm, or another facade composes it.
3. **Integrate through releases.** Use pinned packages, binaries, OCI images, reusable workflows, or versioned contracts—never copied sibling source.
4. **Respect control-plane boundaries.** Hygiene defines; Holon creates; Pace converges; Observatory observes.
5. **Respect developer-platform boundaries.** Realm provisions environments; Mantle configures the shell; Relay runs automation; Egolint defines lint behavior; Empathy proves integration.
6. **Preserve provenance.** A staged or imported artifact needs its origin, license, destination owner, migration PR, validation evidence, and removal state.
7. **No secret state.** Images, Nix modules, templates, fixtures, diagrams, and agent context contain no credentials or personal data.
8. **Prefer reversible PRs.** Fleet changes are proposed as small pull requests with generated diffs and explicit rollback.
9. **Do not redefine siblings.** A repository may describe an external capability only by linking to its owned contract and pinning a compatible version.
10. **Update the map.** Architecture-changing work updates Hygiene's catalog/ADRs first or in the same reviewed change set.

## Local projection shape

Every repository should eventually contain a generated file with this shape:

```yaml
architecture_release: architecture-v0.1.0
repository: egohygiene/example
portfolio: developer-platform
status: active
owns:
  - one explicit capability
does_not_own:
  - the adjacent capability most likely to be confused with it
consumes:
  - producer: egohygiene/producer
    contract: artifact-or-schema-name
publishes:
  - artifact-or-contract
canonical_context: https://github.com/egohygiene/hygiene/tree/architecture-v0.1.0/docs/ecosystem
```

The generated Markdown view should add human-readable intent, current migration gate, and links to local docs. Agents may enrich local implementation detail around this projection but must not edit generated ownership fields by hand.

## Definition of done for repository extraction

An extraction from Empathy is complete only when:

- the target repository has the canonical source and preserved attribution/history appropriate to the import;
- standalone install/build/test paths pass on declared platforms;
- release and compatibility contracts exist;
- local ecosystem context is present;
- Empathy consumes a released artifact rather than a relative source copy;
- the staging ledger records verification and the source duplicate is removed in a separate, reviewable cleanup.

## Fast escalation rule

When uncertain, classify the work before coding:

- architecture/policy/catalog → Hygiene;
- AI specs/skills/agents → Aether;
- new-repo generation → Holon;
- existing-repo sync/migration → Pace;
- telemetry/maturity → Observatory;
- environment/image/workstation projection → Realm;
- shell behavior/installers → Mantle;
- GitHub workflow mechanics → Relay;
- lint semantics/reports → Egolint;
- suite orchestration → Flow;
- specialized content behavior → the owning holon;
- release/distribution → Beacon;
- identity tokens/assets → Identity;
- raw archival/reference material → Athena.
