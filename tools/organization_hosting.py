#!/usr/bin/env python3
"""Validate the single organization sealed-export declaration dialect.

The v1 registry and validator retain their original semantics.  The explicit
v2 dialect names the website renderer truthfully for the organization export;
the private v1 validation projection never becomes a declaration or receipt.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from copy import deepcopy
import hashlib
import importlib.util
from pathlib import Path
import re
import sys
from types import ModuleType
from typing import Any


def _load_owner() -> ModuleType:
    """Load adjacent owner modules without importing anything from a consumer."""
    root = Path(__file__).resolve().parent
    namespace = "_hygiene_surfaces_" + hashlib.sha256(str(root).encode()).hexdigest()
    name = namespace + ".site_surfaces"
    if name in sys.modules:
        return sys.modules[name]
    package = ModuleType(namespace)
    package.__path__ = [str(root)]
    sys.modules[namespace] = package
    spec = importlib.util.spec_from_file_location(name, root / "site_surfaces.py")
    if spec is None or spec.loader is None:
        raise ImportError("Adjacent Hygiene surface validator unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        sys.modules.pop(namespace, None)
        raise
    return module


_owner = _load_owner()
load_json = _owner.load_json
canonical_digest = _owner.canonical_digest
validate_registry = _owner.validate_registry

DECLARATION_SCHEMA = "egohygiene.public-site-surface-declaration/v2"
CONTRACT_VERSION = "2.0.0-alpha.1"
HOSTING_PROFILE = "organization-intelligence-static-export/v1"
RENDERER_CONTRACT = "organization-intelligence-static-export"
RENDERER_OWNER = "egohygiene/egohygiene.io"
IMPLEMENTATION_PATH = "scripts/build-intelligence-export.mts"
EXPORT_SURFACES = frozenset({
    "landing", "audits", "compare", "dashboard", "decisions", "dependencies",
    "diagnostics", "distribution", "health", "hygiene", "identity_intelligence",
    "intelligence", "journey", "now", "releases", "roadmap", "sanity", "search",
    "status", "work",
})
REVISION_RE = re.compile(r"[0-9a-f]{40}")


def validate_declaration(
    declaration: Mapping[str, Any],
    registry: Mapping[str, Any],
    expected_registry_revision: str | None = None,
) -> list[str]:
    """Return errors without changing or substituting the supplied declaration.

    V1 delegates unchanged.  V2 selects only the known public organization
    mount; all other route, source, evidence, state and privacy checks remain
    the v1 owner's checks.  Validation establishes no deployment permission,
    live publication, model truth or human approval.
    """
    if not isinstance(declaration, Mapping):
        return ["declaration must be an object"]
    if declaration.get("schema") == _owner.DECLARATION_SCHEMA:
        return _owner.validate_declaration(
            declaration, registry, expected_registry_revision=expected_registry_revision
        )
    errors: list[str] = []
    if set(declaration) != _owner.DECLARATION_FIELDS | {"hosting_profile"}:
        errors.append("declaration fields must exactly match the organization v2 contract")
    if declaration.get("schema") != DECLARATION_SCHEMA:
        errors.append(f"declaration.schema must be {DECLARATION_SCHEMA}")
    if declaration.get("contract_version") != CONTRACT_VERSION:
        errors.append(f"declaration.contract_version must be {CONTRACT_VERSION}")
    if declaration.get("hosting_profile") != HOSTING_PROFILE:
        errors.append(f"declaration.hosting_profile must be {HOSTING_PROFILE}")
    if declaration.get("synthetic") is not False:
        errors.append("organization v2 declarations must explicitly be non-synthetic")
    site = declaration.get("site")
    expected_site = {
        "id": "egohygiene/.github",
        "publication_repository": "egohygiene/.github",
        "origin": "https://egohygiene.github.io",
        "base_path": "/.github/",
        "route_profile": "organization",
        "visibility": "public",
    }
    if not isinstance(site, Mapping):
        return errors + ["declaration.site must be an object"]
    for key, expected in expected_site.items():
        if site.get(key) != expected:
            errors.append(f"declaration.site.{key} must equal {expected}")

    # This copy is only an internal proof of the unchanged shared invariants.
    # Original v2 bytes, website identity and digest remain the public result.
    projected = deepcopy(dict(declaration))
    projected.pop("hosting_profile", None)
    projected["schema"] = _owner.DECLARATION_SCHEMA
    projected["contract_version"] = _owner.CONTRACT_VERSION
    surfaces = projected.get("surfaces")
    if isinstance(surfaces, list):
        producer_revisions: set[str] = set()
        canonical = {
            row["id"]: row for row in registry.get("surfaces", [])
            if isinstance(row, Mapping) and isinstance(row.get("id"), str)
        }
        for index, row in enumerate(surfaces):
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                continue
            surface_id = row["id"]
            renderer = row.get("renderer")
            if surface_id not in EXPORT_SURFACES or renderer is None:
                continue
            path = f"declaration.surfaces[{index}].renderer"
            if not isinstance(renderer, dict):
                errors.append(f"{path} must be null or an object")
                continue
            if set(renderer) != _owner.RENDERER_FIELDS:
                errors.append(f"{path} fields must exactly match the renderer contract")
            if renderer.get("owner") != RENDERER_OWNER:
                errors.append(f"{path}.owner must equal actual renderer owner {RENDERER_OWNER}")
            if renderer.get("contract") != RENDERER_CONTRACT:
                errors.append(f"{path}.contract must be {RENDERER_CONTRACT}")
            revision = renderer.get("version")
            if not isinstance(revision, str) or REVISION_RE.fullmatch(revision) is None:
                errors.append(f"{path}.version must be the full producer commit SHA")
            else:
                producer_revisions.add(revision)
            expected_implementation = (
                f"https://github.com/{RENDERER_OWNER}/blob/{revision}/{IMPLEMENTATION_PATH}"
            )
            if renderer.get("implementation") != expected_implementation:
                errors.append(f"{path}.implementation must bind the exact producer exporter revision")
            if surface_id in canonical:
                old_contract = canonical[surface_id]["renderer_contract"]
                row["renderer"] = {
                    **renderer,
                    "contract": old_contract,
                    "owner": _owner.RENDERER_OWNERS.get(old_contract, site.get("id")),
                }
        if len(producer_revisions) > 1:
            errors.append("organization export renderers must name one exact producer revision")
    errors.extend(_owner.validate_declaration(
        projected, registry, expected_registry_revision=expected_registry_revision
    ))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path(_owner.REGISTRY_PATH))
    parser.add_argument("command", choices=["validate-declaration"])
    parser.add_argument("--declaration", type=Path, required=True)
    parser.add_argument("--registry-revision", required=True)
    args = parser.parse_args(argv)
    try:
        registry = load_json(args.registry)
        errors = validate_registry(registry)
        if not errors:
            errors = validate_declaration(
                load_json(args.declaration), registry,
                expected_registry_revision=args.registry_revision,
            )
    except (OSError, ValueError, TypeError, KeyError, RecursionError):
        print("Organization surface declaration unavailable: invalid input", file=sys.stderr)
        return 2
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("Organization surface declaration valid; publication and human approval remain separate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
