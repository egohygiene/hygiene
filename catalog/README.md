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
