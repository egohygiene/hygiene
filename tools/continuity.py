#!/usr/bin/env python3
"""Validate Hygiene's repository-continuity policy and local composition.

This checker owns organization applicability, migration, rollout, and required
file composition only. It deliberately does not copy or reimplement Aether's
repository-continuity schema, semantic authoring checks, skill, or provider
projection generator.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
import tomllib
from typing import Any


POLICY_SCHEMA = "egohygiene.repository-continuity-policy/v1"
POLICY_VERSION = "1.0.0-alpha.1"
OWNER = "egohygiene/hygiene"
AETHER_CONTRACT = "aether.repository-continuity/v1"
AETHER_REVISION = "b7597301c4d22a9bcd580967b5753138bb368111"
CONTEXT_CONTRACT_ID = "hygiene-repository-context"
CONTEXT_CONTRACT_VERSION = "2.0.0"
CONTEXT_PROFILE = "hygiene/repository-context"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_PATH_RE = re.compile(r"^[A-Za-z0-9.][A-Za-z0-9._/-]*$")
REPOSITORY_RE = re.compile(r"^egohygiene/(?:\.github|[A-Za-z0-9._-]+)$")
ANGLE_PLACEHOLDER_RE = re.compile(r"<(?!\!--)[^>\n]{1,120}>")

POLICY_FIELDS = {
    "schema",
    "version",
    "status",
    "owner",
    "updated",
    "purpose",
    "upstream",
    "required_files",
    "source_precedence",
    "conflict_policy",
    "applicability",
    "rollout",
    "exceptions",
    "information_safety",
    "compatibility",
    "downstream",
    "ownership",
}
UPSTREAM_FIELDS = {
    "contract_id",
    "contract_version",
    "repository",
    "revision",
    "revision_kind",
    "lifecycle",
    "release_included",
    "evidence",
    "artifacts",
    "activation_gate",
}
EXPECTED_UPSTREAM_ARTIFACTS = {
    "repository-continuity-specification": {
        "kind": "specification",
        "version": "1.0.0",
        "path": "library/organization/specs/methodology/repository-continuity.spec.md",
        "sha256_utf8_lf": "362b7040a0c3dba3477d37edd641d3bf8fab9a447808d262c9576346eae93dae",
    },
    "repository-continuity-schema": {
        "kind": "schema",
        "version": "1.0.0",
        "path": "catalog/schemas/aether.repository-continuity.v1.schema.json",
        "sha256_utf8_lf": "a725e004fe0db2bf96a968c6e3f300d37ecf8b00b9a0923be5c5f4c529655916",
    },
    "maintain-repository-continuity": {
        "kind": "skill",
        "version": "1.1.0",
        "path": "library/organization/skills/methodology/maintain-repository-continuity/SKILL.md",
        "sha256_utf8_lf": "1746b29afa62d7a523d87675430730553079e82cf42e46a6ebe7cf8c82d29e8b",
    },
    "continuity-template": {
        "kind": "template",
        "version": "1.0.0",
        "path": (
            "library/organization/skills/methodology/maintain-repository-continuity/"
            "templates/CONTINUITY.template.md"
        ),
        "sha256_utf8_lf": "494de90d0c344db9ff41b78998445b9e9c02f23a69c25d48442d2af1de1343f2",
    },
    "repository-continuity-instruction": {
        "kind": "instruction",
        "version": "1.0.0",
        "path": "library/organization/instructions/repository-continuity/INSTRUCTION.md",
        "sha256_utf8_lf": "dc2fb66bd5268af2416389fef469d2a13c91d1a6f179e6fc10a21d4f890876a8",
    },
}
EXPECTED_FILES = {
    "agent-instructions": {
        "path": "AGENTS.md",
        "ownership": "repository-owned",
        "required_markers": {
            "<!-- BEGIN AETHER REPOSITORY-CONTINUITY -->",
            "<!-- END AETHER REPOSITORY-CONTINUITY -->",
        },
    },
    "continuity-checkpoint": {
        "path": "CONTINUITY.md",
        "ownership": "repository-owned",
        "required_markers": {
            "schema_version: aether.repository-continuity/v1",
            "continuity_path: CONTINUITY.md",
            "## Current objective and success conditions",
            "## Next dependency-ready work",
        },
    },
    "ecosystem-context": {
        "path": "docs/ecosystem/CONTEXT.md",
        "ownership": "generated",
        "required_markers": {
            "<!-- egohygiene-context: repository-context/v2 -->",
            'generated-by: "egohygiene/hygiene:repository-context@2.0.0"',
            'continuity-policy: "egohygiene.repository-continuity-policy/v1@1.0.0-alpha.1"',
        },
    },
}
SOURCE_PRECEDENCE = [
    "user-instruction-and-applicable-authorization",
    "scoped-repository-instructions",
    "live-repository-git-and-work-tracker-evidence",
    "accepted-decisions-contracts-architecture-and-roadmap",
    "continuity-checkpoint",
    "generated-projections-and-conversational-recollection",
]
INITIAL_REPOSITORIES = {
    "egohygiene/.github",
    "egohygiene/aether",
    "egohygiene/akashic",
    "egohygiene/aniflow",
    "egohygiene/antidote",
    "egohygiene/athena",
    "egohygiene/beacon",
    "egohygiene/civics",
    "egohygiene/egohygiene",
    "egohygiene/egohygiene.io",
    "egohygiene/egolint",
    "egohygiene/empathy",
    "egohygiene/filament",
    "egohygiene/flow",
    "egohygiene/holon",
    "egohygiene/hygiene",
    "egohygiene/identity",
    "egohygiene/mantle",
    "egohygiene/mindcap",
    "egohygiene/mindgarden",
    "egohygiene/observatory",
    "egohygiene/optiflow",
    "egohygiene/pace",
    "egohygiene/realm",
    "egohygiene/reflector",
    "egohygiene/relay",
    "egohygiene/renderflow",
    "egohygiene/sanctuary",
    "egohygiene/store",
}
LIFECYCLES = {
    "active": "required",
    "dormant": "advisory",
    "archived": "not-applicable",
}
REPOSITORY_KINDS = {
    "standard": "required",
    "mirror": "not-applicable",
    "generated-only": "advisory",
    "template": "required",
}
VISIBILITIES = {
    "public": "no-override",
    "private": "no-override",
    "internal": "no-override",
}
STAGES = {
    "observe": (1, "visible-non-blocking"),
    "ratchet": (2, "block-new-regressions"),
    "enforce": (3, "block-nonconformance"),
}
EXCEPTION_FIELDS = [
    "repository",
    "owner",
    "reason",
    "approval",
    "expires_on",
    "review_trigger",
    "validation_state",
    "exit_criteria",
]
EXCEPTION_STATES = ["proposed", "approved", "expired", "revoked"]
DOWNSTREAM_ISSUES = {
    "egohygiene/egolint": "https://github.com/egohygiene/egolint/issues/55",
    "egohygiene/holon": "https://github.com/egohygiene/holon/issues/42",
    "egohygiene/relay": "https://github.com/egohygiene/relay/issues/60",
    "egohygiene/observatory": "https://github.com/egohygiene/observatory/issues/18",
    "egohygiene/pace": "https://github.com/egohygiene/pace/issues/26",
}
OWNERS = {
    "aether",
    "hygiene",
    "egolint",
    "holon",
    "relay",
    "observatory",
    "pace",
    "repository",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load one UTF-8 JSON object."""

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _non_empty_text(value: Any, path: str) -> list[str]:
    return [] if isinstance(value, str) and value.strip() else [f"{path} must be non-empty text"]


def _unique_strings(value: Any, path: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        return [f"{path} must be a {'non-empty ' if not allow_empty else ''}array"]
    errors: list[str] = []
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"{path} must not contain duplicates")
    return errors


def _safe_path(value: Any) -> bool:
    return (
        isinstance(value, str)
        and SAFE_PATH_RE.fullmatch(value) is not None
        and not value.startswith("/")
        and ".." not in Path(value).parts
    )


def _parse_date(value: Any, path: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{path} must be an ISO date")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{path} must be an ISO date")
        return None


def validate_profile(profile: dict[str, Any]) -> list[str]:
    """Return stable diagnostics for the v1 organization policy profile."""

    errors: list[str] = []
    if set(profile) != POLICY_FIELDS:
        errors.append("profile fields must exactly match the v1 policy contract")
    if profile.get("schema") != POLICY_SCHEMA:
        errors.append(f"profile.schema must be {POLICY_SCHEMA}")
    if profile.get("version") != POLICY_VERSION:
        errors.append(f"profile.version must be {POLICY_VERSION}")
    if profile.get("status") not in {"proposed", "active", "deprecated", "superseded"}:
        errors.append("profile.status is invalid")
    if profile.get("owner") != OWNER:
        errors.append(f"profile.owner must be {OWNER}")
    updated = _parse_date(profile.get("updated"), "profile.updated", errors)
    errors.extend(_non_empty_text(profile.get("purpose"), "profile.purpose"))

    upstream = profile.get("upstream")
    if not isinstance(upstream, dict) or set(upstream) != UPSTREAM_FIELDS:
        errors.append("profile.upstream fields must exactly match the v1 policy contract")
        upstream = {}
    if upstream.get("contract_id") != AETHER_CONTRACT:
        errors.append(f"profile.upstream.contract_id must be {AETHER_CONTRACT}")
    if upstream.get("contract_version") != "1.0.0":
        errors.append("profile.upstream.contract_version must be 1.0.0")
    if upstream.get("repository") != "egohygiene/aether":
        errors.append("profile.upstream.repository must be egohygiene/aether")
    if upstream.get("revision") != AETHER_REVISION:
        errors.append("profile.upstream.revision must pin the Aether #80 merge commit")
    if upstream.get("revision_kind") != "git-commit":
        errors.append("profile.upstream.revision_kind must be git-commit")
    if upstream.get("lifecycle") != "draft" or upstream.get("release_included") is not False:
        errors.append("profile.upstream must report Aether's merged draft as unreleased")
    errors.extend(_unique_strings(upstream.get("evidence"), "profile.upstream.evidence"))
    evidence = upstream.get("evidence")
    if isinstance(evidence, list) and set(evidence) != {
        "https://github.com/egohygiene/aether/pull/81",
        "https://github.com/egohygiene/aether/pull/82",
    }:
        errors.append("profile.upstream.evidence must name Aether PRs #81 and #82")
    errors.extend(
        _non_empty_text(
            upstream.get("activation_gate"), "profile.upstream.activation_gate"
        )
    )

    artifacts = upstream.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("profile.upstream.artifacts must be an array")
        artifacts = []
    artifact_index: dict[str, dict[str, Any]] = {}
    for index, artifact in enumerate(artifacts):
        path = f"profile.upstream.artifacts[{index}]"
        if not isinstance(artifact, dict) or set(artifact) != {
            "id",
            "kind",
            "version",
            "path",
            "sha256_utf8_lf",
        }:
            errors.append(f"{path} fields are invalid")
            continue
        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, str) or artifact_id in artifact_index:
            errors.append(f"{path}.id must be unique")
            continue
        artifact_index[artifact_id] = artifact
        if not _safe_path(artifact.get("path")):
            errors.append(f"{path}.path must be a safe repository-relative path")
        if not isinstance(artifact.get("sha256_utf8_lf"), str) or not DIGEST_RE.fullmatch(
            artifact["sha256_utf8_lf"]
        ):
            errors.append(f"{path}.sha256_utf8_lf must be a SHA-256 digest")
    if set(artifact_index) != set(EXPECTED_UPSTREAM_ARTIFACTS):
        errors.append("profile.upstream.artifacts must cover every pinned Aether artifact")
    for artifact_id, expected in EXPECTED_UPSTREAM_ARTIFACTS.items():
        artifact = artifact_index.get(artifact_id)
        if artifact is not None and any(
            artifact.get(key) != value for key, value in expected.items()
        ):
            errors.append(
                f"profile.upstream.artifacts.{artifact_id} must match the pinned digest record"
            )

    required_files = profile.get("required_files")
    if not isinstance(required_files, list):
        errors.append("profile.required_files must be an array")
        required_files = []
    file_index: dict[str, dict[str, Any]] = {}
    for index, requirement in enumerate(required_files):
        path = f"profile.required_files[{index}]"
        if not isinstance(requirement, dict) or set(requirement) != {
            "id",
            "path",
            "kind",
            "ownership",
            "requirement",
            "markers",
            "content_rule",
        }:
            errors.append(f"{path} fields are invalid")
            continue
        requirement_id = requirement.get("id")
        if not isinstance(requirement_id, str) or requirement_id in file_index:
            errors.append(f"{path}.id must be unique")
            continue
        file_index[requirement_id] = requirement
        if requirement.get("kind") != "file" or requirement.get("requirement") != "required":
            errors.append(f"{path} must describe a required regular file")
        errors.extend(_unique_strings(requirement.get("markers"), f"{path}.markers"))
        errors.extend(_non_empty_text(requirement.get("content_rule"), f"{path}.content_rule"))
    if set(file_index) != set(EXPECTED_FILES):
        errors.append(
            "profile.required_files must declare AGENTS.md, CONTINUITY.md, and ecosystem context"
        )
    for requirement_id, expected in EXPECTED_FILES.items():
        requirement = file_index.get(requirement_id)
        if requirement is None:
            continue
        if requirement.get("path") != expected["path"]:
            errors.append(f"profile.required_files.{requirement_id}.path is invalid")
        if requirement.get("ownership") != expected["ownership"]:
            errors.append(f"profile.required_files.{requirement_id}.ownership is invalid")
        markers = requirement.get("markers")
        if isinstance(markers, list) and not expected["required_markers"].issubset(set(markers)):
            errors.append(f"profile.required_files.{requirement_id}.markers are incomplete")

    if profile.get("source_precedence") != SOURCE_PRECEDENCE:
        errors.append("profile.source_precedence must preserve the normative six-layer order")
    if profile.get("conflict_policy") != {
        "live_verification_required": True,
        "stale_checkpoint_action": "repair-or-mark-stale",
        "silent_override_forbidden": True,
        "unavailable_evidence_action": "report-limitation-and-do-not-infer",
    }:
        errors.append("profile.conflict_policy must fail visibly on stale or unavailable evidence")

    applicability = profile.get("applicability")
    expected_applicability_fields = {
        "resolution_order",
        "lifecycles",
        "repository_kinds",
        "visibilities",
        "initial_scope",
    }
    if not isinstance(applicability, dict) or set(applicability) != expected_applicability_fields:
        errors.append("profile.applicability fields are invalid")
        applicability = {}
    if applicability.get("resolution_order") != [
        "approved-unexpired-exception",
        "repository-kind",
        "lifecycle",
        "visibility",
    ]:
        errors.append("profile.applicability.resolution_order is invalid")
    if applicability.get("lifecycles") != LIFECYCLES:
        errors.append("profile.applicability.lifecycles must cover active, dormant, and archived")
    if applicability.get("repository_kinds") != REPOSITORY_KINDS:
        errors.append(
            "profile.applicability.repository_kinds must cover standard, mirror, "
            "generated-only, and template"
        )
    if applicability.get("visibilities") != VISIBILITIES:
        errors.append(
            "profile.applicability.visibilities must cover public, private, and "
            "internal without weakening safety"
        )
    initial = applicability.get("initial_scope")
    if not isinstance(initial, dict) or set(initial) != {
        "observed_at",
        "source",
        "active_repository_count",
        "default_requirement",
        "repositories",
        "catalog_reconciliation",
    }:
        errors.append("profile.applicability.initial_scope fields are invalid")
        initial = {}
    repositories = initial.get("repositories")
    errors.extend(_unique_strings(repositories, "profile.applicability.initial_scope.repositories"))
    if not isinstance(repositories, list) or set(repositories) != INITIAL_REPOSITORIES:
        errors.append(
            "profile.applicability.initial_scope must name the 29 repositories "
            "observed by issue #45"
        )
    if initial.get("active_repository_count") != len(INITIAL_REPOSITORIES):
        errors.append("profile.applicability.initial_scope.active_repository_count must be 29")
    if initial.get("default_requirement") != "required":
        errors.append("profile.applicability.initial_scope.default_requirement must be required")
    if initial.get("source") != "https://github.com/egohygiene/hygiene/issues/45":
        errors.append("profile.applicability.initial_scope.source must be Hygiene issue #45")
    _parse_date(
        initial.get("observed_at"),
        "profile.applicability.initial_scope.observed_at",
        errors,
    )
    errors.extend(
        _non_empty_text(
            initial.get("catalog_reconciliation"),
            "profile.applicability.initial_scope.catalog_reconciliation",
        )
    )

    rollout = profile.get("rollout")
    if not isinstance(rollout, dict) or set(rollout) != {"current_stage", "stages"}:
        errors.append("profile.rollout fields are invalid")
        rollout = {}
    if rollout.get("current_stage") != "observe":
        errors.append("profile.rollout.current_stage must remain observe while upstream is draft")
    stages = rollout.get("stages")
    if not isinstance(stages, list):
        errors.append("profile.rollout.stages must be an array")
        stages = []
    stage_ids: list[str] = []
    for index, stage in enumerate(stages):
        path = f"profile.rollout.stages[{index}]"
        if not isinstance(stage, dict) or set(stage) != {
            "id",
            "order",
            "finding_behavior",
            "entry_gate",
            "exit_gate",
            "rollback",
        }:
            errors.append(f"{path} fields are invalid")
            continue
        stage_id = stage.get("id")
        if isinstance(stage_id, str):
            stage_ids.append(stage_id)
        expected = STAGES.get(stage_id)
        if expected is None or (stage.get("order"), stage.get("finding_behavior")) != expected:
            errors.append(f"{path} order or finding behavior is invalid")
        for field in ("entry_gate", "exit_gate", "rollback"):
            errors.extend(_non_empty_text(stage.get(field), f"{path}.{field}"))
    if stage_ids != list(STAGES):
        errors.append("profile.rollout.stages must order observe, ratchet, then enforce")

    exception_policy = profile.get("exceptions")
    if not isinstance(exception_policy, dict) or set(exception_policy) != {
        "required_fields",
        "allowed_states",
        "approval_required",
        "expiry_required",
        "visible_in_validation",
        "records",
    }:
        errors.append("profile.exceptions fields are invalid")
        exception_policy = {}
    if exception_policy.get("required_fields") != EXCEPTION_FIELDS:
        errors.append("profile.exceptions.required_fields is invalid")
    if exception_policy.get("allowed_states") != EXCEPTION_STATES:
        errors.append("profile.exceptions.allowed_states is invalid")
    if any(
        exception_policy.get(field) is not True
        for field in ("approval_required", "expiry_required", "visible_in_validation")
    ):
        errors.append("profile.exceptions must require approval, expiry, and visible validation")
    records = exception_policy.get("records")
    if not isinstance(records, list):
        errors.append("profile.exceptions.records must be an array")
        records = []
    exception_repositories: list[str] = []
    for index, record in enumerate(records):
        path = f"profile.exceptions.records[{index}]"
        if not isinstance(record, dict) or list(record) != EXCEPTION_FIELDS:
            errors.append(f"{path} fields must exactly match required_fields in order")
            continue
        repository = record.get("repository")
        if not isinstance(repository, str) or repository not in INITIAL_REPOSITORIES:
            errors.append(f"{path}.repository must be in the initial active scope")
        else:
            exception_repositories.append(repository)
        for field in ("owner", "reason", "review_trigger", "exit_criteria"):
            errors.extend(_non_empty_text(record.get(field), f"{path}.{field}"))
        state = record.get("validation_state")
        if state not in EXCEPTION_STATES:
            errors.append(f"{path}.validation_state is invalid")
        approval = record.get("approval")
        if state == "approved" and (
            not isinstance(approval, str) or not approval.startswith("https://")
        ):
            errors.append(f"{path}.approval must be durable HTTPS evidence when approved")
        expires = _parse_date(record.get("expires_on"), f"{path}.expires_on", errors)
        if (
            state == "approved"
            and updated is not None
            and expires is not None
            and expires <= updated
        ):
            errors.append(f"{path} approved exception is already expired")
    if len(exception_repositories) != len(set(exception_repositories)):
        errors.append("profile.exceptions.records must not duplicate repositories")

    safety = profile.get("information_safety")
    if not isinstance(safety, dict) or set(safety) != {
        "minimum_necessary",
        "git_history_owns_chronology",
        "replaceable_current_snapshot",
        "public_excluded",
        "private_rules",
        "untrusted_content",
    }:
        errors.append("profile.information_safety fields are invalid")
        safety = {}
    if any(
        safety.get(field) is not True
        for field in (
            "minimum_necessary",
            "git_history_owns_chronology",
            "replaceable_current_snapshot",
        )
    ):
        errors.append(
            "profile.information_safety must enforce minimum replaceable state "
            "with Git chronology"
        )
    expected_public = {
        "credentials-and-secrets",
        "private-conversation-text",
        "health-and-sensitive-personal-data",
        "private-local-paths",
        "unpublished-private-business-data",
        "unrelated-private-context",
    }
    if set(safety.get("public_excluded", [])) != expected_public:
        errors.append("profile.information_safety.public_excluded is incomplete")
    if set(safety.get("private_rules", [])) != {
        "exclude-credentials-and-secrets",
        "retain-only-minimum-durable-repository-state",
        "apply-repository-access-controls",
    }:
        errors.append("profile.information_safety.private_rules is incomplete")
    if safety.get("untrusted_content") != "context-only-no-authority":
        errors.append("profile.information_safety.untrusted_content is invalid")

    compatibility = profile.get("compatibility")
    if not isinstance(compatibility, dict) or set(compatibility) != {
        "previous_contract",
        "successor_contract",
        "impact",
        "reason",
        "migration",
        "deprecation",
        "rollback",
    }:
        errors.append("profile.compatibility fields are invalid")
        compatibility = {}
    if compatibility.get("previous_contract") != {
        "id": "egohygiene.repository-context/v1",
        "version": "1.0.0",
        "artifact": "contracts/repository-context.v1.toml",
        "status": "deprecated",
    }:
        errors.append("profile.compatibility.previous_contract must retain deprecated v1")
    if compatibility.get("successor_contract") != {
        "id": "egohygiene.repository-context/v2",
        "version": "2.0.0",
        "artifact": "contracts/repository-context.toml",
        "status": "proposed",
    }:
        errors.append("profile.compatibility.successor_contract must introduce proposed v2")
    if compatibility.get("impact") != "breaking":
        errors.append("profile.compatibility.impact must be breaking")
    for field in ("reason", "migration", "deprecation", "rollback"):
        errors.extend(_non_empty_text(compatibility.get(field), f"profile.compatibility.{field}"))

    downstream = profile.get("downstream")
    if not isinstance(downstream, list):
        errors.append("profile.downstream must be an array")
        downstream = []
    downstream_index: dict[str, dict[str, Any]] = {}
    for index, consumer in enumerate(downstream):
        path = f"profile.downstream[{index}]"
        if not isinstance(consumer, dict) or set(consumer) != {
            "repository",
            "issue",
            "responsibility",
        }:
            errors.append(f"{path} fields are invalid")
            continue
        repository = consumer.get("repository")
        if not isinstance(repository, str) or repository in downstream_index:
            errors.append(f"{path}.repository must be unique")
            continue
        downstream_index[repository] = consumer
        errors.extend(_non_empty_text(consumer.get("responsibility"), f"{path}.responsibility"))
    if set(downstream_index) != set(DOWNSTREAM_ISSUES):
        errors.append("profile.downstream must cover Egolint, Holon, Relay, Observatory, and Pace")
    for repository, issue in DOWNSTREAM_ISSUES.items():
        if repository in downstream_index and downstream_index[repository].get("issue") != issue:
            errors.append(f"profile.downstream.{repository}.issue is invalid")

    ownership = profile.get("ownership")
    if not isinstance(ownership, dict) or set(ownership) != OWNERS:
        errors.append("profile.ownership must declare every bounded owner")
    elif any(not isinstance(value, str) or not value.strip() for value in ownership.values()):
        errors.append("profile.ownership values must be non-empty text")
    return sorted(set(errors))


def _approved_exception(
    profile: dict[str, Any], repository: str, as_of: date
) -> dict[str, Any] | None:
    for record in profile["exceptions"]["records"]:
        if (
            record["repository"] == repository
            and record["validation_state"] == "approved"
            and date.fromisoformat(record["expires_on"]) > as_of
        ):
            return record
    return None


def resolve_applicability(
    profile: dict[str, Any],
    repository: str,
    lifecycle: str,
    repository_kind: str,
    visibility: str,
    *,
    as_of: date | None = None,
) -> dict[str, Any]:
    """Resolve applicability with exceptions, kind, lifecycle, then visibility."""

    errors = validate_profile(profile)
    if errors:
        raise ValueError("cannot resolve an invalid continuity policy")
    if REPOSITORY_RE.fullmatch(repository) is None:
        raise ValueError(f"invalid repository: {repository}")
    if lifecycle not in LIFECYCLES:
        raise ValueError(f"unknown lifecycle: {lifecycle}")
    if repository_kind not in REPOSITORY_KINDS:
        raise ValueError(f"unknown repository kind: {repository_kind}")
    if visibility not in VISIBILITIES:
        raise ValueError(f"unknown visibility: {visibility}")
    observed_on = as_of or date.fromisoformat(profile["updated"])
    exception = _approved_exception(profile, repository, observed_on)
    if exception is not None:
        return {
            "repository": repository,
            "requirement": "exempt",
            "reason": "approved-unexpired-exception",
            "exception": exception,
            "stage": profile["rollout"]["current_stage"],
        }
    kind_requirement = profile["applicability"]["repository_kinds"][repository_kind]
    lifecycle_requirement = profile["applicability"]["lifecycles"][lifecycle]
    rank = {"required": 0, "advisory": 1, "not-applicable": 2}
    requirement = max((kind_requirement, lifecycle_requirement), key=rank.__getitem__)
    return {
        "repository": repository,
        "requirement": requirement,
        "reason": "repository-kind-and-lifecycle",
        "exception": None,
        "stage": profile["rollout"]["current_stage"],
    }


def validate_repository(repository: Path, profile: dict[str, Any]) -> list[str]:
    """Validate Hygiene's local file composition without duplicating Aether semantics."""

    errors = validate_profile(profile)
    if errors:
        return ["invalid continuity policy: " + error for error in errors]
    repository = repository.resolve()
    for requirement in profile["required_files"]:
        relative = requirement["path"]
        candidate = repository / relative
        if not candidate.is_file() or candidate.is_symlink():
            errors.append(f"required regular file is missing or linked: {relative}")
            continue
        text = candidate.read_text(encoding="utf-8")
        for marker in requirement["markers"]:
            if marker not in text:
                errors.append(f"{relative} is missing required marker: {marker}")
        if relative == "AGENTS.md":
            for marker in (
                "<!-- BEGIN AETHER REPOSITORY-CONTINUITY -->",
                "<!-- END AETHER REPOSITORY-CONTINUITY -->",
            ):
                if text.count(marker) != 1:
                    errors.append(f"AGENTS.md must contain exactly one managed marker: {marker}")
        if relative == "CONTINUITY.md":
            if len(text.encode("utf-8")) > 16_384:
                errors.append("CONTINUITY.md exceeds Aether v1's 16384-byte limit")
            if len(text.splitlines()) > 240:
                errors.append("CONTINUITY.md exceeds Aether v1's 240-line limit")
            for placeholder in (
                "This template is intentionally invalid",
                "<owner/repository>",
                "<current objective>",
                "<observable conditions>",
            ):
                if placeholder in text:
                    errors.append(f"CONTINUITY.md contains generic template content: {placeholder}")
            placeholder_match = ANGLE_PLACEHOLDER_RE.search(text)
            if placeholder_match is not None:
                errors.append(
                    "CONTINUITY.md contains an unresolved angle-bracket placeholder: "
                    + placeholder_match.group(0)
                )

    contract_path = repository / "contracts" / "repository-context.toml"
    try:
        contract = tomllib.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        errors.append(f"repository-context v2 contract cannot be loaded: {error}")
        return sorted(set(errors))
    if contract.get("id") != CONTEXT_CONTRACT_ID:
        errors.append(f"repository-context contract id must be {CONTEXT_CONTRACT_ID}")
    if contract.get("version") != CONTEXT_CONTRACT_VERSION:
        errors.append(f"repository-context contract version must be {CONTEXT_CONTRACT_VERSION}")
    if contract.get("profile") != CONTEXT_PROFILE:
        errors.append(f"repository-context contract profile must be {CONTEXT_PROFILE}")
    if contract.get("provisional") is not True:
        errors.append("repository-context v2 must remain provisional during observe")
    source = contract.get("source")
    if not isinstance(source, dict):
        errors.append("repository-context contract source must be an object")
    else:
        if (
            source.get("repository") != OWNER
            or source.get("path") != "catalog/repository-context.json"
        ):
            errors.append("repository-context contract must point to Hygiene's context policy")
        if (
            not isinstance(source.get("revision"), str)
            or COMMIT_RE.fullmatch(source["revision"]) is None
        ):
            errors.append("repository-context contract source revision must be an immutable commit")
        if source.get("decision") != "https://github.com/egohygiene/hygiene/issues/45":
            errors.append("repository-context contract must identify issue #45")
    contract_requirements = contract.get("requirements")
    if not isinstance(contract_requirements, list):
        errors.append("repository-context contract requirements must be an array")
    else:
        actual = {
            item.get("id"): (item.get("path"), item.get("ownership"))
            for item in contract_requirements
            if isinstance(item, dict)
        }
        expected = {
            requirement_id: (spec["path"], spec["ownership"])
            for requirement_id, spec in EXPECTED_FILES.items()
        }
        if actual != expected:
            errors.append("repository-context v2 requirements must match the continuity policy")
    return sorted(set(errors))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("catalog/repository-continuity-policy.json"),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-profile")
    resolve = subparsers.add_parser("resolve")
    resolve.add_argument("--repository", required=True)
    resolve.add_argument("--lifecycle", required=True)
    resolve.add_argument("--repository-kind", required=True)
    resolve.add_argument("--visibility", required=True)
    local = subparsers.add_parser("validate-repository")
    local.add_argument("--repository", type=Path, default=Path("."))
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        profile = load_json(arguments.profile)
        if arguments.command == "validate-profile":
            errors = validate_profile(profile)
        elif arguments.command == "resolve":
            print(
                json.dumps(
                    resolve_applicability(
                        profile,
                        arguments.repository,
                        arguments.lifecycle,
                        arguments.repository_kind,
                        arguments.visibility,
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        else:
            errors = validate_repository(arguments.repository, profile)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"repository continuity policy invalid: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"repository continuity policy invalid: {error}", file=sys.stderr)
        return 1
    print(f"repository continuity policy valid: {arguments.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
