# Ego Hygiene Visual Roadmap System

**Specification:** v0.1.0  
**Status:** Proposed  
**Snapshot:** 2026-08-24  
**Primary route:** `/roadmap/`

## Outcome

Every Ego Hygiene repository keeps its strategic intent in `ROADMAP.md`. A reusable pipeline validates that roadmap, enriches each stable step with GitHub evidence, renders it as an accessible quest line, and publishes it without creating a second or conflicting Pages deployment.

The organization-level route at `egohygiene.io/roadmap/` aggregates public-safe repository roadmaps. Repositories with an existing site can also compose the same renderer at their own `/roadmap/` route.

## Architectural principles

- `ROADMAP.md` is canonical intent. Generated JSON, HTML, issue plans, and commit lists are projections.
- Stable roadmap step IDs connect intent to issues, pull requests, commits, releases, and validation evidence.
- Completion is based on declared exit criteria and linked evidence, never on commit volume.
- Missing, stale, inaccessible, and private evidence render explicitly as unknown or restricted.
- Rendering and enrichment happen at build time. Public pages never receive a GitHub token.
- Existing consumer sites own their final Pages artifact. The roadmap workflow composes into it instead of competing with it.
- Issue creation is plan-first and human-approved. A roadmap change does not silently create or close GitHub issues.

## Ownership

| Concern | Canonical owner | Responsibility |
| --- | --- | --- |
| Roadmap policy and normalized schema | Hygiene | Stable IDs, states, dependencies, completion semantics, visibility, supersession, and compatibility. |
| AI authoring support | Aether | Skills, prompts, agents, and evaluations that generate or improve compliant roadmaps. |
| Semantic linting | Egolint | Validate structure, IDs, cycles, issue references, state consistency, and canonical/generated separation. |
| Evidence read model | Observatory | Normalize issues, pull requests, commits, releases, checks, staleness, and organization aggregation. |
| Quest-line renderer | Holon | Versioned static-site blueprint, responsive interaction, accessibility, design-token inputs, and composition interface. |
| GitHub workflow orchestration | Relay | Read-only evidence collection, build, validation, artifact publication, and Pages composition. |
| Fleet adoption | Pace | Detect roadmap drift and open bounded reviewable rollout PRs after upstream releases exist. |
| Brand tokens | Identity | Approved colors, typography, motion, iconography, and accessibility constraints. |
| Public organization route | egohygiene.io | First consumer and canonical public `/roadmap/` navigation surface. |
| Repository intent | Each repository | Own the content, priority, acceptance criteria, visibility, and evidence links in its roadmap. |

## Source contract

The existing `aether.architecture-document/v1` front matter remains intact until its extension rules are reconciled. The roadmap-specific metadata is initially embedded in backward-compatible HTML comments.

```markdown
<!-- roadmap-manifest
schema: hygiene.roadmap/v1alpha1
repository: egohygiene/relay
visibility: public
publication: composed
route: /roadmap/
updated: 2026-08-24
-->
```

Each renderable step uses a stable ID and explicit state.

```markdown
<!-- roadmap-step
id: REL-RM-003
status: active
depends_on: [HYG-RM-001, EGO-RM-002]
issues: [5]
-->
### REL-RM-003 - Publish roadmap validation and evidence assembly

**Outcome:** A versioned action converts validated roadmap intent into a public-safe evidence snapshot.

**Exit criteria:**

- [ ] Stable IDs and dependency cycles are validated.
- [ ] Linked issues, pull requests, commits, releases, and checks resolve deterministically.
- [ ] Missing and private evidence remains explicit.
```

### Required normalized fields

| Field | Requirement |
| --- | --- |
| `schema` | Exact versioned contract identifier. |
| `repository` | Canonical `owner/name`. |
| `visibility` | `public`, `internal`, or `private`. |
| `publication` | `canonical`, `composed`, `central`, `artifact-only`, or `disabled`. |
| `route` | Canonical route, normally `/roadmap/`. |
| `id` | Repository-unique, immutable roadmap step ID. |
| `status` | `complete`, `active`, `ready`, `blocked`, `planned`, `deferred`, or `cancelled`. |
| `depends_on` | Zero or more stable step IDs. |
| `issues` | Explicit local or fully-qualified GitHub issue references. |
| `outcome` | One testable capability or state, not a list of tasks. |
| `exit_criteria` | Markdown checklist used as the primary progress denominator. |

### State semantics

| State | Meaning |
| --- | --- |
| `complete` | All required exit criteria are checked and required evidence validates. |
| `active` | Work is in progress and all mandatory dependencies are complete. |
| `ready` | Dependencies are complete and the step has a bounded executable definition. |
| `blocked` | A named dependency, decision, failure, or external constraint prevents progress. |
| `planned` | Accepted work that is not yet dependency-ready. |
| `deferred` | Intentionally outside the current planning horizon. |
| `cancelled` | Preserved historical intent that will not be delivered. |

## Evidence model

Each generated step snapshot can contain:

- directly linked GitHub issues;
- pull requests that close or explicitly reference those issues;
- commits from linked pull requests;
- commits carrying a `Roadmap-Step: <ID>` trailer;
- releases containing linked pull requests or explicit step metadata;
- validation checks and durable artifacts required by exit criteria;
- timestamps, source URLs, source commit SHA, and freshness state.

Commits are evidence, not progress units. A step with many commits and unmet exit criteria remains incomplete.

### Commit and pull-request convention

Pull-request templates should include a structured roadmap field:

```markdown
Roadmap-Step: REL-RM-003
```

Conventional commits may include the same trailer:

```text
feat(roadmap): publish evidence snapshot

Roadmap-Step: REL-RM-003
Refs: #5
```

The pipeline also follows explicit issue and pull-request links already present in `ROADMAP.md`; adoption does not require rewriting historical commits.

## Generated artifacts

The public build produces a deterministic directory:

```text
dist/roadmap/
  index.html
  assets/
  roadmap.manifest.json
  roadmap.evidence.json
  provenance.json
```

- `roadmap.manifest.json` is the normalized roadmap projection.
- `roadmap.evidence.json` contains GitHub evidence permitted by the visibility policy.
- `provenance.json` records input SHAs, tool versions, timestamps, and redaction decisions.

Issue planning is a separate, private workflow artifact:

```text
build/roadmap-private/
  roadmap.issue-plan.json
  roadmap.issue-plan.md
```

The issue plan may contain unpublished acceptance criteria, duplicate candidates, or private references. It must never be copied into a public Pages artifact.

Generated files must never be hand-edited or treated as the canonical roadmap.

## Quest-line experience

### Information architecture

- Repository identity, lifecycle, current gate, overall completion, and freshness.
- A responsive vertical quest line grouped into horizons or phases.
- Completed, active, ready, blocked, planned, and deferred nodes with a text label in addition to color.
- Dependency locks that explain why a step is not ready.
- Expandable step panels containing the outcome, exit criteria, dependencies, issues, pull requests, commits, releases, checks, and source links.
- Deep links such as `/roadmap/#REL-RM-003`.
- Filters for status, horizon, owner, and repository on the organization view.
- A plain Markdown link and no-JavaScript fallback.

### Visual direction

The visual language should feel like a living constellation or quest path rather than a project-management spreadsheet:

- a gently winding path on wide screens and a straight vertical rail on mobile;
- completed nodes in an Identity-approved success color;
- an active node with a subtle energy halo that respects `prefers-reduced-motion`;
- blocked nodes with clear text and icon treatment;
- restrained depth, soft glow, and high-contrast typography;
- repository-specific Identity tokens without changing interaction semantics.

### Accessibility and quality gates

- WCAG 2.2 AA contrast and interaction behavior.
- Complete keyboard navigation and visible focus.
- Screen-reader names for status, progress, dependencies, and evidence links.
- Reduced-motion behavior and no motion-only meaning.
- Mobile layouts validated at narrow widths.
- Static HTML content remains understandable before JavaScript hydrates.
- Broken-link checks, bundle-size budget, Lighthouse/accessibility evidence, and visual regression coverage.

## Build and publication workflow

The consumer workflow calls an immutable Relay release and uses least-privilege permissions.

### Refresh events

- Pushes to the default branch that change `ROADMAP.md` or roadmap configuration.
- For a repository-owned composed site: issue opened, edited, closed, reopened, labeled, or unlabeled through a safe metadata-only job.
- Merged pull requests through the resulting default-branch push.
- Manual workflow dispatch.
- A low-frequency scheduled refresh to repair missed events and refresh staleness.

The central organization site cannot subscribe to every sibling repository's issue events with Actions alone. Until an approved GitHub App or equivalent event bridge exists, its cross-repository refresh is scheduled and manually dispatchable. `repository_dispatch` may be added only with an explicitly governed sender and least-privilege credential.

Open pull-request metadata may be refreshed only through a job that never checks out untrusted pull-request code with elevated permissions.

### Pipeline

1. Check out the default branch.
2. Validate `ROADMAP.md` locally with Egolint against the pinned Hygiene contract.
3. Collect read-only GitHub evidence.
4. Apply visibility and redaction rules.
5. Emit the deterministic Observatory snapshot.
6. Render the Holon quest-line blueprint with pinned Identity tokens.
7. Run unit, accessibility, link, provenance, and size checks.
8. Upload `dist/roadmap/` as a durable artifact.
9. Compose it into the consumer-owned site artifact under a configurable base path; `/roadmap/` is the default and `/roadmap/<repo>/` is used by the central portfolio.
10. Deploy once through the consumer's existing Pages or hosting workflow.

### Composition modes

| Mode | Use |
| --- | --- |
| `canonical` | `egohygiene.io` publishes the organization-level route. |
| `composed` | A repository with an existing site merges `dist/roadmap/` into that site's final artifact. |
| `central` | A public repo without a site appears at `egohygiene.io/roadmap/<repo>/`. |
| `artifact-only` | The build is retained for review but not publicly deployed. |
| `disabled` | Private or sensitive roadmap publication is intentionally off. |

The first composed consumers should reuse the proven Repository Intelligence composition pattern in Relay.

## Privacy and trust

- Private repositories default to `publication: disabled`.
- The central public aggregator starts from an explicit public-repository allowlist. Disabled/private repositories are excluded before evidence collection and do not appear in public repository counts, placeholders, dependency labels, or error messages.
- A private roadmap can publish only through an explicit public projection whose fields are allowlisted and reviewed.
- Commit messages, issue titles, author data, branch names, and internal URLs are treated as potentially sensitive.
- Build logs must not print tokens, private API responses, or redacted evidence.
- Public artifacts include a provenance record and the exact public/private filtering policy version.
- Stale or unavailable GitHub data renders as unknown; it never silently preserves an old healthy state.

## Roadmap-to-issue planning

The first action is always a dry run:

1. Parse steps whose status is `ready` or `planned` and whose issue list is empty.
2. Propose issue titles, bodies, acceptance criteria, labels, dependency links, and roadmap IDs.
3. Reconcile proposals against existing issues to prevent duplicates.
4. Emit `roadmap.issue-plan.json` and a human-readable summary.
5. Require a manual approval or explicitly authorized Pace operation before creating or updating issues.
6. Write resulting issue references back through a reviewable roadmap pull request.

## Rollout sequence

### Wave 0 - Reconcile truth

- Refresh all repository roadmaps against live implementation and open work.
- Add stable quest IDs, explicit states, dependencies, outcomes, and exit criteria.
- Add Civics to the Hygiene catalog and create its missing roadmap.

### Wave 1 - Contract and validation

- Hygiene publishes `hygiene.roadmap/v1alpha1`.
- Egolint validates the contract locally and in CI.
- Aether publishes authoring guidance and evaluation fixtures.

### Wave 2 - Evidence and renderer

- Observatory publishes the versioned roadmap evidence snapshot.
- Holon publishes the accessible quest-line renderer blueprint.
- Identity publishes the required visual token profile.

### Wave 3 - Reusable automation

- Relay publishes immutable validation, enrichment, build, and composition workflows.
- The workflows pass security review and produce durable provenance.

### Wave 4 - Golden consumers

- `egohygiene.io` publishes the organization route.
- One existing Pages product composes `/roadmap/` without breaking its current deployment.
- One repository without a site appears through the central route.
- A private repository proves artifact-only or disabled behavior without leakage.

### Wave 5 - Fleet adoption

- Pace detects missing or stale adoption state.
- Pace opens bounded PRs using immutable contract and workflow versions.
- Observatory reports coverage, drift, freshness, and blocked dependencies.

## Definition of done

- Every active repository has a validated, evidence-reconciled `ROADMAP.md` with stable steps.
- `egohygiene.io/roadmap/` renders the public organization portfolio.
- Existing site deployments remain single-owner and conflict-free.
- A step expands to show all permitted linked issues, pull requests, commits, releases, and validation evidence.
- Issue plans are deterministic, duplicate-aware, and human-approved before mutation.
- Private data cannot enter public artifacts by default.
- The renderer meets accessibility, mobile, provenance, and performance gates.
- Relay, Holon, Observatory, Egolint, Hygiene, Aether, Pace, Identity, and consumers each remain within their established ownership boundary.
