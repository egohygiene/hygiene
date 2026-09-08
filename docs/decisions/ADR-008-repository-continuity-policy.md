---
schema: egohygiene.architecture-decision/v1
id: ADR-008
title: Require repository-owned continuity checkpoints through a versioned context successor
status: proposed
date: 2026-09-08
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/45
pull_request: null
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/*
affected_contracts:
  - egohygiene.repository-context/v1
  - egohygiene.repository-context/v2
  - egohygiene.repository-continuity-policy/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/45
    description: Reviewed scope, 29-repository baseline, precedence, privacy, compatibility, rollout, and downstream acceptance criteria.
  - type: external
    url: https://github.com/egohygiene/aether/pull/81
    description: Merged portable continuity specification, schema, template, and focused skill at an immutable revision.
  - type: external
    url: https://github.com/egohygiene/aether/pull/82
    description: Merged cross-skill dispositions and managed provider instruction projections at the pinned revision.
exceptions: []
approval: null
---

# ADR-008: Require repository-owned continuity checkpoints through a versioned context successor

## Context

On 2026-09-08, issue #45 recorded 29 active Ego Hygiene repositories, one
root `CONTINUITY.md`, eleven root `AGENTS.md` files, and four Copilot
instruction files. A fresh session therefore cannot consistently recover the
current dependency-ready work without replaying conversation history or doing
an unbounded repository investigation.

Aether now provides `aether.repository-continuity/v1`, its template and focused
maintenance skill, plus a managed provider-neutral instruction block. Aether
owns those portable semantics. Hygiene must decide organization applicability,
required-file composition, compatibility, rollout, and exception policy
without creating a competing schema or skill.

The existing `hygiene-repository-context` contract is version `1.0.0` and has
already been consumed by immutable pins. Adding a mandatory file and managed
content requirement in place would mislabel a breaking change as compatible.

At the selected Aether merge revision, the contract and skill are versioned and
merged but remain `draft` and excluded from Aether's stable release set. That
lifecycle gap must stay visible during Hygiene review.

## Decision

Propose `egohygiene.repository-continuity-policy/v1` at
`1.0.0-alpha.1`. It pins Aether merge commit
`b7597301c4d22a9bcd580967b5753138bb368111` and the exact digests of the
portable specification, schema, skill, template, and instruction projection.
It reports the upstream lifecycle as draft and unreleased rather than
fabricating stable-release evidence.

Propose `egohygiene.repository-context/v2` at `2.0.0` as the breaking
required-file successor. For applicable active repositories it requires:

- repository-owned root `CONTINUITY.md` with repository-specific current
  evidence under Aether's contract;
- repository-owned root `AGENTS.md` containing exactly one pinned managed
  continuity block while preserving local instructions; and
- generated `docs/ecosystem/CONTEXT.md` carrying the versioned Hygiene policy
  pointer.

The policy explicitly scopes all 29 repositories observed by issue #45 and
defines active, dormant, archived, mirror, generated-only, template, public,
private, and internal behavior. It begins in `observe`, advances through
`ratchet`, and reaches `enforce` only through accepted evidence gates.

The policy preserves user and repository authority, live-state verification,
canonical-source precedence, stale/conflict repair, minimum necessary context,
secret exclusion, and Git/work-tracker chronology. Static instructions do not
claim to install an automatic pre-pull-request hook.

The exact v1 TOML artifact remains available as deprecated compatibility
evidence. Existing consumers migrate through reviewed pull requests; new
consumers select v2 only after its proposal and upstream lifecycle are
accepted.

## Alternatives considered and rejected

### Add `CONTINUITY.md` to repository-context v1

Rejected because a new mandatory file invalidates repositories that satisfy a
pinned v1 contract. That is a major compatibility change.

### Copy Aether's schema and skill into Hygiene

Rejected because Aether owns the portable protocol. A copied implementation
would create two authorities and drift across providers.

### Treat Antidote as the fleet contract

Rejected because one prototype proves neither organization applicability nor
portable semantics. It remains migration evidence for the Aether contract.

### Enforce immediately across all repositories

Rejected because 28 of the 29 observed repositories lacked the root
checkpoint, most lacked repository-local agent guidance, downstream
conformance and execution work is not complete, and the upstream artifacts
remain draft.

### Make `CONTINUITY.md` generated or append-only

Rejected because repositories own their current operational truth, while Git
and the work tracker already own chronology. A generated diary would duplicate
history and increase privacy risk.

## Consequences and tradeoffs

- A fresh session gets a bounded repository-owned recovery surface with a
  deterministic contract pointer.
- The major-version transition preserves truth for existing pinned consumers
  but requires dual v1/v2 documentation during migration.
- Observe-first rollout makes current gaps visible without claiming the fleet
  is compliant; promotion needs additional human and downstream work.
- Repository maintainers must reconcile concise current state before PR
  presentation, adding a small but deliberate review cost.
- Public/private redaction and minimum-necessary rules reduce leakage risk but
  mean a checkpoint cannot replace every inaccessible source.
- Hygiene dogfoods the file and managed instruction block while keeping the
  policy proposal's limitations explicit.

## Implementation and evidence links

Issue #45 is the review authority for this proposal. The implementation adds
the machine profile and schema, deterministic organization validator, v2
context projection and offline contract, frozen v1 artifact, architecture and
migration guidance, dependency boundaries, tests, and Hygiene's own
repository-specific checkpoint.

The validator intentionally does not reimplement Aether's free-form semantic
truth checks. EgoLint #55 owns deterministic fleet findings, and Relay #60
owns reusable execution after both consume the same immutable policy.

## Replacement or exit strategy

If the proposal cannot advance, keep repository-owned checkpoints that remain
useful, return the policy to observe, and repin consumers to the immutable v1
context artifact. Do not erase Git history or fabricate passing evidence.

V1 may be removed only after no reviewed consumer depends on it and a separate
decision records deprecation evidence. Changes to required paths, ownership,
applicability precedence, exception authority, safety rules, or stage semantics
require a reviewed major successor with migration fixtures.

## Follow-up work

1. Stabilize and release the Aether continuity artifacts or update this
   proposal to another reviewed immutable revision.
2. Obtain explicit maintainer acceptance for ADR-008 before leaving observe.
3. Implement [egolint#55](https://github.com/egohygiene/egolint/issues/55),
   [holon#42](https://github.com/egohygiene/holon/issues/42),
   [relay#60](https://github.com/egohygiene/relay/issues/60),
   [observatory#18](https://github.com/egohygiene/observatory/issues/18), and
   [pace#26](https://github.com/egohygiene/pace/issues/26) without moving their
   implementations into Hygiene.
4. Run representative public and private pilots before ratchet.
5. Reconcile the older 27-entry architecture catalog through its existing
   catalog-refresh quest without changing this issue's reviewed 29-repository
   scope silently.
