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
- [ADR-002 ratification evidence](RATIFICATION.md)
- [ADR front matter schema](../../schemas/architecture-decision.v1.schema.json)
- [Repository policy-reference schema](../../schemas/architecture-decision-policy-reference.v1.schema.json)
- [Compatibility fixtures](../../fixtures/architecture-decisions)
- [Organization contract index](../../catalog/contracts.yaml)

ADR-002 and policy v1.1.0 are accepted through explicit maintainer approval.
Hygiene provides the canonical contracts and reference checks; reusable agent
promotion, fleet adoption, CI orchestration, generation, and publication remain
owned downstream and are not implemented by this directory.

## Decision index

| ID | Decision | Status | Date |
| --- | --- | --- | --- |
| [ADR-0001](ADR-0001-holistic-architecture-v0.1.md) | Adopt the holistic ecosystem architecture v0.1 | Accepted | 2026-08-18 |
| [ADR-002](ADR-002-organization-adr-and-delivery-history.md) | Establish an organization ADR and delivery-history contract | Accepted | 2026-08-20 |
| [ADR-003](ADR-003-route-filament-infrastructure-contracts.md) | Route reusable infrastructure contracts to Filament | Proposed | 2026-08-21 |
| [ADR-004](ADR-004-register-sanctuary-incubation-boundary.md) | Register Sanctuary as the bounded incubation owner | Proposed | 2026-08-21 |
| [ADR-005](ADR-005-unify-repository-intelligence-projection.md) | Unify repository intelligence as a provenance-aware graph projection | Proposed | 2026-08-25 |
| [ADR-006](ADR-006-repository-presentation-profile.md) | Define an evidence-backed repository presentation profile | Proposed | 2026-08-30 |
| [ADR-007](ADR-007-repository-release-baseline.md) | Define an inheritable repository release-convention baseline | Proposed | 2026-08-31 |
| [ADR-008](ADR-008-repository-continuity-policy.md) | Require repository-owned continuity checkpoints through a versioned context successor | Proposed | 2026-09-08 |
| [ADR-009](ADR-009-agent-ready-web-profile-foundation.md) | Define the Agent-Ready Web profile foundation | Proposed | 2026-09-14 |
| [ADR-010](ADR-010-agent-ready-web-discovery-representations.md) | Specify Agent-Ready Web discovery and representations | Proposed | 2026-09-14 |
| [ADR-011](ADR-011-agent-ready-web-guarded-capability-commerce.md) | Guard Agent-Ready Web capability and commerce publication | Proposed | 2026-09-14 |
| [ADR-012](ADR-012-agent-ready-web-integration-conformance.md) | Integrate Agent-Ready Web conformance without collapsing authority | Proposed | 2026-09-14 |

ADR-0001 predates the proposed three-digit filename convention. Its four-digit
identity and original body remain unchanged for provenance. If the new policy is
accepted, migration metadata will be added in a separate reviewed change rather
than rewriting its history in this proposal.

Rejected, deprecated, accepted, and superseded decisions remain discoverable.
A replacement links the record it supersedes, and the old record links back
after the replacement is accepted.
