---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-03T04:31:47Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Reject malformed or ambiguous Agent-Ready Web provenance URLs using shared HTTPS syntax with
    public-site surfaces.
  includes: &id001
  - Parse complete HTTPS authorities and reject userinfo, raw whitespace/control/backslash ambiguity,
    malformed hosts and invalid/empty ports.
  - Preserve safe relative evidence, supported HTTPS/IPv6 and field-only diagnostics across profile, mechanism
    and conformance locations.
  - Document exact-origin syntax and leave proposed lifecycle, live conformance and authorization boundaries
    unchanged.
  excludes:
  - Network fetches, live-site certification, capability execution, publication and downstream rollout.
  - Test suites, hosted CI, merging, issue closure and unrelated audit repairs.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - tools/https_locations.py
  - tools/agent_ready_web.py
  - tools/site_surfaces.py
  - tests/test_agent_ready_web.py
  - docs/ecosystem/AGENT_READY_WEB.md
  - docs/ecosystem/PUBLIC_SITE_SURFACES.md
  - docs/decisions/POLICY.md
  - https://github.com/egohygiene/hygiene/issues/83
work:
  objective: Reject malformed or ambiguous Agent-Ready Web provenance URLs using shared HTTPS syntax with
    public-site surfaces.
  success_conditions: *id001
  active_issue:
    provider: github
    id: egohygiene/hygiene#83
    url: https://github.com/egohygiene/hygiene/issues/83
  next:
    kind: action
    id: review-draft-and-qualify
    description: Review the shared syntax/compatibility diff and execute the issue83 helper/CLI and neighboring
      surface regression checks in the deferred qualification pass before closure.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/83
    depends_on: []
state:
  base:
    revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    ref: refs/heads/main
    verified_at: '2026-11-03T04:31:47Z'
  candidate:
    branch: codex/83-safe-agent-web-urls
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-03T04:31:47Z'
    default_branch_revision: fa41ccc95d0cd0365b38008e02bdc67b928c5ed2
    issue_state: open
    pull_request_state: not-applicable
    notes: Main fa41ccc is current and issue83 is open. PR86 is already merged; stale predecessor handoff
      instructions are replaced by this bounded candidate. Existing drafts75/89/90/91 remain open and
      untouched. This candidate is not merged, certified or published.
  parallel_changes:
  - provider: github
    id: egohygiene/hygiene#75
    url: https://github.com/egohygiene/hygiene/pull/75
  - provider: github
    id: egohygiene/hygiene#89
    url: https://github.com/egohygiene/hygiene/pull/89
  - provider: github
    id: egohygiene/hygiene#90
    url: https://github.com/egohygiene/hygiene/pull/90
  - provider: github
    id: egohygiene/hygiene#91
    url: https://github.com/egohygiene/hygiene/pull/91
review:
  status: partial
  reviewed_at: '2026-11-03T04:31:47Z'
  reviewed_by: Codex
  evidence:
  - command: Python ast.parse on tools/https_locations.py, tools/agent_ready_web.py, tools/site_surfaces.py
      and tests/test_agent_ready_web.py
    outcome: passed
    observed_at: '2026-11-03T04:31:47Z'
    notes: All four modified/new Python sources parse. Public script and package import branches retain
      local module routing. This is syntax evidence only.
  - command: Local documentation targets and git diff --check
    outcome: passed
    observed_at: '2026-11-03T04:31:47Z'
    notes: Relative targets resolve and whitespace check passes. Profile/schema/catalog/ADR/workflow bytes
      remain unchanged.
  - command: Pinned Aether continuity metadata/schema, twelve headings, privacy and size inspection
    outcome: passed
    observed_at: '2026-11-03T04:31:47Z'
    notes: Within 16384 bytes/240 lines; no private context or local paths.
  - command: Issue83 helper/CLI regressions, public validators, neighboring site-surface suite and hosted
      CI
    outcome: not-run
    observed_at: '2026-11-03T04:31:47Z'
    notes: Four regression methods are authored but unexecuted. No behavior or conformance pass is claimed.
  environment_limitations:
  - Runtime/helper/public-CLI behavior is unqualified until the authored regressions and existing suites
    execute.
  - Official released EgoLint continuity conformance is unexecuted; metadata/schema checks are narrower.
  - The shared module must accompany either checker from the same reviewed revision; no downstream rollout
    is performed.
  - Tracker76 retains independent schema consistency, audit and approval work; all proposed ADRs retain
    their status.
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

This is a bounded issue83 operational handoff. User/runtime and scoped instructions, live evidence and canonical contracts outrank the checkpoint.

## Resume protocol

Read AGENTS, the Agent-Ready Web evidence envelope, tools/https_locations.py and issue83. Verify main and peer PR state. PR86 is already merged, so do not repeat its old merge plan.

## Current objective and success conditions

Use one complete HTTPS syntax parser for both reference checkers while preserving safe relative evidence and field-only diagnostics. No network access or policy activation is added.

## State snapshot

Base main fa41ccc95d0cd0365b38008e02bdc67b928c5ed2 and open issue83 are freshly observed. Candidate branch codex/83-safe-agent-web-urls has null self-revision/PR before creation.

## Completed and material changes

tools/https_locations.py owns the shared local syntax implementation. Agent-Ready Web location/origin checks delegate to it; public-site private helper aliases preserve callers. Documentation defines ports, bracketed unscoped IPv6 and exact-origin delimiters. Four regression methods cover shared semantics and real CLI paths; they have not run.

## Validation and review evidence

All four Python sources pass AST parsing. Local documentation targets and git diff --check pass. Continuity metadata/schema, twelve-section and privacy/size checks pass. These results establish syntax/structure, not behavior.

## Blockers, risks, unknowns, and deferred work

No regression suite, public validator command or hosted CI was executed. The draft is unqualified for behavior until issue83 acceptance runs. Existing tracker76 schema consistency and approval gaps remain; the proposed Agent-Ready Web/site-surface ADR lifecycles are unchanged.

## Next dependency-ready work

Review the source/compatibility draft and run issue83 helper/CLI plus neighboring site-surface checks during qualification. Keep the issue open until actual acceptance evidence exists.

## Parallel changes and reconciliation

Existing drafts75/89/90/91 are preserved. Only root CONTINUITY overlaps those working handoffs; reconcile the final current objective/check evidence semantically against main before merging any of them.

## Privacy and redaction

Retain only scoped public repository facts and synthetic URL test inputs. No private sources, user data, credentials or machine-local paths are included.

## Handoff update protocol

Refresh after actual checks/review. ADR not required: repair reference validation under existing contracts without changing ownership or authority. Applied pinned Aether create-decisions-document2.1.0 and maintain-repository-continuity1.1.0; no merge, closure or publication is authorized by this file.

## Compaction and supersession

Keep twelve required sections and byte/line budgets. Git, canonical policy and issue83/tracker76 retain the detailed acceptance/history.
