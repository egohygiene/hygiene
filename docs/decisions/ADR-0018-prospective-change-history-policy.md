---
schema: egohygiene.architecture-decision/v1
id: ADR-0018
title: Define prospective change-history semantics separately from release authority and historical normalization
status: proposed
date: "2026-11-12"
decision_scope: organization
visibility: public
owners: [egohygiene/hygiene]
issue: https://github.com/egohygiene/hygiene/issues/37
pull_request: null
related: [ADR-0002, ADR-0007]
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/aether
  - egohygiene/egolint
  - egohygiene/relay
  - egohygiene/holon
  - egohygiene/pace
  - egohygiene/empathy
affected_contracts:
  - egohygiene.change-history-policy/v1
  - egohygiene.change-history-input/v1
  - egohygiene.change-history-analysis/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/37
    description: Requested subject, emoji, release-hint, PR, merge, automation, extension and migration semantics.
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/38
    description: Historical normalization has a separate feasibility, provenance and disposition boundary.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/a05b14f8b9e2772124f879f818e09a911e996ad8/docs/decisions/POLICY.md
    description: Accepted ADR policy1.2.0 preserves explicit human authority and proposed record lifecycle.
exceptions: []
approval: null
---

# ADR-0018: Define prospective change-history semantics separately from release authority and historical normalization

## Context

Existing public consumers use scoped arbitrary-emoji validation, a rich
Commitizen prompt and differing conventional commit configurations. A shared
policy needs explicit compatibility choices before these tools converge.
Message syntax, suggested release effects, actual component version decisions,
human approval and immutable Git provenance answer different questions.

## Decision

Propose a versioned Hygiene profile with a required component scope, exact
type/Unicode-emoji table, bang/footer breaking markers and explicit revert,
release, bot/generated and merge-context behavior. A pure text-free advisory
reference and closed schemas make the selected source reviewable. Squash is a
proposed future default; no current repository setting or check changes.

Release hints never replace the repository's pinned Aether version authority
or grant publication. Historical normalization, signatures, DCO/CLA verification
and provider mutations remain independently owned. The source proposal starts
in observe with null approval and no silently effective exceptions.

## Alternatives considered and rejected

- Keeping each parser authoritative would leave cross-repository release
  meaning ambiguous and make shared authoring guidance inconsistent.
- Accepting any emoji would preserve existing flexibility but fail the requested
  stable type-to-emoji contract. The exact table is a proposed compatibility
  change for explicit review rather than retrospective enforcement.
- Inferring actual versions, approvals or revert cancellation from message text
  would erase existing authority and evidence boundaries.
- Rewriting history while installing prospective tooling would change identities,
  signatures, tags and downstream evidence outside this issue's scope.

## Consequences and tradeoffs

Adapters gain one exact semantic target and a concrete source migration map.
Existing emoji aliases, scope-free subjects, non-core purpose types and
permissive whitespace can require prospective changes. ASCII-initial
descriptions and exact Unicode spellings trade flexibility for a portable
bounded alpha reference and need maintainer disposition before activation.
Missing restricted-source mapping remains an explicit acceptance gap.

## Implementation and evidence links

The [policy specification](../ecosystem/CHANGE_HISTORY.md), machine catalog,
closed schemas, pure reference, synthetic examples and pinned public migration
inventory implement this proposed authoring slice. Exact Aether
`create-decisions-document`2.1.0 at
`dc8a16851f452763ef4f7fbe4bf057d4500b1921`, accepted Hygiene policy1.2.0,
ratification and existing decision index were read before authoring.
Static source and schema inspection are distinct from deferred parser/examples,
native tooling, tests, builds, CI, provider and adoption qualification.

## Replacement or exit strategy

Select the profile through an explicit immutable revision/checksum and keep old
tool selections until their own reviewed migration. Roll back prospective
adapters and enforcement to the previous pins while retaining all later commits,
tags, signatures, author records and source evidence. A changed semantic mapping
requires a versioned successor and compatibility review.

## Follow-up work

EgoLint owns production validation; Relay owns safe preview/apply and resulting
subject verification; Holon/Empathy supply a canary; Pace proposes reviewed
adoption. Hygiene #38 retains historical feasibility. Complete private/local
mapping and actual release/merge/exception qualification when authorized.
Human disposition and enforcement activation remain separate from this merge.
