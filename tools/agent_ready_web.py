#!/usr/bin/env python3
"""Validate the proposed Agent-Ready Web profile and compatibility evidence.

This dependency-free reference checker proves the profile's cross-field,
applicability, representation-integrity, and mechanism-policy invariants. It
also validates deterministic, revision-bound synthetic or site-owned evidence.
It does not implement reusable CI, generate site artifacts, certify consumers,
or publish anything.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


PROFILE_SCHEMA = "egohygiene.agent-ready-web-profile/v1"
PROFILE_VERSION = "1.0.0-alpha.4"
PROFILE_OWNER = "egohygiene/hygiene"
FIXTURE_SCHEMA = "egohygiene.agent-ready-web-mechanism-fixture/v1"
CONFORMANCE_SCHEMA = "egohygiene.agent-ready-web-conformance/v1"
CONFORMANCE_FIXTURE_SCHEMA = (
    "egohygiene.agent-ready-web-conformance-fixture/v1"
)
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
OWNERS = {
    "hygiene",
    "holon",
    "relay",
    "pace",
    "store",
    "observatory",
    "sites",
}
ARTIFACT_KINDS = [
    "browser-capability",
    "crawler-guidance",
    "origin-file",
    "page-alternate",
    "page-metadata",
    "path-file",
    "well-known-file",
]
VALIDATION_SEVERITIES = ["advisory", "error"]
SCOPED_MECHANISM_IDS = [
    "ads-txt",
    "ai-crawler-guidance",
    "ai-oriented-hints",
    "app-ads-txt",
    "canonical-metadata",
    "cats-txt",
    "commerce-product-offer-jsonld",
    "entitymap-html",
    "entitymap-json",
    "llms-full-txt",
    "llms-txt",
    "markdown-alternate",
    "mcp-b-runtime",
    "robots-txt",
    "sitemap-xml",
    "structured-discovery-jsonld",
    "webmcp-tools",
]
CAPABILITY_CLASSES = ["read-only", "state-changing"]
CAPABILITY_PROTOCOLS = ["mcp-b", "webmcp"]
CAPABILITY_PROTOCOL_BINDINGS = {
    "mcp-b": {
        "protocol_revision": "package-release-or-immutable-repository-revision",
        "discovery_surface": "mcp-b-runtime-or-bridge-tool-list",
    },
    "webmcp": {
        "protocol_revision": "2026-09-10-community-group-draft",
        "discovery_surface": "document.modelContext-active-document-tool-list",
    },
}
COMMERCE_ROLES = [
    "advertising-authorization-declaration",
    "descriptive-product-offer",
]
COMMERCE_ROLE_IDENTITY_SOURCES = {
    "advertising-authorization-declaration": {
        "publisher-and-advertising-system-contract-evidence",
        "verified-app-store-developer-domain-and-advertising-system-contract-evidence",
    },
    "descriptive-product-offer": {
        "canonical-human-facing-product-and-offer-source",
    },
}
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
CAPABILITY_POLICY = {
    "scope": "browser-agent-tool-exposure",
    "protocol_status": {
        "webmcp": "draft-community-group-report-not-a-web-standard",
        "mcp_b": "experimental-implementation-not-webmcp-or-mcp-authority",
    },
    "declaration_contract": {
        "identity": "stable-origin-bound-capability-id",
        "protocol_revision": "exact-version-or-immutable-revision-required",
        "discovery": "protocol-native-active-authorized-context-plus-origin-bound-contract-evidence",
        "input_contract": "versioned-json-schema-and-runtime-validation-required",
        "output_contract": "versioned-json-schema-and-runtime-validation-required",
        "compatibility": "breaking-input-output-effect-or-permission-change-requires-new-capability-major",
        "unknown_fields": "fail-closed",
    },
    "classification": {
        "classes": CAPABILITY_CLASSES,
        "unclassified": "treat-as-state-changing-and-deny",
        "read_only": {
            "state_effects": "prohibited",
            "sensitive_data": "explicit-permission-and-consent-required",
            "confirmation": "required-before-sensitive-disclosure",
        },
        "state_changing": {
            "effects": "declare-completely-before-consent",
            "permission": "explicit-operation-scoped",
            "confirmation": "fresh-human-confirmation-before-consequential-or-irreversible-effect",
            "retry": "no-automatic-retry-without-idempotency-or-new-confirmation",
        },
    },
    "security": {
        "permission": "explicit-operation-scoped-and-revocable",
        "consent": "informed-specific-and-obtained-before-invocation",
        "least_privilege": "minimum-data-scope-and-duration",
        "origin_binding": "secure-exact-origin-and-current-document",
        "authentication": "required-when-human-ui-requires-authentication",
        "authorization": "server-revalidated-for-every-invocation",
        "credential_handling": "no-token-passthrough-or-secret-in-schema-description-output",
        "data_minimization": "request-and-return-only-necessary-data",
        "annotations": "untrusted-hints-never-authority",
        "prompt_injection": "tool-metadata-input-and-output-treated-as-untrusted",
    },
    "execution_evidence": {
        "provenance": "record-capability-id-version-origin-actor-and-contract-digests",
        "audit": "tamper-evident-invocation-decision-result-and-confirmation-record",
        "observability": "correlation-id-status-latency-and-redacted-error",
        "revocation": "effective-before-next-invocation",
        "expiry": "permissions-consent-and-handles-expire-explicitly",
        "replay_protection": "nonce-or-idempotency-key-bound-to-actor-origin-action-and-expiry",
        "rate_limits": "declared-and-enforced-per-actor-origin-and-capability",
    },
    "failure_policy": {
        "default": "deny-and-perform-no-state-change",
        "partial_failure": "report-observed-effects-and-do-not-claim-rollback",
        "recovery": "human-visible-resume-or-compensating-path-required",
        "timeouts": "bounded-and-cancelable",
        "unknown_or_stale_contract": "deny",
    },
    "publication_gate": "experimental-capability-absence-is-non-blocking-and-present-exposure-must-pass-all-guards",
}
COMMERCE_POLICY = {
    "scope": "descriptive-commerce-and-advertising-boundaries",
    "descriptive_metadata": {
        "media_type": "application/ld+json",
        "vocabulary": ["https://schema.org/Offer", "https://schema.org/Product"],
        "visible_fact_parity": "required",
        "seller_identity": "evidence-backed-explicit-or-omitted",
        "availability_price_currency": "current-visible-and-source-backed",
        "potential_action": "descriptive-only-no-execution-authority",
    },
    "guarded_actions": {
        "owner": "egohygiene/store",
        "capability_class": "state-changing",
        "contract": "versioned-store-owned-contract-required",
        "metadata_authority": "none",
        "missing_contract": "do-not-expose-or-invoke",
        "confirmation": "agent-ready-web-capability-policy-required",
        "recovery": "store-contract-plus-agent-ready-web-failure-policy-required",
    },
    "advertising": {
        "ads_txt_applicability": "actual-web-programmatic-inventory-authorization-or-explicit-iab-no-seller-declaration",
        "app_ads_txt_applicability": "distributed-app-programmatic-inventory-linked-to-developer-domain-or-explicit-iab-no-seller-declaration",
        "relationship_evidence": "current-publisher-and-ad-system-account-evidence-required",
        "direct_or_reseller": "must-match-real-contractual-account-relationship",
        "owner_manager_and_partner_domains": "must-match-current-documented-relationship",
        "no_relationships": "artifact-absent-with-explicit-not-applicable-evidence-or-exact-iab-no-seller-placeholder",
        "placeholder": "iab-reserved-sentinel-only-never-a-seller-relationship",
        "invented_relationships": "prohibited",
        "absence": "valid-when-inapplicable",
    },
    "separation": {
        "metadata_to_capability_inference": "forbidden",
        "advertising_to_commerce_action": "forbidden",
        "offer_to_purchase_authority": "forbidden",
    },
}
INTEGRATION_POLICY = {
    "composition": {
        "concerns": CONCERNS,
        "evaluation": "resolve-each-mechanism-within-primary-concern-then-aggregate",
        "cross_concern_substitution": "prohibited",
        "boundary_preservation": "required",
    },
    "cross_layer_invariants": {
        "non_authoritative_inputs": [
            "discovery",
            "structured-metadata",
            "advertising-declaration",
            "maturity-classification",
        ],
        "cannot_grant": [
            "capability",
            "consent",
            "authorization",
            "transaction-authority",
        ],
        "capability_source": "explicit-versioned-origin-bound-capability-contract-only",
        "consent_source": "fresh-explicit-human-interaction-only",
        "authorization_source": "server-revalidated-per-invocation-only",
        "transaction_source": "store-owned-contract-plus-fresh-confirmation-and-server-authorization-only",
    },
}
CONFORMANCE_LEVELS = ["nonconformant", "exempt", "baseline", "recommended"]
APPLICABILITY_STATES = ["applicable", "not-applicable", "unknown"]
RESOLVED_STRENGTHS = [
    "required",
    "recommended",
    "optional",
    "prohibited",
    "inapplicable",
    "unresolved",
]
CONDITIONAL_STATES = ["met", "not-met", "unknown"]
PRESENCE_STATES = ["present", "absent"]
MECHANISM_VALIDATION_STATES = ["passed", "failed", "not-run"]
DIAGNOSTIC_SEVERITIES = ["error", "advisory", "information"]
EVIDENCE_KINDS_SITE = [
    "approval",
    "configuration",
    "contract",
    "generated-artifact",
    "http-response",
    "human-review",
    "source-manifest",
]
CONFORMANCE_CLAIM = (
    "assessment-only-no-certification-adoption-publication-or-authority"
)
AUTHORITY_ASSERTIONS = {
    "discovery_grants_capability": False,
    "structured_metadata_grants_capability": False,
    "advertising_grants_capability": False,
    "maturity_grants_capability": False,
    "surface_grants_consent": False,
    "surface_grants_authorization": False,
    "surface_grants_transaction_authority": False,
}
CONFORMANCE_POLICY = {
    "schema": CONFORMANCE_SCHEMA,
    "profile_applicability": {
        "scope": "public-human-facing-https-site",
        "not_applicable": "explicit-reason-and-current-evidence-required",
        "unknown": "error",
    },
    "resolution": {
        "order": [
            "verify-profile-pin",
            "select-site-class",
            "evaluate-applicability",
            "resolve-conditional-rule",
            "apply-strength",
            "validate-present-mechanism",
            "apply-narrow-exemption",
            "derive-diagnostics",
            "derive-level",
        ],
        "declared_strengths": REQUIREMENT_STRENGTHS,
        "resolved_strengths": RESOLVED_STRENGTHS,
        "applicability_states": APPLICABILITY_STATES,
        "conditional": {
            "met": "required",
            "not_met": "inapplicable",
            "unknown": "unresolved-error",
        },
        "experimental": {
            "absent": "non-blocking",
            "present": "full-present-mechanism-validation-required",
            "authority": "none",
        },
    },
    "levels": [
        {
            "id": "nonconformant",
            "definition": "One or more error diagnostics remain after deterministic resolution.",
        },
        {
            "id": "exempt",
            "definition": "No unexempted error remains and at least one narrow approved exemption is active; this is not passing.",
        },
        {
            "id": "baseline",
            "definition": "No error or exemption remains, but at least one advisory remains.",
        },
        {
            "id": "recommended",
            "definition": "No error, advisory, or exemption remains; optional or experimental absence is still allowed.",
        },
    ],
    "level_precedence": CONFORMANCE_LEVELS,
    "diagnostics": {
        "shape": "stable-code-severity-mechanism-path-message",
        "severities": DIAGNOSTIC_SEVERITIES,
        "ordering": "profile-mechanism-order-then-severity-code-and-path",
        "unknown_state": "error",
        "claim_limit": CONFORMANCE_CLAIM,
    },
    "evidence": {
        "profile_pin": "exact-version-plus-resolved-immutable-revision-and-sha256",
        "subject_revision": "immutable-revision",
        "mechanism_cardinality": "exactly-once-in-profile-order",
        "current_evidence": "subject-revision-bound-observed-no-later-than-assessment-and-required-for-applicability-and-present-mechanisms",
        "privacy": "allowlisted-minimized-no-secrets-personal-data-or-credentials",
        "authority_assertions": "must-match-cross-layer-invariants",
    },
    "exemptions": {
        "scope": "single-required-absence-only",
        "requirements": "named-owner-reason-approval-evidence-and-future-expiry",
        "non_exemptable": [
            "profile-pin",
            "unknown-applicability",
            "prohibited-presence",
            "present-mechanism-validation",
            "privacy-security-consent-authorization-transaction-and-cross-layer-invariants",
        ],
        "effect": "distinct-exempt-level-never-passing-or-recommended",
    },
}
REFERENCE_REVIEW_CHECKS = [
    "primary-authority-present-and-resolvable",
    "maturity-rationale-supported-by-primary-source",
    "standards-status-not-overstated",
    "living-and-draft-sources-rechecked-at-upgrade",
]
CONSUMER_RESOLUTION_POLICY = {
    "canonical_repository": "egohygiene/hygiene",
    "canonical_path": "catalog/agent-ready-web-profile.json",
    "supported_pins": [
        "exact-released-version-with-resolved-revision-and-sha256",
        "immutable-repository-revision-with-sha256",
    ],
    "digest": "sha256-of-canonical-json-utf8",
    "proposed_profile_use": "review-and-compatibility-testing-only",
    "production_eligibility": "active-lifecycle-plus-eligible-immutable-pin-required",
    "policy_copying": "prohibited",
    "unsupported_version": "fail-closed-with-upgrade-diagnostic",
    "upgrade": "explicit-reviewed-pin-change-full-revalidation-and-fixture-replay",
    "downgrade": "explicit-reviewed-pin-change-and-no-newer-semantics-assumed",
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
    "capability_policy",
    "commerce_policy",
    "integration_policy",
    "conformance_policy",
    "reference_review",
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
CAPABILITY_BINDING_FIELD = "capability"
COMMERCE_BINDING_FIELD = "commerce"
CAPABILITY_BINDING_FIELDS = {
    "protocol",
    "protocol_revision",
    "implementation_pin",
    "identity",
    "discovery_surface",
    "classes",
    "input_contract",
    "output_contract",
    "compatibility",
}
COMMERCE_BINDING_FIELDS = {
    "role",
    "identity_source",
    "executable_authority",
    "transaction_contract",
}
IDENTIFIER_PATTERN = r"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$"
EXTENSION_IDENTIFIER_PATTERN = (
    r"^egohygiene\.[a-z0-9][a-z0-9.-]*\.agent-ready-web\."
    r"[a-z0-9][a-z0-9.-]*/v[0-9]+$"
)
IDENTIFIER_RE = re.compile(IDENTIFIER_PATTERN)
EXTENSION_IDENTIFIER_RE = re.compile(EXTENSION_IDENTIFIER_PATTERN)
REPOSITORY_RE = re.compile(r"^egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)$")
SAFE_PATH_RE = re.compile(r"^(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?$"
)


def load_json(path: Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object."""

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def profile_digest(profile: Mapping[str, Any]) -> str:
    """Return the representation-independent digest used by consumer pins."""

    canonical = json.dumps(
        profile,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


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


def _iso_datetime(value: Any, path: str) -> list[str]:
    if not isinstance(value, str):
        return [f"{path} must be an ISO date-time"]
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return [f"{path} must be an ISO date-time"]
    if parsed.tzinfo is None:
        return [f"{path} must include a timezone"]
    return []


def _https_origin(value: Any, path: str) -> list[str]:
    if not isinstance(value, str):
        return [f"{path} must be an HTTPS origin"]
    try:
        parsed = urlsplit(value)
        parsed.port
    except ValueError:
        return [f"{path} must be an HTTPS origin"]
    if (
        parsed.scheme != "https"
        or parsed.hostname is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        return [f"{path} must be an HTTPS origin"]
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


def _validate_capability_binding(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != CAPABILITY_BINDING_FIELDS:
        errors.append(f"{path} fields must exactly match the v1 contract")
    protocol = value.get("protocol")
    if protocol not in CAPABILITY_PROTOCOLS:
        errors.append(f"{path}.protocol is invalid")
    elif isinstance(protocol, str):
        for field, expected_value in CAPABILITY_PROTOCOL_BINDINGS[protocol].items():
            if value.get(field) != expected_value:
                errors.append(f"{path}.{field} is invalid for {protocol}")
    expected = {
        "implementation_pin": "exact-version-or-immutable-revision",
        "identity": "stable-origin-bound-capability-id",
        "input_contract": "versioned-json-schema-and-runtime-validation-required",
        "output_contract": "versioned-json-schema-and-runtime-validation-required",
        "compatibility": "breaking-change-requires-new-capability-major",
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            errors.append(f"{path}.{field} is invalid")
    if value.get("classes") != CAPABILITY_CLASSES:
        errors.append(f"{path}.classes must preserve read-only/state-changing order")
    return errors


def _validate_commerce_binding(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    if set(value) != COMMERCE_BINDING_FIELDS:
        errors.append(f"{path} fields must exactly match the v1 contract")
    role = value.get("role")
    if role not in COMMERCE_ROLES:
        errors.append(f"{path}.role is invalid")
    elif isinstance(role, str) and value.get("identity_source") not in (
        COMMERCE_ROLE_IDENTITY_SOURCES[role]
    ):
        errors.append(f"{path}.identity_source is invalid for {role}")
    if value.get("executable_authority") != "none":
        errors.append(f"{path}.executable_authority must be none")
    if (
        value.get("transaction_contract")
        != "store-owned-versioned-contract-required-for-actions"
    ):
        errors.append(f"{path}.transaction_contract is invalid")
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
    accepted_fields = {
        frozenset(MECHANISM_BASE_FIELDS),
        frozenset(MECHANISM_FIELDS),
        frozenset(MECHANISM_FIELDS | {CAPABILITY_BINDING_FIELD}),
        frozenset(MECHANISM_FIELDS | {COMMERCE_BINDING_FIELD}),
    }
    if frozenset(fields) not in accepted_fields:
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
        if concern == "capability":
            if CAPABILITY_BINDING_FIELD not in fields:
                errors.append(
                    f"{path}.capability is required for a capability mechanism"
                )
            else:
                errors.extend(
                    _validate_capability_binding(
                        value.get("capability"),
                        f"{path}.capability",
                    )
                )
        elif CAPABILITY_BINDING_FIELD in fields:
            errors.append(
                f"{path}.capability is allowed only for a capability mechanism"
            )
        if concern == "commerce":
            if COMMERCE_BINDING_FIELD not in fields:
                errors.append(f"{path}.commerce is required for a commerce mechanism")
            else:
                errors.extend(
                    _validate_commerce_binding(
                        value.get("commerce"),
                        f"{path}.commerce",
                    )
                )
        elif COMMERCE_BINDING_FIELD in fields:
            errors.append(f"{path}.commerce is allowed only for a commerce mechanism")
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


def _validate_capability_policy(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    policy_without_references = {
        key: item for key, item in value.items() if key != "authoritative_references"
    }
    if policy_without_references != CAPABILITY_POLICY:
        errors.append(f"{path} must preserve the fail-closed capability contract")
    reference_errors, _ = _validate_references(
        value.get("authoritative_references"),
        f"{path}.authoritative_references",
    )
    errors.extend(reference_errors)
    return errors


def _validate_commerce_policy(value: Any, path: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    policy_without_references = {
        key: item for key, item in value.items() if key != "authoritative_references"
    }
    if policy_without_references != COMMERCE_POLICY:
        errors.append(f"{path} must preserve truthful non-executable commerce policy")
    reference_errors, _ = _validate_references(
        value.get("authoritative_references"),
        f"{path}.authoritative_references",
    )
    errors.extend(reference_errors)
    return errors


def _validate_integration_policy(value: Any, path: str) -> list[str]:
    if value != INTEGRATION_POLICY:
        return [f"{path} must preserve independent concerns and authority boundaries"]
    return []


def _validate_conformance_policy(value: Any, path: str) -> list[str]:
    if value != CONFORMANCE_POLICY:
        return [f"{path} must preserve deterministic conformance semantics"]
    return []


def _validate_reference_review(
    value: Any,
    path: str,
    mechanism_ids: list[str],
) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    fields = {"reviewed_on", "scope", "mechanism_ids", "checks", "outcome"}
    if set(value) != fields:
        errors.append(f"{path} fields must exactly match the v1 contract")
    errors.extend(_iso_date(value.get("reviewed_on"), f"{path}.reviewed_on"))
    if value.get("scope") != "all-registered-mechanisms-and-cross-cutting-policies":
        errors.append(f"{path}.scope is invalid")
    if value.get("mechanism_ids") != mechanism_ids:
        errors.append(f"{path}.mechanism_ids must exactly cover the catalog")
    if value.get("checks") != REFERENCE_REVIEW_CHECKS:
        errors.append(f"{path}.checks must preserve the maturity review contract")
    if value.get("outcome") != "coverage-complete-maturity-classifications-retained":
        errors.append(f"{path}.outcome is invalid")
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
        "site_conformance_evidence": CONFORMANCE_SCHEMA,
        "required_primary_references": 1,
        "required_registration_evidence": 1,
        "concern_specific_bindings": ["capability", "commerce"],
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
    errors.extend(
        _validate_capability_policy(
            profile.get("capability_policy"),
            "profile.capability_policy",
        )
    )
    errors.extend(
        _validate_commerce_policy(
            profile.get("commerce_policy"),
            "profile.commerce_policy",
        )
    )
    errors.extend(
        _validate_integration_policy(
            profile.get("integration_policy"),
            "profile.integration_policy",
        )
    )
    errors.extend(
        _validate_conformance_policy(
            profile.get("conformance_policy"),
            "profile.conformance_policy",
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
                expected_fields = set(MECHANISM_FIELDS)
                if mechanism.get("concern") == "capability":
                    expected_fields.add(CAPABILITY_BINDING_FIELD)
                if mechanism.get("concern") == "commerce":
                    expected_fields.add(COMMERCE_BINDING_FIELD)
                if set(mechanism) != expected_fields:
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
        if len(mechanism_ids) != len(set(mechanism_ids)):
            errors.append("profile.mechanisms must use unique ids")
        if mechanism_ids != sorted(mechanism_ids):
            errors.append("profile.mechanisms must use stable id order")
        if mechanism_ids != SCOPED_MECHANISM_IDS:
            errors.append(
                "profile.mechanisms must exactly match the integrated catalog"
            )

    reference_mechanism_ids = (
        mechanism_ids if isinstance(mechanisms, list) else []
    )
    errors.extend(
        _validate_reference_review(
            profile.get("reference_review"),
            "profile.reference_review",
            reference_mechanism_ids,
        )
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
        "consumer_resolution",
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
        if compatibility.get("consumer_resolution") != CONSUMER_RESOLUTION_POLICY:
            errors.append("profile.compatibility.consumer_resolution is invalid")
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


def resolve_requirement(
    mechanism: Mapping[str, Any],
    site_class: str,
    applicability: str,
    requirement_condition: str | None,
) -> tuple[str | None, str]:
    """Resolve one mechanism without conflating strength and maturity."""

    requirements = mechanism.get("requirements")
    if not isinstance(requirements, dict):
        return None, "unresolved"
    rule = requirements.get("default")
    overrides = requirements.get("site_class_overrides")
    if isinstance(overrides, list):
        for override in overrides:
            if isinstance(override, dict) and override.get("site_class") == site_class:
                rule = override
                break
    if not isinstance(rule, dict):
        return None, "unresolved"
    declared = rule.get("strength")
    if not isinstance(declared, str) or declared not in REQUIREMENT_STRENGTHS:
        return None, "unresolved"
    if applicability == "unknown":
        return declared, "unresolved"
    if applicability == "not-applicable":
        return declared, "inapplicable"
    if applicability != "applicable":
        return declared, "unresolved"
    if declared != "conditional":
        return declared, declared
    if requirement_condition == "met":
        return declared, "required"
    if requirement_condition == "not-met":
        return declared, "inapplicable"
    return declared, "unresolved"


def _validate_profile_pin(
    value: Any,
    profile: Mapping[str, Any],
    path: str,
) -> list[str]:
    if not isinstance(value, dict):
        return [f"{path} must be an object"]
    errors: list[str] = []
    fields = {"schema", "version", "status", "repository", "path", "pin"}
    if set(value) != fields:
        errors.append(f"{path} fields must exactly match the v1 contract")
    if value.get("schema") != profile.get("schema"):
        errors.append(f"{path}.schema must match the loaded profile")
    if value.get("version") != profile.get("version"):
        errors.append(f"{path}.version must match the loaded profile")
    if value.get("status") != profile.get("status"):
        errors.append(f"{path}.status must match the loaded profile")
    if value.get("repository") != "egohygiene/hygiene":
        errors.append(f"{path}.repository is invalid")
    if value.get("path") != "catalog/agent-ready-web-profile.json":
        errors.append(f"{path}.path is invalid")
    pin = value.get("pin")
    if not isinstance(pin, dict):
        errors.append(f"{path}.pin must be an object")
        return errors
    pin_fields = {"kind", "value", "resolved_revision", "sha256"}
    if set(pin) != pin_fields:
        errors.append(f"{path}.pin fields must exactly match the v1 contract")
    kind = pin.get("kind")
    if kind not in {"immutable-revision", "released-version"}:
        errors.append(f"{path}.pin.kind is invalid")
    revision = pin.get("resolved_revision")
    if not isinstance(revision, str) or SHA_RE.fullmatch(revision) is None:
        errors.append(f"{path}.pin.resolved_revision must be a full commit SHA")
    digest = pin.get("sha256")
    if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
        errors.append(f"{path}.pin.sha256 must be a SHA-256 digest")
    elif digest != profile_digest(profile):
        errors.append(f"{path}.pin.sha256 must match the loaded canonical profile")
    pin_value = pin.get("value")
    if kind == "immutable-revision" and pin_value != revision:
        errors.append(f"{path}.pin.value must equal the resolved immutable revision")
    if kind == "released-version":
        if profile.get("status") == "proposed":
            errors.append(
                f"{path}.pin.kind released-version requires a non-proposed profile"
            )
        if pin_value != profile.get("version"):
            errors.append(f"{path}.pin.value must equal the exact profile version")
        if not isinstance(pin_value, str) or SEMVER_RE.fullmatch(pin_value) is None:
            errors.append(f"{path}.pin.value must be an exact semantic version")
    return errors


def _validate_site_evidence_registry(
    value: Any,
    subject_revision: str | None,
    assessed_at: str | None,
    path: str,
) -> tuple[list[str], dict[str, Mapping[str, Any]]]:
    errors: list[str] = []
    evidence_by_id: dict[str, Mapping[str, Any]] = {}
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty array"], evidence_by_id
    fields = {
        "id",
        "kind",
        "location",
        "observed_at",
        "subject_revision",
        "description",
        "sha256",
    }
    ids: list[str] = []
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
            evidence_by_id[evidence_id] = evidence
        if evidence.get("kind") not in EVIDENCE_KINDS_SITE:
            errors.append(f"{evidence_path}.kind is invalid")
        errors.extend(_location(evidence.get("location"), f"{evidence_path}.location"))
        observed_at = evidence.get("observed_at")
        errors.extend(_iso_datetime(observed_at, f"{evidence_path}.observed_at"))
        if isinstance(observed_at, str) and isinstance(assessed_at, str):
            try:
                observed_time = datetime.fromisoformat(
                    observed_at.replace("Z", "+00:00")
                )
                assessed_time = datetime.fromisoformat(
                    assessed_at.replace("Z", "+00:00")
                )
                if observed_time > assessed_time:
                    errors.append(
                        f"{evidence_path}.observed_at must not follow the assessment"
                    )
            except ValueError:
                pass
        revision = evidence.get("subject_revision")
        if revision != subject_revision:
            errors.append(
                f"{evidence_path}.subject_revision must match the assessed subject"
            )
        errors.extend(_text(evidence.get("description"), f"{evidence_path}.description"))
        digest = evidence.get("sha256")
        if digest is not None and (
            not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None
        ):
            errors.append(f"{evidence_path}.sha256 must be null or a SHA-256 digest")
    if len(ids) != len(set(ids)):
        errors.append(f"{path} must use unique ids")
    if ids != sorted(ids):
        errors.append(f"{path} must use stable id order")
    return errors, evidence_by_id


def _validate_evidence_ids(
    value: Any,
    evidence_by_id: Mapping[str, Mapping[str, Any]],
    path: str,
    *,
    allow_empty: bool,
) -> list[str]:
    errors = _unique_strings(value, path, allow_empty=allow_empty)
    if not isinstance(value, list):
        return errors
    ids = [item for item in value if isinstance(item, str)]
    if ids != sorted(ids):
        errors.append(f"{path} must use stable id order")
    unknown = sorted(set(ids) - set(evidence_by_id))
    if unknown:
        errors.append(f"{path} contains unknown evidence ids: {', '.join(unknown)}")
    return errors


def _validate_exemption(
    value: Any,
    evidence_by_id: Mapping[str, Mapping[str, Any]],
    assessed_at: str | None,
    path: str,
) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict):
        return [f"{path} must be null or an object"]
    errors: list[str] = []
    fields = {
        "id",
        "scope",
        "owner",
        "reason",
        "approved_by",
        "approval_evidence_id",
        "approved_on",
        "expires_on",
    }
    if set(value) != fields:
        errors.append(f"{path} fields must exactly match the v1 contract")
    errors.extend(_identifier(value.get("id"), f"{path}.id"))
    if value.get("scope") != "required-absence":
        errors.append(f"{path}.scope is not exemptable")
    for field in ("owner", "reason", "approved_by"):
        errors.extend(_text(value.get(field), f"{path}.{field}"))
    approval_id = value.get("approval_evidence_id")
    errors.extend(_identifier(approval_id, f"{path}.approval_evidence_id"))
    approval_evidence = evidence_by_id.get(approval_id)
    if approval_evidence is None or approval_evidence.get("kind") != "approval":
        errors.append(f"{path}.approval_evidence_id must reference approval evidence")
    errors.extend(_iso_date(value.get("approved_on"), f"{path}.approved_on"))
    errors.extend(_iso_date(value.get("expires_on"), f"{path}.expires_on"))
    if isinstance(assessed_at, str):
        try:
            assessed_date = datetime.fromisoformat(
                assessed_at.replace("Z", "+00:00")
            ).date()
            approved_date = date.fromisoformat(value.get("approved_on"))
            expiry_date = date.fromisoformat(value.get("expires_on"))
            if approved_date > assessed_date:
                errors.append(f"{path}.approved_on must not follow the assessment")
            if expiry_date <= assessed_date:
                errors.append(f"{path}.expires_on must be after the assessment")
            if expiry_date <= approved_date:
                errors.append(f"{path}.expires_on must be after approval")
        except (TypeError, ValueError):
            pass
    return errors


def _diagnostic(
    code: str,
    severity: str,
    mechanism_id: str,
    path: str,
    message: str,
) -> dict[str, str]:
    return {
        "code": code,
        "severity": severity,
        "mechanism_id": mechanism_id,
        "path": path,
        "message": message,
    }


def derive_conformance(
    conformance: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Derive the summary and stable diagnostics for one site assessment."""

    subject = conformance.get("subject")
    site_class = subject.get("site_class") if isinstance(subject, dict) else None
    raw_assessments = conformance.get("mechanisms")
    assessments = raw_assessments if isinstance(raw_assessments, list) else []
    assessment_by_id = {
        item.get("id"): item
        for item in assessments
        if isinstance(item, dict)
    }
    diagnostics: list[dict[str, str]] = []
    exemptions = 0
    applicable = 0
    inapplicable = 0
    experimental_present = 0
    mechanism_order: dict[str, int] = {}
    for index, mechanism in enumerate(profile.get("mechanisms", [])):
        if not isinstance(mechanism, dict) or not isinstance(mechanism.get("id"), str):
            continue
        mechanism_id = mechanism["id"]
        mechanism_order[mechanism_id] = index
        assessment = assessment_by_id.get(mechanism_id)
        if not isinstance(assessment, dict):
            continue
        path = f"mechanisms[{index}]"
        applicability = assessment.get("applicability")
        _, resolved = resolve_requirement(
            mechanism,
            site_class if isinstance(site_class, str) else "",
            applicability if isinstance(applicability, str) else "unknown",
            assessment.get("requirement_condition"),
        )
        presence = assessment.get("presence")
        validation = assessment.get("validation")
        exemption = assessment.get("exemption")
        maturity = mechanism.get("maturity")
        is_experimental = (
            isinstance(maturity, dict) and maturity.get("level") == "experimental"
        )
        if resolved == "inapplicable":
            inapplicable += 1
        elif resolved != "unresolved":
            applicable += 1
        if applicability == "unknown":
            diagnostics.append(
                _diagnostic(
                    "ARW-APP-001",
                    "error",
                    mechanism_id,
                    f"{path}.applicability",
                    "Mechanism applicability is unknown and cannot be resolved.",
                )
            )
        elif resolved == "unresolved":
            diagnostics.append(
                _diagnostic(
                    "ARW-CND-001",
                    "error",
                    mechanism_id,
                    f"{path}.requirement_condition",
                    "Conditional requirement state is unknown and cannot be resolved.",
                )
            )
        if resolved == "inapplicable" and presence == "present":
            diagnostics.append(
                _diagnostic(
                    "ARW-APP-002",
                    "error",
                    mechanism_id,
                    f"{path}.presence",
                    "An inapplicable mechanism must be absent.",
                )
            )
        if resolved == "required" and presence == "absent":
            if exemption is None:
                diagnostics.append(
                    _diagnostic(
                        "ARW-REQ-001",
                        "error",
                        mechanism_id,
                        f"{path}.presence",
                        "Applicable required mechanism is absent.",
                    )
                )
            else:
                exemptions += 1
                diagnostics.append(
                    _diagnostic(
                        "ARW-EXM-001",
                        "information",
                        mechanism_id,
                        f"{path}.exemption",
                        "A narrow approved exemption is active; this is not passing.",
                    )
                )
        if resolved == "recommended" and presence == "absent":
            diagnostics.append(
                _diagnostic(
                    "ARW-REC-001",
                    "advisory",
                    mechanism_id,
                    f"{path}.presence",
                    "Applicable recommended mechanism is absent.",
                )
            )
        if resolved == "prohibited" and presence == "present":
            diagnostics.append(
                _diagnostic(
                    "ARW-PRO-001",
                    "error",
                    mechanism_id,
                    f"{path}.presence",
                    "Prohibited mechanism is present and cannot be exempted.",
                )
            )
        if presence == "present":
            evidence_ids = assessment.get("evidence_ids")
            if not isinstance(evidence_ids, list) or not evidence_ids:
                diagnostics.append(
                    _diagnostic(
                        "ARW-EVD-001",
                        "error",
                        mechanism_id,
                        f"{path}.evidence_ids",
                        "Present mechanism requires current evidence.",
                    )
                )
            if validation != "passed":
                diagnostics.append(
                    _diagnostic(
                        "ARW-VAL-001",
                        "error",
                        mechanism_id,
                        f"{path}.validation",
                        "Present mechanism did not pass its complete validation rules.",
                    )
                )
            if is_experimental:
                experimental_present += 1
                diagnostics.append(
                    _diagnostic(
                        "ARW-EXP-001",
                        "information",
                        mechanism_id,
                        path,
                        "Present experimental mechanism is reviewed only and grants no adoption or authority.",
                    )
                )
    severity_order = {value: index for index, value in enumerate(DIAGNOSTIC_SEVERITIES)}
    diagnostics.sort(
        key=lambda item: (
            mechanism_order.get(item["mechanism_id"], len(mechanism_order)),
            severity_order.get(item["severity"], len(severity_order)),
            item["code"],
            item["path"],
        )
    )
    errors = sum(item["severity"] == "error" for item in diagnostics)
    advisories = sum(item["severity"] == "advisory" for item in diagnostics)
    informationals = sum(
        item["severity"] == "information" for item in diagnostics
    )
    if errors:
        level = "nonconformant"
    elif exemptions:
        level = "exempt"
    elif advisories:
        level = "baseline"
    else:
        level = "recommended"
    return (
        {
            "level": level,
            "errors": errors,
            "advisories": advisories,
            "informationals": informationals,
            "exemptions": exemptions,
            "applicable": applicable,
            "inapplicable": inapplicable,
            "experimental_present": experimental_present,
            "claim": CONFORMANCE_CLAIM,
        },
        diagnostics,
    )


def validate_conformance(
    conformance: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> list[str]:
    """Validate one evidence snapshot against the exact loaded profile pin."""

    errors: list[str] = []
    fields = {
        "schema",
        "synthetic",
        "profile",
        "subject",
        "assessment",
        "authority_assertions",
        "evidence",
        "mechanisms",
        "summary",
        "diagnostics",
    }
    if set(conformance) != fields:
        errors.append("conformance fields must exactly match the v1 contract")
    if conformance.get("schema") != CONFORMANCE_SCHEMA:
        errors.append(f"conformance.schema must be {CONFORMANCE_SCHEMA}")
    if not isinstance(conformance.get("synthetic"), bool):
        errors.append("conformance.synthetic must be a boolean")
    errors.extend(_validate_profile_pin(conformance.get("profile"), profile, "conformance.profile"))

    subject = conformance.get("subject")
    subject_revision: str | None = None
    if not isinstance(subject, dict):
        errors.append("conformance.subject must be an object")
        site_class = None
    else:
        subject_fields = {"id", "site_class", "origin", "represented_revision"}
        if set(subject) != subject_fields:
            errors.append("conformance.subject fields must exactly match the v1 contract")
        errors.extend(_identifier(subject.get("id"), "conformance.subject.id"))
        site_class = subject.get("site_class")
        if site_class not in SITE_CLASSES:
            errors.append("conformance.subject.site_class is invalid")
        errors.extend(
            _https_origin(subject.get("origin"), "conformance.subject.origin")
        )
        subject_revision = subject.get("represented_revision")
        if (
            not isinstance(subject_revision, str)
            or SHA_RE.fullmatch(subject_revision) is None
        ):
            errors.append(
                "conformance.subject.represented_revision must be a full commit SHA"
            )

    assessment = conformance.get("assessment")
    assessed_at: str | None = None
    if not isinstance(assessment, dict):
        errors.append("conformance.assessment must be an object")
    else:
        if set(assessment) != {"assessed_at", "assessor"}:
            errors.append(
                "conformance.assessment fields must exactly match the v1 contract"
            )
        assessed_at = assessment.get("assessed_at")
        errors.extend(_iso_datetime(assessed_at, "conformance.assessment.assessed_at"))
        assessor = assessment.get("assessor")
        if not isinstance(assessor, dict):
            errors.append("conformance.assessment.assessor must be an object")
        else:
            if set(assessor) != {"id", "version"}:
                errors.append(
                    "conformance.assessment.assessor fields must exactly match the v1 contract"
                )
            errors.extend(_identifier(assessor.get("id"), "conformance.assessment.assessor.id"))
            version = assessor.get("version")
            if not isinstance(version, str) or SEMVER_RE.fullmatch(version) is None:
                errors.append(
                    "conformance.assessment.assessor.version must be a semantic version"
                )

    if conformance.get("authority_assertions") != AUTHORITY_ASSERTIONS:
        errors.append(
            "conformance.authority_assertions must deny cross-layer authority inference"
        )

    evidence_errors, evidence_by_id = _validate_site_evidence_registry(
        conformance.get("evidence"),
        subject_revision,
        assessed_at,
        "conformance.evidence",
    )
    errors.extend(evidence_errors)

    mechanisms = conformance.get("mechanisms")
    raw_profile_mechanisms = profile.get("mechanisms")
    profile_mechanisms = (
        raw_profile_mechanisms
        if isinstance(raw_profile_mechanisms, list)
        else []
    )
    expected_ids = [
        mechanism.get("id")
        for mechanism in profile_mechanisms
        if isinstance(mechanism, dict)
    ]
    if not isinstance(mechanisms, list):
        errors.append("conformance.mechanisms must be an array")
    else:
        ids = [item.get("id") for item in mechanisms if isinstance(item, dict)]
        if ids != expected_ids:
            errors.append(
                "conformance.mechanisms must cover every mechanism exactly once in profile order"
            )
        assessment_fields = {
            "id",
            "applicability",
            "applicability_evidence_ids",
            "declared_strength",
            "requirement_condition",
            "resolved_strength",
            "presence",
            "validation",
            "evidence_ids",
            "exemption",
        }
        for index, item in enumerate(mechanisms):
            item_path = f"conformance.mechanisms[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{item_path} must be an object")
                continue
            if set(item) != assessment_fields:
                errors.append(f"{item_path} fields must exactly match the v1 contract")
            applicability = item.get("applicability")
            if applicability not in APPLICABILITY_STATES:
                errors.append(f"{item_path}.applicability is invalid")
            errors.extend(
                _validate_evidence_ids(
                    item.get("applicability_evidence_ids"),
                    evidence_by_id,
                    f"{item_path}.applicability_evidence_ids",
                    allow_empty=False,
                )
            )
            condition = item.get("requirement_condition")
            if condition is not None and condition not in CONDITIONAL_STATES:
                errors.append(f"{item_path}.requirement_condition is invalid")
            presence = item.get("presence")
            if presence not in PRESENCE_STATES:
                errors.append(f"{item_path}.presence is invalid")
            validation = item.get("validation")
            if validation not in MECHANISM_VALIDATION_STATES:
                errors.append(f"{item_path}.validation is invalid")
            if presence == "absent" and validation != "not-run":
                errors.append(f"{item_path}.validation must be not-run when absent")
            errors.extend(
                _validate_evidence_ids(
                    item.get("evidence_ids"),
                    evidence_by_id,
                    f"{item_path}.evidence_ids",
                    allow_empty=True,
                )
            )
            exemption = item.get("exemption")
            errors.extend(
                _validate_exemption(
                    exemption,
                    evidence_by_id,
                    assessed_at,
                    f"{item_path}.exemption",
                )
            )
            if index < len(profile_mechanisms) and isinstance(
                profile_mechanisms[index], dict
            ):
                declared, resolved = resolve_requirement(
                    profile_mechanisms[index],
                    site_class if isinstance(site_class, str) else "",
                    applicability if isinstance(applicability, str) else "unknown",
                    condition,
                )
                if item.get("declared_strength") != declared:
                    errors.append(
                        f"{item_path}.declared_strength must equal profile resolution"
                    )
                if item.get("resolved_strength") != resolved:
                    errors.append(
                        f"{item_path}.resolved_strength must equal profile resolution"
                    )
                if declared == "conditional" and condition is None:
                    errors.append(
                        f"{item_path}.requirement_condition is required for a conditional rule"
                    )
                if declared != "conditional" and condition is not None:
                    errors.append(
                        f"{item_path}.requirement_condition must be null unless the rule is conditional"
                    )
                if exemption is not None and not (
                    resolved == "required" and presence == "absent"
                ):
                    errors.append(
                        f"{item_path}.exemption is allowed only for a required absence"
                    )

    summary, diagnostics = derive_conformance(conformance, profile)
    if conformance.get("summary") != summary:
        errors.append("conformance.summary must equal the deterministic derived summary")
    provided_diagnostics = conformance.get("diagnostics")
    if not isinstance(provided_diagnostics, list):
        errors.append("conformance.diagnostics must be an array")
    else:
        diagnostic_fields = {"code", "severity", "mechanism_id", "path", "message"}
        for index, diagnostic in enumerate(provided_diagnostics):
            diagnostic_path = f"conformance.diagnostics[{index}]"
            if not isinstance(diagnostic, dict):
                errors.append(f"{diagnostic_path} must be an object")
                continue
            if set(diagnostic) != diagnostic_fields:
                errors.append(
                    f"{diagnostic_path} fields must exactly match the v1 contract"
                )
            code = diagnostic.get("code")
            if not isinstance(code, str) or re.fullmatch(r"ARW-[A-Z]+-[0-9]{3}", code) is None:
                errors.append(f"{diagnostic_path}.code is invalid")
            if diagnostic.get("severity") not in DIAGNOSTIC_SEVERITIES:
                errors.append(f"{diagnostic_path}.severity is invalid")
            if diagnostic.get("mechanism_id") not in expected_ids:
                errors.append(f"{diagnostic_path}.mechanism_id is invalid")
            for field in ("path", "message"):
                errors.extend(_text(diagnostic.get(field), f"{diagnostic_path}.{field}"))
        if provided_diagnostics != diagnostics:
            errors.append(
                "conformance.diagnostics must equal deterministic derived diagnostics"
            )
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


def validate_conformance_fixture(
    fixture: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> tuple[list[str], list[str]]:
    """Validate a synthetic whole-profile compatibility fixture."""

    envelope_errors: list[str] = []
    fields = {
        "schema",
        "name",
        "expected",
        "synthetic",
        "site_class",
        "conformance",
        "expected_errors",
    }
    if set(fixture) != fields:
        envelope_errors.append(
            "conformance fixture fields must exactly match the v1 contract"
        )
    if fixture.get("schema") != CONFORMANCE_FIXTURE_SCHEMA:
        envelope_errors.append(
            f"conformance fixture.schema must be {CONFORMANCE_FIXTURE_SCHEMA}"
        )
    envelope_errors.extend(
        _identifier(fixture.get("name"), "conformance fixture.name")
    )
    if fixture.get("expected") not in {"valid", "invalid"}:
        envelope_errors.append("conformance fixture.expected is invalid")
    if fixture.get("synthetic") is not True:
        envelope_errors.append("conformance fixture.synthetic must be true")
    site_class = fixture.get("site_class")
    if site_class not in SITE_CLASSES:
        envelope_errors.append("conformance fixture.site_class is invalid")
    expected_errors = fixture.get("expected_errors")
    envelope_errors.extend(
        _unique_strings(
            expected_errors,
            "conformance fixture.expected_errors",
            allow_empty=True,
        )
    )
    if fixture.get("expected") == "valid" and expected_errors != []:
        envelope_errors.append(
            "conformance fixture.expected_errors must be empty for a valid fixture"
        )
    if fixture.get("expected") == "invalid" and expected_errors == []:
        envelope_errors.append(
            "conformance fixture.expected_errors must identify invalid coverage"
        )
    conformance = fixture.get("conformance")
    if not isinstance(conformance, dict):
        return sorted(set(envelope_errors)), [
            "conformance fixture.conformance must be an object"
        ]
    if conformance.get("synthetic") is not True:
        envelope_errors.append(
            "conformance fixture.conformance.synthetic must be true"
        )
    subject = conformance.get("subject")
    if not isinstance(subject, dict) or subject.get("site_class") != site_class:
        envelope_errors.append(
            "conformance fixture.site_class must match conformance.subject.site_class"
        )
    return sorted(set(envelope_errors)), validate_conformance(conformance, profile)


def validate_fixture_directory(
    path: Path,
    profile: Mapping[str, Any],
) -> list[str]:
    """Validate all checked-in valid and invalid compatibility fixtures."""

    errors: list[str] = []
    fixture_paths = sorted(path.glob("*.json"))
    if not fixture_paths:
        return [f"no fixtures found in {path}"]
    mechanism_expected_kinds: set[str] = set()
    conformance_site_classes: set[str] = set()
    for fixture_path in fixture_paths:
        try:
            fixture = load_json(fixture_path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"{fixture_path}: load failed: {error}")
            continue
        schema = fixture.get("schema")
        if schema == FIXTURE_SCHEMA:
            envelope_errors, payload_errors = validate_fixture(fixture)
            fixture_kind = "mechanism"
        elif schema == CONFORMANCE_FIXTURE_SCHEMA:
            envelope_errors, payload_errors = validate_conformance_fixture(
                fixture,
                profile,
            )
            fixture_kind = "conformance"
            site_class = fixture.get("site_class")
            if fixture.get("expected") == "valid" and isinstance(site_class, str):
                conformance_site_classes.add(site_class)
        else:
            errors.append(f"{fixture_path}: fixture.schema is unrecognized")
            continue
        errors.extend(f"{fixture_path}: {error}" for error in envelope_errors)
        expected = fixture.get("expected")
        if fixture_kind == "mechanism" and isinstance(expected, str):
            mechanism_expected_kinds.add(expected)
        if expected == "valid" and payload_errors:
            errors.extend(
                f"{fixture_path}: unexpected: {error}" for error in payload_errors
            )
        if expected == "invalid":
            if not payload_errors:
                errors.append(
                    f"{fixture_path}: expected invalid payload was accepted"
                )
            expected_errors = fixture.get("expected_errors")
            listed_errors = expected_errors if isinstance(expected_errors, list) else []
            for expected_error in listed_errors:
                if expected_error not in payload_errors:
                    errors.append(
                        f"{fixture_path}: missing expected error: {expected_error}"
                    )
    if mechanism_expected_kinds != {"valid", "invalid"}:
        errors.append(
            "fixture directory must contain valid and invalid mechanism coverage"
        )
    missing_site_classes = sorted(set(SITE_CLASSES) - conformance_site_classes)
    if missing_site_classes:
        errors.append(
            "fixture directory lacks valid whole-profile coverage for: "
            + ", ".join(missing_site_classes)
        )
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
    conformance = subparsers.add_parser("validate-conformance")
    conformance.add_argument("--input", type=Path, required=True)
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
        elif arguments.command == "validate-conformance":
            errors = validate_conformance(load_json(arguments.input), profile)
        else:
            errors = validate_fixture_directory(arguments.fixtures, profile)
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
