#!/usr/bin/env python3
"""Validate and render the Ego Hygiene repository catalog contract."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"
REPOSITORY_NAME_PATTERN = re.compile(r"(?:\.github|[a-z0-9][a-z0-9.-]*)")
LIFECYCLES = {"seed", "incubating", "active", "transition", "architecture-first", "unknown"}
VISIBILITIES = {"public", "private"}
REPOSITORY_FIELDS = {
    "name",
    "full_name",
    "visibility",
    "plane",
    "lifecycle",
    "maturity",
    "owns",
    "excludes",
    "consumes",
    "outputs",
    "domains",
    "source_url",
}


def load_catalog(path: Path) -> dict[str, Any]:
    """Load the JSON-compatible YAML 1.2 catalog without third-party code."""

    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("catalog root must be an object")
    return value


def _unique_strings(value: Any, path: str, *, allow_empty: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return [f"{path} must be an array"]
    if not allow_empty and not value:
        errors.append(f"{path} must not be empty")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{path} must contain non-empty strings")
    if len(value) != len(set(item for item in value if isinstance(item, str))):
        errors.append(f"{path} must not contain duplicates")
    return errors


def _valid_repository_name(value: Any) -> bool:
    return isinstance(value, str) and REPOSITORY_NAME_PATTERN.fullmatch(value) is not None


def resolve_name(catalog: dict[str, Any], value: str) -> str | None:
    """Resolve only a declared historical alias; never guess a rename."""
    name = value.removeprefix("egohygiene/")
    for repository in catalog.get("repositories", []):
        if isinstance(repository, dict) and (repository.get("name") == name
                or name in repository.get("aliases", [])):
            return repository["full_name"]
    return None


def _instant(value: Any) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        return False
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") == value
    except ValueError:
        return False


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    """Return deterministic semantic validation errors."""

    errors: list[str] = []
    if catalog.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if catalog.get("organization") != "egohygiene":
        errors.append("organization must be egohygiene")
    public_inventory = catalog.get("public_inventory")
    if public_inventory is not None:
        if (not isinstance(public_inventory, dict) or set(public_inventory) != {"observed_at", "source"}
                or not _instant(public_inventory.get("observed_at"))):
            errors.append("public_inventory observation boundary is incompatible")
        else:
            public_source = public_inventory.get("source")
            if (not isinstance(public_source, dict) or set(public_source) != {"provider", "scope", "completeness", "url"}
                    or public_source.get("provider") != "github" or public_source.get("scope") != "public"
                    or public_source.get("completeness") not in {"complete", "partial"}
                    or public_source.get("url") != "https://api.github.com/orgs/egohygiene/repos?type=public&per_page=100"):
                errors.append("public_inventory source is incompatible")

    planes = catalog.get("planes")
    if not isinstance(planes, list) or not planes:
        errors.append("planes must be a non-empty array")
        plane_ids: set[str] = set()
    else:
        plane_ids = {plane.get("id") for plane in planes if isinstance(plane, dict)}
        if len(plane_ids) != len(planes) or None in plane_ids:
            errors.append("plane ids must be present and unique")

    repositories = catalog.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        errors.append("repositories must be a non-empty array")
        repositories = []

    names: list[str] = []
    for index, repository in enumerate(repositories):
        prefix = f"repositories[{index}]"
        if not isinstance(repository, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = repository.get("name")
        if not _valid_repository_name(name):
            errors.append(f"{prefix}.name must match the catalog repository-name grammar")
            continue
        names.append(name)
        if "target_name" in repository and not _valid_repository_name(repository["target_name"]):
            errors.append(f"{prefix}.target_name must match the catalog repository-name grammar")
        missing = REPOSITORY_FIELDS - repository.keys()
        if missing:
            errors.append(f"{prefix} is missing: {', '.join(sorted(missing))}")
        if repository.get("full_name") != f"egohygiene/{name}":
            errors.append(f"{prefix}.full_name must be egohygiene/{name}")
        if repository.get("source_url") != f"https://github.com/egohygiene/{name}":
            errors.append(f"{prefix}.source_url does not match the repository")
        if repository.get("plane") not in plane_ids and repository.get("plane") != "unknown":
            errors.append(f"{prefix}.plane is not declared")
        if repository.get("visibility") not in VISIBILITIES:
            errors.append(f"{prefix}.visibility is invalid")
        if repository.get("lifecycle") not in LIFECYCLES:
            errors.append(f"{prefix}.lifecycle is invalid")
        for field in ("owns", "outputs"):
            errors.extend(_unique_strings(repository.get(field), f"{prefix}.{field}", allow_empty=False))
        errors.extend(_unique_strings(repository.get("excludes"), f"{prefix}.excludes",
            allow_empty=repository.get("plane") == "unknown"))
        for field in ("consumes", "domains"):
            errors.extend(_unique_strings(repository.get(field), f"{prefix}.{field}", allow_empty=True))
        aliases = repository.get("aliases", [])
        errors.extend(_unique_strings(aliases, f"{prefix}.aliases", allow_empty=True))
        if isinstance(aliases, list) and any(not _valid_repository_name(alias) or alias == name for alias in aliases):
            errors.append(f"{prefix}.aliases must contain distinct historical repository names")
        if "public_observation" in repository:
            observed = repository["public_observation"]
            if (not isinstance(observed, dict) or set(observed) != {"repository_id", "default_branch", "archived", "observed_at", "source_url"}
                    or type(observed.get("repository_id")) is not int or not 1 <= observed["repository_id"] <= 9007199254740991
                    or not isinstance(observed.get("default_branch"), str) or not observed["default_branch"]
                    or type(observed.get("archived")) is not bool or not _instant(observed.get("observed_at"))
                    or observed.get("source_url") != f"https://api.github.com/repos/egohygiene/{name}"
                    or repository.get("visibility") != "public"):
                errors.append(f"{prefix}.public_observation is incompatible")
            elif isinstance(public_inventory, dict) and observed["observed_at"] != public_inventory.get("observed_at"):
                errors.append(f"{prefix}.public_observation must match the public inventory boundary")
        if "role_evidence" in repository:
            errors.extend(_unique_strings(repository["role_evidence"], f"{prefix}.role_evidence", allow_empty=False))
        if repository.get("plane") == "unknown" and not repository.get("role_evidence"):
            errors.append(f"{prefix}.role_evidence must identify the unclassified owner's declaration")
        if "next_gate" in repository:
            gate = repository["next_gate"]
            if not isinstance(gate, dict) or set(gate) != {"state", "description", "source_url", "source_observed_at"}:
                errors.append(f"{prefix}.next_gate is incompatible")
            elif gate.get("state") == "unknown":
                if any(gate.get(key) is not None for key in ("description", "source_url", "source_observed_at")):
                    errors.append(f"{prefix}.next_gate unknown must retain null evidence")
            elif gate.get("state") != "source-declared" or not all(isinstance(gate.get(key), str) and gate[key] for key in ("description", "source_url", "source_observed_at")):
                errors.append(f"{prefix}.next_gate must preserve declared evidence or unknown")

    if len(names) != len(set(names)):
        errors.append("repository names must be unique")
    aliases = [alias for repository in repositories if isinstance(repository, dict)
        and isinstance(repository.get("aliases", []), list)
        for alias in repository.get("aliases", []) if isinstance(alias, str)]
    if len(aliases) != len(set(aliases)) or set(aliases) & set(names):
        errors.append("historical aliases must be unique and must not shadow canonical names")
    if catalog.get("repository_count") != len(repositories):
        errors.append("repository_count must equal the repositories array length")
    canonical = catalog.get("canonical_repository")
    if canonical not in names:
        errors.append("canonical_repository must name a current repository")

    proposed = catalog.get("proposed_repositories")
    if not isinstance(proposed, list):
        errors.append("proposed_repositories must be an array")
        proposed = []
    proposed_names: list[str] = []
    for index, repository in enumerate(proposed):
        prefix = f"proposed_repositories[{index}]"
        if not isinstance(repository, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = repository.get("name")
        if not _valid_repository_name(name):
            errors.append(f"{prefix}.name must match the catalog repository-name grammar")
            continue
        proposed_names.append(name)
        if repository.get("status") != "deferred":
            errors.append(f"{prefix}.status must be deferred")
        if not repository.get("create_after"):
            errors.append(f"{prefix}.create_after must be set")
        if repository.get("target_full_name") != f"egohygiene/{name}":
            errors.append(f"{prefix}.target_full_name must be egohygiene/{name}")
    overlap = set(names) & set(proposed_names)
    if overlap:
        errors.append(f"proposed repositories already exist: {', '.join(sorted(overlap))}")
    if len(proposed_names) != len(set(proposed_names)):
        errors.append("proposed repository names must be unique")

    return sorted(set(errors))


def _cell(value: Any) -> str:
    text = ", ".join(value) if isinstance(value, list) else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(catalog: dict[str, Any]) -> str:
    """Render the stable human repository view."""

    repositories = catalog["repositories"]
    lines = [
        "# Generated repository catalog",
        "",
        "> Generated by `python3 tools/catalog.py render`. Do not edit by hand.",
        "",
        f"- Architecture release: `{catalog['architecture_release']}`",
        f"- Observed: `{catalog['observed_at']}`",
        f"- Current repositories: `{len(repositories)}`",
        "",
    ]
    planes = [*catalog["planes"]]
    if any(repository["plane"] == "unknown" for repository in repositories):
        planes.append({"id": "unknown", "title": "Unclassified owner declarations"})
    for plane in planes:
        lines.extend([
            f"## {plane['title']}",
            "",
            "| Repository | Lifecycle | Maturity | Owns | Does not own | Outputs |",
            "| --- | --- | --- | --- | --- | --- |",
        ])
        for repository in repositories:
            if repository["plane"] != plane["id"]:
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"[`{repository['name']}`]({repository['source_url']})",
                        _cell(repository["lifecycle"]),
                        _cell(repository["maturity"]),
                        _cell(repository["owns"]),
                        _cell(repository["excludes"]),
                        _cell(repository["outputs"]),
                    ]
                )
                + " |"
            )
        lines.append("")
    lines.extend(["## Deferred repository boundaries", ""])
    for repository in catalog["proposed_repositories"]:
        lines.append(
            f"- `{repository['name']}` - create only after `{repository['create_after']}`."
        )
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("catalog/repositories.yaml"),
        help="path to the JSON-compatible YAML catalog",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate the catalog")
    render = subparsers.add_parser("render", help="write the generated Markdown view")
    render.add_argument("--output", type=Path, required=True)
    check = subparsers.add_parser("check-generated", help="check the generated Markdown view")
    check.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        catalog = load_catalog(args.catalog)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"catalog load failed: {error}", file=sys.stderr)
        return 2
    errors = validate_catalog(catalog)
    if errors:
        for error in errors:
            print(f"catalog validation failed: {error}", file=sys.stderr)
        return 1
    if args.command == "validate":
        print(f"catalog valid: {len(catalog['repositories'])} repositories")
        return 0
    rendered = render_markdown(catalog)
    if args.command == "render":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
        return 0
    current = args.output.read_text(encoding="utf-8") if args.output.exists() else ""
    if current != rendered:
        print(f"generated catalog is stale: {args.output}", file=sys.stderr)
        return 1
    print(f"generated catalog current: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
