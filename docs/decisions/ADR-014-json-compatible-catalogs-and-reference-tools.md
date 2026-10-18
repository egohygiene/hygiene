---
schema: egohygiene.architecture-decision/v1
id: ADR-014
title: Keep Hygiene catalogs JSON-compatible with dependency-free reference tools
status: proposed
date: 2026-08-19
decision_scope: repository
visibility: public
owners:
  - egohygiene/hygiene
issue: https://github.com/egohygiene/hygiene/issues/47
pull_request: null
related:
  - ADR-0001
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/hygiene
affected_contracts: []
implementation_status: implemented
evidence:
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/2
    description: Catalog scope explicitly requires dependency-free validation and deterministic generated documentation.
  - type: pull_request
    url: https://github.com/egohygiene/hygiene/pull/4
    description: Merged catalog contract, Python reference validator, deterministic renderer and generated view.
  - type: commit
    url: https://github.com/egohygiene/hygiene/commit/0d61e6ef26af0630dabafc9636b3061749767883
    description: Original catalog implementation, authored 2026-08-19 UTC; evidence of implementation rather than ADR ratification.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/0d61e6ef26af0630dabafc9636b3061749767883/catalog/README.md
    description: Contemporary rationale for JSON syntax valid as YAML 1.2 while avoiding a YAML parser dependency.
  - type: implementation
    url: https://github.com/egohygiene/hygiene/blob/0d61e6ef26af0630dabafc9636b3061749767883/tools/catalog.py
    description: Standard-library JSON loading, semantic checks and deterministic Markdown projection.
exceptions: []
approval: null
---

# ADR-014: Keep Hygiene catalogs JSON-compatible with dependency-free reference tools

## Context

Hygiene's repository catalog is a machine-readable source for repository
ownership and deterministic human views. The original catalog change used
`catalog/repositories.yaml` with JSON syntax valid as YAML 1.2. Its contemporary
README states the reason: keep the requested `.yaml` contract path while
avoiding a YAML parser dependency in the reference validator. Issue #2 also
explicitly requires dependency-free validation and deterministic documentation.

That format/runtime tradeoff is present in source but has no separate local
ADR. It is narrower than the organization topology in ADR-0001 and does not
choose a language or parser for every tool in the ecosystem.

## Decision

Propose retaining JSON-compatible YAML 1.2 for Hygiene's catalog files that are
consumed by its dependency-free Python reference tools. Keep the existing
`.yaml` paths and their JSON-compatible syntax together, use the Python standard
library to decode those files, and generate human-readable views from the
canonical inputs deterministically.

This is a repository-local reconstruction of an implemented choice, pending
human disposition. It does not change catalog schemas or repository ownership,
mandate Python across Hygiene or sibling repositories, or relocate EgoLint's
semantic validation and Relay's execution responsibilities.

## Alternatives considered and rejected

The contemporary README supports one bounded comparison: a catalog requiring
a general YAML parser would add a parser dependency; the selected JSON subset
avoids that dependency while retaining the `.yaml` path. No contemporaneous
record of broader runtime comparisons, benchmarks or rejected languages was
found in this reconstruction. Those alternatives and motives remain unknown.

## Consequences and tradeoffs

- Standard-library JSON readers can consume the selected catalogs without a
  third-party YAML parser, and YAML 1.2 readers can consume the same data.
- Authors must retain the JSON subset: YAML-only syntax, comments and aliases
  would break the existing reference loader.
- Generated Markdown remains a projection; edits belong in canonical catalog
  data followed by regeneration and drift checking.
- Format or dependency changes require an explicit compatibility review;
  this record does not turn every `.yaml` file into a catalog contract.

## Implementation and evidence links

[Issue #2](https://github.com/egohygiene/hygiene/issues/2),
[PR #4](https://github.com/egohygiene/hygiene/pull/4) and
[the original source commit](https://github.com/egohygiene/hygiene/commit/0d61e6ef26af0630dabafc9636b3061749767883)
establish implementation. The
[contemporary catalog guide](https://github.com/egohygiene/hygiene/blob/0d61e6ef26af0630dabafc9636b3061749767883/catalog/README.md)
records the format rationale. Its validator, renderer and tests are part of
the same change. Historical merge and test claims do not supply approval of
this newly reconstructed ADR. The implementation label is `implemented`, not
newly `verified` by this record.

## Replacement or exit strategy

A later reviewed change can choose a general YAML parser or another serialized
format. It must review consumer compatibility, version any incompatible
contract, migrate canonical inputs, regenerate projections, and retain the
old source and migration evidence in Git. Do not silently admit syntax that
the selected loader cannot decode.

## Follow-up work

[Hygiene #47](https://github.com/egohygiene/hygiene/issues/47) owns review of
this reconstruction and the wider repository ADR backfill. Human disposition
is pending; no broader runtime policy is proposed here.

## Reconstruction note

Reconstructed on 2026-10-18 from reachable public source and provider evidence.
The front-matter date names the original implementation's 2026-08-19 UTC date,
not a recovered approval date. The original author timestamp was 2026-08-18
in UTC-04:00. This new record remains proposed with null approval.
