# Organization Intelligence hosting compatibility

Status: **proposed**, declaration contract **2.0.0-alpha.1**. Governing proposal:
[ADR-0020](../decisions/ADR-0020-organization-intelligence-export-hosting.md).

The website owns the organization Intelligence UI and its sealed static export.
`egohygiene/.github` owns the selected organization entry point, composition
selection, project Pages publisher and recovery. The website continues to own
its company site, documentation and store integration. Hygiene owns surface
identity and declaration semantics; Observatory and the report/model owners
retain their evidence semantics. Moving a publisher transfers none of those
authorities. Repository-owned dashboards and publishers remain independent.

## One explicit declaration dialect

The existing v1 registry remains the single route registry, with the same 36
surface IDs, profiles, states, requirements and dependencies. Its current
ownership description separates the website compositor from the selected
publication repository. The three v1 fixture references bind that updated
canonical registry digest; their facts and all v1 validator/schema semantics
remain unchanged. Older immutable pins retain their original bytes and rules.

The new [v2 declaration schema](../../schemas/public-site-surface-declaration.v2.schema.json)
selects a single narrow compatibility profile. It contains the six v1 top-level
members plus `hosting_profile`, with these explicit discriminators:

- `schema`: `egohygiene.public-site-surface-declaration/v2`.
- `contract_version`: `2.0.0-alpha.1`.
- `hosting_profile`: `organization-intelligence-static-export/v1`.
- `synthetic`: `false`.
- Site subject and publication repository: `egohygiene/.github`.
- Origin: `https://egohygiene.github.io`; base: `/.github/`.
- Route profile: `organization`; site visibility: `public`.

All 36 rows remain required in registry order. The declaration still binds the
v1 registry's exact schema, version, source path, externally resolved full
revision and canonical digest. A hash alone authenticates no claimed revision.
The registry digest is sorted, compact UTF-8 JSON **without a final newline**,
using the existing owner's `canonical_digest` function.

The only changed renderer binding covers `landing` and these existing surfaces:
`audits`, `compare`, `dashboard`, `decisions`, `dependencies`, `diagnostics`,
`distribution`, `health`, `hygiene`, `identity_intelligence`, `intelligence`,
`journey`, `now`, `releases`, `roadmap`, `sanity`, `search`, `status`, and `work`.
When a renderer is present for those rows, it must name:

- Owner `egohygiene/egohygiene.io`.
- Contract `organization-intelligence-static-export`.
- Version equal to the actual full producer commit SHA.
- Implementation equal to that commit's exact HTTPS GitHub blob URL for
  `scripts/build-intelligence-export.mts` in `egohygiene/egohygiene.io`.

All present export renderers name the same producer revision. The publisher
must additionally match that revision to the selected manifest and provider
artifact metadata. Other surfaces retain the original renderer rules. The
profile cannot select a repository route profile, another publisher, another
origin, another base, a general website renderer override, or a false Relay
renderer label. There is no global owner alias or runtime mutation of v1 rules.

## Sources, availability and publication evidence

Renderer ownership is distinct from semantic and source ownership. For these
repository-owned surfaces the semantic subject stays `.github`. Its source
artifact can be a repository-owned, immutable composition/selection manifest
that references the producer export and original model sources. It must not
claim that `.github` authored the upstream raw model or that the website owns
the subject's facts. The source kind continues to match each registry row.

A rendered unavailable page can be implemented while its model remains
unavailable. Neither a page nor a successful deployment changes the original
report's represented revision, assessment time, partial scope or human posture.
An unknown applicability assessment remains explicit and evidence-backed; it
cannot be replaced by an invented not-applicable exemption.

Before deployment, an implemented page may be declared `unpublished`: its
renderer and source must be present, publication freshness is `unknown`, and
canonical URL, publication evidence URL, represented publication revision and
publication observation time remain null. A reason explains the unpublished
state. Do not prefill a successful deployment receipt. After actual publication,
the existing published-state evidence, freshness and dependency closure rules
apply. A declaration's validity does not authenticate its observations.

The sealed exporter and review intake remain separate, review-only contracts.
Their original `publication: review-only`, `hosting_transition: not-admitted`
and `deployment_authorized: false` receipts stay unchanged. A separately
authorized publisher verifies those exact bytes and records its own authority,
source/deployment/live verification and recovery evidence. An old review
receipt is neither a publisher permission nor a permanent veto over a later
explicitly authorized publisher.

## Owner API and immutable resource closure

Use [tools/organization_hosting.py](../../tools/organization_hosting.py):

```text
validate_declaration(declaration, registry, expected_registry_revision=None)
    -> list[str]
validate_registry(registry, known_contracts=None) -> list[str]
canonical_digest(value) -> str
load_json(path) -> dict
```

V1 inputs delegate unchanged. V2 first checks its exact profile, real renderer
owner and producer binding. A private copy then maps only that checked renderer
binding into v1's validation vocabulary so the unchanged owner engine checks
all shared invariants. The copy is never returned, persisted, hashed as the
original, published as Relay provenance or used as a deployment receipt.
Consumers retain and hash the original v2 declaration.

Pin the exact source commit and raw hashes of `organization_hosting.py`,
`site_surfaces.py`, adjacent `https_locations.py`, both declaration schemas,
the v1 registry schema and the current registry JSON. Do not load owner code
from a consumer checkout or a moving branch. A command-line check is:

```bash
python3 -I tools/organization_hosting.py validate-declaration \
  --declaration publication/organization-site-surfaces.json \
  --registry-revision "$HYGIENE_REGISTRY_REVISION"
```

The explicit variable must be an independently resolved, full immutable pin;
this command is usage guidance, not a deployment receipt. The schema is
standalone Draft 2020-12; semantic owner checks are also required.

Existing v1-only EgoLint, Holon and Observatory consumers do not automatically
support v2. This change claims the Hygiene owner checker and the separately
selected organization publisher integration, not native EgoLint conformance,
fleet adoption, human ratification or a release. Keep old consumer pins until
their own reviewed v2 adoption.

## Migration, validation and recovery

No existing declaration is rewritten to v2. Repository-profile and other v1
consumers keep their old schema/helper/pin selection. Only the reviewed
organization publisher selects the new dialect. Roll back its source and
selected artifact through its own recorded recovery mechanism; preserve prior
publications and all historical receipts. No fallback weakens artifact identity,
renderer ownership, source evidence or public-scope checks.

Focused tests cover all three existing complete fixtures and the new positive
organization case, schema/owner agreement, false Relay attribution, mixed
producer revisions, unsupported scopes and renderers, missing registry/source/
publication evidence, incomplete declarations and closed discriminators.
These checks are separate from actual provider activation, Pages deployment,
browser/live-byte verification and recovery, which remain publisher-owned.
New ADRs stay proposed with null approval. Explicit user deployment authority
does not ratify those records or the independent Agent-Ready Web proposal.
