#!/usr/bin/env python3
"""Validate the proposed Agent-Ready Web profile and mechanism catalog.

This dependency-free reference checker proves the profile's cross-field,
applicability, representation-integrity, and mechanism-policy invariants. It
does not implement reusable CI, generate site artifacts, assess downstream
conformance, or publish anything.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping
from datetime import date
from pathlib import Path
from typing import Any


PROFILE_SCHEMA = "egohygiene.agent-ready-web-profile/v1"
PROFILE_VERSION = "1.0.0-alpha.2"
PROFILE_OWNER = "egohygiene/hygiene"
FIXTURE_SCHEMA = "egohygiene.agent-ready-web-mechanism-fixture/v1"
CONCERNS = ["readability", "capability", "efficiency", "commerce"]
SITE_CLASSES = ["application", "commerce", "content", "documentation", "hybrid"]
REQUIREMENT_STRENGTHS = [
    "required",
    "recommended",
    "optional",
    "conditional",
    "prohibited",
]
MATURITY_LEVELS = [
    "established",
    "published_specification",
    "emerging",
    "experimental",
]
MATURITY_LABELS = {
    "established": "established web standard / broadly deployed",
    "published_specification": "published industry specification",
    "emerging": "emerging convention",
    "experimental": "experimental/incubating capability",
}
REFERENCE_TYPES = [
    "standard",
    "industry-specification",
    "official-documentation",
    "registry",
    "maintainer-source",
]
REFERENCE_AUTHORITIES = ["primary", "supporting"]
EVIDENCE_KINDS = [
    "specification-publication",
    "implementation-observation",
    "conformance-test",
    "adoption-observation",
    "maintainer-assessment",
]
OWNERS = {"hygiene", "holon", "relay", "pace", "store", "observatory"}
ARTIFACT_KINDS = [
    "crawler-guidance",
    "origin-file",
    "page-alternate",
    "page-metadata",
    "path-file",
    "well-known-file",
]
VALIDATION_SEVERITIES = ["advisory", "error"]
SCOPED_MECHANISM_IDS = [
    "ai-crawler-guidance",
    "ai-oriented-hints",
    "canonical-metadata",
    "cats-txt",
    "entitymap-html",
    "entitymap-json",
    "llms-full-txt",
    "llms-txt",
    "markdown-alternate",
    "robots-txt",
    "sitemap-xml",
    "structured-discovery-jsonld",
]
RESOLUTION_POLICY = {
    "applicability_precedes_strength": True,
    "inapplicable_absence": "valid",
    "optional_absence": "valid",
    "recommended_absence": "advisory",
    "conditional_absence": "valid-when-condition-false",
    "required_absence": "error",
    "prohibited_presence": "error",
    "emerging_and_experimental_default": "non-blocking",
    "fabricated_placeholder": "prohibited",
}
REPRESENTATION_INTEGRITY = {
    "canonical_source": "shared-reviewed-source",
    "source_equivalence": "no-material-additions-omissions-or-changed-claims",
    "freshness": "same-build-or-source-revision",
    "canonical_url": "human-facing-canonical-url",
    "provenance": "record-source-uri-revision-generator-and-generated-at",
    "access_control": "same-or-stricter-than-canonical",
    "hidden_or_privileged_content": "prohibited",
    "drift": "invalidate-present-alternate",
}
CONTENT_NEGOTIATION_POLICY = {
    "canonical_default": "text/html",
    "markdown_selection": (
        "only-when-accept-gives-text-markdown-a-higher-positive-quality-than-text-html"
    ),
    "tie_or_wildcard": "text/html",
    "unavailable_or_unacceptable": "text-html-if-acceptable-otherwise-406",
    "vary": "Accept-required-when-selection-can-vary",
    "content_location": "explicit-markdown-uri-required-for-negotiated-markdown",
    "user_agent_selection": "prohibited",
}
ALTERNATE_DISCOVERY_POLICY = {
    "relation": "alternate",
    "media_type": "text/markdown",
    "html_or_http_link": "required",
    "canonical_backlink": "human-facing-canonical-url-required",
}
PROFILE_FIELDS = {
    "schema",
    "version",
    "status",
    "owner",
    "updated",
    "purpose",
    "concern_policy",
    "concerns",
    "site_classes",
    "requirement_strengths",
    "maturity_levels",
    "mechanism_contract",
    "resolution_policy",
    "representation_policy",
    "mechanisms",
    "compatibility",
    "extensions",
    "ownership",
}
MECHANISM_BASE_FIELDS = {
    "id",
    "title",
    "description",
    "concern",
    "requirements",
    "maturity",
    "authoritative_references",
    "registration_evidence",
    "extensions",
}
MECHANISM_POLICY_FIELDS = {
    "artifact",
    "applicability",
    "content_rules",
    "validation_rules",
}
MECHANISM_FIELDS = MECHANISM_BASE_FIELDS | MECHANISM_POLICY_FIELDS
IDENTIFIER_PATTERN = r"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$"
EXTENSION_IDENTIFIER_PATTERN = (
    r"^egohygiene\.[a-z0-9][a-z0-9.-]*\.agent-ready-web\."
    r"[a-z0-9][a-z0-9.-]*/v[0-9]+$"
)
IDENTIFIER_RE = re.compile(IDENTIFIER_PATTERN)
EXTENSION_IDENTIFIER_RE = re.compile(EXTENSION_IDENTIFIER_PATTERN)
REPOSITORY_RE = re.compile(r"^egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)$")
SAFE_PATH_RE = re.compile(r"^(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+$")


def load_json(path: Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object."""

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _text(value: Any, path: str) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return [f"{path} must be non-empty text"]
    return []


def _unique_strings(value: Any, path: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        return [f"{path} must be an array"]
    errors: list[str] = []
    if not allow_empty and not value:
        errors.append(f"{path} must not be empty")
    if any(not isinstance(item, str) or not item for item in value):
        errors.append(f"{path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"{path} must not contain duplicates")
    return errors


def _iso_date(value: Any, path: str) -> list[str]:
    if not isinstance(value, str):
        return [f"{path} must be an ISO date"]
    try:
        date.fromisoformat(value)
    except ValueError:
        return [f"{path} must be an ISO date"]
    return []


def _location(value: Any, path: str) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{path} must be an HTTPS URL or safe repository-relative path"]
    safe_parts = value.split("/")
    safe_relative = (
        SAFE_PATH_RE.fullmatch(value) is not None
        and all(part not in {".", ".."} for part in safe_parts)
    )
    if value.startswith("https://") or safe_relative:
        return []
    return [f"{path} must be an HTTPS URL or safe repository-relative path"]


def _identifier(value: Any, path: str) -> list[str]:
    if not isinstance(value, str) or IDENTIFIER_RE.fullmatch(value) is None:
        return [f"{path} is invalid"]
    return []


def _validate_vocabulary(
    value: Any,
    path: str,
    expected_ids: list[str],
    *,
    fields: set[str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return [f"{path} must be an array"]
    ids: list[Any] = []
    for index, entry in enumerate(value):
        entry_path = f"{path}[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{entry_path} must be an object")
            continue
        if set(entry) != fields:
            errors.append(f"{entry_path} fields must exactly match the v1 contract")
        entry_id = entry.get("id")
        ids.append(entry_id)
        for field in fields - {"id"}:
            errors.extend(_text(entry.get(field), f"{entry_path}.{field}"))
    if ids != expected_ids:
        errors.append(f"{path} must use the canonical stable order")
    return errors


def _validate_condition(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != {"id", "description"}:
        errors.append(f"{path} fields must exactly match the v1 contract")
    errors.extend(_identifier(value.get("id"), f"{path}.id"))
    errors.extend(_text(value.get("description"), f"{path}.description"))
    return errors


def _validate_requirement_rule(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != {"strength", "condition"}:
        errors.append(f"{path} fields must exactly match the v1 contract")
    strength = value.get("strength")
    condition = value.get("condition")
    if strength not in REQUIREMENT_STRENGTHS:
        errors.append(f"{path}.strength is invalid")
    if strength == "conditional":
        if condition is None:
            errors.append(f"{path}.condition is required when strength is conditional")
        else:
            errors.extend(_validate_condition(condition, f"{path}.condition"))
    elif condition is not None:
        errors.append(f"{path}.condition must be null unless strength is conditional")
    return errors


def _validate_requirements(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != {"default", "site_class_overrides"}:
        errors.append(f"{path} fields must exactly match the v1 contract")
    errors.extend(_validate_requirement_rule(value.get("default"), f"{path}.default"))
    overrides = value.get("site_class_overrides")
    if not isinstance(overrides, list):
        errors.append(f"{path}.site_class_overrides must be an array")
        return errors
    classes: list[Any] = []
    for index, override in enumerate(overrides):
        override_path = f"{path}.site_class_overrides[{index}]"
        if not isinstance(override, dict):
            errors.append(f"{override_path} must be an object")
            continue
        if set(override) != {"site_class", "strength", "condition"}:
            errors.append(
                f"{override_path} fields must exactly match the v1 contract"
            )
        site_class = override.get("site_class")
        classes.append(site_class)
        if site_class not in SITE_CLASSES:
            errors.append(f"{override_path}.site_class is invalid")
        errors.extend(
            _validate_requirement_rule(
                {
                    "strength": override.get("strength"),
                    "condition": override.get("condition"),
                },
                override_path,
            )
        )
    valid_classes = [value for value in classes if isinstance(value, str)]
    if len(valid_classes) != len(set(valid_classes)):
        errors.append(f"{path}.site_class_overrides must not contain duplicates")
    if valid_classes != sorted(valid_classes):
        errors.append(f"{path}.site_class_overrides must use stable site-class order")
    return errors


def _validate_artifact(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != {"kind", "locations", "media_types"}:
        errors.append(f"{path} fields must exactly match the v1 contract")
    if value.get("kind") not in ARTIFACT_KINDS:
        errors.append(f"{path}.kind is invalid")
    for field in ("locations", "media_types"):
        field_path = f"{path}.{field}"
        field_value = value.get(field)
        errors.extend(_unique_strings(field_value, field_path))
        if isinstance(field_value, list):
            strings = [item for item in field_value if isinstance(item, str)]
            if strings != sorted(strings):
                errors.append(f"{field_path} must use stable order")
    return errors


def _validate_applicability(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != {"condition", "evaluation", "inapplicable_result"}:
        errors.append(f"{path} fields must exactly match the v1 contract")
    errors.extend(_validate_condition(value.get("condition"), f"{path}.condition"))
    if value.get("evaluation") != "before-requirement-strength":
        errors.append(f"{path}.evaluation is invalid")
    if value.get("inapplicable_result") != "valid-absent":
        errors.append(f"{path}.inapplicable_result is invalid")
    return errors


def _validate_content_rules(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty array"]
    ids: list[str] = []
    fields = {"id", "strength", "description"}
    for index, rule in enumerate(value):
        rule_path = f"{path}[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{rule_path} must be an object")
            continue
        if set(rule) != fields:
            errors.append(f"{rule_path} fields must exactly match the v1 contract")
        rule_id = rule.get("id")
        errors.extend(_identifier(rule_id, f"{rule_path}.id"))
        if isinstance(rule_id, str):
            ids.append(rule_id)
        if rule.get("strength") not in {"required", "recommended", "prohibited"}:
            errors.append(f"{rule_path}.strength is invalid")
        errors.extend(_text(rule.get("description"), f"{rule_path}.description"))
    if len(ids) != len(set(ids)):
        errors.append(f"{path} must use unique ids")
    if ids != sorted(ids):
        errors.append(f"{path} must use stable id order")
    return errors


def _validate_validation_rules(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty array"]
    ids: list[str] = []
    severities: list[str] = []
    fields = {"id", "severity", "description"}
    for index, rule in enumerate(value):
        rule_path = f"{path}[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{rule_path} must be an object")
            continue
        if set(rule) != fields:
            errors.append(f"{rule_path} fields must exactly match the v1 contract")
        rule_id = rule.get("id")
        errors.extend(_identifier(rule_id, f"{rule_path}.id"))
        if isinstance(rule_id, str):
            ids.append(rule_id)
        severity = rule.get("severity")
        if severity not in VALIDATION_SEVERITIES:
            errors.append(f"{rule_path}.severity is invalid")
        elif isinstance(severity, str):
            severities.append(severity)
        errors.extend(_text(rule.get("description"), f"{rule_path}.description"))
    if len(ids) != len(set(ids)):
        errors.append(f"{path} must use unique ids")
    if ids != sorted(ids):
        errors.append(f"{path} must use stable id order")
    if "error" not in severities:
        errors.append(f"{path} must include at least one error rule")
    return errors


def _validate_maturity(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != {"level", "assessed_on", "rationale", "reference_ids"}:
        errors.append(f"{path} fields must exactly match the v1 contract")
    if value.get("level") not in MATURITY_LEVELS:
        errors.append(f"{path}.level is invalid")
    errors.extend(_iso_date(value.get("assessed_on"), f"{path}.assessed_on"))
    errors.extend(_text(value.get("rationale"), f"{path}.rationale"))
    errors.extend(_unique_strings(value.get("reference_ids"), f"{path}.reference_ids"))
    return errors


def _validate_references(value: Any, path: str) -> tuple[list[str], dict[str, str]]:
    errors: list[str] = []
    authorities: dict[str, str] = {}
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty array"], authorities
    ids: list[str] = []
    fields = {
        "id",
        "title",
        "publisher",
        "type",
        "authority",
        "location",
        "retrieved_on",
    }
    for index, reference in enumerate(value):
        reference_path = f"{path}[{index}]"
        if not isinstance(reference, dict):
            errors.append(f"{reference_path} must be an object")
            continue
        if set(reference) != fields:
            errors.append(
                f"{reference_path} fields must exactly match the v1 contract"
            )
        reference_id = reference.get("id")
        errors.extend(_identifier(reference_id, f"{reference_path}.id"))
        if isinstance(reference_id, str):
            ids.append(reference_id)
            if isinstance(reference.get("authority"), str):
                authorities[reference_id] = reference["authority"]
        for field in ("title", "publisher"):
            errors.extend(_text(reference.get(field), f"{reference_path}.{field}"))
        if reference.get("type") not in REFERENCE_TYPES:
            errors.append(f"{reference_path}.type is invalid")
        if reference.get("authority") not in REFERENCE_AUTHORITIES:
            errors.append(f"{reference_path}.authority is invalid")
        errors.extend(
            _location(reference.get("location"), f"{reference_path}.location")
        )
        errors.extend(
            _iso_date(reference.get("retrieved_on"), f"{reference_path}.retrieved_on")
        )
    if len(ids) != len(set(ids)):
        errors.append(f"{path} must use unique ids")
    if ids != sorted(ids):
        errors.append(f"{path} must use stable id order")
    if "primary" not in authorities.values():
        errors.append(
            f"{path} must include at least one primary authoritative reference"
        )
    return errors, authorities


def _validate_registration_evidence(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty array"]
    ids: list[str] = []
    fields = {"id", "kind", "location", "description", "observed_on"}
    for index, evidence in enumerate(value):
        evidence_path = f"{path}[{index}]"
        if not isinstance(evidence, dict):
            errors.append(f"{evidence_path} must be an object")
            continue
        if set(evidence) != fields:
            errors.append(f"{evidence_path} fields must exactly match the v1 contract")
        evidence_id = evidence.get("id")
        errors.extend(_identifier(evidence_id, f"{evidence_path}.id"))
        if isinstance(evidence_id, str):
            ids.append(evidence_id)
        if evidence.get("kind") not in EVIDENCE_KINDS:
            errors.append(f"{evidence_path}.kind is invalid")
        errors.extend(_location(evidence.get("location"), f"{evidence_path}.location"))
        errors.extend(
            _text(evidence.get("description"), f"{evidence_path}.description")
        )
        errors.extend(
            _iso_date(evidence.get("observed_on"), f"{evidence_path}.observed_on")
        )
    if len(ids) != len(set(ids)):
        errors.append(f"{path} must use unique ids")
    if ids != sorted(ids):
        errors.append(f"{path} must use stable id order")
    return errors


def validate_mechanism(value: Any, *, path: str = "mechanism") -> list[str]:
    """Return deterministic errors for one mechanism registry record."""

    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    fields = set(value)
    if fields != MECHANISM_BASE_FIELDS and fields != MECHANISM_FIELDS:
        errors.append(f"{path} fields must exactly match the v1 contract")
    errors.extend(_identifier(value.get("id"), f"{path}.id"))
    for field in ("title", "description"):
        errors.extend(_text(value.get(field), f"{path}.{field}"))
    concern = value.get("concern")
    if not isinstance(concern, str) or concern not in CONCERNS:
        errors.append(f"{path}.concern must identify exactly one canonical concern")
    errors.extend(
        _validate_requirements(value.get("requirements"), f"{path}.requirements")
    )
    policy_fields = fields & MECHANISM_POLICY_FIELDS
    if policy_fields:
        if policy_fields != MECHANISM_POLICY_FIELDS:
            errors.append(f"{path} policy fields must be complete when present")
        errors.extend(_validate_artifact(value.get("artifact"), f"{path}.artifact"))
        errors.extend(
            _validate_applicability(
                value.get("applicability"),
                f"{path}.applicability",
            )
        )
        errors.extend(
            _validate_content_rules(
                value.get("content_rules"),
                f"{path}.content_rules",
            )
        )
        errors.extend(
            _validate_validation_rules(
                value.get("validation_rules"),
                f"{path}.validation_rules",
            )
        )
    errors.extend(_validate_maturity(value.get("maturity"), f"{path}.maturity"))
    maturity = value.get("maturity")
    requirements = value.get("requirements")
    if (
        policy_fields == MECHANISM_POLICY_FIELDS
        and isinstance(maturity, dict)
        and maturity.get("level") in {"emerging", "experimental"}
        and isinstance(requirements, dict)
    ):
        rules = [requirements.get("default")]
        overrides = requirements.get("site_class_overrides")
        if isinstance(overrides, list):
            rules.extend(overrides)
        if any(
            isinstance(rule, dict) and rule.get("strength") == "required"
            for rule in rules
        ):
            errors.append(
                f"{path} emerging or experimental mechanisms must remain "
                "non-blocking by default"
            )
    reference_errors, authorities = _validate_references(
        value.get("authoritative_references"),
        f"{path}.authoritative_references",
    )
    errors.extend(reference_errors)
    if isinstance(maturity, dict) and isinstance(maturity.get("reference_ids"), list):
        reference_ids = maturity["reference_ids"]
        unknown = sorted(
            reference_id
            for reference_id in reference_ids
            if isinstance(reference_id, str) and reference_id not in authorities
        )
        if unknown:
            errors.append(
                f"{path}.maturity.reference_ids contains unknown references: "
                + ", ".join(unknown)
            )
        if not any(
            authorities.get(reference_id) == "primary"
            for reference_id in reference_ids
            if isinstance(reference_id, str)
        ):
            errors.append(
                f"{path}.maturity.reference_ids must include a primary "
                "authoritative reference"
            )
    errors.extend(
        _validate_registration_evidence(
            value.get("registration_evidence"),
            f"{path}.registration_evidence",
        )
    )
    extensions = value.get("extensions")
    if not isinstance(extensions, dict):
        errors.append(f"{path}.extensions must be an object")
    else:
        for extension_id, payload in extensions.items():
            if EXTENSION_IDENTIFIER_RE.fullmatch(extension_id) is None:
                errors.append(f"{path}.extensions contains invalid id {extension_id}")
            if not isinstance(payload, dict):
                errors.append(f"{path}.extensions.{extension_id} must be an object")
    return sorted(set(errors))


def _validate_representation_policy(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    fields = {
        "scope",
        "integrity",
        "content_negotiation",
        "alternate_discovery",
        "authoritative_references",
    }
    if set(value) != fields:
        errors.append(f"{path} fields must exactly match the v1 contract")
    if value.get("scope") != "public-source-equivalent-alternate-representations":
        errors.append(f"{path}.scope is invalid")
    if value.get("integrity") != REPRESENTATION_INTEGRITY:
        errors.append(f"{path}.integrity must preserve canonical source integrity")
    if value.get("content_negotiation") != CONTENT_NEGOTIATION_POLICY:
        errors.append(f"{path}.content_negotiation is invalid")
    if value.get("alternate_discovery") != ALTERNATE_DISCOVERY_POLICY:
        errors.append(f"{path}.alternate_discovery is invalid")
    reference_errors, _ = _validate_references(
        value.get("authoritative_references"),
        f"{path}.authoritative_references",
    )
    errors.extend(reference_errors)
    return errors


def validate_profile(profile: Mapping[str, Any]) -> list[str]:
    """Return deterministic errors for the canonical profile foundation."""

    errors: list[str] = []
    if set(profile) != PROFILE_FIELDS:
        errors.append("profile fields must exactly match the v1 contract")
    if profile.get("schema") != PROFILE_SCHEMA:
        errors.append(f"profile.schema must be {PROFILE_SCHEMA}")
    if profile.get("version") != PROFILE_VERSION:
        errors.append(f"profile.version must be {PROFILE_VERSION}")
    if profile.get("status") not in {"proposed", "active", "deprecated", "superseded"}:
        errors.append("profile.status is invalid")
    if profile.get("owner") != PROFILE_OWNER:
        errors.append(f"profile.owner must be {PROFILE_OWNER}")
    errors.extend(_iso_date(profile.get("updated"), "profile.updated"))
    errors.extend(_text(profile.get("purpose"), "profile.purpose"))

    if profile.get("concern_policy") != {
        "primary_concern_cardinality": "exactly-one",
        "independent_requirement_resolution": True,
        "cross_concern_inference": "forbidden",
    }:
        errors.append(
            "profile.concern_policy must keep concerns structurally independent"
        )
    errors.extend(
        _validate_vocabulary(
            profile.get("concerns"),
            "profile.concerns",
            CONCERNS,
            fields={"id", "title", "definition", "boundary"},
        )
    )
    errors.extend(
        _validate_vocabulary(
            profile.get("site_classes"),
            "profile.site_classes",
            SITE_CLASSES,
            fields={"id", "title", "definition"},
        )
    )
    errors.extend(
        _validate_vocabulary(
            profile.get("requirement_strengths"),
            "profile.requirement_strengths",
            REQUIREMENT_STRENGTHS,
            fields={"id", "definition"},
        )
    )
    maturity_levels = profile.get("maturity_levels")
    errors.extend(
        _validate_vocabulary(
            maturity_levels,
            "profile.maturity_levels",
            MATURITY_LEVELS,
            fields={"id", "label", "definition"},
        )
    )
    if isinstance(maturity_levels, list):
        for index, entry in enumerate(maturity_levels):
            if isinstance(entry, dict) and entry.get("id") in MATURITY_LABELS:
                expected = MATURITY_LABELS[entry["id"]]
                if entry.get("label") != expected:
                    errors.append(
                        f"profile.maturity_levels[{index}].label must be {expected}"
                    )

    expected_mechanism_contract = {
        "identifier_pattern": IDENTIFIER_PATTERN,
        "reference_types": REFERENCE_TYPES,
        "reference_authorities": REFERENCE_AUTHORITIES,
        "evidence_kinds": EVIDENCE_KINDS,
        "evidence_scope": "mechanism-registration-only",
        "site_conformance_evidence": "deferred",
        "required_primary_references": 1,
        "required_registration_evidence": 1,
    }
    if profile.get("mechanism_contract") != expected_mechanism_contract:
        errors.append("profile.mechanism_contract must exactly match the v1 foundation")

    if profile.get("resolution_policy") != RESOLUTION_POLICY:
        errors.append(
            "profile.resolution_policy must preserve truthful applicability and absence"
        )
    errors.extend(
        _validate_representation_policy(
            profile.get("representation_policy"),
            "profile.representation_policy",
        )
    )

    mechanisms = profile.get("mechanisms")
    if not isinstance(mechanisms, list):
        errors.append("profile.mechanisms must be an array")
    else:
        mechanism_ids: list[str] = []
        for index, mechanism in enumerate(mechanisms):
            errors.extend(
                validate_mechanism(
                    mechanism,
                    path=f"profile.mechanisms[{index}]",
                )
            )
            if isinstance(mechanism, dict) and isinstance(mechanism.get("id"), str):
                mechanism_ids.append(mechanism["id"])
                mechanism_path = f"profile.mechanisms[{index}]"
                if set(mechanism) != MECHANISM_FIELDS:
                    errors.append(
                        f"{mechanism_path} must include the complete catalog policy"
                    )
                requirements = mechanism.get("requirements")
                if isinstance(requirements, dict):
                    overrides = requirements.get("site_class_overrides")
                    if isinstance(overrides, list):
                        classes = [
                            override.get("site_class")
                            for override in overrides
                            if isinstance(override, dict)
                        ]
                        if classes != SITE_CLASSES:
                            errors.append(
                                f"{mechanism_path}.requirements.site_class_overrides "
                                "must resolve every canonical site class"
                            )
                maturity = mechanism.get("maturity")
                if (
                    isinstance(maturity, dict)
                    and maturity.get("level") in {"emerging", "experimental"}
                    and isinstance(requirements, dict)
                ):
                    rules = [requirements.get("default")]
                    overrides = requirements.get("site_class_overrides")
                    if isinstance(overrides, list):
                        rules.extend(overrides)
                    if any(
                        isinstance(rule, dict) and rule.get("strength") == "required"
                        for rule in rules
                    ):
                        errors.append(
                            f"{mechanism_path} emerging or experimental mechanisms "
                            "must remain non-blocking by default"
                        )
                if mechanism.get("concern") not in {"readability", "efficiency"}:
                    errors.append(
                        f"{mechanism_path}.concern exceeds checkpoint 2 scope"
                    )
        if len(mechanism_ids) != len(set(mechanism_ids)):
            errors.append("profile.mechanisms must use unique ids")
        if mechanism_ids != sorted(mechanism_ids):
            errors.append("profile.mechanisms must use stable id order")
        if mechanism_ids != SCOPED_MECHANISM_IDS:
            errors.append(
                "profile.mechanisms must exactly match the checkpoint 2 catalog"
            )

    compatibility = profile.get("compatibility")
    compatibility_fields = {
        "contract_major",
        "versioning",
        "consumer_pinning",
        "same_major_guarantee",
        "additive_changes",
        "breaking_changes",
        "unknown_core_values",
        "unknown_extensions",
    }
    if not isinstance(compatibility, dict):
        errors.append("profile.compatibility must be an object")
    else:
        if set(compatibility) != compatibility_fields:
            errors.append(
                "profile.compatibility fields must exactly match the v1 contract"
            )
        expected_values = {
            "contract_major": 1,
            "versioning": "semantic-versioning",
            "consumer_pinning": "exact-version-or-immutable-revision",
            "unknown_core_values": "fail-closed",
            "unknown_extensions": (
                "preserve-uninterpreted-and-exclude-from-core-conformance"
            ),
        }
        for field, expected in expected_values.items():
            if compatibility.get(field) != expected:
                errors.append(f"profile.compatibility.{field} is invalid")
        errors.extend(
            _text(
                compatibility.get("same_major_guarantee"),
                "profile.compatibility.same_major_guarantee",
            )
        )
        for field in ("additive_changes", "breaking_changes"):
            errors.extend(
                _unique_strings(
                    compatibility.get(field),
                    f"profile.compatibility.{field}",
                )
            )

    extensions = profile.get("extensions")
    extension_fields = {
        "identifier_pattern",
        "registered",
        "unknown_behavior",
        "allowed",
        "prohibited",
    }
    if not isinstance(extensions, dict):
        errors.append("profile.extensions must be an object")
    else:
        if set(extensions) != extension_fields:
            errors.append(
                "profile.extensions fields must exactly match the v1 contract"
            )
        if extensions.get("identifier_pattern") != EXTENSION_IDENTIFIER_PATTERN:
            errors.append("profile.extensions.identifier_pattern is invalid")
        expected_unknown = "preserve-uninterpreted-and-exclude-from-core-conformance"
        if extensions.get("unknown_behavior") != expected_unknown:
            errors.append("profile.extensions.unknown_behavior is invalid")
        for field in ("allowed", "prohibited"):
            errors.extend(
                _unique_strings(
                    extensions.get(field),
                    f"profile.extensions.{field}",
                )
            )
        registered = extensions.get("registered")
        if not isinstance(registered, list):
            errors.append("profile.extensions.registered must be an array")
        else:
            registered_ids: list[str] = []
            fields = {"id", "owner", "schema", "status", "purpose"}
            for index, extension in enumerate(registered):
                extension_path = f"profile.extensions.registered[{index}]"
                if not isinstance(extension, dict):
                    errors.append(f"{extension_path} must be an object")
                    continue
                if set(extension) != fields:
                    errors.append(
                        f"{extension_path} fields must exactly match the v1 contract"
                    )
                extension_id = extension.get("id")
                if (
                    not isinstance(extension_id, str)
                    or EXTENSION_IDENTIFIER_RE.fullmatch(extension_id) is None
                ):
                    errors.append(f"{extension_path}.id is invalid")
                else:
                    registered_ids.append(extension_id)
                owner = extension.get("owner")
                if not isinstance(owner, str) or REPOSITORY_RE.fullmatch(owner) is None:
                    errors.append(f"{extension_path}.owner is invalid")
                schema = extension.get("schema")
                schema_is_safe = (
                    isinstance(schema, str)
                    and schema.startswith("schemas/")
                    and schema.endswith(".json")
                    and SAFE_PATH_RE.fullmatch(schema) is not None
                    and all(part not in {".", ".."} for part in schema.split("/"))
                )
                if not schema_is_safe:
                    errors.append(f"{extension_path}.schema is invalid")
                if extension.get("status") not in {"proposed", "active", "deprecated"}:
                    errors.append(f"{extension_path}.status is invalid")
                errors.extend(
                    _text(extension.get("purpose"), f"{extension_path}.purpose")
                )
            if len(registered_ids) != len(set(registered_ids)):
                errors.append("profile.extensions.registered must use unique ids")
            if registered_ids != sorted(registered_ids):
                errors.append("profile.extensions.registered must use stable id order")

    ownership = profile.get("ownership")
    if not isinstance(ownership, dict) or set(ownership) != OWNERS:
        errors.append("profile.ownership must declare every bounded owner")
    else:
        for owner, boundary in ownership.items():
            path = f"profile.ownership.{owner}"
            if not isinstance(boundary, dict):
                errors.append(f"{path} must be an object")
                continue
            if set(boundary) != {"owns", "excludes"}:
                errors.append(f"{path} fields must exactly match the v1 contract")
            errors.extend(_text(boundary.get("owns"), f"{path}.owns"))
            errors.extend(_text(boundary.get("excludes"), f"{path}.excludes"))
    return sorted(set(errors))


def validate_fixture(fixture: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    """Validate a synthetic fixture envelope and its mechanism independently."""

    envelope_errors: list[str] = []
    fields = {"schema", "name", "expected", "synthetic", "mechanism", "expected_errors"}
    if set(fixture) != fields:
        envelope_errors.append("fixture fields must exactly match the v1 contract")
    if fixture.get("schema") != FIXTURE_SCHEMA:
        envelope_errors.append(f"fixture.schema must be {FIXTURE_SCHEMA}")
    envelope_errors.extend(_identifier(fixture.get("name"), "fixture.name"))
    if fixture.get("expected") not in {"valid", "invalid"}:
        envelope_errors.append("fixture.expected is invalid")
    if fixture.get("synthetic") is not True:
        envelope_errors.append("fixture.synthetic must be true")
    expected_errors = fixture.get("expected_errors")
    envelope_errors.extend(
        _unique_strings(expected_errors, "fixture.expected_errors", allow_empty=True)
    )
    if fixture.get("expected") == "valid" and expected_errors != []:
        envelope_errors.append(
            "fixture.expected_errors must be empty for a valid fixture"
        )
    if fixture.get("expected") == "invalid" and expected_errors == []:
        envelope_errors.append("fixture.expected_errors must identify invalid coverage")
    mechanism_errors = validate_mechanism(fixture.get("mechanism"))
    return sorted(set(envelope_errors)), mechanism_errors


def validate_fixture_directory(path: Path) -> list[str]:
    """Validate all checked-in valid and invalid compatibility fixtures."""

    errors: list[str] = []
    fixture_paths = sorted(path.glob("*.json"))
    if not fixture_paths:
        return [f"no fixtures found in {path}"]
    expected_kinds: set[str] = set()
    for fixture_path in fixture_paths:
        try:
            fixture = load_json(fixture_path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"{fixture_path}: load failed: {error}")
            continue
        envelope_errors, mechanism_errors = validate_fixture(fixture)
        errors.extend(f"{fixture_path}: {error}" for error in envelope_errors)
        expected = fixture.get("expected")
        if isinstance(expected, str):
            expected_kinds.add(expected)
        if expected == "valid" and mechanism_errors:
            errors.extend(
                f"{fixture_path}: unexpected: {error}" for error in mechanism_errors
            )
        if expected == "invalid":
            if not mechanism_errors:
                errors.append(
                    f"{fixture_path}: expected invalid mechanism was accepted"
                )
            expected_errors = fixture.get("expected_errors")
            listed_errors = expected_errors if isinstance(expected_errors, list) else []
            for expected_error in listed_errors:
                if expected_error not in mechanism_errors:
                    errors.append(
                        f"{fixture_path}: missing expected error: {expected_error}"
                    )
    if expected_kinds != {"valid", "invalid"}:
        errors.append("fixture directory must contain valid and invalid coverage")
    return sorted(set(errors))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("catalog/agent-ready-web-profile.json"),
        help="path to the canonical Agent-Ready Web profile",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-profile")
    mechanism = subparsers.add_parser("validate-mechanism")
    mechanism.add_argument("--input", type=Path, required=True)
    fixtures = subparsers.add_parser("validate-fixtures")
    fixtures.add_argument(
        "--fixtures",
        type=Path,
        default=Path("fixtures/agent-ready-web"),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        profile = load_json(arguments.profile)
        profile_errors = validate_profile(profile)
        if arguments.command == "validate-profile":
            errors = profile_errors
        elif profile_errors:
            errors = [f"profile invalid: {error}" for error in profile_errors]
        elif arguments.command == "validate-mechanism":
            errors = validate_mechanism(load_json(arguments.input))
        else:
            errors = validate_fixture_directory(arguments.fixtures)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"agent-ready web load failed: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"agent-ready web invalid: {error}", file=sys.stderr)
        return 1
    if arguments.command == "validate-fixtures":
        fixture_count = len(list(arguments.fixtures.glob("*.json")))
        print(f"agent-ready web fixtures valid: {fixture_count}")
    else:
        print(f"agent-ready web valid: {arguments.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
