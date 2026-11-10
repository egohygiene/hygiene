---
schema: egohygiene.architecture-decision/v1
id: ADR-0017
title: Separate architecture-coherence governance from assessment and conformance
status: proposed
date: "2026-11-09"
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/59
pull_request: null
related:
  - ADR-0002
  - ADR-0005
  - ADR-0016
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/aether
  - egohygiene/observatory
  - egohygiene/relay
  - egohygiene/pace
  - egohygiene/reflector
affected_contracts:
  - egohygiene.architecture-coherence-policy/v1
  - egohygiene.architecture-coherence-governance/v1
  - egohygiene.architecture-coherence-material-change/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/59
    description: Requested policy, applicability, human authority, freshness and advisory adoption boundaries.
  - type: issue
    url: https://github.com/egohygiene/aether/issues/87
    description: Portable read-only architecture reconstruction and critique ending at a Human Alignment Anchor boundary.
  - type: issue
    url: https://github.com/egohygiene/observatory/issues/21
    description: Read-only posture preserves assessment, human ratification, conformance, audit and CI dimensions separately.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/a05b14f8b9e2772124f879f818e09a911e996ad8/docs/decisions/POLICY.md
    description: Accepted organization ADR policy preserves explicit human lifecycle authority and repository ownership.
exceptions: []
approval: null
---

# ADR-0017: Separate architecture-coherence governance from assessment and conformance

## Context

The requested Sanity experience needs an explicit answer about represented
architecture, human review and material drift. Passing CI, clean audit findings,
contract conformance, implementation activity and an AI recommendation answer
different questions. A JSON field labelled human cannot authenticate approval.
Organization review must also remain separate from ratifying each repository.

## Decision

Propose Hygiene-owned versioned applicability, governance and material-change
semantics with a pure standard-library reference. Aether retains the full review
assessment contract and read-only skill. Observatory normalizes source posture;
Relay transports and presents it; Pace proposes adoption. Repositories retain
facts, authority sources and publication.

Human claims bind scope, exact represented revisions and an assessment digest
that excludes mutable governance. Effective human dispositions require separate
typed trusted-source context; source JSON alone stays unverified. Explicit
expiry and sourced material events determine freshness. Routine implementation
and a different Git SHA do not automatically invalidate a review. Protected
scope is omitted before public payload inspection, counting or hashing.

The policy remains proposed and starts in observe. No real applicability
exception, ratification, approval, scheduler, gate or publication is introduced.

## Alternatives considered and rejected

- A single green/red architecture score would merge unrelated evidence and hide
  intentional tradeoffs, partial implementation and unknown source coverage.
- Ratifying from an AI recommendation, actor string, merge or source JSON would
  permit self-approval without authentic human evidence.
- Invalidating on every commit would create review noise and misclassify routine
  development as architecture drift.
- Placing review prompts or presentation code in Hygiene would duplicate Aether
  and Relay authority. A governance subrecord preserves those owners.

## Consequences and tradeoffs

Consumers can preserve unknown, due, in-progress, stale, deferred and human
disposition independently. Exact assessment binding avoids a self-referential
digest. Separate source verification costs an explicit adapter and can leave
valid-looking human claims unverified; that is preferable to manufacturing
authority. Complete material-change inventory is needed to establish current
freshness when no observed event already proves staleness.

## Implementation and evidence links

The proposed policy, closed schemas and reference helper implement this bounded
source seam. The linked issues define requested scope. Pinned Aether
`create-decisions-document` 2.1.0 at `dc8a16851f452763ef4f7fbe4bf057d4500b1921`
was read from exact Git objects; accepted policy v1.2.0 and its ratification were
read before drafting. Static inspection remains distinct from deferred tests,
fixtures, native/provider execution, publication and actual human disposition.

## Replacement or exit strategy

Consumers opt in at one immutable helper/schema/policy revision. Unsupported or
incompatible records remain unavailable rather than being reinterpreted. A
successor version must preserve historical human statements and use a reviewed
migration. Reverting a proposed profile cannot rewrite prior source authority,
ADR lifecycle, consumer recovery bytes or the separate Hygiene #47 hold.

## Follow-up work

Aether #87 supplies authoring; Observatory #21 supplies normalized read models;
Relay and Reflector own bounded downstream presentation and orchestration.
Implement genuine human-source verification and qualify current, stale,
deferred, revision-required, not-applicable and missing-review cases in the
deferred validation pass. Explicit human ratification and scoped policy
activation remain separate decisions.
