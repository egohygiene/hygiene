#!/usr/bin/env python3
"""Validate Hygiene's repository-release policy and local baseline composition.

This checker validates Hygiene policy composition only. It deliberately does
not reimplement Aether's release-declaration schema, execute Task targets, or
publish a tag, package, image, site, or archive.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import sys
import types
from collections.abc import Mapping
from pathlib import Path
from typing import Any


POLICY_SCHEMA = "egohygiene.repository-release-policy/v1"
POLICY_VERSION = "1.0.0-alpha.1"
OWNER = "egohygiene/hygiene"
AETHER_SCHEMA = "egohygiene.repository-release/v1"
AETHER_SCHEMA_URL = "https://egohygiene.io/schemas/aether/repository-release/v1.json"
AETHER_REVISION = "8a2a3d08f3aa9da3847bd5277843506ab855192e"
REQUIREMENTS = {"required", "advisory", "not_applicable"}
ADOPTION_STATES = {"required", "advisory", "exempt", "not_applicable"}
REPOSITORY_PROFILES = [
    "cli-library",
    "container-image",
    "contract",
    "internal-only",
    "npm-package",
    "publication",
    "python-package",
    "static-site",
    "workspace",
]
LIFECYCLES = ["active", "incubating", "internal", "archived"]
VISIBILITIES = ["public", "internal", "private"]
SLOT_IDS = {
    "agents_profile_pointer",
    "aether_declaration",
    "changelog",
    "manual_workflow",
    "release_rollback_docs",
    "task_handoffs",
    "version_authority",
}
EXAMPLE_IDS = {
    "archived-repository",
    "container-image",
    "contract-repository",
    "legacy-advisory-migration",
    "private-repository",
    "publication",
    "static-site",
    "tool-library",
    "workspace",
}
POLICY_FIELDS = {
    "schema",
    "version",
    "status",
    "owner",
    "updated",
    "purpose",
    "aether_contract",
    "requirements",
    "adoption_states",
    "repository_profiles",
    "lifecycles",
    "visibilities",
    "slots",
    "profile_overrides",
    "lifecycle_overrides",
    "visibility_overrides",
    "migration",
    "examples",
    "ownership",
}
SLOT_FIELDS = {
    "id",
    "title",
    "default_requirement",
    "authority",
    "description",
    "checks",
}
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SLOT_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SAFE_RELATIVE_PATH_RE = re.compile(r"^[A-Za-z0-9.][A-Za-z0-9._/-]*$")


def _json_object(text: str, label: str) -> dict[str, Any]:
    def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{label} has duplicate JSON key {key!r}")
            result[key] = value
        return result
    value = json.loads(text, object_pairs_hook=unique_keys)
    if not isinstance(value, dict):
        raise ValueError(f"{label} must contain a JSON object")
    return value


def load_json(path: Path) -> dict[str, Any]:
    return _json_object(path.read_text(encoding="utf-8"), str(path))


class OwnerValidationUnavailable(ValueError):
    """Full selected owner/structural validation could not execute."""


def _runtime_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError as error:
        raise OwnerValidationUnavailable(f"validation runtime version unavailable: {name}") from error


OWNER_VALIDATOR = "library/organization/specs/release/validate.py"
OWNER_SCHEMA = "catalog/schemas/aether.repository-release.v1.schema.json"
OWNER_REQUIREMENTS = "requirements-dev.lock"


def verify_owner_source(source: Path, profile: Mapping[str, Any]) -> tuple[dict[str, bytes], dict[str, Any]]:
    lock = load_json(Path(__file__).with_name("release-owner.lock.json"))
    if (
        lock.get("schema") != "hygiene.aether-release-selection/v1"
        or lock.get("repository") != "egohygiene/aether"
        or lock.get("revision") != profile["aether_contract"]["revision"]
        or set(lock.get("files", {})) != {OWNER_VALIDATOR, OWNER_SCHEMA, OWNER_REQUIREMENTS}
    ):
        raise ValueError("release owner lock does not match the selected contract")
    payloads: dict[str, bytes] = {}
    for relative, digest in lock["files"].items():
        path = source / relative
        try:
            path.resolve(strict=True).relative_to(source.resolve(strict=True))
            content = path.read_bytes()
        except (OSError, ValueError, RuntimeError) as error:
            raise OwnerValidationUnavailable(f"selected owner source unavailable: {relative}; prepare the exact Aether pin and pass --aether-source") from error
        if hashlib.sha256(content).hexdigest() != digest:
            raise OwnerValidationUnavailable(f"selected owner bytes do not match the immutable lock: {relative}")
        payloads[relative] = content
    return payloads, {
        "repository": lock["repository"], "revision": lock["revision"],
        "source_verification": "sha256-of-selected-files", "files": lock["files"],
    }


def _owner_validation(repository: Path, source: Path, profile: Mapping[str, Any], declaration: dict[str, Any]) -> dict[str, Any]:
    payloads, evidence = verify_owner_source(source, profile)
    module = types.ModuleType("hygiene_pinned_aether_release")
    module.__file__ = str(source / OWNER_VALIDATOR)
    try:
        # Execute exactly the verified payload, without a second source read.
        exec(compile(payloads[OWNER_VALIDATOR], module.__file__, "exec"), module.__dict__)
        if module.Draft202012Validator is None:
            raise OwnerValidationUnavailable("full jsonschema validation is unavailable; the owner's weaker fallback cannot qualify this declaration")
        selected_schema = module._schema_path().resolve()
        if selected_schema != (source / OWNER_SCHEMA).resolve():
            raise OwnerValidationUnavailable("owner selected a schema outside the locked canonical path")
        result = module.validate_release_declaration(repository)
    except ImportError as error:
        raise OwnerValidationUnavailable("selected owner runtime dependencies are unavailable") from error
    except module.ReleaseContractError as error:
        raise ValueError(f"pinned Aether declaration validation failed: {error}") from error
    if result != declaration:
        raise ValueError("declaration changed during owner validation")
    verify_owner_source(source, profile)
    engine_version = _runtime_version("jsonschema")
    evidence.update({
        "entrypoint": "validate_release_declaration", "validator_path": OWNER_VALIDATOR,
        "engine": "jsonschema.Draft202012Validator",
        "engine_version": engine_version,
    })
    return evidence


def _yaml_mapping(text: str, label: str) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as error:
        raise OwnerValidationUnavailable("PyYAML is unavailable for structural workflow/Taskfile validation") from error

    class WorkflowLoader(yaml.SafeLoader):
        # YAML 1.1 interprets the GitHub Actions key `on` as a boolean.
        yaml_implicit_resolvers = {
            key: [(tag, rule) for tag, rule in rules if tag != "tag:yaml.org,2002:bool"]
            for key, rules in yaml.SafeLoader.yaml_implicit_resolvers.items()
        }
    WorkflowLoader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$", re.IGNORECASE), list("tTfF"))

    def unique_mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError(f"{label} requires string mapping keys")
            if key in result:
                raise ValueError(f"{label} has duplicate YAML key {key!r}")
            result[key] = loader.construct_object(value_node, deep=deep)
        return result
    WorkflowLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
    try:
        value = yaml.load(text, Loader=WorkflowLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"{label} is not supported valid YAML") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping")
    return value


def _manual_workflow(text: str) -> None:
    workflow = _yaml_mapping(text, "release workflow")
    events = workflow.get("on")
    if isinstance(events, str):
        names = [events]
    elif isinstance(events, list) and all(isinstance(item, str) for item in events):
        names = events
    elif isinstance(events, dict):
        names = list(events)
        config = events.get("workflow_dispatch")
        if config is not None and not isinstance(config, dict):
            raise ValueError("workflow_dispatch configuration must be null or a mapping")
    else:
        raise ValueError("release workflow requires an explicit workflow_dispatch trigger")
    if names != ["workflow_dispatch"]:
        raise ValueError("release workflow must expose only workflow_dispatch; automatic or ambiguous triggers are prohibited")


def _task_handoff_names(repository: Path, taskfile: Path) -> set[str]:
    visiting: set[Path] = set()

    def visit(path: Path, namespace: str = "") -> set[str]:
        if path in visiting:
            raise ValueError("Taskfile include cycle is unsupported")
        visiting.add(path)
        document = _yaml_mapping(path.read_text(encoding="utf-8"), "release Taskfile")
        tasks, includes = document.get("tasks", {}), document.get("includes", {})
        if not isinstance(tasks, dict) or not isinstance(includes, dict):
            raise ValueError("Taskfile tasks/includes must be mappings")
        qualified = lambda name: f"{namespace}:{name}" if namespace else name
        names = {qualified(name) for name in tasks}
        for alias, include in includes.items():
            if isinstance(include, str):
                value, flatten = include, False
            elif isinstance(include, dict):
                value, flatten = include.get("taskfile"), include.get("flatten", False)
                if not isinstance(flatten, bool):
                    raise ValueError("Taskfile include flatten must be boolean")
            else:
                raise ValueError("unsupported Taskfile include declaration")
            selected = _repository_path(repository, value.removeprefix("./") if isinstance(value, str) else value, "Taskfile include")
            if not selected.is_file():
                raise ValueError("declared Taskfile include is missing")
            child = visit(selected, namespace if flatten else qualified(alias))
            if names.intersection(child):
                raise ValueError("Taskfile handoff names collide")
            names.update(child)
        visiting.remove(path)
        return names
    return visit(taskfile)


def _non_empty_strings(value: Any, path: str) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{path} must be a non-empty array"]
    errors: list[str] = []
    if any(not isinstance(item, str) or not item for item in value):
        errors.append(f"{path} must contain non-empty strings")
    strings = [item for item in value if isinstance(item, str)]
    if len(strings) != len(set(strings)):
        errors.append(f"{path} must not contain duplicate values")
    return errors


def _is_safe_relative_path(value: Any) -> bool:
    return (
        isinstance(value, str)
        and SAFE_RELATIVE_PATH_RE.fullmatch(value) is not None
        and ".." not in Path(value).parts
    )


def _validate_overrides(
    profile: Mapping[str, Any],
    field: str,
    expected_keys: list[str],
    slot_ids: set[str],
) -> list[str]:
    value = profile.get(field)
    if not isinstance(value, dict):
        return [f"profile.{field} must be an object"]
    errors: list[str] = []
    if set(value) != set(expected_keys):
        errors.append(f"profile.{field} keys must match its declared dimension")
    for variant, changes in value.items():
        if not isinstance(changes, dict):
            errors.append(f"profile.{field}.{variant} must be an object")
            continue
        for slot_id, requirement in changes.items():
            if slot_id not in slot_ids:
                errors.append(f"profile.{field}.{variant} references unknown slot {slot_id}")
            if requirement not in REQUIREMENTS:
                errors.append(f"profile.{field}.{variant}.{slot_id} has invalid requirement")
    return errors


def validate_profile(profile: Mapping[str, Any]) -> list[str]:
    """Return deterministic semantic errors for the canonical policy profile."""

    errors: list[str] = []
    if set(profile) != POLICY_FIELDS:
        errors.append("profile fields must exactly match the v1 contract")
    if profile.get("schema") != POLICY_SCHEMA:
        errors.append(f"profile.schema must be {POLICY_SCHEMA}")
    if profile.get("version") != POLICY_VERSION:
        errors.append(f"profile.version must be {POLICY_VERSION}")
    if profile.get("status") not in {"proposed", "active", "deprecated", "superseded"}:
        errors.append("profile.status is invalid")
    if profile.get("owner") != OWNER:
        errors.append(f"profile.owner must be {OWNER}")
    if not isinstance(profile.get("updated"), str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}", profile["updated"]
    ):
        errors.append("profile.updated must be an ISO date")
    if not isinstance(profile.get("purpose"), str) or not profile["purpose"]:
        errors.append("profile.purpose must be a non-empty string")

    aether = profile.get("aether_contract")
    expected_aether_fields = {
        "id",
        "version",
        "repository",
        "revision",
        "specification",
        "schema_url",
        "authoring_skill",
    }
    if not isinstance(aether, dict) or set(aether) != expected_aether_fields:
        errors.append("profile.aether_contract fields must exactly match the v1 contract")
    else:
        if aether.get("id") != AETHER_SCHEMA:
            errors.append(f"profile.aether_contract.id must be {AETHER_SCHEMA}")
        if aether.get("version") != "1.0.0":
            errors.append("profile.aether_contract.version must pin Aether 1.0.0")
        if aether.get("repository") != "egohygiene/aether":
            errors.append("profile.aether_contract.repository must be egohygiene/aether")
        if aether.get("revision") != AETHER_REVISION:
            errors.append("profile.aether_contract.revision must pin the Aether #61 merge commit")
        if not _is_safe_relative_path(aether.get("specification")):
            errors.append("profile.aether_contract.specification must be a safe repository-relative path")
        if aether.get("schema_url") != AETHER_SCHEMA_URL:
            errors.append("profile.aether_contract.schema_url must identify Aether's v1 schema")
        skill = aether.get("authoring_skill")
        if not isinstance(skill, dict) or set(skill) != {"id", "path", "url"}:
            errors.append("profile.aether_contract.authoring_skill fields are invalid")
        else:
            if skill.get("id") != "prepare-repository-release":
                errors.append("profile.aether_contract.authoring_skill.id is invalid")
            if not _is_safe_relative_path(skill.get("path")):
                errors.append("profile.aether_contract.authoring_skill.path is invalid")
            if not isinstance(skill.get("url"), str) or AETHER_REVISION not in skill["url"]:
                errors.append("profile.aether_contract.authoring_skill.url must use the pinned revision")

    if profile.get("requirements") != ["required", "advisory", "not_applicable"]:
        errors.append("profile.requirements must use canonical order")
    if profile.get("adoption_states") != [
        "required",
        "advisory",
        "exempt",
        "not_applicable",
    ]:
        errors.append("profile.adoption_states must use canonical order")
    if profile.get("repository_profiles") != REPOSITORY_PROFILES:
        errors.append("profile.repository_profiles must use Aether's canonical stable order")
    if profile.get("lifecycles") != LIFECYCLES:
        errors.append("profile.lifecycles must use Aether's canonical order")
    if profile.get("visibilities") != VISIBILITIES:
        errors.append("profile.visibilities must use canonical order")

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
        if set(slot) != SLOT_FIELDS:
            errors.append(f"{path} fields must exactly match the v1 contract")
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or SLOT_RE.fullmatch(slot_id) is None:
            errors.append(f"{path}.id is invalid")
        else:
            slot_ids.append(slot_id)
        for field in ("title", "description", "authority"):
            if not isinstance(slot.get(field), str) or not slot[field]:
                errors.append(f"{path}.{field} must be a non-empty string")
        if slot.get("default_requirement") not in REQUIREMENTS:
            errors.append(f"{path}.default_requirement is invalid")
        errors.extend(_non_empty_strings(slot.get("checks"), f"{path}.checks"))
    if len(slot_ids) != len(set(slot_ids)):
        errors.append("profile.slots must use unique ids")
    if set(slot_ids) != SLOT_IDS:
        errors.append("profile.slots must declare every canonical release slot")

    errors.extend(_validate_overrides(profile, "profile_overrides", REPOSITORY_PROFILES, set(slot_ids)))
    errors.extend(_validate_overrides(profile, "lifecycle_overrides", LIFECYCLES, set(slot_ids)))
    errors.extend(_validate_overrides(profile, "visibility_overrides", VISIBILITIES, set(slot_ids)))

    migration = profile.get("migration")
    expected_migration_fields = {
        "new_repositories",
        "existing_active_repositories",
        "incubating_repositories",
        "legacy_history",
        "exceptions",
        "repository_facts",
    }
    if not isinstance(migration, dict) or set(migration) != expected_migration_fields:
        errors.append("profile.migration fields must exactly match the v1 contract")
    else:
        if migration.get("new_repositories") != "required":
            errors.append("profile.migration.new_repositories must be required")
        if migration.get("existing_active_repositories") != "required":
            errors.append("profile.migration.existing_active_repositories must be required")
        if migration.get("incubating_repositories") != "advisory":
            errors.append("profile.migration.incubating_repositories must be advisory")
        if migration.get("legacy_history") != {
            "preserve_existing_tags": True,
            "preserve_existing_changelog": True,
            "invent_history_forbidden": True,
            "tag_rewrite_forbidden": True,
        }:
            errors.append("profile.migration.legacy_history must preserve facts and immutable history")
        exceptions = migration.get("exceptions")
        if not isinstance(exceptions, dict) or set(exceptions) != {
            "repository_owned",
            "approval_required",
            "expiry_required",
            "required_fields",
        }:
            errors.append("profile.migration.exceptions fields are invalid")
        elif (
            exceptions.get("repository_owned") is not True
            or exceptions.get("approval_required") is not True
            or exceptions.get("expiry_required") is not True
            or exceptions.get("required_fields")
            != ["scope", "reason", "legacy_evidence", "owner", "approval", "expires", "exit_criteria"]
        ):
            errors.append("profile.migration.exceptions must be explicit, reviewed, and expiring")
        facts = migration.get("repository_facts")
        if not isinstance(facts, dict) or facts.get("declaration_path") != ".egohygiene/release.json":
            errors.append("profile.migration.repository_facts must name the local declaration")
        elif facts.get("external_registry_required") is not False or not isinstance(
            facts.get("one_source_of_truth"), str
        ):
            errors.append("profile.migration.repository_facts must preserve local truth without a registry")

    examples = profile.get("examples")
    if not isinstance(examples, list) or not examples:
        errors.append("profile.examples must be a non-empty array")
        examples = []
    example_ids: list[str] = []
    for index, example in enumerate(examples):
        path = f"profile.examples[{index}]"
        if not isinstance(example, dict):
            errors.append(f"{path} must be an object")
            continue
        if set(example) != {
            "id",
            "title",
            "repository_profile",
            "lifecycle",
            "visibility",
            "adoption_state",
            "notes",
        }:
            errors.append(f"{path} fields must exactly match the v1 contract")
        example_id = example.get("id")
        if not isinstance(example_id, str):
            errors.append(f"{path}.id is invalid")
        else:
            example_ids.append(example_id)
        if example.get("repository_profile") not in REPOSITORY_PROFILES:
            errors.append(f"{path}.repository_profile is invalid")
        if example.get("lifecycle") not in LIFECYCLES:
            errors.append(f"{path}.lifecycle is invalid")
        if example.get("visibility") not in VISIBILITIES:
            errors.append(f"{path}.visibility is invalid")
        if example.get("adoption_state") not in ADOPTION_STATES:
            errors.append(f"{path}.adoption_state is invalid")
        for field in ("title", "notes"):
            if not isinstance(example.get(field), str) or not example[field]:
                errors.append(f"{path}.{field} must be a non-empty string")
    if len(example_ids) != len(set(example_ids)):
        errors.append("profile.examples must use unique ids")
    if set(example_ids) != EXAMPLE_IDS:
        errors.append("profile.examples must cover every required repository class and legacy migration")

    ownership = profile.get("ownership")
    if not isinstance(ownership, dict) or set(ownership) != {
        "aether",
        "hygiene",
        "relay",
        "egolint",
        "pace",
        "repository",
    }:
        errors.append("profile.ownership must declare every bounded owner")
    elif any(not isinstance(value, str) or not value for value in ownership.values()):
        errors.append("profile.ownership values must be non-empty strings")
    return sorted(set(errors))


def resolve_requirements(
    profile: Mapping[str, Any],
    repository_profile: str,
    lifecycle: str,
    visibility: str,
    adoption_state: str,
) -> dict[str, Any]:
    """Resolve one baseline with fixed applicability precedence."""

    if validate_profile(profile):
        raise ValueError("cannot resolve an invalid repository release policy")
    if repository_profile not in REPOSITORY_PROFILES:
        raise ValueError(f"unknown repository profile: {repository_profile}")
    if lifecycle not in LIFECYCLES:
        raise ValueError(f"unknown lifecycle: {lifecycle}")
    if visibility not in VISIBILITIES:
        raise ValueError(f"unknown visibility: {visibility}")
    if adoption_state not in ADOPTION_STATES:
        raise ValueError(f"unknown adoption state: {adoption_state}")
    resolved = {
        slot["id"]: slot["default_requirement"] for slot in profile["slots"]
    }
    for field, variant in (
        ("profile_overrides", repository_profile),
        ("visibility_overrides", visibility),
        ("lifecycle_overrides", lifecycle),
    ):
        resolved.update(profile[field][variant])
    if adoption_state == "advisory":
        resolved = {
            slot_id: "advisory" if requirement == "required" else requirement
            for slot_id, requirement in resolved.items()
        }
    elif adoption_state == "not_applicable":
        resolved = {slot_id: "not_applicable" for slot_id in resolved}
    return {"adoption_state": adoption_state, "requirements": dict(sorted(resolved.items()))}


def _repository_path(repository: Path, value: Any, label: str) -> Path:
    if not _is_safe_relative_path(value):
        raise ValueError(f"{label} is not a safe repository-relative path: {value!r}")
    candidate = (repository / str(value)).resolve()
    try:
        candidate.relative_to(repository.resolve())
    except ValueError as error:
        raise ValueError(f"{label} escapes the repository: {value!r}") from error
    return candidate


def validate_declaration_with_evidence(repository: Path, profile: Mapping[str, Any], *, aether_source: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate one repository's baseline composition around its Aether declaration."""

    policy_errors = validate_profile(profile)
    if policy_errors:
        raise ValueError("invalid policy: " + "; ".join(policy_errors))
    repository = repository.resolve()
    declaration_path = repository / ".egohygiene" / "release.json"
    declaration_bytes = declaration_path.read_bytes()
    declaration = _json_object(declaration_bytes.decode("utf-8"), "release declaration")
    source = (aether_source or repository / ".cache/release/aether").resolve()
    owner_evidence = _owner_validation(repository, source, profile, declaration)
    if declaration.get("$schema") != profile["aether_contract"]["schema_url"]:
        raise ValueError("release declaration must identify Aether's pinned v1 schema URL")
    if declaration.get("schema_version") != AETHER_SCHEMA:
        raise ValueError(f"release declaration must use {AETHER_SCHEMA}")
    subject = declaration.get("repository")
    if not isinstance(subject, dict):
        raise ValueError("release declaration.repository must be an object")
    repository_profile = subject.get("release_profile")
    lifecycle = subject.get("lifecycle")
    if repository_profile not in REPOSITORY_PROFILES:
        raise ValueError("release declaration repository.release_profile is not covered by the baseline")
    if lifecycle not in LIFECYCLES:
        raise ValueError("release declaration repository.lifecycle is not covered by the baseline")

    changelog = declaration.get("changelog")
    if not isinstance(changelog, dict) or changelog.get("path") != "CHANGELOG.md":
        raise ValueError("release declaration must use the root CHANGELOG.md")
    if changelog.get("format") != "keep-a-changelog/1.1" or changelog.get("unreleased_heading") != "Unreleased":
        raise ValueError("release declaration must retain Aether's Keep a Changelog Unreleased convention")
    changelog_path = repository / "CHANGELOG.md"
    if not changelog_path.is_file():
        raise ValueError("root CHANGELOG.md is missing")
    if re.search(r"^## \[Unreleased\]\s*$", changelog_path.read_text(encoding="utf-8"), re.MULTILINE) is None:
        raise ValueError("root CHANGELOG.md must contain the exact ## [Unreleased] heading")

    components = declaration.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("release declaration must name at least one component")
    if any(not isinstance(component, dict) or not isinstance(component.get("version_authority"), dict) for component in components):
        raise ValueError("every declared component must retain one version_authority")

    automation = declaration.get("automation")
    if not isinstance(automation, dict):
        raise ValueError("release declaration.automation must be an object")
    taskfile = _repository_path(repository, automation.get("taskfile_path"), "Taskfile path")
    if not taskfile.is_file():
        raise ValueError("declared Taskfile is missing")
    handoff_names = _task_handoff_names(repository, taskfile)
    tasks = automation.get("tasks")
    if not isinstance(tasks, dict) or set(tasks) != {"plan", "prepare", "verify", "publish"}:
        raise ValueError("release declaration must name the four Aether Taskfile handoffs")
    expected_tasks = {slot: f"release:{slot}" for slot in ("plan", "prepare", "verify", "publish")}
    if tasks != expected_tasks:
        raise ValueError("declared task identity must match the four baseline handoffs")
    for task_name in expected_tasks.values():
        if task_name not in handoff_names:
            raise ValueError(f"declared Taskfile handoff is missing: {task_name}")

    github = automation.get("github")
    if not isinstance(github, dict) or github.get("manual_dispatch_required") is not True:
        raise ValueError("release declaration must retain the manual GitHub handoff")
    workflow = _repository_path(repository, github.get("workflow_path"), "release workflow path")
    if not workflow.is_file():
        raise ValueError("declared manual release workflow is missing")
    workflow_text = workflow.read_text(encoding="utf-8")
    _manual_workflow(workflow_text)

    release_doc = repository / "docs" / "ecosystem" / "REPOSITORY_RELEASE.md"
    if not release_doc.is_file():
        raise ValueError("repository release and rollback guidance is missing")
    release_doc_text = release_doc.read_text(encoding="utf-8")
    if AETHER_REVISION not in release_doc_text or "Rollback" not in release_doc_text:
        raise ValueError("release guidance must name the immutable Aether pin and rollback path")
    agents = repository / "AGENTS.md"
    if not agents.is_file() or "REPOSITORY_RELEASE.md" not in agents.read_text(encoding="utf-8"):
        raise ValueError("AGENTS.md must point to repository release guidance")
    if declaration_path.read_bytes() != declaration_bytes:
        raise ValueError("declaration bytes changed during composed validation")
    evidence = {
        "status": "passed", "scope": "owner-contract-and-local-handoffs",
        "declaration_sha256": hashlib.sha256(declaration_bytes).hexdigest(),
        "owner": owner_evidence,
        "local": {"task_handoffs": "structural", "workflow_triggers": ["workflow_dispatch"], "yaml_engine": "PyYAML.SafeLoader-with-string-on-keys", "yaml_engine_version": _runtime_version("PyYAML"), "publication": "not-performed"},
    }
    return declaration, evidence


def validate_declaration(repository: Path, profile: Mapping[str, Any], *, aether_source: Path | None = None) -> dict[str, Any]:
    return validate_declaration_with_evidence(repository, profile, aether_source=aether_source)[0]


def render_plan(declaration: Mapping[str, Any], profile: Mapping[str, Any], validation: Mapping[str, Any] | None = None) -> str:
    """Render deterministic, non-publishing baseline validation output."""

    subject = declaration["repository"]
    return json.dumps(
        {
            "schema": "egohygiene.repository-release-baseline-plan/v1",
            "policy": {
                "id": profile["schema"],
                "version": profile["version"],
                "status": profile["status"],
                "aether_revision": profile["aether_contract"]["revision"],
            },
            "repository": subject.get("id"),
            "release_profile": subject["release_profile"],
            "lifecycle": subject["lifecycle"],
            "validation": validation or {"status": "unavailable", "reason": "No composed validation evidence supplied"},
            "next_step": "Create or review a release PR; this command does not tag, publish, deploy, or use credentials.",
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("catalog/repository-release-policy.json"),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-profile")
    resolve = subparsers.add_parser("resolve")
    resolve.add_argument("--repository-profile", required=True)
    resolve.add_argument("--lifecycle", required=True)
    resolve.add_argument("--visibility", required=True)
    resolve.add_argument("--adoption-state", required=True)
    declaration = subparsers.add_parser("validate-declaration")
    declaration.add_argument("--repository", type=Path, default=Path("."))
    declaration.add_argument("--format", choices=("text", "json"), default="text")
    declaration.add_argument("--aether-source", type=Path, help="Prepared exact owner source; defaults to .cache/release/aether in the repository")
    owner = subparsers.add_parser("verify-owner")
    owner.add_argument("--aether-source", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        profile = load_json(arguments.profile)
        if arguments.command == "verify-owner":
            errors = validate_profile(profile)
            if errors:
                raise ValueError("invalid selected policy")
            _, evidence = verify_owner_source(arguments.aether_source.resolve(), profile)
            print(json.dumps({"status": "source-verified", "owner": evidence}, indent=2, sort_keys=True))
            return 0
        if arguments.command == "validate-profile":
            errors = validate_profile(profile)
        elif arguments.command == "resolve":
            errors = validate_profile(profile)
            if not errors:
                print(
                    json.dumps(
                        resolve_requirements(
                            profile,
                            arguments.repository_profile,
                            arguments.lifecycle,
                            arguments.visibility,
                            arguments.adoption_state,
                        ),
                        indent=2,
                        sort_keys=True,
                    )
                )
                return 0
        else:
            declaration, evidence = validate_declaration_with_evidence(arguments.repository, profile, aether_source=arguments.aether_source)
            if arguments.format == "json":
                print(render_plan(declaration, profile, evidence), end="")
            else:
                print("repository release baseline valid: reviewed release preparation remains required")
            return 0
    except OwnerValidationUnavailable as error:
        print(f"repository release validation unavailable: {error}", file=sys.stderr)
        return 2
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"repository release policy invalid: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"repository release policy invalid: {error}", file=sys.stderr)
        return 1
    print("repository release policy valid: validate-profile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
