---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/hygiene
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: "2026-09-22T00:04:51Z"
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Preserve the bounded maintainer-review handoff for Hygiene issue 25 and the proposed canonical public-site surface and route registry.
  includes:
    - 36 canonical public-site surfaces with organization and repository route profiles, base-path resolution, and redirect-only aliases
    - separate requirement, applicability, implementation, publication, visibility, freshness, assertion, disposition, ownership, provenance, and evidence semantics
    - route-profile-specific publication prerequisites, immutable registry and renderer pins, privacy-safe redaction, and subject-versus-publication authority
    - strict schemas, a dependency-free semantic validator, three complete synthetic site declarations, architecture integration, and consumer handoffs
  excludes:
    - conversation transcripts
    - duplicated registry, architecture, roadmap, or policy text
    - live site facts, private topology, credentials, or real conformance claims
    - redirects, rendering, hosting, deployment, monitoring, legal review, incident semantics, or downstream consumer implementations
    - acceptance, merge, release, lifecycle promotion, adoption, or publication
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
    - docs/ecosystem/PUBLIC_SITE_SURFACES.md
    - docs/decisions/ADR-013-public-site-surface-route-registry.md
    - catalog/public-site-surface-registry.json
    - schemas/public-site-surface-registry.v1.schema.json
    - schemas/public-site-surface-declaration.v1.schema.json
    - catalog/contracts.yaml
    - catalog/dependency-boundaries.yaml
    - docs/generated/DEPENDENCY_BOUNDARIES.md
    - ROADMAP.md
    - README.md
    - https://github.com/egohygiene/hygiene/issues/25
    - https://github.com/egohygiene/hygiene/issues/17
    - https://github.com/egohygiene/hygiene/pull/63
    - https://github.com/egohygiene/.github/issues/30
work:
  objective: Present one proposed, consumer-reviewable registry and declaration contract without implementing or claiming downstream publication.
  success_conditions:
    - Provide a strict machine-readable registry and schemas plus one human-readable specification.
    - Give every surface a stable ID, profile-specific canonical route and aliases, applicability, owner, source, renderer, dependencies, and truthful delivery evidence.
    - Keep missing, stale, blocked, private, unknown, withdrawn, and not-applicable states distinct and fail closed on contradictions.
    - Make aliases redirect-only and prevent duplicate canonical content.
    - Let product repositories declare complete state without copying renderer implementations.
    - Compose explicitly with Agent-Ready Web, public-site policy, Repository Intelligence, presentation, Identity, Renderflow, and System Status boundaries.
    - Validate small-content, documentation-heavy, and organization-hybrid synthetic declarations and document Holon, Relay, Observatory, and Pace handoffs.
    - Pass focused checks, the exact README suite, schema/runtime parity tests, malformed-input mutation, generated-view, boundary, continuity, size, and diff checks.
    - Leave one unmerged pull request that closes issue 25 only when maintainers merge it.
  active_issue:
    provider: github
    id: egohygiene/hygiene#25
    url: https://github.com/egohygiene/hygiene/issues/25
  next:
    kind: pull-request-review
    id: egohygiene/hygiene#63
    description: Maintainers review the proposed registry contract; do not merge, promote, publish, deploy, or begin consumer adoption from this handoff.
    readiness: ready-for-review
    references:
      - https://github.com/egohygiene/hygiene/pull/63
    depends_on:
      - egohygiene/hygiene#25
state:
  base:
    revision: c589587395750cd1c79c6fa0bef010189c547249
    ref: refs/heads/main
    verified_at: "2026-09-22T00:01:20Z"
  candidate:
    branch: codex/hygiene-25-public-site-surface-registry
    revision: af413e07033929b5da7dc8477ce1ea2267aff367
    revision_role: validated-remote-implementation-snapshot
    pull_request: https://github.com/egohygiene/hygiene/pull/63
    handoff_state: review-open
    finalization: A continuity-and-ADR-link-only commit follows this exact implementation snapshot; the GitHub pull-request head is authoritative for final review.
  live:
    status: verified
    observed_at: "2026-09-22T00:01:20Z"
    default_branch_revision: c589587395750cd1c79c6fa0bef010189c547249
    issue_state: open
    pull_request_state: open
    notes: Pull request 63 targets the exact verified main revision and is the sole issue-25 implementation review. The issue has no comments. The contract remains proposed and unmerged.
  parallel_changes: []
review:
  status: passed
  reviewed_at: "2026-09-22T00:04:51Z"
  reviewed_by: Codex
  evidence:
    - command: python3 tools/site_surfaces.py validate-registry && python3 tools/site_surfaces.py validate-fixtures && python3 -m unittest -v tests.test_site_surfaces
      outcome: passed
      observed_at: "2026-09-22T00:00:00Z"
      notes: The proposed alpha.1 registry has 36 surfaces, all three complete declarations validate, and all 43 focused tests pass.
    - command: README.md exact complete repository validation sequence
      outcome: passed
      observed_at: "2026-09-22T00:00:00Z"
      notes: Catalog, generated views, context, continuity, Agent-Ready Web, boundaries and scan, Repository Intelligence, presentation, public-site surfaces, ADR fixtures, and all 176 unit tests passed.
    - command: python3 tools/boundaries.py validate && python3 tools/boundaries.py check-generated --output docs/generated/DEPENDENCY_BOUNDARIES.md && python3 tools/boundaries.py scan --repository-root . --repository egohygiene/hygiene
      outcome: passed
      observed_at: "2026-09-22T00:00:00Z"
      notes: The 27-relationship register, exact generated view, and local dependency scan passed.
    - command: recursive malformed-input mutation sweep over registry and declaration values
      outcome: passed
      observed_at: "2026-09-22T00:00:00Z"
      notes: Replacing every nested value with object, array, null, and number shapes caused zero validator crashes.
    - command: independent adversarial contract, schema, validator, and documentation review
      outcome: passed
      observed_at: "2026-09-22T00:00:00Z"
      notes: Profile-specific dependency, ownership, public-site-policy composition, impacted-consumer, boolean, synthetic-ID, and URL parity findings were resolved and re-reviewed clear.
    - command: GitHub atomic tree publication and focused pull-request creation
      outcome: passed
      observed_at: "2026-09-22T00:01:20Z"
      notes: Remote tree 76fd430b0076aa46d888dcd277f1bb507ed6c459 exactly matched the validated local implementation tree; revision af413e07033929b5da7dc8477ce1ea2267aff367 opened pull request 63 against the exact base.
    - command: python3 tools/continuity.py validate-profile && python3 tools/continuity.py validate-repository --repository . && fixed byte and line limits && git diff --check
      outcome: passed
      observed_at: "2026-09-22T00:04:51Z"
      notes: The final checkpoint remains below 16384 bytes and 240 lines with no whitespace errors.
  environment_limitations:
    - Hygiene exposes only a manually dispatched release-policy workflow; no automatic pull-request CI run or commit status is assumed.
    - The host does not expose Aether's maintain-repository-continuity skill, so the checked-in pointer and local policy were applied manually and verified with repository tooling.
    - The checkout has no writable HTTPS Git credential; the GitHub connector created an atomic commit from the exact validated tree and updated only the issue branch.
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

This checkpoint hands off issue #25's proposed canonical public-site surface
and route registry. It is subordinate to instructions, live GitHub state, and
the canonical sources above. It cannot grant lifecycle, publication, or
downstream implementation authority.

## Current objective and success conditions

Present one unmerged review PR with stable surface identities, profile-specific
routes and prerequisites, complete declaration semantics, strict schemas,
synthetic reference declarations, architecture integration, and every
validation green. Success does not include merge, release, live redirects,
deployment, adoption, or conformance.

## State snapshot

- Base: `c589587395750cd1c79c6fa0bef010189c547249` on verified live `main`.
- Remote implementation: `af413e07033929b5da7dc8477ce1ea2267aff367`
  on `codex/hygiene-25-public-site-surface-registry`.
- Review: [PR #63](https://github.com/egohygiene/hygiene/pull/63) is open and
  unmerged; issue #25 remains open until review and merge.
- Contract: `1.0.0-alpha.1`, 36 surfaces, lifecycle `proposed`.

## Material result

The candidate defines one canonical registry, two route profiles, strict
declarations, profile-specific publication prerequisites, immutable provenance
and renderer pins, privacy-safe state, separate subject and publisher
authority, and explicit neighboring-contract boundaries. Three complete
synthetic site classes validate the model. No live site or downstream
implementation is claimed.

## Validation and limitations

Focused validation, all fixtures, the exact README sequence with 176 tests,
generated views, continuity and size checks, the boundary scan, independent
adversarial review, a zero-crash mutation sweep, and `git diff --check` passed.
The repository has no automatic pull-request CI evidence. The unavailable
Aether skill and connector-based publication are recorded above.

## Next dependency-ready work

After maintainers review and merge this proposal, Relay can consume an eligible
immutable pin for reusable validation, rendering, redirects, and publication
workflows. Holon, Observatory, and Pace retain their documented scaffold,
aggregation, and adoption boundaries. The immediate safe action is review of
PR #63; do not merge, publish, deploy, or start consumer work from this
checkpoint.

## Handoff update protocol

Before any PR update, recheck `main`, issue #25 and comments, PR #63, the
branch head, competing PRs, and CI. Re-run affected and complete validation,
record the exact remote head when a continuity-only commit follows the
implementation snapshot, and never predict merge, release, or adoption.

## Compaction and supersession

Keep this file below 16,384 UTF-8 bytes and 240 lines. Replace stale snapshot
prose instead of accumulating chronology. Git and GitHub retain history.
