# ADR acceptance and validation plan

## Current capability

Hygiene publishes machine-readable front matter and repository-policy-reference
schemas, compatibility fixtures, and a dependency-free reference checker for
already-decoded JSON objects. The checker deliberately does not parse repository
Markdown or claim to be the fleet validator:

```bash
python3 tools/decisions.py decision \
  --input fixtures/architecture-decisions/decision.proposed.valid.json
python3 tools/decisions.py decision-set \
  --input fixtures/architecture-decisions/decision.superseded.valid.json \
  --input fixtures/architecture-decisions/decision.accepted.valid.json
python3 tools/decisions.py policy-reference \
  --input fixtures/architecture-decisions/policy-reference.valid.json
```

Egolint owns production semantic rules; Relay owns reusable CI and generation
mechanics. A decoded-reference result establishes none of the separate Markdown,
Git-source, collection, publication or deployment outcomes. The complete
[local regression gate](../CONTRACT_VALIDATION.md) runs this helper's suite and
selected fixtures; native source admission remains a distinct result.

## Reference alignment and pinned compatibility — 2026-10-30

[Issue #82](https://github.com/egohygiene/hygiene/issues/82) aligns the current
reference/schema with already selected policy v1.2.0, sections 4, 9 and 10:

- A proposed replacement may declare `supersedes` while the predecessor retains
  its status/body and empty `superseded_by`. A rejected or deprecated proposal
  may retain its declared intent without becoming effective. No old record is
  edited to make a pending or declined proposal pass.
- Effective accepted/superseded replacement declarations retain reciprocal
  lineage and disposition checks. A predecessor with an effective replacement
  must be `superseded`; a proposed, rejected or deprecated record cannot serve
  as the effective replacement. Self-links and cycles among supplied local
  supersession declarations remain invalid, including pending declarations.
- `implementation_status: verified` requires a non-blank named evidence
  descriptor of `type: validation`, with the ordinary URL/description shape.
  Approval, implementation or workflow-run descriptors alone do not satisfy
  this declaration. The helper does not visit the URL, execute its claimed
  command, authenticate an approving person or establish that a result passed.
- Canonical IDs range from `ADR-0001` through `ADR-9999`. `ADR-0000` is invalid.
  Three-/four-digit reference strings keep the accepted historical grammar and
  exact identity lookup. Both widths receive attributable dangling/self-link
  diagnostics; `ADR-006` is never silently treated as `ADR-0006`.
- Globally qualified references are syntax-checked only by this decoded helper;
  it has no repository/index selection or external resolver. Explicit trusted
  pinned indexes and native consumer validation remain separate prerequisites
  for cross-repository resolution.

Exercise the pending pair and structural validation descriptor directly:

```sh
python3 tools/decisions.py decision-set \
  --input fixtures/architecture-decisions/decision.pending-predecessor.valid.json \
  --input fixtures/architecture-decisions/decision.pending-replacement.valid.json
python3 tools/decisions.py decision \
  --input fixtures/architecture-decisions/decision.verified.valid.json
```

The immutable Aether authoring guide at
[`dc8a16851f452763ef4f7fbe4bf057d4500b1921`](https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/skills/architecture/create-decisions-document/references/decision-record-guide.md)
still correctly warns that the older Hygiene helper at its selected policy pin
requires a premature backlink. That historical helper remains unchanged; this
candidate removes the incompatibility in Hygiene's current reference. It does
not edit the Aether warning, repin a consumer or claim native replay. Exact
selected EgoLint `d917ea524962639494e5bb4b3196192238ba57d9` execution was
unavailable because no cached binary was proven bound to that source; a different
cached runtime was not substituted.

The [synthetic historical fixtures](../../fixtures/architecture-decisions/README.md)
retain exact three-digit IDs for the explicitly older policy/helper pin. The
current canonical mode rejects those record IDs while still resolving exact
locally supplied historical references. A separate, explicit synthetic padding
map demonstrates the reviewed-migration shape without renaming actual records.
Current helper/schema changes do not alter any immutable consumer pin or supply
new policy ratification, ADR disposition, original ADR-0001 approval or source
admission. Per-record schema validation cannot establish cross-record lineage;
run `decision-set` as well.

## Phase 1 review gates

- [x] Hygiene is the unambiguous policy and schema owner.
- [x] Aether, Holon, Relay, Observatory, repositories, and `.github` retain their
      stated responsibility boundaries.
- [x] New ADRs begin as `proposed` and cannot become `accepted` without durable
      human approval evidence.
- [x] The schema contains every required front matter field.
- [x] The inheritance schema requires the canonical owner, semantic version,
      and full source commit.
- [x] Local extensions are namespaced and cannot override global semantics.
- [x] Decision status remains independent from implementation status.
- [x] Effective supersession is bidirectional; pending proposals preserve old authority. Local declared supersession remains cycle-free.
- [x] Exceptions are explicit, scoped, owned, and approval-gated.
- [x] Legacy IDs and rationale can be preserved without making them validate as
      new records.
- [x] Public projections fail closed for private or unknown visibility.
- [x] The dashboard plan extends Relay and Observatory instead of adding a new
      framework to every repository.
- [x] No current CI, release, dashboard, or implementation capability is
      represented as complete when it is only planned.

## Egolint and Relay consumer contract

Egolint rules, orchestrated by Relay in CI, execute these deterministic stages:

1. Load exactly one `docs/decisions/policy-reference.json`; validate its
   repository identity, supported semantic version, canonical Hygiene owner and
   path, and full commit pin without resolving a moving branch.
2. Resolve the pinned policy and schema from an explicit trusted checkout or
   verified artifact. Network fetching is never an implicit validation side
   effect.
3. Enumerate `docs/decisions/ADR-*.md` from the represented Git tree in lexical
   path order.
4. Parse only the first YAML front matter document with safe parsing and no
   custom tags, aliases, duplicate keys, or multiple documents.
5. Validate metadata against the pinned Hygiene schema, then validate only
   registered local extensions against repository-owned schemas.
6. Under policy v1.2.0, enforce four-digit canonical IDs and filename/ID
   agreement. Validate older snapshots only through their explicit supported
   policy pin. A naming migration records the number-preserving old/new map;
   four-digit IDs require no legacy-width exception.
7. Detect duplicate local IDs, duplicate global keys, and case-folding path
   collisions.
8. Verify that `docs/decisions/README.md` has exactly one linked row per
   canonical record, including rejected, deprecated, and superseded history.
9. Resolve local and cross-repository decision references against pinned input
   indexes.
10. Preserve pending proposal intent without an effective backlink; validate both
    directions of effective supersession and reject self-links and cycles.
11. Require durable human disposition metadata for every non-proposed status
    without interpreting an automated merge as human authority.
12. Reject prohibited overrides, unregistered extension keys, weakening local
    rules, and unsupported policy versions.
13. Check that `verified` implementation status has validation evidence.
14. Emit errors in stable order with stable rule identifiers and nonzero exit
    status.

Network reachability checks should be separate from structural validation so
offline validation remains reproducible. A link checker may report unavailable
resources but must not copy protected content into logs or artifacts.

## Generated `decisions.json`

Relay should generate the repository decision index from validated front
matter and explicitly allowlisted Markdown fields. The contract should include:

- schema and generator versions;
- repository, source commit, and exact policy/schema pins;
- canonical global decision key and source link;
- status, implementation status, scope, visibility, owners, and date;
- related and supersession keys;
- affected repositories and contracts;
- allowlisted issue, pull-request, release, commit, and validation links; and
- explicit incomplete, invalid, or unavailable states.

Output order is stable by date, ID, and canonical key. JSON uses UTF-8, a final
newline, stable key ordering, and no wall-clock timestamp unless it is an
explicit input. Generated output contains no absolute paths or ambient machine
state.

## Generated `activity.json`

Relay should collect allowlisted GitHub metadata for issues, pull requests,
milestones, releases, and commits. The represented repository, source revision,
visibility policy, and collection window are explicit inputs.

Public-safe events may include type, public number or tag, state, timestamps,
and canonical URL. Titles are opt-in and only allowed when the source repository
and resource are public. Bodies, comments, review text, private titles, actor
identities, email addresses, workflow logs, artifact URLs, and raw API payloads
are never copied into public output.

For a private repository, the default public result is an omitted repository or
aggregate counts with no identifying event text. Unknown visibility is a hard
failure. A separate internal artifact may retain additional allowlisted
metadata, but public and internal outputs must use different explicit targets
that cannot overlap.

## Observatory aggregation plan

Observatory consumes versioned repository `decisions.json` and `activity.json`
contracts. It validates every input, preserves source links and visibility, and
represents missing, stale, invalid, and inaccessible inputs explicitly. It does
not scrape repository Markdown or reinterpret decision status.

The first static UI supports:

- decision list and status filters;
- chronological decision and delivery timelines;
- related/supersession graph;
- links to issues, pull requests, commits, releases, and validation evidence;
- activity for issues, pull requests, milestones, and releases; and
- `/adr` redirection to `/intelligence/decisions`.

## Compatibility fixtures and downstream fixture requirements

Hygiene's `fixtures/architecture-decisions/` covers every decision lifecycle,
including a bidirectional accepted/superseded pair, a pending accepted/proposed
pair, named structural validation evidence, approval-only verified rejection,
canonical zero-ID rejection, a proposed ADR with a namespaced extension,
declared disposition evidence, false acceptance, a valid inherited policy pin
and an invalid moving/wrong-owner pin. Separate historical fixtures preserve
older identities. These synthetic records define minimum cross-consumer
compatibility; their metadata is not live approval or execution evidence.

Egolint and Relay must extend the corpus to cover:

- every decision and implementation status;
- accepted, rejected, deprecated, and superseded dispositions with explicit
  human evidence but independent implementation state;
- a verified implementation with validation evidence;
- a valid supersession pair and a rejected cycle;
- missing, duplicate, malformed, and filename-mismatched IDs;
- missing, moving, unsupported, and owner/path-mismatched policy pins;
- permitted optional and required local extensions plus prohibited overrides;
- canonical four-digit records, rejected three-/five-digit canonical IDs, and
  explicitly pinned historical/alternate-prefix migration fixtures;
- the known Empathy-style ID collision;
- a private repository and private issue metadata;
- deterministic regeneration under different locale, time zone, and working
  directories; and
- incomplete GitHub metadata represented as unavailable rather than success.

## Phase 3 acceptance criteria

- [ ] Validator fixtures cover every status, implementation status, and
      exception state.
- [ ] Identical inputs produce byte-identical JSON outputs.
- [ ] Invalid lineage, duplicate IDs, false approval, and unknown visibility
      fail closed.
- [ ] Moving or unsupported policy pins and prohibited overrides fail closed.
- [ ] Public fixtures contain no protected text, identities, local paths, or
      session data.
- [ ] Egolint defines semantic validation; Relay orchestrates and generates but
      never deploys repository output.
- [ ] Repository sites retain final composition and deployment authority.
- [ ] Observatory aggregates only validated contracts and preserves
      unavailable states.
- [ ] Identity migration proves existing provenance is retained before wider
      rollout.
