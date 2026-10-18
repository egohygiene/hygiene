# Continuous decision capture in Hygiene

Hygiene owns the canonical ADR policy. Use the
[accepted policy and significance test](../decisions/POLICY.md),
[ratification evidence](../decisions/RATIFICATION.md) and
[canonical index](../decisions/README.md). Do not add a self-inheritance reference.

## Selected authoring source

The managed decision-impact block in `AGENTS.md` is the exact Aether module
0.2.0 from commit `8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2`:

- [Module source](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/projections/templates/decision-impact.AGENTS.md)
- [create-decisions-document 2.0.0](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/skills/architecture/create-decisions-document/SKILL.md)
- [architecture-decisions 3.0.0](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/specs/architecture/governance/decisions.spec.md)
- [Policy selection and source digests](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/skills/architecture/create-decisions-document/references/policy-selection.json)
- [Installation, managed merge and rollback procedure](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/skills/architecture/create-decisions-document/references/adoption.md)

The Aether package remains draft. Its policy selection is accepted Hygiene
v1.1.0 at `c589587395750cd1c79c6fa0bef010189c547249`; its independent
Intelligence selection remains proposed. Those authorities do not collapse.

A host with the supported GitHub skills CLI can install this exact selection:

```bash
gh skill install egohygiene/aether create-decisions-document --pin 8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2
```

Review the selected package and follow its host-specific discovery procedure.
This checkpoint loaded the skill and references directly from the clean pinned
source checkout; it did not run this installation command or verify persistent
host discovery. A future agent must report an unavailable skill rather than
claiming it loaded. Static instructions do not install an automatic PR hook.
The selected package's older EgoLint/Relay matrix lacks canonical-owner support;
the newer candidates below are the separate explicit selections prepared for review.

## Before work and before handoff

Apply the managed checkpoint at both points. Cite a real governing/new/updated
ADR or give a concise `ADR not required` reason. Keep implementation evidence,
decision disposition and verification separate. An index addition, passing
check or merged implementation does not approve a proposal.

Repository-owned ADRs are authored source. Only the marked Aether guidance is
managed. Upgrading it requires an exact source revision, module/skill policy
parity, a preview through Aether's bounded merge helper, preservation of local
instructions and continuity, and a reviewed diff. Roll back only the managed
selection after checking for later edits; retain authored records and history.

## Source review through the shared validator

[EgoLint PR #82](https://github.com/egohygiene/egolint/pull/82) merged native
canonical-owner support at `72267fd0a371da6d94922cbc6bd3dedddb68df30`.
[Relay PR #154](https://github.com/egohygiene/relay/pull/154) merged canonical-owner
adoption at `f2e624cbbd1bb1150e29743061140f601b8486f6`.
[Relay PR #155](https://github.com/egohygiene/relay/pull/155) then merged explicit
external ADR selection at **`6cddad3124bdda1b1e3d54a40931f23322b7be26`**.
Use that exact merged revision for both CLI and action/workflow adoption, with
its [preparation instructions](https://github.com/egohygiene/relay/blob/6cddad3124bdda1b1e3d54a40931f23322b7be26/docs/repository-adr-collector.md#native-commands-and-reproducible-checks)
and locked dependencies. Keep its runtime and output outside this repository.
For an immutable source replay, bind caller-selected absolute paths:

```bash
ADR_SOURCE_REVISION="$(git rev-parse --verify HEAD)"
ADR_OBSERVED_AT="$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
python3 -I "${ADR_RELAY_SOURCE}/actions/repository-intelligence/scripts/collect_repository_adrs.py" collect \
  --runtime "${ADR_RUNTIME}" --repository-root "${ADR_HYGIENE_SOURCE}" \
  --repository egohygiene/hygiene --visibility public \
  --source-commit "${ADR_SOURCE_REVISION}" --observed-at "${ADR_OBSERVED_AT}" \
  --adoption legacy --policy-owner \
  --known-external-decisions '["egohygiene/identity#ADR-017"]' \
  --output "${ADR_REVIEW_DIRECTORY}/adr-collection.review.json"
```

`ADR_RELAY_SOURCE`, `ADR_RUNTIME`, `ADR_HYGIENE_SOURCE` and
`ADR_REVIEW_DIRECTORY` are explicit caller inputs. Run the revision command
inside the inspected Hygiene checkout. Review exit 2 and remaining source
findings are expected while ADR-0001's migration is unresolved. Every review
envelope says `publication: denied`; it is not a production build input.
The explicit external key is the existing public relationship in ADR-013.
Its target front matter was separately inspected at
[Identity `69d55c1`](https://github.com/egohygiene/identity/blob/69d55c1caaa5b3959ed2ffdbbcd1fd69357d87dc/docs/decisions/ADR-017-zensical-launchkit-publication-architecture.md).
This is a caller declaration, not collector-acquired target observation. The
paired native replay removes exactly its undeclared-reference finding while
preserving all source hashes, candidate digests and legacy findings.
Reference metadata checks alone cannot establish full Markdown/native conformance.

## Publication and upkeep gate

The selected repository origin is `https://hygiene.egohygiene.io` with canonical
`/intelligence/decisions/` and `/decisions/` plus `/adr/` shortcuts. The
[consumer publisher/runbook](../../publication/README.md) binds the merged Relay
selection, read-only source gate, exact artifact handoff and actual recovery/
HTTPS verification. The central roadmap host does not replace this local origin.

ADR-0001's real approval and legacy-identity exception remain the source gate.
Its prepared patch remains unapplied; advisory execution success cannot admit
an invalid corpus. Keep the organization `/decisions/` aggregation distinct.
Close #47 only after source admission, live bytes, accessibility/favicons and
recovery have actually been evidenced.
