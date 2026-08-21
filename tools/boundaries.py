#!/usr/bin/env python3
"""Validate, render, and scan the Ego Hygiene dependency-boundary contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.0.0"
REQUIRED_RULES = {f"BOUNDARY-{number:03d}" for number in range(1, 8)}
INTERFACE_TYPES = {
    "api",
    "binary",
    "generated-projection",
    "oci-image",
    "package",
    "reusable-workflow",
    "schema",
}
PINNING_POLICIES = {"immutable", "immutable-or-versioned", "versioned"}
CONTRACT_STATUSES = {"active", "required"}
EXCEPTION_STATUSES = {"approved", "expired", "proposed"}
DEFAULT_BRANCHES = "main|master|develop|trunk|HEAD"
IGNORED_DIRECTORIES = {
    ".dart_tool",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "target",
    "vendor",
}
COPY_CONTAINER_DIRECTORIES = {".staging", "third_party", "vendor", "vendored"}
DEPENDENCY_FILENAMES = {
    ".gitmodules",
    "Cargo.lock",
    "Cargo.toml",
    "Dockerfile",
    "compose.yaml",
    "compose.yml",
    "deno.json",
    "deno.jsonc",
    "go.mod",
    "package-lock.json",
    "package.json",
    "pnpm-lock.yaml",
    "pubspec.lock",
    "pubspec.yaml",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
    "yarn.lock",
}
DEPENDENCY_SUFFIXES = {".json", ".toml", ".yaml", ".yml"}
MAX_SCANNED_BYTES = 1_000_000


@dataclass(frozen=True, order=True)
class Finding:
    """A stable repository-boundary scan result."""

    rule: str
    path: str
    line: int
    message: str


def load_object(path: Path) -> dict[str, Any]:
    """Load a JSON-compatible YAML 1.2 object without third-party code."""

    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be an object")
    return value


def _repository_names(catalog: dict[str, Any]) -> set[str]:
    repositories = catalog.get("repositories")
    if not isinstance(repositories, list):
        return set()
    return {
        repository["full_name"]
        for repository in repositories
        if isinstance(repository, dict) and isinstance(repository.get("full_name"), str)
    }


def _duplicate_values(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _validate_repository_reference(
    value: Any,
    path: str,
    repositories: set[str],
    *,
    allow_wildcard: bool,
) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{path} must be a non-empty repository reference"]
    if allow_wildcard and value == "egohygiene/*":
        return []
    if value not in repositories:
        return [f"{path} references unknown repository {value}"]
    return []


def validate_register(
    register: dict[str, Any],
    catalog: dict[str, Any],
    contract_index: dict[str, Any],
) -> list[str]:
    """Return deterministic semantic errors for a boundary register."""

    errors: list[str] = []
    repositories = _repository_names(catalog)
    contracts = contract_index.get("contracts")
    if not isinstance(contracts, list):
        errors.append("contract index contracts must be an array")
        contracts = []
    contract_statuses = {
        contract.get("id"): contract.get("status")
        for contract in contracts
        if isinstance(contract, dict) and isinstance(contract.get("id"), str)
    }
    for duplicate in _duplicate_values(
        contract.get("id")
        for contract in contracts
        if isinstance(contract, dict) and isinstance(contract.get("id"), str)
    ):
        errors.append(f"duplicate contract id: {duplicate}")

    if register.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if register.get("architecture_release") != catalog.get("architecture_release"):
        errors.append("architecture_release must match the repository catalog")
    if register.get("organization") != "egohygiene":
        errors.append("organization must be egohygiene")
    if register.get("canonical_repository") != "egohygiene/hygiene":
        errors.append("canonical_repository must be egohygiene/hygiene")
    if register.get("governed_by") != ["ADR-0001"]:
        errors.append("governed_by must contain ADR-0001")

    expected_policy = {
        "integration": "versioned-public-contract",
        "pinning": "immutable-or-versioned",
        "copied_sibling_source": "forbidden",
        "mutable_default_branch": "forbidden",
        "unknown_dependency": "deny",
    }
    if register.get("default_policy") != expected_policy:
        errors.append("default_policy must fail closed with versioned interfaces")

    rules = register.get("rules")
    if not isinstance(rules, list) or not rules:
        errors.append("rules must be a non-empty array")
        rules = []
    rule_ids: list[str] = []
    for index, rule in enumerate(rules):
        path = f"rules[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{path} must be an object")
            continue
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not re.fullmatch(r"BOUNDARY-[0-9]{3}", rule_id):
            errors.append(f"{path}.id must match BOUNDARY-NNN")
        else:
            rule_ids.append(rule_id)
        if rule.get("severity") not in {"error", "warning"}:
            errors.append(f"{path}.severity is invalid")
        for field in ("title", "statement"):
            if not isinstance(rule.get(field), str) or not rule[field].strip():
                errors.append(f"{path}.{field} must be a non-empty string")
    for duplicate in _duplicate_values(rule_ids):
        errors.append(f"duplicate rule id: {duplicate}")
    missing_rules = REQUIRED_RULES - set(rule_ids)
    if missing_rules:
        errors.append(f"required rules missing: {', '.join(sorted(missing_rules))}")

    relationships = register.get("relationships")
    if not isinstance(relationships, list) or not relationships:
        errors.append("relationships must be a non-empty array")
        relationships = []
    relationship_ids: list[str] = []
    for index, relationship in enumerate(relationships):
        path = f"relationships[{index}]"
        if not isinstance(relationship, dict):
            errors.append(f"{path} must be an object")
            continue
        relationship_id = relationship.get("id")
        if not isinstance(relationship_id, str) or not re.fullmatch(
            r"RELATIONSHIP-[0-9]{3}", relationship_id
        ):
            errors.append(f"{path}.id must match RELATIONSHIP-NNN")
        else:
            relationship_ids.append(relationship_id)
        errors.extend(
            _validate_repository_reference(
                relationship.get("producer"),
                f"{path}.producer",
                repositories,
                allow_wildcard=False,
            )
        )
        consumers = relationship.get("consumers")
        if not isinstance(consumers, list) or not consumers:
            errors.append(f"{path}.consumers must be a non-empty array")
        else:
            if len(consumers) != len(set(item for item in consumers if isinstance(item, str))):
                errors.append(f"{path}.consumers must not contain duplicates")
            for consumer_index, consumer in enumerate(consumers):
                errors.extend(
                    _validate_repository_reference(
                        consumer,
                        f"{path}.consumers[{consumer_index}]",
                        repositories,
                        allow_wildcard=True,
                    )
                )
        if not isinstance(relationship.get("capability"), str) or not relationship[
            "capability"
        ].strip():
            errors.append(f"{path}.capability must be a non-empty string")
        interfaces = relationship.get("interfaces")
        if not isinstance(interfaces, list) or not interfaces:
            errors.append(f"{path}.interfaces must be a non-empty array")
        else:
            unknown_interfaces = {
                item for item in interfaces if item not in INTERFACE_TYPES
            }
            if unknown_interfaces:
                errors.append(
                    f"{path}.interfaces contains invalid values: "
                    + ", ".join(sorted(str(item) for item in unknown_interfaces))
                )
            if len(interfaces) != len(set(interfaces)):
                errors.append(f"{path}.interfaces must not contain duplicates")
        contract_status = relationship.get("contract_status")
        contract = relationship.get("contract")
        if contract_status not in CONTRACT_STATUSES:
            errors.append(f"{path}.contract_status is invalid")
        if contract_status == "active" and (
            not isinstance(contract, str) or not contract.strip()
        ):
            errors.append(f"{path}.contract is required when contract_status is active")
        if (
            contract_status == "active"
            and isinstance(contract, str)
            and contract_statuses.get(contract) != "active"
        ):
            errors.append(
                f"{path}.contract must resolve to an active organization contract"
            )
        if contract_status == "required" and contract is not None:
            errors.append(f"{path}.contract must be null until the contract is active")
        if relationship.get("pinning") not in PINNING_POLICIES:
            errors.append(f"{path}.pinning is invalid")
    for duplicate in _duplicate_values(relationship_ids):
        errors.append(f"duplicate relationship id: {duplicate}")

    forbidden = register.get("forbidden_dependencies")
    if not isinstance(forbidden, list):
        errors.append("forbidden_dependencies must be an array")
        forbidden = []
    forbidden_pairs: list[tuple[str, str]] = []
    for index, dependency in enumerate(forbidden):
        path = f"forbidden_dependencies[{index}]"
        if not isinstance(dependency, dict):
            errors.append(f"{path} must be an object")
            continue
        source = dependency.get("source")
        target = dependency.get("target")
        errors.extend(
            _validate_repository_reference(
                source, f"{path}.source", repositories, allow_wildcard=False
            )
        )
        errors.extend(
            _validate_repository_reference(
                target, f"{path}.target", repositories, allow_wildcard=False
            )
        )
        if isinstance(source, str) and isinstance(target, str):
            forbidden_pairs.append((source, target))
            if source == target:
                errors.append(f"{path} must not forbid a self-dependency")
        if dependency.get("rule") not in set(rule_ids):
            errors.append(f"{path}.rule must reference a declared rule")
        if not isinstance(dependency.get("reason"), str) or not dependency[
            "reason"
        ].strip():
            errors.append(f"{path}.reason must be a non-empty string")
    for duplicate in _duplicate_values(
        f"{source}->{target}" for source, target in forbidden_pairs
    ):
        errors.append(f"duplicate forbidden dependency: {duplicate}")

    media_repositories = {
        "egohygiene/aniflow",
        "egohygiene/optiflow",
        "egohygiene/renderflow",
    }
    required_media_pairs = {
        (source, target)
        for source in media_repositories
        for target in media_repositories
        if source != target
    }
    missing_media_pairs = required_media_pairs - set(forbidden_pairs)
    if missing_media_pairs:
        formatted = ", ".join(
            f"{source}->{target}" for source, target in sorted(missing_media_pairs)
        )
        errors.append(f"media sibling prohibitions missing: {formatted}")

    exceptions = register.get("exceptions")
    if not isinstance(exceptions, list):
        errors.append("exceptions must be an array")
        exceptions = []
    exception_ids: list[str] = []
    for index, exception in enumerate(exceptions):
        path = f"exceptions[{index}]"
        if not isinstance(exception, dict):
            errors.append(f"{path} must be an object")
            continue
        exception_id = exception.get("id")
        if not isinstance(exception_id, str) or not re.fullmatch(
            r"EXCEPTION-[0-9]{3}", exception_id
        ):
            errors.append(f"{path}.id must match EXCEPTION-NNN")
        else:
            exception_ids.append(exception_id)
        if exception.get("rule") not in set(rule_ids):
            errors.append(f"{path}.rule must reference a declared rule")
        errors.extend(
            _validate_repository_reference(
                exception.get("owner"),
                f"{path}.owner",
                repositories,
                allow_wildcard=False,
            )
        )
        if not isinstance(exception.get("reason"), str) or not exception[
            "reason"
        ].strip():
            errors.append(f"{path}.reason must be a non-empty string")
        status = exception.get("status")
        approval = exception.get("approval")
        expires_on = exception.get("expires_on")
        if status not in EXCEPTION_STATUSES:
            errors.append(f"{path}.status is invalid")
        if status == "proposed" and approval is not None:
            errors.append(f"{path}.approval must be null while proposed")
        if status in {"approved", "expired"} and not isinstance(approval, str):
            errors.append(f"{path}.approval is required when {status}")
        if not isinstance(expires_on, str):
            errors.append(f"{path}.expires_on is required")
        else:
            try:
                date.fromisoformat(expires_on)
            except ValueError:
                errors.append(f"{path}.expires_on must be an ISO date")
        affected = exception.get("affected_repositories")
        if not isinstance(affected, list) or not affected:
            errors.append(f"{path}.affected_repositories must be a non-empty array")
        else:
            for affected_index, repository in enumerate(affected):
                errors.extend(
                    _validate_repository_reference(
                        repository,
                        f"{path}.affected_repositories[{affected_index}]",
                        repositories,
                        allow_wildcard=False,
                    )
                )
    for duplicate in _duplicate_values(exception_ids):
        errors.append(f"duplicate exception id: {duplicate}")

    return sorted(set(errors))


def render_markdown(register: dict[str, Any]) -> str:
    """Render the stable human view of the dependency-boundary register."""

    lines = [
        "# Generated dependency-boundary register",
        "",
        "> Generated by `python3 tools/boundaries.py render`. Do not edit by hand.",
        "",
        f"- Architecture release: `{register['architecture_release']}`",
        f"- Governing decision: `{', '.join(register['governed_by'])}`",
        f"- Relationships: `{len(register['relationships'])}`",
        "- Active exceptions: "
        f"`{sum(item['status'] == 'approved' for item in register['exceptions'])}`",
        "",
        "## Rules",
        "",
        "| Rule | Severity | Requirement |",
        "| --- | --- | --- |",
    ]
    for rule in sorted(register["rules"], key=lambda item: item["id"]):
        lines.append(
            f"| `{rule['id']}` | {rule['severity']} | {rule['statement']} |"
        )
    lines.extend(
        [
            "",
            "## Allowed relationships",
            "",
            "| ID | Producer | Consumers | Capability | Interfaces | Contract | Pinning |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for relationship in sorted(register["relationships"], key=lambda item: item["id"]):
        consumers = ", ".join(f"`{item}`" for item in relationship["consumers"])
        interfaces = ", ".join(f"`{item}`" for item in relationship["interfaces"])
        contract = (
            f"`{relationship['contract']}`"
            if relationship["contract"] is not None
            else f"_{relationship['contract_status']}_"
        )
        lines.append(
            f"| `{relationship['id']}` | `{relationship['producer']}` | "
            f"{consumers} | {relationship['capability']} | {interfaces} | "
            f"{contract} | `{relationship['pinning']}` |"
        )
    lines.extend(
        [
            "",
            "## Forbidden direct dependencies",
            "",
            "| Source | Target | Rule | Reason |",
            "| --- | --- | --- | --- |",
        ]
    )
    for dependency in sorted(
        register["forbidden_dependencies"],
        key=lambda item: (item["source"], item["target"]),
    ):
        lines.append(
            f"| `{dependency['source']}` | `{dependency['target']}` | "
            f"`{dependency['rule']}` | {dependency['reason']} |"
        )
    lines.extend(["", "## Exceptions", ""])
    if register["exceptions"]:
        lines.extend(
            [
                "| ID | Rule | Owner | Status | Expires |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for exception in sorted(register["exceptions"], key=lambda item: item["id"]):
            lines.append(
                f"| `{exception['id']}` | `{exception['rule']}` | "
                f"`{exception['owner']}` | {exception['status']} | "
                f"`{exception['expires_on']}` |"
            )
    else:
        lines.append("No exceptions are registered.")
    lines.append("")
    return "\n".join(lines)


def _is_dependency_file(relative_path: Path) -> bool:
    if relative_path.name in DEPENDENCY_FILENAMES:
        return True
    if relative_path.name.startswith("Dockerfile"):
        return True
    if relative_path.suffix in DEPENDENCY_SUFFIXES:
        return True
    return relative_path.parts[:2] == (".github", "workflows")


def _iter_dependency_files(repository_root: Path) -> Iterable[Path]:
    for path in sorted(repository_root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(repository_root)
        if any(part in IGNORED_DIRECTORIES for part in relative_path.parts[:-1]):
            continue
        if _is_dependency_file(relative_path) and path.stat().st_size <= MAX_SCANNED_BYTES:
            yield path


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _target_repository(match: re.Match[str]) -> str | None:
    for group_name in ("action_repo", "raw_repo", "github_repo", "git_repo"):
        value = match.groupdict().get(group_name)
        if value:
            return f"egohygiene/{value.removesuffix('.git')}"
    return None


MUTABLE_REFERENCE_PATTERNS = [
    re.compile(
        rf"uses\s*:\s*egohygiene/(?P<action_repo>[a-z0-9.-]+)"
        rf"(?:/[^\s@]+)?@(?:{DEFAULT_BRANCHES})(?=$|[\s#])",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(
        rf"https?://raw\.githubusercontent\.com/egohygiene/"
        rf"(?P<raw_repo>[a-z0-9.-]+)/(?:{DEFAULT_BRANCHES})(?:/|$)",
        re.IGNORECASE,
    ),
    re.compile(
        rf"https?://github\.com/egohygiene/(?P<github_repo>[a-z0-9.-]+)/"
        rf"(?:blob|tree)/(?:{DEFAULT_BRANCHES})(?:/|$)",
        re.IGNORECASE,
    ),
    re.compile(
        rf"https?://github\.com/egohygiene/(?P<git_repo>[a-z0-9.-]+?)"
        rf"(?:\.git)?(?:#|\?ref=)(?:{DEFAULT_BRANCHES})(?=$|[&#\s\"'])",
        re.IGNORECASE,
    ),
    re.compile(
        rf"https?://github\.com/egohygiene/(?P<git_repo>[a-z0-9.-]+?)"
        rf"(?:\.git)?[\s\S]{{0,240}}?(?:branch|ref)\s*[=:]\s*[\"']?"
        rf"(?:{DEFAULT_BRANCHES})(?=$|[\s,}}\"'])",
        re.IGNORECASE,
    ),
]
ESCAPING_PATH_PATTERN = re.compile(
    r"(?:\bpath\s*[=:]\s*[\"']?|[\"']file:)(?:\.\./)+",
    re.IGNORECASE,
)


def scan_repository(
    repository_root: Path,
    repository: str,
    catalog: dict[str, Any],
) -> list[Finding]:
    """Scan dependency surfaces for copied source and mutable sibling refs."""

    repository_root = repository_root.resolve()
    repositories = _repository_names(catalog)
    if repository not in repositories:
        return [
            Finding(
                rule="BOUNDARY-003",
                path=".",
                line=1,
                message=f"repository is not declared in the catalog: {repository}",
            )
        ]

    sibling_names = {
        full_name.split("/", maxsplit=1)[1]
        for full_name in repositories
        if full_name != repository
    }
    findings: set[Finding] = set()

    for path in sorted(repository_root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(repository_root)
        parts = relative_path.parts
        for index, part in enumerate(parts[:-1]):
            if part not in COPY_CONTAINER_DIRECTORIES:
                continue
            candidate = parts[index + 1]
            if candidate in sibling_names:
                findings.add(
                    Finding(
                        rule="BOUNDARY-001",
                        path=relative_path.as_posix(),
                        line=1,
                        message=(
                            "sibling-owned source appears under a copy container: "
                            f"egohygiene/{candidate}"
                        ),
                    )
                )
        if any(part in IGNORED_DIRECTORIES for part in relative_path.parts[:-1]):
            continue

    for path in _iter_dependency_files(repository_root):
        relative_path = path.relative_to(repository_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in ESCAPING_PATH_PATTERN.finditer(text):
            findings.add(
                Finding(
                    rule="BOUNDARY-001",
                    path=relative_path,
                    line=_line_number(text, match.start()),
                    message="dependency path escapes the repository root",
                )
            )
        for pattern in MUTABLE_REFERENCE_PATTERNS:
            for match in pattern.finditer(text):
                target = _target_repository(match)
                if target is None or target == repository or target not in repositories:
                    continue
                findings.add(
                    Finding(
                        rule="BOUNDARY-002",
                        path=relative_path,
                        line=_line_number(text, match.start()),
                        message=f"mutable default-branch dependency on {target}",
                    )
                )
    return sorted(findings)


def _write_findings(findings: list[Finding], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps([asdict(finding) for finding in findings], indent=2, sort_keys=True))
        return
    for finding in findings:
        print(
            f"{finding.rule} {finding.path}:{finding.line}: {finding.message}",
            file=sys.stderr,
        )


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--register",
        type=Path,
        default=Path("catalog/dependency-boundaries.yaml"),
        help="path to the JSON-compatible YAML boundary register",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("catalog/repositories.yaml"),
        help="path to the repository catalog",
    )
    parser.add_argument(
        "--contracts",
        type=Path,
        default=Path("catalog/contracts.yaml"),
        help="path to the organization contract index",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate the register")
    render = subparsers.add_parser("render", help="write the generated Markdown view")
    render.add_argument("--output", type=Path, required=True)
    check = subparsers.add_parser(
        "check-generated", help="check the generated Markdown view"
    )
    check.add_argument("--output", type=Path, required=True)
    scan = subparsers.add_parser("scan", help="scan one repository checkout")
    scan.add_argument("--repository-root", type=Path, required=True)
    scan.add_argument("--repository", required=True)
    scan.add_argument("--format", choices=("json", "text"), default="text")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run a boundary-register command."""

    args = build_parser().parse_args(argv)
    try:
        register = load_object(args.register)
        catalog = load_object(args.catalog)
        contract_index = load_object(args.contracts)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"boundary input load failed: {error}", file=sys.stderr)
        return 2

    errors = validate_register(register, catalog, contract_index)
    if errors:
        for error in errors:
            print(f"boundary validation failed: {error}", file=sys.stderr)
        return 1

    if args.command == "validate":
        print(
            "boundary register valid: "
            f"{len(register['relationships'])} relationships, "
            f"{len(register['exceptions'])} exceptions"
        )
        return 0

    rendered = render_markdown(register)
    if args.command == "render":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
        return 0
    if args.command == "check-generated":
        current = args.output.read_text(encoding="utf-8") if args.output.exists() else ""
        if current != rendered:
            print(f"generated boundary register is stale: {args.output}", file=sys.stderr)
            return 1
        print(f"generated boundary register current: {args.output}")
        return 0

    findings = scan_repository(args.repository_root, args.repository, catalog)
    if findings:
        _write_findings(findings, args.format)
        return 1
    if args.format == "json":
        print("[]")
    else:
        print(f"boundary scan clean: {args.repository}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
