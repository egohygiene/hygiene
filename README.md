# hygiene

The canonical ecosystem architecture and platform-control repository for the
Ego Hygiene organization.

Hygiene owns the repository registry, cross-repository architecture decisions,
platform policy, adoption model, organization contract index, and migration
context. It does not own the implementations of every policy or product
capability.

Current work is handed off through the repository-owned
[`CONTINUITY.md`](CONTINUITY.md). Reconcile it against live Git and GitHub
evidence; it is not a substitute for the canonical sources below.

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
- [Deprecated repository context v1 schema](schemas/repository-context.v1.schema.json)
- [Proposed repository continuity policy](docs/ecosystem/REPOSITORY_CONTINUITY.md)
- [Repository continuity policy source](catalog/repository-continuity-policy.json)
- [Repository continuity policy schema](schemas/repository-continuity-policy.v1.schema.json)
- [Repository context v2 schema](schemas/repository-context.v2.schema.json)
- [Proposed Agent-Ready Web profile](docs/ecosystem/AGENT_READY_WEB.md)
- [Agent-Ready Web profile source](catalog/agent-ready-web-profile.json)
- [Agent-Ready Web profile schema](schemas/agent-ready-web-profile.v1.schema.json)
- [Agent-Ready Web compatibility fixtures](fixtures/agent-ready-web)
- [Dependency-boundary register](catalog/dependency-boundaries.yaml)
- [Dependency-boundary schema](schemas/dependency-boundary-register.v1.schema.json)
- [Generated dependency-boundary view](docs/generated/DEPENDENCY_BOUNDARIES.md)
- [Dependency-boundary guide](docs/ecosystem/DEPENDENCY_BOUNDARIES.md)
- [Proposed Repository Intelligence contract](docs/ecosystem/REPOSITORY_INTELLIGENCE.md)
- [Repository Intelligence schema](schemas/repository-intelligence.v1.schema.json)
- [Repository Intelligence vocabulary](catalog/repository-intelligence-vocabulary.json)
- [Complete quest fixture](fixtures/repository-intelligence/complete-quest.json)
- [Proposed repository presentation profile](docs/ecosystem/REPOSITORY_PRESENTATION.md)
- [Repository presentation profile source](catalog/repository-presentation-profile.json)
- [Repository presentation profile schema](schemas/repository-presentation-profile.v1.schema.json)
- [Repository presentation evidence schema](schemas/repository-presentation-evidence.v1.schema.json)
- [Repository presentation fixtures](fixtures/repository-presentation)

The accepted written architecture and versioned machine-readable catalog are
authoritative. Rendered diagrams, local repository context, and future landscape
sites are projections of those sources.

## Accepted ADR and delivery-history foundation

- [ADR policy](docs/decisions/POLICY.md)
- [Accepted governing decision](docs/decisions/ADR-002-organization-adr-and-delivery-history.md)
- [Proposed Repository Intelligence decision](docs/decisions/ADR-005-unify-repository-intelligence-projection.md)
- [Proposed Agent-Ready Web foundation decision](docs/decisions/ADR-009-agent-ready-web-profile-foundation.md)
- [ADR reference template](docs/decisions/ADR-TEMPLATE.md)
- [ADR migration guide](docs/decisions/MIGRATION.md)
- [ADR validation plan](docs/decisions/VALIDATION.md)
- [ADR-002 ratification evidence](docs/decisions/RATIFICATION.md)
- [ADR front matter schema](schemas/architecture-decision.v1.schema.json)
- [Repository ADR policy-reference schema](schemas/architecture-decision-policy-reference.v1.schema.json)
- [ADR compatibility fixtures](fixtures/architecture-decisions)
- [Organization contract index](catalog/contracts.yaml)

ADR-002 and policy v1.1.0 are accepted organization authority. This repository
provides their canonical schemas, fixtures, and reference checks; it does not
claim that downstream fleet validation, generated decision/activity data, or
dashboard publication is complete.

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
python3 tools/continuity.py validate-profile
python3 tools/continuity.py validate-repository --repository .
python3 tools/agent_ready_web.py validate-profile
python3 tools/agent_ready_web.py validate-fixtures
python3 tools/boundaries.py validate
python3 tools/boundaries.py \
  check-generated \
  --output docs/generated/DEPENDENCY_BOUNDARIES.md
python3 tools/boundaries.py scan \
  --repository-root . \
  --repository egohygiene/hygiene
python3 tools/intelligence.py validate \
  --snapshot fixtures/repository-intelligence/complete-quest.json \
  --vocabulary catalog/repository-intelligence-vocabulary.json
python3 tools/presentation.py validate-profile
python3 tools/presentation.py validate-evidence \
  --evidence fixtures/repository-presentation/minimal.valid.json
python3 tools/presentation.py validate-evidence \
  --evidence fixtures/repository-presentation/rich.valid.json
python3 tools/decisions.py decision \
  --input fixtures/architecture-decisions/decision.proposed.valid.json
python3 tools/decisions.py decision-set \
  --input fixtures/architecture-decisions/decision.superseded.valid.json \
  --input fixtures/architecture-decisions/decision.accepted.valid.json
python3 tools/decisions.py policy-reference \
  --input fixtures/architecture-decisions/policy-reference.valid.json
python3 -m unittest discover --start-directory tests --pattern "test_*.py"
```

The dependency-free Repository Intelligence and decoded ADR checkers are
contract references, not fleet enforcement or full Markdown parsers. Production
lint semantics belong to Egolint and reusable collection, generation, and
publication workflows belong to Relay.
