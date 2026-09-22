# Cross-repository dependency boundaries

- Status: **accepted architecture contract implementation**
- Governing decision: [`ADR-0001`](../decisions/ADR-0001-holistic-architecture-v0.1.md)
- Machine source: [`catalog/dependency-boundaries.yaml`](../../catalog/dependency-boundaries.yaml)

## Purpose

The dependency-boundary register turns the accepted ecosystem architecture into
a versioned, machine-readable contract. It records:

- producer and consumer direction;
- the public interface types allowed between repositories;
- immutable or versioned pinning requirements;
- explicitly forbidden direct dependencies;
- stable rule identifiers for validation output; and
- narrow, owned, expiring exceptions.

The register describes allowed integration direction. It does not claim that
every required contract is already published. A relationship with
`contract_status: required` is an explicit delivery gap, not permission to use
copied source or a mutable branch while waiting.

## Default policy

Every cross-repository dependency fails closed unless the register permits its
direction and interface:

1. Source stays in the repository that owns the capability.
2. Consumers use producer-owned schemas, packages, binaries, OCI images,
   reusable workflows, APIs, or deterministic generated projections.
3. Production consumers pin an immutable commit or a versioned release.
4. Mutable default branches such as `main`, `master`, `develop`, `trunk`, and
   `HEAD` are not dependency versions.
5. Unknown dependencies are denied until their owner and contract are reviewed.

Documentation links to a sibling's default branch are allowed because they are
navigation rather than executable dependencies. Dependency manifests,
workflows, container definitions, and machine configuration are scanned.

## Stable rules

| Rule | Requirement |
| --- | --- |
| `BOUNDARY-001` | Do not copy, vendor, or import sibling-owned source. |
| `BOUNDARY-002` | Pin cross-repository dependencies immutably or by version. |
| `BOUNDARY-003` | Integrate only through stable producer-owned interfaces. |
| `BOUNDARY-004` | Compose Aniflow, Optiflow, and Renderflow through Flow. |
| `BOUNDARY-005` | Keep Realm images bounded by explicit capability profiles. |
| `BOUNDARY-006` | Keep secrets and private identity data out of source and artifacts. |
| `BOUNDARY-007` | Preserve review boundaries between Holon, Pace, and Observatory. |
| `BOUNDARY-008` | Keep stable repositories from depending on mutable Sanctuary source. |

## Media-suite boundary

Aniflow, Optiflow, and Renderflow remain independently buildable, testable,
documented, and releasable. None may take a direct source or runtime dependency
on another engine. Flow owns compatibility and composition through their
versioned CLI, library, or JSON contracts.

This prohibition does not prevent documentation links, shared test vocabulary,
or Flow-owned compatibility fixtures that consume released interfaces.

## Incubation boundary

Sanctuary may preserve unfinished source while its owner and value are being
evaluated, but physical presence does not create a durable dependency surface.
Stable repositories must not import or execute mutable Sanctuary source.

Graduation transfers or reconstructs the implementation at one durable owner,
preserves immutable provenance and decision evidence, and gives consumers that
owner's versioned contract. A link to an immutable Sanctuary record may provide
history; it is not the runtime or build dependency.

## Validation and scanning

Validate the register against the repository catalog:

```bash
python3 tools/boundaries.py validate
```

Check that its generated human view is current:

```bash
python3 tools/boundaries.py \
  check-generated \
  --output docs/generated/DEPENDENCY_BOUNDARIES.md
```

Scan a repository checkout:

```bash
python3 tools/boundaries.py scan \
  --repository-root . \
  --repository egohygiene/hygiene
```

The local scanner deterministically reports:

- sibling-owned source stored under `.staging/<sibling>`,
  `third_party/<sibling>`, `vendor/<sibling>`, or `vendored/<sibling>`;
- dependency paths that escape the repository root; and
- Ego Hygiene sibling references that pin a mutable default branch in
  workflows, manifests, lockfiles, container definitions, or machine
  configuration.

The scanner intentionally does not attempt to prove source originality from
content similarity. Fleet-wide hash/provenance comparison and enforcement in
consumer CI belong to Relay after the contract is adopted. A clean local scan
means no supported violation was found; it is not a security or license audit.

## Exception process

An exception is a narrow deviation from one named `BOUNDARY-NNN` rule. It must
be added to the register with:

- a stable `EXCEPTION-NNN` identifier;
- the affected rule and repositories;
- one repository owner;
- a concrete reason;
- `proposed`, `approved`, or `expired` status;
- durable human approval evidence for approved or expired exceptions; and
- an ISO expiry date.

`proposed` exceptions grant no authority. The validator rejects approved
exceptions without an owner, approval link, or expiry. Expired exceptions stay
in history until a reviewed cleanup or superseding decision removes the need.
Exceptions cannot authorize secret publication, fabricate evidence, or move a
capability away from its canonical owner.

## Ownership and rollout

- Hygiene owns the register, schema, rule semantics, and exception records.
- Aether may package pinned authoring guidance but must not redefine the rules.
- Holon may scaffold the pinned contract into new repositories.
- Relay owns reusable fleet validation after this local reference validator is
  accepted.
- Pace may propose reviewable updates to existing repositories.
- Observatory may report conformance evidence but must not silently remediate.
- Each producer owns and versions its actual integration contract.

Repository continuity preserves that split: Aether owns the portable
specification, schema, template, skill, and managed instruction projection;
Hygiene consumes an immutable revision and owns organization applicability,
required-file composition, rollout, migration, and exceptions. Egolint, Holon,
Relay, Observatory, and Pace consume the proposed Hygiene policy through their
linked follow-up issues rather than placing their implementations here.

The Agent-Ready Web relationship follows the same control-plane boundary.
Hygiene owns the proposed integrated profile and conformance schemas,
independent concern resolution, cross-layer authority denials, diagnostics,
evidence shape, compatibility, reference review, and lifecycle. Consumers use
an exact released version with resolved revision and digest, or an immutable
repository revision with digest; they do not copy Hygiene policy. The current
proposed pin is review- and compatibility-test-only.

Holon may later scaffold and generate for new sites from an eligible immutable
pin. Relay may implement reusable validation and publication workflows and
transport privacy-safe evidence. Pace may plan reviewed adoption and propose
reversible existing-site rollout and convergence. Store retains transaction-
domain capability contracts. Observatory may collect privacy-safe evidence and
aggregate metrics. Sites retain their facts, site class, credentials, consent
interaction, configuration, represented revision, and final publication
authority. The relationship remains `required`; this repository does not claim
those downstream implementations, any passing site state, adoption,
publication, monitoring, or enforcement.

The public-site surface relationship preserves a separate policy, artifact,
execution, and publication boundary. Hygiene owns stable surface IDs, route
profiles and bindings, base-path resolution, applicability and state semantics,
schemas, compatibility, dependency rules, and privacy boundaries; it neither
renders nor publishes a site. A declaring repository owns its facts and source
evidence, while the named publication repository retains final route
composition, hosting, credentials, deployment, rollback, and publication
authority. `egohygiene/website` remains the current catalog identity for the
renamed `egohygiene.io` site; this proposed relationship does not perform the
separate catalog reconciliation.

Relay may implement reusable validation, redirect, rendering, and publication
mechanics without acquiring site authority. Renderflow owns versioned magazine
and presentation transformation artifacts, and Identity retains the
`/identity/` product experience plus versioned brand and asset inputs; neither
owns a consuming site's declaration or deployment. Holon may scaffold complete
new-repository declarations from an eligible immutable pin, Observatory may
normalize only privacy-safe declarations and freshness evidence, and Pace may
propose reviewed adoption changes without direct default-branch mutation. The
relationship remains `required` while the registry and declaration contracts
are proposed; it records a delivery boundary, not downstream implementation,
adoption, or publication.

The continuity relationships remain `required` instead of `active` while the
Aether artifacts are draft and the Hygiene profile is proposed. This is a
lifecycle statement, not permission to use a mutable default-branch dependency.
See [`REPOSITORY_CONTINUITY.md`](REPOSITORY_CONTINUITY.md) for the immutable pin
and promotion gates.

Changes to dependency direction, ownership, allowed interface types, or a
forbidden relationship require an architecture review. Routine additions of a
new released version under an existing relationship do not redefine this
register.
