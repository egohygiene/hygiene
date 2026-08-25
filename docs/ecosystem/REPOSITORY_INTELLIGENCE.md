# Repository Intelligence contract

- Contract: `egohygiene.repository-intelligence/v1`
- Contract version: `1.0.0-alpha.1`
- Vocabulary: `egohygiene.repository-intelligence-vocabulary/v1`
- Status: **proposed**
- Owner: `egohygiene/hygiene`
- Governing proposal: [`ADR-005`](../decisions/ADR-005-unify-repository-intelligence-projection.md)

> This contract is review material until a human maintainer accepts its
> governing ADR. Its presence does not claim that fleet collection, rendering,
> publication, or adoption is implemented.

## 1. Purpose

Repository Intelligence connects why work exists, what was decided, how it was
delivered, whether it passed validation, and where it was released or deployed.
It supports Roadmap, Decisions, Journey, Now, Dependencies, Health, Releases,
Work, Search, and Compare views without making those views sources of truth.

The projection answers questions such as:

- Which decision informed this roadmap step?
- Which issue and pull request implemented it?
- Which commits and checks provide delivery evidence?
- Which release contains the work, and where was that release deployed?
- Is the claim authoritative or inferred?
- Is the evidence current, stale, unavailable, or not applicable?

## 2. Authority model

The projection is generated. A snapshot is rooted in one repository but may
include public, provenance-backed external entities needed to represent an
explicit cross-repository dependency. Canonical facts stay with their owners:

| Fact | Canonical source |
| --- | --- |
| Intent, sequence, outcomes, exit criteria | Repository `ROADMAP.md` |
| Decision context, status, approval, lineage | Repository ADR Markdown |
| Commit topology and file changes | Git |
| Issue and pull-request state | GitHub |
| Check results | The named check provider |
| Release contents and tags | The repository release record and Git tag |
| Deployment state | The named deployment provider |

A generated snapshot may normalize and link those facts. It may not silently
override them. When sources disagree, the snapshot preserves the conflict or
marks the value unknown; it does not choose the most convenient answer.

## 3. Projection envelope

Every snapshot validates against
[`repository-intelligence.v1.schema.json`](../../schemas/repository-intelligence.v1.schema.json)
and includes:

- exact schema and pre-release contract versions;
- a projection ID containing the repository and represented commit;
- the represented repository, commit, visibility, and observation time;
- generator identity and version;
- normalized sources, entities, directed relationships, and events;
- explicit redactions; and
- namespaced extensions.

`observed_at` is an explicit collector input. Generators must not substitute the
ambient wall clock when reproducibility requires a pinned observation time.

Arrays use stable order:

- sources, entities, and relationships by `id`;
- events by `occurred_at`, then `id`;
- redactions by `field`, then `reason`.

JSON uses UTF-8, two-space indentation, stable key ordering, and a final newline
for checked-in fixtures and durable artifacts.

## 4. Stable identifiers

Entity identifiers use this shape:

```text
ri:<owner>/<repository>:<kind>:<native-key>
```

Examples:

```text
ri:egohygiene/relay:repository:egohygiene/relay
ri:egohygiene/relay:roadmap-step:REL-RM-003
ri:egohygiene/relay:architecture-decision:ADR-007
ri:egohygiene/relay:issue:27
ri:egohygiene/relay:pull-request:28
ri:egohygiene/relay:commit:0123456789abcdef0123456789abcdef01234567
ri:egohygiene/relay:check:repository-intelligence
ri:egohygiene/relay:release:v0.4.0
ri:egohygiene/relay:deployment:github-pages-1842
```

Rules:

1. A native canonical key is reused; a title, sequence position, or database
   offset is not an identity.
2. IDs are immutable after publication. A renamed title retains the same ID.
3. Roadmap-step and ADR IDs are repository-local but become globally unique
   through the repository-qualified prefix.
4. An external entity retains its owning repository prefix and requires an
   explicit source; it is never re-keyed under the snapshot repository.
5. Git commit identity is the full lowercase 40-character object ID for v1.
6. Provider IDs for checks and deployments must be stable within the represented
   repository. A generator documents any encoding it applies.
7. A changed canonical identity creates a new entity plus a `supersedes`
   relationship when the domain supports supersession.

Source, relationship, and event IDs are stable within one projection series.
They must not depend on array position or collection order.

## 5. Entities

V1 represents these kinds:

- `repository`
- `roadmap_step`
- `architecture_decision`
- `issue`
- `pull_request`
- `commit`
- `check`
- `release`
- `deployment`

Every entity supplies its repository, native key, canonical URL, visibility,
current state, freshness, one or more provenance-source references, typed
attributes, and optional namespaced extensions.

Titles are nullable because privacy policy may allow a public identifier and
link while withholding human-readable text. A missing title must remain `null`;
generators must not invent one.

## 6. Relationship vocabulary

The machine-readable vocabulary is
[`catalog/repository-intelligence-vocabulary.json`](../../catalog/repository-intelligence-vocabulary.json)
and validates against its own schema. Each definition states direction, inverse
display label, cardinality, permitted source kinds, permitted target kinds, and
whether consumers may compute a transitive closure.

The initial directed types are:

| Type | Direction |
| --- | --- |
| `implements` | delivery entity → intent, decision, or preceding delivery entity |
| `informs` | decision, intent, or issue → shaped intent or work |
| `supersedes` | replacement → retained historical entity |
| `blocks` | blocker → blocked entity |
| `depends-on` | dependent → prerequisite |
| `releases` | release → included intent or delivery entity |
| `deploys` | deployment → activated release or commit |
| `tracks` | roadmap step or decision → coordinating issue or pull request |
| `verifies` | check → validated delivery or intent entity |
| `evidences` | delivery or validation entity → intent or decision |

Relationship instances are directed even when a UI displays an inverse label.
Consumers must not reverse an edge or infer transitivity unless the vocabulary
permits it. Every edge carries assertion, freshness, and provenance independently
from its endpoints.

## 7. Event envelope

Events are normalized observations, not a mutable audit log. Each event records:

- a stable ID and typed event name;
- the subject entity;
- when the source says it occurred and when the collector recorded it;
- actor attribution or explicit `null` when absent or redacted;
- changed fields with before/after values;
- visibility, assertion, freshness, and provenance; and
- namespaced extensions.

Event names cover repository observations, roadmap creation/status changes, ADR
lifecycle changes, issue and pull-request lifecycle, commit creation, completed
checks, published releases, and completed deployments.

Events never make Git immutable history into a blockchain. A later collection
may correct an inferred edge or provider state. The next snapshot preserves the
new observation and its source; durable Git history remains in Git.

## 8. Assertion and freshness

Assertion and freshness answer different questions.

### Assertion

- `authoritative` — directly reported by the canonical source for this fact.
- `inferred` — derived by a documented rule from authoritative inputs.
- `unknown` — the collector cannot establish the fact.

### Freshness

- `current` — observed within the configured freshness policy.
- `stale` — valid evidence exists but exceeds that policy.
- `unknown` — age or source availability cannot be established.
- `not_applicable` — freshness has no meaning for this immutable or excluded
  source.

`unknown` is never success. `inferred` is never displayed as authoritative.
`stale` evidence remains useful historical context but cannot silently support a
current healthy state.

## 9. Provenance

Every entity, relationship, and event references at least one top-level source.
A source identifies:

- source kind and canonical URL;
- repository and immutable revision when one exists;
- explicit observation time;
- visibility;
- assertion; and
- freshness.

Mutable GitHub and provider records may have `revision: null`; their canonical
URL and observation time are still required. Git-backed sources use the
represented full commit SHA. Consumers reject dangling provenance references.

## 10. Commit trailers and Markdown references

Trailers improve future linkage but are never the only accepted evidence.

```text
feat(intelligence): publish the normalized graph

Roadmap-Step: HYG-Q05
ADR-Ref: egohygiene/hygiene#ADR-005
Refs: #19
```

Conventions:

- `Roadmap-Step:` contains one stable local step ID or one fully qualified
  `<owner>/<repository>#<step-id>` value. It may be repeated.
- `ADR-Ref:` contains one local `ADR-NNN` value or one fully qualified
  `<owner>/<repository>#ADR-NNN` value. It may be repeated.
- Trailers appear in the Git trailer block, not an arbitrary prose match.
- A cross-repository reference is always fully qualified.
- Generators preserve the trailer as source evidence and still validate that
  the target resolves.
- Missing trailers do not invalidate historical work when roadmap, ADR, issue,
  or pull-request links establish the relationship.

Canonical Markdown references include:

- `roadmap-step` metadata in `ROADMAP.md` for IDs, dependencies, and issues;
- ADR front matter for issue, pull request, related, supersession, affected
  repositories, affected contracts, and evidence;
- explicit GitHub links in roadmap or ADR evidence sections; and
- structured pull-request template fields using the same `Roadmap-Step:` and
  `ADR-Ref:` labels.

Source precedence is canonical structured metadata, canonical Git/GitHub or
provider state, explicit trailer/template references, then documented inference.
Conflicts remain visible and fail closed where authority would otherwise be
ambiguous.

## 11. Visibility and redaction

Snapshot visibility is an upper bound. A public snapshot contains only public
sources, entities, relationships, events, and actor fields. Internal and private
items are excluded before rendering, with aggregate redaction records where
policy permits them.

Public output never copies issue or pull-request bodies, comments, review text,
email addresses, workflow logs, credentials, raw provider payloads, private
titles, local paths, or session data. Unknown source visibility fails closed.

Actor attribution is optional publication data. When attribution is unavailable
or disallowed, `actor` is `null`; a generator must not infer identity from commit
text or other indirect data.

## 12. Compatibility and extensions

- Consumers pin both `schema` and exact `contract_version` while the contract is
  alpha.
- Adding an optional field is compatible only when older consumers ignore it
  without changing meaning.
- Removing or renaming a required field, changing identity, authority,
  visibility, event meaning, relationship direction, or cardinality requires a
  new major contract.
- New core entity, event, assertion, freshness, or relationship enum values are
  breaking in v1 because closed-enum consumers fail closed.
- Experimental data uses namespaced extension keys such as
  `egohygiene.observatory/confidence-score`.
- An extension may not override a core field or weaken visibility, provenance,
  or authority requirements.
- A migration publishes old-to-new identifier rules and fixtures. It never
  rewrites canonical ADR or Git history merely to satisfy a projection.

## 13. Consumer responsibilities

| Owner | Responsibility |
| --- | --- |
| Hygiene | Own schema, vocabulary, compatibility, visibility, and authority semantics. |
| Aether | Package pinned authoring guidance and decision/linkage hooks without redefining policy. |
| Egolint | Validate canonical inputs, IDs, cycles, links, trailers, and declared profile rules. |
| Observatory | Normalize evidence, build query/fleet snapshots, and preserve uncertainty. |
| Holon | Render accessible reusable components from versioned view models. |
| Relay | Collect read-only evidence, run validation, generate artifacts, and compose publication workflows. |
| Pace | Propose bounded adoption and migration pull requests; report drift and exemptions. |
| Each repository | Own roadmap intent, local decisions, publication configuration, and final site composition. |

No consumer copies a sibling implementation or reads a mutable default branch as
a production dependency. Compatibility fixtures may be copied only as released,
checksummed test artifacts under the owning contract's license and provenance.

## 14. Reference validation and fixture

The complete quest fixture at
[`fixtures/repository-intelligence/complete-quest.json`](../../fixtures/repository-intelligence/complete-quest.json)
connects a roadmap dependency and decision through issue, pull request, commit,
check, release, and deployment.

Validate it with:

```bash
python3 tools/intelligence.py validate \
  --snapshot fixtures/repository-intelligence/complete-quest.json \
  --vocabulary catalog/repository-intelligence-vocabulary.json
```

The reference validator is intentionally local and dependency-free. Egolint and
Relay own production enforcement after the proposed contract is accepted and
released.
