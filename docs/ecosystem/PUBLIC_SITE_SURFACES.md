# Public-site surface and route registry

- Status: **proposed**
- Contract version: **1.0.0-alpha.1**
- Registry: [`catalog/public-site-surface-registry.json`](../../catalog/public-site-surface-registry.json)
- Registry schema: [`public-site-surface-registry.v1.schema.json`](../../schemas/public-site-surface-registry.v1.schema.json)
- Declaration schema: [`public-site-surface-declaration.v1.schema.json`](../../schemas/public-site-surface-declaration.v1.schema.json)
- Governing proposal: [`ADR-013`](../decisions/ADR-013-public-site-surface-route-registry.md)
- Tracking issue: [Hygiene #25](https://github.com/egohygiene/hygiene/issues/25)

## Purpose

The registry gives public mini-apps and supporting pages stable identities,
scope-specific canonical routes, redirect aliases, applicability rules,
requirements, ownership, source and renderer expectations, dependencies, and
truthful state semantics. A separate declaration records what one repository
or organization site actually owns, inherits, omits, implements, and publishes.

The split is authoritative:

- Hygiene owns registry meaning and schemas;
- a subject repository owns its facts and applicability evidence;
- a publication repository owns the final hosted artifact;
- renderer owners keep their implementations; and
- consumers resolve a pin instead of copying policy or code.

The proposal is contract-complete and fixture-tested. Its `proposed` lifecycle
does not claim acceptance, release, live adoption, deployment, or conformance.

## Route profiles and hosting bases

One universal route map cannot represent both the organization control plane
and Relay's shipped Repository Intelligence bundle. Every declaration selects
exactly one route profile:

- `organization` gives first-class organization modules top-level routes such
  as `/roadmap/`, `/decisions/`, `/dependencies/`, and `/health/`;
- `repository` keeps Repository Intelligence modules under `/intelligence/`,
  such as `/intelligence/roadmap/` and `/intelligence/decisions/`.

Modules that the v1 organization roadmap keeps local to Intelligence or a
repository detail—Now, Journey, Compare, Work, Diagnostics, and the legacy
Dashboard—remain under `/intelligence/` in both profiles. A declaration can
still mark any site-declared surface not applicable; a registered route is not
a publication claim.

`site.origin` contains only the HTTPS scheme and host. `site.base_path` handles
GitHub project Pages, product mounts, and versioned documentation. The final
canonical URL is `origin + base_path + selected profile route`.

For example, origin `https://docs.example.invalid`, base path
`/synthetic-docs/`, and logical route `/docs/` resolve to
`https://docs.example.invalid/synthetic-docs/docs/`. The subject repository is
`site.id`; `site.publication_repository` may be different for central hosting.

Directory routes end in `/`; file endpoints do not. Routes are lowercase,
absolute, unencoded paths without query strings, fragments, wildcards, empty
segments, or backslashes. An alias is a redirect only and cannot serve a second
copy of canonical content.

| Surface | Organization canonical | Repository canonical | Default | Renderer |
| --- | --- | --- | --- | --- |
| `accessibility` | `/accessibility/` | `/accessibility/` | recommended | site-owned |
| `audits` | `/audits/` | `/intelligence/audits/` | optional | Relay-compatible |
| `blog` | `/blog/` | `/blog/` | optional | site-owned |
| `community` | `/community/` | `/community/` | optional | site-owned |
| `compare` | `/intelligence/compare/` | `/intelligence/compare/` | optional | Relay-compatible |
| `dashboard` | `/intelligence/dashboard/` | `/intelligence/dashboard/` | optional | Relay-compatible |
| `decisions` | `/decisions/` | `/intelligence/decisions/` | optional | Relay-compatible |
| `dependencies` | `/dependencies/` | `/intelligence/dependencies/` | optional | Relay-compatible |
| `diagnostics` | `/intelligence/diagnostics/` | `/intelligence/diagnostics/` | optional | Relay-compatible |
| `distribution` | `/distribution/` | `/intelligence/distribution/` | optional | Relay-compatible |
| `documentation` | `/docs/` | `/docs/` | optional | site-owned |
| `donate` | `/donate/` | `/donate/` | optional | site-owned |
| `feed` | `/feed.xml` | `/feed.xml` | optional | site-owned |
| `garden` | `/garden/` | `/garden/` | optional | site-owned |
| `health` | `/health/` | `/intelligence/health/` | optional | Relay-compatible |
| `help` | `/help/` | `/help/` | optional | site-owned |
| `hygiene` | `/hygiene/` | `/intelligence/hygiene/` | optional | Relay-compatible |
| `identity` | `/identity/` | `/identity/` | recommended | Identity-compatible |
| `identity_intelligence` | `/intelligence/identity/` | `/intelligence/identity/` | optional | Relay-compatible |
| `intelligence` | `/intelligence/` | `/intelligence/` | optional | Relay-compatible |
| `journey` | `/intelligence/journey/` | `/intelligence/journey/` | optional | Relay-compatible |
| `landing` | `/` | `/` | required | site-owned |
| `legal` | `/legal/` | `/legal/` | recommended | site-owned |
| `magazine` | `/magazine/` | `/magazine/` | optional | Renderflow-compatible |
| `now` | `/intelligence/now/` | `/intelligence/now/` | optional | Relay-compatible |
| `presentation` | `/presentation/` | `/presentation/` | optional | Renderflow-compatible |
| `privacy` | `/privacy/` | `/privacy/` | recommended | site-owned |
| `privacy_choices` | `/privacy/choices/` | `/privacy/choices/` | optional | site-owned |
| `releases` | `/releases/` | `/intelligence/releases/` | optional | Relay-compatible |
| `roadmap` | `/roadmap/` | `/intelligence/roadmap/` | optional | Relay-compatible |
| `sanity` | `/sanity/` | `/intelligence/sanity/` | optional | Relay-compatible |
| `search` | `/search/` | `/intelligence/search/` | optional | Relay-compatible |
| `status` | `/status/` | `/status/` | optional | Relay-compatible |
| `support` | `/support/` | `/support/` | optional | site-owned |
| `trust` | `/trust/` | `/trust/` | optional | site-owned |
| `work` | `/intelligence/work/` | `/intelligence/work/` | optional | Relay-compatible |

The machine registry is authoritative for aliases. Important compatibility
rules include:

- organization `/intelligence/roadmap/` redirects to `/roadmap/`, while a
  repository `/roadmap/` redirects to `/intelligence/roadmap/`;
- `/adr/` remains a decisions redirect in both profiles;
- `/activity/` and `/journey/` redirect to `/intelligence/journey/`;
- `/documentation/` redirects to `/docs/`;
- `/slideshow/` redirects to `/presentation/`; and
- `/status/` stays canonical in both profiles because System Status is not a
  Repository Intelligence submodule.

## Identity route conflict

Two different products currently want the same organization path. Accepted
Identity ADR-017 assigns `/identity/` to the Identity product experience.
`.github#37` asks for an Observatory-backed organization adoption module at
that path. The registry does not collapse their source, renderer, dependency,
or ownership contracts:

- `identity` remains the Identity-owned product surface at `/identity/`;
- `identity_intelligence` remains the adoption/provenance module at
  `/intelligence/identity/`.

Identity Intelligence depends on the Intelligence shell, not publication of
the Identity product surface. It must be able to report missing, inapplicable,
or stale Identity adoption without making `/identity/` a publication gate.

The `.github#37` implementation issue must reconcile its requested top-level
route with this accepted product route before publication. Until then, the
nested module route is canonical and no alias may duplicate `/identity/`.

## Applicability, requirement, and truthful absence

Applicability resolves before requirement and delivery state. It is a separate
evidence object so an application with no consent-control obligation or a
static site with no monitored service can truthfully declare a recommended
surface not applicable without weakening the registry's requirement strength.

| Axis | Values | Meaning |
| --- | --- | --- |
| Applicability | `applicable`, `not_applicable`, `unknown` | Whether the surface applies to this site, with assertion, freshness, reason, represented revision, observation time, and evidence URL. |
| Requirement | `required`, `recommended`, `optional` | Site-class policy strength when applicable. |
| Disposition | `owned`, `inherited`, `omitted` | Semantic ownership or explicit omission. |
| Implementation | `unknown`, `missing`, `planned`, `blocked`, `implemented`, `unsupported`, `not_applicable` | Whether implementation exists and why it may not. |
| Publication | `unknown`, `unpublished`, `preview`, `published`, `withdrawn`, `not_applicable` | Publication lifecycle, independent of implementation. |
| Visibility | `public`, `internal`, `private` | Maximum audience for the declaration and surface. |
| Freshness | `current`, `stale`, `unknown`, `not_applicable` | Whether evidence represents the declared site revision. |
| Assertion | `authoritative`, `inferred`, `unknown` | Strength of a state claim. |

`landing` is always applicable. Other surfaces are site-declared. Applicable,
not-applicable, and unresolved-unknown applicability results require complete
current-or-stale assessment evidence unless private visibility requires
redaction. An unknown result records that a current review could not resolve
applicability; it still forces delivery state to remain unknown and cannot
carry delivery evidence. Not-applicable applicability synchronizes disposition,
implementation, publication, and freshness to the not-applicable tuple.

The remaining states are not interchangeable:

- **missing** is an evidence-backed observation that no implementation exists;
- **planned** records intent but no implementation;
- **blocked** requires named blockers, except private topology uses the literal
  redaction marker;
- **private** records existence and reason while redacting source, renderer,
  URLs, revisions, observations, evidence, and dependency topology;
- **stale** records evidence that no longer represents the current site
  revision;
- **not applicable** is an authoritative, reasoned applicability decision; and
- **unknown** preserves uncertainty instead of fabricating absence.

Every declaration covers every registry surface in registry order. Any new
surface ID is therefore a breaking registry change with an explicit migration;
optional additions are not silently compatible. A published surface requires
an immutable source, exact-version or full-SHA renderer pin, canonical URL,
evidence URL, represented revision, observation time, and current-or-stale
freshness. `current` revisions equal `site.represented_revision`.

Dependencies are route-profile-specific publication prerequisites, not
navigation hints. A published surface can depend only on surfaces that are
also implemented and published in the selected profile. Repository-profile
Intelligence modules depend on the Intelligence shell. First-class
organization routes such as `/roadmap/`, `/decisions/`, and `/health/` do not;
they can publish independently. System Status is not a prerequisite for Health
in either profile; those domains remain separate until an explicit composition
contract says otherwise.

## Ownership, provenance, and privacy

A declaration separates:

- `site.id`: repository whose facts are represented;
- `site.publication_repository`: repository with final host/deploy authority;
- `owner`: semantic surface owner;
- `source_artifact.owner`: immutable source owner; and
- `renderer.owner`: exact-pinned renderer owner.

The registry value `default_owner: repository` means the subject repository
owns the surface semantics. A repository ID instead names a global semantic
authority that declarations must preserve. In v1, the Identity product surface
names `egohygiene/identity`; its adoption/provenance intelligence module remains
repository-owned. Source artifacts for owned and inherited surfaces must name
that semantic owner. Renderer ownership is contract-bound: site-owned
renderers belong to the subject repository, while Identity-, Relay-, and
Renderflow-compatible renderers name those canonical owners. Publication
authority still stays with the declared publication repository. Relative source paths cannot be absolute, traverse
with either slash style, or escape the repository; external sources use HTTPS.

The declaration binds the registry schema, exact version, canonical path, full
revision, and canonical JSON SHA-256. For non-synthetic declarations, the
validator also requires an externally resolved expected registry revision;
matching bytes alone cannot prove a claimed commit. Consumers fail closed on
unknown surfaces, incomplete coverage, mismatched routes, pins, or digests.

Private site or surface visibility cannot be widened downstream. Observatory
may retain privacy-safe state and reason, but must not infer or publish private
applicability evidence, URLs, repository topology, blockers, source paths,
renderer details, revisions, or evidence locations.

## Composition with neighboring contracts

| Contract | Composition boundary |
| --- | --- |
| Agent-Ready Web | Shares site classes and applicability-first resolution. That profile still owns discovery, representations, capability, commerce, and conformance. |
| Public-site policy | The proposed contract tracked by [Hygiene #17](https://github.com/egohygiene/hygiene/issues/17) owns legal, policy, trust, disclosure, review, and jurisdiction semantics. This registry owns only the corresponding route identities and declaration state. |
| Repository Intelligence | Supplies provenance-aware projections; dashboards never replace canonical roadmap, ADR, Git, GitHub, release, deployment, or provider truth. |
| Repository presentation | Owns README/orientation slots and evidence badges, not public route identity. |
| Identity | Owns `/identity/`, brand intent, released assets, and renderer inputs; the separate adoption module cannot take that authority. |
| Renderflow | Supplies versioned magazine and presentation artifacts; the consuming publication repository owns routing and deployment. |
| System Status | Owns incident, component, severity, uptime, and operational semantics; this registry only reserves `/status/`. |

Agent-Ready Web discovery and representation resources stay in that profile.
They are referenced by composition and are not duplicated as route surfaces.

## Consumer handoff

- **Hygiene** owns IDs, profiles, route bindings, applicability, state
  semantics, schemas, compatibility, dependencies, and privacy boundaries.
- **Repositories** own truthful declarations, source facts, applicability
  evidence, and represented revisions.
- **Holon** may scaffold complete declarations for new repositories from an
  eligible immutable pin without inventing facts or evidence.
- **Relay** may implement validation, redirect, rendering, and publication
  workflows without redefining the contract or taking deploy authority.
- **Observatory** may normalize privacy-safe declarations and freshness without
  remediation or private-topology disclosure.
- **Pace** may propose reviewed adoption and reconciliation changes for
  existing repositories without direct default-branch mutation.
- **Identity** and **Renderflow** publish versioned inputs and retain their own
  implementation boundaries.
- **egohygiene.io** owns organization-site composition and hosting, not the
  canonical facts displayed by its modules.

## Normative validation and fixtures

The JSON Schemas define the exchange shape and key state conditionals. The
dependency-free Python checker is the normative v1 semantic validator for
route collisions, complete coverage, state cross-products, base-path URL
resolution, evidence, dependency closure, privacy, and pin verification.
JSON Schema URI `format` support varies by implementation, so consumers must
also run the normative checker for hostname, credential, port-range,
control-character, and browser backslash-normalization checks.
It proves alias uniqueness and canonical mapping at declaration time. Relay or
another site-owned deployment workflow must separately verify that published
aliases are redirects and never duplicate canonical content; this proposal
does not claim a live redirect check.

```bash
python3 tools/site_surfaces.py validate-registry
python3 tools/site_surfaces.py validate-fixtures
python3 tools/site_surfaces.py validate-declaration \
  --declaration path/to/site-surfaces.json \
  --registry-revision 0123456789abcdef0123456789abcdef01234567
python3 tools/site_surfaces.py digest
```

The explicitly synthetic fixtures cover a small content site, a documentation-
heavy repository hosted under a project base path by a separate publication
repository, and an organization hybrid using the organization route profile.
Together they prove inherited rendering, missing and planned work, blockers,
private redaction, stale publication, distinct Identity surfaces, explicit
not-applicability, dependencies, and top-level versus nested routes. Synthetic
origins, revisions, and evidence are shape proofs only.

## Non-goals

This proposal does not implement or deploy a site, create redirects, generate
Repository Intelligence, resolve the Identity route conflict, define System
Status semantics, copy a renderer, certify conformance, or adopt declarations
in another repository. Those remain separately reviewed downstream changes.
