#!/usr/bin/env python3
"""Validate and render repository-local ecosystem context projections."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

import catalog as repository_catalog


SCHEMA_VERSION = "1.0.0"
SOURCE_REPOSITORY = "egohygiene/hygiene"
REVISION_PATTERN = re.compile(r"^[0-9a-f]{40}$")
MARKER = "<!-- egohygiene-context: repository-context/v1 -->"


def load_json(path: Path) -> dict[str, Any]:
    """Load one dependency-free JSON contract."""

    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _unique_strings(value: Any, path: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be an array"]
    errors: list[str] = []
    if not allow_empty and not value:
        errors.append(f"{path} must not be empty")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"{path} must not contain duplicates")
    return errors


def validate_policy(catalog: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    """Return stable errors for the context policy and catalog relationship map."""

    errors = repository_catalog.validate_catalog(catalog)
    for field in ("schema_version", "context_version"):
        if policy.get(field) != SCHEMA_VERSION:
            errors.append(f"{field} must be {SCHEMA_VERSION}")
    if policy.get("architecture_release") != catalog.get("architecture_release"):
        errors.append("context architecture_release must match the repository catalog")
    if policy.get("source_catalog") != "catalog/repositories.yaml":
        errors.append("source_catalog must be catalog/repositories.yaml")

    generator = policy.get("generator")
    if not isinstance(generator, dict):
        errors.append("generator must be an object")
    elif generator != {
        "id": "egohygiene/hygiene:repository-context",
        "version": SCHEMA_VERSION,
    }:
        errors.append("generator identity must be the version-1 Hygiene context generator")

    required_sections = policy.get("required_sections")
    errors.extend(_unique_strings(required_sections, "required_sections", allow_empty=False))
    expected_sections = {
        "identity",
        "ownership",
        "dependencies",
        "neighbors",
        "constraints",
        "links",
        "upgrade",
    }
    if isinstance(required_sections, list) and set(required_sections) != expected_sections:
        errors.append("required_sections must declare every version-1 context section")
    errors.extend(
        _unique_strings(policy.get("global_constraints"), "global_constraints", allow_empty=False)
    )

    repositories = {
        item["full_name"] for item in catalog.get("repositories", []) if isinstance(item, dict)
    }
    dependency_sources = policy.get("dependency_sources")
    if not isinstance(dependency_sources, dict):
        return sorted(set(errors + ["dependency_sources must be an object"]))
    consumed_inputs = {
        value
        for repository in catalog.get("repositories", [])
        for value in repository.get("consumes", [])
    }
    missing = consumed_inputs - dependency_sources.keys()
    extra = dependency_sources.keys() - consumed_inputs
    if missing:
        errors.append(f"dependency_sources is missing: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"dependency_sources is unused: {', '.join(sorted(extra))}")
    for source_name, producers in dependency_sources.items():
        errors.extend(_unique_strings(producers, f"dependency_sources.{source_name}"))
        if isinstance(producers, list):
            unknown = set(producers) - repositories
            if unknown:
                errors.append(
                    f"dependency_sources.{source_name} references unknown repositories: "
                    + ", ".join(sorted(unknown))
                )

    links = policy.get("canonical_links")
    expected_links = {"architecture", "agent_context", "catalog", "decisions", "migration"}
    if not isinstance(links, dict) or set(links) != expected_links:
        errors.append("canonical_links must declare the five version-1 Hygiene links")
    elif any(
        not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts
        for path in links.values()
    ):
        errors.append("canonical_links must contain normalized repository-relative paths")

    stale = policy.get("stale_behavior")
    if stale != {
        "comparison_key": "architecture_release",
        "on_mismatch": "fail",
        "upgrade_owner": "egohygiene/pace",
        "upgrade_action": (
            "Regenerate from the pinned Hygiene release and review the resulting pull request."
        ),
    }:
        errors.append("stale_behavior must fail closed and route upgrades through Pace")
    return sorted(set(errors))


def _repository_index(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {repository["full_name"]: repository for repository in catalog["repositories"]}


def build_context(
    catalog: dict[str, Any],
    policy: dict[str, Any],
    repository_name: str,
    source_revision: str,
) -> dict[str, Any]:
    """Build one deterministic machine-readable repository projection."""

    errors = validate_policy(catalog, policy)
    if errors:
        raise ValueError("; ".join(errors))
    if not REVISION_PATTERN.fullmatch(source_revision):
        raise ValueError("source revision must be a 40-character lowercase Git commit")
    full_name = (
        repository_name if "/" in repository_name else f"{catalog['organization']}/{repository_name}"
    )
    repositories = _repository_index(catalog)
    if full_name not in repositories:
        raise ValueError(f"unknown repository: {repository_name}")
    repository = repositories[full_name]
    mapping = policy["dependency_sources"]
    upstream = sorted(
        {
            producer
            for consumed_input in repository["consumes"]
            for producer in mapping[consumed_input]
            if producer != full_name
        }
    )
    external_inputs = sorted(
        consumed_input
        for consumed_input in repository["consumes"]
        if not mapping[consumed_input]
    )
    downstream = sorted(
        candidate["full_name"]
        for candidate in catalog["repositories"]
        if candidate["full_name"] != full_name
        and full_name
        in {
            producer
            for consumed_input in candidate["consumes"]
            for producer in mapping[consumed_input]
        }
    )
    base_url = "https://github.com/egohygiene/hygiene/blob/" + source_revision + "/"
    constraints = list(policy["global_constraints"])
    constraints.extend(
        f"Do not absorb or claim ownership of {excluded}." for excluded in repository["excludes"]
    )
    generator = policy["generator"]
    return {
        "schema_version": SCHEMA_VERSION,
        "context_version": policy["context_version"],
        "architecture_release": policy["architecture_release"],
        "repository": full_name,
        "source": {
            "repository": SOURCE_REPOSITORY,
            "revision": source_revision,
            "catalog": policy["source_catalog"],
            "generator": f"{generator['id']}@{generator['version']}",
        },
        "identity": {
            "plane": repository["plane"],
            "visibility": repository["visibility"],
            "lifecycle": repository["lifecycle"],
            "maturity": repository["maturity"],
            "domains": sorted(repository["domains"]),
        },
        "ownership": {
            "owns": list(repository["owns"]),
            "does_not_own": list(repository["excludes"]),
            "publishes": list(repository["outputs"]),
        },
        "dependencies": {
            "repositories": upstream,
            "inputs": list(repository["consumes"]),
            "external_inputs": external_inputs,
        },
        "neighbors": {"upstream": upstream, "downstream": downstream},
        "constraints": constraints,
        "links": {
            "repository": repository["source_url"],
            **{
                name: base_url + path for name, path in sorted(policy["canonical_links"].items())
            },
        },
        "upgrade": {
            "comparison_key": policy["stale_behavior"]["comparison_key"],
            "on_mismatch": policy["stale_behavior"]["on_mismatch"],
            "owner": policy["stale_behavior"]["upgrade_owner"],
            "action": policy["stale_behavior"]["upgrade_action"],
        },
    }


def _list(values: list[str], empty: str = "None declared.") -> list[str]:
    return [f"- {value}" for value in values] if values else [f"- {empty}"]


def render_markdown(context: dict[str, Any]) -> str:
    """Render a stable, human-readable context projection."""

    source = context["source"]
    identity = context["identity"]
    ownership = context["ownership"]
    dependencies = context["dependencies"]
    neighbors = context["neighbors"]
    lines = [
        MARKER,
        "---",
        f'schema-version: "{context["schema_version"]}"',
        f'context-version: "{context["context_version"]}"',
        f'architecture-release: "{context["architecture_release"]}"',
        f'repository: "{context["repository"]}"',
        f'source-repository: "{source["repository"]}"',
        f'source-revision: "{source["revision"]}"',
        f'generated-by: "{source["generator"]}"',
        "---",
        "",
        f'# Ecosystem context for `{context["repository"]}`',
        "",
        "> Generated from the pinned Hygiene catalog. Do not edit this projection by hand.",
        "",
        "## Identity",
        "",
        f'- Plane: `{identity["plane"]}`',
        f'- Visibility: `{identity["visibility"]}`',
        f'- Lifecycle: `{identity["lifecycle"]}`',
        f'- Maturity: `{identity["maturity"]}`',
        "",
        "## Ownership",
        "",
        "### Owns",
        "",
        *_list(ownership["owns"]),
        "",
        "### Does not own",
        "",
        *_list(ownership["does_not_own"]),
        "",
        "### Publishes",
        "",
        *_list(ownership["publishes"]),
        "",
        "## Dependencies",
        "",
        "### Repository inputs",
        "",
        *_list(dependencies["repositories"]),
        "",
        "### Consumed contracts and artifacts",
        "",
        *_list(dependencies["inputs"]),
        "",
        "## Neighbors",
        "",
        "### Upstream",
        "",
        *_list(neighbors["upstream"]),
        "",
        "### Downstream",
        "",
        *_list(neighbors["downstream"]),
        "",
        "## Constraints",
        "",
        *_list(context["constraints"]),
        "",
        "## Canonical links",
        "",
        *[
            f'- [{name.replace("_", " ").title()}]({url})'
            for name, url in sorted(context["links"].items())
        ],
        "",
        "## Upgrade and stale-context behavior",
        "",
        f'- Compare `{context["upgrade"]["comparison_key"]}` with the selected Hygiene release.',
        f'- On mismatch: `{context["upgrade"]["on_mismatch"]}`.',
        f'- Upgrade owner: `{context["upgrade"]["owner"]}`.',
        f'- Action: {context["upgrade"]["action"]}',
        "",
    ]
    return "\n".join(lines)


def render_egolint_contract(policy: dict[str, Any], source_revision: str) -> str:
    """Render the canonical offline repository contract consumed by EgoLint."""

    if not REVISION_PATTERN.fullmatch(source_revision):
        raise ValueError("source revision must be a 40-character lowercase Git commit")
    generator = policy["generator"]
    return f'''schema-version = 1
id = "hygiene-repository-context"
version = "{policy["context_version"]}"
profile = "hygiene/repository-context"
provisional = false

[source]
repository = "egohygiene/hygiene"
revision = "{source_revision}"
revision-kind = "git-commit"
path = "catalog/repository-context.json"
decision = "https://github.com/egohygiene/hygiene/issues/6"

[[requirements]]
id = "agent-instructions"
path = "AGENTS.md"
kind = "file"
ownership = "required"

[[requirements]]
id = "ecosystem-context"
path = "docs/ecosystem/CONTEXT.md"
kind = "file"
ownership = "generated"
markers = [
  "{MARKER}",
  "architecture-release: \\"{policy["architecture_release"]}\\"",
  "generated-by: \\"{generator["id"]}@{generator["version"]}\\"",
]
'''


def _write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def _check(path: Path, contents: str) -> bool:
    return path.exists() and path.read_text(encoding="utf-8") == contents


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("catalog/repositories.yaml"))
    parser.add_argument("--policy", type=Path, default=Path("catalog/repository-context.json"))
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    for command in ("render", "check"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--repository", required=True)
        subparser.add_argument("--source-revision", required=True)
        subparser.add_argument("--output", type=Path, required=True)
    render_all = subparsers.add_parser("render-all")
    render_all.add_argument("--source-revision", required=True)
    render_all.add_argument("--output-directory", type=Path, required=True)
    for command in ("render-contract", "check-contract"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--source-revision", required=True)
        subparser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        catalog = repository_catalog.load_catalog(arguments.catalog)
        policy = load_json(arguments.policy)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"context contract load failed: {error}", file=sys.stderr)
        return 2
    errors = validate_policy(catalog, policy)
    if errors:
        for error in errors:
            print(f"context contract validation failed: {error}", file=sys.stderr)
        return 1
    if arguments.command == "validate":
        print(f"context contract valid: {len(catalog['repositories'])} repositories")
        return 0
    try:
        if arguments.command in {"render", "check"}:
            context = build_context(
                catalog, policy, arguments.repository, arguments.source_revision
            )
            rendered = render_markdown(context)
            if arguments.command == "render":
                _write(arguments.output, rendered)
                print(f"wrote {arguments.output}")
                return 0
            if not _check(arguments.output, rendered):
                print(f"generated context is stale: {arguments.output}", file=sys.stderr)
                return 1
            print(f"generated context current: {arguments.output}")
            return 0
        if arguments.command == "render-all":
            for repository in catalog["repositories"]:
                context = build_context(
                    catalog, policy, repository["full_name"], arguments.source_revision
                )
                _write(
                    arguments.output_directory / f"{repository['name']}.md",
                    render_markdown(context),
                )
            print(
                f"wrote {len(catalog['repositories'])} contexts to "
                f"{arguments.output_directory}"
            )
            return 0
        rendered = render_egolint_contract(policy, arguments.source_revision)
        if arguments.command == "render-contract":
            _write(arguments.output, rendered)
            print(f"wrote {arguments.output}")
            return 0
        if not _check(arguments.output, rendered):
            print(f"generated EgoLint contract is stale: {arguments.output}", file=sys.stderr)
            return 1
        print(f"generated EgoLint contract current: {arguments.output}")
        return 0
    except (OSError, ValueError) as error:
        print(f"context generation failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
