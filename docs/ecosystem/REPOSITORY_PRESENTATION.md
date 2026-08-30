# Repository presentation and evidence-badge profile

Status: **proposed `1.0.0-alpha.1`**

Policy owner: `egohygiene/hygiene`

Tracked by: [hygiene#22](https://github.com/egohygiene/hygiene/issues/22)

## Purpose

An Ego Hygiene repository README should help a person understand what the
repository is, whether it is usable, where its canonical information lives,
and what current evidence supports its public claims. Presentation is an
orientation and evidence surface. It is not proof that the software is safe,
correct, legally compliant, accessible in every context, maintained, or fit
for a particular purpose.

This profile defines:

- the minimum semantic slots for repository presentation;
- required, recommended, optional, and not-applicable applicability;
- repository-type, visibility, and lifecycle variations;
- evidence states and fail-closed badge behavior;
- the boundary between repository-authored facts and generated regions; and
- producer and consumer responsibilities across the organization.

The canonical machine source is
[`catalog/repository-presentation-profile.json`](../../catalog/repository-presentation-profile.json).
The profile and evidence schemas are proposals until explicit maintainer
approval activates them. Alpha consumers must pin an exact release or commit.

## Principles

1. **Truth before polish.** A beautiful README cannot compensate for unknown,
   stale, or contradictory evidence.
2. **Repository-owned facts.** Purpose, status, commands, support, license, and
   final publication decisions remain with the repository.
3. **Evidence-linked claims.** A badge identifies a specific check, artifact,
   profile version, and represented commit.
4. **Fail closed.** Unknown, stale, partial, blocked, or failing evidence never
   appears as passing.
5. **Progressive enhancement.** The README remains understandable when images,
   hosted badge services, styles, or the network fail.
6. **Bounded generation.** Tools update declared generated regions and preserve
   repository-authored prose.
7. **Applicability over uniformity.** Repositories share semantics, not
   identical prose or irrelevant sections.

## Contract family

| Contract | Purpose |
| --- | --- |
| `egohygiene.repository-presentation-profile/v1` | Policy, slots, applicability, evidence-state vocabulary, composition rules, and ownership. |
| `egohygiene.repository-presentation-evidence/v1` | One repository assessment, represented revision, resolved slot requirements, evidence records, and badge descriptor. |

The first contract version is `1.0.0-alpha.1`. It is deliberately proposed:
Identity, Holon, and Egolint can implement against an exact pin without this
review artifact claiming organization-wide activation.

## Applicability model

The profile resolves every slot through four deterministic layers:

1. the slot's default requirement;
2. repository-type overrides;
3. visibility overrides; and
4. lifecycle overrides.

Later layers win. This order is normative and prevents different consumers
from inventing incompatible precedence.

### Requirement meanings

| Requirement | Meaning |
| --- | --- |
| `required` | Must pass for a passing or advisory profile assessment. |
| `recommended` | A gap produces an advisory result after all required slots pass. |
| `optional` | May be present; its absence does not lower the profile result. Any claim it does make still needs evidence. |
| `not_applicable` | The resolved profile says the slot does not apply. Evidence records the reason; a repository cannot self-select this value. |

### Repository types

The initial type vocabulary covers applications, collections, control-plane
repositories, documentation, infrastructure, libraries, publications,
templates, tools, and websites. A repository chooses the closest durable
capability type rather than whichever type produces fewer requirements.

Type is only one axis. `private` is a visibility, while `incubating` and
`archived` are lifecycle states. This avoids misclassifying a private library
or an archived publication as a unique repository kind.

### Visibility variations

- Public repositories require the identity banner and license slots by
  default.
- Internal repositories may make those slots recommended where public-facing
  assets or licensing are not appropriate.
- Private repositories may omit public imagery, externally hosted badges, and
  public license claims. Their text must still state purpose, lifecycle,
  support, and applicable access paths without exposing private information.

No private evidence, token, issue title, internal URL, or repository name may
enter a public projection merely to fill a slot.

### Lifecycle variations

- Active repositories use the default profile.
- Incubating repositories must make their maturity explicit; evidence badges
  are optional until stable checks exist.
- Archived repositories must clearly say they are archived. Installation,
  development, validation, and contribution slots become not applicable, with
  reasons, rather than displaying stale instructions as current.

### Maturity matrix

| Lifecycle | Status disclosure | Evidence badges | Installation/development | Validation/contributing | Passing boundary |
| --- | --- | --- | --- | --- | --- |
| `active` | Required | Recommended | Resolve from repository type | Recommended | All required and recommended slots have current passing evidence. |
| `incubating` | Required and visibly experimental | Optional | Resolve from repository type and state only current capabilities | Recommended where a real path exists | All resolved required slots pass; missing optional evidence remains visible without implying maturity. |
| `archived` | Required and visibly archived | Recommended if durable evidence remains | Not applicable with reasons | Not applicable with reasons | Remaining required and recommended archival-orientation slots pass. |

Maturity is repository-authored and evidence-backed. Neither commit activity,
badge count, nor visual completeness may silently promote a repository from
incubating to active or reopen an archived repository.

## Canonical content slots

| Slot | Default | Canonical authority | Intent |
| --- | --- | --- | --- |
| `identity_banner` | Required | Identity assets; repository selects | Centered, accessible repository identity with stable fallback. |
| `purpose` | Required | Repository | What the repository is for and who it serves. |
| `maturity_status` | Required | Repository | Honest lifecycle, maturity, and support state. |
| `support_boundary` | Required | Repository | Support path, limitations, and security-reporting boundary. |
| `canonical_navigation` | Required | Repository | Applicable canonical documentation and policy destinations. |
| `evidence_badges` | Recommended | Hygiene semantics; evidence producers supply facts | Linked evidence, never unsupported decoration. |
| `installation` | Required | Repository | Shortest truthful install, consume, read, or access path. |
| `development` | Recommended | Repository | Reproducible local setup. |
| `documentation` | Recommended | Repository | Canonical user and reference documentation. |
| `validation` | Recommended | Repository and CI evidence | Canonical checks and current evidence. |
| `architecture` | Recommended | Repository | Architecture and ownership entry point. |
| `contributing` | Recommended | Repository | Contribution path or honest closed-contribution statement. |
| `license` | Required | Repository | License and applicable third-party notices. |
| `security` | Required | Repository | Applicable security-reporting path or honest limitation. |
| `generated_ownership` | Optional | Generator manifest and repository | Source, generator, update path, and manual-edit boundary. |

A template may group slots into a clean visual hierarchy. It must not delete a
required semantic slot because another badge or image appears to imply it.

## README composition contract

Holon may create a new README projection and Pace may propose bounded updates
to existing READMEs. Both operate on explicit generated regions. They must:

- preserve repository-authored purpose, commands, caveats, and custom prose;
- avoid destructive full-file replacement;
- show a review diff before changing an existing repository;
- record the profile version, generator version, and source digest;
- leave unsupported sections absent or explicitly not applicable instead of
  generating plausible filler; and
- support rollback by restoring the preceding reviewed regions.

HTML in a README should remain restrained: centered banner or hero markup,
badges, and compact navigation are reasonable. Critical meaning belongs in
text that remains available to assistive technology and when images fail.

## Identity banner requirements

Identity owns the visual source and renderer-neutral descriptor. The consumer
repository owns the selected repository identity, its placement, and final
review. A conforming banner projection provides:

- a repository-owned file or an immutable released Identity asset;
- intrinsic dimensions and a content digest;
- meaningful alt text;
- light, dark, high-contrast, and narrow-rendering behavior where variants are
  claimed;
- a textual repository title and purpose adjacent to the image; and
- a stable fallback that does not require a hosted image provider.

The banner is never the sole carrier of repository identity or status.

## Evidence badges

### Badge descriptor

The Hygiene badge descriptor contains:

- label `Hygienic`;
- the exact profile version;
- the evidence state;
- the profile-owned text message for that state;
- the full represented commit;
- a short state message; and
- an evidence URL or repository-relative evidence artifact.

Static local SVG or raster projections are preferred as the durable baseline.
A hosted provider such as shields.io may be an optional projection, never the
only source or evidence destination.

### State vocabulary

| State | Meaning |
| --- | --- |
| `unknown` | No trustworthy assessment is available. |
| `evaluating` | An assessment is running and has no final result. |
| `advisory` | Required slots pass, but one or more recommended slots need attention. |
| `passing` | Every required and recommended slot has current passing evidence. |
| `failing` | At least one required slot has current failing evidence. |
| `partial` | Required evidence is missing, incomplete, exempt, or otherwise insufficient for passing. |
| `stale` | Required evidence no longer represents the declared revision or freshness window. |
| `exempt` | A narrow slot exception has durable approval evidence; exemption is not passing. |
| `not_applicable` | The released profile does not apply to the assessed subject or slot. |
| `blocked` | A required assessment cannot complete because a named dependency or authority is unavailable. |

State colors are presentation hints, not the identity of the state. Every
projection includes text. `unknown`, `evaluating`, `advisory`, `partial`,
`stale`, `exempt`, `not_applicable`, and `blocked` remain visibly distinct from
`passing` and `failing`.

### Claims policy

The profile prohibits unsupported claims such as **compliant**, **certified**,
**guaranteed**, or **secure** in the Hygiene badge message. Those terms could
imply a legal, universal, or security conclusion that this presentation
profile does not establish.

Use precise wording instead:

- `Hygienic · repository profile passing`
- `Hygienic · advisory`
- `Hygienic · evidence stale`
- `Hygienic · unknown`

Individual workflow, package, license, documentation, release, or
accessibility badges follow the same evidence rule: the link identifies what
was checked, for which revision, and when. A workflow badge proves only that
workflow's declared result.

## Evidence document

A repository presentation evidence document records:

- the exact profile ID, version, status, and source;
- repository identity, type, visibility, lifecycle, and represented commit;
- assessment state, time, assessor identity, and assessor version;
- every profile slot exactly once, with its resolved requirement;
- evidence kind, location, assertion type, and freshness; and
- the derived badge descriptor.

The reference validator derives the top-level state from slot states. A
consumer cannot label the assessment `passing` while a required slot is
unknown, stale, blocked, partial, or failing. Not-applicable slots require a
profile-derived requirement and a reason. Exemptions require approval evidence.

Evidence artifacts are snapshots, not canonical README content. A repository
regenerates them when its represented commit, profile version, relevant source,
or evidence changes.

## Ownership boundary

| Owner | Responsibility | Does not own |
| --- | --- | --- |
| Hygiene | Policy, applicability, slots, evidence states, and claim limits. | Visual assets, templates, lint implementation, rollout, or dashboards. |
| Identity | Banner and badge visual profiles, variants, manifests, checksums, and descriptors. | Conformance state or README edits. |
| Holon | New-repository README blueprint and generated-region composition. | Existing-fleet mutation or repository facts. |
| Egolint | Applicability evaluation, lint rules, diagnostics, and normalized reports. | Policy meaning or CI orchestration. |
| Relay | Reusable validation orchestration and evidence transport. | Presentation policy or conformance semantics. |
| Pace | Previewed, reversible adoption pull requests for existing repositories. | Direct default-branch mutation. |
| Observatory | Read-only fleet aggregation, freshness, and conformance views. | Remediation or passing-state inference. |
| Repository | Purpose, status, commands, support, license, exceptions, custom prose, and final review. | Redefining organization policy or sibling-owned evidence. |

## Fixtures

Two synthetic fixtures prove different valid shapes:

- [`minimal.valid.json`](../../fixtures/repository-presentation/minimal.valid.json)
  is an archived public publication. It records honest not-applicable reasons
  and does not invent development or installation paths.
- [`rich.valid.json`](../../fixtures/repository-presentation/rich.valid.json)
  is an active public tool with all recommended slots and generated-region
  ownership evidence.

The names and commit IDs are intentionally synthetic. They are contract test
inputs, not claims about live repositories.

## Validation

Validate the proposed profile and fixtures without third-party packages:

```bash
python3 tools/presentation.py validate-profile
python3 tools/presentation.py validate-evidence \
  --evidence fixtures/repository-presentation/minimal.valid.json
python3 tools/presentation.py validate-evidence \
  --evidence fixtures/repository-presentation/rich.valid.json
```

Resolve one repository variant:

```bash
python3 tools/presentation.py resolve \
  --repository-type tool \
  --visibility public \
  --lifecycle active
```

The checker is a policy reference. Egolint owns production diagnostics and
Relay owns reusable execution after the contracts are reviewed and released.

## Adoption and migration

1. Review and release the Hygiene profile and evidence contract.
2. Identity publishes matching visual descriptors and assets.
3. Holon implements a new-repository README blueprint from the pinned profile.
4. Egolint implements applicability and conformance reporting against the same
   pin.
5. Prove minimal and rich consumers before a fleet rollout.
6. Pace produces repository-specific preview plans and reversible pull
   requests.
7. Observatory may aggregate released evidence without blocking rollout.

Existing customized READMEs are migrated section by section. Adoption never
means replacing a complete file with generic prose. A repository may retain
custom layout and additional material so long as every applicable semantic
slot remains discoverable and truthful.

## Compatibility and replacement

Within v1, additive optional slots or evidence fields may be compatible when
unknown fields remain rejectable until consumers upgrade deliberately. Changes
to requirement meanings, override precedence, state derivation, badge claims,
ownership, or required evidence require a new major version and migration plan.

Alpha versions may change through review. Consumers pin the exact alpha
version. Activation requires explicit human approval; merging generated output
or a downstream implementation does not activate the policy by itself.
