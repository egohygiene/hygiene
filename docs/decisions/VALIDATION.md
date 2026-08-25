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

Organization-wide Markdown validation, JSON generation, GitHub activity
collection, routing, and dashboards remain unimplemented. Egolint owns the
production semantic rules; Relay owns reusable CI and generation mechanics.
Until those consumers ship against an approved pin, review is manual and
repository-local CI remains unchanged.

## Phase 1 review gates

- [ ] Hygiene is the unambiguous policy and schema owner.
- [ ] Aether, Holon, Relay, Observatory, repositories, and `.github` retain their
      stated responsibility boundaries.
- [ ] New ADRs begin as `proposed` and cannot become `accepted` without durable
      human approval evidence.
- [ ] The schema contains every required front matter field.
- [ ] The inheritance schema requires the canonical owner, semantic version,
      and full source commit.
- [ ] Local extensions are namespaced and cannot override global semantics.
- [ ] Decision status remains independent from implementation status.
- [ ] Supersession is bidirectional and cycle-free by policy.
- [ ] Exceptions are explicit, scoped, owned, and approval-gated.
- [ ] Legacy IDs and rationale can be preserved without making them validate as
      new records.
- [ ] Public projections fail closed for private or unknown visibility.
- [ ] The dashboard plan extends Relay and Observatory instead of adding a new
      framework to every repository.
- [ ] No current CI, release, dashboard, or implementation capability is
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
6. Enforce filename/ID agreement for new records and require an approved or
   migration-pending exception for legacy variance.
7. Detect duplicate local IDs, duplicate global keys, and case-folding path
   collisions.
8. Verify that `docs/decisions/README.md` has exactly one linked row per
   canonical record, including rejected, deprecated, and superseded history.
9. Resolve local and cross-repository decision references against pinned input
   indexes.
10. Validate both directions of supersession and reject self-links and cycles.
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
including a bidirectional accepted/superseded pair, a proposed ADR with a
namespaced extension, durable human disposition evidence, false acceptance, a
valid inherited policy pin, and an invalid moving/wrong-owner pin. These
fixtures define minimum cross-consumer compatibility.

Egolint and Relay must extend the corpus to cover:

- every decision and implementation status;
- accepted, rejected, deprecated, and superseded dispositions with explicit
  human evidence but independent implementation state;
- a verified implementation with validation evidence;
- a valid supersession pair and a rejected cycle;
- missing, duplicate, malformed, and filename-mismatched IDs;
- missing, moving, unsupported, and owner/path-mismatched policy pins;
- permitted optional and required local extensions plus prohibited overrides;
- four-digit and alternate-prefix legacy records with migration notes;
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
