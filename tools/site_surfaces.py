#!/usr/bin/env python3
"""Validate the public-site surface registry and site declarations.

This dependency-free reference checker proves route, ownership, state,
provenance, privacy, and compatibility invariants. Relay owns reusable
workflow execution; Observatory owns read-only aggregation; sites retain final
publication authority.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import sys
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from pathlib import Path, PureWindowsPath
from typing import Any
from urllib.parse import urlsplit


REGISTRY_SCHEMA = "egohygiene.public-site-surface-registry/v1"
DECLARATION_SCHEMA = "egohygiene.public-site-surface-declaration/v1"
CONTRACT_VERSION = "1.0.0-alpha.1"
OWNER = "egohygiene/hygiene"
REGISTRY_PATH = "catalog/public-site-surface-registry.json"

REQUIREMENTS = ["required", "recommended", "optional"]
APPLICABILITY_STATES = ["applicable", "not_applicable", "unknown"]
APPLICABILITY_RULES = ["always", "site-declared"]
IMPLEMENTATION_STATES = [
    "unknown",
    "missing",
    "planned",
    "blocked",
    "implemented",
    "unsupported",
    "not_applicable",
]
PUBLICATION_STATES = [
    "unknown",
    "unpublished",
    "preview",
    "published",
    "withdrawn",
    "not_applicable",
]
FRESHNESS_STATES = ["current", "stale", "unknown", "not_applicable"]
ASSERTIONS = ["authoritative", "inferred", "unknown"]
VISIBILITIES = ["public", "internal", "private"]
DISPOSITIONS = ["owned", "inherited", "omitted"]
SITE_CLASSES = ["application", "commerce", "content", "documentation", "hybrid"]
ROUTE_PROFILES = ["organization", "repository"]

SOURCE_KINDS = {
    "generated-index",
    "identity-artifact",
    "operational-evidence",
    "publication-artifact",
    "repository-content",
    "repository-intelligence",
    "repository-policy",
}
RENDERER_CONTRACTS = {
    "identity-compatible",
    "relay-compatible",
    "renderflow-compatible",
    "site-owned",
}
RENDERER_OWNERS = {
    "identity-compatible": "egohygiene/identity",
    "relay-compatible": "egohygiene/relay",
    "renderflow-compatible": "egohygiene/renderflow",
}
REGISTRY_FIELDS = {
    "schema",
    "version",
    "status",
    "owner",
    "updated",
    "purpose",
    "requirements",
    "applicability_states",
    "applicability_rules",
    "implementation_states",
    "publication_states",
    "freshness_states",
    "assertions",
    "visibilities",
    "dispositions",
    "site_classes",
    "route_profiles",
    "dependency_policy",
    "route_policy",
    "surfaces",
    "compatibility",
    "composition",
    "ownership",
}
SURFACE_FIELDS = {
    "id",
    "title",
    "description",
    "route_bindings",
    "applicability_rule",
    "default_requirement",
    "site_class_overrides",
    "default_owner",
    "source_artifact_kind",
    "renderer_contract",
    "dependencies",
    "related_contracts",
}
DECLARATION_FIELDS = {
    "schema",
    "contract_version",
    "synthetic",
    "registry",
    "site",
    "surfaces",
}
REGISTRY_REFERENCE_FIELDS = {"schema", "version", "source_path", "revision", "sha256"}
ROUTE_PROFILE_FIELDS = {"id", "description"}
ROUTE_BINDING_FIELDS = {"canonical_route", "aliases"}
APPLICABILITY_FIELDS = {
    "state",
    "freshness",
    "assertion",
    "evidence_url",
    "represented_revision",
    "observed_at",
    "reason",
}
DEPENDENCY_POLICY = {
    "meaning": "publication-prerequisite",
    "binding": "route-profile",
    "published_requires_published_dependencies": True,
}
SITE_FIELDS = {
    "id",
    "publication_repository",
    "origin",
    "base_path",
    "route_profile",
    "site_class",
    "visibility",
    "represented_revision",
}
SURFACE_DECLARATION_FIELDS = {
    "id",
    "canonical_route",
    "aliases",
    "requirement",
    "applicability",
    "disposition",
    "owner",
    "publication_owner",
    "source_artifact",
    "renderer",
    "dependencies",
    "publication",
}
SOURCE_FIELDS = {"owner", "kind", "location", "revision"}
RENDERER_FIELDS = {"owner", "contract", "implementation", "version"}
PUBLICATION_FIELDS = {
    "implementation_state",
    "publication_state",
    "visibility",
    "freshness",
    "assertion",
    "canonical_url",
    "evidence_url",
    "represented_revision",
    "observed_at",
    "reason",
    "blocked_by",
}
ROUTE_POLICY = {
    "canonical_routes_are_absolute": True,
    "directory_routes_use_trailing_slash": True,
    "aliases_are_redirects_only": True,
    "aliases_must_not_publish_duplicate_canonical_content": True,
    "query_and_fragment_routes_forbidden": True,
}
COMPATIBILITY_FIELDS = {
    "consumer_pin",
    "unknown_surface_behavior",
    "declaration_coverage",
    "breaking_changes",
}
COMPOSITION_FIELDS = {
    "agent_ready_web",
    "public_site_policy",
    "repository_intelligence",
    "repository_presentation",
    "identity",
    "renderflow",
    "status",
}
OWNERSHIP_FIELDS = {
    "hygiene",
    "subject_repository",
    "publication_repository",
    "identity",
    "holon",
    "relay",
    "observatory",
    "pace",
    "egohygiene_io",
}

ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
DIRECTORY_SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
FILE_SEGMENT_RE = re.compile(
    r"^[a-z0-9][a-z0-9_-]*\.[a-z0-9][a-z0-9._-]*$"
)
SOURCE_LOCATION_RE = re.compile(r"^[A-Za-z0-9._@+-]+(?:/[A-Za-z0-9._@+-]+)*$")
DATETIME_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})$"
)
HOST_LABEL_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"
)
REPOSITORY_RE = re.compile(r"^egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)$")
SYNTHETIC_REPOSITORY_RE = re.compile(
    r"^egohygiene/synthetic-[a-z0-9][a-z0-9.-]*$"
)
CONTRACT_RE = re.compile(r"^egohygiene\.[a-z0-9][a-z0-9.-]*/v[0-9]+$")
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
RENDERER_VERSION_RE = re.compile(
    r"^(?:(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?|[0-9a-f]{40})$"
)


def load_json(path: Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object."""

    with path.open(encoding="utf-8") as stream:
        value = json.load(stream, object_pairs_hook=_object_without_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def canonical_digest(value: Mapping[str, Any]) -> str:
    """Return the SHA-256 digest of canonical UTF-8 JSON."""

    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _typed_json_equal(actual: Any, expected: Any) -> bool:
    """Compare JSON values without conflating booleans and numbers."""

    if isinstance(expected, bool) or isinstance(actual, bool):
        return (
            isinstance(expected, bool)
            and isinstance(actual, bool)
            and actual == expected
        )
    if isinstance(expected, Mapping) or isinstance(actual, Mapping):
        return (
            isinstance(expected, Mapping)
            and isinstance(actual, Mapping)
            and set(actual) == set(expected)
            and all(
                _typed_json_equal(actual[key], expected[key])
                for key in expected
            )
        )
    if isinstance(expected, list) or isinstance(actual, list):
        return (
            isinstance(expected, list)
            and isinstance(actual, list)
            and len(actual) == len(expected)
            and all(
                _typed_json_equal(actual_item, expected_item)
                for actual_item, expected_item in zip(actual, expected)
            )
        )
    return actual == expected


def _is_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _is_datetime(value: Any) -> bool:
    if not isinstance(value, str) or DATETIME_RE.fullmatch(value) is None:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "T" in value and parsed.tzinfo is not None
    except ValueError:
        return False


def _is_hostname(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        labels = value.rstrip(".").split(".")
        return (
            len(value) <= 253
            and bool(labels)
            and all(HOST_LABEL_RE.fullmatch(label) is not None for label in labels)
        )


def _is_https(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("https://"):
        return False
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and bool(parsed.hostname)
        and _is_hostname(parsed.hostname)
        and parsed.username is None
        and parsed.password is None
        and "\\" not in value
        and not any(
            character.isspace() or ord(character) < 32 or ord(character) == 127
            for character in value
        )
        and (port is None or 1 <= port <= 65535)
    )


def _is_origin(value: Any) -> bool:
    if not _is_https(value):
        return False
    parsed = urlsplit(value)
    return (
        parsed.path in {"", "/"}
        and "?" not in value
        and "#" not in value
    )


def _is_canonical_url(value: Any) -> bool:
    if not _is_https(value):
        return False
    parsed = urlsplit(value)
    return "?" not in value and "#" not in value


def _join_site_route(origin: str, base_path: str, route: str) -> str:
    if base_path == "/":
        path = route
    elif route == "/":
        path = base_path
    else:
        path = f"{base_path.rstrip('/')}{route}"
    return f"{origin.rstrip('/')}{path}"


def _validate_route(value: Any, path: str) -> list[str]:
    if not isinstance(value, str) or not value.startswith("/"):
        return [f"{path} must be an absolute route"]
    if any(token in value for token in ("?", "#", "\\", "//", "%")):
        return [f"{path} must not contain query, fragment, encoding, or empty segments"]
    if value == "/":
        return []
    trailing = value.endswith("/")
    body = value[1:-1] if trailing else value[1:]
    segments = body.split("/")
    if not segments or any(SEGMENT_RE.fullmatch(segment) is None for segment in segments[:-1]):
        return [f"{path} contains an invalid route segment"]
    last = segments[-1]
    if trailing and DIRECTORY_SEGMENT_RE.fullmatch(last) is None:
        return [f"{path} contains an invalid directory route segment"]
    if not trailing and FILE_SEGMENT_RE.fullmatch(last) is None:
        return [f"{path} file endpoints require a valid extension"]
    return []


def _validate_base_path(value: Any, path: str) -> list[str]:
    if not isinstance(value, str) or not value.startswith("/"):
        return [f"{path} must be an absolute directory route"]
    if any(token in value for token in ("?", "#", "\\", "//", "%")):
        return [f"{path} must not contain query, fragment, encoding, or empty segments"]
    if value == "/":
        return []
    if not value.endswith("/"):
        return [f"{path} must be a directory route"]
    segments = value[1:-1].split("/")
    if not segments or any(SEGMENT_RE.fullmatch(segment) is None for segment in segments):
        return [f"{path} contains an invalid directory route segment"]
    return []


def _unique_strings(
    value: Any,
    path: str,
    *,
    allow_empty: bool,
    pattern: re.Pattern[str] | None = None,
) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be an array"]
    errors: list[str] = []
    if not allow_empty and not value:
        errors.append(f"{path} must not be empty")
    if any(not _is_text(item) for item in value):
        errors.append(f"{path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"{path} must not contain duplicates")
    if pattern and any(pattern.fullmatch(item) is None for item in strings):
        errors.append(f"{path} contains an invalid value")
    return errors


def _validate_dependency_cycles(
    surfaces: Sequence[Mapping[str, Any]],
    profile: str,
) -> list[str]:
    graph = {
        str(surface.get("id")): [
            dependency
            for dependency in surface.get("dependencies", {}).get(profile, [])
            if isinstance(dependency, str)
        ]
        for surface in surfaces
        if isinstance(surface, Mapping)
        and isinstance(surface.get("dependencies"), Mapping)
        and isinstance(surface.get("dependencies", {}).get(profile), list)
    }
    visiting: set[str] = set()
    visited: set[str] = set()
    errors: list[str] = []

    def visit(node: str, trail: list[str]) -> None:
        if node in visiting:
            start = trail.index(node) if node in trail else 0
            cycle = trail[start:] + [node]
            errors.append(
                f"{profile} surface dependency cycle: {' -> '.join(cycle)}"
            )
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency, trail + [node])
        visiting.remove(node)
        visited.add(node)

    for surface_id in sorted(graph):
        visit(surface_id, [])
    return errors


def validate_registry(
    registry: Mapping[str, Any],
    known_contracts: set[str] | None = None,
) -> list[str]:
    """Return deterministic semantic errors for the canonical registry."""

    errors: list[str] = []
    if set(registry) != REGISTRY_FIELDS:
        errors.append("registry fields must exactly match the v1 contract")
    if registry.get("schema") != REGISTRY_SCHEMA:
        errors.append(f"registry.schema must be {REGISTRY_SCHEMA}")
    if registry.get("version") != CONTRACT_VERSION:
        errors.append(f"registry.version must be {CONTRACT_VERSION}")
    status = registry.get("status")
    if not isinstance(status, str) or status not in {
        "proposed",
        "active",
        "deprecated",
        "superseded",
    }:
        errors.append("registry.status is invalid")
    if registry.get("owner") != OWNER:
        errors.append(f"registry.owner must be {OWNER}")
    if not _is_date(registry.get("updated")):
        errors.append("registry.updated must be an ISO date")
    if not _is_text(registry.get("purpose")):
        errors.append("registry.purpose must be non-empty")

    expected_arrays = {
        "requirements": REQUIREMENTS,
        "applicability_states": APPLICABILITY_STATES,
        "applicability_rules": APPLICABILITY_RULES,
        "implementation_states": IMPLEMENTATION_STATES,
        "publication_states": PUBLICATION_STATES,
        "freshness_states": FRESHNESS_STATES,
        "assertions": ASSERTIONS,
        "visibilities": VISIBILITIES,
        "dispositions": DISPOSITIONS,
        "site_classes": SITE_CLASSES,
    }
    for field, expected in expected_arrays.items():
        if registry.get(field) != expected:
            errors.append(f"registry.{field} must use canonical order")

    route_profiles = registry.get("route_profiles")
    if not isinstance(route_profiles, list):
        errors.append("registry.route_profiles must be an array")
    else:
        profile_ids: list[str] = []
        for index, profile in enumerate(route_profiles):
            path = f"registry.route_profiles[{index}]"
            if not isinstance(profile, dict) or set(profile) != ROUTE_PROFILE_FIELDS:
                errors.append(f"{path} fields must exactly match the v1 route-profile contract")
                continue
            profile_id = profile.get("id")
            if not isinstance(profile_id, str):
                errors.append(f"{path}.id must be a string")
            else:
                profile_ids.append(profile_id)
            if not _is_text(profile.get("description")):
                errors.append(f"{path}.description must be non-empty")
        if profile_ids != ROUTE_PROFILES:
            errors.append("registry.route_profiles must use canonical order")

    if not _typed_json_equal(registry.get("dependency_policy"), DEPENDENCY_POLICY):
        errors.append("registry.dependency_policy must preserve publication prerequisites")

    if not _typed_json_equal(registry.get("route_policy"), ROUTE_POLICY):
        errors.append("registry.route_policy must preserve every v1 route invariant")

    surfaces = registry.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        errors.append("registry.surfaces must be a non-empty array")
        surfaces = []

    surface_ids: list[str] = []
    path_owners: dict[str, dict[str, str]] = {
        profile: {} for profile in ROUTE_PROFILES
    }
    for index, surface in enumerate(surfaces):
        path = f"registry.surfaces[{index}]"
        if not isinstance(surface, dict):
            errors.append(f"{path} must be an object")
            continue
        if set(surface) != SURFACE_FIELDS:
            errors.append(f"{path} fields must exactly match the v1 surface contract")
        surface_id = surface.get("id")
        if not isinstance(surface_id, str) or ID_RE.fullmatch(surface_id) is None:
            errors.append(f"{path}.id is invalid")
            surface_id = f"invalid-{index}"
        surface_ids.append(surface_id)
        for field in ("title", "description"):
            if not _is_text(surface.get(field)):
                errors.append(f"{path}.{field} must be non-empty")

        bindings = surface.get("route_bindings")
        if not isinstance(bindings, dict) or set(bindings) != set(ROUTE_PROFILES):
            errors.append(f"{path}.route_bindings must cover every route profile")
            bindings = {}
        for profile in ROUTE_PROFILES:
            binding_path = f"{path}.route_bindings.{profile}"
            binding = bindings.get(profile)
            if not isinstance(binding, dict) or set(binding) != ROUTE_BINDING_FIELDS:
                errors.append(
                    f"{binding_path} fields must exactly match the v1 route-binding contract"
                )
                continue
            canonical_route = binding.get("canonical_route")
            errors.extend(_validate_route(canonical_route, f"{binding_path}.canonical_route"))
            aliases = binding.get("aliases")
            errors.extend(
                _unique_strings(aliases, f"{binding_path}.aliases", allow_empty=True)
            )
            if isinstance(aliases, list):
                if all(isinstance(alias, str) for alias in aliases) and aliases != sorted(aliases):
                    errors.append(f"{binding_path}.aliases must use stable order")
                for alias_index, alias in enumerate(aliases):
                    errors.extend(
                        _validate_route(alias, f"{binding_path}.aliases[{alias_index}]")
                    )
                    if alias == canonical_route:
                        errors.append(
                            f"{binding_path}.aliases must not repeat the canonical route"
                        )

            for route in [
                canonical_route,
                *(aliases if isinstance(aliases, list) else []),
            ]:
                if not isinstance(route, str):
                    continue
                previous = path_owners[profile].get(route)
                if previous is not None:
                    errors.append(
                        f"{profile} route {route} collides between {previous} and {surface_id}"
                    )
                else:
                    path_owners[profile][route] = surface_id

        if surface.get("applicability_rule") not in APPLICABILITY_RULES:
            errors.append(f"{path}.applicability_rule is invalid")
        if surface.get("default_requirement") not in REQUIREMENTS:
            errors.append(f"{path}.default_requirement is invalid")
        overrides = surface.get("site_class_overrides")
        if not isinstance(overrides, dict) or set(overrides) != set(SITE_CLASSES):
            errors.append(f"{path}.site_class_overrides must cover every site class")
        elif any(value not in REQUIREMENTS for value in overrides.values()):
            errors.append(f"{path}.site_class_overrides contains an invalid requirement")
        owner = surface.get("default_owner")
        if owner != "repository" and (
            not isinstance(owner, str) or REPOSITORY_RE.fullmatch(owner) is None
        ):
            errors.append(f"{path}.default_owner is invalid")
        source_kind = surface.get("source_artifact_kind")
        if not isinstance(source_kind, str) or source_kind not in SOURCE_KINDS:
            errors.append(f"{path}.source_artifact_kind is invalid")
        renderer_contract = surface.get("renderer_contract")
        if (
            not isinstance(renderer_contract, str)
            or renderer_contract not in RENDERER_CONTRACTS
        ):
            errors.append(f"{path}.renderer_contract is invalid")
        dependencies = surface.get("dependencies")
        if not isinstance(dependencies, dict) or set(dependencies) != set(ROUTE_PROFILES):
            errors.append(f"{path}.dependencies must cover every route profile")
        else:
            for profile in ROUTE_PROFILES:
                dependency_path = f"{path}.dependencies.{profile}"
                profile_dependencies = dependencies.get(profile)
                errors.extend(
                    _unique_strings(
                        profile_dependencies,
                        dependency_path,
                        allow_empty=True,
                        pattern=ID_RE,
                    )
                )
                if isinstance(profile_dependencies, list):
                    if (
                        all(
                            isinstance(dependency, str)
                            for dependency in profile_dependencies
                        )
                        and profile_dependencies != sorted(profile_dependencies)
                    ):
                        errors.append(f"{dependency_path} must use stable order")
                    if surface_id in profile_dependencies:
                        errors.append(f"{dependency_path} must not contain itself")
        related = surface.get("related_contracts")
        errors.extend(
            _unique_strings(
                related,
                f"{path}.related_contracts",
                allow_empty=True,
                pattern=CONTRACT_RE,
            )
        )
        if isinstance(related, list):
            if all(isinstance(contract, str) for contract in related) and related != sorted(related):
                errors.append(f"{path}.related_contracts must use stable order")
            if known_contracts is not None:
                for contract in related:
                    if isinstance(contract, str) and contract not in known_contracts:
                        errors.append(f"{path}.related_contracts references unknown {contract}")

    if surface_ids != sorted(surface_ids):
        errors.append("registry.surfaces must use stable id order")
    if len(surface_ids) != len(set(surface_ids)):
        errors.append("registry.surfaces must use unique ids")
    declared_ids = set(surface_ids)
    for index, surface in enumerate(surfaces):
        if not isinstance(surface, dict):
            continue
        dependencies = surface.get("dependencies")
        if not isinstance(dependencies, Mapping):
            continue
        for profile in ROUTE_PROFILES:
            profile_dependencies = dependencies.get(profile)
            if not isinstance(profile_dependencies, list):
                continue
            for dependency in profile_dependencies:
                if isinstance(dependency, str) and dependency not in declared_ids:
                    errors.append(
                        f"registry.surfaces[{index}].dependencies.{profile} "
                        f"references unknown {dependency}"
                    )
    for profile in ROUTE_PROFILES:
        errors.extend(_validate_dependency_cycles(surfaces, profile))

    compatibility = registry.get("compatibility")
    if not isinstance(compatibility, dict) or set(compatibility) != COMPATIBILITY_FIELDS:
        errors.append("registry.compatibility fields must exactly match the v1 contract")
    else:
        if compatibility.get("consumer_pin") != "exact-version-or-immutable-revision":
            errors.append("registry.compatibility.consumer_pin is invalid")
        if compatibility.get("unknown_surface_behavior") != "fail-closed":
            errors.append("registry.compatibility.unknown_surface_behavior is invalid")
        if compatibility.get("declaration_coverage") != "complete":
            errors.append("registry.compatibility.declaration_coverage is invalid")
        errors.extend(
            _unique_strings(
                compatibility.get("breaking_changes"),
                "registry.compatibility.breaking_changes",
                allow_empty=False,
            )
        )

    composition = registry.get("composition")
    if not isinstance(composition, dict) or set(composition) != COMPOSITION_FIELDS:
        errors.append("registry.composition fields must exactly match the v1 contract")
    elif any(not _is_text(value) for value in composition.values()):
        errors.append("registry.composition values must be non-empty")
    ownership = registry.get("ownership")
    if not isinstance(ownership, dict) or set(ownership) != OWNERSHIP_FIELDS:
        errors.append("registry.ownership fields must exactly match the v1 contract")
    elif any(not _is_text(value) for value in ownership.values()):
        errors.append("registry.ownership values must be non-empty")
    return sorted(set(errors))


def resolved_requirement(surface: Mapping[str, Any], site_class: str) -> str | None:
    overrides = surface.get("site_class_overrides")
    if isinstance(overrides, Mapping):
        value = overrides.get(site_class)
        return value if isinstance(value, str) else None
    return None


def _validate_source(value: Any, path: str, expected_kind: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict):
        return [f"{path} must be null or an object"]
    errors: list[str] = []
    if set(value) != SOURCE_FIELDS:
        errors.append(f"{path} fields must exactly match the v1 source contract")
    if not isinstance(value.get("owner"), str) or REPOSITORY_RE.fullmatch(value["owner"]) is None:
        errors.append(f"{path}.owner is invalid")
    if value.get("kind") != expected_kind:
        errors.append(f"{path}.kind must be {expected_kind}")
    location = value.get("location")
    if not _is_text(location):
        errors.append(f"{path}.location must be non-empty")
    elif not _is_https(location):
        first_segment = location.split("/", 1)[0]
        if (
            location.startswith("/")
            or "\\" in location
            or PureWindowsPath(location).drive
            or ":" in first_segment
            or any(segment in {"", ".", ".."} for segment in location.split("/"))
            or any(character in location for character in "?#\x00")
            or SOURCE_LOCATION_RE.fullmatch(location) is None
        ):
            errors.append(f"{path}.location must be repository-relative or HTTPS")
        elif "://" in location:
            errors.append(f"{path}.location external references must use HTTPS")
    if not isinstance(value.get("revision"), str) or REVISION_RE.fullmatch(value["revision"]) is None:
        errors.append(f"{path}.revision must be a full commit SHA")
    return errors


def _validate_renderer(
    value: Any,
    path: str,
    expected_contract: str,
    site_id: str,
) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict):
        return [f"{path} must be null or an object"]
    errors: list[str] = []
    if set(value) != RENDERER_FIELDS:
        errors.append(f"{path} fields must exactly match the v1 renderer contract")
    if not isinstance(value.get("owner"), str) or REPOSITORY_RE.fullmatch(value["owner"]) is None:
        errors.append(f"{path}.owner is invalid")
    if value.get("contract") != expected_contract:
        errors.append(f"{path}.contract must be {expected_contract}")
    expected_owner = RENDERER_OWNERS.get(expected_contract, site_id)
    if value.get("owner") != expected_owner:
        errors.append(
            f"{path}.owner must equal renderer authority {expected_owner}"
        )
    if not _is_text(value.get("implementation")):
        errors.append(f"{path}.implementation must be non-empty")
    version = value.get("version")
    if not isinstance(version, str) or RENDERER_VERSION_RE.fullmatch(version) is None:
        errors.append(f"{path}.version must be an exact semantic version or full commit SHA")
    return errors


def _validate_applicability(
    value: Any,
    path: str,
    *,
    rule: str,
    site_revision: str,
    private: bool,
) -> tuple[list[str], str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"], "unknown"
    errors: list[str] = []
    if set(value) != APPLICABILITY_FIELDS:
        errors.append(f"{path} fields must exactly match the v1 applicability contract")
    state = value.get("state")
    freshness = value.get("freshness")
    assertion = value.get("assertion")
    evidence_url = value.get("evidence_url")
    revision = value.get("represented_revision")
    observed_at = value.get("observed_at")
    reason = value.get("reason")
    if state not in APPLICABILITY_STATES:
        errors.append(f"{path}.state is invalid")
        state = "unknown"
    if freshness not in FRESHNESS_STATES:
        errors.append(f"{path}.freshness is invalid")
        freshness = "__invalid__"
    if assertion not in ASSERTIONS:
        errors.append(f"{path}.assertion is invalid")
        assertion = "__invalid__"
    if evidence_url is not None and not _is_https(evidence_url):
        errors.append(f"{path}.evidence_url must be null or an HTTPS URL")
    if revision is not None and (
        not isinstance(revision, str) or REVISION_RE.fullmatch(revision) is None
    ):
        errors.append(f"{path}.represented_revision must be null or a full commit SHA")
    if observed_at is not None and not _is_datetime(observed_at):
        errors.append(
            f"{path}.observed_at must be null or an ISO date-time with a timezone"
        )
    if reason is not None and not _is_text(reason):
        errors.append(f"{path}.reason must be null or non-empty text")

    evidence_count = sum(
        item is not None for item in (evidence_url, revision, observed_at)
    )
    if evidence_count not in {0, 3}:
        errors.append(
            f"{path} evidence URL, revision, and observation must resolve together"
        )
    if revision is not None:
        if freshness == "current" and revision != site_revision:
            errors.append(
                f"{path}.represented_revision must equal the site revision when current"
            )
        if freshness == "stale" and revision == site_revision:
            errors.append(
                f"{path}.represented_revision must differ from the site revision when stale"
            )
    if private:
        if evidence_count:
            errors.append(f"{path} private surfaces must redact applicability evidence")
        if freshness != "unknown":
            errors.append(f"{path}.freshness must be unknown when private")
    if state == "unknown":
        if rule == "always":
            errors.append(f"{path}.state must be applicable for an always-applicable surface")
        if private:
            if freshness != "unknown" or evidence_count:
                errors.append(
                    f"{path} private unknown applicability must redact assessment evidence"
                )
        else:
            if evidence_count != 3 or freshness not in {"current", "stale"}:
                errors.append(
                    f"{path} unknown applicability requires fresh or stale complete evidence"
                )
        if assertion == "unknown":
            errors.append(
                f"{path}.assertion must not be unknown for an evidence-backed unresolved assessment"
            )
        if not _is_text(reason):
            errors.append(f"{path}.reason is required for unknown applicability")
    elif state == "not_applicable":
        if rule == "always":
            errors.append(f"{path}.state must be applicable for an always-applicable surface")
        if assertion != "authoritative":
            errors.append(
                f"{path}.assertion must be authoritative for not-applicable"
            )
        if not private and (
            freshness not in {"current", "stale"} or evidence_count != 3
        ):
            errors.append(
                f"{path} not-applicable state requires fresh or stale complete evidence"
            )
        if not _is_text(reason):
            errors.append(f"{path}.reason is required for not-applicable")
    else:
        if rule == "always" and state != "applicable":
            errors.append(f"{path}.state must be applicable for an always-applicable surface")
        if assertion == "unknown":
            errors.append(f"{path}.assertion must not be unknown when applicable")
        if not private and (
            evidence_count != 3 or freshness not in {"current", "stale"}
        ):
            errors.append(
                f"{path} applicable state requires fresh or stale complete evidence"
            )
    return errors, str(state)


def _validate_publication(
    publication: Any,
    path: str,
    *,
    applicability_state: str,
    disposition: str,
    route: str,
    site_origin: str,
    site_base_path: str,
    site_revision: str,
    source: Any,
    renderer: Any,
) -> list[str]:
    if not isinstance(publication, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(publication) != PUBLICATION_FIELDS:
        errors.append(f"{path} fields must exactly match the v1 publication contract")
    implementation = publication.get("implementation_state")
    publication_state = publication.get("publication_state")
    visibility = publication.get("visibility")
    freshness = publication.get("freshness")
    assertion = publication.get("assertion")
    if implementation not in IMPLEMENTATION_STATES:
        errors.append(f"{path}.implementation_state is invalid")
        implementation = "__invalid__"
    if publication_state not in PUBLICATION_STATES:
        errors.append(f"{path}.publication_state is invalid")
        publication_state = "__invalid__"
    if visibility not in VISIBILITIES:
        errors.append(f"{path}.visibility is invalid")
        visibility = "__invalid__"
    if freshness not in FRESHNESS_STATES:
        errors.append(f"{path}.freshness is invalid")
        freshness = "__invalid__"
    if assertion not in ASSERTIONS:
        errors.append(f"{path}.assertion is invalid")
        assertion = "__invalid__"

    canonical_url = publication.get("canonical_url")
    evidence_url = publication.get("evidence_url")
    revision = publication.get("represented_revision")
    observed_at = publication.get("observed_at")
    reason = publication.get("reason")
    blocked_by = publication.get("blocked_by")
    errors.extend(_unique_strings(blocked_by, f"{path}.blocked_by", allow_empty=True))

    if canonical_url is not None and not _is_canonical_url(canonical_url):
        errors.append(
            f"{path}.canonical_url must be null or an HTTPS URL without query or fragment"
        )
    if evidence_url is not None and not _is_https(evidence_url):
        errors.append(f"{path}.evidence_url must be null or an HTTPS URL")
    if revision is not None and (
        not isinstance(revision, str) or REVISION_RE.fullmatch(revision) is None
    ):
        errors.append(f"{path}.represented_revision must be null or a full commit SHA")
    if observed_at is not None and not _is_datetime(observed_at):
        errors.append(
            f"{path}.observed_at must be null or an ISO date-time with a timezone"
        )
    if reason is not None and not _is_text(reason):
        errors.append(f"{path}.reason must be null or non-empty text")
    if _is_canonical_url(canonical_url):
        expected_url = _join_site_route(site_origin, site_base_path, route)
        if canonical_url != expected_url:
            errors.append(f"{path}.canonical_url must equal {expected_url}")

    if revision is not None:
        if freshness == "current" and revision != site_revision:
            errors.append(
                f"{path}.represented_revision must equal the site revision when current"
            )
        if freshness == "stale" and revision == site_revision:
            errors.append(
                f"{path}.represented_revision must differ from the site revision when stale"
            )

    if visibility == "private":
        if any(
            value is not None
            for value in (source, renderer, canonical_url, evidence_url, revision, observed_at)
        ):
            errors.append(f"{path} private surfaces must redact publication evidence")
        if applicability_state != "not_applicable" and freshness != "unknown":
            errors.append(f"{path}.freshness must be unknown when private")
        if blocked_by and blocked_by != ["redacted"]:
            errors.append(f"{path}.blocked_by must redact private dependency topology")

    not_applicable_axis = (
        implementation == "not_applicable"
        or publication_state == "not_applicable"
        or freshness == "not_applicable"
    )
    if applicability_state == "not_applicable" or not_applicable_axis:
        if not (
            applicability_state == "not_applicable"
            and disposition == "omitted"
            and implementation == "not_applicable"
            and publication_state == "not_applicable"
            and freshness == "not_applicable"
        ):
            errors.append(f"{path} not-applicable axes must resolve together")
        if assertion != "authoritative":
            errors.append(f"{path}.assertion must be authoritative for not-applicable")
        if any(
            value is not None
            for value in (source, renderer, canonical_url, evidence_url, revision, observed_at)
        ):
            errors.append(
                f"{path} not-applicable surfaces must not expose implementation or publication evidence"
            )
        if not _is_text(reason):
            errors.append(f"{path}.reason is required for not-applicable")
        if blocked_by:
            errors.append(f"{path}.blocked_by must be empty for not-applicable")
        return errors

    if applicability_state == "unknown":
        if not (
            disposition == "omitted"
            and implementation == "unknown"
            and publication_state == "unknown"
            and freshness == "unknown"
            and assertion == "unknown"
        ):
            errors.append(f"{path} unknown applicability must preserve unknown delivery state")
        if any(
            value is not None
            for value in (source, renderer, canonical_url, evidence_url, revision, observed_at)
        ):
            errors.append(f"{path} unknown applicability must not expose delivery evidence")
        if blocked_by:
            errors.append(f"{path}.blocked_by must be empty for unknown applicability")
        if not _is_text(reason):
            errors.append(f"{path}.reason is required for unknown applicability")
        return errors

    if disposition == "omitted" and implementation == "implemented":
        errors.append(f"{path} omitted surfaces cannot be implemented")

    if implementation == "implemented" and publication_state == "published":
        if disposition == "omitted":
            errors.append(f"{path} published surfaces cannot be omitted")
        if visibility != "public":
            errors.append(f"{path}.visibility must be public when published")
        if freshness not in {"current", "stale"}:
            errors.append(f"{path}.freshness must be current or stale when published")
        if assertion == "unknown":
            errors.append(f"{path}.assertion must not be unknown when published")
        if source is None:
            errors.append(f"{path} published surfaces require a source artifact")
        if renderer is None:
            errors.append(f"{path} published surfaces require a renderer")
        if not _is_canonical_url(canonical_url):
            errors.append(f"{path}.canonical_url must be HTTPS when published")
        if not _is_https(evidence_url):
            errors.append(f"{path}.evidence_url must be HTTPS when published")
        if not isinstance(revision, str) or REVISION_RE.fullmatch(revision) is None:
            errors.append(f"{path}.represented_revision must be a full commit SHA when published")
        if not _is_datetime(observed_at):
            errors.append(f"{path}.observed_at must be an ISO date-time when published")
        if reason is not None:
            errors.append(f"{path}.reason must be null when published")
        if blocked_by:
            errors.append(f"{path}.blocked_by must be empty when published")
        return errors

    if implementation == "unknown":
        if publication_state != "unknown" or freshness != "unknown" or assertion != "unknown":
            errors.append(f"{path} unknown implementation must preserve unknown publication, freshness, and assertion")
        if any(
            value is not None
            for value in (
                source,
                renderer,
                canonical_url,
                evidence_url,
                revision,
                observed_at,
            )
        ):
            errors.append(f"{path} unknown implementation must not claim delivery evidence")
        if not _is_text(reason):
            errors.append(f"{path}.reason is required for unknown implementation")
        if blocked_by:
            errors.append(f"{path}.blocked_by must be empty for unknown implementation")
        return errors

    if implementation in {"missing", "planned", "blocked", "unsupported"}:
        if publication_state not in {"unknown", "unpublished"}:
            errors.append(f"{path}.publication_state must be unknown or unpublished before implementation")
        if source is not None or renderer is not None:
            errors.append(f"{path} unimplemented surfaces must not claim source or renderer evidence")
        if canonical_url is not None:
            errors.append(f"{path} unimplemented surfaces must not claim a canonical URL")
        assessment_values = (evidence_url, revision, observed_at)
        evidence_count = sum(value is not None for value in assessment_values)
        if evidence_count not in {0, 3}:
            errors.append(
                f"{path} assessment evidence URL, revision, and observation must resolve together"
            )
        if visibility == "private":
            if evidence_count != 0 or freshness != "unknown":
                errors.append(f"{path} private unimplemented surfaces must redact assessment evidence")
            if assertion == "unknown":
                errors.append(
                    f"{path}.assertion must not be unknown for a known private implementation state"
                )
        else:
            if evidence_count != 3:
                errors.append(
                    f"{path} known unimplemented states require complete assessment evidence"
                )
            if freshness not in {"current", "stale"}:
                errors.append(
                    f"{path}.freshness must be current or stale for a known unimplemented state"
                )
            if assertion == "unknown":
                errors.append(
                    f"{path}.assertion must not be unknown for a known unimplemented state"
                )
        if not _is_text(reason):
            errors.append(f"{path}.reason is required before implementation")
        if implementation == "blocked":
            if not isinstance(blocked_by, list) or not blocked_by:
                errors.append(f"{path}.blocked_by is required when blocked")
        elif blocked_by:
            errors.append(f"{path}.blocked_by must be empty unless blocked")
        return errors

    if implementation == "implemented":
        if assertion == "unknown":
            errors.append(
                f"{path}.assertion must not be unknown for an implemented surface"
            )
        if visibility != "private":
            if source is None:
                errors.append(f"{path} implemented surfaces require a source artifact")
            if renderer is None:
                errors.append(f"{path} implemented surfaces require a renderer")
        if publication_state == "unknown":
            errors.append(f"{path}.publication_state must be known for implemented surfaces")
        if publication_state == "published":
            return errors
        if publication_state == "not_applicable":
            errors.append(f"{path}.publication_state cannot be not_applicable when implemented")
        if publication_state == "unpublished":
            if freshness != "unknown":
                errors.append(f"{path}.freshness must be unknown when unpublished")
            if any(
                value is not None
                for value in (canonical_url, evidence_url, revision, observed_at)
            ):
                errors.append(f"{path} unpublished surfaces must not claim publication evidence")
        if visibility != "private" and publication_state in {"preview", "withdrawn"}:
            if not _is_https(evidence_url):
                errors.append(f"{path}.evidence_url is required for preview or withdrawn state")
            if not isinstance(revision, str) or REVISION_RE.fullmatch(revision) is None:
                errors.append(f"{path}.represented_revision is required for preview or withdrawn state")
            if not _is_datetime(observed_at):
                errors.append(f"{path}.observed_at is required for preview or withdrawn state")
            if freshness not in {"current", "stale"}:
                errors.append(
                    f"{path}.freshness must be current or stale for preview or withdrawn state"
                )
            if assertion == "unknown":
                errors.append(
                    f"{path}.assertion must not be unknown for preview or withdrawn state"
                )
        if not _is_text(reason):
            errors.append(f"{path}.reason is required when implemented but not published")
        if blocked_by:
            errors.append(f"{path}.blocked_by must be empty when implemented")
    return errors


def validate_declaration(
    declaration: Mapping[str, Any],
    registry: Mapping[str, Any],
    expected_registry_revision: str | None = None,
) -> list[str]:
    """Return deterministic semantic errors for one complete site declaration."""

    errors: list[str] = []
    if set(declaration) != DECLARATION_FIELDS:
        errors.append("declaration fields must exactly match the v1 contract")
    if declaration.get("schema") != DECLARATION_SCHEMA:
        errors.append(f"declaration.schema must be {DECLARATION_SCHEMA}")
    if declaration.get("contract_version") != CONTRACT_VERSION:
        errors.append(f"declaration.contract_version must be {CONTRACT_VERSION}")
    if not isinstance(declaration.get("synthetic"), bool):
        errors.append("declaration.synthetic must be a boolean")
    if expected_registry_revision is not None and (
        REVISION_RE.fullmatch(expected_registry_revision) is None
    ):
        errors.append("expected registry revision must be a full commit SHA")
    if declaration.get("synthetic") is False and expected_registry_revision is None:
        errors.append(
            "non-synthetic declarations require an externally resolved registry revision"
        )

    reference = declaration.get("registry")
    if not isinstance(reference, dict) or set(reference) != REGISTRY_REFERENCE_FIELDS:
        errors.append("declaration.registry fields must exactly match the v1 reference contract")
        reference = {}
    if reference.get("schema") != REGISTRY_SCHEMA:
        errors.append(f"declaration.registry.schema must be {REGISTRY_SCHEMA}")
    if reference.get("version") != registry.get("version"):
        errors.append("declaration.registry.version must match the loaded registry")
    if reference.get("source_path") != REGISTRY_PATH:
        errors.append(f"declaration.registry.source_path must be {REGISTRY_PATH}")
    revision = reference.get("revision")
    if not isinstance(revision, str) or REVISION_RE.fullmatch(revision) is None:
        errors.append("declaration.registry.revision must be a full commit SHA")
    elif (
        expected_registry_revision is not None
        and revision != expected_registry_revision
    ):
        errors.append(
            "declaration.registry.revision must match the externally resolved revision"
        )
    digest = reference.get("sha256")
    if not isinstance(digest, str) or DIGEST_RE.fullmatch(digest) is None:
        errors.append("declaration.registry.sha256 must be a SHA-256 digest")
    elif digest != canonical_digest(registry):
        errors.append("declaration.registry.sha256 must match the loaded registry")

    site = declaration.get("site")
    if not isinstance(site, dict) or set(site) != SITE_FIELDS:
        errors.append("declaration.site fields must exactly match the v1 site contract")
        site = {}
    site_id = site.get("id")
    if not isinstance(site_id, str) or REPOSITORY_RE.fullmatch(site_id) is None:
        errors.append("declaration.site.id is invalid")
    publication_repository = site.get("publication_repository")
    if (
        not isinstance(publication_repository, str)
        or REPOSITORY_RE.fullmatch(publication_repository) is None
    ):
        errors.append("declaration.site.publication_repository is invalid")
    origin = site.get("origin")
    if not _is_origin(origin):
        errors.append("declaration.site.origin must be an HTTPS origin")
        origin = "https://invalid.example"
    if declaration.get("synthetic") is True:
        synthetic_site = (
            isinstance(site_id, str)
            and SYNTHETIC_REPOSITORY_RE.fullmatch(site_id) is not None
        )
        synthetic_publisher = (
            isinstance(publication_repository, str)
            and SYNTHETIC_REPOSITORY_RE.fullmatch(publication_repository) is not None
        )
        try:
            synthetic_origin = (
                isinstance(origin, str)
                and urlsplit(origin).hostname is not None
                and urlsplit(origin).hostname.endswith(".invalid")
            )
        except ValueError:
            synthetic_origin = False
        if not (synthetic_site and synthetic_publisher and synthetic_origin):
            errors.append(
                "synthetic declarations require synthetic repository IDs and a .invalid origin"
            )
    base_path = site.get("base_path")
    base_path_errors = _validate_base_path(base_path, "declaration.site.base_path")
    errors.extend(base_path_errors)
    if base_path_errors or not isinstance(base_path, str):
        base_path = "/"
    route_profile = site.get("route_profile")
    if not isinstance(route_profile, str) or route_profile not in ROUTE_PROFILES:
        errors.append("declaration.site.route_profile is invalid")
        route_profile = "repository"
    site_class = site.get("site_class")
    if site_class not in SITE_CLASSES:
        errors.append("declaration.site.site_class is invalid")
    if site.get("visibility") not in VISIBILITIES:
        errors.append("declaration.site.visibility is invalid")
    represented = site.get("represented_revision")
    if not isinstance(represented, str) or REVISION_RE.fullmatch(represented) is None:
        errors.append("declaration.site.represented_revision must be a full commit SHA")

    surfaces = declaration.get("surfaces")
    if not isinstance(surfaces, list):
        errors.append("declaration.surfaces must be an array")
        surfaces = []
    registry_surfaces = {
        surface["id"]: surface
        for surface in registry.get("surfaces", [])
        if isinstance(surface, dict) and isinstance(surface.get("id"), str)
    }
    expected_ids = list(registry_surfaces)
    actual_ids: list[str] = []
    for index, declared in enumerate(surfaces):
        path = f"declaration.surfaces[{index}]"
        if not isinstance(declared, dict):
            errors.append(f"{path} must be an object")
            continue
        if set(declared) != SURFACE_DECLARATION_FIELDS:
            errors.append(f"{path} fields must exactly match the v1 declaration contract")
        surface_id = declared.get("id")
        if not isinstance(surface_id, str) or ID_RE.fullmatch(surface_id) is None:
            errors.append(f"{path}.id is invalid")
            continue
        actual_ids.append(surface_id)
        canonical = registry_surfaces.get(surface_id)
        if canonical is None:
            errors.append(f"{path}.id references unknown surface {surface_id}")
            continue
        route_binding = canonical["route_bindings"][route_profile]
        if declared.get("canonical_route") != route_binding["canonical_route"]:
            errors.append(f"{path}.canonical_route must match the registry")
        if declared.get("aliases") != route_binding["aliases"]:
            errors.append(f"{path}.aliases must match the registry")
        if declared.get("dependencies") != canonical["dependencies"][route_profile]:
            errors.append(f"{path}.dependencies must match the registry")

        requirement = declared.get("requirement")
        resolved = resolved_requirement(canonical, str(site_class))
        if requirement != resolved:
            errors.append(f"{path}.requirement must equal resolved requirement {resolved}")
        declared_publication = declared.get("publication")
        private_surface = (
            isinstance(declared_publication, Mapping)
            and declared_publication.get("visibility") == "private"
        )
        applicability_errors, applicability_state = _validate_applicability(
            declared.get("applicability"),
            f"{path}.applicability",
            rule=canonical["applicability_rule"],
            site_revision=str(represented),
            private=private_surface,
        )
        errors.extend(applicability_errors)
        disposition = declared.get("disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"{path}.disposition is invalid")
            disposition = "__invalid__"
        semantic_owner = declared.get("owner")
        default_owner = canonical["default_owner"]
        if not isinstance(semantic_owner, str) or REPOSITORY_RE.fullmatch(semantic_owner) is None:
            errors.append(f"{path}.owner is invalid")
        elif disposition == "owned" and semantic_owner != site_id:
            errors.append(f"{path}.owner must equal the site for owned surfaces")
        elif disposition == "inherited" and semantic_owner == site_id:
            errors.append(f"{path}.owner must name the upstream owner when inherited")
        elif disposition == "omitted" and semantic_owner != site_id:
            errors.append(f"{path}.owner must retain the site disposition authority when omitted")
        if disposition in {"owned", "inherited"}:
            expected_owner = site_id if default_owner == "repository" else default_owner
            if semantic_owner != expected_owner:
                errors.append(
                    f"{path}.owner must equal registry authority {expected_owner}"
                )
        if declared.get("publication_owner") != publication_repository:
            errors.append(
                f"{path}.publication_owner must equal the site publication repository"
            )

        source = declared.get("source_artifact")
        renderer = declared.get("renderer")
        errors.extend(
            _validate_source(source, f"{path}.source_artifact", canonical["source_artifact_kind"])
        )
        errors.extend(
            _validate_renderer(
                renderer,
                f"{path}.renderer",
                canonical["renderer_contract"],
                str(site_id),
            )
        )
        if (
            disposition in {"owned", "inherited"}
            and isinstance(source, Mapping)
            and source.get("owner") != semantic_owner
        ):
            errors.append(
                f"{path}.source_artifact.owner must equal the semantic owner"
            )
        errors.extend(
            _validate_publication(
                declared.get("publication"),
                f"{path}.publication",
                applicability_state=applicability_state,
                disposition=str(disposition),
                route=route_binding["canonical_route"],
                site_origin=str(origin),
                site_base_path=base_path,
                site_revision=str(represented),
                source=source,
                renderer=renderer,
            )
        )
        publication = declared.get("publication")
        if isinstance(publication, Mapping):
            site_visibility = site.get("visibility")
            surface_visibility = publication.get("visibility")
            allowed_visibility = {
                "public": {"public", "internal", "private"},
                "internal": {"internal", "private"},
                "private": {"private"},
            }
            if (
                isinstance(site_visibility, str)
                and site_visibility in allowed_visibility
                and (
                    not isinstance(surface_visibility, str)
                    or surface_visibility not in allowed_visibility[site_visibility]
                )
            ):
                errors.append(
                    f"{path}.publication.visibility cannot be broader than the site"
                )

    if actual_ids != expected_ids:
        errors.append("declaration.surfaces must cover every registry surface in registry order")
    if len(actual_ids) != len(set(actual_ids)):
        errors.append("declaration.surfaces must use unique ids")
    declared_by_id = {
        item.get("id"): item
        for item in surfaces
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    }
    for index, declared in enumerate(surfaces):
        if not isinstance(declared, Mapping):
            continue
        publication = declared.get("publication")
        if not isinstance(publication, Mapping):
            continue
        if not (
            publication.get("implementation_state") == "implemented"
            and publication.get("publication_state") == "published"
        ):
            continue
        dependencies = declared.get("dependencies", [])
        if not isinstance(dependencies, list):
            continue
        for dependency_id in dependencies:
            if not isinstance(dependency_id, str):
                continue
            dependency = declared_by_id.get(dependency_id)
            dependency_publication = (
                dependency.get("publication")
                if isinstance(dependency, Mapping)
                else None
            )
            if not (
                isinstance(dependency_publication, Mapping)
                and dependency_publication.get("implementation_state") == "implemented"
                and dependency_publication.get("publication_state") == "published"
            ):
                errors.append(
                    f"declaration.surfaces[{index}] published surface requires "
                    f"published dependency {dependency_id}"
                )
    return sorted(set(errors))


def _known_contracts(path: Path) -> set[str]:
    index = load_json(path)
    contracts = index.get("contracts", [])
    return {
        item["id"]
        for item in contracts
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(REGISTRY_PATH),
        help="path to the canonical public-site surface registry",
    )
    parser.add_argument(
        "--contracts",
        type=Path,
        default=Path("catalog/contracts.yaml"),
        help="path to the organization contract index",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-registry", help="validate the canonical registry")
    declaration = subparsers.add_parser(
        "validate-declaration",
        help="validate one complete site declaration",
    )
    declaration.add_argument("--declaration", type=Path, required=True)
    declaration.add_argument(
        "--registry-revision",
        help="externally resolved full registry commit SHA; required for non-synthetic declarations",
    )
    fixtures = subparsers.add_parser(
        "validate-fixtures",
        help="validate every JSON declaration fixture in a directory",
    )
    fixtures.add_argument(
        "--fixtures-directory",
        type=Path,
        default=Path("fixtures/public-site-surfaces"),
    )
    subparsers.add_parser("digest", help="print the canonical registry digest")
    return parser


def _print_errors(prefix: str, errors: Sequence[str]) -> None:
    for error in errors:
        print(f"{prefix}: {error}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        registry = load_json(arguments.registry)
        contracts = _known_contracts(arguments.contracts)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"site-surface load failed: {error}", file=sys.stderr)
        return 2
    registry_errors = validate_registry(registry, contracts)
    if registry_errors:
        _print_errors("registry validation failed", registry_errors)
        return 1
    if arguments.command == "validate-registry":
        print(f"public-site surface registry valid: {len(registry['surfaces'])} surfaces")
        return 0
    if arguments.command == "digest":
        print(canonical_digest(registry))
        return 0
    if arguments.command == "validate-declaration":
        try:
            declaration = load_json(arguments.declaration)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"site declaration load failed: {error}", file=sys.stderr)
            return 2
        errors = validate_declaration(
            declaration,
            registry,
            expected_registry_revision=arguments.registry_revision,
        )
        if errors:
            _print_errors("site declaration validation failed", errors)
            return 1
        print(f"public-site surface declaration valid: {arguments.declaration}")
        return 0
    fixture_paths = sorted(arguments.fixtures_directory.glob("*.valid.json"))
    if not fixture_paths:
        print("site fixture validation failed: no valid fixtures found", file=sys.stderr)
        return 1
    failures = 0
    for fixture_path in fixture_paths:
        try:
            fixture = load_json(fixture_path)
            errors = validate_declaration(fixture, registry)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors = [str(error)]
        if errors:
            failures += 1
            _print_errors(f"{fixture_path} failed", errors)
    if failures:
        return 1
    print(f"public-site surface fixtures valid: {len(fixture_paths)} declarations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
