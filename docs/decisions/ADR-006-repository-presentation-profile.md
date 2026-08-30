---
schema: egohygiene.architecture-decision/v1
id: ADR-006
title: Define an evidence-backed repository presentation profile
status: proposed
date: 2026-08-30
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/22
pull_request: https://github.com/egohygiene/hygiene/pull/24
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/*
affected_contracts:
  - egohygiene.repository-presentation-profile/v1
  - egohygiene.repository-presentation-evidence/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/22
    description: Approved implementation scope and downstream ownership graph.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/24
    description: Review surface for the profile, schemas, fixtures, validator, documentation, and tests.
exceptions: []
approval: null
---

# ADR-006: Define an evidence-backed repository presentation profile

## Context

Ego Hygiene repositories use varied README structures, banner assets, badge
providers, maturity language, and navigation. Copying one attractive README to
every repository would overwrite repository-specific facts and encourage
badges that look authoritative without identifying evidence, freshness, or the
represented revision.

The organization needs one semantic presentation baseline that supports a
centered Identity banner, useful repository orientation, and an honest Hygiene
badge while preserving repository ownership and applicability. The contract
must precede Identity assets, Holon templates, Egolint rules, and Pace rollout.

## Decision

Propose `egohygiene.repository-presentation-profile/v1` and
`egohygiene.repository-presentation-evidence/v1` at `1.0.0-alpha.1`.

The profile defines semantic slots, a four-level applicability vocabulary,
repository-type/visibility/lifecycle overrides, evidence states, fail-closed
badge derivation, generated-region composition, and cross-repository ownership.
The evidence contract binds a resolved assessment and badge descriptor to an
exact profile version and represented commit.

The Hygiene badge reports only the named repository-presentation profile. It
must not say or imply that a repository is legally compliant, certified,
universally secure, or otherwise trustworthy beyond the linked evidence.

Hygiene owns policy meaning. Identity owns visual assets and descriptors;
Holon owns new-repository composition; Egolint owns lint semantics; Relay owns
reusable orchestration; Pace owns reviewable existing-fleet adoption;
Observatory owns read-only aggregation; repositories retain their facts and
final review.

## Alternatives considered and rejected

### Mandate one complete README template

Rejected because repository classes need different content, existing READMEs
contain valuable local prose, and full-file replacement would create drift and
fabricated placeholders.

### Treat badge presence as conformance

Rejected because an image can be stale, cached, copied, or disconnected from
the represented commit. The badge is a projection of a versioned evidence
document, not evidence by itself.

### Use “hygienic and compliant” as the success claim

Rejected because the profile does not establish legal compliance, complete
security, universal accessibility, or fitness. Precise profile-state language
is more useful and defensible.

### Let each implementation define applicability

Rejected because Identity, Holon, Egolint, Pace, Relay, and Observatory would
derive different answers. Hygiene must own deterministic override precedence
and state semantics.

### Require a hosted badge service

Rejected because no-network and long-term rendering should remain useful.
Hosted badges may be optional projections over local descriptors and evidence.

## Consequences and tradeoffs

- Repositories share a polished, recognizable baseline without identical
  prose.
- Identity #54 receives an exact visual input boundary.
- Honest unknown, stale, partial, blocked, exempt, and not-applicable states
  remain visible.
- Consumers must resolve applicability and preserve generated-region
  boundaries, which is more work than copying Markdown.
- Alpha consumers must pin the exact version and may need migrations before v1
  activation.
- A passing presentation profile remains a narrow claim, not a substitute for
  product, security, legal, or accessibility review.

## Implementation and evidence links

The proposed profile, schemas, reference validator, synthetic minimal/rich
fixtures, documentation, and tests are implemented with issue #22. Downstream
implementation is tracked by Identity #54, Holon #24, Egolint #27, and Pace
#14. Observatory reporting may follow the released evidence contract without
blocking rollout.

## Replacement or exit strategy

Additive optional fields may evolve within v1 under explicit compatibility
rules. Changes to requirement meanings, override precedence, badge-state
derivation, claims policy, ownership, or required evidence require a proposed
major-version replacement and migration fixtures.

Because repository facts remain local and generated sections are bounded, a
future profile can replace this one without rewriting canonical repository
history or custom prose.

## Follow-up work

1. Obtain explicit maintainer review before activating either contract.
2. Implement Identity #54 and Holon #24 against an immutable profile pin.
3. Implement Egolint #27 and validate reference fixtures.
4. Pilot representative repositories before Pace #14 proposes fleet changes.
5. Add Observatory aggregation after the released evidence boundary exists.
