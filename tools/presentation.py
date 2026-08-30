#!/usr/bin/env python3
"""Validate and resolve the repository-presentation reference contracts.

This dependency-free checker proves cross-field policy invariants. Egolint owns
fleet lint semantics; Relay owns reusable CI and evidence transport.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any


PROFILE_SCHEMA = "egohygiene.repository-presentation-profile/v1"
EVIDENCE_SCHEMA = "egohygiene.repository-presentation-evidence/v1"
PROFILE_VERSION = "1.0.0-alpha.1"
OWNER = "egohygiene/hygiene"
REQUIREMENTS = {"required", "recommended", "optional", "not_applicable"}
EVIDENCE_STATES = {
    "unknown",
    "evaluating",
    "advisory",
    "passing",
    "failing",
    "partial",
    "stale",
    "exempt",
    "not_applicable",
    "blocked",
}
EVIDENCE_REQUIRED_STATES = {
    "advisory",
    "passing",
    "failing",
    "partial",
    "stale",
    "exempt",
    "blocked",
}
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)$")
SLOT_RE = re.compile(r"^[a-z][a-z0-9_]*$")
EXPECTED_OVERRIDE_ORDER = [
    "default",
    "repository_type",
    "visibility",
    "lifecycle",
]
EXPECTED_OWNERS = {
    "hygiene",
    "identity",
    "holon",
    "egolint",
    "relay",
    "pace",
    "observatory",
    "repository",
}
EXPECTED_SLOT_IDS = {
    "architecture",
    "canonical_navigation",
    "contributing",
    "development",
    "documentation",
    "evidence_badges",
    "generated_ownership",
    "identity_banner",
    "installation",
    "license",
    "maturity_status",
    "purpose",
    "security",
    "support_boundary",
    "validation",
}
PROFILE_FIELDS = {
    "schema",
    "version",
    "status",
    "owner",
    "updated",
    "purpose",
    "claim_policy",
    "requirements",
    "evidence_states",
    "repository_types",
    "visibilities",
    "lifecycles",
    "slots",
    "type_overrides",
    "visibility_overrides",
    "lifecycle_overrides",
    "composition",
    "ownership",
}
EVIDENCE_FIELDS = {"schema", "profile", "repository", "assessment", "slots", "badge"}
SLOT_EVIDENCE_FIELDS = {"id", "requirement", "state", "evidence", "reason"}
EVIDENCE_RECORD_FIELDS = {"kind", "location", "assertion", "freshness"}
EVIDENCE_KINDS = {
    "approval",
    "documentation",
    "local_file",
    "manifest",
    "release",
    "workflow",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object."""

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _unique_strings(value: Any, path: str) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty array"]
    errors: list[str] = []
    if any(not isinstance(item, str) or not item for item in value):
        errors.append(f"{path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"{path} must not contain duplicates")
    return errors


def validate_profile(profile: Mapping[str, Any]) -> list[str]:
    """Return deterministic semantic errors for the canonical profile."""

    errors: list[str] = []
    if set(profile) != PROFILE_FIELDS:
        errors.append("profile fields must exactly match the v1 contract")
    if profile.get("schema") != PROFILE_SCHEMA:
        errors.append(f"profile.schema must be {PROFILE_SCHEMA}")
    if profile.get("version") != PROFILE_VERSION:
        errors.append(f"profile.version must be {PROFILE_VERSION}")
    if profile.get("status") not in {"proposed", "active", "deprecated", "superseded"}:
        errors.append("profile.status is invalid")
    if profile.get("owner") != OWNER:
        errors.append(f"profile.owner must be {OWNER}")
    if profile.get("requirements") != [
        "required",
        "recommended",
        "optional",
        "not_applicable",
    ]:
        errors.append("profile.requirements must use canonical order")
    if profile.get("evidence_states") != [
        "unknown",
        "evaluating",
        "advisory",
        "passing",
        "failing",
        "partial",
        "stale",
        "exempt",
        "not_applicable",
        "blocked",
    ]:
        errors.append("profile.evidence_states must use canonical order")

    repository_types = profile.get("repository_types")
    visibilities = profile.get("visibilities")
    lifecycles = profile.get("lifecycles")
    errors.extend(_unique_strings(repository_types, "profile.repository_types"))
    errors.extend(_unique_strings(visibilities, "profile.visibilities"))
    errors.extend(_unique_strings(lifecycles, "profile.lifecycles"))
    if isinstance(repository_types, list) and repository_types != sorted(repository_types):
        errors.append("profile.repository_types must use stable order")
    if visibilities != ["public", "internal", "private"]:
        errors.append("profile.visibilities must use canonical order")
    if lifecycles != ["active", "incubating", "archived"]:
        errors.append("profile.lifecycles must use canonical order")

    slots = profile.get("slots")
    if not isinstance(slots, list) or not slots:
        errors.append("profile.slots must be a non-empty array")
        slots = []
    slot_ids: list[str] = []
    for index, slot in enumerate(slots):
        path = f"profile.slots[{index}]"
        if not isinstance(slot, dict):
            errors.append(f"{path} must be an object")
            continue
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or SLOT_RE.fullmatch(slot_id) is None:
            errors.append(f"{path}.id is invalid")
        else:
            slot_ids.append(slot_id)
        if slot.get("default_requirement") not in REQUIREMENTS:
            errors.append(f"{path}.default_requirement is invalid")
        if not isinstance(slot.get("authority"), str) or not slot["authority"]:
            errors.append(f"{path}.authority must be a non-empty string")
        for field in ("title", "description"):
            if not isinstance(slot.get(field), str) or not slot[field]:
                errors.append(f"{path}.{field} must be a non-empty string")
        errors.extend(_unique_strings(slot.get("checks"), f"{path}.checks"))
    if len(slot_ids) != len(set(slot_ids)):
        errors.append("profile.slots must use unique ids")
    if set(slot_ids) != EXPECTED_SLOT_IDS:
        errors.append("profile.slots must declare every canonical presentation slot")

    dimensions = (
        ("type_overrides", repository_types),
        ("visibility_overrides", visibilities),
        ("lifecycle_overrides", lifecycles),
    )
    for field, declared_values in dimensions:
        overrides = profile.get(field)
        if not isinstance(overrides, dict):
            errors.append(f"profile.{field} must be an object")
            continue
        expected = set(declared_values) if isinstance(declared_values, list) else set()
        if set(overrides) != expected:
            errors.append(f"profile.{field} keys must match their declared dimension")
        for variant, values in overrides.items():
            path = f"profile.{field}.{variant}"
            if not isinstance(values, dict):
                errors.append(f"{path} must be an object")
                continue
            for slot_id, requirement in values.items():
                if slot_id not in slot_ids:
                    errors.append(f"{path} references unknown slot {slot_id}")
                if requirement not in REQUIREMENTS:
                    errors.append(f"{path}.{slot_id} has invalid requirement")

    composition = profile.get("composition")
    if not isinstance(composition, dict):
        errors.append("profile.composition must be an object")
    else:
        if composition.get("override_order") != EXPECTED_OVERRIDE_ORDER:
            errors.append("profile.composition.override_order is invalid")
        for field in (
            "generated_regions_only",
            "preserve_repository_authored_prose",
            "full_file_replacement_forbidden",
        ):
            if composition.get(field) is not True:
                errors.append(f"profile.composition.{field} must be true")

    ownership = profile.get("ownership")
    if not isinstance(ownership, dict) or set(ownership) != EXPECTED_OWNERS:
        errors.append("profile.ownership must declare every bounded owner")

    claim_policy = profile.get("claim_policy")
    if not isinstance(claim_policy, dict):
        errors.append("profile.claim_policy must be an object")
    else:
        if set(claim_policy) != {
            "badge_label",
            "state_messages",
            "prohibited_claim_terms",
            "represented_commit_required",
            "evidence_url_required",
            "unknown_fails_closed",
        }:
            errors.append(
                "profile.claim_policy fields must exactly match the v1 contract"
            )
        if claim_policy.get("badge_label") != "Hygienic":
            errors.append("profile.claim_policy.badge_label must be Hygienic")
        state_messages = claim_policy.get("state_messages")
        if not isinstance(state_messages, dict) or set(state_messages) != EVIDENCE_STATES:
            errors.append(
                "profile.claim_policy.state_messages must cover every evidence state"
            )
        elif any(
            not isinstance(message, str) or not message
            for message in state_messages.values()
        ):
            errors.append(
                "profile.claim_policy.state_messages must be non-empty strings"
            )
        for field in (
            "represented_commit_required",
            "evidence_url_required",
            "unknown_fails_closed",
        ):
            if claim_policy.get(field) is not True:
                errors.append(f"profile.claim_policy.{field} must be true")
        terms = claim_policy.get("prohibited_claim_terms")
        errors.extend(_unique_strings(terms, "profile.claim_policy.prohibited_claim_terms"))
        if isinstance(terms, list) and "compliant" not in terms:
            errors.append("profile must prohibit unsupported compliant claims")
        if isinstance(state_messages, dict) and isinstance(terms, list) and any(
            isinstance(message, str)
            and any(
                re.search(rf"\b{re.escape(term)}\b", message, re.IGNORECASE)
                for term in terms
                if isinstance(term, str)
            )
            for message in state_messages.values()
        ):
            errors.append("profile state messages contain a prohibited claim term")
    return sorted(set(errors))


def resolve_requirements(
    profile: Mapping[str, Any],
    repository_type: str,
    visibility: str,
    lifecycle: str,
) -> dict[str, str]:
    """Resolve slot requirements with the profile's fixed precedence."""

    if validate_profile(profile):
        raise ValueError("cannot resolve an invalid presentation profile")
    dimensions = (
        ("type_overrides", repository_type),
        ("visibility_overrides", visibility),
        ("lifecycle_overrides", lifecycle),
    )
    for field, value in dimensions:
        if value not in profile[field]:
            raise ValueError(f"unknown {field.removesuffix('_overrides')}: {value}")
    resolved = {
        slot["id"]: slot["default_requirement"] for slot in profile["slots"]
    }
    for field, value in dimensions:
        resolved.update(profile[field][value])
    return resolved


def derive_state(slots: Sequence[Mapping[str, Any]]) -> str:
    """Derive the honest badge state from resolved slot evidence."""

    required = [slot for slot in slots if slot.get("requirement") == "required"]
    recommended = [
        slot for slot in slots if slot.get("requirement") == "recommended"
    ]
    required_states = {slot.get("state") for slot in required}
    if "failing" in required_states:
        return "failing"
    if "blocked" in required_states:
        return "blocked"
    if "stale" in required_states:
        return "stale"
    if "evaluating" in required_states:
        return "evaluating"
    if required_states & {"unknown", "partial", "advisory", "exempt"}:
        return "partial"
    if any(slot.get("state") not in {"passing", "not_applicable"} for slot in recommended):
        return "advisory"
    return "passing"


def validate_evidence(
    evidence: Mapping[str, Any], profile: Mapping[str, Any]
) -> list[str]:
    """Validate a repository presentation evidence document."""

    errors = validate_profile(profile)
    if errors:
        return [f"profile invalid: {error}" for error in errors]
    if set(evidence) != EVIDENCE_FIELDS:
        errors.append("evidence fields must exactly match the v1 contract")
    if evidence.get("schema") != EVIDENCE_SCHEMA:
        errors.append(f"evidence.schema must be {EVIDENCE_SCHEMA}")
    profile_ref = evidence.get("profile")
    if not isinstance(profile_ref, dict):
        errors.append("evidence.profile must be an object")
    else:
        expected = {
            "id": profile["schema"],
            "version": profile["version"],
            "status": profile["status"],
            "source": "catalog/repository-presentation-profile.json",
        }
        if profile_ref != expected:
            errors.append("evidence.profile must exactly identify the checked profile")

    repository = evidence.get("repository")
    if not isinstance(repository, dict):
        errors.append("evidence.repository must be an object")
        return sorted(set(errors))
    if set(repository) != {
        "name",
        "type",
        "visibility",
        "lifecycle",
        "represented_commit",
    }:
        errors.append("evidence.repository fields must exactly match the v1 contract")
    if not isinstance(repository.get("name"), str) or REPOSITORY_RE.fullmatch(
        repository["name"]
    ) is None:
        errors.append("evidence.repository.name is invalid")
    represented_commit = repository.get("represented_commit")
    if not isinstance(represented_commit, str) or COMMIT_RE.fullmatch(
        represented_commit
    ) is None:
        errors.append("evidence.repository.represented_commit must be a full commit")
    try:
        resolved = resolve_requirements(
            profile,
            str(repository.get("type")),
            str(repository.get("visibility")),
            str(repository.get("lifecycle")),
        )
    except ValueError as error:
        errors.append(str(error))
        resolved = {}

    slots = evidence.get("slots")
    if not isinstance(slots, list):
        errors.append("evidence.slots must be an array")
        return sorted(set(errors))
    slot_ids: list[str] = []
    for index, slot in enumerate(slots):
        path = f"evidence.slots[{index}]"
        if not isinstance(slot, dict):
            errors.append(f"{path} must be an object")
            continue
        if set(slot) != SLOT_EVIDENCE_FIELDS:
            errors.append(f"{path} fields must exactly match the v1 contract")
        slot_id = slot.get("id")
        if not isinstance(slot_id, str):
            errors.append(f"{path}.id must be a string")
            continue
        slot_ids.append(slot_id)
        if slot_id not in resolved:
            errors.append(f"{path}.id references unknown slot {slot_id}")
            continue
        requirement = slot.get("requirement")
        state = slot.get("state")
        records = slot.get("evidence")
        reason = slot.get("reason")
        if requirement != resolved[slot_id]:
            errors.append(f"{path}.requirement does not match resolved profile")
        if state not in EVIDENCE_STATES:
            errors.append(f"{path}.state is invalid")
        if not isinstance(records, list):
            errors.append(f"{path}.evidence must be an array")
            records = []
        for record_index, record in enumerate(records):
            record_path = f"{path}.evidence[{record_index}]"
            if not isinstance(record, dict):
                errors.append(f"{record_path} must be an object")
                continue
            if set(record) != EVIDENCE_RECORD_FIELDS:
                errors.append(
                    f"{record_path} fields must exactly match the v1 contract"
                )
            if record.get("kind") not in EVIDENCE_KINDS:
                errors.append(f"{record_path}.kind is invalid")
            if not isinstance(record.get("location"), str) or not record["location"]:
                errors.append(f"{record_path}.location must be a non-empty string")
            if record.get("assertion") not in {"authoritative", "derived", "unknown"}:
                errors.append(f"{record_path}.assertion is invalid")
            if record.get("freshness") not in {
                "current",
                "stale",
                "unknown",
                "not_applicable",
            }:
                errors.append(f"{record_path}.freshness is invalid")
        if state in EVIDENCE_REQUIRED_STATES and not records:
            errors.append(f"{path}.evidence is required for state {state}")
        if requirement == "not_applicable":
            if state != "not_applicable":
                errors.append(f"{path}.state must be not_applicable")
            if not isinstance(reason, str) or not reason:
                errors.append(f"{path}.reason is required when not applicable")
        elif state == "not_applicable":
            errors.append(f"{path}.state cannot be not_applicable")
        if state == "exempt" and not any(
            isinstance(record, dict) and record.get("kind") == "approval"
            for record in records
        ):
            errors.append(f"{path}.exempt state requires approval evidence")
    if len(slot_ids) != len(set(slot_ids)):
        errors.append("evidence.slots must use unique ids")
    if set(slot_ids) != set(resolved):
        errors.append("evidence.slots must cover every profile slot exactly once")
    if slots != sorted(
        [slot for slot in slots if isinstance(slot, dict)], key=lambda slot: slot.get("id", "")
    ):
        errors.append("evidence.slots must use stable id order")

    derived = derive_state([slot for slot in slots if isinstance(slot, dict)])
    assessment = evidence.get("assessment")
    if not isinstance(assessment, dict):
        errors.append("evidence.assessment must be an object")
    else:
        if set(assessment) != {
            "state",
            "observed_at",
            "assessor",
            "assessor_version",
        }:
            errors.append(
                "evidence.assessment fields must exactly match the v1 contract"
            )
        observed_at = assessment.get("observed_at")
        if not isinstance(observed_at, str) or not observed_at.endswith("Z"):
            errors.append("evidence.assessment.observed_at must be RFC 3339 UTC")
        else:
            try:
                datetime.fromisoformat(observed_at[:-1] + "+00:00")
            except ValueError:
                errors.append("evidence.assessment.observed_at must be RFC 3339 UTC")
        for field in ("assessor", "assessor_version"):
            if not isinstance(assessment.get(field), str) or not assessment[field]:
                errors.append(f"evidence.assessment.{field} must be a non-empty string")
    if not isinstance(assessment, dict) or assessment.get("state") != derived:
        errors.append(f"evidence.assessment.state must equal derived state {derived}")
    badge = evidence.get("badge")
    if not isinstance(badge, dict):
        errors.append("evidence.badge must be an object")
    else:
        if set(badge) != {
            "label",
            "message",
            "state",
            "profile_version",
            "represented_commit",
            "evidence_url",
        }:
            errors.append("evidence.badge fields must exactly match the v1 contract")
        if badge.get("label") != profile["claim_policy"]["badge_label"]:
            errors.append("evidence.badge.label does not match the profile")
        if badge.get("state") != derived:
            errors.append(f"evidence.badge.state must equal derived state {derived}")
        if badge.get("profile_version") != profile["version"]:
            errors.append("evidence.badge.profile_version does not match the profile")
        if badge.get("represented_commit") != represented_commit:
            errors.append("evidence.badge.represented_commit does not match repository")
        if not isinstance(badge.get("evidence_url"), str) or not badge["evidence_url"]:
            errors.append("evidence.badge.evidence_url is required")
        message = badge.get("message")
        prohibited = profile["claim_policy"]["prohibited_claim_terms"]
        if message != profile["claim_policy"]["state_messages"][derived]:
            errors.append("evidence.badge.message must match the profile state message")
        if isinstance(message, str) and any(
            re.search(rf"\b{re.escape(term)}\b", message, re.IGNORECASE)
            for term in prohibited
        ):
            errors.append("evidence.badge.message contains a prohibited claim term")
    return sorted(set(errors))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("catalog/repository-presentation-profile.json"),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-profile")
    evidence = subparsers.add_parser("validate-evidence")
    evidence.add_argument("--evidence", type=Path, required=True)
    resolve = subparsers.add_parser("resolve")
    resolve.add_argument("--repository-type", required=True)
    resolve.add_argument("--visibility", required=True)
    resolve.add_argument("--lifecycle", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        profile = load_json(arguments.profile)
        if arguments.command == "validate-profile":
            errors = validate_profile(profile)
        elif arguments.command == "validate-evidence":
            errors = validate_evidence(load_json(arguments.evidence), profile)
        else:
            errors = validate_profile(profile)
            if not errors:
                resolved = resolve_requirements(
                    profile,
                    arguments.repository_type,
                    arguments.visibility,
                    arguments.lifecycle,
                )
                print(json.dumps(resolved, indent=2, sort_keys=True))
                return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"repository presentation load failed: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"repository presentation invalid: {error}", file=sys.stderr)
        return 1
    print(f"repository presentation valid: {arguments.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
