# Agent-Ready Web integrated profile and conformance contract

Status: **proposed `1.0.0-alpha.4`**

Policy owner: `egohygiene/hygiene`

Tracked by: [hygiene#53](https://github.com/egohygiene/hygiene/issues/53),
checkpoint 4 of [hygiene#16](https://github.com/egohygiene/hygiene/issues/16)

## Purpose and authority

The Agent-Ready Web profile defines how an Ego Hygiene website can remain an
excellent human-facing experience while exposing explicit, efficient, and safe
machine-readable surfaces. Checkpoints 1–3 established the vocabulary,
discovery and representation records, guarded browser-capability publication,
descriptive Product and Offer metadata, and truthful advertising declarations.
This final checkpoint composes those independent layers into one deterministic
conformance and compatibility contract without allowing one layer to satisfy
or authorize another. It does not implement a consumer, browser tool, or
transaction contract.

The canonical machine source is
[`catalog/agent-ready-web-profile.json`](../../catalog/agent-ready-web-profile.json),
validated against
[`schemas/agent-ready-web-profile.v1.schema.json`](../../schemas/agent-ready-web-profile.v1.schema.json).
Site-owned assessment evidence uses
[`schemas/agent-ready-web-conformance.v1.schema.json`](../../schemas/agent-ready-web-conformance.v1.schema.json).
This guide explains that policy but does not override it. The profile remains
proposed: “consumer-ready” means the schema, fixtures, pinning rules, and
handoffs are reviewable. It does not mean accepted, released, deployed,
adopted, published, or actively enforced.

## Contract identity

| Field | Value |
| --- | --- |
| Contract | `egohygiene.agent-ready-web-profile/v1` |
| Profile version | `1.0.0-alpha.4` |
| Status | `proposed` |
| Canonical owner | `egohygiene/hygiene` |
| Consumer pin | Exact semantic version or immutable repository revision |
| Catalog scope | Discovery, representations, guarded capability publication, non-executable commerce descriptions, and deterministic conformance evidence |

The four independent concerns, five stable site classes, five requirement
strengths, and four maturity levels defined by checkpoint 1 remain unchanged.
Each mechanism still has exactly one primary concern. Concern assignment does
not transfer authority across boundaries: discovery metadata cannot authorize
a capability, commerce metadata cannot authorize a purchase, and advertising
declarations cannot authorize a commerce action.

## Integrated boundary invariants

The profile is coherent because all four concerns use one version, one site
classification, one applicability pass, one evidence envelope, and one
deterministic aggregate. Their meanings remain separate. The evaluator
resolves each mechanism within its single primary concern and only then
aggregates diagnostics; a mechanism from one concern cannot substitute for a
mechanism in another.

The profile schema and conformance evidence schema enforce these negative
authority assertions:

| Surface or hint | It can describe | It can never grant |
| --- | --- | --- |
| Discovery | Public locations and representations | Capability, consent, authorization, or transaction authority |
| Structured metadata | Visible public facts and descriptive actions | Capability, consent, authorization, or transaction authority |
| Advertising declaration | A current seller relationship or exact IAB no-seller sentinel | Capability, consent, authorization, or transaction authority |
| Maturity label | The reviewed stability of a mechanism | Capability, consent, authorization, or transaction authority |

A capability exists only through an explicit, versioned, origin-bound
capability contract. Consent comes only from fresh explicit human interaction;
authorization is revalidated by the server for each invocation. A transaction
also needs a Store-owned contract, fresh confirmation, and server-side
authorization. A conformance record must state every corresponding authority
assertion as `false`; changing one to `true` invalidates the record rather than
changing profile meaning.

## Resolution and truthful absence

Applicability is resolved before requirement strength. A validator first asks
whether the mechanism's explicit condition is true for the site and only then
applies the site-class rule.

| Input state | Deterministic resolution |
| --- | --- |
| Applicability unknown | `unresolved`, error `ARW-APP-001` |
| Not applicable and absent | `inapplicable`, no requirement diagnostic |
| Not applicable and present | `inapplicable`, error `ARW-APP-002` |
| Required and absent | `required`, error `ARW-REQ-001` |
| Recommended and absent | `recommended`, advisory `ARW-REC-001` |
| Optional and absent | `optional`, no diagnostic |
| Conditional and condition met | `required` |
| Conditional and condition not met | `inapplicable` |
| Conditional and condition unknown | `unresolved`, error `ARW-CND-001` |
| Prohibited and present | `prohibited`, error `ARW-PRO-001` |
| Present without evidence | error `ARW-EVD-001` |
| Present without complete validation | error `ARW-VAL-001` |
| Experimental and absent | Non-blocking |
| Experimental and present | Full validation plus information `ARW-EXP-001`; no authority |
| Valid narrow exemption | information `ARW-EXM-001` and distinct `exempt` level; never passing |

An inapplicable or unsupported artifact must be absent. Empty files, invented
entities, placeholder links, permissive claims, and stale generated output do
not satisfy a requirement. Evidence can explain why a recommendation was not
implemented. A narrowly approved required-absence exemption can produce only
the distinct `exempt` level; it cannot turn the omission into a pass.

Every catalog record declares an applicability condition, a default strength,
and an explicit override for all five site classes. That makes resolution
deterministic and prevents a consumer from treating a missing override as an
implicit requirement.

### Conformance levels and precedence

Levels are derived, never asserted by a consumer:

1. `nonconformant`: one or more errors remain.
2. `exempt`: no unexempted error remains and at least one valid exemption is
   active. This is not a passing level.
3. `baseline`: no error or exemption remains, but one or more advisories remain.
4. `recommended`: no error, advisory, or exemption remains. Optional and
   experimental absence is still allowed.

The order above is strict precedence. Information diagnostics do not lower a
level. An exemption applies to one required absence only and needs a named
owner, reason, approving party, approval evidence, approval date, and future
expiry. Profile pins, unknown applicability, prohibited presence, validation
of present mechanisms, and privacy, security, consent, authorization,
transaction, or cross-layer rules are never exemptable.

### Evidence envelope

Every assessment binds to the exact profile schema and version, canonical
repository path, resolved full revision, and SHA-256 digest. It also binds to
one HTTPS origin, one site class, and the immutable revision represented by the
site evidence. The assessment covers every profile mechanism exactly once in
profile order. Each mechanism records applicability evidence, declared and
resolved strength, presence, validation result, implementation evidence, and
an optional narrow exemption. Evidence IDs are unique and stable; observations
record time, subject revision, type, location, description, and optional
digest.

The profile digest is SHA-256 over UTF-8 canonical JSON with object keys sorted,
no insignificant whitespace, and non-ASCII characters retained. The reference
validator derives that digest from the loaded profile and rejects a mismatch;
the resolved revision identifies where the consumer obtained those verified
bytes.

Evidence must be allowlisted and minimized. It contains no secret, credential,
personal data, fabricated implementation result, or inferred relationship.
Diagnostics have stable code, severity, mechanism ID, path, and message fields
in profile order. The fixed claim string says the record is an assessment only,
not certification, adoption, publication, or authority.

## Mechanism catalog

Strength abbreviations are `R` required, `A` recommended (advisory when
absent), and `O` optional. They apply only after the applicability condition is
true.

| Mechanism | Concern | Maturity | Applicability condition | App | Commerce | Content | Docs | Hybrid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ads-txt` | commerce | established | Web inventory has real programmatic seller relationships or an intentional IAB no-seller declaration | R | R | R | R | R |
| `ai-crawler-guidance` | readability | emerging | Identified crawler operator publishes authoritative product-token policy | O | O | O | O | O |
| `ai-oriented-hints` | readability | experimental | Identified consumer owns a public hint specification | O | O | O | O | O |
| `app-ads-txt` | commerce | established | Distributed app inventory resolves through a verified developer domain or an intentional IAB no-seller declaration | R | R | R | R | R |
| `canonical-metadata` | readability | established | Page is public/indexable or duplicates an equivalent URL | R | R | R | R | R |
| `cats-txt` | readability | experimental | Operator intentionally maintains a truthful cats file | O | O | O | O | O |
| `commerce-product-offer-jsonld` | commerce | established | A visible real product or offer has current authoritative facts | O | A | O | O | A |
| `entitymap-html` | readability | published specification | A conforming `entitymap.json` is published | R | R | R | R | R |
| `entitymap-json` | readability | published specification | A source-backed public entity index can be maintained | O | O | O | O | O |
| `llms-full-txt` | efficiency | emerging | A bounded public documentation corpus can be aggregated safely | O | O | O | O | O |
| `llms-txt` | readability | emerging | Curated public AI-readable content benefits from an index | O | O | A | A | A |
| `markdown-alternate` | efficiency | emerging | A current public source-equivalent can be maintained | O | O | A | A | A |
| `mcp-b-runtime` | capability | experimental | The site deliberately uses and can immutably pin an MCP-B runtime or bridge | O | O | O | O | O |
| `robots-txt` | readability | established | A public HTTP origin exposes crawlable resources | R | R | R | R | R |
| `sitemap-xml` | readability | established | A truthful public indexable URL set exists | A | R | R | R | R |
| `structured-discovery-jsonld` | readability | established | Stable vocabulary describes visible public facts | A | A | A | A | A |
| `webmcp-tools` | capability | experimental | The active document deliberately registers a guarded compatible WebMCP tool | O | O | O | O | O |

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

### Authoritative-reference and maturity review

The `reference_review` record binds the 2026-09-14 review to every registered
mechanism in catalog order. Each mechanism retains at least one resolvable
primary authority, and each maturity rationale cites a primary source. The
review retained the classifications rather than promoting them: WebMCP remains
a 2026-09-10 Community Group draft and experimental; MCP-B remains an
experimental implementation; EntityMap v1.0 remains a published industry
specification; llms.txt, `/llms-full.txt`, Markdown alternates, and AI crawler
guidance remain emerging; and cats.txt and AI-oriented hints remain
experimental. The established entries remain anchored in the cited RFC, W3C,
Sitemaps, Schema.org, or IAB primary material.

Living, community-draft, and implementation sources must be checked again on
every profile-pin upgrade. A changed source does not silently change the
meaning of an immutable pin.

## Guarded browser capabilities

`webmcp-tools` covers the current
[WebMCP Community Group draft](https://webmachinelearning.github.io/webmcp/)
surface at `document.modelContext`. A Community Group report is not a W3C
Standard and is not on the W3C standards track. `mcp-b-runtime` covers the
independent [MCP-B implementation and bridge](https://docs.mcp-b.ai/explanation/what-is-webmcp).
MCP-B is neither W3C WebMCP nor an official Model Context Protocol authority.
Both mechanisms are experimental, optional for every site class, and
non-blocking when absent. When present, however, every guard below is required.

| Contract element | Required behavior |
| --- | --- |
| Identity | Stable capability ID bound to the active secure exact origin |
| Protocol | Exact version or immutable revision, with an exact implementation pin |
| Discovery | Protocol-native active-document tool list plus origin-bound contract evidence |
| Input | Independently versioned JSON Schema and runtime validation |
| Output | Independently versioned JSON Schema and runtime validation, even when a draft API has no native output-schema field |
| Compatibility | A breaking input, output, effect, or permission change receives a new capability major |
| Unknown or stale data | Fail closed and do not invoke |

Every tool is classified as `read-only` or `state-changing`; an unclassified
tool is treated as state-changing and denied. Read-only tools cannot produce
state effects. Access to or disclosure of sensitive data still needs explicit
permission, informed consent, and confirmation before disclosure.
State-changing tools declare all possible effects before consent and use
operation-scoped permission. A consequential or irreversible effect requires
fresh human confirmation immediately before execution. No automatic retry is
permitted without an idempotency guarantee or a new confirmation.

Tool names, descriptions, schemas, annotations such as `readOnlyHint`, inputs,
and outputs are untrusted data, never authority. Present exposure also requires:

- explicit, specific, revocable permission and informed consent before use;
- least-privilege data scope and duration, data minimization, and exact-origin
  binding, including applicable Permissions Policy constraints;
- authentication whenever the human interface requires it and server-side
  authorization revalidation on every call;
- no token passthrough and no credentials or secrets in schema, description,
  input, or output material; and
- prompt-injection defenses that do not trust tool-controlled content.

Each invocation records provenance for the capability, version, origin, actor,
and input/output contract digests. Audit records cover the decision,
confirmation, invocation, and result without exposing secrets. Correlation,
status, latency, and redacted errors support observability. Permission and
consent expire explicitly and revocation takes effect before the next call.
Replay protection binds a nonce or idempotency key to actor, origin, action,
and expiry, and declared limits are enforced per actor, origin, and capability.

Timeouts are bounded and cancelable. The default failure performs no state
change. A partial failure reports observed effects and never invents rollback;
the user receives a visible resume or compensating path. These are publication
requirements for a declared tool contract, not an implementation of the tool
or a claim that any browser supports it.

## Descriptive commerce and advertising

`commerce-product-offer-jsonld` uses
[JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) and Schema.org
[`Product`](https://schema.org/Product) and
[`Offer`](https://schema.org/Offer) to describe current facts already visible
on the canonical human-facing page. Product identity, identifiers, variants,
seller, price, currency, availability, validity, eligibility, condition, and
URLs are published only when current and source-backed. A seller is explicit
and evidenced or omitted—never inferred. `potentialAction`, an `Offer`, a URL,
or an `EntryPoint` remains descriptive and grants no consent, permission,
executable endpoint contract, purchase authority, or proof of transaction.

Any future guarded commerce action is a `state-changing` capability and must
reference a separately reviewed, versioned contract owned by
`egohygiene/store`. Without that Store contract, the action is neither exposed
nor invoked. The capability policy's authority, fresh-confirmation, audit,
replay, rate-limit, and failure rules remain the outer safety envelope; this
profile does not define cart, checkout, payment, inventory, fulfillment,
refund, or other transaction-domain semantics.

`ads-txt` and `app-ads-txt` are applicable only when a publisher has actual
programmatic advertising inventory relationships or deliberately publishes
the exact IAB no-seller declaration. Once applicable, the artifact is required
regardless of site class. Records follow the cited IAB Tech Lab specifications:

- seller account IDs and `DIRECT` or `RESELLER` values match current contract
  evidence; owner, manager, and partner domains match documented relationships;
- `app-ads.txt` follows the verified app-store listing to the developer domain;
- no seller, reseller, account, certification authority, domain, or
  authorization relationship is invented; and
- a site with no applicable relationship records not-applicable evidence and
  omits the artifact, or uses the exact IAB reserved no-seller placeholder.
  That placeholder is a sentinel only and never represents a seller.

Advertising authorization cannot be inferred into commerce action authority,
and descriptive offers cannot be inferred into browser capability authority.

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
Alpha.3 preserves that group and adds an exact `capability` binding to
capability records and an exact `commerce` binding to commerce records. A
binding on another concern, a missing binding, a floating implementation,
unversioned contract, or executable authority inferred from commerce metadata
fails closed. Alpha.4 adds the integrated boundary policy, conformance evidence
schema, deterministic resolver and diagnostics, reference review, and precise
consumer-resolution rules. Canonical entries still supply explicit rules for
every site class.

Consumers resolve policy directly from `egohygiene/hygiene` at
`catalog/agent-ready-web-profile.json`; they do not copy or reinterpret Hygiene
policy. A supported pin is either an exact released semantic version with its
resolved immutable revision and canonical-JSON SHA-256 digest, or an immutable
repository revision with that digest. An unknown version, digest mismatch, missing
revision, floating branch, or unknown core value fails closed with an upgrade
diagnostic. Unknown namespaced extensions may be preserved, but they do not
affect core conformance or grant authority.

An upgrade is an explicit reviewed pin change followed by full profile
validation, replay of the compatibility fixtures, and full revalidation of the
site evidence. A downgrade is also explicit and reviewed, and the consumer
must not assume semantics introduced by the newer pin. Because this profile is
`proposed`, its pins are eligible only for review and compatibility testing.
Production generation or enforcement requires an `active` lifecycle and an
otherwise eligible immutable pin; this document supplies neither.

Validate the canonical source and synthetic compatibility fixtures with:

```bash
python3 tools/agent_ready_web.py validate-profile
python3 tools/agent_ready_web.py validate-fixtures
python3 tools/agent_ready_web.py validate-conformance --input <site-evidence.json>
python3 -m unittest tests.test_agent_ready_web
```

Fixtures cover the checkpoint-1 base shape, a complete checkpoint-2 policy
record, complete checkpoint-3 capability and commerce bindings, and focused
invalid pinning and authority cases. Five whole-profile fixtures cover
application, commerce, content, documentation, and hybrid sites. Their
`.invalid` origins, placeholder revisions, digests, observations, and outcomes
are explicitly synthetic compatibility data—not evidence about any real site,
standard implementation, adoption, publication, or downstream state.

## Ownership boundary

| Consumer | Exact handoff | Explicitly retained boundary |
| --- | --- | --- |
| Hygiene | Own the profile, lifecycle, schema, conformance semantics, compatibility, and reference review | No generation, workflow execution, rollout, transaction contract, metrics dashboard, credentials, or publication |
| Holon | Deterministically scaffold and generate for new sites from an eligible immutable profile pin | No profile semantics or lifecycle, existing-site adoption, site facts, credentials, consent, reusable publication workflow, or final publication authority |
| Relay | Provide reusable validation and publication workflows and transport privacy-safe evidence for eligible pins | No profile semantics or lifecycle, site-class decision, adoption policy, transaction semantics, credentials, or final publication decision |
| Pace | Plan reviewed adoption, preview rollout, open reversible migration pull requests, and drive convergence after eligibility | No direct default-branch mutation, profile policy or lifecycle, generator or workflow implementation, or automatic adoption claim |
| Store | Define separately reviewed transaction-domain capability semantics and versioned guarded action contracts | No core-profile ownership, descriptive metadata policy, fabricated seller relationship, credential, consent, or metadata-derived authorization |
| Observatory | Collect and report allowlisted privacy-safe evidence and aggregate metrics for eligible pins | No policy, lifecycle, remediation, rollout, secrets or personal data, passing-state fabrication, or site mutation |
| Individual sites | Supply truthful facts, site class, credentials, consent interaction, configuration, represented revision, and final publication authority | No policy rewrite, lifecycle promotion, evidence or relationship fabrication, or authority delegated to discovery surfaces |

None of these handoffs is implemented or claimed adopted here.

### Precise handoff to `egohygiene/holon#7`

[Holon issue #7](https://github.com/egohygiene/holon/issues/7) may consume this
contract later; this checkpoint does not implement or change that issue. Its
safe implementation boundary is:

1. Require a profile pin eligible under Hygiene lifecycle policy, resolve the
   canonical path at that full revision, verify its digest, and reject a
   floating or unsupported pin. The current `proposed` alpha.4 profile is not
   production-eligible.
2. Accept site-owned site class, public facts, local configuration, target
   revision, and explicit applicability decisions as inputs. Never invent
   relationships, capability support, credentials, consent, authorization,
   evidence, exemptions, or a passing result.
3. Resolve each registered mechanism with the canonical policy and generate or
   scaffold only the eligible artifact set. Preserve concern boundaries and
   record generator identity, profile pin, source revision, and output digests.
4. Emit reviewable output for site authority and later Relay validation. Do not
   publish, mutate an existing fleet, or claim conformance, adoption, release,
   deployment, monitoring, or publication.
5. Treat `humans.txt`, mentioned by Holon #7, as outside the current Agent-Ready
   Web mechanism catalog. It cannot satisfy this profile or count toward its
   conformance unless separately registered by reviewed Hygiene policy.

## Checkpoint boundary

This review checkpoint is scoped to issue #53 only. It does not:

- add mechanisms beyond the bounded catalog or define application-specific
  WebMCP/MCP-B capability details;
- implement browser tools, transaction operations, Store-owned cart, checkout,
  payment, inventory, fulfillment, refund, or other commerce-domain contracts;
- implement Holon generation, Relay workflows, Pace rollout, Observatory
  dashboards, site publication, or any downstream consumer state;
- activate the proposed profile, merge its pull request, or publish a release;
- certify any site, create real evidence or exemptions, or claim organization-
  wide adoption, enforcement, monitoring, deployment, or publication; or
- merge this checkpoint pull request.

The parent tracker may close only when checkpoints #50–#52 are verified closed
by merged pull requests and every parent acceptance criterion is evidenced by
this final checkpoint. Tracker checkboxes alone are not merge evidence.
