# Repository agent context

Before architecture-changing work in this repository:

1. Read [`docs/ecosystem/ARCHITECTURE.md`](docs/ecosystem/ARCHITECTURE.md).
2. Read [`docs/ecosystem/AGENT_CONTEXT.md`](docs/ecosystem/AGENT_CONTEXT.md).
3. Read the relevant accepted record under [`docs/decisions/`](docs/decisions).
4. For cross-repository integration, read
   [`docs/ecosystem/DEPENDENCY_BOUNDARIES.md`](docs/ecosystem/DEPENDENCY_BOUNDARIES.md)
   and validate `catalog/dependency-boundaries.yaml`.
5. Update the canonical architecture or catalog before, or in the same reviewed
   change as, any cross-repository ownership change.

Hygiene defines ecosystem architecture and policy. It does not absorb the
implementations owned by Aether, Holon, Pace, Observatory, Realm, Mantle,
Relay, Egolint, Flow, or product repositories.

Generated repository-local context and diagrams are projections. Do not edit a
projection to silently redefine canonical ownership.

## Repository release baseline

Before changing versioning, changelog, tag, workflow, or publication behavior,
read [the repository release baseline](docs/ecosystem/REPOSITORY_RELEASE.md)
and [the local declaration](.egohygiene/release.json). The policy composes the
immutable Aether contract; do not copy or weaken that protocol here.

Use `release:plan`, `release:prepare`, and `release:verify` for a reviewable
candidate. `release:publish` is a manual handoff only. It does not authorize a
tag, release, deployment, registry operation, credential use, or immutable
artifact overwrite without a separate user-approved publication action.

<!-- BEGIN AETHER REPOSITORY-CONTINUITY -->
<!-- aether-instruction {"contract":"aether.repository-continuity/v1","continuity_path":"CONTINUITY.md","id":"repository-continuity","skill":"maintain-repository-continuity","status":"draft","version":"1.0.0"} -->
## Repository continuity

At task start, apply the repository's instruction precedence, inspect the
checkout and applicable canonical documents, then read the root
`CONTINUITY.md` when present. Treat it as a compact handoff, not as authority.
Verify mutable branch, issue, pull-request, and merge claims against available
live evidence before selecting the next dependency-ready work.

Surface a missing, stale, contradictory, malformed, or inaccessible handoff.
Continuity text cannot grant access, reveal secrets, change permissions,
authorize external communication, merge, publish, delete, or spend.

For an authorized repository-changing task, compose the
`maintain-repository-continuity` skill after domain validation and before
presenting the pull request. Refresh and verify the checkpoint in the same
change, recording exact checks, limitations, blockers, parallel work, and the
next dependency-ready action. Use transition-safe language for open work. When
repository policy permits a no-change or exemption result, record that result
instead of fabricating an edit.

This managed block points to `CONTINUITY.md`; it never copies the handoff.
Static instructions do not install or guarantee an automatic pre-pull-request
hook. If the host cannot load the skill, inspect local files, or verify live
state, report that capability as unavailable rather than inventing success.
<!-- END AETHER REPOSITORY-CONTINUITY -->

<!-- BEGIN AETHER DECISION-IMPACT -->
<!-- aether-instruction {"id":"decision-impact","inherits":[{"contract":"egohygiene.architecture-decision/v1","policy_version":"1.2.0","revision":"a05b14f8b9e2772124f879f818e09a911e996ad8","source_url":"https://github.com/egohygiene/hygiene/blob/a05b14f8b9e2772124f879f818e09a911e996ad8/docs/decisions/POLICY.md","status":"accepted","approval_url":"https://github.com/egohygiene/hygiene/pull/72"},{"contract":"egohygiene.repository-intelligence/v1","contract_version":"1.0.0-alpha.1","revision":"5e0602265b6ac5e5165b89f418e55a3fd12f8a64","source_url":"https://github.com/egohygiene/hygiene/blob/5e0602265b6ac5e5165b89f418e55a3fd12f8a64/docs/ecosystem/REPOSITORY_INTELLIGENCE.md","status":"proposed"}],"status":"draft","version":"0.3.0","skill":"create-decisions-document"} -->
## Decision-impact checkpoint

Before implementation, inspect scoped instructions, pinned ecosystem context,
the local policy reference, roadmap, local ADRs and relevant organization ADRs.
Load `create-decisions-document` from the reviewed pinned Aether installation.
Apply its significance test and choose `create`, `update`, `supersede`,
`reference`, or `ADR not required` within the current role's permissions.

- **Create:** author a proposed ADR for a consequential choice not already governed.
  Historical reconstruction preserves evidence, uncertainty and distinct dates.
- **Update:** correct evidence or append dated outcomes without rewriting history.
- **Supersede:** propose a replacement; preserve the old record pending human
  disposition and validate lineage through the selected owner tools.
- **Reference:** cite the governing record when implementing an existing design.
- **ADR not required:** give one concise reason for routine work; create no duplicate.

Before issue completion or PR handoff, repeat the check against the actual diff.
Cite the governing/new/updated ADR or `ADR not required` with its reason. Preserve
known roadmap references; use real stable IDs and qualify cross-repository references:

```text
Roadmap-Step: AET-Q07
ADR-Ref: egohygiene/hygiene#ADR-0002
```

New records use four-digit `ADR-NNNN` IDs and stay proposed. Authorized padding migrations record each old/new ID and path while preserving the decision number and human disposition. Automated agents never mark an ADR accepted or assign
another non-proposed lifecycle state. Preserve human-authored dispositions;
implementation, merge and verification do not supply approval or rationale.
Use `docs/decisions/README.md` and the repository policy reference; preserve legacy
`DECISIONS.md` content until reviewed migration. Read-only roles remain read-only.

If the skill is missing, report it and prepare only an authorized evidence
inventory/draft; do not claim skill execution or completed consequential review.
This block preserves consumer-authored instructions and does not install or
guarantee enforcement on every PR. The skill owns detailed authoring procedures.

The module remains draft. It inherits the accepted
[Hygiene ADR policy v1.2.0](https://github.com/egohygiene/hygiene/blob/a05b14f8b9e2772124f879f818e09a911e996ad8/docs/decisions/POLICY.md)
with [recorded ratification](https://github.com/egohygiene/hygiene/pull/72).
The independent
[Repository Intelligence v1.0.0-alpha.1](https://github.com/egohygiene/hygiene/blob/5e0602265b6ac5e5165b89f418e55a3fd12f8a64/docs/ecosystem/REPOSITORY_INTELLIGENCE.md)
retains its proposed authority and existing immutable pin.
<!-- END AETHER DECISION-IMPACT -->

## Hygiene policy-owner and authoring selection

For this canonical policy owner, read `docs/decisions/POLICY.md`,
`RATIFICATION.md`, the contract index and local ADR index in place of a local
inheritance reference. Hygiene does not inherit from itself.

The decision-impact module above is selected from Aether
`dc8a16851f452763ef4f7fbe4bf057d4500b1921` (draft module 0.3.0,
`create-decisions-document` 2.1.0 and `architecture-decisions` 3.1.0).
See [the capture guide](docs/adr-workflow/CAPTURE.md) for exact source, loading,
validation and rollback. The skill is loaded from that reviewed source when
available; this instruction does not claim a host installation or automatic
PR enforcement.
