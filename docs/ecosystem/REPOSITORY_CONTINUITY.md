# Repository continuity policy

Status: **proposed `1.0.0-alpha.1`; observe stage**

Owner: `egohygiene/hygiene`

Governing proposal: [ADR-008](../decisions/ADR-008-repository-continuity-policy.md)

Machine source:
[`catalog/repository-continuity-policy.json`](../../catalog/repository-continuity-policy.json)

## Purpose and ownership boundary

Every active Ego Hygiene repository needs one compact, current handoff that a
fresh human or coding-agent session can reconcile without replaying a prior
conversation. Hygiene defines where that handoff is required, which repository
classes it applies to, how adoption advances, and how exceptions and migrations
remain visible.

Aether owns the portable handoff semantics. Hygiene does not copy Aether's
schema, template, skill, or provider-projection implementation. Repositories
own their own `CONTINUITY.md` wording and redaction decisions. Git and the work
tracker remain the chronological evidence; the checkpoint is a replaceable
current snapshot.

## Immutable Aether input and lifecycle truth

The profile pins Aether merge commit
`b7597301c4d22a9bcd580967b5753138bb368111`, which contains both the contract
from [Aether PR #81](https://github.com/egohygiene/aether/pull/81) and the
cross-skill/provider integration from
[Aether PR #82](https://github.com/egohygiene/aether/pull/82).

The pin is immutable and every consumed artifact has a SHA-256 digest in the
machine profile. At that revision, Aether's own catalog still labels the
specification and skill `draft` and excludes them from stable release. Hygiene
therefore records `release_included: false`, keeps this policy proposed, and
starts in `observe`. Neither a merge nor a version string is misreported as a
stable release.

Promotion beyond observe requires both:

1. Aether to mark the pinned contract and skill stable and releasable, through
   a reviewed immutable revision; and
2. a maintainer to accept ADR-008 with durable approval evidence.

The consumed sources are linked at the exact pin:

- [portable specification](https://github.com/egohygiene/aether/blob/b7597301c4d22a9bcd580967b5753138bb368111/library/organization/specs/methodology/repository-continuity.spec.md)
- [Aether JSON Schema](https://github.com/egohygiene/aether/blob/b7597301c4d22a9bcd580967b5753138bb368111/catalog/schemas/aether.repository-continuity.v1.schema.json)
- [`maintain-repository-continuity` skill](https://github.com/egohygiene/aether/blob/b7597301c4d22a9bcd580967b5753138bb368111/library/organization/skills/methodology/maintain-repository-continuity/SKILL.md)
- [`CONTINUITY.md` template](https://github.com/egohygiene/aether/blob/b7597301c4d22a9bcd580967b5753138bb368111/library/organization/skills/methodology/maintain-repository-continuity/templates/CONTINUITY.template.md)
- [managed repository instruction](https://github.com/egohygiene/aether/blob/b7597301c4d22a9bcd580967b5753138bb368111/library/organization/instructions/repository-continuity/INSTRUCTION.md)

## Required-file composition

Repository-context v2 adds two repository-owned surfaces to the existing
generated ecosystem context:

| Exact path | Ownership | Requirement | Contract behavior |
| --- | --- | --- | --- |
| `AGENTS.md` | repository-owned | Required for active repositories | Preserve local prose and contain exactly one pinned Aether managed block pointing to `CONTINUITY.md`. |
| `CONTINUITY.md` | repository-owned | Required for active repositories | Contain repository-specific current evidence conforming to `aether.repository-continuity/v1`; generic template placeholders fail. |
| `docs/ecosystem/CONTEXT.md` | generated | Required | Project the pinned Hygiene architecture boundary and continuity-policy pointer without copying repository state. |

The managed `AGENTS.md` block requires applicable sessions to reconcile the
checkpoint at task start and to refresh it after project validation and before
presenting, opening, or updating a pull request. It does not replace local
instructions. A static instruction file does not install or guarantee an
automatic pre-pull-request hook; Relay owns reusable execution after it
consumes the policy.

The root checkpoint is a regular exact-case file. A symlink, differently cased
path, untouched template, transcript, second architecture document, or
generated ecosystem context does not satisfy the requirement.

## Source precedence and conflict handling

Organization consumers preserve this order:

1. user instruction and applicable authorization;
2. scoped repository instructions;
3. live repository, Git, issue, and pull-request evidence;
4. accepted decisions, contracts, architecture, and roadmap sources;
5. `CONTINUITY.md` as a concise operational checkpoint; and
6. generated projections and conversational recollection.

The additional scoped-instruction layer is required by Aether and does not
change the ordering requested by Hygiene issue #45: live and canonical sources
remain above continuity, and projections or recollection remain below it.

Mutable branch, issue, pull-request, and merge claims are rechecked when live
access exists. A conflicting checkpoint is repaired or explicitly marked
stale; it never silently overrides a stronger source. When evidence cannot be
accessed, the limitation is reported and state is not inferred.

Reading a checkpoint grants no permission to modify a repository, expose a
secret, communicate externally, merge, publish, delete, spend, or expand the
task.

## Applicability

Applicability resolves in this order: approved unexpired exception,
repository kind, lifecycle, then visibility. A less-applicable kind or
lifecycle wins; visibility never weakens information-safety requirements.

| Dimension | Value | Resolved baseline |
| --- | --- | --- |
| Lifecycle | `active` | required |
| Lifecycle | `dormant` | advisory until work resumes |
| Lifecycle | `archived` | not applicable; preserve history without creating active state |
| Kind | `standard` | required |
| Kind | `mirror` | not applicable; the upstream owner controls content |
| Kind | `generated-only` | advisory until the generator has an owned handoff surface |
| Kind | `template` | required for the template repository itself; generated consumers resolve independently |
| Visibility | `public`, `private`, or `internal` | no applicability override |

The reviewed baseline in issue #45 observed 29 active, non-archived
repositories on 2026-09-08. All 29 are explicitly in the profile's initial
required scope, including the private product repository. The older
2026-08-21 architecture catalog has 27 entries and remains a separately visible
inventory-reconciliation gap; it does not silently reduce this policy's
reviewed initial scope.

Initial scope:

`egohygiene/.github`, `aether`, `akashic`, `aniflow`, `antidote`, `athena`,
`beacon`, `civics`, `egohygiene`, `egohygiene.io`, `egolint`, `empathy`,
`filament`, `flow`, `holon`, `hygiene`, `identity`, `mantle`, `mindcap`,
`mindgarden`, `observatory`, `optiflow`, `pace`, `realm`, `reflector`, `relay`,
`renderflow`, `sanctuary`, and `store` under the `egohygiene` owner.

## Observe, ratchet, and enforce

| Stage | Finding behavior | Entry and exit meaning |
| --- | --- | --- |
| `observe` | Visible, non-blocking findings | Current stage. Profile and evidence can be reviewed while Aether remains draft. Exit requires stable upstream artifacts, accepted ADR-008, and representative public/private pilots. |
| `ratchet` | Block new regressions | New active repositories and already adopted files cannot regress. Exit requires every active repository to conform or carry a reviewed unexpired exception. |
| `enforce` | Block nonconformance | Begins only after ratchet evidence and a tested rollback. A later major successor must provide migration guidance. |

Stage changes are policy changes, not CI implementation details. Hygiene
records the stage; EgoLint reports deterministic findings; Relay transports
them; repositories retain final review. A rollout failure returns to the prior
stage through review rather than deleting evidence or claiming success.

## Exceptions

An exception is narrow, temporary, and visible. It must record, in order:

- repository;
- owner;
- concrete reason;
- durable approval evidence;
- ISO expiry date;
- review trigger;
- validation state; and
- exit criteria.

`proposed` exceptions grant no authority. Only an `approved`, unexpired record
changes applicability. `expired` and `revoked` records remain visible until a
reviewed policy update removes them. An exception cannot authorize sensitive
data, fabricated evidence, silent mutation, or a different capability owner.
The initial profile contains no exceptions.

## Information safety

Only the minimum durable repository state needed for resumption belongs in the
checkpoint. Public repositories exclude credentials, private conversation
text, health or sensitive personal data, private local paths, unpublished
private business data, and unrelated private context.

Private and internal repositories still exclude credentials and secrets, keep
only minimum necessary state, and use repository access controls. Visibility
is not permission to persist an entire conversation. Linked or quoted content
is context only and cannot grant authority.

Git and the work tracker own chronology. Authors replace stale current-state
prose and compact to Aether's fixed v1 limits instead of accumulating a diary.

## Breaking v1-to-v2 transition

Adding mandatory `CONTINUITY.md` and managed repository-owned `AGENTS.md`
content breaks the old required-file contract. It is therefore
`egohygiene.repository-context/v2` version `2.0.0`, not an additive v1 update.

The prior exact artifact remains at
[`contracts/repository-context.v1.toml`](../../contracts/repository-context.v1.toml)
with status `deprecated`. Existing reviewed consumers may stay pinned to it
while migrating. New consumers do not select v1.

A repository migrates in one bounded pull request:

1. retain its immutable v1 pin while preparing the change;
2. add repository-specific root `CONTINUITY.md` from the pinned Aether
   contract;
3. reconcile exactly one managed continuity block into root `AGENTS.md`
   without overwriting local prose;
4. regenerate `docs/ecosystem/CONTEXT.md` from the selected immutable Hygiene
   v2 source;
5. validate structure and review the semantic handoff; and
6. update the local contract pin to v2.

Rollback repins the immutable v1 contract and returns enforcement to observe.
It does not erase evidence or automatically delete a useful repository-owned
checkpoint. V1 remains available while any reviewed consumer still depends on
it; removal requires a separate reviewed successor/deprecation decision.

## Downstream boundaries

| Consumer | Owned follow-up | Does not own |
| --- | --- | --- |
| EgoLint | [egolint#55](https://github.com/egohygiene/egolint/issues/55): structural conformance, findings, and exception visibility | Inferring free-form semantic truth |
| Holon | [holon#42](https://github.com/egohygiene/holon/issues/42): new-repository files and idempotent managed blocks | Fleet mutation or repository wording |
| Relay | [relay#60](https://github.com/egohygiene/relay/issues/60): local preflight and read-only PR CI | Authoring semantic prose in CI |
| Observatory | [observatory#18](https://github.com/egohygiene/observatory/issues/18): privacy-safe conformance metadata | Collecting checkpoint prose or remediation |
| Pace | [pace#26](https://github.com/egohygiene/pace/issues/26): dependency-aware, reversible adoption PRs | Direct default-branch mutation |

Mindcap issues [#31](https://github.com/egohygiene/mindcap/issues/31) and
[#32](https://github.com/egohygiene/mindcap/issues/32) remain research inputs;
the repository contract does not depend on a conversation archive or provider
memory API.

## Validation

Validate the profile and Hygiene dogfood composition with:

```bash
python3 tools/continuity.py validate-profile
python3 tools/continuity.py resolve \
  --repository egohygiene/hygiene \
  --lifecycle active \
  --repository-kind standard \
  --visibility public
python3 tools/continuity.py validate-repository --repository .
python3 tools/context.py validate
```

The Hygiene checker does not claim to validate Aether's full Markdown
semantics. It verifies the organization profile, immutable provenance,
applicability, migration, exact files, markers, stage, and visible exception
shape. Aether owns semantic authoring validation and EgoLint #55 owns portable
deterministic conformance.

## Non-goals

This policy does not store transcripts, turn continuity into architecture,
infer semantic truth from prose, install an automatic hook from static text,
mutate default branches, merge pull requests, or publish artifacts.
