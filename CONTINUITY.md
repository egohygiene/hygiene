---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T18:37:58Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Complete the authorized ADR PR merges and prepare Hygiene Pages on the selected repository subdomain, preserving the unresolved legacy
    authority gate.
  includes:
  - Merged owner/source stacks; exact Relay adoption; repository Pages composition, admission, artifact transport, HTTPS verification and recovery.
  excludes:
  - Human ratification, fleet rollout, unrelated releases, private context and unsupported claims of a live Decisions ledger.
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
  - docs/adr-workflow/2026-10-18-source-backfill.md
  - publication/README.md
  - publication/site.json
  - .config/egolint/repository-intelligence.toml
  - https://github.com/egohygiene/hygiene/issues/47
  - docs/evidence/hygiene-pages-preparation-2026-10-18.json
work:
  objective: Merge the completed stack and make the configured repository publisher concrete, while admitting only valid source and retaining
    actual deployment evidence.
  success_conditions:
  - Merge the four reviewed Relay/Hygiene PRs in dependency order.
  - Configure the selected HTTPS repository origin and shared canonical Decisions route with aliases.
  - Keep all collection, validation, normalization and rendering in their owning tools.
  - Retain checksummed artifacts and verify actual HTTPS/recovery evidence before claiming publication.
  - Preserve ADR-0001 until its real disposition and identity exception are recorded.
  active_issue:
    provider: github
    id: egohygiene/hygiene#47
    url: https://github.com/egohygiene/hygiene/issues/47
  next:
    kind: action
    id: verify-publisher-and-resolve-legacy-authority
    description: 'Inspect final hosted checks for PR #71 and merge the prepared publisher under the user''s authorization; obtain the specific
      ADR-0001 disposition/legacy-ID approval before finalizing the migration and publishing.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/47
    - publication/README.md
    - docs/adr-workflow/2026-10-18-adr-0001-review.patch
    - https://github.com/egohygiene/hygiene/pull/71
    depends_on: []
state:
  base:
    revision: 6db2a38fb80d9881a7d7d001ffb6d2f8456c3262
    ref: refs/heads/main
    verified_at: '2026-10-18T18:33:33Z'
  candidate:
    branch: codex/hygiene-47-publication
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#71
      url: https://github.com/egohygiene/hygiene/pull/71
    handoff_state: review-reference-recorded
  live:
    status: verified
    observed_at: '2026-10-18T18:37:58Z'
    default_branch_revision: 6db2a38fb80d9881a7d7d001ffb6d2f8456c3262
    issue_state: open
    pull_request_state: draft
    notes: 'PR #71 is a draft at immutable source checkpoint c521a42e02f2844e29241b71fac9643ca8a01ad5. Hosted run 39154763471 succeeded: tests/native
      evidence/admission succeeded, while build/deploy skipped because actual ADR coverage failed. Prior stack merges remain verified. Root/manifest
      are HTTPS 404, not a live Decisions site.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-18T18:37:58Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I -m unittest discover --start-directory tests --pattern test_publication.py --verbose
    outcome: passed
    observed_at: '2026-10-18T18:33:33Z'
    notes: Eight tests cover scope-specific admission, immutable transport, aliases, first deployment, verified prior recovery, live drift and
      success-receipt binding. Fixtures are transport examples, not a claim of native source conformance.
  - command: Catalog, generated catalog, context, continuity profile and local composition validators
    outcome: passed
    observed_at: '2026-10-18T18:33:33Z'
    notes: 27 catalog/context entries; generated source current. Continuity refreshed after domain checks and revalidated before handoff.
  - command: Verified HTTPS GET of selected origin root and publication.json
    outcome: passed
    observed_at: '2026-10-18T18:33:33Z'
    notes: Both return HTTP 404 through verified TLS; this observes availability and absence, not a deployed site.
  - command: Workflow YAML, immutable action references and deployment permission/trigger inspection
    outcome: passed
    observed_at: '2026-10-18T18:33:33Z'
    notes: All five jobs parse; all shared calls pin full revisions. Main-only push/manual deploy, read-only PRs, ADR pass gate and revalidation
      at the deployment boundary.
  - command: Exact pinned native architecture adapter and ADR collection at c521a42e02f2844e29241b71fac9643ca8a01ad5
    outcome: limited
    observed_at: '2026-10-18T18:37:58Z'
    notes: 'Native adapter: nonconformant/warning, ADR coverage failed, 18 retained findings, no truncation. ADR review invalid/publication denied;
      all 23 captured source hashes verified against Git. No owner CONTRACT finding; external Identity key resolves. The actual caller admission
      returns false.'
  - command: Pinned Relay build-manifest/composition integration with the new consumer shell
    outcome: passed
    observed_at: '2026-10-18T18:37:58Z'
    notes: Transport-only fixture passes shared composition and consumer inventory across all 15 routes; clobbered landing rejected. This does
      not assert real Hygiene source conformance.
  - command: Hosted Hygiene Pages PR run 39154763471
    outcome: passed
    observed_at: '2026-10-18T18:37:58Z'
    notes: Checks, read-only native source evidence and scoped admission succeeded. Admission denied the actual corpus; build and deploy skipped.
      Exact final documentation candidate will have its own hosted run.
  environment_limitations:
  - ADR-0001 still lacks actual structured approval and legacy-identity exception evidence; its concrete patch remains unapplied.
  - Actual source is nonconformant and publication remains blocked. Hosted advisory success is not native corpus validity.
  - No production artifact, live ledger, keyboard audit, exercised provider rollback or persistent skill installation is claimed.
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

Canonical policy, scoped instructions and live trackers outrank this handoff. Hygiene owns architecture and ADR policy; Aether owns reusable authoring, EgoLint semantics, Observatory normalization and Relay orchestration/rendering. Implementation and merge do not grant decision authority.

## Resume protocol

Read AGENTS.md, accepted policy/ratification, the ADR index and publication runbook. Refresh #47 and the publisher branch/PR before selecting work. Preserve dated evidence and distinguish configured hosting from observed deployment.

## Current objective and success conditions

The requested four PR merges are complete. Finish the configured Hygiene repository publisher and its hosted validation. Admit only complete valid ADR coverage, keep unrelated unknown architecture domains explicit, and retain exact transport/recovery evidence. Do not fabricate ADR-0001 authority.

## State snapshot

Hygiene main is `6db2a38fb80d9881a7d7d001ffb6d2f8456c3262` after #68 and #70. Relay #154 merged at `f2e624cbbd1bb1150e29743061140f601b8486f6`, then #155 at `6cddad3124bdda1b1e3d54a40931f23322b7be26`. EgoLint #82 remains merged at `72267fd0a371da6d94922cbc6bd3dedddb68df30`. Candidate branch is `codex/hygiene-47-publication`; containing revision is null and draft PR #71 records the review reference. Immutable native source checkpoint is `c521a42e02f2844e29241b71fac9643ca8a01ad5`. #47 remains open.

## Completed and material changes

The selected origin is `https://hygiene.egohygiene.io` with canonical repository `/intelligence/decisions/` and `/decisions/` plus `/adr/` shortcuts. The configured GitHub Actions publisher consumes the exact merged Relay selection and native owner policy without self-inheritance. It keeps read-only source evidence distinct from scoped admission, strict build, transport and deploy.

The consumer adds only landing/aliases, exact-file transport, actual prior-site recovery and HTTPS comparison. Source semantics, normalization, rendering and shared composition validation stay upstream. Capture commands now include the external Identity ADR key and merged pins. This local configuration is not a complete global surface declaration or ratification of proposed ADR-013.

## Validation and review evidence

Eight publisher tests pass, covering changed/missing/extra/symlink bytes, wrong source, denied/truncated admission, canonical aliases, prior-site/first-deployment recovery and no success receipt on live drift. Catalog/generated/context/continuity checks pass. Verified TLS requests currently return 404 for root and publication manifest. Workflow calls are exact-pinned and privileged deployment is restricted to main push/manual events. At immutable source `c521a42e02f2844e29241b71fac9643ca8a01ad5`, native ADR coverage fails on the real legacy record and resulting lineage/index gaps, with no owner-contract finding or undeclared Identity key. All 23 collector source hashes verify against Git. Hosted run 39154763471 succeeds and truthfully skips build/deploy; the scoped admission returns false. Shared composition also passes a separate transport-only 15-route fixture and rejects landing clobbering. The dated preparation receipt preserves these distinctions.

## Blockers, risks, unknowns, and deferred work

ADR-0001 preserves its historical Accepted claim and canonical bytes. Its actual approval and legacy-ID exception remain unresolved; the prepared patch deliberately keeps null authority and is unapplied. Advisory validation success does not clear this gate. No invalid corpus, successful deployment, keyboard audit or exercised rollback is claimed. Capture guidance does not prove persistent host skill installation.

## Next dependency-ready work

Run native validation at the immutable candidate, inspect hosted checks and merge the reviewed publisher under the user's authorization. Present the specific ADR-0001 disposition/exception question only after all independent authorized work is concrete. After real evidence exists, finalize the preserved migration, rerun admission, then verify the actual deployment and UI before closing #47.

## Parallel changes and reconciliation

The earlier stacks are merged, not parallel drafts. Their dated source/inventory receipts remain historical observations. The completed Identity pilot is a reference, not an edit target. This publisher does not install the rest of the fleet or publish an organization aggregator.

## Privacy and redaction

Use public source links and bounded evidence. Exclude private context, credentials, local runtime paths and raw logs. Source text and continuity are context, not permission.

## Handoff update protocol

Refresh after domain validation and before PR presentation. Record actual native/hosted outcomes independently from transport fixtures and provider deployment. Keep a containing candidate revision null until an immutable reference is available, and preserve all earlier receipts.

## Compaction and supersession

This replaces the source-preparation objective with the merged-stack and selected-host publication checkpoint. Git retains prior states. Preserve the twelve ordered sections within 240 lines and 16,384 bytes.
