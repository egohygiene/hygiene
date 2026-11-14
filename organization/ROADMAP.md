# Ego Hygiene organization roadmap

<!-- Generated from roadmap.v1.json; edit that canonical source. -->

Proposed strategy under [the organization-roadmap contract](../docs/ecosystem/ORGANIZATION_ROADMAP.md).
Hygiene's [repository roadmap](../ROADMAP.md) remains separate. All initiative placement below is a reviewable proposal.
The [organization execution plan](https://github.com/egohygiene/.github/tree/main/docs/coordination) owns the current issue queue.

## Strategic context

Build independently useful tools that compose through versioned contracts, preserve provenance and keep consequential choices reviewable.
This is a public projection of declared strategy, not an exhaustive repository or participant inventory. Source tests and merged PRs do not ratify priority.

## Now

### ORG-I001 — Make foundations and evidence trustworthy

Converge canonical ownership, authoring contracts and provenance so source, policy approval and operational acceptance remain distinguishable.

Owner: `egohygiene/hygiene`. State: `proposed`; assertion: `inferred`; freshness: `current`.

Depends on: no declared initiative dependency.

Repository strategy:

- [egohygiene/hygiene HYG-Q03](https://github.com/egohygiene/hygiene/blob/main/ROADMAP.md) (active).
- [egohygiene/aether AET-Q07](https://github.com/egohygiene/aether/blob/main/ROADMAP.md) (active).
- [egohygiene/empathy EMP-Q02](https://github.com/egohygiene/empathy/blob/main/ROADMAP.md) (active).
- [egohygiene/empathy EMP-Q03](https://github.com/egohygiene/empathy/blob/main/ROADMAP.md) (active).
- [egohygiene/.github ORG-Q02](https://github.com/egohygiene/.github/blob/main/ROADMAP.md) (active).
- [egohygiene/.github ORG-Q03](https://github.com/egohygiene/.github/blob/main/ROADMAP.md) (active).

## Next

### ORG-I002 — Prove independently consumable delivery

Qualify immutable artifacts and clean consumer installation before treating release configuration or source preparation as delivered platform capability.

Owner: `egohygiene/aether`. State: `blocked`; assertion: `inferred`; freshness: `current`.

Depends on: ORG-I001.

Repository strategy:

- [egohygiene/aether AET-Q02](https://github.com/egohygiene/aether/blob/main/ROADMAP.md) (active).
- [egohygiene/aether AET-Q04](https://github.com/egohygiene/aether/blob/main/ROADMAP.md) (active).
- [egohygiene/aether AET-Q05](https://github.com/egohygiene/aether/blob/main/ROADMAP.md) (active).
- [egohygiene/empathy EMP-Q05](https://github.com/egohygiene/empathy/blob/main/ROADMAP.md) (active).
- [egohygiene/holon HOL-Q05](https://github.com/egohygiene/holon/blob/main/ROADMAP.md) (active).

### ORG-I003 — Compose a source-backed organization control plane

Connect repository-owned strategy and operational evidence to public Intelligence through owner contracts while preserving unknown, stale and restricted state.

Owner: `egohygiene/.github`. State: `proposed`; assertion: `inferred`; freshness: `current`.

Depends on: ORG-I001.

Repository strategy:

- [egohygiene/hygiene HYG-Q04](https://github.com/egohygiene/hygiene/blob/main/ROADMAP.md) (active).
- [egohygiene/hygiene HYG-Q06](https://github.com/egohygiene/hygiene/blob/main/ROADMAP.md) (active).
- [egohygiene/.github ORG-Q04](https://github.com/egohygiene/.github/blob/main/ROADMAP.md) (active).
- [egohygiene/holon HOL-Q06](https://github.com/egohygiene/holon/blob/main/ROADMAP.md) (active).

## Later

### ORG-I004 — Make organization foundations reusable

Create new repositories and evolve existing fleets from qualified versioned blueprints, then prove portability through a second organization consumer.

Owner: `egohygiene/holon`. State: `proposed`; assertion: `inferred`; freshness: `current`.

Depends on: ORG-I002, ORG-I003.

Repository strategy:

- [egohygiene/holon HOL-Q04](https://github.com/egohygiene/holon/blob/main/ROADMAP.md) (active).
- [egohygiene/holon HOL-Q08](https://github.com/egohygiene/holon/blob/main/ROADMAP.md) (active).
- [egohygiene/holon HOL-Q09](https://github.com/egohygiene/holon/blob/main/ROADMAP.md) (active).
- [egohygiene/holon HOL-Q10](https://github.com/egohygiene/holon/blob/main/ROADMAP.md) (active).
- [egohygiene/hygiene HYG-Q05](https://github.com/egohygiene/hygiene/blob/main/ROADMAP.md) (active).
- [egohygiene/empathy EMP-Q04](https://github.com/egohygiene/empathy/blob/main/ROADMAP.md) (active).

## Maybe

### ORG-I005 — Keep research and optional capabilities bounded

Evaluate alternative frameworks, local AI, confidentiality and agent-ready web capabilities only through explicit hypotheses, evidence and exit criteria.

Owner: `egohygiene/hygiene`. State: `optional`; assertion: `inferred`; freshness: `current`.

Depends on: no declared initiative dependency.

## Dependencies, uncertainty and review

Contracts and trustworthy evidence unblock qualified delivery and control-plane integration; those streams can progress independently after their shared prerequisites. Consumer proof precedes reusable fleet materialization.
Existing repository strategy IDs remain owned locally. Release acceptance, human ADR disposition, fleet adoption and source-rights clearance retain their own gates. Optional research stays optional.
Human review may change this proposed ordering. No target dates or activity-derived reprioritization are inferred. Pace's focus queue is a separate execution projection.

## Validation

`python3 tools/organization_roadmap.py check-generated` checks this view. The contract defines identity, provenance, privacy, transitions and rollback; synthetic tests do not prove live adoption or human approval.
