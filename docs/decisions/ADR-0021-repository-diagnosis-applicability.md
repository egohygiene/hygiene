---
schema: egohygiene.architecture-decision/v1
id: ADR-0021
title: Compose repository diagnosis applicability without taking record ownership
status: proposed
date: "2026-11-14"
decision_scope: organization
visibility: public
owners: [egohygiene/hygiene]
issue: https://github.com/egohygiene/hygiene/issues/41
pull_request: null
related: [ADR-0002, ADR-0005]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/hygiene, egohygiene/aether, egohygiene/egolint, egohygiene/observatory, egohygiene/relay, egohygiene/pace]
affected_contracts: [egohygiene.repository-diagnosis-policy/v1, egohygiene.repository-diagnosis-capability/v1]
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/41
    description: Versioned applicability, privacy, bounded path and index-freshness requirements; upstream completion reconciliation.
  - type: pull_request
    url: https://github.com/egohygiene/aether/pull/75
    description: Existing owner record specification and authoring implementation; draft lifecycle remains distinct from merge.
exceptions: []
approval: null
---

# ADR-0021: Compose repository diagnosis applicability without taking record ownership

## Context

Aether owns evidence-labelled diagnosis records. Repositories still need explicit
applicability, path, sensitivity, retention and index rules. Missing records cannot
be read as healthy systems. Copying the schema would create a competing owner.

## Decision

Propose an observe-only alpha.1 Hygiene policy and declaration. Pin the existing
Aether draft revision and both artifact digests, preserve all six applicability
states and separate adoption. Reference checks consume explicit declarations and
clocks; public projection excludes protected visibility before inspection and
admits only a four-field summary. Structural review never claims diagnosis truth,
health, remediation or publication authority.

## Alternatives considered

Requiring every debug interaction to create a record adds noise and violates the
owner specification. Scanning every repository directory or projecting record
counts by default exposes protected context. Reimplementing record parsing in
Hygiene takes ownership from Aether/EgoLint. These approaches are rejected by
this proposal; existing systems retain their own authority.

## Consequences

Consumers need explicit opt-in, compatible owner artifacts and authenticated
visibility. Read-only declarations are useful before downstream rollout, but
cannot establish actual files, human approval or policy enforcement. Tracked
indexes require source/time bindings and regeneration; ephemeral is the default.

## Validation

Executable synthetic declarations exercise opted-out, private, public restricted
and allowlisted-summary cases. Refusal controls cover path escapes, wrong pins,
private metadata, stale/mismatched source, ambiguous JSON and clock order.
The capability guide records exact commands and limits; structural validation
does not authenticate supplied observations or validate Aether records.

## Rollout and rollback

Begin with reviewed exact revision/digest pins in report-only mode. Preserve
authored records/IDs/history and prior paths/pins; opt-out stops collection
without deleting evidence. Required enforcement needs separate maintainer
disposition and eligible upstream artifacts. Restore the old selection and
stop the new projection to roll back. No fleet migration is performed here.

## Ownership

Hygiene owns applicability and policy; Aether owns the record artifact; EgoLint
owns production validation; Observatory observes; Relay executes/presents only
admitted data; Pace proposes adoption. Repositories own facts, access, retention,
holds and final publication. Approval remains null.
