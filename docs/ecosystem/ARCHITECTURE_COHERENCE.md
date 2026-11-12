# Architecture-coherence governance policy

Version `1.0.0-alpha.1` · **proposed**, approval `null` · Refs
[Hygiene #59](https://github.com/egohygiene/hygiene/issues/59).
Governing proposal: [ADR-0017](../decisions/ADR-0017-architecture-coherence-governance.md).
The [machine profile](../../catalog/architecture-coherence-policy.json) and its
[schema](../../schemas/architecture-coherence-policy.v1.schema.json) describe
this exact version. Merge, implementation and source validation do not activate
policy, ratify an architecture or waive Hygiene #47's existing human source hold.

## Purpose and ownership

A coherence review asks whether the represented responsibilities, dependency
directions and design choices form an intentional basis for continued work.
It is distinct from contract adoption, operational Health, audit severity, CI,
implementation completeness and release readiness. A system can be coherent
with unresolved audit findings, or conformant with an architecture that a human
wants revised. Complexity alone is neither failure nor proof of value.

Hygiene owns applicability, evidence/governance and freshness semantics.
[Aether #87](https://github.com/egohygiene/aether/issues/87) owns the portable
full review/assessment contract, explanation, critique, alternatives, authoring
skill and Human Alignment Anchor procedure. This policy embeds no prompt.
[Observatory #21](https://github.com/egohygiene/observatory/issues/21) owns
read-only normalization and public repository/fleet queries. Relay owns bounded
capture, transport and repository presentation. Pace proposes reviewed adoption
changes. Each repository owns canonical architecture, local facts, human
authority sources and final publication. No owner is transferred.

ADRs preserve consequential choices and their dispositions. A coherence review
can identify a missing or contradictory ADR, but cannot rewrite its lifecycle.
Audit evidence can inform a review without becoming ratification. Human
ratification accepts only the represented architecture as an intentional basis
for work; it certifies neither optimality nor correctness, security, conformance
or permanence.

## Applicability and progressive adoption

Missing applicability remains `unknown`. A declared owner source may choose
`required`, `recommended` or `optional`, with dated rationale and evidence.
Candidate required triggers are an architecture milestone; material ownership,
topology or organization change; an accepted ADR that changes topology; a new
cross-repository dependency, persistence or trust boundary; a major runtime
replacement; a split/merge/extraction; source-backed architecture drift; or a
material architecture-document change. An explicit human invalidation is also
material when independently verified. Repeated ownership confusion and an
explicit maintainer request are recommended review triggers.

These are sourced classifications, not heuristics over commit volume, changed
file names, complexity, audit severity or an AI confidence score. Routine
implementation is noninvalidating. A caller does not infer `required` merely
because a new source is missing. The reference evaluator can expose `review-due`
from explicit scoped triggers while retaining declared applicability `unknown`.

`not-applicable` requires narrow scope, rationale and explicit human authority.
`deferred` additionally requires a future UTC deadline. Those fields remain
unverified claims until separate trusted human evidence is supplied; then a
deferred applicability becomes `review-due` after its deadline. A temporary
deferral is not a permanent exemption or an accepted architecture.
An admitted material event after the exception's dated declaration also makes
its current applicability unknown and review due. The original human exception
remains a verified historical claim; it cannot mask a new material boundary.

Adopt progressively: observe → advisory → review-due → scoped ratchet/enforce
where mature and explicitly adopted. This profile installs no scheduler,
publisher, gate or organization-wide blocker. Required/current record existence
and freshness may later inform conformance; architecture quality remains a
separate human judgment. Proposed applicability is not active enforcement.

## Governance source and assessment binding

The [closed governance schema](../../schemas/architecture-coherence-governance.v1.schema.json)
defines `egohygiene.architecture-coherence-governance/v1`. It is a governance
subrecord; Aether's full assessment remains the canonical review artifact.

Each source preserves visibility, a stable scope key, explicit repository
members and exactly one full immutable revision per member. Repository scope
uses the canonical repository key and one member. Subsystem scope uses
`<repository>:<stable-slug>` and one member. Organization scope uses
`egohygiene` and an explicit nonempty member set. A public organization review
represents only those admitted members; it does not imply coverage of protected
repositories or ratify their architectures. Organization and repository
ratification are separate acts, even at matching source revisions.

Progress is `not-started`, `due`, `in-progress` or `complete`. A complete review
has an immutable `review_ref` with ID, canonical URL, completion time and
`assessment_sha256`. That digest binds the canonical Aether assessment subject
**excluding governance**, preventing a circular digest when a later human
decision is appended. Noncomplete progress has no completed review reference.

A human decision preserves disposition, public governance-authority reference,
durable evidence URL/time, exact review ID/assessment digest, scope key,
represented revisions, notes and follow-up references. Supported dispositions
are `ratified`, `ratified-with-notes`, `revision-required`, `rejected`, `deferred`
and `not-applicable`. Ratification with notes requires actual notes. Every
disposition is a source claim until independently verified. AI output cannot
populate verified human context. Silence, continued work, a merge, a passing
check, a closed issue and a field labelled `human` are insufficient.

## Trusted human evidence boundary

The [standard-library reference](../../tools/architecture_coherence.py) checks
shape and bindings; it cannot authenticate a person or fetch approval evidence.
`admit_governance(value, public_repositories=...)` and its `validate_governance`
alias return a validated public source or `None` for an exclusion. Callers supply
a separately authenticated public roster; source claims do not authenticate it.

`human_statement(governance, kind="decision"|"applicability", public_repositories=...)`
returns the exact public statement subject. `statement_sha256(subject)` hashes
UTF-8 JSON with sorted keys, compact separators, `ensure_ascii=False`,
`allow_nan=False` and no trailing newline. Decision statements bind the review
and expiry as well as scope/revisions; applicability statements bind their own
scope/deadline without acquiring an unrelated later review reference.

A trusted adapter must independently verify authentic human provenance and
exact statement content **before** constructing
`TrustedHumanEvidence(statement_sha256, capture_sha256)`. The immutable type
has no JSON decoder. It is an explicit trusted-code input, not a credential,
signature verifier or attestation service. Its capture digest stays operational
and is never emitted by evaluation. Do not construct it from review JSON,
AI/provider recommendations, a `human` actor label or a self-declared hash.
This foundation implements no such provider adapter and creates no real
human-evidence instance.

Without matching typed context, evaluation preserves
`claimed_human_disposition`, but `human_disposition` is `null` and
`human_evidence` is `unverified`. An unverified applicability exemption/deferral
has effective applicability `unknown` and state `unavailable`. The separate
source claim remains available for review. No raw source JSON can self-ratify.

## Freshness, material changes and normalized state

`evaluate(governance, as_of=..., public_repositories=..., material_changes=(),
change_inventory="unknown", current_revisions=None, availability="unavailable",
trusted_human_evidence=())` is pure and reads no system clock. `current_revisions`
uses the same sorted repository/revision list as the source. A changed Git SHA
sets `revision_match="different"`; it does not establish materiality.

The [material-change schema](../../schemas/architecture-coherence-material-change.v1.schema.json)
binds each event to public scope, review ID, explicit classification, evidence
and observation time. A `null` review ID permits an explicitly scoped trigger
before any completed review. Only events after the completed assessment count
against it. Future observations are invalid. Explicit human invalidation also
requires typed evidence for `material_change_statement(...)`; an unverified
claim is retained separately and cannot establish passing freshness.

An explicit `valid_until` becomes stale strictly after that deadline. No default
wall-clock expiry is invented. A witnessed relevant material event can establish
staleness despite partial inventory. Otherwise a completed review is current
only with `change_inventory="complete"`; unknown, partial or unavailable
inventory yields unknown freshness. Empty input alone proves no completeness.

The result keeps applicability, progress, claimed and verified human
dispositions, evidence state, freshness, revision match and trigger IDs separate.
Effective states include `not-reviewed`, `review-due`, `review-in-progress`,
human dispositions, `stale`, `not-applicable`, `deferred` and `unavailable`.
A completed AI assessment without a verified human decision remains
`review-in-progress`. Verified decisions with unknown current freshness are
historical human dispositions with effective state `unavailable`; witnessed
invalidation/expiry yields `stale` without changing their historical source.
No scores are calculated.

For an absent source, only explicit `availability="missing"` yields
`not-reviewed`; inaccessible or uncollected evidence stays `unavailable`.
Excluded protected input cannot become an absence placeholder.

## Privacy, compatibility and deferred qualification

Public admission precedes IDs, prose, duplicate validation, counts and hashes.
If any represented member is not admitted, omit the whole record rather than
partially relabelling its original scope. Irrelevant change scopes/review IDs
are omitted before payload validation and selected limits. Do not publish
excluded identities, counts, raw input digests, private authority details or
process diagnostics. The initial reference profile evaluates admitted public
Ego Hygiene scopes only; schema visibility supports internal/restricted source
authoring without providing an implicit public export path.

Consumers pin this helper, schemas and policy together at one reviewed immutable
revision. Unsupported versions fail closed. Incompatible authority, scope or
freshness semantics require a successor contract and migration. This change
does not modify existing graph/read models, catalog roles, policy activation,
owner pins, historical source approvals or recovery evidence.

Tests, fixtures, native evaluation, provider adapters, hosted execution, broader
qualification and actual ratification remain deferred. Static schema/source
inspection is not evidence of those outcomes. Aether, Observatory and Relay
integration may be implemented against the proposed immutable contracts while
policy adoption and human disposition remain separate.
