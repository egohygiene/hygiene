---
schema: egohygiene.architecture-decision/v1
id: ADR-0015
title: Compose pinned owner validation for local release declarations
status: proposed
date: "2026-11-03"
decision_scope: repository
visibility: public
owners: [egohygiene/hygiene]
issue: https://github.com/egohygiene/hygiene/issues/84
pull_request: null
related: [ADR-0007, ADR-0014]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/hygiene]
affected_contracts: [egohygiene.repository-release-policy/v1]
implementation_status: implemented
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/84
    description: Requires actual pinned owner composition, structural manual-only triggers and honest unavailable evidence.
  - type: implementation
    url: https://github.com/egohygiene/aether/blob/8a2a3d08f3aa9da3847bd5277843506ab855192e/library/organization/specs/release/validate.py
    description: Selected owner validator supports full Draft 2020-12 validation and a deliberately weaker optional fallback.
  - type: implementation
    url: https://github.com/egohygiene/aether/blob/8a2a3d08f3aa9da3847bd5277843506ab855192e/requirements-dev.lock
    description: Existing selected owner runtime pins PyYAML and jsonschema dependencies.
exceptions: []
approval: null
---

# ADR-0015: Compose pinned owner validation for local release declarations

## Context

Hygiene's existing local string checks do not establish conformance to its
selected Aether declaration schema. The owner helper has a standard-library
fallback that deliberately covers less than the normative schema. Workflow
trigger structure also needs real YAML parsing: comments, quoted keys and inline
events cannot be classified safely by substring searches.

ADR-0014 records JSON-compatible catalog loading without mandatory catalog
dependencies. This proposal is limited to composed release-declaration checks;
profile/requirement resolution and the catalog format retain that boundary.

## Decision

Propose requiring the exact selected owner validator/schema for declaration
composition. Verify selected source bytes against a reviewed lock, execute the
native validator with full jsonschema support, and reject unavailable or weaker
fallback validation. Load the owner from an explicitly prepared source directory;
the checker neither downloads nor installs it implicitly. The manual workflow
selects the same immutable source and its existing pinned runtime dependencies.

Use PyYAML only for release workflow/Taskfile structure, with string `on` keys
and duplicate-key rejection. Require only `workflow_dispatch` events and actual
declared Task handoff names. Record the selected source hashes, actual engine
and declaration digest in deterministic plan evidence. Validation remains
read-only and supplies no tag, release, deployment or credential authority.

## Alternatives considered and rejected

- Keep prefix/token checks or accept the owner's stdlib fallback: insufficient
  evidence for the schema and trigger invariant in #84.
- Copy the owner's schema or reconstruct its required fields locally: creates
  competing protocol authority and independent drift.
- Fetch default-branch source or install dependencies inside the checker: hides
  mutability and network effects from a read-only preparation command.

## Consequences and tradeoffs

Declaration checks now need a prepared owner source and its runtime. Missing
inputs produce an explicit unavailable result instead of partial success.
Source hashes permit an equivalent selected artifact without claiming the
caller's checkout HEAD equals the historical revision. Profile/resolve commands
remain standard-library-only. Compatibility and real Task/workflow execution
still need separate qualification; this proposal does not ratify the policy.

## Implementation and evidence links

Issue84 owns acceptance. The same draft proposes the source lock, composed
checker, thin Task/manual workflow wiring and tests. Implementation and actual
validation results must be recorded separately in CONTINUITY.md and the PR;
authored tests, a merge and this proposed record are not human acceptance.

## Replacement or exit strategy

A released owner artifact can replace the prepared checkout through a reviewed
lock/adapter update that retains full validation and evidence. Unsupported
selections stay unavailable; preserve the old pin and historical evidence.

## Follow-up work

Qualify #84's native, structural and public command regressions and seek human
disposition of this proposal through the existing ADR workflow. No speculative
policy activation, new release engine or publication issue is created.
