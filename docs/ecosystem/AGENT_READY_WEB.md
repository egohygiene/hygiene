# Agent-Ready Web profile foundation

Status: **proposed `1.0.0-alpha.1`**

Policy owner: `egohygiene/hygiene`

Tracked by: [hygiene#50](https://github.com/egohygiene/hygiene/issues/50),
checkpoint 1 of [hygiene#16](https://github.com/egohygiene/hygiene/issues/16)

## Purpose

The Agent-Ready Web profile defines how an Ego Hygiene website can remain an
excellent human-facing web experience while exposing explicit, efficient, and
safe machine-readable surfaces. This first checkpoint establishes the profile
language and registration boundary. It does not decide which concrete web
artifacts or interactive capabilities a site must publish.

The canonical machine source is
[`catalog/agent-ready-web-profile.json`](../../catalog/agent-ready-web-profile.json),
validated against
[`schemas/agent-ready-web-profile.v1.schema.json`](../../schemas/agent-ready-web-profile.v1.schema.json).
The source deliberately contains an empty `mechanisms` array. Later checkpoints
must add concrete entries through review rather than treating examples or issue
prose as accepted catalog data.

## Contract identity and lifecycle

| Field | Value |
| --- | --- |
| Contract | `egohygiene.agent-ready-web-profile/v1` |
| Profile version | `1.0.0-alpha.1` |
| Status | `proposed` |
| Canonical owner | `egohygiene/hygiene` |
| Consumer pin | Exact semantic version or immutable repository revision |

`proposed` is a review state. It permits reference validation and downstream
planning, but it does not claim acceptance, publication, rollout, or
conformance. Only explicit maintainer authority may change the lifecycle.

## Four independent concerns

| Concern | Scope | Boundary |
| --- | --- | --- |
| `readability` | Discovery metadata and alternate content representations for crawlers, retrieval systems, and agents. | Describing content does not grant permission to invoke actions. |
| `capability` | Explicit browser-agent or tool interactions and their permission, consent, security, audit, and revocation envelope. | A capability declaration does not imply readability, efficiency, or commercial authority. |
| `efficiency` | Lower-overhead, source-equivalent representations and delivery behavior. | Optimization must not weaken meaning, access control, provenance, or capability safeguards. |
| `commerce` | Machine-readable commercial meaning and the boundary around guarded transaction-oriented capabilities. | Commercial metadata does not authorize a transaction or define Store-owned action semantics. |

Every registered mechanism has exactly one primary concern. Requirement
resolution occurs independently within that concern, and consumers must not
infer one concern from another. If a future mechanism depends on another
concern, the registry must express that dependency explicitly rather than
assigning multiple primary concerns or silently coupling their requirements.

## Stable site classes

| Site class | Use when the site's primary purpose is... |
| --- | --- |
| `application` | An interactive browser-delivered product or tool. |
| `commerce` | Presenting products, offers, or guarded transaction paths. |
| `content` | Publishing articles, media, research, or other human-readable content. |
| `documentation` | Structured product, project, API, or reference documentation. |
| `hybrid` | Multiple first-class purposes that no one other class represents truthfully. |

Classification describes the durable public surface, not whichever choice
produces fewer requirements. `hybrid` is an explicit class, not a wildcard or
permission to combine every rule. Future class additions must follow the
compatibility and extension rules below.

## Requirement-strength vocabulary

| Strength | Meaning |
| --- | --- |
| `required` | An applicable site must implement the mechanism and provide current evidence. |
| `recommended` | The site should implement it; an evidenced omission remains advisory. |
| `optional` | The site may implement it; absence alone does not fail conformance. |
| `conditional` | It becomes required only when the rule's explicit, machine-identified condition applies. |
| `prohibited` | The site must not publish, advertise, infer, or fabricate it under the resolved rule. |

A conditional rule always carries a stable condition identifier and a human
description. A non-conditional rule carries `null`, preventing prose-only
conditions from changing requirement meaning. Site-class overrides are
explicit, unique, and evaluated against the selected stable class.

## Maturity taxonomy

| Level | Canonical label | Meaning |
| --- | --- | --- |
| `established` | established web standard / broadly deployed | Standards-based or broadly deployed interoperability is evidenced. |
| `published_specification` | published industry specification | A public primary specification exists, but broad web deployment is not established. |
| `emerging` | emerging convention | Documentation and observable adoption exist while compatibility or governance remains in motion. |
| `experimental` | experimental/incubating capability | The mechanism is exploratory and must not block unrelated publication or imply production readiness by default. |

Maturity and requirement strength are independent. A published specification
is not automatically required, and an experimental mechanism cannot become a
blocking default merely because it is registered. Every maturity assessment
records a date, rationale, and reference IDs that include at least one primary
authority.

## Mechanism registration contract

A future mechanism record contains:

| Field | Contract |
| --- | --- |
| `id`, `title`, `description` | Stable identity and bounded intent. |
| `concern` | Exactly one of the four core concerns. |
| `requirements` | One default rule plus unique, stable site-class overrides. |
| `maturity` | Level, assessment date, rationale, and supporting reference IDs. |
| `authoritative_references` | At least one primary source using the reference shape below. |
| `registration_evidence` | At least one record supporting inclusion or maturity classification. |
| `extensions` | Namespaced object payloads isolated from core conformance. |

The profile currently registers no real mechanisms. The synthetic fixtures
exercise this shape without claiming that a discovery artifact, browser-agent
protocol, advertising file, or commerce action has entered the canonical
catalog.

### Authoritative references

Each reference records a stable ID, title, publisher, reference type,
`primary` or `supporting` authority, HTTPS URL or safe repository-relative
path, and retrieval date. Allowed source types distinguish standards,
industry specifications, official documentation, registries, and maintainer
sources without treating them as equally mature.

At least one reference must be primary, and the maturity record must cite a
primary reference ID. Commentary may support a classification but cannot
replace the source that owns the mechanism's specification or registry.

### Registration evidence

Each evidence record has a stable ID, evidence kind, location, description,
and observation date. The bounded kinds cover specification publication,
implementation observation, conformance tests, adoption observations, and
maintainer assessment.

This is **mechanism-registration evidence**. It supports why a mechanism is in
the profile and how its maturity was classified. It is not a site-conformance
claim, deployment result, permission grant, or transaction record. The
site-conformance evidence contract remains deferred to the integration
checkpoint.

## Compatibility model

The profile uses semantic versioning, and consumers pin an exact version or
immutable revision.

Compatible additive evolution may clarify non-normative prose, add optional
mechanism records, add new site classes or vocabulary values without changing
existing values, or register optional namespaced extensions that do not affect
core conformance. Core vocabulary additions require a reviewed minor version;
producers emit them only after the consumer opts into that exact version.

A breaking change requires a new contract major and migration evidence when it:

- removes or renames a core concern, site class, requirement strength,
  maturity level, or registered mechanism;
- changes lifecycle, requirement, maturity, or concern meaning;
- makes previously optional data required or relaxes prohibited behavior; or
- changes concern assignment, reference or evidence shape, extension
  isolation, or ownership boundaries.

Unknown core values fail closed. A consumer must not reinterpret an unknown
value as optional or passing.

## Extension rules

Extension identifiers use the form
`egohygiene.<owner>.agent-ready-web.<name>/vN`. Their schemas and owners are
registered before the extension is treated as understood. Unknown namespaced
objects may be preserved as uninterpreted data, but they are excluded from core
conformance and cannot satisfy a core requirement.

An extension may add optional metadata or stricter validation owned by its
namespace. It may not redefine core vocabulary, lifecycle, compatibility,
reference/evidence semantics, or ownership. It also cannot grant capability,
consent, deployment, publication, or transaction authority.

## Ownership boundary

| Owner | Owns | Does not own here |
| --- | --- | --- |
| Hygiene | Profile identity, vocabulary, lifecycle, schema, compatibility, extensions, and reference validation. | Generators, reusable workflow implementation, rollout, commerce actions, dashboards, or publication. |
| Holon | Deterministic generation for new sites from an accepted immutable pin. | Policy meaning, existing-fleet mutation, site facts, or publication authority. |
| Relay | Reusable validation/publication workflow execution and evidence transport. | Policy semantics, site-class selection, credentials, commerce semantics, or final publication. |
| Pace | Previewed, reversible migration and convergence pull requests for existing sites. | Direct default-branch mutation, policy definition, or automatic adoption claims. |
| Store | Separately reviewed transaction-domain semantics and guarded commerce contracts. | The core profile, other concerns, fabricated seller relationships, or authorization inferred from metadata. |
| Observatory | Privacy-safe conformance evidence and metrics for an accepted profile. | Policy, remediation, rollout, passing-state fabrication, or site mutation. |

Hygiene's local checker is a reference implementation for this proposed
contract. It does not absorb Relay's reusable workflow role, Pace's fleet role,
Holon's generator role, Store's commerce domain, or Observatory's reporting
role.

## Validation and fixtures

Validate the canonical source and all synthetic compatibility fixtures with:

```bash
python3 tools/agent_ready_web.py validate-profile
python3 tools/agent_ready_web.py validate-fixtures
python3 -m unittest tests.test_agent_ready_web
```

The fixture set contains one valid synthetic mechanism and focused invalid
records for ambiguous concern assignment, a missing conditional predicate, and
a missing primary reference. `example.com` locations are deliberate reserved
fixture data, not claimed standards or implementations.

## Checkpoint boundary

This checkpoint establishes only the foundation. It does not:

- enumerate the discovery or alternate-representation catalog;
- define WebMCP or other browser-agent capability details;
- define advertising or commerce action semantics;
- implement generators, shared workflows, rollout, dashboards, publication,
  or downstream conformance; or
- activate the proposed profile.

After this checkpoint is reviewed and merged, issue
[#51](https://github.com/egohygiene/hygiene/issues/51) may add the discovery and
efficient-representation catalog against this exact foundation. Issues #52 and
#53 remain later dependent checkpoints.
