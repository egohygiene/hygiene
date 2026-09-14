# Agent-Ready Web discovery and representation profile

Status: **proposed `1.0.0-alpha.2`**

Policy owner: `egohygiene/hygiene`

Tracked by: [hygiene#51](https://github.com/egohygiene/hygiene/issues/51),
checkpoint 2 of [hygiene#16](https://github.com/egohygiene/hygiene/issues/16)

## Purpose and authority

The Agent-Ready Web profile defines how an Ego Hygiene website can remain an
excellent human-facing experience while exposing explicit, efficient, and safe
machine-readable surfaces. Checkpoint 1 established the vocabulary and
ownership boundary. This checkpoint registers only discovery and efficient
representation mechanisms.

The canonical machine source is
[`catalog/agent-ready-web-profile.json`](../../catalog/agent-ready-web-profile.json),
validated against
[`schemas/agent-ready-web-profile.v1.schema.json`](../../schemas/agent-ready-web-profile.v1.schema.json).
This guide explains that policy but does not override it. The profile remains
proposed: registration supports review and pinned experimentation, not
acceptance, publication, rollout, or a downstream conformance claim.

## Contract identity

| Field | Value |
| --- | --- |
| Contract | `egohygiene.agent-ready-web-profile/v1` |
| Profile version | `1.0.0-alpha.2` |
| Status | `proposed` |
| Canonical owner | `egohygiene/hygiene` |
| Consumer pin | Exact semantic version or immutable repository revision |
| Catalog scope | Discovery and source-equivalent representations only |

The four independent concerns, five stable site classes, five requirement
strengths, and four maturity levels defined by checkpoint 1 remain unchanged.
Each mechanism still has exactly one primary concern. The entries below use
only `readability` or `efficiency`; no entry grants a capability or supplies
commerce semantics.

## Resolution and truthful absence

Applicability is resolved before requirement strength. A validator first asks
whether the mechanism's explicit condition is true for the site and only then
applies the site-class rule.

| Resolved state | Result |
| --- | --- |
| Not applicable and absent | Valid |
| Optional and absent | Valid |
| Recommended and absent | Advisory |
| Conditional and condition false | Valid |
| Required and absent | Error |
| Prohibited and present | Error |
| Emerging or experimental and absent | Non-blocking by default |
| Fabricated placeholder | Prohibited |

An inapplicable or unsupported artifact must be absent. Empty files, invented
entities, placeholder links, permissive claims, and stale generated output do
not satisfy a requirement. Evidence can explain why a recommendation was not
implemented, but it cannot turn a required omission into a pass.

Every catalog record declares an applicability condition, a default strength,
and an explicit override for all five site classes. That makes resolution
deterministic and prevents a consumer from treating a missing override as an
implicit requirement.

## Discovery and representation catalog

Strength abbreviations are `R` required, `A` recommended (advisory when
absent), and `O` optional. They apply only after the applicability condition is
true.

| Mechanism | Concern | Maturity | Applicability condition | App | Commerce | Content | Docs | Hybrid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ai-crawler-guidance` | readability | emerging | Identified crawler operator publishes authoritative product-token policy | O | O | O | O | O |
| `ai-oriented-hints` | readability | experimental | Identified consumer owns a public hint specification | O | O | O | O | O |
| `canonical-metadata` | readability | established | Page is public/indexable or duplicates an equivalent URL | R | R | R | R | R |
| `cats-txt` | readability | experimental | Operator intentionally maintains a truthful cats file | O | O | O | O | O |
| `entitymap-html` | readability | published specification | A conforming `entitymap.json` is published | R | R | R | R | R |
| `entitymap-json` | readability | published specification | A source-backed public entity index can be maintained | O | O | O | O | O |
| `llms-full-txt` | efficiency | emerging | A bounded public documentation corpus can be aggregated safely | O | O | O | O | O |
| `llms-txt` | readability | emerging | Curated public AI-readable content benefits from an index | O | O | A | A | A |
| `markdown-alternate` | efficiency | emerging | A current public source-equivalent can be maintained | O | O | A | A | A |
| `robots-txt` | readability | established | A public HTTP origin exposes crawlable resources | R | R | R | R | R |
| `sitemap-xml` | readability | established | A truthful public indexable URL set exists | A | R | R | R | R |
| `structured-discovery-jsonld` | readability | established | Stable vocabulary describes visible public facts | A | A | A | A | A |

The canonical records contain the complete paths, media types, content rules,
validation rules, maturity rationale, primary references, and registration
evidence. The summaries below highlight the policy boundaries that consumers
must not lose.

### Established discovery mechanisms

- `robots-txt` follows [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)
  at `/robots.txt`. It is crawler guidance, not authentication,
  confidentiality, training consent, or action permission. It must not be used
  to advertise secret paths.
- `sitemap-xml` follows the
  [Sitemaps protocol](https://www.sitemaps.org/protocol.html). It contains only
  canonical, intentionally public URLs on permitted hosts. Optional timestamps
  reflect real source changes; invented priority or change-frequency values
  are omitted.
- `canonical-metadata` follows
  [RFC 6596](https://www.rfc-editor.org/rfc/rfc6596.html). A canonical relation
  identifies the preferred human-facing URL, never an access grant or a way to
  combine materially different content.
- `structured-discovery-jsonld` uses
  [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) and an authoritative stable
  vocabulary such as [Schema.org](https://schema.org/docs/gs.html). Structured
  facts remain visible on and consistent with the canonical page. This entry
  deliberately does not define advertising, seller, offer, payment,
  fulfillment, action, or transaction semantics.

### Published specifications

`entitymap-json` and its generated `entitymap-html` companion follow the
[EntityMap v1.0 specification](https://www.entitymap.org/spec/v1.0). They are
registered as a published industry specification, not a broadly established
web standard. The JSON index is optional and must contain public,
source-supported entities, evidence, verification state, and provenance. If it
is published, the HTML companion is required, is generated from the same
revision, and exposes equivalent attribution and source links. Failure to
support EntityMap is a valid absence; a partial or invented map is not.

### Emerging conventions

- `llms-txt` follows the path-scoped
  [llms.txt v2 proposal](https://llmstxt.org/) and its documented
  [changes](https://llmstxt.org/changes.html). It is a concise curated overview
  and link index, not crawl permission, training consent, authorization, or a
  capability declaration.
- `llms-full-txt` records the separately observed
  [documentation-platform convention](https://www.mintlify.com/docs/ai/llmstxt)
  for `/llms-full.txt`. It is not part of the cited llms.txt v2 proposal. A
  present aggregation must have a bounded public corpus, explicit provenance,
  a size budget, and the same freshness and access controls as its sources.
- `markdown-alternate` is a typed, explicitly linked `text/markdown`
  alternative to a canonical page. Its media type and discovery link use
  [RFC 7763](https://www.rfc-editor.org/rfc/rfc7763.html) and
  [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288.html). It is recommended
  only where the site can generate a trustworthy source-equivalent view.
- `ai-crawler-guidance` is a logical specialization of RFC 9309. A site may
  target a product token only when that crawler's operator authoritatively
  documents the token. Generic invented AI groups or unsupported policy claims
  are invalid.

Emerging entries remain optional or recommended and therefore cannot block
publication by default.

### Experimental mechanisms

`ai-oriented-hints` permits a narrowly scoped metadata name or HTTP field only
when an identified consumer publishes its name, processing semantics, and
privacy expectations. The profile does not invent a universal AI-hint
vocabulary. HTML metadata extensions follow the
[WHATWG extension rules](https://html.spec.whatwg.org/multipage/semantics.html#other-metadata-names).

`cats-txt` records the intentionally satirical
[cats.txt draft](https://catstxt.org/docs/draft-catstxt-00/) at
`/.well-known/cats.txt` as an optional experiment. It is not a standards-track
or AI-interoperability requirement. Operators omit the file unless they choose
to maintain truthful, non-sensitive content, and its well-known path does not
override the registration rules in
[RFC 8615](https://www.rfc-editor.org/rfc/rfc8615.html).

Experimental entries are always optional in this profile and never satisfy an
established discovery requirement.

## Source-equivalent representation integrity

Markdown alternates and aggregate representations derive from a shared,
reviewed source. “Equivalent” means no material additions, omissions, or
changed claims; formatting and navigation may differ without changing meaning.
The human-facing HTML URL remains canonical.

A present representation must:

- identify its canonical source URI and the human-facing canonical URL;
- record the source revision, generator identity, and generation time;
- be generated from the same build or source revision as the canonical view;
- apply the same or stricter access control;
- exclude private, draft, hidden, internal, and privileged source material; and
- be removed or marked invalid when drift is detected rather than served stale.

These are publication-integrity rules, not permission to expose new content.
An efficient view cannot contain facts that a human with the same access could
not obtain from the canonical source.

## Deterministic content negotiation

An explicit alternate URI is preferred. If the canonical URI also negotiates
between HTML and Markdown, it follows this algorithm:

1. Treat `text/html` as the canonical default.
2. Evaluate `Accept` using HTTP semantics. Select `text/markdown` only when it
   has a positive effective quality value strictly greater than `text/html`.
3. Resolve ties and wildcard-only requests to `text/html`.
4. If Markdown is unavailable or unacceptable, return HTML when acceptable;
   return `406 Not Acceptable` when neither representation is acceptable.
5. Emit `Vary: Accept` whenever selection can vary and emit `Content-Location`
   with the explicit Markdown URI for negotiated Markdown.
6. Never select a representation by user-agent string.

The canonical page or its HTTP response links the Markdown URI with
`rel="alternate"; type="text/markdown"`; the alternate links back to the
human-facing canonical URL. Examples: `Accept: */*` selects HTML, equal HTML
and Markdown qualities select HTML, and a higher positive Markdown quality
selects Markdown.

## Compatibility and validation

The profile remains contract major v1. Checkpoint-1 mechanism records retain
their meaning and remain readable by the reference checker. Alpha.2 catalog
entries add a complete `artifact`, `applicability`, `content_rules`, and
`validation_rules` group. Supplying only part of that group is invalid.
Canonical alpha.2 entries must supply all four fields and explicit rules for
every site class.

Consumers pin the exact profile version or an immutable repository revision.
Unknown core values fail closed. Unknown namespaced extensions may be
preserved, but they do not affect core conformance or grant authority.

Validate the canonical source and synthetic compatibility fixtures with:

```bash
python3 tools/agent_ready_web.py validate-profile
python3 tools/agent_ready_web.py validate-fixtures
python3 -m unittest tests.test_agent_ready_web
```

Fixtures cover the checkpoint-1 base shape, a complete checkpoint-2 policy
record, and focused invalid cases. Reserved `example.com` locations are
synthetic test data, not claimed standards or implementations.

## Ownership boundary

Hygiene owns the profile, catalog meaning, schema, references, and reference
validation. Holon may later generate artifacts for new sites from an accepted
immutable pin. Relay may later provide reusable validation and publication
workflow execution. Pace may later propose reversible existing-site adoption.
Observatory may later report privacy-safe evidence. Store continues to own
separately reviewed transaction-domain semantics. None of those downstream
responsibilities moves into this checkpoint, and this repository does not
claim their adoption.

## Checkpoint boundary

This checkpoint closes only the discovery and efficient-representation work in
issue #51. It does not:

- define WebMCP, MCP-B, browser-agent capability, consent, audit, or revocation
  semantics assigned to #52;
- define advertising seller declarations or transaction-oriented commerce
  semantics;
- implement generators, shared workflows, fleet rollout, dashboards, site
  publication, or downstream conformance;
- activate the proposed profile, merge its pull request, or publish a release;
  or
- close parent issue #16.

Issue #52 remains the next blocked checkpoint and must not begin until the pull
request for #51 is reviewed and merged.
