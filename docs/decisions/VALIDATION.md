# ADR acceptance and validation plan

## Current capability

This foundation pull request defines contracts and review criteria only. It does
not claim that organization-wide ADR validation, JSON generation, GitHub
activity collection, routing, or dashboards are implemented. Until Relay ships
the approved tooling, review is manual and repository-local CI remains
unchanged.

## Phase 1 review gates

- [ ] Hygiene is the unambiguous policy and schema owner.
- [ ] Aether, Holon, Relay, Observatory, repositories, and `.github` retain their
      stated responsibility boundaries.
- [ ] New ADRs begin as `proposed` and cannot become `accepted` without durable
      human approval evidence.
- [ ] The schema contains every required front matter field.
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

## Relay validator plan

The Phase 3 validator should execute these deterministic stages:

1. Enumerate `docs/decisions/ADR-*.md` from the represented Git tree in lexical
   path order.
2. Parse only the first YAML front matter document with safe parsing and no
   custom tags.
3. Validate metadata against the pinned Hygiene schema.
4. Enforce filename/ID agreement for new records and require an approved or
   migration-pending exception for legacy variance.
5. Detect duplicate local IDs, duplicate global keys, and case-folding path
   collisions.
6. Resolve local and cross-repository decision references against pinned input
   indexes.
7. Validate both directions of supersession and reject self-links and cycles.
8. Require approval metadata for accepted and superseded records without
   interpreting an automated merge as human approval.
9. Check that `verified` implementation status has validation evidence.
10. Emit errors in stable order with stable rule identifiers and nonzero exit
    status.

Network reachability checks should be separate from structural validation so
offline validation remains reproducible. A link checker may report unavailable
resources but must not copy protected content into logs or artifacts.

## Generated `decisions.json`

Relay should generate the repository decision index from validated front
matter and explicitly allowlisted Markdown fields. The contract should include:

- schema and generator versions;
- repository, source commit, and policy/schema pins;
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

## Test fixture plan

Phase 3 fixtures must cover:

- a minimal proposed repository ADR;
- an accepted ADR with explicit approval evidence but no implementation;
- a verified implementation with validation evidence;
- a valid supersession pair and a rejected cycle;
- missing, duplicate, malformed, and filename-mismatched IDs;
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
- [ ] Public fixtures contain no protected text, identities, local paths, or
      session data.
- [ ] Relay generates but never deploys repository output.
- [ ] Repository sites retain final composition and deployment authority.
- [ ] Observatory aggregates only validated contracts and preserves
      unavailable states.
- [ ] Identity migration proves existing provenance is retained before wider
      rollout.
