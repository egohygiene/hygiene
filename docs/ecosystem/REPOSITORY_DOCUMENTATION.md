# Repository documentation locations and navigation

Status: **proposed `1.0.0-alpha.1`; observe only; approval absent**.

Owner: `egohygiene/hygiene`. Governing proposal:
[ADR-0019](../decisions/ADR-0019-repository-documentation-locations.md).
This is the policy checkpoint for [#64](https://github.com/egohygiene/hygiene/issues/64),
under [#76](https://github.com/egohygiene/hygiene/issues/76). It does not activate a
fleet rule, relocate documents, or complete the later Aether/Empathy pilot.

The [versioned profile](../../catalog/repository-documentation-profile.json),
[profile schema](../../schemas/repository-documentation-profile.v1.schema.json),
[inventory schema](../../schemas/repository-documentation-inventory.v1.schema.json),
and [local assessment schema](../../schemas/repository-documentation-assessment.v1.schema.json)
form this proposal's machine contract. The schema major is `v1`; this initial
compatible review profile is `1.0.0-alpha.1`. Adoption selects an exact revision
and the matching schema/profile/helper digests. No current consumer pin changes.

## One canonical source, useful entry points

Newly selected detailed architecture normally belongs under `docs/architecture/`.
Established canonical locations remain valid. Declare `legacy-root` for an
existing root corpus, `nested-architecture` for the proposed arrangement, or a
repository-owned exception path map with reason, owner, and review trigger.
Unknown selection is a review gap, not permission to generate a second corpus.

`architecture_selected` is explicit: `true` selects the relevant architecture
concerns, `false` does not mandate a corpus, and `null` leaves selection unknown.
Aether owns architecture-set profiles, stable IDs, front matter, dependency
closure, and content validation. This location contract neither selects all 18
documents nor replaces an existing accepted discoverable alternative.

| Category | Proposed location or compatibility | Authority and update path |
| --- | --- | --- |
| Orientation | Root `README.md` | Repository facts and local prose; reviewed repository change. |
| Shared agent entry | Root `AGENTS.md` | Repository-owned instructions; preserve local content and pinned managed blocks. |
| Current handoff | Root `CONTINUITY.md` | Repository-owned compact state under Aether's selected continuity contract. |
| Claude adapter | Regular root `CLAUDE.md` when explicitly selected | Provider compatibility; first nonblank line `@AGENTS.md`. |
| Root architecture entry | `ARCHITECTURE.md` | Detailed canonical source in a declared legacy layout; navigation to that source in a nested layout. |
| Documentation index | `docs/README.md` or a declared established index | Question-oriented navigation to applicable canonical sources. |
| Structural architecture | Selected `docs/architecture/**`, established root files, or declared exception | Repository-owned details with Aether-owned identity/metadata semantics. |
| Mission and change admission | Selected `PURPOSE.md` concern in that corpus | Reuse purpose, scope, limits, and a practical change-admission test; do not introduce competing MISSION authority. |
| Decisions | Existing `docs/decisions/` and index | Accepted ADR policy v1.2.0; preserve dispositions, IDs, lineage and human approval evidence. |
| Guides and procedures | `docs/guides/` or established declared location | Durable instructions, with prerequisites and an update owner. |
| Reference and contracts | `docs/reference/` or established declared location | Owning source retains schemas/specifications; link generated copies to exact sources. |
| Design explanations | `docs/design/`, selected architecture, or established location | Select PRDs, whitepapers and detailed specifications only when useful. |
| Audit/validation evidence | `audits/`, `docs/evidence/`, or established evidence location | Dated, source-bound observations with scope, qualification and reopenable originals. |
| Retained work reports | `docs/evidence/`, `docs/development/`, or established location | Promote lengthy useful implementation explanations/diagnostics; link from navigation rather than copying a session. |
| Archive | `docs/archive/` or established historical location | Preserve dates, provenance, stable citations and a pointer to current sources. |
| Temporary agent notes | Outside versioned source | Disposable scratch; promote durable requirements, decisions and proof before handoff. |

These are question/authority categories, not a universal required filename list.
An omitted optional concern is different from a missing selected dependency.
Literal repository-relative paths can contain spaces and Unicode. The reference
does not decode URLs, normalize filenames, or require renaming existing sources.

## Compose existing applicability and presentation

This profile pins unchanged Hygiene presentation bytes SHA-256
`94132769e6cb9d4bc68abd6314bbe797ce6ab9abaad3bb424775d1157367d573`
and continuity bytes
`2f694682df641f9c9741d79c7d23bca2ae5bd0d1e3aa6ca00cb31db17e0e2e2c`
with exact helper hashes in `composes`: presentation selects
`eb38eb790bb0cad38c8d651d11d3dc4cc7ab7bb4` (duplicate-record parity repair),
while continuity retains `ae4e4c1399aeed3b82c97959c82741892c230fbf`. The reference calls their existing pure resolvers rather than
reimplementing applicability. Their statuses remain proposed. The independent
accepted ADR policy and draft Aether continuity contract keep their own states.

This selection includes the merged continuity-clock repair (#91) and
presentation-witness repair (#89). The adapter passes the inventory's explicit
`as_of` date and retains the owner's actual `assessment_date` and
`assessment_mode` in `continuity_assessment`; unavailable applicability leaves
that field null. It does not substitute a historical policy date or claim that
the caller's assessment date is a fresh filesystem observation. Presentation
composition selects requirements only; it does not inspect slot evidence or
claim that a current passing witness exists.

Continuity resolves approved unexpired exceptions, kind, lifecycle, then
visibility. Active standard/template repositories resolve required; dormant or
generated-only scopes resolve advisory; archived/mirror scopes resolve not
applicable. Unknown dimensions remain unknown. Private/internal visibility
does not weaken the actual continuity obligation; this public review adapter
declines their payload instead of evaluating or publishing it. Separate
`lifecycle` and `presentation_lifecycle` fields preserve the two owners'
different vocabularies; neither is silently derived from the other.

README guidance supplements the existing presentation slots. Keep a truthful
starting path and link detailed material. A concise README with useful links
and a rich README with a repository-owned justification are both supported;
there is no universal word limit. Preserve justified local sections. Identity
supplies already reviewed presentation assets through the existing Holon
region; this proposal generates no brand, mandates no social metadata, and
does not overwrite facts or authored prose.

`AGENTS.md` and `CONTINUITY.md` keep the existing continuity applicability.
Claude selection independently requires its shared `AGENTS.md` import target.
The regular compatibility file imports only `AGENTS.md` in this initial bounded
profile; additional provider prose needs an explicit justification. It does not
eagerly import the architecture corpus. Other provider adapters stay optional.
No provider is activated and no enforcement hook is installed by these files.

## Metadata, authority and retention

Canonical documentation records the question it answers, source/authority, and
how to update it. Preserve actual stable IDs where the owner contract defines
them; do not invent IDs or rewrite dependencies merely to move a path. Generated
material additionally identifies the source repository, immutable revision,
path, and generated ownership. Navigation identifies the inventory entry for
its canonical target and links to that exact declared path. It does not become
a second copy of the detailed authoritative prose.

The inventory's `id` is a local observation handle; `stable_id` is the optional
existing source identity. `canonical_id` refers to an inventory handle. Declared
paths and links are exact literal repository-relative names, not URI fragments.
Missing targets, unknown/inaccessible state, conflicting identities, missing
metadata, or a generated canonical claim produce explicit review diagnostics.
Report those gaps to the maintainer with the owning source and next review
action; do not fabricate a destination, approval, command result or author.

Continuity remains the current compact handoff; Git and the tracker retain
history. It is neither a transcript archive nor another architecture document.
Retained evidence keeps actual source revisions, dates and execution limits.
Temporary notes have no durable authority: promote useful requirements and
decisions through normal repository review before discarding scratch. Archival
does not authorize deletion, approval changes, or loss of historical links.

## Optional reference and review examples

[`tools/documentation_layout.py`](../../tools/documentation_layout.py) accepts a
closed explicit inventory. It reads no consumer documents, imports no consumer
code, crawls no checkout, and verifies no Git/provider visibility or approval.
When invoked later, it calls only exact hash-bound existing Hygiene resolvers.
The CLI reads one bounded regular nonsymlink JSON input on hosts supporting
`O_NOFOLLOW` and `O_NONBLOCK`; unsupported input admission is unavailable. The
pure JSON boundary rejects duplicate keys, invalid UTF-8, nonfinite values,
oversize/deep input, traversal/control/backslash/.git path components, and typed
metadata mismatches. The source inventory itself remains declared observations.

```bash
python3 tools/documentation_layout.py /path/to/review-inventory.json
```

Exit `0` means only that no supported declared-inventory gap was found (`advisory`),
`1` means `review_required`, and `2` means unavailable/incompatible. Output is
`local-review-only`, omits inventory names, paths, prose and checksums, and never
claims passing conformance or activation. Caller-declared `visibility: public`
is not public-source authentication. Production acquisition, full link/content
checks and reporting remain with their existing owners.

The [self-contained synthetic cases](../../fixtures/repository-documentation/examples.json)
cover concise and justified-rich READMEs, durable scratch, eager Claude imports,
legacy root compatibility, spaces/Unicode, proposed exceptions, unknown and
archived applicability, and protected input. Expectations are authored examples,
not results from execution. Tests, helper execution, builds, CI, production
discovery and Aether content qualification are deferred under the current user
instruction. See the [consumer migration map](../migration/2026-11-12-documentation-layout.md)
for exact inspected source pins, sequencing, preservation and rollback gates.
