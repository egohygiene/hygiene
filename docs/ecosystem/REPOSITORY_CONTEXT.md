# Repository-local ecosystem context contract

Status: **version 2 proposed executable successor; version 1 deprecated**

Owner: `egohygiene/hygiene`

## Purpose

Each Ego Hygiene repository receives a compact `docs/ecosystem/CONTEXT.md`
projection so agents and maintainers can understand that repository's place in
the ecosystem without copying the complete organization architecture.

The canonical inputs are:

- `catalog/repositories.yaml` for repository identity, ownership, lifecycle,
  consumed inputs, and outputs; and
- `catalog/repository-context.json` for v2 projection structure, relationship
  resolution, required markers, canonical links, stale-context behavior, and
  the continuity-policy pointer; and
- `catalog/repository-continuity-policy.json` for applicability, exact required
  files, immutable Aether provenance, rollout, exceptions, and migration.

The generated projection is never a second architecture source. Ownership and
dependency changes begin in the Hygiene catalog or a governing decision, then
flow into repository projections through a reviewed update.

## Version-2 sections

Every context contains:

1. source and version markers;
2. repository identity and lifecycle;
3. owned, excluded, and published capabilities;
4. repository dependencies, consumed inputs, and external inputs;
5. direct upstream and downstream neighbors;
6. global and repository-specific constraints;
7. immutable links to the source Hygiene revision;
8. explicit upgrade and stale-context behavior; and
9. the Hygiene continuity-policy version, Aether contract identity, exact
   repository-owned paths, and resume/handoff triggers.

The Markdown header includes the stable
`<!-- egohygiene-context: repository-context/v2 -->` marker, architecture
release, source revision, repository identity, and generator identity. EgoLint
can verify these markers without fetching Hygiene during a lint run.

The projection points to `CONTINUITY.md`; it does not copy the repository-owned
handoff. Its continuity section is policy context, not current execution state.

## Generation and verification

Generate one repository projection:

```bash
python3 tools/context.py render \
  --repository "egohygiene/empathy" \
  --source-revision "<40-character-hygiene-commit>" \
  --output "docs/ecosystem/CONTEXT.md"
```

Verify a checked-in projection byte-for-byte:

```bash
python3 tools/context.py check \
  --repository "egohygiene/empathy" \
  --source-revision "<40-character-hygiene-commit>" \
  --output "docs/ecosystem/CONTEXT.md"
```

`render-all` emits one projection per current catalog entry for release or
fleet tooling. Holon may consume this contract when creating repositories; Pace
owns reviewed fleet upgrades. Neither tool may silently redefine the context.

## Upgrade and stale behavior

The `architecture_release` field is the compatibility comparison key. A
mismatch fails closed: consumers keep their current reviewed projection until
Pace or a maintainer regenerates it from the newly selected immutable Hygiene
release and reviews the diff. Generated content must never overwrite local
architecture detail outside the owned `CONTEXT.md` path.

The canonical `contracts/repository-context.toml` projection supplies EgoLint's
offline repository-contract envelope. Version 2 requires exact-case root
`AGENTS.md` and `CONTINUITY.md` as repository-owned regular files plus generated
`docs/ecosystem/CONTEXT.md`. The root instruction file retains local prose and
contains exactly one managed Aether continuity block.

Its immutable source revision points to the policy input in this repository,
not to a mutable branch. The v2 envelope remains provisional during observe
because the Hygiene policy is proposed and the pinned Aether artifacts remain
draft.

## Compatibility and migration

Adding mandatory root files is a breaking contract change, so v2 uses major
version `2.0.0`; it is not presented as an additive v1 revision. The exact
prior artifact remains at `contracts/repository-context.v1.toml` and the v1
schema remains available with deprecated status.

Existing reviewed consumers may retain their immutable v1 pin until one
bounded migration adds repository-specific continuity, reconciles the managed
instruction block, regenerates ecosystem context, and moves the local pin to
v2. New consumers do not select v1.

Rollback returns the policy to observe and repins v1. It preserves useful
repository-owned continuity state and all Git evidence; it does not pretend a
failed migration never occurred. Full applicability, deprecation, exception,
and rollout rules are in
[`REPOSITORY_CONTINUITY.md`](REPOSITORY_CONTINUITY.md).
