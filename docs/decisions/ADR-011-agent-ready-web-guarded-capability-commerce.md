---
schema: egohygiene.architecture-decision/v1
id: ADR-011
title: Guard Agent-Ready Web capability and commerce publication
status: proposed
date: 2026-09-14
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/52
pull_request: https://github.com/egohygiene/hygiene/pull/56
related:
  - ADR-0001
  - ADR-002
  - ADR-009
  - ADR-010
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
  - egohygiene/holon
  - egohygiene/relay
  - egohygiene/pace
  - egohygiene/store
  - egohygiene/observatory
affected_contracts:
  - egohygiene.agent-ready-web-profile/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/52
    description: Reviewed checkpoint scope, capability safeguards, commerce boundaries, exclusions, and acceptance criteria.
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/16
    description: Parent roadmap and ordered four-checkpoint dependency boundary.
  - type: external
    url: https://webmachinelearning.github.io/webmcp/
    description: Primary current WebMCP Community Group draft, including document.modelContext tool registration and non-standards-track status.
  - type: external
    url: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
    description: Primary current Model Context Protocol tool contract and safety guidance.
  - type: external
    url: https://docs.mcp-b.ai/explanation/what-is-webmcp
    description: MCP-B maintainer documentation distinguishing its independent implementation from WebMCP and MCP authority.
  - type: external
    url: https://www.w3.org/TR/json-ld11/
    description: W3C Recommendation defining JSON-LD 1.1 syntax and processing.
  - type: external
    url: https://iabtechlab.com/ads-txt/
    description: IAB Tech Lab primary publication and specification index for ads.txt and app-ads.txt.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/56
    description: Focused review surface for the proposed checkpoint 3 capability and commerce policy.
exceptions: []
approval: null
---

# ADR-011: Guard Agent-Ready Web capability and commerce publication

## Context

ADR-009 and merged checkpoint #50 establish the proposed Agent-Ready Web v1
vocabulary and ownership boundary. ADR-010 and merged checkpoint #51 add the
bounded discovery and source-equivalent representation catalog. Issue #52 now
requires a policy foundation for browser-agent capabilities and commercially
descriptive surfaces without implementing either browser tools or transaction
semantics.

The cited technologies carry different authority. WebMCP is a current W3C
Community Group draft report, not a W3C Standard. MCP-B is an independent
implementation and bridge, not WebMCP governance or official Model Context
Protocol authority. Tool annotations are descriptive hints and can be false or
stale. Treating a tool name, schema, `readOnlyHint`, origin, or successful call
as authorization would permit confused-deputy, cross-origin, replay,
over-privilege, and irreversible-action failures.

Commerce publication has a parallel inference risk. Schema.org Product and
Offer terms describe things and offers but do not authorize a purchase.
`ads.txt` and `app-ads.txt` represent real advertising account relationships;
invented seller IDs, reseller status, domains, or placeholders would publish
false authorization. Hygiene can define these publication boundaries, but
Store owns cart, checkout, payment, inventory, fulfillment, refund, and other
transaction-domain contracts.

## Decision

Propose `egohygiene.agent-ready-web-profile/v1` version `1.0.0-alpha.3`. Keep
the lifecycle `proposed` and add only the checkpoint-3 capability and commerce
policy foundation to the previously merged catalog.

WebMCP and MCP-B publication records are `experimental` and optional for every
site class. Their absence is non-blocking. When either is present, the record
identifies the exact protocol revision, exact package or immutable
implementation revision, stable origin-bound capability identity, active
authorized discovery surface, independently versioned input and output JSON
Schemas, runtime validation, and compatibility behavior. A breaking input,
output, effect, or permission change requires a new capability major. Unknown
or stale contracts fail closed.

Every capability is classified as `read-only` or `state-changing`.
Unclassified tools are treated as state-changing and denied. Read-only tools
cannot change state; sensitive access or disclosure still requires explicit
permission, informed consent, and confirmation. State-changing tools declare
effects before consent, use operation-scoped permission, and obtain fresh
human confirmation before consequential or irreversible effects. Unsafe
automatic retry is prohibited.

Present exposure binds to the active secure exact origin and applicable
Permissions Policy, minimizes data and duration, revalidates authorization on
every invocation, and passes no bearer token or secret through tool material.
Tool-controlled metadata, inputs, and outputs remain untrusted. Invocation
evidence covers provenance, tamper-evident audit, observability, revocation,
expiry, replay protection, and declared rate limits. Timeouts are bounded and
cancelable. Default failure changes no state; partial failure reports observed
effects without claiming rollback and gives the human a visible recovery path.

Product and Offer JSON-LD remains source-backed descriptive metadata in parity
with the canonical human page. Seller, price, currency, availability,
eligibility, validity, and identifiers are explicit and current or omitted.
Product, Offer, `potentialAction`, URL, and EntryPoint data grants no consent,
permission, endpoint contract, purchase authority, or transaction evidence.

Any future commerce action is a state-changing capability and requires a
separately reviewed, versioned Store-owned contract in addition to the profile
safety envelope. Without that contract, the action is not exposed or invoked.
This decision does not define the Store contract.

`ads.txt` and `app-ads.txt` apply only to real programmatic inventory
relationships or an intentional exact IAB no-seller declaration. When
applicable they are required, independent of site class. Seller account,
`DIRECT` or `RESELLER` classification, certification authority, owner/manager,
partner domain, app-store listing, and developer-domain claims require current
evidence. Inapplicable absence is valid. The reserved no-seller placeholder is
a sentinel, never a seller relationship. Fabricated relationships are
prohibited.

## Alternatives considered and rejected

### Treat WebMCP annotations as authority

Rejected because annotations are untrusted hints. They cannot establish
identity, origin, permission, consent, effect class, or server authorization.

### Make experimental browser capabilities a conformance requirement

Rejected because WebMCP and MCP-B remain experimental and implementation
support is unsettled. Optional absence is truthful; present unsafe exposure is
still an error.

### Infer executable actions from Product, Offer, or potentialAction

Rejected because descriptive semantic vocabulary is not a versioned operation
contract, user confirmation, authorization decision, or proof of transaction.

### Generate advertising placeholders for sites without relationships

Rejected because fabricated seller or account relationships are false. Safe
absence or the exact IAB no-seller sentinel expresses the real state.

### Define commerce-domain contracts in Hygiene

Rejected because contract semantics belong with their capability owner. Store
retains transaction behavior while Hygiene defines only the outer publication
and browser-agent safety boundary.

## Consequences and tradeoffs

- Consumers gain machine-readable distinctions between discovery,
  capability, descriptive commerce, advertising authorization, and transaction
  authority.
- Browser tool experimentation remains possible under an exact pin, while the
  stricter envelope adds schema, confirmation, authorization, evidence,
  lifecycle, and failure-handling work.
- Read-only classification cannot bypass sensitive-data consent and
  confirmation, and state-changing behavior cannot rely on descriptive hints.
- Sites must maintain current commercial facts and relationship evidence or
  omit inapplicable surfaces; this prevents conformance theater at the cost of
  explicit applicability records.
- Store and site owners retain their respective domain and publication
  authority. This repository makes no claim of downstream implementation,
  deployment, conformance, or adoption.
- Checkpoint-1 base fixtures and checkpoint-2 catalog shapes remain readable;
  checkpoint-3 capability and commerce records require their concern-specific
  bindings and fail closed when incomplete.

## Implementation and evidence links

The proposal is represented by the canonical
[`agent-ready-web-profile.json`](../../catalog/agent-ready-web-profile.json),
its [JSON Schema](../../schemas/agent-ready-web-profile.v1.schema.json), the
[human-readable profile](../ecosystem/AGENT_READY_WEB.md), synthetic
[compatibility fixtures](../../fixtures/agent-ready-web), the dependency-free
reference validator, and focused unit tests.

The canonical records link the primary WebMCP, Model Context Protocol, MCP-B,
JSON-LD, Schema.org, ads.txt, and app-ads.txt sources used to assess maturity
and boundaries. Issue #52 is the review authority. The focused change is
[PR #56](https://github.com/egohygiene/hygiene/pull/56), which merged on
2026-09-14; no automatic pull-request CI evidence was recorded. The decision
lifecycle remains proposed.

## Replacement or exit strategy

Consumers pin the exact proposed profile version or an immutable repository
revision. A later standards or implementation revision can be added through a
reviewed compatible release when it preserves existing meaning. A change to
capability identity, contracts, effects, permissions, commerce authority,
advertising relationship meaning, lifecycle, or ownership is breaking and
requires migration under the versioning policy. Unsupported experimental
exposure can be removed without fabricating a substitute.

## Follow-up work

[Issue #53](https://github.com/egohygiene/hygiene/issues/53) and ADR-012 now own
the final integration and conformance contract. Parent #16 remains open until
that final checkpoint merges. Browser tools, transaction contracts, generators,
reusable workflows, fleet rollout, publication, dashboards, release activity,
and downstream adoption remain outside this decision.
