---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: "2026-09-14T14:11:20Z"
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Preserve the bounded review handoff for Hygiene issue 52 and the proposed Agent-Ready Web guarded capability and commerce foundation.
  includes:
    - issue 52 capability identity, contracts, authority, human control, execution evidence, expiry, revocation, replay, rate-limit, and failure policy
    - descriptive Product and Offer metadata, truthful ads.txt and app-ads.txt applicability, and the Store-owned action boundary
    - compatibility with merged checkpoints 50 and 51 plus the blocked checkpoint 4 handoff
  excludes:
    - conversation transcripts
    - duplicated architecture, roadmap, and changelog content
    - application-specific browser tools and Store-owned transaction-domain contracts
    - checkpoint 53 integration, generators, workflows, rollout, publication, dashboards, releases, and adoption claims
  precedence:
    - user-and-runtime-instructions
    - scoped-repository-instructions
    - live-repository-and-work-tracker-state
    - canonical-repository-sources
    - continuity-checkpoint
  canonical_sources:
    - AGENTS.md
    - docs/ecosystem/ARCHITECTURE.md
    - docs/ecosystem/AGENT_CONTEXT.md
    - docs/ecosystem/DEPENDENCY_BOUNDARIES.md
    - docs/decisions/ADR-009-agent-ready-web-profile-foundation.md
    - docs/decisions/ADR-010-agent-ready-web-discovery-representations.md
    - docs/decisions/ADR-011-agent-ready-web-guarded-capability-commerce.md
    - docs/ecosystem/AGENT_READY_WEB.md
    - catalog/agent-ready-web-profile.json
    - schemas/agent-ready-web-profile.v1.schema.json
    - catalog/contracts.yaml
    - catalog/dependency-boundaries.yaml
    - ROADMAP.md
    - https://github.com/egohygiene/hygiene/issues/52
    - https://github.com/egohygiene/hygiene/issues/16
work:
  objective: Implement checkpoint 3 as one proposed guarded browser-capability and descriptive-commerce policy foundation without beginning integration or downstream work.
  success_conditions:
    - Keep WebMCP and MCP-B experimental and optional while requiring versioned origin-bound contracts and fail-closed safeguards whenever present.
    - Separate read-only from state-changing tools and enforce permission, consent, confirmation, security, audit, provenance, revocation, expiry, replay, rate-limit, and recovery policy.
    - Keep Product and Offer metadata non-executable, require truthful advertising relationships when applicable, and preserve Store ownership of action contracts.
    - Preserve checkpoint 1 and 2 compatibility and keep schema, fixtures, docs, indexes, roadmap, decision, tests, and generated views consistent.
    - Pass focused checks, the complete README validation sequence, continuity verification, and git diff checks before opening one unmerged PR that closes only issue 52.
  active_issue:
    provider: github
    id: egohygiene/hygiene#52
    url: https://github.com/egohygiene/hygiene/issues/52
  next:
    kind: issue
    id: egohygiene/hygiene#53
    description: Integrate and validate the complete profile only after checkpoint 3 is reviewed and merged.
    readiness: blocked
    references:
      - https://github.com/egohygiene/hygiene/issues/53
    depends_on:
      - egohygiene/hygiene#52
state:
  base:
    revision: c7c603023c444142bed82af14af23b5898ef568e
    ref: refs/heads/main
    verified_at: "2026-09-14T14:10:00Z"
  candidate:
    branch: codex/hygiene-16-guarded-capability-commerce
    revision: c7c603023c444142bed82af14af23b5898ef568e
    pull_request: null
    handoff_state: implementation-validated
  live:
    status: verified
    observed_at: "2026-09-14T14:10:00Z"
    default_branch_revision: c7c603023c444142bed82af14af23b5898ef568e
    issue_state: open
    pull_request_state: absent
    notes: Main is checkpoint-2 PR 55's merge; issue 52 is dependency-ready with no comments, issue 16 remains open, issue 53 remains blocked, no pull request is open, this remote branch does not yet exist, and no workflow run exists for main. The parent checklist still shows earlier children unchecked despite their closed issue state.
  parallel_changes: []
review:
  status: passed
  reviewed_at: "2026-09-14T14:11:20Z"
  reviewed_by: Codex
  evidence:
    - command: python3 tools/agent_ready_web.py validate-profile && python3 tools/agent_ready_web.py validate-fixtures && python3 -m unittest tests.test_agent_ready_web
      outcome: passed
      observed_at: "2026-09-14T14:05:00Z"
      notes: The proposed alpha.3 profile, all 10 expectation-aware fixtures, and all 28 focused tests passed.
    - command: python3 tools/boundaries.py render --output docs/generated/DEPENDENCY_BOUNDARIES.md && python3 tools/boundaries.py validate && python3 tools/boundaries.py check-generated --output docs/generated/DEPENDENCY_BOUNDARIES.md
      outcome: passed
      observed_at: "2026-09-14T14:01:00Z"
      notes: The 26-relationship register validated and its generated view is exact.
    - command: README.md repository validation sequence
      outcome: passed
      observed_at: "2026-09-14T14:09:00Z"
      notes: Catalog, generated views, context, continuity, Agent-Ready Web, boundaries, Repository Intelligence, presentation, ADR fixtures, and all 123 unit tests passed.
    - command: git diff --check
      outcome: passed
      observed_at: "2026-09-14T14:09:00Z"
      notes: No whitespace errors were reported before this continuity refresh.
    - command: GitHub main, issue, comments, predecessor, parent, successor, branch, open-PR, and workflow inspection
      outcome: passed
      observed_at: "2026-09-14T14:10:00Z"
      notes: Live main is PR 55's merge, issue 51 is closed, issue 52 is open with no comments, issue 16 is open, issue 53 is blocked, no PR competes, the remote candidate is absent, and main has no workflow run.
  environment_limitations:
    - Hygiene exposes only a manually dispatched release-policy workflow; no automatic pull-request CI exists to run before a pull request is opened.
    - The host does not expose Aether's maintain-repository-continuity skill as an installed skill, so its checked-in pointer and required local policy were applied manually with the repository validator.
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

This checkpoint hands off issue #52's proposed guarded capability and
descriptive-commerce foundation. It is subordinate to user and repository
instructions, live GitHub evidence, and the canonical sources above. It does
not replace issue #16's order or authorize checkpoint #53.

## Resume protocol

Read `AGENTS.md` and the canonical sources above, then recheck `main`, issue
#52 and its comments, this branch and pull request, parent #16, predecessor
#51, successor #53, open pull requests, and current CI. Surface stale or
contradictory evidence and do not begin checkpoint #53 before this candidate
is reviewed and merged.

## Current objective and success conditions

The candidate advances the proposed profile to `1.0.0-alpha.3`. Success means
browser capabilities are structurally independent, origin-bound, versioned,
explicitly authorized, human-controlled, auditable, revocable, replay-safe,
rate-limited, and fail closed; commerce metadata remains descriptive;
advertising claims remain truthful; Store retains action contracts; canonical
surfaces agree; and one unmerged PR closes only issue #52.

## State snapshot

- Base: `c7c603023c444142bed82af14af23b5898ef568e` on live `main`, the
  verified merge commit of checkpoint-2 PR #55.
- Candidate: local validated work on
  `codex/hygiene-16-guarded-capability-commerce`; the recorded revision is its
  pre-commit base and must be replaced after branch publication.
- Review: no PR exists yet; issue #52 and parent #16 remain open, issue #53 is
  blocked, and no automatic pull-request CI is configured.

## Completed and material changes

- The proposed profile adds exact capability and commerce policy objects plus
  five bounded mechanism records without redefining earlier catalog entries.
- WebMCP and MCP-B are optional experiments that require exact protocol and
  implementation pins, versioned I/O schemas, read/state classification,
  explicit permission and consent, fresh confirmation, security controls,
  execution evidence, revocation, expiry, replay protection, rate limits, and
  deterministic failure behavior when present.
- Product and Offer JSON-LD is descriptive only; ads.txt and app-ads.txt use
  real relationship evidence or safe absence; Store owns transaction domains.
- Schema bindings, compatibility fixtures, the reference checker, focused
  tests, ADR-011, architecture, dependency/contract indexes, roadmap, human
  guide, generated boundary view, and README surfaces agree.
- No browser tool, commerce transaction, Store contract, generator, workflow,
  rollout, publication, dashboard, release, or adoption was implemented.

## Validation and review evidence

Focused checks, all 10 fixtures, the complete README sequence with 123 tests,
the regenerated boundary check, and `git diff --check` passed. The refreshed
continuity document still requires its final repository and size validation.

## Blockers, risks, unknowns, and deferred work

- Blockers: none observed for committing and opening the focused review.
- Risks: protocol revisions and all lifecycle choices remain proposed; every
  consumer must pin exactly and cannot infer adoption or executable authority.
- Unknowns: no automatic pull-request CI exists, so local checks are the only
  current executable evidence.
- Deferred: issue #53 and every application capability, Store domain contract,
  Holon, Relay, Pace, Observatory, or site implementation.

## Next dependency-ready work

[Issue #53](https://github.com/egohygiene/hygiene/issues/53) remains blocked by
the reviewed merge of issue #52. A future checkpoint must branch from that new
live `main`; this branch must not begin integration.

## Parallel changes and reconciliation

No competing pull request or remote candidate branch was observed. This work
began directly from the verified PR #55 merge commit and carries no unmerged
sibling history.

## Privacy and redaction

This public checkpoint contains only public repository state, public standards
references, and synthetic fixture data. It excludes secrets, private
conversations, personal data, local paths, and unpublished private business
information.

## Handoff update protocol

Before presenting or updating the pull request, recheck mutable GitHub state,
replace stale candidate details, record exact checks and limitations, and keep
this checkpoint in the same bounded change. Never predict a merge or treat
generated text as maintainer authority.

## Compaction and supersession

Keep this file below 16,384 UTF-8 bytes and 240 lines. Replace stale snapshot
prose rather than accumulating chronology. Git and GitHub retain history; mark
this checkpoint stale or superseded only with the required reason or pointer.
