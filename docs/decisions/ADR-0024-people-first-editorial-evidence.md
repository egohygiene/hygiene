---
schema: egohygiene.architecture-decision/v1
id: ADR-0024
title: Separate content metadata evidence from editorial judgment
status: proposed
date: "2026-11-15"
decision_scope: organization
visibility: public
owners: [egohygiene/hygiene]
issue: https://github.com/egohygiene/hygiene/issues/23
pull_request: null
related: [ADR-0002, ADR-0013, ADR-0022]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/hygiene, egohygiene/aether, egohygiene/holon, egohygiene/egolint, egohygiene/relay, egohygiene/pace, egohygiene/observatory]
affected_contracts: [egohygiene.helpful-content-profile/v1, egohygiene.content-quality-evidence/v1]
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/23
    description: People-first quality, provenance, distinct human/mechanical review and honest freshness/archive requirements.
  - type: documentation
    url: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
    description: Reviewed people-first editorial self-assessment and who/how/why guidance; adaptation is not endorsement.
exceptions: []
approval: null
---

# ADR-0024: Separate content metadata evidence from editorial judgment

## Context

Useful publication needs accountability, evidence, corrections and audience value.
Ranking/traffic and schema completeness cannot establish that a reader was helped,
an expert reviewed content or an organization is legally compliant. Turning these
signals into one score would hide important missing and qualitative evidence.

## Proposed decision

Define a versioned proposed profile with stable source-mapped rules, applicability
and explicit mechanical/human verification boundaries. Add an evidence shape and
pure reference qualification that binds declared content revisions, review dates,
corrections, AI provenance, accessibility and archival metadata. Preserve unknown,
missing, partial, stale and blocked evidence rather than render it as passing.

Keep human/editorial authenticity outside JSON. Even a complete good fixture
requires independent qualitative review; no score, actor label or field supplies
approval. High-stakes and AI-assisted content retain their additional evidence
and review obligations. Broader editorial/corrections/legal surfaces stay in17.

## Alternatives and consequences

A universal helpfulness score would confuse search outcomes with quality and hide
judgment. Requiring specialist review for every ordinary note would overgeneralize
high-stakes applicability. Copied policy in every workflow would create competing
owners. A proposed profile/reference layer keeps semantics inspectable but cannot
authenticate sources, judge meaning, qualify an expert or measure reader value.

## Validation, adoption and rollback

Synthetic good/partial/stale/archived/high-stakes/AI/unknown cases and adversarial
controls qualify declared source behavior. Actual bytes, review identity, domain
expertise and final publication remain consumer-owned independent acceptance.
Hygiene defines policy; EgoLint/Relay retain production validation/orchestration,
Aether authoring, Observatory reporting, Holon scaffolding and Pace reviewed rollout.

Human activation is separate. This record and both new contracts remain proposed;
approval is null after integration. No content or policy is published/enforced.
Roll back the selected profile/reference change through normal source review,
preserving authored content, corrections, prior assessments and human dispositions.

The reference reuses the JSON Schema runtime already pinned and required by the
complete gate through its selected Aether release owner. It adds no independently
versioned package/runtime selection. This is a bounded exception to the proposed
ADR-0014 preference for dependency-free reference checks; it avoids a second
handwritten schema implementation. Production lint semantics remain EgoLint-owned.
