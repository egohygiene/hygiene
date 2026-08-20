---
schema: aether.architecture-document/v1
id: hygiene-architecture-decision-policy
title: Organization Architecture Decision Record Policy
kind: policy
version: 1.0.0
status: proposed
owners:
  - egohygiene/hygiene
created: 2026-08-20
updated: 2026-08-20
governed_by:
  - ADR-002
related:
  - hygiene-decisions
supersedes: []
---

# Organization Architecture Decision Record Policy

> **Proposal status:** This policy has no organization-wide authority until a
> human maintainer explicitly approves its governing ADR. The schema, template,
> and conventions in this pull request are review material until then.

## 1. Purpose

Architecture Decision Records preserve consequential choices, their approval,
their tradeoffs, and the evidence that later demonstrates implementation. They
are durable institutional memory for humans and coding agents; they are not a
second backlog or a requirement to document routine implementation work.

## 2. Authority and repository boundaries

- `egohygiene/hygiene` owns this policy, its schema, organization-level ADRs,
  cross-repository reference conventions, exceptions, and the organization
  contract index.
- `egohygiene/aether` owns reusable agent guidance and authoring packages that
  pin and project this policy. Aether guidance must not redefine it.
- `egohygiene/holon` owns scaffolding and managed repository projections.
- `egohygiene/relay` owns reusable validation and static-data generation
  implementations after their contracts are approved.
- `egohygiene/observatory` owns organization-wide aggregation and reporting.
- Each repository owns its local ADR documents and its local public projection.
- `egohygiene/.github` may expose thin intake templates but is not a canonical
  policy or implementation source.

Before architecture-changing work, an agent must read the repository's pinned
`docs/ecosystem/CONTEXT.md` when it exists, then inspect local decisions and the
relevant organization decisions. A local record may add implementation detail;
it may not silently redefine cross-repository ownership.

## 3. When an ADR is required

Create or update an ADR when a choice affects any of the following:

- public schemas, compatibility guarantees, migrations, or release contracts;
- repository or organization ownership boundaries;
- security, privacy, licensing, provenance, or publication authority;
- durable dependency, framework, platform, protocol, or format adoption or
  rejection;
- cross-repository integration or dependency direction;
- generated-versus-canonical source authority; or
- an irreversible or expensive-to-reverse technical direction.

An ADR is normally not required for routine bug fixes, localized refactors,
straightforward dependency patches, formatting, or implementation details that
do not alter a durable boundary. When useful, the pull-request description
should say `ADR not required` and give one concise reason.

When uncertain, prefer a short proposed record over an undocumented durable
choice, but first confirm that an existing ADR cannot be amended or superseded.

## 4. Location, identity, and canonical keys

New local records use:

```text
docs/decisions/ADR-NNN-short-slug.md
```

`NNN` is the next unused three-digit repository-local number. IDs are never
reused. The globally unique machine key is `<owner>/<repository>#<id>`, for
example `egohygiene/identity#ADR-004`.

Historical IDs and filenames remain unchanged. A four-digit `ADR-NNNN` or an
established repository-specific prefix may be retained only as migration
history with a documented exception. New records must not copy a legacy
prefix.

`DECISIONS.md`, when present, is a human navigation index. The detailed ADR file
is the canonical record. An index must summarize and link; it must not duplicate
complete rationale that can drift from the ADR.

## 5. Front matter contract

Every new ADR must validate against
[`schemas/architecture-decision.v1.schema.json`](../../schemas/architecture-decision.v1.schema.json)
and use `schema: egohygiene.architecture-decision/v1`.

Required metadata includes:

- identity and lifecycle: `id`, `title`, `status`, `date`, `decision_scope`;
- authority and visibility: `owners`, `visibility`, `approval`;
- delivery links: `issue`, `pull_request`, `implementation_status`, `evidence`;
- lineage: `related`, `supersedes`, `superseded_by`;
- blast radius: `affected_repositories`, `affected_contracts`; and
- explicit deviations: `exceptions`.

Empty values remain explicit as `null` or `[]`. Agents must not invent links,
approval, implementation, or validation evidence to make a record look
complete.

## 6. Required record sections

Every ADR contains these sections:

1. Context
2. Decision
3. Alternatives considered and rejected
4. Consequences and tradeoffs
5. Implementation and evidence links
6. Replacement or exit strategy
7. Follow-up work

Keep records concise and specific. Link large evaluations, specifications, and
plans instead of copying them into the decision.

## 7. Decision and implementation lifecycle

Decision status and implementation status are independent.

### Decision status

- `proposed` — review material; grants no implementation or publication
  authority.
- `accepted` — explicitly approved by a human authority identified in
  `approval`.
- `superseded` — replaced by an accepted ADR linked in both directions.
- `deprecated` — retained but no longer recommended or being advanced; a
  replacement may not yet exist.

Normal transitions are:

```text
proposed -> accepted -> superseded
    |           |
    +-----------+-> deprecated
deprecated -> accepted or superseded only with new approval evidence
```

An accepted or superseded record requires an approval date, approving human or
team, and a GitHub review, pull request, discussion, or other durable approval
URL. Opening or merging a pull request is not by itself approval unless the
linked evidence clearly records the approving authority. Automated agents must
never mark a decision accepted.

### Implementation status

- `not_started`
- `in_progress`
- `implemented`
- `verified`
- `not_applicable`
- `unknown` — migration-only when history cannot establish the state

Acceptance does not mean implemented. Implementation does not mean verified.
`verified` requires named validation evidence. A proposed ADR may link an
experiment, but an experiment does not make the decision accepted.

## 8. Related decisions and supersession

Local decision references use `ADR-NNN`. Cross-repository references use the
global key. A relation is symmetric only when its meaning requires it;
supersession always links both directions.

To supersede a record:

1. create the replacement as `proposed` with `supersedes` populated;
2. obtain explicit human approval;
3. transition the replacement to `accepted`;
4. transition the old record to `superseded` and populate `superseded_by`; and
5. validate that both records resolve and that no supersession cycle exists.

Do not edit historical context or delete the replaced record. Corrections that
do not change meaning may be amended with a clear change note and evidence.

## 9. Exceptions

Exceptions are narrow, time-bounded deviations from a named policy rule. Each
exception records the rule, reason, owner, status, approval evidence, and expiry
date when applicable.

- `proposed` exceptions grant no authority.
- `approved` exceptions require durable human approval evidence.
- `expired` exceptions remain visible for history.

An exception cannot waive the requirement for human acceptance, fabricate
evidence, expose private data, or move ownership away from the canonical
repository. Repeated exceptions indicate that the policy or rollout needs a
new ADR.

## 10. Cross-repository indexes and public projections

ADRs remain the source of truth. Dashboards and JSON files are generated
projections and must never be hand-authored as parallel decision logs.

Relay will eventually generate, under an approved contract:

- per-repository `decisions.json` from ADR front matter and allowed document
  content; and
- per-repository `activity.json` from allowlisted GitHub metadata.

Observatory will aggregate those repository contracts without changing their
meaning. The first static routes are:

- `/intelligence`
- `/intelligence/decisions`
- `/intelligence/activity`
- `/adr`, which redirects to `/intelligence/decisions`

The organization contract index is
[`catalog/contracts.yaml`](../../catalog/contracts.yaml). A contract is added
only when its canonical schema exists; planned `decisions.json` and
`activity.json` contracts are therefore not claimed by this proposal.

## 11. Privacy and publication

ADR front matter declares `visibility` as `public`, `internal`, or `private`.
Public output uses an allowlist, never a copy-everything approach.

- Never copy issue or pull-request bodies, comments, private titles, actor
  identities, secrets, local paths, workflow logs, or session data into public
  output.
- A public repository may expose allowlisted public metadata and links.
- A private repository defaults to aggregate counts or no public entry unless a
  human-owned publication configuration explicitly permits particular fields.
- Unknown visibility fails closed.
- A link to a private resource may remain private; the public projection must
  not summarize its protected content.

## 12. Agent and pull-request behavior

Before proposing an architecture change, agents must:

1. inspect existing local and relevant organization decisions;
2. determine and state whether an ADR is required;
3. create or update a `proposed` ADR in the same scoped pull request when
   required;
4. link the issue, pull request, evidence, contracts, repositories, and lineage;
5. preserve the difference between proposed, accepted, implemented, and
   verified; and
6. avoid duplicates when an existing record can be amended or superseded.

Aether will package this behavior as a concise reusable instruction module only
after the policy is approved. Repository `AGENTS.md` and Copilot instructions
will reference the pinned module instead of copying this complete policy.

## 13. Adoption

Adoption is migration-safe and evidence-driven:

- **validate** repositories with existing decision or instruction history before
  changing files;
- **scaffold** missing local decision structures without inventing past
  decisions; and
- **manage** only generated or pinned artifacts with explicit provenance
  markers, never repository-owned ADR content.

See [`MIGRATION.md`](MIGRATION.md) for the rollout procedure and
[`VALIDATION.md`](VALIDATION.md) for the acceptance and validation plan.
