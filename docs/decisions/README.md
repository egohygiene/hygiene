# Ecosystem architecture decisions

This directory contains organization decisions that materially change
cross-repository ownership, dependency direction, platform policy, or the shape
of the Ego Hygiene ecosystem. Product and tool repositories retain their own
local ADRs.

## Proposed ADR foundation

- [Organization ADR policy](POLICY.md)
- [Normative ADR reference template](ADR-TEMPLATE.md)
- [Onboarding and migration](MIGRATION.md)
- [Acceptance and validation plan](VALIDATION.md)
- [ADR front matter schema](../../schemas/architecture-decision.v1.schema.json)
- [Organization contract index](../../catalog/contracts.yaml)

These foundation artifacts remain proposals until ADR-002 receives explicit
human approval. Reusable agent packaging, validation, generation, and dashboards
are not implemented by this directory.

## Decision index

| ID | Decision | Status | Date |
| --- | --- | --- | --- |
| [ADR-0001](ADR-0001-holistic-architecture-v0.1.md) | Adopt the holistic ecosystem architecture v0.1 | Accepted | 2026-08-18 |
| [ADR-002](ADR-002-organization-adr-and-delivery-history.md) | Establish an organization ADR and delivery-history contract | Proposed | 2026-08-20 |
| [ADR-003](ADR-003-route-filament-infrastructure-contracts.md) | Route reusable infrastructure contracts to Filament | Proposed | 2026-08-21 |

ADR-0001 predates the proposed three-digit filename convention. Its four-digit
identity and original body remain unchanged for provenance. If the new policy is
accepted, migration metadata will be added in a separate reviewed change rather
than rewriting its history in this proposal.

Accepted decisions remain discoverable when superseded. A replacement links the
record it supersedes, and the old record links back after the replacement is
accepted.
