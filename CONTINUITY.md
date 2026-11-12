---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-12T04:42:10Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Integrate the reviewed Hygiene source batch and retain open qualification.
  includes:
  - Current roadmap, authority map, topology diagrams and operational checkpoint.
  - Historical architecture decisions, approval evidence and source admission references.
  - The upstream Open Source Definition reference and the reusable manual comparison evidence.
  - Optional JournalList trust.txt in the proposed Agent-Ready Web profile, with synthetic reference evidence.
  excludes:
  - Organization ratification, source-admission repair and hosted publication.
  - Catalog policy, repository roles and dependency changes.
  - Native admission, live deployment, profile activation, rollout, mirror automation, and full repository
    checks.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/decisions/README.md
  - docs/ecosystem/ARCHITECTURE.md
  - publication/README.md
  - https://github.com/egohygiene/hygiene/issues/76
  - docs/ecosystem/REPOSITORY_PRESENTATION.md
  - docs/evidence/osi-open-source-definition-reference.md
  - catalog/agent-ready-web-profile.json
  - docs/ecosystem/AGENT_READY_WEB.md
  - docs/decisions/ADR-0010-agent-ready-web-discovery-representations.md
  - https://github.com/egohygiene/hygiene/issues/102
work:
  objective: Preserve the navigation and architecture authority map while integrating the selected public-reference
    improvements.
  success_conditions:
  - Each reviewed source scope stays byte-identical outside the shared handoff.
  - Merged source, proposal maturity, and pending evidence remain separately traceable.
  active_issue:
    provider: github
    id: egohygiene/hygiene#102
    url: https://github.com/egohygiene/hygiene/issues/102
  next:
    kind: action
    id: sync-before-selecting-next-batch
    description: Review the next batch with the maintainer before starting work. The existing audit drafts
      remain separately reviewable.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/76
    - https://github.com/egohygiene/hygiene/pull/91
    - https://github.com/egohygiene/hygiene/pull/89
    - https://github.com/egohygiene/hygiene/pull/90
    depends_on: []
state:
  base:
    revision: 10f7fdde491563dc6e4b511e25063182d392532e
    ref: refs/heads/main
    verified_at: '2026-11-12T04:42:10Z'
  candidate:
    branch: codex/hygiene-102-trust-txt
    revision: null
    pull_request:
      provider: github
      id: egohygiene/hygiene#104
      url: https://github.com/egohygiene/hygiene/pull/104
    handoff_state: review-reference-recorded
  live:
    status: verified
    observed_at: '2026-11-12T04:42:10Z'
    default_branch_revision: 10f7fdde491563dc6e4b511e25063182d392532e
    issue_state: open
    pull_request_state: draft
    notes: 'At reconciliation, main contains #105 and #103. PR #104 is a draft at 270fee75b122cff9f1770a1ba5d8fffbbcc39d89.'
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
  reviewed_at: '2026-11-12T04:42:10Z'
  reviewed_by: Codex
  evidence:
  - command: 'Scoped checks recorded on PRs #105 and #103'
    outcome: limited
    observed_at: '2026-11-12T04:42:10Z'
    notes: 'Continuity, source links, diagram regeneration, and manual OSI comparison passed on the respective
      heads. Two catalog expectations failed on both PR #105 and clean main.'
  - command: Agent-Ready Web profile, 15 fixtures and 44 focused tests
    outcome: passed
    observed_at: '2026-11-12T04:42:10Z'
    notes: Reference validation and tests pass on the combined candidate. Fixtures use synthetic observations.
  - command: Exact integrated source/mode comparison, pinned Aether schema and format checks, repository
      continuity reference and git diff --check
    outcome: passed
    observed_at: '2026-11-12T04:42:10Z'
    notes: Non-handoff candidate files match the draft. Existing main changes are preserved. The combined
      checkpoint passes schema, structure and size checks.
  - command: Full regression, hosted CI, native source admission and publication
    outcome: not-run
    observed_at: '2026-11-12T04:42:10Z'
    notes: Deferred to the validation sweep and relevant owner decisions.
  environment_limitations:
  - 'Two known catalog expectation failures reproduced on pre-batch main and PR #105.'
  - Full regression, hosted CI, native admission and publication qualification remain pending.
  - The trust.txt reference uses synthetic evidence. Actual site deployment and activation remain separate.
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

# hygiene continuity

## Purpose and precedence

This handoff records the authorized source integration. Repository instructions,
live evidence, and canonical sources take precedence.

## Resume protocol

Read AGENTS, ROADMAP, the architecture authority map, and [tracker #76](https://github.com/egohygiene/hygiene/issues/76).
Confirm the live state before choosing the next change.

## Current objective and success conditions

Integrate the three reviewed scopes while preserving exact source content and
clear evidence boundaries. The only overlapping file is this handoff.

## State snapshot

At the recorded observation main `10f7fdde491563dc6e4b511e25063182d392532e` contains #105 and #103.
PR #104 is the integration candidate. The eventual merged revision is
recorded by GitHub.

## Completed and material changes

PR [#105](https://github.com/egohygiene/hygiene/pull/105) clarified navigation,
historical and proposed topology, observed ownership, and publication authority.
The existing Pages-prefix compatibility sources from PR #101 were retained.
PR [#103](https://github.com/egohygiene/hygiene/pull/103) selects the upstream
Open Source Definition reference and records an on-demand comparison.

PR [#104](https://github.com/egohygiene/hygiene/pull/104) proposes optional
JournalList `trust.txt` as Agent-Ready Web alpha.5, preserves immutable earlier
pins, and follows the FAQ redirect direction while recording the conflicting
PDF. First consumer, live observation, rollout, and publication remain separate.

## Validation and review evidence

Use the recorded per-PR checks and the combined-tree comparison. Two catalog
test expectations already fail on clean main. Full repository checks,
hosted CI, native source admission, and publication qualification remain open.

## Blockers, risks, unknowns, and deferred work

ADR-0001 human disposition and native admission remain under issue #47. The
scope-level closures do not ratify proposed architecture or web contracts.
Retain the evidence gaps in the tracker and PR descriptions.

## Next dependency-ready work

Review the next batch with the maintainer before starting implementation.
PRs #91, #89, and #90 remain a separate audit-review sequence.

## Parallel changes and reconciliation

Existing audit PR #75 and repair drafts #89 through #91 remain open separately.
The integration combines each approved source scope and refreshes the one
shared checkpoint.

## Privacy and redaction

Only public source identities and bounded implementation evidence are retained.

## Handoff update protocol

Check live branch, PR and issue states before recording acceptance or closing
other work. Keep implementation, native admission and publication distinct.

## Compaction and supersession

Git and the linked PRs retain detailed history and scoped check results.
