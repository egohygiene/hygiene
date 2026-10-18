# Ecosystem architecture decisions

This directory contains organization decisions that materially change
cross-repository ownership, dependency direction, platform policy, or the shape
of the Ego Hygiene ecosystem. Product and tool repositories retain their own
local ADRs.

## Accepted ADR foundation

- [Organization ADR policy](POLICY.md)
- [Normative ADR reference template](ADR-TEMPLATE.md)
- [Onboarding and migration](MIGRATION.md)
- [Acceptance and validation plan](VALIDATION.md)
- [ADR-0002 ratification evidence](RATIFICATION.md)
- [Hygiene #47 inventory and migration checkpoint](../adr-workflow/2026-10-10-hygiene-inventory.md)
- [Continuous decision capture and pinned authoring guidance](../adr-workflow/CAPTURE.md)
- [Source-backfill checkpoint and remaining gates](../adr-workflow/2026-10-18-source-backfill.md)
- [ADR front matter schema](../../schemas/architecture-decision.v1.schema.json)
- [Repository policy-reference schema](../../schemas/architecture-decision-policy-reference.v1.schema.json)
- [Compatibility fixtures](../../fixtures/architecture-decisions)
- [Organization contract index](../../catalog/contracts.yaml)

ADR-0002 and policy v1.1.0 are accepted through explicit maintainer approval.
Hygiene provides the canonical contracts and reference checks; reusable agent
promotion, fleet adoption, CI orchestration, generation, and publication remain
owned downstream and are not implemented by this directory.

## Decision index

| ID | Decision | Status | Date |
| --- | --- | --- | --- |
| [ADR-0001](ADR-0001-holistic-architecture-v0.1.md) | Adopt the holistic ecosystem architecture v0.1 | Accepted | 2026-08-18 |
| [ADR-0002](ADR-0002-organization-adr-and-delivery-history.md) | Establish an organization ADR and delivery-history contract | Accepted | 2026-08-20 |
| [ADR-0003](ADR-0003-route-filament-infrastructure-contracts.md) | Route reusable infrastructure contracts to Filament | Proposed | 2026-08-21 |
| [ADR-0004](ADR-0004-register-sanctuary-incubation-boundary.md) | Register Sanctuary as the bounded incubation owner | Proposed | 2026-08-21 |
| [ADR-0005](ADR-0005-unify-repository-intelligence-projection.md) | Unify repository intelligence as a provenance-aware graph projection | Proposed | 2026-08-25 |
| [ADR-0006](ADR-0006-repository-presentation-profile.md) | Define an evidence-backed repository presentation profile | Proposed | 2026-08-30 |
| [ADR-0007](ADR-0007-repository-release-baseline.md) | Define an inheritable repository release-convention baseline | Proposed | 2026-08-31 |
| [ADR-0008](ADR-0008-repository-continuity-policy.md) | Require repository-owned continuity checkpoints through a versioned context successor | Proposed | 2026-09-08 |
| [ADR-0009](ADR-0009-agent-ready-web-profile-foundation.md) | Define the Agent-Ready Web profile foundation | Proposed | 2026-09-14 |
| [ADR-0010](ADR-0010-agent-ready-web-discovery-representations.md) | Specify Agent-Ready Web discovery and representations | Proposed | 2026-09-14 |
| [ADR-0011](ADR-0011-agent-ready-web-guarded-capability-commerce.md) | Guard Agent-Ready Web capability and commerce publication | Proposed | 2026-09-14 |
| [ADR-0012](ADR-0012-agent-ready-web-integration-conformance.md) | Integrate Agent-Ready Web conformance without collapsing authority | Proposed | 2026-09-14 |
| [ADR-0013](ADR-0013-public-site-surface-route-registry.md) | Define the canonical public-site surface and route registry | Proposed | 2026-09-21 |
| [ADR-0014](ADR-0014-json-compatible-catalogs-and-reference-tools.md) | Keep Hygiene catalogs JSON-compatible with dependency-free reference tools | Proposed | 2026-08-19 |

ADR-0001 predates the accepted policy's three-digit filename convention. Its
four-digit identity and original body remain unchanged for provenance. The
Hygiene #47 migration checkpoint records its missing structured metadata and
human-authority evidence review; any migration is a separate reviewed change.
The historical Accepted label is not new ratification by this inventory.

Rejected, deprecated, accepted, and superseded decisions remain discoverable.
A replacement links the record it supersedes, and the old record links back
after the replacement is accepted.
