# hygiene

The canonical ecosystem architecture and platform-control repository for the
Ego Hygiene organization.

Hygiene owns the repository registry, cross-repository architecture decisions,
platform policy, adoption model, organization contract index, and migration
context. It does not own the implementations of every policy or product
capability.

## Ecosystem architecture

- [Holistic architecture](docs/ecosystem/ARCHITECTURE.md)
- [Repository catalog](docs/ecosystem/REPOSITORY_CATALOG.md)
- [Migration plan](docs/ecosystem/MIGRATION_PLAN.md)
- [Agent context](docs/ecosystem/AGENT_CONTEXT.md)
- [Diagram sources](docs/ecosystem/diagrams/README.md)
- [Architecture acceptance decision](docs/decisions/ADR-0001-holistic-architecture-v0.1.md)
- [Machine-readable repository catalog](catalog/repositories.yaml)
- [Repository catalog schema](schemas/repository-catalog.v1.schema.json)
- [Generated repository catalog](docs/generated/REPOSITORIES.md)
- [Repository-local context contract](docs/ecosystem/REPOSITORY_CONTEXT.md)
- [Repository context policy](catalog/repository-context.json)
- [Repository context schema](schemas/repository-context.v1.schema.json)

The accepted written architecture and versioned machine-readable catalog are
authoritative. Rendered diagrams, local repository context, and future landscape
sites are projections of those sources.

## Proposed ADR and delivery-history foundation

- [ADR policy](docs/decisions/POLICY.md)
- [Proposed governing decision](docs/decisions/ADR-002-organization-adr-and-delivery-history.md)
- [ADR reference template](docs/decisions/ADR-TEMPLATE.md)
- [ADR migration guide](docs/decisions/MIGRATION.md)
- [ADR validation plan](docs/decisions/VALIDATION.md)
- [ADR front matter schema](schemas/architecture-decision.v1.schema.json)
- [Organization contract index](catalog/contracts.yaml)

These artifacts are proposals pending human review. This repository does not yet
claim organization-wide ADR validation, generated decision/activity data, or
dashboard implementation.

## Control-plane boundary

The public organization repository, `egohygiene/.github`, remains the
organization-facing inbox, profile, public defaults, and fallback coordination
surface. Hygiene is the canonical long-term home for ecosystem architecture,
the repository catalog, organization contracts, and cross-repository ADRs.

See [issue #1](https://github.com/egohygiene/hygiene/issues/1) for the initial
architecture import and [issue #2](https://github.com/egohygiene/hygiene/issues/2)
for the validated repository catalog contract.

Validate the existing repository catalog and its generated view with:

```bash
python3 tools/catalog.py --catalog catalog/repositories.yaml validate
python3 tools/catalog.py \
  --catalog catalog/repositories.yaml \
  check-generated \
  --output docs/generated/REPOSITORIES.md
python3 tools/context.py validate
python3 -m unittest discover --start-directory tests --pattern "test_*.py"
```

The proposed ADR schemas are reviewed structurally in this phase; executable
validation belongs to the later Relay implementation.
