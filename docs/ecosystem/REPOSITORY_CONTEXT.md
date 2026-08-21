# Repository-local ecosystem context contract

Status: **version 1 executable contract**

Owner: `egohygiene/hygiene`

## Purpose

Each Ego Hygiene repository receives a compact `docs/ecosystem/CONTEXT.md`
projection so agents and maintainers can understand that repository's place in
the ecosystem without copying the complete organization architecture.

The canonical inputs remain:

- `catalog/repositories.yaml` for repository identity, ownership, lifecycle,
  consumed inputs, and outputs; and
- `catalog/repository-context.json` for projection structure, relationship
  resolution, required markers, canonical links, and stale-context behavior.

The generated projection is never a second architecture source. Ownership and
dependency changes begin in the Hygiene catalog or a governing decision, then
flow into repository projections through a reviewed update.

## Version-1 sections

Every context contains:

1. source and version markers;
2. repository identity and lifecycle;
3. owned, excluded, and published capabilities;
4. repository dependencies, consumed inputs, and external inputs;
5. direct upstream and downstream neighbors;
6. global and repository-specific constraints;
7. immutable links to the source Hygiene revision; and
8. explicit upgrade and stale-context behavior.

The Markdown header includes the stable
`<!-- egohygiene-context: repository-context/v1 -->` marker, architecture
release, source revision, repository identity, and generator identity. EgoLint
can verify these markers without fetching Hygiene during a lint run.

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
offline repository-contract envelope. Its immutable source revision points to
the policy input in this repository, not to a mutable branch.
