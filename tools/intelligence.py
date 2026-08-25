#!/usr/bin/env python3
"""Validate the proposed Repository Intelligence reference contract.

This validator intentionally uses only the Python standard library. It proves
the cross-record invariants that JSON Schema cannot express without becoming
the production implementation owned by Egolint and Relay.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA = "egohygiene.repository-intelligence/v1"
CONTRACT_VERSION = "1.0.0-alpha.1"
VOCABULARY_SCHEMA = "egohygiene.repository-intelligence-vocabulary/v1"
REPOSITORY_RE = re.compile(r"^egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SOURCE_ID_RE = re.compile(r"^source:[a-z0-9][a-z0-9._-]*$")
ENTITY_ID_RE = re.compile(
    r"^ri:(?P<repository>egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)):"
    r"(?P<kind>repository|roadmap-step|architecture-decision|issue|"
    r"pull-request|commit|check|release|deployment):"
    r"(?P<key>[A-Za-z0-9][A-Za-z0-9._~@/+:-]*)$"
)
ASSERTIONS = {"authoritative", "inferred", "unknown"}
FRESHNESS = {"current", "stale", "unknown", "not_applicable"}
VISIBILITY_RANK = {"public": 0, "internal": 1, "private": 2}
SOURCE_KINDS = {
    "roadmap",
    "architecture_decision",
    "git",
    "github_issue",
    "github_pull_request",
    "check_provider",
    "release",
    "deployment",
    "manual",
}
ENTITY_KIND_TO_ID = {
    "repository": "repository",
    "roadmap_step": "roadmap-step",
    "architecture_decision": "architecture-decision",
    "issue": "issue",
    "pull_request": "pull-request",
    "commit": "commit",
    "check": "check",
    "release": "release",
    "deployment": "deployment",
}
ENTITY_STATES = {
    "roadmap_step": {
        "complete",
        "active",
        "ready",
        "blocked",
        "planned",
        "deferred",
        "cancelled",
    },
    "architecture_decision": {
        "proposed",
        "accepted",
        "rejected",
        "superseded",
        "deprecated",
    },
    "issue": {"open", "closed"},
    "pull_request": {"open", "merged", "closed"},
}
EVENT_SUBJECT_KINDS = {
    "repository": "repository",
    "roadmap_step": "roadmap_step",
    "architecture_decision": "architecture_decision",
    "issue": "issue",
    "pull_request": "pull_request",
    "commit": "commit",
    "check": "check",
    "release": "release",
    "deployment": "deployment",
}
EVENT_TYPES = {
    "repository.observed",
    "roadmap_step.created",
    "roadmap_step.status_changed",
    "architecture_decision.proposed",
    "architecture_decision.accepted",
    "architecture_decision.rejected",
    "architecture_decision.deprecated",
    "architecture_decision.superseded",
    "issue.opened",
    "issue.closed",
    "issue.reopened",
    "pull_request.opened",
    "pull_request.merged",
    "pull_request.closed",
    "commit.created",
    "check.completed",
    "release.published",
    "deployment.completed",
}
RELATIONSHIP_TYPES = {
    "blocks",
    "depends-on",
    "deploys",
    "evidences",
    "implements",
    "informs",
    "releases",
    "supersedes",
    "tracks",
    "verifies",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object from *path*."""

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _required(mapping: Mapping[str, Any], fields: Iterable[str], path: str) -> list[str]:
    return [f"{path}.{field} is required" for field in fields if field not in mapping]


def _unique_ids(items: Sequence[Any], path: str) -> tuple[dict[str, Mapping[str, Any]], list[str]]:
    index: dict[str, Mapping[str, Any]] = {}
    errors: list[str] = []
    for position, item in enumerate(items):
        item_path = f"{path}[{position}]"
        if not isinstance(item, dict):
            errors.append(f"{item_path} must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{item_path}.id must be a non-empty string")
            continue
        if item_id in index:
            errors.append(f"{path} contains duplicate id {item_id}")
            continue
        index[item_id] = item
    return index, errors


def _validate_stable_order(items: Sequence[Any], key, path: str) -> list[str]:
    comparable = [item for item in items if isinstance(item, dict)]
    try:
        expected = sorted(comparable, key=key)
    except (KeyError, TypeError):
        return []
    if comparable != expected:
        return [f"{path} must use stable contract order"]
    return []


def _timestamp(value: Any, path: str) -> tuple[datetime | None, list[str]]:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None, [f"{path} must be an RFC 3339 UTC timestamp ending in Z"]
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None, [f"{path} must be a valid RFC 3339 timestamp"]
    return parsed, []


def _validate_visibility(value: Any, snapshot_visibility: str, path: str) -> list[str]:
    if value not in VISIBILITY_RANK:
        return [f"{path} must be public, internal, or private"]
    if VISIBILITY_RANK[value] > VISIBILITY_RANK[snapshot_visibility]:
        return [f"{path} exceeds snapshot visibility {snapshot_visibility}"]
    return []


def _validate_provenance(
    references: Any, source_ids: set[str], path: str
) -> list[str]:
    if not isinstance(references, list) or not references:
        return [f"{path} must contain at least one source id"]
    errors: list[str] = []
    if len(references) != len(set(references)):
        errors.append(f"{path} must not contain duplicates")
    for reference in references:
        if reference not in source_ids:
            errors.append(f"{path} references unknown source {reference}")
    return errors


def _validate_common_claim(item: Mapping[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    if item.get("assertion") not in ASSERTIONS:
        errors.append(f"{path}.assertion is invalid")
    if item.get("freshness") not in FRESHNESS:
        errors.append(f"{path}.freshness is invalid")
    return errors


def validate_vocabulary(vocabulary: Mapping[str, Any]) -> list[str]:
    """Validate the relationship vocabulary and return stable diagnostics."""

    errors = _required(
        vocabulary,
        ["schema", "version", "status", "owner", "relationship_types"],
        "vocabulary",
    )
    if vocabulary.get("schema") != VOCABULARY_SCHEMA:
        errors.append(f"vocabulary.schema must be {VOCABULARY_SCHEMA}")
    if vocabulary.get("version") != CONTRACT_VERSION:
        errors.append(f"vocabulary.version must be {CONTRACT_VERSION}")
    if vocabulary.get("owner") != "egohygiene/hygiene":
        errors.append("vocabulary.owner must be egohygiene/hygiene")

    definitions = vocabulary.get("relationship_types")
    if not isinstance(definitions, list):
        errors.append("vocabulary.relationship_types must be an array")
        return sorted(set(errors))

    definitions_by_type: dict[str, Mapping[str, Any]] = {}
    for position, definition in enumerate(definitions):
        path = f"vocabulary.relationship_types[{position}]"
        if not isinstance(definition, dict):
            errors.append(f"{path} must be an object")
            continue
        errors.extend(
            _required(
                definition,
                [
                    "type",
                    "description",
                    "direction",
                    "inverse",
                    "cardinality",
                    "source_kinds",
                    "target_kinds",
                    "transitive",
                ],
                path,
            )
        )
        relation_type = definition.get("type")
        if relation_type in definitions_by_type:
            errors.append(f"vocabulary contains duplicate relationship type {relation_type}")
        elif isinstance(relation_type, str):
            definitions_by_type[relation_type] = definition
        if definition.get("direction") != "directed":
            errors.append(f"{path}.direction must be directed")
        for field in ("source_kinds", "target_kinds"):
            values = definition.get(field)
            if not isinstance(values, list) or not values:
                errors.append(f"{path}.{field} must be a non-empty array")
            elif len(values) != len(set(values)):
                errors.append(f"{path}.{field} must not contain duplicates")

    if set(definitions_by_type) != RELATIONSHIP_TYPES:
        missing = sorted(RELATIONSHIP_TYPES - set(definitions_by_type))
        extra = sorted(set(definitions_by_type) - RELATIONSHIP_TYPES)
        if missing:
            errors.append(f"vocabulary is missing relationship types: {', '.join(missing)}")
        if extra:
            errors.append(f"vocabulary has unknown relationship types: {', '.join(extra)}")
    errors.extend(
        _validate_stable_order(
            definitions,
            lambda item: item["type"],
            "vocabulary.relationship_types",
        )
    )
    return sorted(set(errors))


def _validate_source(
    source: Mapping[str, Any],
    snapshot_visibility: str,
    path: str,
) -> list[str]:
    errors = _required(
        source,
        [
            "id",
            "kind",
            "url",
            "repository",
            "revision",
            "observed_at",
            "visibility",
            "assertion",
            "freshness",
        ],
        path,
    )
    if not isinstance(source.get("id"), str) or not SOURCE_ID_RE.fullmatch(source["id"]):
        errors.append(f"{path}.id is invalid")
    if source.get("kind") not in SOURCE_KINDS:
        errors.append(f"{path}.kind is invalid")
    source_repository = source.get("repository")
    if not isinstance(source_repository, str) or not REPOSITORY_RE.fullmatch(
        source_repository
    ):
        errors.append(f"{path}.repository is invalid")
    revision = source.get("revision")
    if revision is not None and (
        not isinstance(revision, str) or not COMMIT_RE.fullmatch(revision)
    ):
        errors.append(f"{path}.revision must be null or a full lowercase commit SHA")
    _, timestamp_errors = _timestamp(source.get("observed_at"), f"{path}.observed_at")
    errors.extend(timestamp_errors)
    errors.extend(
        _validate_visibility(
            source.get("visibility"), snapshot_visibility, f"{path}.visibility"
        )
    )
    errors.extend(_validate_common_claim(source, path))
    return errors


def _validate_entity(
    entity: Mapping[str, Any],
    snapshot_visibility: str,
    source_ids: set[str],
    path: str,
) -> list[str]:
    errors = _required(
        entity,
        [
            "id",
            "kind",
            "repository",
            "key",
            "title",
            "canonical_url",
            "visibility",
            "state",
            "freshness",
            "provenance",
            "attributes",
            "extensions",
        ],
        path,
    )
    entity_id = entity.get("id")
    match = ENTITY_ID_RE.fullmatch(entity_id) if isinstance(entity_id, str) else None
    if match is None:
        errors.append(f"{path}.id is invalid")
    else:
        if match.group("repository") != entity.get("repository"):
            errors.append(f"{path}.id repository must match entity.repository")
        expected_id_kind = ENTITY_KIND_TO_ID.get(entity.get("kind"))
        if match.group("kind") != expected_id_kind:
            errors.append(f"{path}.id kind does not match entity.kind")
        if match.group("key") != entity.get("key"):
            errors.append(f"{path}.id native key does not match entity.key")
    entity_repository = entity.get("repository")
    if not isinstance(entity_repository, str) or not REPOSITORY_RE.fullmatch(
        entity_repository
    ):
        errors.append(f"{path}.repository is invalid")
    errors.extend(
        _validate_visibility(
            entity.get("visibility"), snapshot_visibility, f"{path}.visibility"
        )
    )
    if entity.get("freshness") not in FRESHNESS:
        errors.append(f"{path}.freshness is invalid")
    state = entity.get("state")
    if not isinstance(state, dict):
        errors.append(f"{path}.state must be an object")
    elif state.get("assertion") not in ASSERTIONS:
        errors.append(f"{path}.state.assertion is invalid")
    if isinstance(state, dict) and entity.get("kind") in ENTITY_STATES:
        if state.get("value") not in ENTITY_STATES[entity["kind"]]:
            errors.append(f"{path}.state.value is invalid for {entity.get('kind')}")
    errors.extend(_validate_provenance(entity.get("provenance"), source_ids, f"{path}.provenance"))

    attributes = entity.get("attributes")
    if not isinstance(attributes, dict):
        errors.append(f"{path}.attributes must be an object")
        return errors
    kind = entity.get("kind")
    if kind == "roadmap_step":
        if not attributes.get("outcome"):
            errors.append(f"{path}.attributes.outcome is required")
        criteria = attributes.get("exit_criteria")
        if not isinstance(criteria, list) or not criteria:
            errors.append(f"{path}.attributes.exit_criteria must be non-empty")
        elif isinstance(state, dict) and state.get("value") == "complete":
            if not all(
                isinstance(item, dict) and item.get("complete") is True
                for item in criteria
            ):
                errors.append(f"{path} is complete but has incomplete exit criteria")
    elif kind == "architecture_decision":
        for field in ("decision_scope", "implementation_status"):
            if field not in attributes:
                errors.append(f"{path}.attributes.{field} is required")
    elif kind in {"issue", "pull_request"}:
        if not isinstance(attributes.get("number"), int) or attributes["number"] < 1:
            errors.append(f"{path}.attributes.number must be a positive integer")
        if kind == "pull_request" and not isinstance(attributes.get("draft"), bool):
            errors.append(f"{path}.attributes.draft must be boolean")
    elif kind == "commit":
        sha = attributes.get("sha")
        if not isinstance(sha, str) or not COMMIT_RE.fullmatch(sha):
            errors.append(f"{path}.attributes.sha must be a full lowercase commit SHA")
        elif sha != entity.get("key"):
            errors.append(f"{path}.attributes.sha must match entity.key")
    elif kind == "check":
        for field in ("name", "status", "conclusion"):
            if field not in attributes:
                errors.append(f"{path}.attributes.{field} is required")
    elif kind == "release":
        if not attributes.get("tag_name"):
            errors.append(f"{path}.attributes.tag_name is required")
        _, timestamp_errors = _timestamp(
            attributes.get("published_at"), f"{path}.attributes.published_at"
        )
        errors.extend(timestamp_errors)
    elif kind == "deployment":
        for field in ("environment", "status"):
            if not attributes.get(field):
                errors.append(f"{path}.attributes.{field} is required")
    elif kind != "repository":
        errors.append(f"{path}.kind is invalid")
    return errors


def _cycle_errors(
    relationships: Sequence[Mapping[str, Any]], relation_type: str
) -> list[str]:
    graph: dict[str, set[str]] = {}
    for relationship in relationships:
        if relationship.get("type") == relation_type:
            graph.setdefault(str(relationship.get("source")), set()).add(
                str(relationship.get("target"))
            )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(target) for target in sorted(graph.get(node, set()))):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    if any(visit(node) for node in sorted(graph)):
        return [f"relationships contain a {relation_type} cycle"]
    return []


def validate_snapshot(
    snapshot: Mapping[str, Any], vocabulary: Mapping[str, Any]
) -> list[str]:
    """Validate a Repository Intelligence snapshot and return diagnostics."""

    errors = validate_vocabulary(vocabulary)
    errors.extend(
        _required(
            snapshot,
            [
                "schema",
                "contract_version",
                "projection_id",
                "repository",
                "visibility",
                "represented_commit",
                "observed_at",
                "generator",
                "sources",
                "entities",
                "relationships",
                "events",
                "redactions",
                "extensions",
            ],
            "snapshot",
        )
    )
    if snapshot.get("schema") != SCHEMA:
        errors.append(f"snapshot.schema must be {SCHEMA}")
    if snapshot.get("contract_version") != CONTRACT_VERSION:
        errors.append(f"snapshot.contract_version must be {CONTRACT_VERSION}")

    repository = snapshot.get("repository")
    if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
        errors.append("snapshot.repository is invalid")
        repository = ""
    snapshot_visibility = snapshot.get("visibility")
    if snapshot_visibility not in VISIBILITY_RANK:
        errors.append("snapshot.visibility must be public, internal, or private")
        snapshot_visibility = "public"
    represented_commit = snapshot.get("represented_commit")
    if not isinstance(represented_commit, str) or not COMMIT_RE.fullmatch(represented_commit):
        errors.append("snapshot.represented_commit must be a full lowercase commit SHA")
    expected_projection = f"{repository}@{represented_commit}"
    if snapshot.get("projection_id") != expected_projection:
        errors.append("snapshot.projection_id must combine repository and represented_commit")
    observed_at, timestamp_errors = _timestamp(snapshot.get("observed_at"), "snapshot.observed_at")
    errors.extend(timestamp_errors)

    generator = snapshot.get("generator")
    if not isinstance(generator, dict):
        errors.append("snapshot.generator must be an object")
    elif generator.get("contract") != SCHEMA:
        errors.append(f"snapshot.generator.contract must be {SCHEMA}")

    collections: dict[str, list[Any]] = {}
    for name in ("sources", "entities", "relationships", "events", "redactions"):
        value = snapshot.get(name)
        if not isinstance(value, list):
            errors.append(f"snapshot.{name} must be an array")
            collections[name] = []
        else:
            collections[name] = value

    sources_by_id, id_errors = _unique_ids(collections["sources"], "snapshot.sources")
    errors.extend(id_errors)
    errors.extend(
        _validate_stable_order(
            collections["sources"], lambda item: item["id"], "snapshot.sources"
        )
    )
    for position, source in enumerate(collections["sources"]):
        if isinstance(source, dict):
            errors.extend(
                _validate_source(
                    source,
                    snapshot_visibility,
                    f"snapshot.sources[{position}]",
                )
            )

    entities_by_id, id_errors = _unique_ids(collections["entities"], "snapshot.entities")
    errors.extend(id_errors)
    errors.extend(
        _validate_stable_order(
            collections["entities"], lambda item: item["id"], "snapshot.entities"
        )
    )
    for position, entity in enumerate(collections["entities"]):
        if isinstance(entity, dict):
            errors.extend(
                _validate_entity(
                    entity,
                    snapshot_visibility,
                    set(sources_by_id),
                    f"snapshot.entities[{position}]",
                )
            )

    relationship_definitions = {
        item["type"]: item
        for item in vocabulary.get("relationship_types", [])
        if isinstance(item, dict) and isinstance(item.get("type"), str)
    }
    _, id_errors = _unique_ids(
        collections["relationships"], "snapshot.relationships"
    )
    errors.extend(id_errors)
    errors.extend(
        _validate_stable_order(
            collections["relationships"], lambda item: item["id"], "snapshot.relationships"
        )
    )
    valid_relationships: list[Mapping[str, Any]] = []
    for position, relationship in enumerate(collections["relationships"]):
        if not isinstance(relationship, dict):
            continue
        valid_relationships.append(relationship)
        path = f"snapshot.relationships[{position}]"
        errors.extend(_validate_common_claim(relationship, path))
        errors.extend(
            _validate_provenance(
                relationship.get("provenance"), set(sources_by_id), f"{path}.provenance"
            )
        )
        source_id = relationship.get("source")
        target_id = relationship.get("target")
        if source_id not in entities_by_id:
            errors.append(f"{path}.source references unknown entity {source_id}")
        if target_id not in entities_by_id:
            errors.append(f"{path}.target references unknown entity {target_id}")
        if source_id == target_id:
            errors.append(f"{path} must not be a self-link")
        definition = relationship_definitions.get(relationship.get("type"))
        if definition is None:
            errors.append(f"{path}.type is not in the pinned vocabulary")
            continue
        if source_id in entities_by_id:
            source_kind = entities_by_id[source_id].get("kind")
            if source_kind not in definition.get("source_kinds", []):
                errors.append(
                    f"{path}.source kind {source_kind} is invalid for "
                    f"{relationship.get('type')}"
                )
        if target_id in entities_by_id:
            target_kind = entities_by_id[target_id].get("kind")
            if target_kind not in definition.get("target_kinds", []):
                errors.append(
                    f"{path}.target kind {target_kind} is invalid for "
                    f"{relationship.get('type')}"
                )
    errors.extend(_cycle_errors(valid_relationships, "depends-on"))
    errors.extend(_cycle_errors(valid_relationships, "supersedes"))

    _, id_errors = _unique_ids(collections["events"], "snapshot.events")
    errors.extend(id_errors)
    errors.extend(
        _validate_stable_order(
            collections["events"],
            lambda item: (item["occurred_at"], item["id"]),
            "snapshot.events",
        )
    )
    for position, event in enumerate(collections["events"]):
        if not isinstance(event, dict):
            continue
        path = f"snapshot.events[{position}]"
        subject = event.get("subject")
        if subject not in entities_by_id:
            errors.append(f"{path}.subject references unknown entity {subject}")
        event_type = event.get("type")
        if event_type not in EVENT_TYPES:
            errors.append(f"{path}.type is invalid")
        elif subject in entities_by_id:
            prefix = event_type.split(".", 1)[0]
            expected_kind = EVENT_SUBJECT_KINDS.get(prefix)
            if entities_by_id[subject].get("kind") != expected_kind:
                errors.append(f"{path}.type does not match subject kind")
        occurred_at, occurred_errors = _timestamp(event.get("occurred_at"), f"{path}.occurred_at")
        recorded_at, recorded_errors = _timestamp(event.get("recorded_at"), f"{path}.recorded_at")
        errors.extend(occurred_errors)
        errors.extend(recorded_errors)
        if occurred_at is not None and recorded_at is not None and occurred_at > recorded_at:
            errors.append(f"{path}.occurred_at must not be after recorded_at")
        if recorded_at is not None and observed_at is not None and recorded_at > observed_at:
            errors.append(f"{path}.recorded_at must not be after snapshot.observed_at")
        errors.extend(
            _validate_visibility(
                event.get("visibility"), snapshot_visibility, f"{path}.visibility"
            )
        )
        errors.extend(_validate_common_claim(event, path))
        errors.extend(
            _validate_provenance(event.get("provenance"), set(sources_by_id), f"{path}.provenance")
        )

    errors.extend(
        _validate_stable_order(
            collections["redactions"],
            lambda item: (item["field"], item["reason"]),
            "snapshot.redactions",
        )
    )
    root_entity_id = f"ri:{repository}:repository:{repository}"
    if root_entity_id not in entities_by_id:
        errors.append(f"snapshot.entities must contain root repository entity {root_entity_id}")

    actor_redaction = next(
        (
            item
            for item in collections["redactions"]
            if isinstance(item, dict) and item.get("field") == "events.actor"
        ),
        None,
    )
    redacted_actor_count = sum(
        1
        for item in collections["events"]
        if isinstance(item, dict) and item.get("actor") is None
    )
    if (
        actor_redaction is not None
        and actor_redaction.get("count") != redacted_actor_count
    ):
        errors.append("events.actor redaction count must match null actors")
    return sorted(set(errors))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the proposed Repository Intelligence contract."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="Validate one snapshot.")
    validate_parser.add_argument(
        "--snapshot", required=True, type=Path, help="Repository Intelligence JSON file."
    )
    validate_parser.add_argument(
        "--vocabulary", required=True, type=Path, help="Relationship vocabulary JSON file."
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line validator."""

    arguments = _build_parser().parse_args(argv)
    try:
        snapshot = load_json(arguments.snapshot)
        vocabulary = load_json(arguments.vocabulary)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    errors = validate_snapshot(snapshot, vocabulary)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"valid: {arguments.snapshot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
