# Ego Hygiene Visual Roadmap Rollout Plan

**Plan version:** 0.1.0  
**Source specification:** `egohygiene-visual-roadmap-system-spec-v0.1.0.md`  
**Fleet snapshot:** 2026-08-24  
**Scope:** all 28 live `egohygiene/*` repositories  
**Mutation policy:** plan only; no GitHub changes are authorized by this document

## Executive decision

Adopt the visual roadmap system, but do not begin with 28 hand-edited roadmap pull requests.

The safe rollout order is:

1. reconcile the specification against live repository and hosting state;
2. release the canonical Hygiene contract;
3. release the validator, evidence model, Identity token profile, and renderer;
4. release Relay's build-only and composition automation;
5. repair and publish the `egohygiene.io` organization consumer;
6. prove one composed public site, one central public repository, and one disabled private repository;
7. release Pace adoption and issue-plan application only after those proofs pass;
8. roll out roadmap truth PRs and automation PRs in bounded repository waves.

Each consumer receives two independently reviewable changes:

- a **truth PR** that strengthens `ROADMAP.md` and adds stable roadmap metadata;
- an **adoption PR** that pins released tooling and selects a publication mode.

Combining fleet-wide roadmap rewrites with workflow and hosting changes would make review, rollback, and evidence attribution unnecessarily difficult.

## Live fleet facts that constrain the rollout

The live organization currently contains 28 repositories:

`.github`, `aether`, `akashic`, `aniflow`, `athena`, `beacon`, `civics`, `egohygiene`, `egohygiene.io`, `egolint`, `empathy`, `filament`, `flow`, `holon`, `hygiene`, `identity`, `mantle`, `mindcap`, `mindgarden`, `observatory`, `optiflow`, `pace`, `realm`, `reflector`, `relay`, `renderflow`, `sanctuary`, and `store`.

Current publication and source facts:

- 27 repositories are public.
- `egohygiene/egohygiene` is private and is the correct disabled-publication proof.
- 27 repositories contain a root `ROADMAP.md`.
- `civics` is the only live repository without `ROADMAP.md`.
- Six repositories already publish GitHub Pages: `akashic`, `civics`, `empathy`, `optiflow`, `reflector`, and `renderflow`.
- `egohygiene.io` has no live Pages deployment; its preview and deploy workflows are explicitly disabled.
- `egohygiene.io` latest CI fails because the workflow invokes undefined package scripts, and its latest CodeQL run also fails.
- `empathy` is already a composed Quartz and Repository Intelligence site. It cannot accept a competing Pages deployer.
- `store` has a `/store/` Vite/Vercel base but no proven live deployment; it must begin centrally and move to `/store/roadmap/` only after hosting is real.
- `identity` intends to publish under `/identity` but has no public renderer or route yet; it also begins centrally.
- `realm`, `flow`, and `filament` have no GitHub workflow surface today.
- `hygiene` and `observatory` are not yet executable enough to satisfy the roles assigned to them by the proposed specification.

## Specification corrections required before implementation

The source specification is directionally sound, but the following corrections are release blockers.

| Finding | Conflict | Required resolution |
| --- | --- | --- |
| Fleet rewrites precede the schema | Wave 0 asks every roadmap to be rewritten before `hygiene.roadmap/v1alpha1` and its validator exist. | Wave 0 produces a read-only transformation inventory and candidate manifests. Merge consumer truth PRs only after the contract and validator release. |
| Issue plans are inside `dist/roadmap/` | Unpublished roadmap work and proposed issue bodies could be deployed publicly. | Public site output must exclude the issue plan. Emit it to a separate access-controlled workflow artifact. |
| Deterministic output includes wall-clock timestamps | A current timestamp makes otherwise identical builds byte-different. | Use `SOURCE_DATE_EPOCH` or the source commit timestamp inside deterministic files. Put run time in a non-deterministic signed envelope excluded from the content digest. |
| `route: /roadmap/` ignores site bases | GitHub project Pages, `/store`, `/identity`, and versioned documentation require different base paths. | Add normalized `site_base_path` and `public_url` fields. Renderer assets and deep links must be base-aware. |
| `canonical` publication is ambiguous | It is unclear whether the value describes the organization aggregate or a repository's own canonical route. | Reserve `canonical` for `egohygiene.io/roadmap/`. Repositories use `composed`, `central`, `artifact-only`, or `disabled`. |
| Event-driven central refresh has no safe cross-repo trigger | A workflow in one repository cannot deploy `egohygiene.io` without cross-repository credentials. | V1 central aggregation refreshes on schedule and manual dispatch. Add event-driven refresh later through a reviewed GitHub App or webhook, never a broad PAT. |
| “All commits” can be incomplete | GitHub pagination, inaccessible history, rate limits, and rewritten history can truncate results. | Every evidence collection reports `complete`, cursors/counts, source range, and truncation reason. The UI must never imply completeness when it is unknown. |
| `planned` steps automatically generate issue proposals | This can flood 28 repositories with premature issue plans. | Require explicit `issue_policy: propose`. Default planning candidates to `ready`; `planned` is preview-only unless explicitly opted in. |
| Existing Pages consumers rebuild differently | A second Pages artifact replaces rather than merges the live site. Reflector and Renderflow also have expensive/versioned builds. | Relay is build-only. Each existing site copies `dist/roadmap/` into its own final staging directory and deploys exactly once. Trigger cadence is consumer-specific. |
| Organization completeness can reveal private repositories | Aggregate counts or names could reveal the private cognition repository. | Public aggregation uses a Hygiene-owned public allowlist. Disabled/private repositories do not appear in public names, totals, filters, or missing-repository warnings. |
| The private proof was described abstractly | The fleet does contain a private repository. | Use `egohygiene/egohygiene` with `publication: disabled`. Validate exclusion, not publication. |
| Assigned owners are not equally mature | Observatory is docs-only, Holon is early implementation, and Relay must not absorb their semantics permanently. | Require owner-specific releases before Relay integration. Temporary code does not change canonical ownership. |
| The first organization consumer is currently broken | `egohygiene.io` cannot serve as a golden consumer while CI and deployment are disabled. | Land a separate CI/hosting repair PR before the roadmap route PR. |
| HTML-comment metadata is provisional | It is compatible with current front matter but is not yet an Aether extension contract. | V1alpha may use comments, but Hygiene must define parsing, escaping, duplicate-block, and forward-migration behavior. V1 must reconcile with Aether extension rules. |

## Exact ownership and non-ownership

### Hygiene

Hygiene owns:

- `hygiene.roadmap/v1alpha1` and its compatibility policy;
- roadmap states, stable ID rules, dependency semantics, visibility, publication modes, and completion semantics;
- the public repository allowlist used by organization aggregation;
- public/private projection policy and field allowlists;
- migration rules from existing roadmap prose.

Hygiene does not own authoring prompts, semantic-lint implementation, GitHub collection, rendering, workflow orchestration, or repository priority decisions.

Required deliverables:

- JSON Schema and normative Markdown contract;
- positive, negative, legacy, private, and base-path fixtures;
- schema compatibility and deprecation policy;
- public fleet catalog projection that excludes private repositories by construction.

### Aether

Aether owns authoring and maintenance guidance:

- roadmap-authoring skill and agent instructions;
- examples for converting prose phases into stable outcome steps;
- evaluation fixtures for hallucinated completion, invalid dependencies, stale facts, and over-broad milestones;
- guidance for issue-plan review and evidence interpretation.

Aether does not define roadmap state semantics or mutate repository roadmaps.

### Egolint

Egolint owns deterministic source validation:

- comment-block parsing;
- schema validation;
- duplicate and immutable ID checks;
- local and cross-document dependency-cycle validation;
- state/dependency/checklist consistency;
- canonical/generated separation;
- public/private configuration safety checks.

Egolint does not query GitHub or decide whether an outcome is actually complete.

### Observatory

Observatory owns the evidence read model:

- normalized issues, pull requests, commits, releases, checks, and freshness;
- pagination, completeness, inaccessible-data, and staleness semantics;
- public-field filtering and evidence provenance;
- organization-level aggregation inputs.

Observatory does not render HTML, deploy Pages, or create issues.

### Identity

Identity owns a versioned roadmap visual profile:

- status and semantic colors;
- typography, icons, focus treatment, and reduced-motion tokens;
- contrast and motion budgets;
- token package integrity and compatibility.

Identity does not own quest interaction code or roadmap meaning.

### Holon

Holon owns the static quest-line blueprint:

- server/static rendering from normalized inputs;
- base-path-aware routing and assets;
- no-JavaScript fallback;
- accessible interaction and responsive layouts;
- composition contract for an arbitrary staging directory.

Holon does not collect GitHub evidence or deploy consumer sites.

### Relay

Relay owns orchestration only:

- pinned setup of released Hygiene, Egolint, Observatory, Holon, and Identity artifacts;
- build-only `roadmap-validate`, `roadmap-evidence`, `roadmap-render`, and `roadmap-compose` actions;
- reusable workflow examples;
- artifact upload, provenance assembly, and consumer-owned composition hooks.

Relay must not become the source of roadmap schema, evidence semantics, renderer components, or issue mutation policy. Its default action must not call `deploy-pages`.

### Pace

Pace owns fleet adoption and explicitly approved mutations:

- detect missing/stale contract and action versions;
- open bounded truth/adoption PRs;
- apply a reviewed issue plan by exact digest;
- open a follow-up PR that records resulting issue references.

Pace is the only roadmap-system owner permitted to create or reconcile issues, and only through the approval design below. It does not decide roadmap priority or completion.

### `egohygiene.io`

The website owns:

- the organization aggregate route at `/roadmap/`;
- navigation, hosting, routing, caching, deployment, and rollback;
- public repository filters and public freshness presentation;
- consumption of immutable roadmap-system releases.

It does not own repository roadmaps or evidence semantics.

### Consumer repositories

Each repository owns:

- its outcomes, priorities, dependencies, exit criteria, state, and visibility;
- whether it is central, composed, artifact-only, or disabled;
- final site artifact and deployment when composed;
- review and acceptance of generated issue plans.

## Dependency and merge order

### Stage 0 — specification amendment and inventory

No consumer repository changes merge in this stage.

1. Amend the specification with the corrections in this plan.
2. Freeze the 28-repository inventory and current Pages topology.
3. Produce dry-run candidate roadmap manifests without opening PRs.
4. Record existing stable issue IDs, current blockers, and route bases.

**Exit gate:** every proposed consumer change is representable against one draft contract, and no plan output has been published.

### Stage 1 — canonical contract

1. Merge Hygiene's contract, fixtures, visibility rules, and public allowlist.
2. Add Civics to the accepted public catalog, but do not publish its route yet.
3. Tag an immutable Hygiene v1alpha release.

**Exit gate:** legacy roadmaps parse without mutation; invalid IDs, states, cycles, routes, and visibility configurations fail closed.

### Stage 2 — parallel owner implementations

After the Hygiene release:

- Aether publishes authoring guidance and evaluations.
- Egolint publishes roadmap validation.
- Observatory publishes the evidence snapshot schema and read-only collector.
- Identity publishes the roadmap token profile.

These may proceed in parallel but must consume the same immutable Hygiene contract.

**Exit gate:** all four owners publish immutable versions and pass the shared fixture suite.

### Stage 3 — renderer

Holon consumes Hygiene, Observatory fixture snapshots, and Identity tokens to publish the static renderer.

**Exit gate:** static output is base-path independent, accessible, deterministic, sanitized, and usable without JavaScript.

### Stage 4 — automation

Relay composes released owner tools into build-only actions and reusable workflows.

**Exit gate:** Relay produces validated public site output and a separate private issue-plan artifact without deploying or mutating GitHub.

### Stage 5 — organization host repair

Use two `egohygiene.io` PRs:

1. repair CI scripts, runtime-version alignment, CodeQL, preview, and production deployment;
2. add the aggregate `/roadmap/` route using immutable releases.

**Exit gate:** production hosting is real, the existing root portal remains intact, and rollback to the previous site artifact is tested.

### Stage 6 — golden consumers

Use three different proofs:

1. **Composed public site:** `akashic` copies the renderer into `dist/roadmap/` before its existing Pages upload.
2. **Central public repository:** `realm` validates its roadmap and appears under `egohygiene.io/roadmap/realm/` without enabling its own Pages.
3. **Disabled private repository:** `egohygiene` validates privately and is absent from all public artifacts, counts, and diagnostics.

**Exit gate:** all three modes pass security, routing, provenance, and rollback tests.

### Stage 7 — Pace adoption

Only after Stage 6:

1. Pace implements drift detection against immutable contract/action versions.
2. Pace proves truth-PR and adoption-PR generation in dry-run mode.
3. Pace implements guarded issue-plan apply behind an approval environment.

**Exit gate:** no operation can execute without an exact plan digest, source SHA, non-expired plan, repository allowlist, and reviewer approval.

### Stage 8 — fleet rollout

Roll out in bounded waves:

1. control-plane owners;
2. remaining existing Pages consumers;
3. public repositories without sites;
4. product route migrations after their hosts become real.

Do not open all rollout PRs simultaneously. Limit each wave to a reviewable number and stop when a shared contract or workflow defect appears.

## Pages and hosting coexistence

### Non-negotiable rule

There is exactly one final deployment owner per site.

Relay renders and copies. The consumer's existing workflow uploads and deploys. A roadmap adoption PR must not introduce a second `actions/deploy-pages` invocation, a second `github-pages` environment owner, or a parallel artifact that omits existing site content.

### Existing Pages consumers

| Repository | Existing final staging directory | Required composition | Trigger policy | Public route |
| --- | --- | --- | --- | --- |
| `akashic` | `dist` | Copy renderer to `dist/roadmap/` before the existing upload step. | Default push, roadmap change, issue events, schedule, manual; full site build is comparatively bounded. | `https://akashic.egohygiene.io/roadmap/` |
| `civics` | `dist` | Create `ROADMAP.md`, then copy to `dist/roadmap/` before the existing upload. | Use issue-event rebuild only after civic-data validation cost and rate limits are measured. | Require verified HTTPS before declaring `https://civics.egohygiene.io/roadmap/` canonical. |
| `empathy` | `.cache/mindgarden/site` | Copy to `.cache/mindgarden/site/roadmap/` inside `mindgarden-pages.yml`. | Preserve current Mindgarden/report triggers; add roadmap changes and a low-frequency evidence refresh. | `https://egohygiene.github.io/empathy/roadmap/` |
| `optiflow` | `dist`, produced through `scripts/site/build.sh` | Add roadmap as another producer and compose into `dist/roadmap/`. | Default push, roadmap changes, bounded schedule; do not bypass the complete-site verifier. | Require verified HTTPS for `https://optiflow.egohygiene.io/roadmap/`. |
| `reflector` | `_site` | Copy to `_site/roadmap/` before the existing checksum and upload steps. | Do not rebuild LaTeX publications on every issue edit. Use roadmap pushes, manual dispatch, and a low-frequency scheduled full build until a verified base-artifact cache exists. | `https://egohygiene.github.io/reflector/roadmap/` |
| `renderflow` | `/tmp/renderflow-pages` after Mike/`gh-pages` synchronization | Copy to `/tmp/renderflow-pages/roadmap/` after the versioned docs tree is assembled. | Roadmap changes, docs/default pushes, manual, and schedule. Preserve all Mike versions and the default alias. | `https://egohygiene.github.io/renderflow/roadmap/` |

### Route-base contract

The normalized manifest must distinguish:

- logical route: `/roadmap/`;
- site base: `/`, `/store/`, `/identity/`, or GitHub's `/<repository>/` base;
- final public URL;
- asset base.

All generated links, service-worker behavior, canonical metadata, and fragments must be tested under:

- a custom-domain root;
- GitHub project Pages;
- a nested product route;
- a versioned documentation tree.

### Composition acceptance

Before and after every composed adoption:

- snapshot the existing artifact inventory and primary entrypoint;
- preserve `CNAME`, `.nojekyll`, redirects, version aliases, PDFs, intelligence dashboards, and generated manifests;
- verify every pre-existing route still responds;
- verify the new roadmap cannot write outside its assigned subdirectory;
- deploy once;
- retain the previous successful artifact or release for rollback.

## Private-data and untrusted-input safeguards

### Public aggregation

The aggregate must read only repositories explicitly present in Hygiene's released public allowlist. It must never enumerate every repository visible to the workflow token.

`egohygiene/egohygiene` must be:

- configured as `publication: disabled`;
- validated only in its private repository context;
- absent from public repository names, totals, filters, dependency labels, errors, and freshness warnings;
- excluded before GitHub evidence collection, not merely redacted after collection.

### Public evidence allowlist

Default public fields:

- public repository slug;
- roadmap step ID and canonical roadmap-authored text;
- public issue/PR number, state, URL, and timestamps;
- merge commit SHA and public URL;
- release tag and public URL;
- check name, conclusion, and public URL;
- evidence completeness, freshness, and policy version.

Default excluded fields:

- author email or account profile data;
- branch names other than a separately approved public default-branch fact;
- issue and PR bodies or comments;
- private/internal URLs;
- raw API payloads;
- workflow log excerpts;
- commit bodies;
- proposed issue-plan bodies;
- secret names, environment names, and runner paths.

Public issue, PR, and commit titles require an explicit policy flag even when the repository is public. The roadmap-authored outcome remains the primary public description.

### Untrusted text

- Treat roadmap Markdown, issue titles, PR titles, release names, and commit subjects as hostile input.
- Escape HTML and URLs before rendering.
- Allow only reviewed Markdown constructs.
- Reject scripts, event attributes, unsafe protocols, raw iframe/embed content, and path traversal.
- Never use `pull_request_target` to check out or execute pull-request code.
- Issue-triggered workflows check out the trusted default branch at a resolved SHA with read-only permissions.
- Pages write and OIDC permissions exist only in the final trusted deploy job.

### Logging and artifacts

- Logs report counts, step IDs, policy versions, and redaction totals, not private values.
- Tokens and API payloads must not appear in command lines, debug output, annotations, or uploaded diagnostics.
- Public site artifacts contain only filtered `roadmap.manifest.json`, `roadmap.evidence.json`, and public provenance.
- Private issue plans use a short-retention Actions artifact, recommended seven days.
- Public provenance records filtering policy version and redaction counts, never the redacted values.

## Issue-plan dry-run design

### Candidate policy

A step is a creation candidate only when all are true:

- `status: ready`;
- `issue_policy: propose`;
- required dependencies are complete;
- `issues` is empty;
- all required source fields validate;
- the repository allows local issue planning.

`planned` steps may appear in a preview section but do not become create operations by default. Blocked, complete, deferred, and cancelled steps never propose new issues.

### Reconciliation identity

The authoritative managed marker is:

`<!-- hygiene-roadmap-step: REL-RM-003 -->`

Reconciliation order:

1. explicit issue reference in `ROADMAP.md`;
2. exact managed marker in an existing issue;
3. exact fully qualified roadmap-step field in linked PR metadata;
4. title similarity only as a reported conflict requiring human resolution.

The planner must never silently adopt an issue based only on title similarity.

### Plan format

Each plan records:

- plan schema and tool versions;
- repository and visibility;
- roadmap source commit SHA;
- normalized manifest digest;
- evidence snapshot digest;
- plan digest;
- creation and expiry timestamps;
- operation count and maximum permitted operations;
- one operation per step with `create`, `update-managed-block`, `noop`, or `conflict`;
- exact expected current issue identity/state for updates;
- proposed title, managed body block, acceptance criteria, labels, and dependencies;
- risk flags and reasons;
- public/private redaction classification.

Plan generation is byte-deterministic for the same source/evidence inputs. The expiry envelope is separate from the deterministic operation payload.

### Safety limits

- No close, reopen, delete, transfer, milestone, assignee, or cross-repository operation in v1.
- No more than a configured small operation count per apply; default five.
- Updates touch only the marked managed block and preserve human-authored content.
- A conflict produces no mutation.
- A stale source SHA, changed issue state, expired plan, changed contract, or digest mismatch invalidates the entire apply.
- Cross-repository issue creation requires a future separately approved contract.

### Approval and apply

Relay generates the plan but cannot apply it.

Pace apply requires:

1. manual workflow dispatch or an explicitly authorized Pace operation;
2. exact plan artifact and digest;
3. protected environment approval;
4. current repository permission verification;
5. unchanged source SHA and expected issue state;
6. non-expired plan;
7. repository and operation allowlists;
8. a second dry-run summary displayed to the reviewer.

After successful creation or managed-block update, Pace opens a normal pull request adding the resulting issue references to `ROADMAP.md`. It never pushes directly to the default branch.

## Acceptance gates

### Gate A — source contract

- Legacy front matter remains valid.
- Stable IDs are repository-unique and immutable.
- Dependency cycles and missing references fail closed.
- State, dependency, checklist, and completion rules agree.
- Duplicate metadata blocks and unsafe paths fail closed.
- Migration output is idempotent.

### Gate B — evidence

- Every source has timestamp, URL, and source SHA where available.
- Pagination and rate-limit handling are tested.
- Missing, inaccessible, stale, and truncated states are distinct.
- `complete: false` propagates to the UI.
- Rewritten or force-pushed history cannot preserve a false healthy state.

### Gate C — privacy and security

- The private repository exclusion test proves zero public leakage, including aggregate counts.
- Public artifacts pass a secret and private-URL scan.
- Rendered untrusted strings pass XSS and URL-scheme tests.
- Build logs contain no token or API payload.
- All external actions and owner artifacts are pinned immutably.
- PR and issue triggers never execute untrusted code with write permissions.

### Gate D — deterministic rendering

- Identical canonical inputs produce byte-identical content artifacts.
- Source-date behavior is documented and tested.
- Every supported base path passes link and asset checks.
- No-JavaScript HTML contains the complete roadmap meaning.
- Bundle size stays within the accepted budget.

### Gate E — accessibility and visual quality

- WCAG 2.2 AA automated and manual checks pass.
- Keyboard, focus, screen reader, mobile, zoom, contrast, and reduced-motion cases pass.
- Status is never color- or motion-only.
- Visual regression baselines are human-approved and versioned.

### Gate F — Pages coexistence

- One final deploy job and one complete site artifact exist.
- Existing entrypoints, custom domains, version aliases, publications, and dashboards remain valid.
- The roadmap is confined to its route.
- A failed roadmap build cannot partially replace the live site.
- Previous deployment rollback succeeds.

### Gate G — issue planning

- Dry-run has zero GitHub mutations.
- Duplicate, conflict, stale-plan, permission, and operation-limit tests pass.
- The issue plan is absent from public output.
- Apply requires protected approval and exact digests.
- Resulting references return through a reviewable PR.

### Gate H — fleet adoption

- Pace detects versions without rewriting repository-owned intent.
- Rollout PRs are bounded to truth or adoption, not both.
- Central aggregation clearly reports freshness.
- A contract defect stops the active wave before more PRs open.

## Repository-by-repository PR rollout matrix

`T` means truth PR. `A` means automation/publication adoption PR. Provider-owner implementation PRs may update their own roadmap in the same scoped change, but must not include unrelated fleet changes.

| # | Repository | Current gate / truth PR (`T`) | Adoption PR (`A`) and publication mode | Dependency and merge gate |
| ---: | --- | --- | --- | --- |
| 1 | `.github` | Strengthen the organization-standard roadmap around label/routing completion and roadmap PR conventions. | `central`. Add the `Roadmap-Step` field to PR/issue templates only after the contract is released. | Hygiene + Aether guidance; no Pages deployment. |
| 2 | `aether` | Reconcile the pre-release roadmap with the release-workflow blocker and authoring deliverables. | `artifact-only` owner validation plus `central` public projection. | Hygiene release; repair zero-job release workflow before claiming published guidance. |
| 3 | `akashic` | Replace generic phases with current curated-list/site outcomes and stable evidence gates. | `composed` into `dist/roadmap/`. This is the first composed golden consumer. | Relay release; all existing Pages routes and Repository Intelligence checks remain green. |
| 4 | `aniflow` | Align the roadmap with independently released temporal-processing ownership and Flow adapter requirements. | `central` at `/roadmap/aniflow/`; validation workflow only. | Hygiene/Egolint/Relay releases; no new Pages site. |
| 5 | `athena` | Clarify asset-library intake, provenance, licensing, catalog, and release milestones. | `central`; add a pinned roadmap validation workflow because no workflow surface exists. | Contract/tool releases; honest provisional state for unimplemented capabilities. |
| 6 | `beacon` | Reconcile publishing-platform milestones, template ownership, Antidote dependency, and release evidence. | `central`; add pinned validation without enabling Pages. | Contract/tool releases; coordinate Empathy #71 without copying project content. |
| 7 | `civics` | Create the missing `ROADMAP.md` with civic-data, provenance, visualization, and publication gates. | `composed` into `dist/roadmap/`. | Hygiene catalog acceptance; civic privacy review; existing data tests green; HTTPS custom-domain verification. |
| 8 | `egohygiene` | Review and strengthen the private roadmap inside the private repository only. | `disabled`. Validation may run privately; no public evidence or aggregate entry. | Private exclusion and zero-leakage gates; never included in public totals. |
| 9 | `egohygiene.io` | First repair CI, runtime-version drift, CodeQL, metadata, preview, and deployment; then refresh the portal roadmap. | `canonical` organization route at `/roadmap/`. | Separate repair PR must be green and deployed before route PR; consumes immutable owner releases. |
| 10 | `egolint` | Map early-alpha roadmap work to roadmap parser/rule-pack delivery and existing dogfood blockers. | `artifact-only` owner validation plus `central` projection. | Hygiene release; existing dogfood CI must be green before release claims. |
| 11 | `empathy` | Reconcile the detailed baseline roadmap with OSV/OpenSSF failures, ownership drain, #63–#65, and Antidote #71. | `composed` into `.cache/mindgarden/site/roadmap/`. | Relay release; modify only the existing Mindgarden Pages workflow; never add a deployer. |
| 12 | `filament` | Keep architecture-first status explicit; add Firmament reconciliation, license, module-contract, vertical-slice, and adoption gates. | `central`; add pinned validation because no workflow exists. | Boundary approval and license correction; no claim of implemented IaC. |
| 13 | `flow` | Retain the strong federated boundaries; add CI, adapter, restore-and-assess #3, recovery, and release steps. | `central`; add contract/roadmap validation only. | Hygiene/Egolint/Relay; no orchestration completion without executable evidence. |
| 14 | `holon` | Reconcile early implementation with renderer-blueprint ownership and its existing React/Vite gate. | `artifact-only` owner preview plus `central` projection. | Hygiene + Identity + Observatory fixtures; publish renderer before Relay consumes it. |
| 15 | `hygiene` | Accept architecture ADRs, publish roadmap policy/schema, and make current execution gates explicit. | `central` data/contract projection; no Pages. | First implementation owner PR and immutable release; CI must exist for contract validation. |
| 16 | `identity` | Continue its strong active roadmap from #13 through renderer/studio, public route, pilots, and v1.0.0. | Initially `central`; later `composed` at `/identity/roadmap/` after #14–#16 deploy. | Publish token profile first; product route migration is a separate later PR. |
| 17 | `mantle` | Record red/cancelled CI, classify the 73-bin inventory, finish #17, #18–#20, and Realm adoption. | `central`. | Main static/Linux/macOS CI green before progress is represented as release-ready. |
| 18 | `mindcap` | Reconcile capture-engine sources, normalization, provenance, plugin, and extraction milestones. | `central` with pinned validation. | Contract/tool releases; public roadmap must not expose captured user content. |
| 19 | `mindgarden` | Clarify standalone knowledge lifecycle, extraction from Empathy, publication boundary, and consumer evidence. | `central`; add validation because no workflow surface exists. | Coordinate Empathy composed site without creating a second canonical implementation. |
| 20 | `observatory` | Replace docs-only phases with evidence ingestion, snapshot schema, completeness, aggregation, and release milestones. | `artifact-only` owner evidence fixtures plus `central` projection. | Hygiene release; executable collector and tests must precede Relay integration. |
| 21 | `optiflow` | Reconcile the site/product roadmap with current read-only safety boundary, v1 work, and Flow contracts. | `composed` through the existing site producer into `dist/roadmap/`. | Relay release; complete-site verifier, docs, and intelligence routes stay green; verify HTTPS custom domain. |
| 22 | `pace` | Keep lock-v1 observed-state/drift work ahead of mutation; add truth/adoption PR and guarded issue-plan phases. | `artifact-only` for mutation plans plus `central` public roadmap. | Golden consumers must pass before Pace apply exists; protected approval gate mandatory. |
| 23 | `realm` | Replace generic phases with exact pin/CI, base image #1, profiles #5/#6/#8, supply chain #7/#10, and services #9/#13 outcomes. | `central`. This is the central golden consumer. | Zero SHA pins removed and roadmap validation green; no Pages enablement. |
| 24 | `reflector` | Reconcile paper, magazine, research, release, and publication milestones with current WIP/final artifacts. | `composed` into `_site/roadmap/`. | Do not rebuild LaTeX on every issue event; preserve all PDFs, previews, checksums, and publication metadata. |
| 25 | `relay` | Reconcile released v1.2 state with roadmap validation, evidence, rendering, composition, and security-review steps. | `artifact-only` action previews plus `central` projection. | Depends on all owner releases; action is build-only and pinned by immutable SHA/tag. |
| 26 | `renderflow` | Reconcile renderer-engine releases and supported-format/docs gates with Flow integration. | `composed` into `/tmp/renderflow-pages/roadmap/` after Mike synchronization. | Preserve every versioned docs route and `latest` alias; one existing deploy job. |
| 27 | `sanctuary` | Mark bootstrap complete, then register in Hygiene, prove one real incubation, terminal decision, and evidence-driven automation. | `central`. | Hygiene registration and one real public-safe lifecycle; no Pages required. |
| 28 | `store` | Consolidate root and `docs/roadmap.md`; record E2E failure, live Fourthwall, deployment, provider-neutral #11, and #9/#12/#13 gates. | Initially `central`; migrate to `composed` at `/store/roadmap/` only after the `/store` host is deployed and green. | Fix E2E and red dependency PR first; product-route migration remains separate. |

## Rollout wave assignments

### Owner wave

`hygiene` → `aether`, `egolint`, `observatory`, `identity` → `holon` → `relay`

### Host and golden wave

`egohygiene.io` repair → `egohygiene.io` route → `akashic` → `realm` → private `egohygiene` exclusion

### Control-plane consumer wave

`.github`, `aether`, `egolint`, `holon`, `hygiene`, `identity`, `observatory`, `pace`, `relay`

Provider-owner changes already merged in the owner wave do not need duplicate truth PRs.

### Existing Pages wave

`civics`, `empathy`, `optiflow`, `reflector`, `renderflow`

Roll out one at a time because each has a distinct staging and deployment topology.

### Public central wave

`aniflow`, `athena`, `beacon`, `filament`, `flow`, `mantle`, `mindcap`, `mindgarden`, `sanctuary`, `store`

`store` remains central until its product host passes its own deployment gate.

## Rollback

- Truth PR rollback restores the previous roadmap but retains stable IDs in a supersession record if they were already published.
- Adoption rollback removes the pinned consumer workflow/configuration and restores the previous complete site workflow.
- A composed deployment must retain the prior successful complete artifact or release.
- Organization aggregation can disable one repository entry through a reviewed Hygiene allowlist update without changing that repository's intent.
- A failed issue-plan apply stops before any operation if preconditions drift. If some operations succeed before an external failure, the result records exact created/updated issue IDs and opens no write-back PR until reconciliation is reviewed.
- No rollback deletes issues or historical roadmap IDs.

## Program completion

The rollout is complete only when:

- all 28 repositories have reviewed roadmap intent, including a private-only review for `egohygiene`;
- all 27 public repositories except intentionally central-only owner artifacts appear through an approved public projection;
- Civics has a canonical `ROADMAP.md`;
- all six existing Pages sites still deploy through one consumer-owned artifact and expose a working roadmap subroute;
- `egohygiene.io/roadmap/` is deployed, accessible, and freshness-aware;
- the private repository is absent from public names, counts, evidence, and diagnostics;
- all generated public artifacts pass privacy, XSS, secret, link, accessibility, base-path, provenance, and reproducibility gates;
- issue-plan generation is deterministic and mutation-free;
- Pace apply is protected, digest-bound, bounded, and human-approved;
- no canonical ownership boundary in the specification has been collapsed into Relay or the website for rollout convenience.
