# ADR onboarding and migration

This guide migrates existing repositories without rewriting architectural
history or treating generated files as canonical source.

## Rollout modes

### Validate first

Use when a repository already has `DECISIONS.md`, detailed ADRs, custom agent
instructions, or an intelligence/site integration.

1. Inventory every decision ID, title, status claim, link, and canonical
   location.
2. Identify duplicates, ID collisions, missing approval evidence, and local
   conventions.
3. Record a migration map before moving or rewriting anything.
4. Ask a human to resolve ambiguous canonical records and acceptance claims.
5. Add front matter or extract records in small pull requests that preserve the
   original body, blame context, and provenance.

### Scaffold first

Use when no durable local decision log exists.

1. Add `docs/decisions/README.md` as the canonical local index.
2. Add `docs/decisions/policy-reference.json`, pinning an approved Hygiene
   policy version and full commit through
   `egohygiene.architecture-decision-policy-reference/v1`.
3. Add a proposed ADR only when the scoped change requires one.
4. Do not reconstruct historical decisions without contemporaneous evidence.

### Managed projection

Use only for files explicitly marked as generated or pinned, including
`docs/ecosystem/CONTEXT.md`, a concise shared-instruction reference, and thin
workflow callers. Holon defines the artifact; Pace proposes later updates.

Repository-owned ADRs, their rationale, and local implementation evidence are
never overwritten by a managed projection.

## Existing patterns found in the audit

- Hygiene has a detailed four-digit `ADR-0001` without YAML front matter.
- Identity has inline ADR-001 through ADR-003 and detailed ADR-004 through
  ADR-011.
- Optiflow uses an established `OFD-NNN` inline convention.
- Empathy has two different records identified as ADR-0001, one inline and one
  detailed. The collision must be resolved by human review before migration.
- Several repositories contain compact reconstructed records described as
  accepted without durable human-approval evidence.
- Aether retains a legacy draft decision specification and now also contains a
  draft decision-impact hook pinned to a proposed Hygiene revision. The pinned
  consumer demonstrates the intended boundary but does not activate policy.

These are migration inputs, not authorization to renumber records, change their
meaning, or retroactively accept them.

## Migration rules

1. **Preserve identity.** Never reuse an ID. Retain historical prefixes and
   digit widths with an exception when changing them would break provenance.
2. **Preserve content.** Do not silently rewrite original context, rationale,
   alternatives, or consequences to satisfy a new template.
3. **Preserve authority.** A legacy `accepted` label without clear approval is
   recorded as an evidence gap. A human decides whether to retain, correct, or
   supersede the status.
4. **Preserve lineage.** Do not delete superseded or deprecated records. Link
   replacements in both directions.
5. **Avoid duplicate truth.** When extracting an inline record, replace its full
   text with a concise index link in the same reviewed migration.
6. **Use aliases only for discovery.** If an old identifier must remain
   searchable, record it in the migration note; do not create a second ADR with
   the same decision content.
7. **Fail closed on collisions.** Freeze both records, document the conflict,
   and require human selection of the canonical identity before generation.
8. **Keep proposals proposed.** Migration mechanics do not supply missing
   acceptance or implementation evidence.
9. **Pin before projecting.** A repository policy reference names an exact
   supported policy version and full Hygiene commit. Moving branch references
   and copied policy prose are invalid.
10. **Register extensions.** Preserve local fields under a versioned,
    repository-owned extension contract. Do not reinterpret a legacy local
    status or approval field as a global override.

## Policy-version upgrades

Treat a policy pin update as a reviewed migration, not a dependency refresh:

1. read the target policy changelog and migration guidance;
2. validate the repository's reference, ADR metadata, indexes, extensions, and
   lineage against the target revision;
3. record any incompatibility as a proposed exception or a blocking migration
   issue rather than weakening validation;
4. update the semantic version and full commit pin together; and
5. retain the prior pin in Git history and attach the validation result to the
   upgrade pull request.

Patch releases may require only deterministic revalidation. Minor releases may
introduce optional features or new lifecycle values that consumers must support
before use. A major contract upgrade requires an explicit repository migration
plan; unsupported versions fail closed.

## Per-repository rollout classification

The read-only audit proposes this first operation for the current fleet:

| First operation | Repositories |
| --- | --- |
| Validate existing history and integrations | `.github`, `aether`, `akashic`, `athena`, `beacon`, `egolint`, `empathy`, `filament`, `holon`, `hygiene`, `identity`, `mantle`, `mindcap`, `mindgarden`, `observatory`, `optiflow`, `pace`, `realm`, `reflector`, `relay`, `renderflow`, `store` |
| Scaffold missing decision structure | `aniflow`, `egohygiene`, `egohygiene.io`, `flow` |

All repositories move to managed mode only for generated or pinned artifacts
after Phase 2 defines provenance markers and migration-safe ownership rules.

## Rollout sequence

1. Pin the accepted ADR-002 policy revision and its durable human approval
   evidence.
2. Release Aether's pinned reusable instruction module; retain its legacy policy
   text only as clearly non-canonical migration evidence.
3. Define Holon scaffold/validate artifacts and provenance markers.
4. Implement Egolint semantic rules and Relay CI/generation mechanics with
   fixtures for every legacy pattern above.
5. Pilot Identity with an explicit migration map and no mechanical history
   rewrite.
6. Implement Observatory aggregation only after repository contracts are
   stable.
7. Use Pace to roll out grouped repository pull requests, stopping for review
   after each group.

## Migration completion evidence

A repository is migrated only when:

- `docs/decisions/policy-reference.json` resolves an approved, supported Hygiene
  policy version at the pinned full commit;
- local IDs are unique or every unresolved collision blocks generation;
- every canonical detailed record has schema-valid front matter or a documented
  migration exception;
- status and implementation claims link real evidence or declare an evidence
  gap;
- the local index points to one canonical record per decision;
- cross-repository references resolve without redefining ownership;
- generated files identify their source policy version and generator revision;
  and
- public output passes the privacy rules in [`POLICY.md`](POLICY.md).
