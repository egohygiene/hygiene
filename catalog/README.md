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
