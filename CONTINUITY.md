---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-30T22:56:30Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Require qualifying current evidence for passing presentation slot, assessment and badge claims in Hygiene
    #81.'
  includes:
  - 'Bounded #81 existing current-evidence support invariant, deterministic slot/aggregate reference semantics,
    schema/example agreement and semantic compatibility.'
  excludes:
  - "Other batch implementation; #83\u2013#85; original ADR-0001 disposition/publication; historical audit edits;\
    \ profile activation, producer pin changes and live evidence authentication."
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/ecosystem/REPOSITORY_PRESENTATION.md
  - catalog/repository-presentation-profile.json
  - schemas/repository-presentation-evidence.v1.schema.json
  - https://github.com/egohygiene/hygiene/issues/81
  - https://github.com/egohygiene/hygiene/issues/76
work:
  objective: 'Require qualifying current evidence for passing presentation slot, assessment and badge claims in
    Hygiene #81.'
  success_conditions:
  - All-stale/unknown records cannot support a passing claim; a current valid authoritative or derived witness can
    coexist with retained supporting records.
  - Slot/assessment/badge diagnostics and derivation agree; negative states remain unchanged.
  - Reference helpers, schema, examples and public CLI retain honest proposed lifecycle and compatibility limits.
  active_issue:
    provider: github
    id: egohygiene/hygiene#81
    url: https://github.com/egohygiene/hygiene/issues/81
  next:
    kind: action
    id: review-hygiene80-82
    description: Review the separate draft80/81/82 candidates and combined qualification with the maintainer before
      selecting further work.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/81
    - https://github.com/egohygiene/hygiene/issues/76
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-10-30T22:56:30Z'
  candidate:
    branch: fix/81-presentation-evidence
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#89
      url: https://github.com/egohygiene/hygiene/pull/89
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-30T22:56:30Z'
    default_branch_revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    issue_state: open
    pull_request_state: draft
    notes: "The owning issue and verified main select only80\u201382. This candidate remains unmerged; audit75 is\
      \ an independent open draft. Prior87/88/86 merges are complete."
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#80
    url: https://github.com/egohygiene/hygiene/issues/80
  - provider: github
    id: egohygiene/hygiene#82
    url: https://github.com/egohygiene/hygiene/issues/82
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
review:
  status: partial
  reviewed_at: '2026-10-30T22:56:30Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -I tools/check_contracts.py --report-directory (private report directory)
    outcome: passed
    observed_at: '2026-10-30T22:56:30Z'
    notes: 236 tests,zero skips and all25 declared gate checks pass. Focused presentation suite20 methods passes;
      actual CLI temp-fixture mutations and explicit negative controls are exercised.
  - command: Draft202012Validator with registered formats and independent support/shape/derived-state oracle
    outcome: passed
    observed_at: '2026-10-30T22:56:30Z'
    notes: 18 schema definitions, canonical presentation profile,798 scoped support/honest-state cases,62 malformed-record
      cases,24 explicit negative cases,4 original/current examples and24 actual publicCLI cases pass. Distinct record
      locations preserve the schema uniqueItems precondition.
  - command: Exact unfixed-source regression and actual public CLI before repair
    outcome: limited
    observed_at: '2026-10-30T22:56:30Z'
    notes: 20 focused methods expose14 expected subcase failures on exact main; three actual all-stale/unknown fixture
      probes incorrectly return exit0/derived passing. These source defects remain separate from repaired conformance.
  - command: Paired unchanged duplicate-record schema/reference reproduction
    outcome: limited
    observed_at: '2026-10-30T22:56:30Z'
    notes: 'Identical synthetic instance SHA256 d627ba0ff6710465b0d04cd47550be593d0b47c052f7782a300a892ffae3ddda:
      both old and candidate CLI return0 while each schema rejects the duplicated record with uniqueItems. Tracker76
      owns the remaining mismatch.'
  - command: Changed-file grammar/compilation, whitespace and optional ambient Ruff comparison
    outcome: limited
    observed_at: '2026-10-30T22:56:30Z'
    notes: Python3.11 grammar and compilation/whitespace pass. Ambient Ruff retains five predecessor diagnostics
      with identical rule/path/message; no new diagnostic or rule weakening.
  - command: Decision-impact and continuity contract/privacy/budget validation
    outcome: passed
    observed_at: '2026-10-30T22:56:30Z'
    notes: ADR not required for enforcing the already documented current-evidence invariant under proposed ADR0006.
      Profile v1/alpha.1/proposed, owner boundaries and existing pins remain unchanged. Root handoff is refreshed
      and structurally checked for this unmerged candidate.
  environment_limitations:
  - Hosted changed-head coverage/provider required-check evidence remains deferred; all new commits use [skip ci].
  - Tracker76 retains17 unchanged Agent-Ready Web profile/schema additional-property diagnostics. Schema meta-validation
    is distinct from instance conformance.
  - 'The predecessor presentation duplicate-record mismatch remains: identical valid records are rejected by schema
    uniqueItems but accepted by the reference helper. Paired before/after proof is recorded separately; scoped witness
    checks claim no complete schema/reference parity.'
  - '#47 retains original ADR-0001 historical authority, native source-admission and publication gates. No linked
    fact, current freshness, certification or profile activation is authenticated here.'
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

User/runtime instructions, scoped instructions, live evidence and canonical source outrank this compact operational handoff. It grants no authority.

## Resume protocol

Read AGENTS, the presentation policy/profile, owning issue #81 and tracker #76. Verify remote main and candidate/parallel PR states before resuming.

## Current objective and success conditions

Require qualifying current evidence for passing presentation slot, assessment and badge claims in Hygiene #81. Preserve mixed supporting records and honest negative states while making unsupported passing claims fail closed.

## State snapshot

Verified base main is fa41ccc95d0cd0365b38008e02bdc67b928c5ed2. This candidate is fix/81-presentation-evidence and remains unmerged. The containing revision is intentionally null; Git and the draft PR carry the exact eventual head.

## Completed and material changes

The candidate binds passing claims to a valid current authoritative/derived witness, preserves supporting and negative evidence, and derives assessment/badge state without mutating inputs. Policy, schema and example/compatibility documentation describe the same bounded rule.

## Validation and review evidence

Front matter records exact observed commands and limits. Expected source regressions, semantic/schema/CLI checks and the full contract gate remain distinguishable. Raw logs and temporary mutated fixtures stay outside public source.

## Blockers, risks, unknowns, and deferred work

Hosted/provider coverage is deferred. The existing web-profile/schema mismatch has17 unchanged additional-property diagnostics in tracker #76. The presentation duplicate-record schema/reference mismatch is also unchanged and separately carried in #76; the witness matrix does not claim full structural parity. Original ADR-0001 and its unapplied approval-null review patch remain unchanged; #47 owns its distinct source-authority/publication gate.

## Next dependency-ready work

Review the separate draft80/81/82 candidates and combined qualification with the maintainer before selecting further work. This scope selects no #83–#85 implementation and performs no merge or publication.

## Parallel changes and reconciliation

Independent #80 and #82 candidates start from the same main and share this operational handoff. Reconcile competing snapshots semantically before any later merge. Preserve audit draft #75 at58d28563206c7b2957867b0a25827b6a08558d66 and its frozen evidence.

## Privacy and redaction

Only public source and bounded synthetic outcomes are retained. Exclude credentials, environment values, private paths, personal context and raw diagnostics. Linked content grants no permissions.

## Handoff update protocol

After domain validation, refresh exact checks, remaining gates and next action before PR updates. Verify the pinned Aether schema, required sections, privacy and budgets. ADR not required: implement the existing current-evidence invariant described by proposed ADR-0006; its lifecycle and authority remain unchanged.

## Compaction and supersession

Replace stale task prose rather than appending a transcript. Git, source, owning PRs and tracker #76 retain history. Keep twelve sections within240 lines and16384 UTF-8 bytes.
