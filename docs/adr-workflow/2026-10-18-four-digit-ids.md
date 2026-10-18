# Four-digit ADR identifiers — 2026-10-18

The maintainer selected **four digits** and authorized the existing-record migration,
shared authoring standard and reviewed merges on 2026-10-18. This records that
specific naming decision; it does not approve unrelated architectural proposals
or fill missing historical approval evidence.

Canonical new identifiers use `ADR-NNNN`, for example `ADR-0001` and
`ADR-0024`. Keep the decision number, original date, rationale, disposition,
implementation state and approval evidence. Change padding and current references
together. Existing immutable citations and dated validation receipts retain the
identifiers they actually observed.

## Scope and dependency order

The reviewed default branches contain 37 three-digit canonical files: 13 in
Hygiene and 24 in Identity. The existing four-digit records need no ID change.
Each changed repository records its own exact old-to-new map. This change does
not add a redirect framework or promise preservation of unused old site URLs;
the prior files and references remain recoverable from Git history.

1. Hygiene: policy amendment, reference validation, examples and this corpus/map.
2. EgoLint: explicit compatible policy selection and four-digit conformance.
3. Relay: immutable adoption in both runtimes and production collection.
4. Aether/Holon: canonical specification, skill, examples and scaffolding.
5. Consumers: exact pins, canonical IDs, current cross-references and local map.

The numbering work is in progress. No pending downstream merge or validation
result is inferred by this preparation record. Hygiene #47's independent
historical approval/source-publication gate remains visible.

## Hygiene mapping

| Previous ID | Canonical ID | Previous path | Canonical path |
| --- | --- | --- | --- |
| `ADR-002` | `ADR-0002` | `docs/decisions/ADR-002-organization-adr-and-delivery-history.md` | `docs/decisions/ADR-0002-organization-adr-and-delivery-history.md` |
| `ADR-003` | `ADR-0003` | `docs/decisions/ADR-003-route-filament-infrastructure-contracts.md` | `docs/decisions/ADR-0003-route-filament-infrastructure-contracts.md` |
| `ADR-004` | `ADR-0004` | `docs/decisions/ADR-004-register-sanctuary-incubation-boundary.md` | `docs/decisions/ADR-0004-register-sanctuary-incubation-boundary.md` |
| `ADR-005` | `ADR-0005` | `docs/decisions/ADR-005-unify-repository-intelligence-projection.md` | `docs/decisions/ADR-0005-unify-repository-intelligence-projection.md` |
| `ADR-006` | `ADR-0006` | `docs/decisions/ADR-006-repository-presentation-profile.md` | `docs/decisions/ADR-0006-repository-presentation-profile.md` |
| `ADR-007` | `ADR-0007` | `docs/decisions/ADR-007-repository-release-baseline.md` | `docs/decisions/ADR-0007-repository-release-baseline.md` |
| `ADR-008` | `ADR-0008` | `docs/decisions/ADR-008-repository-continuity-policy.md` | `docs/decisions/ADR-0008-repository-continuity-policy.md` |
| `ADR-009` | `ADR-0009` | `docs/decisions/ADR-009-agent-ready-web-profile-foundation.md` | `docs/decisions/ADR-0009-agent-ready-web-profile-foundation.md` |
| `ADR-010` | `ADR-0010` | `docs/decisions/ADR-010-agent-ready-web-discovery-representations.md` | `docs/decisions/ADR-0010-agent-ready-web-discovery-representations.md` |
| `ADR-011` | `ADR-0011` | `docs/decisions/ADR-011-agent-ready-web-guarded-capability-commerce.md` | `docs/decisions/ADR-0011-agent-ready-web-guarded-capability-commerce.md` |
| `ADR-012` | `ADR-0012` | `docs/decisions/ADR-012-agent-ready-web-integration-conformance.md` | `docs/decisions/ADR-0012-agent-ready-web-integration-conformance.md` |
| `ADR-013` | `ADR-0013` | `docs/decisions/ADR-013-public-site-surface-route-registry.md` | `docs/decisions/ADR-0013-public-site-surface-route-registry.md` |
| `ADR-014` | `ADR-0014` | `docs/decisions/ADR-014-json-compatible-catalogs-and-reference-tools.md` | `docs/decisions/ADR-0014-json-compatible-catalogs-and-reference-tools.md` |

The existing `ADR-0001` already uses four digits and keeps its original source.
Normalizing other IDs does not supply its missing structured historical approval.

## Verification and recovery

Check unique four-digit canonical IDs, matching filenames/front matter/headings,
one index row per record, local and cross-repository lineage, the migration map,
and exact supported policy/runtime pins. Run each owner's normal tests and retain
actual hosted outcomes. Revert the corresponding reviewed change to restore the
previous names and references together; do not mix old names with new metadata.
