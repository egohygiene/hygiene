# Repository catalog contract

`repositories.yaml` is the canonical machine-readable registry for the Ego
Hygiene organization. It uses JSON syntax that is valid YAML 1.2, allowing the
validator to remain dependency-free while retaining the requested `.yaml`
contract path.

The contract records current repositories separately from proposed boundaries.
A proposed repository is not permission to create it. Its `create_after` gate
must be satisfied through an accepted architecture decision.

## Validate

```bash
python3 tools/catalog.py --catalog catalog/repositories.yaml validate
python3 -m unittest discover --start-directory tests --pattern "test_*.py"
```

## Generate the human view

```bash
python3 tools/catalog.py \
  --catalog catalog/repositories.yaml \
  render \
  --output docs/generated/REPOSITORIES.md

python3 tools/catalog.py \
  --catalog catalog/repositories.yaml \
  check-generated \
  --output docs/generated/REPOSITORIES.md
```

The generated view is a projection. Ownership changes must be made in the
catalog and accompanied by an architecture decision when they cross repository
boundaries.

## Dependency boundaries

`dependency-boundaries.yaml` is the canonical machine-readable register for
allowed producer-to-consumer direction, stable interface requirements,
forbidden couplings, and expiring exceptions. It is validated against this
repository catalog so boundary entries cannot silently reference an unknown
repository.

```bash
python3 tools/boundaries.py validate
python3 tools/boundaries.py \
  check-generated \
  --output docs/generated/DEPENDENCY_BOUNDARIES.md
python3 tools/boundaries.py scan \
  --repository-root . \
  --repository egohygiene/hygiene
```

See the [dependency-boundary guide](../docs/ecosystem/DEPENDENCY_BOUNDARIES.md)
for rule semantics, scanner scope, and the exception process.

## Repository Intelligence vocabulary

`repository-intelligence-vocabulary.json` is the proposed machine-readable
definition of directed graph relationships used by Repository Intelligence.
Its source/target kinds, inverse display labels, cardinality, and transitivity
rules are owned by Hygiene and validated with the complete-quest fixture.

```bash
python3 tools/intelligence.py validate \
  --snapshot fixtures/repository-intelligence/complete-quest.json \
  --vocabulary catalog/repository-intelligence-vocabulary.json
```

See the
[Repository Intelligence contract](../docs/ecosystem/REPOSITORY_INTELLIGENCE.md)
for identifier, provenance, event, privacy, extension, and compatibility rules.

## Repository presentation profile

`repository-presentation-profile.json` is the proposed semantic baseline for
repository banners, purpose/status, navigation, evidence badges, applicable
setup and policy links, and generated-region ownership. It defines type,
visibility, and lifecycle overrides without generating repository facts.

```bash
python3 tools/presentation.py validate-profile
python3 tools/presentation.py validate-evidence \
  --evidence fixtures/repository-presentation/minimal.valid.json
python3 tools/presentation.py validate-evidence \
  --evidence fixtures/repository-presentation/rich.valid.json
```

See the
[repository presentation guide](../docs/ecosystem/REPOSITORY_PRESENTATION.md)
for applicability, badge-state derivation, evidence, composition, ownership,
and rollout boundaries.

## Repository continuity policy

`repository-continuity-policy.json` composes an immutable Aether continuity
revision into Hygiene-owned applicability, exact required files, source
precedence, information safety, observe/ratchet/enforce rollout, exceptions,
and v1-to-v2 migration. Its upstream artifact paths and SHA-256 digests are
provenance records, not copied protocol implementations.

```bash
python3 tools/continuity.py validate-profile
python3 tools/continuity.py validate-repository --repository .
```

The profile explicitly records all 29 repositories observed by issue #45. The
older repository architecture catalog remains a visible reconciliation input;
its stale count does not reduce the continuity scope. See the
[repository continuity guide](../docs/ecosystem/REPOSITORY_CONTINUITY.md) for
lifecycle truth, privacy, rollout, exception, downstream, and rollback rules.

## Agent-Ready Web profile

`agent-ready-web-profile.json` is the proposed versioned policy and catalog for
human-first websites that expose explicit machine-readable surfaces. It keeps
readability, capability, efficiency, and commerce independent; defines stable
site classes, requirement strengths, maturity, compatibility, extensions, and
ownership; and requires primary references plus registration evidence.

Checkpoint 2 registers the bounded discovery and efficient-representation
catalog from issue #51. Each entry declares applicability, a rule for every
site class, content and validation expectations, maturity, and authoritative
references. The global representation policy defines source equivalence,
freshness, canonical URLs, provenance, drift, privacy, typed alternate
discovery, and deterministic HTTP content negotiation. Emerging and
experimental entries remain non-blocking. Interactive capabilities,
advertising declarations, and commerce semantics remain deferred.

```bash
python3 tools/agent_ready_web.py validate-profile
python3 tools/agent_ready_web.py validate-fixtures
```

See the
[Agent-Ready Web profile guide](../docs/ecosystem/AGENT_READY_WEB.md) for the
catalog matrix, applicability and absence behavior, representation-integrity
rules, compatibility model, ownership split, and checkpoint exclusions.
