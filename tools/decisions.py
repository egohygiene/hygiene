#!/usr/bin/env python3
"""Validate decoded Ego Hygiene ADR and policy-inheritance contracts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


DECISION_SCHEMA = "egohygiene.architecture-decision/v1"
POLICY_REFERENCE_SCHEMA = (
    "egohygiene.architecture-decision-policy-reference/v1"
)
DECISION_STATUSES = {
    "proposed",
    "accepted",
    "rejected",
    "superseded",
    "deprecated",
}
IMPLEMENTATION_STATUSES = {
    "not_started",
    "in_progress",
    "implemented",
    "verified",
    "not_applicable",
    "unknown",
}
DECISION_FIELDS = {
    "schema",
    "id",
    "title",
    "status",
    "date",
    "decision_scope",
    "visibility",
    "owners",
    "issue",
    "pull_request",
    "related",
    "supersedes",
    "superseded_by",
    "affected_repositories",
    "affected_contracts",
    "implementation_status",
    "evidence",
    "exceptions",
    "approval",
    "extensions",
}
DECISION_REQUIRED_FIELDS = DECISION_FIELDS - {"extensions"}
POLICY_REFERENCE_FIELDS = {
    "schema",
    "repository",
    "policy",
    "decision_directory",
    "index",
    "extensions",
    "exceptions",
}
ADR_ID = re.compile(r"^ADR-[0-9]{3,4}$")
DECISION_REFERENCE = re.compile(
    r"^(ADR-[0-9]{3,4}|[a-z0-9][a-z0-9.-]*/"
    r"[a-z0-9][a-z0-9.-]*#ADR-[0-9]{3,4})$"
)
REPOSITORY = re.compile(r"^egohygiene/(\.github|[a-z0-9][a-z0-9.-]*|\*)$")
LOCAL_REPOSITORY = re.compile(r"^egohygiene/(\.github|[a-z0-9][a-z0-9.-]*)$")
CONTRACT_ID = re.compile(r"^egohygiene\.[a-z0-9][a-z0-9.-]*/v[0-9]+$")
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
REVISION = re.compile(r"^[0-9a-f]{40}$")
RELATIVE_PATH = re.compile(r"^[A-Za-z0-9._/-]+$")


def load_object(path: Path) -> dict[str, Any]:
    """Load a JSON object without accepting ambiguous top-level values."""

    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("document root must be an object")
    return value


def _is_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return dt.date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _is_uri(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlsplit(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_safe_relative_path(value: Any, *, suffix: str | None = None) -> bool:
    if not isinstance(value, str) or not RELATIVE_PATH.fullmatch(value):
        return False
    if value.startswith("/") or ".." in Path(value).parts:
        return False
    return suffix is None or value.endswith(suffix)


def _unique_strings(
    value: Any,
    path: str,
    *,
    allow_empty: bool,
    pattern: re.Pattern[str] | None = None,
) -> list[str]:
    if not isinstance(value, list):
        return [f"E_TYPE {path} must be an array"]
    errors: list[str] = []
    if not allow_empty and not value:
        errors.append(f"E_EMPTY {path} must not be empty")
    if any(not isinstance(item, str) or not item for item in value):
        errors.append(f"E_TYPE {path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"E_DUPLICATE {path} must not contain duplicates")
    if pattern and any(not pattern.fullmatch(item) for item in strings):
        errors.append(f"E_FORMAT {path} contains an invalid value")
    return errors


def _validate_approval(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"E_APPROVAL {path} must be an object"]
    fields = {"date", "by", "evidence"}
    errors: list[str] = []
    if set(value) != fields:
        errors.append(f"E_FIELDS {path} fields must be: {', '.join(sorted(fields))}")
    if not _is_date(value.get("date")):
        errors.append(f"E_DATE {path}.date must be an ISO date")
    if not isinstance(value.get("by"), str) or not value["by"].strip():
        errors.append(f"E_TYPE {path}.by must be a non-empty string")
    if not _is_uri(value.get("evidence")):
        errors.append(f"E_URI {path}.evidence must be an HTTP(S) URI")
    return errors


def _validate_evidence(value: Any, path: str) -> list[str]:
    if not isinstance(value, list):
        return [f"E_TYPE {path} must be an array"]
    errors: list[str] = []
    allowed_types = {
        "approval",
        "issue",
        "pull_request",
        "commit",
        "release",
        "workflow_run",
        "documentation",
        "implementation",
        "validation",
        "external",
    }
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"E_TYPE {item_path} must be an object")
            continue
        if set(item) != {"type", "url", "description"}:
            errors.append(
                f"E_FIELDS {item_path} fields must be: description, type, url"
            )
        if item.get("type") not in allowed_types:
            errors.append(f"E_ENUM {item_path}.type is invalid")
        if not _is_uri(item.get("url")):
            errors.append(f"E_URI {item_path}.url must be an HTTP(S) URI")
        description = item.get("description")
        if not isinstance(description, str) or not 1 <= len(description) <= 240:
            errors.append(
                f"E_LENGTH {item_path}.description must contain 1-240 characters"
            )
    return errors


def _validate_exceptions(value: Any, path: str) -> list[str]:
    if not isinstance(value, list):
        return [f"E_TYPE {path} must be an array"]
    errors: list[str] = []
    fields = {
        "rule",
        "reason",
        "status",
        "owner",
        "approval_evidence",
        "expires",
    }
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"E_TYPE {item_path} must be an object")
            continue
        if set(item) != fields:
            errors.append(
                f"E_FIELDS {item_path} fields must be: {', '.join(sorted(fields))}"
            )
        for field in ("rule", "reason", "owner"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"E_TYPE {item_path}.{field} must be non-empty")
        reason = item.get("reason")
        if isinstance(reason, str) and len(reason) > 500:
            errors.append(f"E_LENGTH {item_path}.reason must not exceed 500 characters")
        if item.get("status") not in {"proposed", "approved", "expired"}:
            errors.append(f"E_ENUM {item_path}.status is invalid")
        approval = item.get("approval_evidence")
        if approval is not None and not _is_uri(approval):
            errors.append(
                f"E_URI {item_path}.approval_evidence must be null or an HTTP(S) URI"
            )
        if item.get("status") == "approved" and not _is_uri(approval):
            errors.append(
                f"E_APPROVAL {item_path}.approval_evidence is required when approved"
            )
        expires = item.get("expires")
        if expires is not None and not _is_date(expires):
            errors.append(f"E_DATE {item_path}.expires must be null or an ISO date")
    return errors


def validate_decision(document: dict[str, Any]) -> list[str]:
    """Return stable contract errors for decoded ADR front matter."""

    errors: list[str] = []
    missing = DECISION_REQUIRED_FIELDS - set(document)
    unknown = set(document) - DECISION_FIELDS
    if missing:
        errors.append(f"E_REQUIRED missing fields: {', '.join(sorted(missing))}")
    if unknown:
        errors.append(f"E_OVERRIDE unknown top-level fields: {', '.join(sorted(unknown))}")
    if document.get("schema") != DECISION_SCHEMA:
        errors.append(f"E_SCHEMA schema must be {DECISION_SCHEMA}")
    if not isinstance(document.get("id"), str) or not ADR_ID.fullmatch(document["id"]):
        errors.append("E_ID id must match ADR-NNN or preserved ADR-NNNN")
    title = document.get("title")
    if not isinstance(title, str) or not 1 <= len(title) <= 160:
        errors.append("E_TITLE title must contain 1-160 characters")
    status = document.get("status")
    if status not in DECISION_STATUSES:
        errors.append("E_STATUS status is invalid")
    if not _is_date(document.get("date")):
        errors.append("E_DATE date must be an ISO date")
    if document.get("decision_scope") not in {"repository", "organization"}:
        errors.append("E_SCOPE decision_scope is invalid")
    if document.get("visibility") not in {"public", "internal", "private"}:
        errors.append("E_VISIBILITY visibility is invalid")
    errors.extend(_unique_strings(document.get("owners"), "owners", allow_empty=False))
    for field in ("issue", "pull_request"):
        value = document.get(field)
        if value is not None and (
            not _is_uri(value) or not value.startswith("https://github.com/")
        ):
            errors.append(f"E_GITHUB_URL {field} must be null or a GitHub URL")
    for field in ("related", "supersedes", "superseded_by"):
        errors.extend(
            _unique_strings(
                document.get(field),
                field,
                allow_empty=True,
                pattern=DECISION_REFERENCE,
            )
        )
    errors.extend(
        _unique_strings(
            document.get("affected_repositories"),
            "affected_repositories",
            allow_empty=False,
            pattern=REPOSITORY,
        )
    )
    errors.extend(
        _unique_strings(
            document.get("affected_contracts"),
            "affected_contracts",
            allow_empty=True,
            pattern=CONTRACT_ID,
        )
    )
    implementation_status = document.get("implementation_status")
    if implementation_status not in IMPLEMENTATION_STATUSES:
        errors.append("E_IMPLEMENTATION_STATUS implementation_status is invalid")
    evidence = document.get("evidence")
    errors.extend(_validate_evidence(evidence, "evidence"))
    errors.extend(_validate_exceptions(document.get("exceptions"), "exceptions"))

    approval = document.get("approval")
    if status == "proposed":
        if approval is not None:
            errors.append("E_FALSE_APPROVAL proposed decisions require approval: null")
    elif status in DECISION_STATUSES:
        errors.extend(_validate_approval(approval, "approval"))
        if isinstance(approval, dict) and isinstance(evidence, list):
            approval_url = approval.get("evidence")
            matching_evidence = any(
                isinstance(item, dict)
                and item.get("type") == "approval"
                and item.get("url") == approval_url
                for item in evidence
            )
            if not matching_evidence:
                errors.append(
                    "E_APPROVAL_EVIDENCE approval.evidence must match an "
                    "evidence item of type approval"
                )

    superseded_by = document.get("superseded_by")
    if isinstance(superseded_by, list):
        if status == "superseded" and not superseded_by:
            errors.append("E_SUPERSESSION superseded decisions require superseded_by")
        if status in {"proposed", "rejected", "deprecated"} and superseded_by:
            errors.append(f"E_SUPERSESSION {status} decisions cannot set superseded_by")
    if implementation_status == "verified" and isinstance(evidence, list) and not evidence:
        errors.append("E_VERIFICATION verified decisions require evidence")

    extensions = document.get("extensions", {})
    if not isinstance(extensions, dict):
        errors.append("E_EXTENSIONS extensions must be an object")
    else:
        for extension_id, payload in extensions.items():
            if not isinstance(extension_id, str) or not CONTRACT_ID.fullmatch(extension_id):
                errors.append(
                    f"E_EXTENSION_ID extension key {extension_id!r} must be a contract ID"
                )
            if not isinstance(payload, dict):
                errors.append(
                    f"E_EXTENSION_TYPE extensions.{extension_id} must be an object"
                )
    return sorted(set(errors))


def validate_decision_set(documents: list[dict[str, Any]]) -> list[str]:
    """Validate repository-local IDs, references, supersession, and cycles."""

    errors: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, document in enumerate(documents):
        decision_id = document.get("id")
        label = decision_id if isinstance(decision_id, str) else f"document[{index}]"
        errors.extend(
            f"E_DOCUMENT {label}: {error}"
            for error in validate_decision(document)
        )
        if isinstance(decision_id, str):
            if decision_id in by_id:
                errors.append(f"E_DUPLICATE_ID duplicate local ID: {decision_id}")
            else:
                by_id[decision_id] = document

    for decision_id, document in by_id.items():
        for field in ("related", "supersedes", "superseded_by"):
            references = document.get(field)
            if not isinstance(references, list):
                continue
            for reference in references:
                if isinstance(reference, str) and ADR_ID.fullmatch(reference):
                    if reference == decision_id:
                        errors.append(
                            f"E_SELF_REFERENCE {decision_id}.{field} references itself"
                        )
                    elif reference not in by_id:
                        errors.append(
                            f"E_DANGLING_REFERENCE {decision_id}.{field} -> {reference}"
                        )

        supersedes = document.get("supersedes")
        if isinstance(supersedes, list):
            for predecessor_id in supersedes:
                predecessor = by_id.get(predecessor_id)
                if predecessor is None:
                    continue
                backlinks = predecessor.get("superseded_by")
                if not isinstance(backlinks, list) or decision_id not in backlinks:
                    errors.append(
                        f"E_SUPERSESSION_BACKLINK {decision_id} -> {predecessor_id} "
                        "is not linked through superseded_by"
                    )

        superseded_by = document.get("superseded_by")
        if isinstance(superseded_by, list):
            for replacement_id in superseded_by:
                replacement = by_id.get(replacement_id)
                if replacement is None:
                    continue
                if replacement.get("status") not in {"accepted", "superseded"}:
                    errors.append(
                        f"E_SUPERSESSION_AUTHORITY {decision_id} replacement "
                        f"{replacement_id} is not accepted"
                    )
                forward = replacement.get("supersedes")
                if not isinstance(forward, list) or decision_id not in forward:
                    errors.append(
                        f"E_SUPERSESSION_FORWARD {decision_id} <- {replacement_id} "
                        "is not linked through supersedes"
                    )

    graph: dict[str, list[str]] = {
        decision_id: [
            reference
            for reference in document.get("supersedes", [])
            if isinstance(reference, str) and reference in by_id
        ]
        for decision_id, document in by_id.items()
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(decision_id: str, trail: tuple[str, ...]) -> None:
        if decision_id in visiting:
            start = trail.index(decision_id)
            cycle = trail[start:] + (decision_id,)
            errors.append(f"E_SUPERSESSION_CYCLE {' -> '.join(cycle)}")
            return
        if decision_id in visited:
            return
        visiting.add(decision_id)
        for predecessor_id in graph[decision_id]:
            visit(predecessor_id, trail + (decision_id,))
        visiting.remove(decision_id)
        visited.add(decision_id)

    for decision_id in sorted(graph):
        visit(decision_id, ())
    return sorted(set(errors))


def validate_policy_reference(document: dict[str, Any]) -> list[str]:
    """Return stable errors for a repository ADR policy inheritance reference."""

    errors: list[str] = []
    missing = POLICY_REFERENCE_FIELDS - set(document)
    unknown = set(document) - POLICY_REFERENCE_FIELDS
    if missing:
        errors.append(f"E_REQUIRED missing fields: {', '.join(sorted(missing))}")
    if unknown:
        errors.append(f"E_OVERRIDE unknown top-level fields: {', '.join(sorted(unknown))}")
    if document.get("schema") != POLICY_REFERENCE_SCHEMA:
        errors.append(f"E_SCHEMA schema must be {POLICY_REFERENCE_SCHEMA}")
    repository = document.get("repository")
    if not isinstance(repository, str) or not LOCAL_REPOSITORY.fullmatch(repository):
        errors.append("E_REPOSITORY repository must name one egohygiene repository")

    policy = document.get("policy")
    if not isinstance(policy, dict):
        errors.append("E_POLICY policy must be an object")
    else:
        if set(policy) != {"contract", "version", "source"}:
            errors.append("E_POLICY_FIELDS policy fields must be: contract, source, version")
        if policy.get("contract") != DECISION_SCHEMA:
            errors.append(f"E_POLICY_CONTRACT policy.contract must be {DECISION_SCHEMA}")
        version = policy.get("version")
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            errors.append("E_POLICY_VERSION policy.version must be semantic version x.y.z")
        source = policy.get("source")
        if not isinstance(source, dict):
            errors.append("E_POLICY_SOURCE policy.source must be an object")
        else:
            if set(source) != {"repository", "revision", "path"}:
                errors.append(
                    "E_POLICY_SOURCE_FIELDS policy.source fields must be: "
                    "path, repository, revision"
                )
            if source.get("repository") != "egohygiene/hygiene":
                errors.append("E_POLICY_OWNER policy.source.repository must be egohygiene/hygiene")
            revision = source.get("revision")
            if not isinstance(revision, str) or not REVISION.fullmatch(revision):
                errors.append("E_POLICY_PIN policy.source.revision must be a full commit SHA")
            if source.get("path") != "docs/decisions/POLICY.md":
                errors.append(
                    "E_POLICY_PATH policy.source.path must be docs/decisions/POLICY.md"
                )

    if not _is_safe_relative_path(document.get("decision_directory")):
        errors.append("E_DECISION_DIRECTORY decision_directory must be a safe relative path")
    if not _is_safe_relative_path(document.get("index"), suffix=".md"):
        errors.append("E_INDEX index must be a safe relative Markdown path")

    extensions = document.get("extensions")
    if not isinstance(extensions, list):
        errors.append("E_EXTENSIONS extensions must be an array")
    else:
        extension_ids: list[str] = []
        for index, extension in enumerate(extensions):
            path = f"extensions[{index}]"
            if not isinstance(extension, dict):
                errors.append(f"E_TYPE {path} must be an object")
                continue
            if set(extension) != {"id", "kind", "schema", "required"}:
                errors.append(
                    f"E_FIELDS {path} fields must be: id, kind, required, schema"
                )
            extension_id = extension.get("id")
            if not isinstance(extension_id, str) or not CONTRACT_ID.fullmatch(extension_id):
                errors.append(f"E_EXTENSION_ID {path}.id must be a contract ID")
            else:
                extension_ids.append(extension_id)
            if extension.get("kind") not in {"metadata", "validation"}:
                errors.append(f"E_EXTENSION_KIND {path}.kind is invalid")
            schema = extension.get("schema")
            if (
                not _is_safe_relative_path(schema, suffix=".json")
                or not schema.startswith("schemas/")
            ):
                errors.append(
                    f"E_EXTENSION_SCHEMA {path}.schema must be a local "
                    "schemas/*.json path"
                )
            if not isinstance(extension.get("required"), bool):
                errors.append(f"E_EXTENSION_REQUIRED {path}.required must be boolean")
        if len(extension_ids) != len(set(extension_ids)):
            errors.append("E_EXTENSION_DUPLICATE extension IDs must be unique")

    errors.extend(_validate_exceptions(document.get("exceptions"), "exceptions"))
    return sorted(set(errors))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("decision", "policy-reference"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--input", type=Path, required=True)
    decision_set = subparsers.add_parser("decision-set")
    decision_set.add_argument("--input", type=Path, action="append", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        documents = (
            [load_object(path) for path in args.input]
            if args.command == "decision-set"
            else [load_object(args.input)]
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"E_LOAD {error}", file=sys.stderr)
        return 2
    if args.command == "decision":
        errors = validate_decision(documents[0])
    elif args.command == "decision-set":
        errors = validate_decision_set(documents)
    else:
        errors = validate_policy_reference(documents[0])
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    for path in args.input if isinstance(args.input, list) else [args.input]:
        print(f"valid: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
