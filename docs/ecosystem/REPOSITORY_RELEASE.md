# Repository release-convention baseline

Status: **proposed `1.0.0-alpha.1`**

Policy owner: `egohygiene/hygiene`
Tracked by: [hygiene#27](https://github.com/egohygiene/hygiene/issues/27)

## Purpose

This is the inheritable policy layer for repository releases. It composes
Aether's release declaration into repository applicability, migration, and
ownership rules. It does not replace the declaration schema, select a version,
run a release, or publish to any provider.

The canonical machine source is
[`catalog/repository-release-policy.json`](../../catalog/repository-release-policy.json).
It is a proposed policy until maintainer approval activates it. Repositories
pin a released Hygiene policy version or full commit before enforcement.

## Immutable Aether dependency

The policy consumes Aether's `egohygiene.repository-release/v1` contract at
version `1.0.0`, pinned to merge commit
[`8a2a3d08f3aa9da3847bd5277843506ab855192e`](https://github.com/egohygiene/aether/tree/8a2a3d08f3aa9da3847bd5277843506ab855192e).

- [Aether specification](https://github.com/egohygiene/aether/blob/8a2a3d08f3aa9da3847bd5277843506ab855192e/library/organization/specs/release/repository-release.spec.md)
- [Aether JSON Schema](https://github.com/egohygiene/aether/blob/8a2a3d08f3aa9da3847bd5277843506ab855192e/catalog/schemas/aether.repository-release.v1.schema.json)
- [Aether authoring skill](https://github.com/egohygiene/aether/blob/8a2a3d08f3aa9da3847bd5277843506ab855192e/library/organization/skills/publishing/prepare-repository-release/SKILL.md)

Those links are the protocol source. Hygiene intentionally repeats only the
applicability and ownership composition needed to govern adoption. A later
policy revision must change the version and full Aether revision together; it
must never follow Aether's default branch.

## Baseline

Each applicable repository keeps its release facts in
`.egohygiene/release.json`. There is no organization-wide external registry to
keep in sync. The local declaration is the source of truth for its release
profile, component authority, delivery state, evidence state, and rollback
instructions; Hygiene is the source of truth for policy applicability.

| Slot | Normal state | Requirement |
| --- | --- | --- |
| Aether declaration | `.egohygiene/release.json` uses `egohygiene.repository-release/v1`. | Required |
| Root changelog | `CHANGELOG.md` has an exact `## [Unreleased]` heading in Keep a Changelog 1.1 format. | Required |
| Version authority | Every declared component names exactly one Aether-defined authority. | Required |
| Task handoffs | `release:plan`, `release:prepare`, `release:verify`, and `release:publish` are bounded, review-first Taskfile actions. | Required |
| Manual workflow | The declaration names a `workflow_dispatch` handoff; normal PRs do not publish. | Required |
| Release and rollback guidance | Local docs describe review, evidence boundaries, and immutable-artifact recovery. | Required |
| Agent pointer | `AGENTS.md` points agents to the local release guidance before behavior changes. | Required |

`release:publish` is a handoff, not standing authority. It must not create a
tag, publish an artifact, deploy a site, use credentials, or overwrite an
immutable release unless a separate reviewed action explicitly authorizes that
operation.

## Applicability and migration

Requirement resolution is deterministic: default slots, release-profile
overrides, visibility overrides, then lifecycle overrides. The current profile
has the following activation rules:

- New repositories and existing active repositories are **required** to adopt
  the baseline.
- Incubating repositories are **advisory** until they have a durable release
  boundary; they still state the facts they know rather than presenting an
  invented release path.
- Archived repositories retain their declaration and changelog with Aether
  release state `frozen`; new-release Taskfile and workflow handoffs are
  **not applicable**.
- A narrow **exempt** state is only a temporary, repository-owned exception. It
  records scope, reason, legacy evidence, owner, approval, expiry, and exit
  criteria. It never implies passing conformance.

Migration preserves the historical record. Existing non-SemVer tags, unusual
tag prefixes, partial changelogs, missing checksums, external delivery, or
unavailable evidence are documented as facts. Do not rewrite tags, fabricate a
release chronology, retrofit version numbers, or claim a provider published an
artifact. The first compliant future release establishes the new boundary.

## Baseline examples

| Repository kind | Aether profile | Adoption notes |
| --- | --- | --- |
| Contract repository | `contract` | A catalog record or tag is authoritative; GitHub Release evidence does not prove another channel. |
| Tool or library | `cli-library`, `python-package`, or `npm-package` | The selected language manifest is the single authority. |
| Container image | `container-image` | A release tag and immutable image digest remain distinct evidence. |
| Static site | `static-site` | Deployment evidence is separate from a source release. |
| Publication | `publication` | Publication metadata governs version; DOI or archive delivery can be external. |
| Workspace | `workspace` | Each component retains one authority; unrelated manifests do not become a synthetic release version. |
| Private repository | `internal-only` | Local declaration and manual review still apply; distribution and evidence stay private and repository-owned. |
| Archived repository | Any suitable historical profile | Declaration and changelog stay visible; release state is `frozen` and new-release handoffs are not applicable. |

## Rollback

Release artifacts and tags are immutable. The repository declaration selects
one Aether rollback strategy:

- `revert-and-successor-tag` for corrected source or contract releases;
- `revoke-channel` for a package or container distribution;
- `redeploy-prior-artifact` for a site; or
- `freeze` for a historical or archived repository.

The recovery creates new evidence; it never replaces a prior tag, release
asset, changelog entry, image digest, or deployment record.

## Ownership boundary

| Owner | Owns | Does not own |
| --- | --- | --- |
| Aether | Declaration schema, specification, and authoring skill. | Hygiene applicability or reusable CI execution. |
| Hygiene | This baseline's applicability, migration rules, and policy composition. | Aether protocol semantics, tags, or publication adapters. |
| Relay | Reusable immutable execution and durable reports. | Release-policy meaning or component-version decisions. |
| Egolint | Conformance diagnostics and normalized results. | Policy applicability or publication. |
| Pace | Previewed, reversible adoption pull requests. | Direct default-branch mutation. |
| Repository | Local facts, version authorities, delivery adapters, credentials, exceptions, release decisions, and final review. | Redefining the shared policy. |

## Hygiene dogfood

Hygiene itself is an active `contract` profile consumer. Its
[declaration](../../.egohygiene/release.json), root
[changelog](../../CHANGELOG.md), [Taskfile](../../Taskfile.yml), manual
[release workflow](../../.github/workflows/release-policy.yml), and this guide
are validated together by `tools/releases.py`. The version authority for this
proposed policy artifact is `catalog/repository-release-policy.json`.

## Validation

```bash
python3 tools/releases.py validate-profile
python3 tools/releases.py validate-declaration --repository "." --format "json"
python3 tools/releases.py resolve --repository-profile "contract" --lifecycle "active" --visibility "public" --adoption-state "required"
```

The checker is intentionally offline and non-publishing. Relay #47 and
Egolint #29 may consume its stable profile boundary after this proposed policy
is reviewed and released.
