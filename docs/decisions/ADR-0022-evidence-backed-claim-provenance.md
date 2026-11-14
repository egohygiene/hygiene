---
schema: egohygiene.architecture-decision/v1
id: ADR-0022
title: Qualify quantitative and compatibility claims through referenced provenance
status: proposed
date: "2026-11-14"
decision_scope: organization
visibility: public
owners: [egohygiene/hygiene]
issue: https://github.com/egohygiene/hygiene/issues/30
pull_request: null
related: [ADR-0002, ADR-0005, ADR-0006, ADR-0007]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/hygiene, egohygiene/aether, egohygiene/egolint, egohygiene/relay, egohygiene/observatory, egohygiene/identity, egohygiene/holon]
affected_contracts: [egohygiene.claim-provenance-policy/v1, egohygiene.claim-provenance/v1]
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/30
    description: General quantitative/performance/support/compatibility claim policy and bounded provenance requirements.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/627b448f655afb2f4366654ba3ca3050389e464a/docs/ecosystem/REPOSITORY_PRESENTATION.md
    description: Existing proposed evidence-linked badge semantics, not universal conformance or scientific proof.
exceptions: []
approval: null
---

# ADR-0022: Qualify quantitative and compatibility claims through referenced provenance

## Context

Documentation, compatibility cells and dashboards can silently strengthen an
estimate, provider statement or stale result. Existing Intelligence, presentation,
release and AI artifact systems own useful evidence, but no general compact
record connects a quantitative claim to its represented subject and method.

## Decision

Propose alpha.1 provenance and wording contracts with eleven explicit evidence
states. Keep declared and currently qualified states separate, require explicit
clock/provenance for stronger labels, and reference existing canonical evidence.
Safe opaque handles permit protected evidence without publishing private logs.
The pure reference implementation never fetches evidence or executes commands.

## Alternatives considered

Treating schema success or a green workflow badge as universal support loses
revision/method limits. Requiring all raw datasets public violates privacy.
Copying every benchmark, release or Intelligence artifact creates a second
canonical store. This proposal instead references those owners and makes
qualification gaps visible without asserting independent verification.

## Consequences

Consumers must preserve state/scope/clocks and link provenance rather than show
unsupported headlines. Complete provenance still cannot establish scientific
quality, actual execution or authenticity. Required enforcement and production
integration remain separately reviewed; this source contract is observe only.

## Validation

Executable synthetic benchmark, compatibility, provider, estimate, stale and
blocked examples qualify deterministically. Adversarial controls cover all
states, missing evidence, false strong labels, clocks, retention, supersession,
private locators, ambiguous JSON and nonfinite values. No actual product
performance or platform support is inferred from these fixtures.

## Rollout and rollback

Inventory and link existing claims in report-only mode. Review representative
methods/privacy, select exact compatible policy/consumer pins, and retain
unknowns and historical records. Human disposition precedes activation. Roll
back the selected renderer/enforcement policy without overwriting evidence or
retiming prior claims. No fleet rollout occurs in this change.

## Ownership

Hygiene owns semantics; Aether owns AI artifacts; Relay integrates rendering and
execution; EgoLint validates; Observatory observes; Identity/Holon compose
presentation assets/new repositories. Consumers own facts, methods, raw access,
retention and publication. Approval remains null.
