---
schema: egohygiene.architecture-decision/v1
id: ADR-012
title: Integrate Agent-Ready Web conformance without collapsing authority
status: proposed
date: 2026-09-14
decision_scope: organization
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/53
pull_request: https://github.com/egohygiene/hygiene/pull/57
related:
  - ADR-0001
  - ADR-002
  - ADR-009
  - ADR-010
  - ADR-011
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
  - egohygiene.agent-ready-web-conformance/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/53
    description: Authoritative final-checkpoint integration, conformance, compatibility, reference-review, handoff, and exclusion scope.
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/16
    description: Parent roadmap and acceptance criteria, with stale checklist state reconciled against live merged pull requests.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/54
    description: Merged checkpoint 1 foundation evidence for closed issue 50.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/55
    description: Merged checkpoint 2 discovery and representation evidence for closed issue 51.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/56
    description: Merged checkpoint 3 guarded capability and commerce evidence for closed issue 52.
  - type: issue
    url: https://github.com/egohygiene/holon/issues/7
    description: Downstream generator request inspected for a precise handoff only; no Holon work is implemented or claimed.
  - type: external
    url: https://webmachinelearning.github.io/webmcp/
    description: Current 2026-09-10 WebMCP Community Group draft and explicit non-standards-track status.
  - type: external
    url: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
    description: Current primary Model Context Protocol tool contract and safety guidance.
  - type: external
    url: https://www.entitymap.org/spec/v1.0
    description: Current stable EntityMap v1.0 primary specification.
  - type: external
    url: https://llmstxt.org/
    description: Current llms.txt v2 community proposal used without overstating maturity.
  - type: external
    url: https://iabtechlab.com/ads-txt/
    description: Current IAB Tech Lab primary specification index for ads.txt and app-ads.txt.
exceptions: []
approval: null
---

# ADR-012: Integrate Agent-Ready Web conformance without collapsing authority

## Context

ADR-009 through ADR-011 and merged pull requests #54 through #56 establish the
proposed profile foundation, discovery and representation catalog, and guarded
capability and commerce policy. The final checkpoint must make that profile
deterministically consumable as one version without allowing readability,
efficiency, capability, or commerce mechanisms to substitute for one another.

The principal risk is authority laundering. Discovery or structured metadata
can make a surface easy to find, an advertising declaration can describe a
seller relationship, and a maturity label can describe review status. None can
create a capability, consent, authorization, or transaction authority. A
consumer also needs a stable way to resolve applicability, conditional rules,
strengths, exemptions, evidence, diagnostics, levels, and upgrades without
copying Hygiene policy.

Live checkpoint inspection on 2026-09-14 verified that issues #50, #51, and #52
were closed by merged pull requests #54, #55, and #56. The parent #16 body still
showed stale unchecked child boxes and the tracker had been closed while #53
remained open. This decision treats live issue and merged-pull-request state as
evidence and requires visible tracker reconciliation rather than inferring
completion from either stale markdown or premature closure.

## Decision

Propose `egohygiene.agent-ready-web-profile/v1` version `1.0.0-alpha.4` and keep
its lifecycle `proposed`. “Consumer-ready” means the contract can be resolved,
validated, fixture-tested, and reviewed; it does not mean accepted, released,
deployed, adopted, published, monitored, or enforced.

Resolve every mechanism inside its exactly one primary concern, then aggregate
diagnostics. Cross-concern substitution is prohibited. The profile and
conformance schemas state that discovery, structured metadata, advertising
declarations, and maturity classifications cannot grant capability, consent,
authorization, or transaction authority. Capability comes only from an
explicit versioned origin-bound contract; consent from fresh explicit human
interaction; authorization from server revalidation per invocation; and a
transaction from a Store-owned contract plus fresh confirmation and server
authorization.

Introduce `egohygiene.agent-ready-web-conformance/v1`. Each evidence record
binds to the canonical profile schema, version, path, full resolved revision,
and SHA-256 digest; one site class and HTTPS origin; an immutable represented
site revision; assessment identity and time; minimized evidence; and exactly
one assessment per profile mechanism in profile order. Fixed negative authority
assertions are required. The evidence is an assessment only and cannot claim
certification, adoption, publication, or authority.

Applicability resolves before strength. Unknown applicability is an error;
not-applicable resolves to `inapplicable`; conditional `met`, `not-met`, and
`unknown` resolve to `required`, `inapplicable`, and `unresolved` respectively.
Required absence, prohibited presence, inapplicable presence, missing evidence
for a present mechanism, and incomplete present-mechanism validation are
errors. Recommended absence is advisory. Optional absence is allowed.
Experimental absence is non-blocking; a present experiment must pass its full
rules and still grants no authority.

Derive four levels in strict precedence: `nonconformant`, `exempt`, `baseline`,
and `recommended`. An exemption is narrow, time-bounded, owner- and
approval-evidenced, and applies only to one required absence. It always yields
the distinct non-passing `exempt` level. Pins, unknown applicability,
prohibited presence, present validation, and privacy, security, consent,
authorization, transaction, or cross-layer invariants cannot be exempted.
Stable diagnostics contain code, severity, mechanism, path, and message.

Consumers resolve the canonical Hygiene path without copying policy. Supported
pins are an exact released version with resolved revision and digest, or an
immutable repository revision with digest. Unknown or mismatched pins fail
closed. Upgrade and downgrade are explicit reviewed pin changes; upgrade
replays all fixtures and revalidates all site evidence, while downgrade assumes
no newer semantics. A proposed pin is review- and compatibility-test-only;
production eligibility requires an active lifecycle plus an eligible immutable
pin.

Five explicitly synthetic fixtures cover application, commerce, content,
documentation, and hybrid sites across the complete mechanism list. Focused
tests exercise every requirement state, conditional resolution, level,
exemption boundary, authority invariant, pin, evidence reference, and derived
diagnostic behavior. Synthetic observations and placeholder revisions are not
real site evidence.

The consumer handoff is exact and non-overlapping:

- Holon may later perform deterministic scaffolding and generation for new
  sites from an eligible immutable pin. It receives site-owned facts and
  configuration and never invents evidence, credentials, consent, authority,
  exemptions, or passing state.
- Relay may later implement reusable validation and publication workflows and
  evidence transport.
- Pace may later own reviewed adoption planning, rollout, migration pull
  requests, and convergence for existing sites.
- Store retains transaction-domain capability semantics and guarded action
  contracts.
- Observatory may later collect privacy-safe evidence and aggregate metrics.
- Each individual site retains its facts, credentials, consent interaction,
  configuration, represented revision, and final publication authority.

For `egohygiene/holon#7`, Holon must resolve and verify an eligible canonical
pin, accept site-owned inputs, generate only resolved artifacts with provenance,
and hand reviewable output to site authority and later Relay validation. It
must fail closed on a proposed production pin and make no conformance or
publication claim. `humans.txt` is outside the current profile catalog and
cannot satisfy profile conformance without a separately reviewed Hygiene
registration. This is a handoff only; no Holon repository or issue is changed.

## Alternatives considered and rejected

### Collapse all concerns into one checklist

Rejected because a readability artifact could then appear to satisfy a
capability or commerce obligation and blur ownership and authority.

### Let metadata, advertising, or maturity imply authority

Rejected because descriptive and review surfaces cannot supply capability
identity, human consent, server authorization, or a transaction contract.

### Let each consumer copy and interpret the policy

Rejected because copies drift and make version pinning, diagnostics, upgrades,
and cross-consumer comparison nondeterministic.

### Treat exemptions as passing

Rejected because an approved required omission remains a material gap. A
distinct level preserves the decision without fabricating conformance.

### Activate or publish the profile with this checkpoint

Rejected because no explicit maintainer lifecycle authority or release action
exists in the live evidence. Review completeness is not lifecycle approval.

## Consequences and tradeoffs

- Consumers gain a complete, deterministic, version-bound contract and do not
  need to copy Hygiene policy.
- Full-profile evidence is intentionally more verbose because applicability,
  implementation, and authority decisions remain inspectable and cannot hide
  behind aggregate scores.
- Narrow exemptions can be reviewed without being mislabeled as passing.
- An immutable pin prevents silent source changes but requires deliberate
  upgrades and full fixture replay.
- Experimental mechanisms can be tested without blocking unrelated profile
  use or gaining implied authority.
- No downstream implementation, adoption, conformance, publication, release,
  or organization-wide state is established by this decision.

## Implementation and evidence links

The proposal is represented by the canonical
[`agent-ready-web-profile.json`](../../catalog/agent-ready-web-profile.json),
the [profile schema](../../schemas/agent-ready-web-profile.v1.schema.json), the
[conformance evidence schema](../../schemas/agent-ready-web-conformance.v1.schema.json),
the [human guide](../ecosystem/AGENT_READY_WEB.md), synthetic whole-profile
[compatibility fixtures](../../fixtures/agent-ready-web), the dependency-free
validator, and focused tests. The contract catalog, dependency register and
generated projection, architecture and agent context, roadmap, README, and
continuity checkpoint link those canonical sources without duplicating their
policy.

Issue #53 is the review authority, and
[PR #57](https://github.com/egohygiene/hygiene/pull/57) is the focused,
unmerged review surface. No automatic pull-request CI evidence is assumed.

## Replacement or exit strategy

Consumers keep their existing immutable pin until an explicit reviewed change.
A compatible revision can add optional information while preserving IDs and
meaning. A change to concern, applicability, strength, maturity, authority,
diagnostic, level, evidence, exemption, pin, lifecycle, or ownership semantics
is breaking and needs a documented migration. Unsupported experimental
mechanisms can be omitted rather than replaced with fabricated state.

## Follow-up work

Maintainers review and, if authorized, merge the focused checkpoint pull
request. Only that merge may close issue #53. Parent #16 may close with the same
merge only after its stale tracker state is visibly reconciled and all earlier
merged checkpoints plus every parent acceptance criterion have concrete
evidence. Holon #7 and every other downstream consumer handoff remain separate,
unimplemented work. Release, lifecycle promotion, tag, deployment, registry
publication, workflow rollout, site publication, monitoring, adoption, and
enforcement remain out of scope.
