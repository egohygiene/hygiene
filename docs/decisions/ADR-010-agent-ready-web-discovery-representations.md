---
schema: egohygiene.architecture-decision/v1
id: ADR-010
title: Specify Agent-Ready Web discovery and representations
status: proposed
date: 2026-09-14
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/51
pull_request: https://github.com/egohygiene/hygiene/pull/55
related:
  - ADR-0001
  - ADR-002
  - ADR-009
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
    url: https://github.com/egohygiene/hygiene/issues/51
    description: Reviewed checkpoint scope, requested mechanisms, representation semantics, exclusions, and acceptance criteria.
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/16
    description: Parent roadmap and ordered four-checkpoint dependency boundary.
  - type: external
    url: https://www.rfc-editor.org/rfc/rfc9110.html
    description: Primary HTTP semantics for deterministic proactive content negotiation and response metadata.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/55
    description: Focused review surface for the proposed checkpoint 2 catalog and representation policy.
exceptions: []
approval: null
---

# ADR-010: Specify Agent-Ready Web discovery and representations

## Context

ADR-009 and merged checkpoint #50 establish the proposed Agent-Ready Web v1
vocabulary, compatibility model, evidence shape, and ownership boundary. The
foundation intentionally registered no mechanisms. Issue #51 now requires a
bounded catalog of discovery artifacts and efficient representations before
interactive browser-agent capabilities can be considered.

The requested mechanisms have materially different authority and adoption.
Robots Exclusion and JSON-LD have formal standards; Sitemaps and EntityMap have
published specifications with different deployment evidence; `llms.txt` and
`llms-full.txt` are evolving conventions; and `cats.txt` is explicitly
satirical and experimental. Treating every named artifact as equally required
would turn registration into a false standards or adoption claim.

Alternate representations also create risks absent from a simple artifact
list. They can drift from canonical content, expose draft or privileged source
material, create ambiguous URLs, poison caches when negotiation is
underspecified, or show machine consumers claims unavailable to people. A
profile-aware applicability and truthful-absence rule is needed so sites do
not fabricate unsupported artifacts merely to pass a checklist.

## Decision

Propose `egohygiene.agent-ready-web-profile/v1` version `1.0.0-alpha.2` with a
closed checkpoint-2 catalog of twelve mechanisms: optional AI crawler
guidance, justified AI-oriented hints, canonical metadata, `cats.txt`,
EntityMap JSON and HTML, `llms-full.txt`, `llms.txt`, source-equivalent Markdown
alternates, `robots.txt`, XML Sitemaps, and discovery-oriented JSON-LD.

Every record declares its artifact locations and media types, an explicit
applicability condition, requirement strength for all five site classes,
content rules, validation rules, dated maturity, primary references,
registration evidence, and isolated extensions. Applicability is evaluated
before strength. Inapplicable and optional absence is valid, recommended
absence is advisory, required absence and prohibited presence are errors, and
fabricated placeholders are prohibited.

Established mechanisms may be required or recommended where applicable.
Published specifications remain governed by their evidence and conditions.
Emerging and experimental mechanisms may be optional or recommended but never
required in this proposal, so they cannot block publication by default.

The profile defines one representation-integrity policy for Markdown
alternates and aggregate machine views. A present alternate derives from the
same reviewed source revision as the canonical human page, makes no material
additions, omissions, or changed claims, records canonical URL and provenance,
uses the same or stricter access controls, excludes hidden or privileged
content, and is invalidated when it drifts.

When one URI can serve HTML or Markdown, HTTP `Accept` selection is
deterministic: HTML is the default; Markdown is selected only with a positive
effective quality strictly greater than HTML; ties and wildcard-only requests
select HTML; an unacceptable pair returns 406; varying responses emit
`Vary: Accept`; negotiated Markdown identifies its explicit URI using
`Content-Location`; and user-agent sniffing is prohibited. Canonical HTML and
Markdown alternates are connected by typed alternate and canonical links.

This decision assigns all twelve mechanisms only to readability or
efficiency. It does not define WebMCP or MCP-B capability semantics,
advertising declarations, seller relationships, offers, payments,
fulfillment, or transaction authority. Hygiene continues to own policy;
downstream generators, reusable workflows, rollout, reporting, and site
publication remain outside this checkpoint.

## Alternatives considered and rejected

### Require every named artifact on every site

Rejected because site purpose and mechanism applicability differ, and several
artifacts are proposals or experiments. Such a rule would reward fabricated
placeholder output and misrepresent maturity.

### Select Markdown by crawler or agent user-agent string

Rejected because user-agent lists drift, are easily spoofed, create hidden
behavior, and do not express representation preference. Typed alternate links
and RFC 9110 `Accept` semantics are explicit and cache-aware.

### Treat all public specifications as established standards

Rejected because publication proves that a proposal can be reviewed, not that
it has standards authority or broad interoperable adoption. The existing
maturity taxonomy records those distinctions.

### Defer privacy and drift rules to downstream generators

Rejected because a generator cannot safely invent the meaning of source
equivalence or decide whether hidden material may be exposed. Those are
canonical policy decisions; implementation remains downstream.

### Include capability and commerce fields for completeness

Rejected because issues #52 and later Store-owned work require separate
security, consent, and domain review. Discovery metadata must not become
implicit permission to act or transact.

## Consequences and tradeoffs

- Consumers gain a finite, versioned discovery catalog with deterministic
  applicability, site-class strength, content, validation, and reference data.
- Established mechanisms can produce actionable errors, while emerging and
  experimental mechanisms remain reviewable without becoming release gates.
- Truthful absence prevents conformance theater but requires validators to
  resolve applicability before checking presence.
- Source-equivalence and negotiation rules reduce drift, privacy, caching, and
  canonicalization ambiguity, at the cost of provenance and freshness checks
  for sites that choose alternates.
- Checkpoint-1 base mechanism records remain readable. Canonical alpha.2
  entries require the complete additive policy-field group, so partial upgrades
  fail closed.
- The proposed state permits review and pinned experiments but makes no claim
  that downstream sites have adopted or conform to the profile.

## Implementation and evidence links

The proposal is represented by the canonical
[`agent-ready-web-profile.json`](../../catalog/agent-ready-web-profile.json),
its [JSON Schema](../../schemas/agent-ready-web-profile.v1.schema.json), the
[human-readable profile](../ecosystem/AGENT_READY_WEB.md), synthetic
[compatibility fixtures](../../fixtures/agent-ready-web), the dependency-free
reference validator, and focused unit tests.

Each canonical record links its primary specifications or maintainer sources
and dated registration evidence. Issue #51 is the review authority, and
[PR #55](https://github.com/egohygiene/hygiene/pull/55) is the focused review
surface that merged this checkpoint. The decision lifecycle remains proposed.

## Replacement or exit strategy

Clarifications may evolve under an exact reviewed pin. Adding optional
mechanisms or vocabulary requires a compatible reviewed release only when it
does not change existing meaning. Removing or renaming a mechanism, changing
its concern, applicability, requirement strength, maturity meaning, or
representation integrity is breaking and requires a proposed successor plus
migration fixtures.

If this proposal is declined, downstream consumers must not infer policy from
the catalog or fixtures. No rollout needs reversal because the proposal does
not authorize generation, deployment, or publication.

## Follow-up work

PR #56 subsequently merged issue #52's guarded capability and commerce layer.
ADR-012 and issue #53 own final integration and conformance evidence. Parent
#16 remains open until that final checkpoint merges; lifecycle promotion,
release, and downstream implementation or adoption remain separate.
