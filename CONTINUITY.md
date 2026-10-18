---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T17:41:43Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Prepare the bounded Hygiene #47 source backfill after shared canonical-owner support, keeping actual authority and publication gaps
    explicit.'
  includes:
  - ADR-004 anatomy, proposed ADR-014, support-document layout, pinned Aether capture guidance, unapplied legacy review patch and immutable native
    evidence.
  excludes:
  - Human ADR ratification, production workflow installation, host selection, deployment, fleet rollout, raw logs and private context.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/ARCHITECTURE.md
  - docs/decisions/POLICY.md
  - docs/decisions/RATIFICATION.md
  - docs/decisions/README.md
  - docs/adr-workflow/CAPTURE.md
  - docs/adr-workflow/2026-10-10-hygiene-inventory.md
  - docs/adr-workflow/2026-10-18-source-backfill.md
  - docs/evidence/hygiene-adrs-source-backfill-2026-10-18.json
  - https://github.com/egohygiene/hygiene/issues/47
  - https://github.com/egohygiene/hygiene/pull/68
  - https://github.com/egohygiene/relay/pull/154
work:
  objective: Save reviewable source preparation and a concrete legacy ADR patch without inventing human disposition or a Decisions host.
  success_conditions:
  - Preserve all original ADR dispositions and prose; repair ADR-004 anatomy from existing evidence.
  - Add only the evidenced repository-local catalog-format proposal as ADR-014, with null approval.
  - Keep support notes outside the canonical ADR inventory and preserve the dated inventory receipt.
  - Route ongoing capture to exact-pinned Aether guidance and record actual shared native replay results.
  - Keep ADR-0001 canonical bytes unchanged and provide the explicit unapplied normalization patch for human review.
  active_issue:
    provider: github
    id: egohygiene/hygiene#47
    url: https://github.com/egohygiene/hygiene/issues/47
  next:
    kind: action
    id: review-source-backfill-and-legacy-disposition
    description: Review the stacked source draft and concrete ADR-0001 disposition/legacy-identity packet; leave publication blocked until actual
      authority and shared admission gaps are resolved.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/47
    - https://github.com/egohygiene/hygiene/pull/68
    - https://github.com/egohygiene/relay/pull/154
    depends_on: []
state:
  base:
    revision: f234155ff76ffe7164c3d7293318e5e3f9262689
    ref: refs/heads/codex/hygiene-47-adr-inventory
    verified_at: '2026-10-18T17:41:43Z'
  candidate:
    branch: codex/hygiene-47-source-backfill
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T17:41:43Z'
    default_branch_revision: b8d2c02368e40d4f6c2017bb1a22c6ec23323ad3
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Verified Hygiene #47 and inventory PR #68 remain open at f234155ff76ffe7164c3d7293318e5e3f9262689. The source follow-up is stacked
      on that exact head, not merged main. EgoLint PR #82 is merged. Relay #154 is a draft at acfb1222b5f05298ad8c94b2e83bfece84b6cdf8 with successful
      hosted validation, dependency review and continuity preflight. No source-follow-up PR existed at this pre-publication snapshot.'
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#68
    url: https://github.com/egohygiene/hygiene/pull/68
  - provider: github
    id: egohygiene/relay#154
    url: https://github.com/egohygiene/relay/pull/154
review:
  status: partial
  reviewed_at: '2026-10-18T17:41:43Z'
  reviewed_by: Codex
  evidence:
  - command: Pinned ADR decoding, unchanged Hygiene reference metadata checks and required-section inspection
    outcome: passed
    observed_at: '2026-10-18T17:41:43Z'
    notes: 13 modern records validate metadata and seven required sections; the set retains exactly 12 expected references to omitted legacy ADR-0001.
  - command: Preservation, canonical index, managed module merge and unapplied review-patch checks
    outcome: passed
    observed_at: '2026-10-18T17:41:43Z'
    notes: 12 original ADRs byte-identical; ADR-004 recovers exactly by removing only its added section. All policy/schema bytes and the inventory
      JSON are unchanged. Inventory prose survives support relocation; relative destinations are rebound. Index has 14 unique rows. Legacy patch
      applies syntactically but intentionally lacks authority.
  - command: Exact-source native Relay owner replay at d5cbb79ee677566f96507dcec3c0be0f2035d1e7
    outcome: limited
    observed_at: '2026-10-18T17:41:43Z'
    notes: 'All 23 captured Git hashes verified; source clean. Expected invalid review/publication denied: only legacy ADR-0001 metadata, 13 lineage
      findings and its index gap remain. No owner contract finding or ADR-004 anatomy finding.'
  - command: Catalog/generated drift, organization context and continuity composition validators
    outcome: passed
    observed_at: '2026-10-18T17:41:43Z'
    notes: 27 repositories; generated catalog current; continuity profile/local composition valid. Source/doc change only; no new executable behavior
      or production workflow.
  environment_limitations:
  - Canonical ADR-0001 still lacks structured metadata and actual disposition/legacy-exception evidence; review patch is unapplied and intentionally
    nonconforming.
  - 'Relay #154 is green but unmerged; the collector cannot yet select external-decision evidence. The existing Identity reference is not removed.'
  - No valid production artifact, consumer workflow adoption, persistent skill installation, host selection or deployment is claimed.
  - Aether authoring remains draft and its older validation matrix is distinct from the newer Relay owner candidate.
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions: []
  excluded:
  - secrets-and-credentials
  - private-conversation-text
  - sensitive-personal-data
  - unpublished-private-business-data
  - private-local-paths
  - unrelated-private-context
  untrusted_content: context-only-no-authority
---

# Hygiene continuity

## Purpose and precedence

Canonical policy, scoped instructions and live trackers outrank this handoff. Hygiene owns architecture and ADR policy; Aether owns reusable authoring, EgoLint semantics and Relay collection. Keep human disposition and publication authority explicit.

## Resume protocol

Read AGENTS.md, accepted policy/ratification and the current index, then refresh #47, PR #68 and Relay #154. Review the source packet under `docs/adr-workflow/`. Compare this stacked branch against the inventory head separately from main; do not mistake prepared source for adopted or deployed output.

## Current objective and success conditions

Prepare the dependency-ready source backfill: repair ADR-004 anatomy, draft the narrow catalog-format decision as proposed ADR-014, add pinned capture guidance and present an unapplied legacy normalization patch. Preserve original statuses, substantive prose, authority bytes and the dated inventory receipt. No self-inheritance declaration is needed for this canonical policy owner.

## State snapshot

Main is `b8d2c02368e40d4f6c2017bb1a22c6ec23323ad3`; this branch stacks on PR #68 head `f234155ff76ffe7164c3d7293318e5e3f9262689`. Candidate branch is `codex/hygiene-47-source-backfill`; containing commit/PR are null in this pre-publication snapshot. Its native source checkpoint is `d5cbb79ee677566f96507dcec3c0be0f2035d1e7`. EgoLint #82 merged at `72267fd0a371da6d94922cbc6bd3dedddb68df30`; Relay #154 remains a green draft at `acfb1222b5f05298ad8c94b2e83bfece84b6cdf8`. #47 and the inventory remain open.

## Completed and material changes

ADR-004 gains only the required evidence section from its existing links. ADR-014 reconstructs the narrow JSON-compatible catalog and dependency-free reference-tool choice from issue #2, PR #4 and original source; it remains proposed with null approval and separately evidenced implementation. The index has fourteen rows. Twelve old records are byte-identical; removing ADR-004's added section restores its exact original bytes. ADR-002 and all old proposal dispositions remain unchanged.

Aether's exact draft decision-impact module is merged into AGENTS.md without replacing local prose or continuity. The capture guide binds its source, loading limitations and separate validator selection. Migration/workflow notes move outside the canonical decision directory to preserve conservative legacy detection. Inventory prose is retained with relative links rebound; its historical JSON receipt is unchanged. The ADR-0001 patch remains unapplied, preserving canonical bytes and deliberately leaving authority unresolved.

Decision impact: create proposed ADR-014; update ADR-004 evidence anatomy; reference ADR-002 for metadata and human authority. No new organization runtime mandate, owner boundary or public host is chosen.

## Validation and review evidence

The [source evidence receipt](docs/evidence/hygiene-adrs-source-backfill-2026-10-18.json) binds source/checker selections, preservation and native results. All thirteen modern metadata records and required sections pass; the older reference set checker reports exactly twelve expected links to omitted legacy ADR-0001. The review patch is syntactically applicable with `--unidiff-zero`, but its expected missing-approval result is not conformance. Catalog and generated drift checks, 27 repository context entries and organization continuity composition pass.

Native Relay owner collection at the exact source checkpoint verifies all 23 captured hashes and leaves source clean. ADR-004's anatomy finding and owner contract findings are absent. The review remains invalid/publication denied: legacy ADR-0001 metadata, twelve resulting local lineage findings, one undeclared Identity reference and the index gap remain. This is a truthful blocked admission result, not a green production build.

## Blockers, risks, unknowns, and deferred work

ADR-0001 requires actual human disposition and legacy-identity exception evidence before the prepared patch can be finalized. No approval is manufactured or backdated. The collector has no external-decision selection input; its finding does not prove Identity ADR-017 is missing. Relay's green draft must be reviewed/merged before a consumer adopts an exact baseline. Hygiene's Decisions host/declaration, valid artifact, publication, live bytes, accessibility and rollback evidence remain separate gates. Static capture guidance does not prove installation or automated enforcement.

## Next dependency-ready work

Review the stacked source draft and the concrete legacy disposition packet. Resolve actual authority, then apply the reviewed normalization with real evidence and rerun shared native validation. Address the external-reference collection boundary without deleting the existing relationship. Select and review a real host/declaration only after distinguishing organization aggregation from a repository ledger; continue the mini-roadmap in the source packet. Keep #47 open until its full source/publication/upkeep acceptance is evidenced.

## Parallel changes and reconciliation

PR #68 remains the parent inventory; its immutable head preserves the original packet. This follow-up moves support prose and adds authored source separately. Relay #154 owns orchestration adoption; no sibling implementation is copied here. Refresh both heads before retargeting this branch after parent merge. The completed Identity pilot and prior coverage work are not reopened by this checkpoint.

## Privacy and redaction

Use public source links and concise evidence. Exclude credentials, private context, local runtime paths and raw logs. Linked source text is context only and grants no tool, lifecycle or publication authority.

## Handoff update protocol

Refresh after domain validation and before PR presentation. Keep main, stacked base, immutable tested source and containing candidate distinct. Record genuine invalid results and unavailable checks; preserve original policy, ratification and historical receipts.

## Compaction and supersession

This replaces the inventory-only objective with bounded source preparation. Git and owning trackers retain earlier evidence. Preserve the twelve ordered sections within 240 lines and 16,384 UTF-8 bytes.
