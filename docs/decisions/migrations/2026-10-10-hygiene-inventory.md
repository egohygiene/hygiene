# Hygiene ADR inventory and migration checkpoint

This is the preparation checkpoint for [Hygiene #47](https://github.com/egohygiene/hygiene/issues/47)
under [Pace #5](https://github.com/egohygiene/pace/issues/5) and
[the Intelligence program](https://github.com/egohygiene/.github/issues/30).
It inventories existing evidence and proposes the next bounded work. It does
not change decision dispositions, canonical ADR bodies, policy, or publication.

## Observation boundary

- Repository: `egohygiene/hygiene`, public, default branch `main`.
- Inspected source: `b8d2c02368e40d4f6c2017bb1a22c6ec23323ad3`, observed 2026-10-10.
- Full reachable history: 81 commits; checkout is not shallow; no tags were
  advertised by this clone. No open Hygiene pull requests were observed before
  this checkpoint was prepared.
- [Machine-readable inventory](../../evidence/hygiene-adrs-inventory-2026-10-10.json)
  records each canonical ADR's source hash and Git blob, preservation hashes,
  and bounded reference-check results. It is a dated receipt, not a generated
  Decisions publication or a new ADR contract.
- The previous continuity checkpoint still described Hygiene PR #67 as a
  candidate and Observatory #25 as pending. PR #67 is in this inspected main;
  Observatory #25 is closed. This candidate refreshes that operational handoff.

## Source surfaces and ownership

| Surface | Observed role | Migration treatment |
| --- | --- | --- |
| `docs/decisions/ADR-0001-*.md`, `ADR-002-*.md` through `ADR-013-*.md` | 13 organization decisions | Preserve exact identity, filename, body, links and Git history. No ADR-001 alias or duplicate. |
| `docs/decisions/README.md` | Complete 13-row canonical index | Keep as the complete index; correct only its stale policy-acceptance wording and link this packet. |
| `DECISIONS.md` | Compatibility/navigation document with two historical rows and pending topics | Preserve its content; it links the complete index and contains no additional inline ADR to extract. A later navigation cleanup can remove the partial duplicate table. |
| `POLICY.md`, `RATIFICATION.md`, schemas and `catalog/contracts.yaml` | Hygiene-owned accepted v1.1.0 ADR policy and contracts | Preserve ownership and ratification. These are not local ADRs to backfill. |
| `MIGRATION.md`, `VALIDATION.md`, template and fixtures | Organization migration/consumer guidance and reference examples | Do not count templates or fixtures as canonical decisions. Some implementation-status prose predates delivered consumers; reconcile separately with exact producer evidence. |
| Architecture, catalog, source review, roadmap, context and Git history | Supporting evidence and proposed work | Reference evidence selectively; do not turn each commit, pending topic or implementation fact into an accepted ADR. |

All 13 current records concern organization architecture or policy. A new
repository-local implementation decision must explicitly use repository scope;
it must not duplicate or silently redefine those organization records.

Policy section 6 states **Hygiene does not inherit from itself**. The generic
policy-reference checkbox in #47 therefore needs owner-specific treatment:
retain the canonical policy/catalog and verified ratification evidence; do not
create a false `docs/decisions/policy-reference.json` inheritance declaration.

## Record-by-record migration map

The implementation column reports existing source labels, not new verification.
The receipt binds each row to the unchanged source bytes.

| ID and canonical record | Current disposition | Current implementation | Authority and proposed treatment |
| --- | --- | --- | --- |
| [ADR-0001](../ADR-0001-holistic-architecture-v0.1.md), holistic architecture | Legacy Accepted claim, 2026-08-18 | No structured value | No YAML front matter. Preserve four-digit identity and original anatomy; confirm the legacy disposition and migration exceptions before metadata normalization. |
| [ADR-002](../ADR-002-organization-adr-and-delivery-history.md), ADR policy | Accepted | verified | Explicit approval and validation packet exist. Preserve; no repeat policy ratification. |
| [ADR-003](../ADR-003-route-filament-infrastructure-contracts.md), Filament | Proposed | in_progress | Preserve proposal and evidence; no acceptance inferred from implementation. |
| [ADR-004](../ADR-004-register-sanctuary-incubation-boundary.md), Sanctuary | Proposed | in_progress | Missing required Implementation and evidence links section; add it later from existing evidence while preserving original prose. |
| [ADR-005](../ADR-005-unify-repository-intelligence-projection.md), Intelligence projection | Proposed | in_progress | Preserve proposal, including its alpha.2 collection-coverage amendment; do not create a duplicate coverage ADR. |
| [ADR-006](../ADR-006-repository-presentation-profile.md), presentation profile | Proposed | in_progress | Preserve proposal and evidence. |
| [ADR-007](../ADR-007-repository-release-baseline.md), release baseline | Proposed | in_progress | Preserve proposal; it already covers Hygiene's local release validation. |
| [ADR-008](../ADR-008-repository-continuity-policy.md), continuity | Proposed | in_progress | Preserve proposal; local use and context-v2 implementation do not ratify it. |
| [ADR-009](../ADR-009-agent-ready-web-profile-foundation.md), web foundation | Proposed | in_progress | Preserve proposal and evidence. |
| [ADR-010](../ADR-010-agent-ready-web-discovery-representations.md), discovery | Proposed | in_progress | Preserve proposal and evidence. |
| [ADR-011](../ADR-011-agent-ready-web-guarded-capability-commerce.md), guarded capabilities | Proposed | in_progress | Preserve proposal and evidence. |
| [ADR-012](../ADR-012-agent-ready-web-integration-conformance.md), conformance | Proposed | in_progress | Preserve proposal and evidence. |
| [ADR-013](../ADR-013-public-site-surface-route-registry.md), surface registry | Proposed | in_progress | Preserve proposal; its implementation does not choose Hygiene's Decisions host. |

The canonical index resolves all 13 files without duplicate IDs or paths.
The eleven proposed records may remain proposed in a valid Decisions view;
fleet adoption must not force their acceptance.

The later source checkpoint should also reconcile bounded evidence staleness:
ADR-003 and ADR-008 omit known implementing PR links; ADR-005 still requests
ADR-002 approval; ADR-010 through ADR-012 contain old parent/merge wording.
[PR #57](https://github.com/egohygiene/hygiene/pull/57) is merged and its
[parent #16](https://github.com/egohygiene/hygiene/issues/16) and
[checkpoint #53](https://github.com/egohygiene/hygiene/issues/53) are closed.
Use dated correction notes and durable evidence without promoting lifecycle
or implementation labels. ADR-004's anatomy gap is independent of metadata
checks passing.

## ADR-0001 disposition packet

The original record was introduced at
[`a10a05dcd748547c8df31e249559868a7f19faee`](https://github.com/egohygiene/hygiene/commit/a10a05dcd748547c8df31e249559868a7f19faee)
and later amended with dependency-boundary verification at
[`ada6e5f320260cacde25228f31c1a9abed528f1a`](https://github.com/egohygiene/hygiene/commit/ada6e5f320260cacde25228f31c1a9abed528f1a).
[PR #3](https://github.com/egohygiene/hygiene/pull/3) is a concrete legacy
authority candidate: its body explicitly asserts acceptance and it is attributed
to the maintainer. The inspected PR has no reviews and only a bot discussion
comment; [issue #1](https://github.com/egohygiene/hygiene/issues/1) has no comments.
Authorship and merge alone do not resolve whether that assertion is the intended
human disposition. This packet preserves the existing claim and records the
uncertainty instead of inventing approval metadata or downgrading the record.

**Recommended maintainer disposition:** reaffirm the historical acceptance of
the [unchanged source record at this checkpoint](https://github.com/egohygiene/hygiene/blob/b8d2c02368e40d4f6c2017bb1a22c6ec23323ad3/docs/decisions/ADR-0001-holistic-architecture-v0.1.md),
retain `ADR-0001` and its original substantive prose, and approve the narrow
migration exception for its legacy ID/filename width. Source SHA-256:
`5b7a4f36456e80790d4f7d989600310f8effdb2f800058f0f0bb23826730655b`.
Any reaffirmation is recorded with its actual date and durable evidence, not
backdated to the historical claim. Implementation remains independent and is
`unknown` until the next migration supplies bounded evidence for another value.

The policy does not authorize waiving its required seven sections. The source
migration must preserve the original prose and history while adding or
reorganizing the required anatomy with explicit evidence gaps. Retaining a
nonstandard anatomy would need a separate supported policy/validator treatment;
this packet does not propose an exemption that weakens the policy.

This recommendation does not approve ADR-003 through ADR-013 or rewrite the
historical five-plane model into today's six-plane architecture. Filament and
later ownership changes retain their own decision records and review.

ADR-002 is different: the
[explicit v1.1.0 approval](https://github.com/egohygiene/hygiene/issues/15#issuecomment-5647398908)
and [95-test ratification packet](https://github.com/egohygiene/hygiene/issues/15#issuecomment-5647360172)
already resolve its authority. Its `verified` label concerns that policy
package, not all downstream implementations or this migration.

## Historical choices worth recording

The 81-commit review found one narrow repository-local backfill candidate:
[PR #4](https://github.com/egohygiene/hygiene/pull/4) and
[`0d61e6ef26af0630dabafc9636b3061749767883`](https://github.com/egohygiene/hygiene/commit/0d61e6ef26af0630dabafc9636b3061749767883)
establish JSON-compatible YAML 1.2 catalogs and dependency-free Python reference
validation/deterministic projections. `catalog/README.md` explains the actual
tradeoff: preserve `.yaml` contract paths without adding a YAML parser dependency.
The next source checkpoint can draft this as proposed ADR-014 after rechecking
that the ID remains unused. It must not invent rejected runtimes, performance
claims, or a repository-wide Python mandate; diagram tooling also uses Node.

Catalog/context and dependency-boundary work implements ADR-0001. Release,
continuity, web and site-registry work is already covered by ADR-007 through
ADR-013. The alpha.2 coverage addition amends ADR-005. Pending topics in the
root index are not evidence that new decisions were made. Historical review is
bounded by reachable public evidence, not a claim to recover unrecorded intent.

## Prerequisite and publication assessment

| Dependency | Verified preparation state | Remaining boundary |
| --- | --- | --- |
| [Hygiene #15](https://github.com/egohygiene/hygiene/issues/15) | Closed; v1.1.0 explicitly ratified | Preserve accepted policy and ADR-002; decide only unresolved local history. |
| [Holon #6](https://github.com/egohygiene/holon/issues/6) | Closed; migration-safe scaffold exists | Use validate-first. Its current blueprint pins pre-activation `f598ed659a43dd759d4ede41c27f9e5daf991aa7`; do not blindly scaffold or silently upgrade policy. |
| [Relay #5](https://github.com/egohygiene/relay/issues/5), [#99](https://github.com/egohygiene/relay/issues/99) | Open parents; operational advisory workflow | Required-mode and remaining broader acceptance are separate. Hygiene policy-owner support remains missing in the current consumer path. |
| [Relay #27](https://github.com/egohygiene/relay/issues/27), [#33](https://github.com/egohygiene/relay/issues/33) | Open broader parents; collector #115 closed | Identity proves one bounded shared publication, not Hygiene corpus admission or host readiness. |
| [Pace #5](https://github.com/egohygiene/pace/issues/5) | Sequential preparation is ready | Record one repository's source, validation, publication and upkeep independently. |

Hygiene has no site declaration, CNAME, Pages publisher, Repository Intelligence
workflow, architecture workflow or EgoLint configuration in the inspected
tree. Its sole workflow, `release-policy.yml`, performs manual read-only release
validation and does not publish. `ROADMAP.md` explicitly selects central
roadmap publication through `egohygiene.io` and says not to add a second site
deployment. That is not an existing declaration of a Decisions route.

Prefer preparing a source-owned, read-only validated artifact, then review its
composition into the organization host. Do not invent a Hygiene Pages site or
assume an organization `/decisions/` aggregation route is the same product as a
repository `/intelligence/decisions/` ledger. Host and route selection require
their own concrete declaration and publication evidence.

## Production policy-owner compatibility gap

The bounded shared fix is tracked in
[EgoLint #81](https://github.com/egohygiene/egolint/issues/81), including Relay
adoption and positive/negative owner-versus-consumer acceptance cases.

At Relay `f19b65b3f8bd8466884dee5529fa77f2430440b6`, the ADR collector emits a
consumer `policy-reference` configuration unconditionally. Its ADR toolchain
pins EgoLint `2d3600f14848e28099acc34ce8043699da2b9a32`, whose
`src/rules/repository_intelligence.rs` validator requires that file. The
architecture path's EgoLint `933472b6322d2060c487e5a8a6f0bc5197696af0` has the
same behavior. No explicit policy-owner mode was found in those pinned paths.

This conflicts with Hygiene policy section 6. Fix the distinction in EgoLint's
shared validation semantics and Relay's adapter, with an explicit immutable
owner-policy source and fail-closed consumer behavior. Do not add a fake
self-inheritance file, weaken validation, or copy a validator into Hygiene.
Source inspection establishes this gap; a native production run was not made
for this documentation checkpoint.

## Validation results and limits

The unchanged `tools/decisions.py` reference checker was run over safely decoded
YAML front matter from the exact source revision. Extraction rejected aliases
and duplicate/non-string keys, and retained ISO dates as JSON strings.

- Twelve individual `decision --input` calls, ADR-002 through ADR-013: exit 0,
  no diagnostics.
- ADR-0001 has no front matter: no synthetic JSON record was fabricated.
- One `decision-set` call with all twelve decoded inputs: exit 1, exactly eleven
  `E_DANGLING_REFERENCE` diagnostics pointing to omitted ADR-0001 from ADR-002,
  ADR-003, ADR-004 and ADR-006 through ADR-013. Its Markdown file exists; the
  legacy metadata gap prevents its inclusion in this decoded set.
- These are reference metadata checks, not full Markdown conformance, current
  native EgoLint acceptance, a generated site, CI acceptance, or live deployment.

The receipt contains each grouped diagnostic, source digest and checker digest.
Canonical ADRs and policy documents are byte-preserved by this checkpoint.
Documentation link, inventory-preservation and continuity checks are recorded
in the root handoff. No broad runtime or release suite is warranted by this
documentation-only change.

## Ordered next checkpoints

1. Review this migration map and resolve the concrete ADR-0001 recommendation.
   Preserve all eleven proposals and ADR-002's existing ratification.
2. Prepare the source migration: legacy metadata/approved identity exception,
   required anatomy preserving original prose, proposed ADR-014 if still warranted, canonical
   index reconciliation and pinned Aether decision-impact guidance. No duplicate
   policy declaration for its owner.
3. Implement and verify [EgoLint #81](https://github.com/egohygiene/egolint/issues/81)
   policy-owner support in the shared EgoLint/Relay path;
   then validate Hygiene's whole corpus at an exact revision and produce the
   bounded read-only artifact. Keep other uncollected domains explicit.
4. Review the real host/declaration and compose the ledger using shared Relay
   publication. Preserve existing routes/assets, show source and freshness,
   verify the GitHub/org-logo links and keyboard focus, and use/verify the
   organization-logo favicon. Record exact deployed bytes and rollback inputs.
5. Close #47 only when source, review, validation, publication and continuous
   capture meet its acceptance; then select the next repository under Pace #5.

Rollback for this checkpoint is reverting its documentation-only commit. No
canonical ADR, executable, dependency, workflow, release or deployed site changes.
**ADR not required:** this inventory records evidence and proposed follow-up
work without making a new architectural or lifecycle decision.
