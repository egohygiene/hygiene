from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "public-site-surfaces"
sys.path.insert(0, str(ROOT / "tools"))

import site_surfaces  # noqa: E402


def _strict_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )


def _resolve_local_ref(root: dict, reference: str) -> dict:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {reference}")
    value: object = root
    for raw_token in reference[2:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            raise ValueError(f"unresolvable schema reference: {reference}")
        value = value[token]
    if not isinstance(value, dict):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return value


def _schema_errors(
    instance: object,
    schema: dict,
    root: dict,
    path: str = "$",
) -> list[str]:
    """Validate the JSON Schema subset used by the two public-site contracts."""

    if "$ref" in schema:
        return _schema_errors(instance, _resolve_local_ref(root, schema["$ref"]), root, path)

    def json_equal(left: object, right: object) -> bool:
        if isinstance(left, bool) or isinstance(right, bool):
            return (
                isinstance(left, bool)
                and isinstance(right, bool)
                and left == right
            )
        if isinstance(left, dict) or isinstance(right, dict):
            return (
                isinstance(left, dict)
                and isinstance(right, dict)
                and set(left) == set(right)
                and all(json_equal(left[key], right[key]) for key in left)
            )
        if isinstance(left, list) or isinstance(right, list):
            return (
                isinstance(left, list)
                and isinstance(right, list)
                and len(left) == len(right)
                and all(json_equal(a, b) for a, b in zip(left, right))
            )
        return left == right

    errors: list[str] = []
    if "const" in schema and not json_equal(instance, schema["const"]):
        errors.append(f"{path} does not equal const")
    if "enum" in schema and not any(
        json_equal(instance, candidate) for candidate in schema["enum"]
    ):
        errors.append(f"{path} is not in enum")

    expected_types = schema.get("type")
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        type_checks = {
            "array": lambda value: isinstance(value, list),
            "boolean": lambda value: isinstance(value, bool),
            "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
            "null": lambda value: value is None,
            "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
            "object": lambda value: isinstance(value, dict),
            "string": lambda value: isinstance(value, str),
        }
        if not any(type_checks[item](instance) for item in expected_types):
            errors.append(f"{path} has the wrong type")
            return errors

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                errors.append(f"{path}.{key} is required")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(
                    _schema_errors(value, properties[key], root, f"{path}.{key}")
                )
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}.{key} is an additional property")

    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path} has too few items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path} has too many items")
        if schema.get("uniqueItems"):
            serialized = [
                json.dumps(value, sort_keys=True, separators=(",", ":"))
                for value in instance
            ]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path} contains duplicate items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                errors.extend(
                    _schema_errors(value, item_schema, root, f"{path}[{index}]")
                )

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path} is too short")
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, instance) is None:
            errors.append(f"{path} does not match pattern")
        if schema.get("format") == "date-time" and not site_surfaces._is_datetime(instance):  # noqa: SLF001
            errors.append(f"{path} is not a date-time")
        if schema.get("format") == "uri" and not site_surfaces._is_https(instance):  # noqa: SLF001
            errors.append(f"{path} is not a valid HTTPS URI")

    if "not" in schema and not _schema_errors(instance, schema["not"], root, path):
        errors.append(f"{path} matches a prohibited schema")
    if "oneOf" in schema:
        matches = sum(
            not _schema_errors(instance, candidate, root, path)
            for candidate in schema["oneOf"]
        )
        if matches != 1:
            errors.append(f"{path} must match exactly one alternative")
    for candidate in schema.get("allOf", []):
        errors.extend(_schema_errors(instance, candidate, root, path))
    if "if" in schema:
        branch = "then" if not _schema_errors(instance, schema["if"], root, path) else "else"
        if branch in schema:
            errors.extend(_schema_errors(instance, schema[branch], root, path))
    return errors


def _schema_structure_errors(schema: object, root: dict, path: str = "$schema") -> list[str]:
    errors: list[str] = []
    if isinstance(schema, list):
        for index, value in enumerate(schema):
            errors.extend(_schema_structure_errors(value, root, f"{path}[{index}]"))
        return errors
    if not isinstance(schema, dict):
        return errors
    if "$ref" in schema:
        try:
            _resolve_local_ref(root, schema["$ref"])
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
    properties = schema.get("properties")
    required = schema.get("required")
    if isinstance(properties, dict) and isinstance(required, list):
        missing = sorted(set(required) - set(properties))
        if missing:
            errors.append(f"{path} requires undeclared properties: {missing}")
    for key, value in schema.items():
        errors.extend(_schema_structure_errors(value, root, f"{path}.{key}"))
    return errors


class PublicSiteSurfaceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = site_surfaces.load_json(
            ROOT / "catalog" / "public-site-surface-registry.json"
        )
        cls.registry_schema = _strict_json(
            ROOT / "schemas" / "public-site-surface-registry.v1.schema.json"
        )
        cls.declaration_schema = _strict_json(
            ROOT / "schemas" / "public-site-surface-declaration.v1.schema.json"
        )
        cls.fixtures = {
            path.name: site_surfaces.load_json(path)
            for path in sorted(FIXTURES.glob("*.valid.json"))
        }

    def surface(self, surface_id: str) -> dict:
        return next(
            surface
            for surface in self.registry["surfaces"]
            if surface["id"] == surface_id
        )

    @staticmethod
    def declared(fixture: dict, surface_id: str) -> dict:
        return next(
            surface
            for surface in fixture["surfaces"]
            if surface["id"] == surface_id
        )

    def test_schema_documents_are_strict_json_schema_2020_12(self) -> None:
        expected_ids = {
            "public-site-surface-registry.v1.schema.json": (
                "https://egohygiene.io/schemas/hygiene/"
                "public-site-surface-registry.v1.schema.json"
            ),
            "public-site-surface-declaration.v1.schema.json": (
                "https://egohygiene.io/schemas/hygiene/"
                "public-site-surface-declaration.v1.schema.json"
            ),
        }
        for filename, expected_id in expected_ids.items():
            with self.subTest(filename=filename):
                schema = _strict_json(ROOT / "schemas" / filename)
                self.assertEqual(
                    "https://json-schema.org/draft/2020-12/schema",
                    schema["$schema"],
                )
                self.assertEqual(expected_id, schema["$id"])
                self.assertFalse(schema["additionalProperties"])
                version_field = (
                    "version"
                    if "version" in schema["properties"]
                    else "contract_version"
                )
                self.assertEqual(
                    "1.0.0-alpha.1",
                    schema["properties"][version_field]["const"],
                )
                self.assertEqual([], _schema_structure_errors(schema, schema))

        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            site_surfaces._object_without_duplicates(  # noqa: SLF001
                [("schema", "first"), ("schema", "second")]
            )
        with tempfile.TemporaryDirectory() as directory:
            duplicate = Path(directory) / "duplicate.json"
            duplicate.write_text(
                '{"schema":"first","schema":"second"}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                site_surfaces.load_json(duplicate)

    def test_shipped_contract_instances_satisfy_their_json_schemas(self) -> None:
        self.assertEqual(
            [],
            _schema_errors(
                self.registry,
                self.registry_schema,
                self.registry_schema,
            ),
        )
        for filename, fixture in self.fixtures.items():
            with self.subTest(filename=filename):
                self.assertEqual(
                    [],
                    _schema_errors(
                        fixture,
                        self.declaration_schema,
                        self.declaration_schema,
                    ),
                )

    def test_json_schema_and_semantic_checker_reject_key_state_contradictions(self) -> None:
        mutations = []

        missing_evidence = copy.deepcopy(self.fixtures["content-small.valid.json"])
        missing = self.declared(missing_evidence, "documentation")["publication"]
        missing.update(
            freshness="unknown",
            assertion="unknown",
            evidence_url=None,
            represented_revision=None,
            observed_at=None,
        )
        mutations.append(missing_evidence)

        published_without_evidence = copy.deepcopy(
            self.fixtures["content-small.valid.json"]
        )
        self.declared(published_without_evidence, "landing")["publication"][
            "evidence_url"
        ] = None
        mutations.append(published_without_evidence)

        private_leak = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        diagnostics = self.declared(private_leak, "diagnostics")
        diagnostics["applicability"].update(
            freshness="current",
            evidence_url="https://example.invalid/private-applicability",
            represented_revision=private_leak["site"]["represented_revision"],
            observed_at="2026-09-21T00:00:00Z",
        )
        mutations.append(private_leak)

        mismatched_not_applicable = copy.deepcopy(
            self.fixtures["organization-hybrid.valid.json"]
        )
        donate = self.declared(mismatched_not_applicable, "donate")
        donate["applicability"] = copy.deepcopy(
            self.declared(mismatched_not_applicable, "landing")["applicability"]
        )
        donate["disposition"] = "owned"
        mutations.append(mismatched_not_applicable)

        for index, candidate in enumerate(mutations):
            with self.subTest(index=index):
                self.assertNotEqual(
                    [],
                    _schema_errors(
                        candidate,
                        self.declaration_schema,
                        self.declaration_schema,
                    ),
                )
                self.assertNotEqual(
                    [],
                    site_surfaces.validate_declaration(candidate, self.registry),
                )

    def test_registry_is_complete_valid_and_proposed(self) -> None:
        contracts = site_surfaces._known_contracts(  # noqa: SLF001
            ROOT / "catalog" / "contracts.yaml"
        )
        self.assertEqual(
            [],
            site_surfaces.validate_registry(self.registry, contracts),
        )
        self.assertEqual("proposed", self.registry["status"])
        self.assertEqual("1.0.0-alpha.1", self.registry["version"])
        self.assertEqual(36, len(self.registry["surfaces"]))

    def test_both_contracts_are_registered_as_proposed(self) -> None:
        contract_index = site_surfaces.load_json(
            ROOT / "catalog" / "contracts.yaml"
        )["contracts"]
        contracts = {item["id"]: item for item in contract_index}
        expected = {
            site_surfaces.REGISTRY_SCHEMA: (
                "schemas/public-site-surface-registry.v1.schema.json"
            ),
            site_surfaces.DECLARATION_SCHEMA: (
                "schemas/public-site-surface-declaration.v1.schema.json"
            ),
        }
        for contract_id, source in expected.items():
            with self.subTest(contract_id=contract_id):
                self.assertEqual("proposed", contracts[contract_id]["status"])
                self.assertEqual("egohygiene/hygiene", contracts[contract_id]["owner"])
                self.assertEqual(source, contracts[contract_id]["source"])

    def test_route_profiles_preserve_organization_and_repository_contracts(self) -> None:
        expected = {
            "documentation": {
                "organization": ("/docs/", ["/documentation/"]),
                "repository": ("/docs/", ["/documentation/"]),
            },
            "roadmap": {
                "organization": ("/roadmap/", ["/intelligence/roadmap/"]),
                "repository": ("/intelligence/roadmap/", ["/roadmap/"]),
            },
            "decisions": {
                "organization": (
                    "/decisions/",
                    ["/adr/", "/intelligence/decisions/"],
                ),
                "repository": (
                    "/intelligence/decisions/",
                    ["/adr/", "/decisions/"],
                ),
            },
            "journey": {
                "organization": (
                    "/intelligence/journey/",
                    ["/activity/", "/intelligence/activity/", "/journey/"],
                ),
                "repository": (
                    "/intelligence/journey/",
                    ["/activity/", "/intelligence/activity/", "/journey/"],
                ),
            },
            "identity": {
                "organization": ("/identity/", []),
                "repository": ("/identity/", []),
            },
            "status": {
                "organization": ("/status/", []),
                "repository": ("/status/", []),
            },
        }
        for surface_id, profiles in expected.items():
            for profile, (route, aliases) in profiles.items():
                with self.subTest(surface_id=surface_id, profile=profile):
                    binding = self.surface(surface_id)["route_bindings"][profile]
                    self.assertEqual(route, binding["canonical_route"])
                    self.assertEqual(aliases, binding["aliases"])
        self.assertEqual(
            "/intelligence/dashboard/",
            self.surface("dashboard")["route_bindings"]["repository"][
                "canonical_route"
            ],
        )
        self.assertEqual(
            "/intelligence/identity/",
            self.surface("identity_intelligence")["route_bindings"][
                "organization"
            ]["canonical_route"],
        )
        self.assertEqual(
            ["intelligence"],
            self.surface("identity_intelligence")["dependencies"]["organization"],
        )
        self.assertEqual(
            {"organization": [], "repository": ["intelligence"]},
            self.surface("roadmap")["dependencies"],
        )
        self.assertTrue(self.registry["route_policy"]["aliases_are_redirects_only"])
        self.assertTrue(
            self.registry["route_policy"][
                "aliases_must_not_publish_duplicate_canonical_content"
            ]
        )
        self.assertEqual("egohygiene/identity", self.surface("identity")["default_owner"])

    def test_three_site_class_fixtures_are_complete_and_valid(self) -> None:
        self.assertEqual(
            {
                "content-small.valid.json",
                "documentation-heavy.valid.json",
                "organization-hybrid.valid.json",
            },
            set(self.fixtures),
        )
        expected_classes = {"content", "documentation", "hybrid"}
        self.assertEqual(
            expected_classes,
            {fixture["site"]["site_class"] for fixture in self.fixtures.values()},
        )
        for filename, fixture in self.fixtures.items():
            with self.subTest(filename=filename):
                self.assertTrue(fixture["synthetic"])
                self.assertEqual(
                    [],
                    site_surfaces.validate_declaration(fixture, self.registry),
                )
                self.assertEqual(
                    [item["id"] for item in self.registry["surfaces"]],
                    [item["id"] for item in fixture["surfaces"]],
                )

    def test_fixture_states_keep_absence_freshness_and_privacy_distinct(self) -> None:
        content = self.fixtures["content-small.valid.json"]
        docs = self.fixtures["documentation-heavy.valid.json"]
        organization = self.fixtures["organization-hybrid.valid.json"]
        checks = [
            (content, "documentation", "missing", "unpublished", "current"),
            (docs, "roadmap", "implemented", "published", "stale"),
            (organization, "audits", "blocked", "unpublished", "current"),
            (organization, "diagnostics", "implemented", "unpublished", "unknown"),
            (
                organization,
                "donate",
                "not_applicable",
                "not_applicable",
                "not_applicable",
            ),
            (organization, "status", "planned", "unpublished", "current"),
        ]
        for fixture, surface_id, implementation, publication, freshness in checks:
            with self.subTest(surface_id=surface_id, implementation=implementation):
                declared = self.declared(fixture, surface_id)["publication"]
                self.assertEqual(implementation, declared["implementation_state"])
                self.assertEqual(publication, declared["publication_state"])
                self.assertEqual(freshness, declared["freshness"])
        private = self.declared(organization, "diagnostics")
        self.assertEqual("private", private["publication"]["visibility"])
        self.assertIsNone(private["source_artifact"])
        self.assertIsNone(private["renderer"])
        self.assertIsNone(private["publication"]["evidence_url"])
        missing = self.declared(content, "documentation")["publication"]
        self.assertIsNotNone(missing["evidence_url"])
        self.assertIsNotNone(missing["represented_revision"])
        self.assertIsNotNone(missing["observed_at"])
        not_applicable = self.declared(organization, "donate")
        self.assertEqual("optional", not_applicable["requirement"])
        self.assertEqual(
            "not_applicable",
            not_applicable["applicability"]["state"],
        )
        self.assertEqual("current", not_applicable["applicability"]["freshness"])
        self.assertIsNotNone(not_applicable["applicability"]["evidence_url"])

    def test_base_path_and_publication_repository_are_explicit(self) -> None:
        docs = self.fixtures["documentation-heavy.valid.json"]
        self.assertEqual("/synthetic-docs/", docs["site"]["base_path"])
        self.assertEqual("repository", docs["site"]["route_profile"])
        self.assertEqual(
            "egohygiene/synthetic-docs-host",
            docs["site"]["publication_repository"],
        )
        landing = self.declared(docs, "landing")
        documentation = self.declared(docs, "documentation")
        self.assertEqual(
            "https://docs.example.invalid/synthetic-docs/",
            landing["publication"]["canonical_url"],
        )
        self.assertEqual(
            "https://docs.example.invalid/synthetic-docs/docs/",
            documentation["publication"]["canonical_url"],
        )
        self.assertEqual(
            "egohygiene/synthetic-docs-host",
            documentation["publication_owner"],
        )

        candidate = copy.deepcopy(docs)
        candidate["site"]["base_path"] = "/docs/v1.0/"
        for surface in candidate["surfaces"]:
            publication = surface["publication"]
            if publication["canonical_url"] is not None:
                route = surface["canonical_route"]
                publication["canonical_url"] = (
                    "https://docs.example.invalid/docs/v1.0/"
                    if route == "/"
                    else f"https://docs.example.invalid/docs/v1.0{route}"
                )
        self.assertEqual([], site_surfaces.validate_declaration(candidate, self.registry))

    def test_route_collision_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.registry)
        blog = next(item for item in candidate["surfaces"] if item["id"] == "blog")
        blog["route_bindings"]["organization"]["aliases"] = ["/docs/"]
        errors = site_surfaces.validate_registry(candidate)
        self.assertTrue(
            any("organization route /docs/ collides" in error for error in errors)
        )

    def test_dependency_cycle_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.registry)
        next(item for item in candidate["surfaces"] if item["id"] == "blog")[
            "dependencies"
        ]["organization"] = ["community"]
        next(item for item in candidate["surfaces"] if item["id"] == "community")[
            "dependencies"
        ]["organization"] = ["blog"]
        errors = site_surfaces.validate_registry(candidate)
        self.assertTrue(
            any("organization surface dependency cycle" in error for error in errors)
        )

    def test_malformed_registry_collections_return_errors_without_crashing(self) -> None:
        candidate = copy.deepcopy(self.registry)
        blog = next(item for item in candidate["surfaces"] if item["id"] == "blog")
        blog["route_bindings"]["organization"]["aliases"] = ["/news/", 7]
        blog["dependencies"]["organization"] = ["landing", {"invalid": True}]
        blog["related_contracts"] = [
            "egohygiene.repository-intelligence/v1",
            {"invalid": True},
        ]
        errors = site_surfaces.validate_registry(candidate, set())
        self.assertTrue(
            any("aliases must contain non-empty strings" in error for error in errors)
        )
        self.assertTrue(
            any(
                "dependencies.organization must contain non-empty strings" in error
                for error in errors
            )
        )
        self.assertTrue(any("related_contracts must contain non-empty strings" in error for error in errors))

    def test_policy_booleans_do_not_accept_json_numbers(self) -> None:
        for policy, field in (
            ("dependency_policy", "published_requires_published_dependencies"),
            ("route_policy", "aliases_are_redirects_only"),
        ):
            with self.subTest(policy=policy):
                candidate = copy.deepcopy(self.registry)
                candidate[policy][field] = 1
                self.assertNotEqual([], site_surfaces.validate_registry(candidate))
                self.assertNotEqual(
                    [],
                    _schema_errors(
                        candidate,
                        self.registry_schema,
                        self.registry_schema,
                    ),
                )

    def test_declaration_must_pin_the_exact_registry_digest(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        candidate["registry"]["sha256"] = "0" * 64
        self.assertIn(
            "declaration.registry.sha256 must match the loaded registry",
            site_surfaces.validate_declaration(candidate, self.registry),
        )

    def test_declaration_routes_and_complete_coverage_are_registry_controlled(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        self.declared(candidate, "landing")["canonical_route"] = "/home/"
        candidate["surfaces"].pop()
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("canonical_route must match" in error for error in errors))
        self.assertIn(
            "declaration.surfaces must cover every registry surface in registry order",
            errors,
        )

    def test_always_applicable_surface_cannot_be_declared_not_applicable(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        landing = self.declared(candidate, "landing")
        landing["applicability"] = copy.deepcopy(
            self.declared(candidate, "donate")["applicability"]
        )
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("always-applicable surface" in error for error in errors))

    def test_always_applicable_surface_cannot_be_unknown(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        landing = self.declared(candidate, "landing")
        landing["applicability"] = {
            "state": "unknown",
            "freshness": "unknown",
            "assertion": "unknown",
            "evidence_url": None,
            "represented_revision": None,
            "observed_at": None,
            "reason": "Synthetic uncertainty.",
        }
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("always-applicable surface" in error for error in errors))

    def test_unknown_applicability_is_evidence_backed_but_delivery_remains_unknown(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        community = self.declared(candidate, "community")
        community["applicability"] = {
            "state": "unknown",
            "freshness": "current",
            "assertion": "authoritative",
            "evidence_url": "https://example.invalid/applicability/unresolved",
            "represented_revision": candidate["site"]["represented_revision"],
            "observed_at": "2026-09-21T00:00:00Z",
            "reason": "A current review could not resolve whether this surface applies.",
        }
        community["disposition"] = "omitted"
        community["source_artifact"] = None
        community["renderer"] = None
        community["publication"] = {
            "implementation_state": "unknown",
            "publication_state": "unknown",
            "visibility": "public",
            "freshness": "unknown",
            "assertion": "unknown",
            "canonical_url": None,
            "evidence_url": None,
            "represented_revision": None,
            "observed_at": None,
            "reason": "Delivery cannot resolve before applicability.",
            "blocked_by": [],
        }
        self.assertEqual([], site_surfaces.validate_declaration(candidate, self.registry))
        self.assertEqual(
            [],
            _schema_errors(
                candidate,
                self.declaration_schema,
                self.declaration_schema,
            ),
        )

        community["applicability"]["evidence_url"] = None
        community["applicability"]["represented_revision"] = None
        community["applicability"]["observed_at"] = None
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("unknown applicability requires" in error for error in errors))

        community["applicability"] = {
            "state": "unknown",
            "freshness": "current",
            "assertion": "authoritative",
            "evidence_url": "https://example.invalid/applicability/unresolved",
            "represented_revision": candidate["site"]["represented_revision"],
            "observed_at": "2026-09-21T00:00:00Z",
            "reason": "Applicability remains unresolved.",
        }
        community["publication"]["reason"] = None
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("reason is required for unknown applicability" in error for error in errors))

    def test_applicable_surface_requires_complete_assessment_evidence(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        community = self.declared(candidate, "community")["applicability"]
        community["freshness"] = "unknown"
        community["evidence_url"] = None
        community["represented_revision"] = None
        community["observed_at"] = None
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("applicable state requires" in error for error in errors))

    def test_not_applicable_axes_must_resolve_together(self) -> None:
        candidate = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        donate = self.declared(candidate, "donate")
        donate["publication"]["implementation_state"] = "planned"
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("not-applicable axes must resolve together" in error for error in errors))

    def test_published_surface_requires_evidence(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        self.declared(candidate, "landing")["publication"]["evidence_url"] = None
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("evidence_url must be HTTPS when published" in error for error in errors))

    def test_blocked_surface_requires_a_named_blocker(self) -> None:
        candidate = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        self.declared(candidate, "audits")["publication"]["blocked_by"] = []
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("blocked_by is required when blocked" in error for error in errors))

    def test_known_unimplemented_surface_requires_assessment_evidence(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        documentation = self.declared(candidate, "documentation")["publication"]
        documentation["freshness"] = "unknown"
        documentation["assertion"] = "unknown"
        documentation["evidence_url"] = None
        documentation["represented_revision"] = None
        documentation["observed_at"] = None
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(
            any("known unimplemented states require complete assessment evidence" in error for error in errors)
        )

    def test_whitespace_only_text_is_rejected_by_schema_and_checker(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        self.declared(candidate, "community")["publication"]["reason"] = " "
        self.assertNotEqual(
            [],
            site_surfaces.validate_declaration(candidate, self.registry),
        )
        self.assertNotEqual(
            [],
            _schema_errors(
                candidate,
                self.declaration_schema,
                self.declaration_schema,
            ),
        )

    def test_private_surface_rejects_evidence_leakage(self) -> None:
        candidate = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        diagnostics = self.declared(candidate, "diagnostics")
        diagnostics["publication"]["evidence_url"] = (
            "https://organization.example.invalid/private-evidence"
        )
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("private surfaces must redact publication evidence" in error for error in errors))

    def test_site_visibility_caps_surface_visibility_in_schema_and_checker(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        candidate["site"]["visibility"] = "private"
        self.assertTrue(
            any(
                "publication.visibility cannot be broader than the site" in error
                for error in site_surfaces.validate_declaration(candidate, self.registry)
            )
        )
        self.assertNotEqual(
            [],
            _schema_errors(
                candidate,
                self.declaration_schema,
                self.declaration_schema,
            ),
        )

    def test_private_surface_rejects_applicability_evidence_leakage(self) -> None:
        candidate = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        diagnostics = self.declared(candidate, "diagnostics")
        diagnostics["applicability"]["freshness"] = "current"
        diagnostics["applicability"]["evidence_url"] = (
            "https://organization.example.invalid/private-applicability"
        )
        diagnostics["applicability"]["represented_revision"] = "d" * 40
        diagnostics["applicability"]["observed_at"] = "2026-09-21T00:00:00Z"
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(
            any("private surfaces must redact applicability evidence" in error for error in errors)
        )

    def test_private_not_applicable_requires_unknown_applicability_freshness(self) -> None:
        errors, _ = site_surfaces._validate_applicability(  # noqa: SLF001
            {
                "state": "not_applicable",
                "freshness": "current",
                "assertion": "authoritative",
                "evidence_url": None,
                "represented_revision": None,
                "observed_at": None,
                "reason": "Private applicability evidence is redacted.",
            },
            "surface.applicability",
            rule="site-declared",
            site_revision="d" * 40,
            private=True,
        )
        self.assertIn("surface.applicability.freshness must be unknown when private", errors)

        candidate = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        donate = self.declared(candidate, "donate")
        donate["applicability"].update(
            freshness="unknown",
            evidence_url=None,
            represented_revision=None,
            observed_at=None,
        )
        donate["publication"]["visibility"] = "private"
        self.assertEqual([], site_surfaces.validate_declaration(candidate, self.registry))
        self.assertEqual(
            [],
            _schema_errors(
                candidate,
                self.declaration_schema,
                self.declaration_schema,
            ),
        )

    def test_registry_authority_and_source_owner_are_enforced(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        identity = self.declared(candidate, "identity")
        identity["owner"] = "egohygiene/fake"
        identity["source_artifact"]["owner"] = "egohygiene/fake"
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(
            any("owner must equal registry authority egohygiene/identity" in error for error in errors)
        )

        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        landing = self.declared(candidate, "landing")
        landing["source_artifact"]["owner"] = "egohygiene/unrelated"
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(
            any("source_artifact.owner must equal the semantic owner" in error for error in errors)
        )

    def test_current_surface_revision_must_match_site_revision(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        landing = self.declared(candidate, "landing")
        landing["publication"]["represented_revision"] = "e" * 40
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("must equal the site revision when current" in error for error in errors))

    def test_stale_surface_revision_must_precede_site_revision(self) -> None:
        candidate = copy.deepcopy(self.fixtures["documentation-heavy.valid.json"])
        roadmap = self.declared(candidate, "roadmap")["publication"]
        roadmap["represented_revision"] = candidate["site"]["represented_revision"]
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("must differ from the site revision when stale" in error for error in errors))

    def test_published_surface_requires_published_dependencies(self) -> None:
        candidate = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        intelligence = self.declared(candidate, "intelligence")["publication"]
        intelligence["publication_state"] = "unpublished"
        intelligence["canonical_url"] = None
        intelligence["evidence_url"] = None
        intelligence["represented_revision"] = None
        intelligence["observed_at"] = None
        intelligence["freshness"] = "unknown"
        intelligence["reason"] = "Synthetic dependency failure."
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("requires published dependency intelligence" in error for error in errors))

    def test_identity_intelligence_can_report_absent_identity_product(self) -> None:
        candidate = copy.deepcopy(self.fixtures["organization-hybrid.valid.json"])
        identity = self.declared(candidate, "identity")
        not_applicable = self.declared(candidate, "donate")
        identity["applicability"] = copy.deepcopy(not_applicable["applicability"])
        identity["disposition"] = "omitted"
        identity["owner"] = candidate["site"]["id"]
        identity["source_artifact"] = None
        identity["renderer"] = None
        identity["publication"] = copy.deepcopy(not_applicable["publication"])
        self.assertEqual(
            "published",
            self.declared(candidate, "identity_intelligence")["publication"][
                "publication_state"
            ],
        )
        self.assertEqual([], site_surfaces.validate_declaration(candidate, self.registry))

    def test_renderer_version_must_be_immutable(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        self.declared(candidate, "landing")["renderer"]["version"] = "latest"
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("exact semantic version or full commit SHA" in error for error in errors))

        for invalid in ("01.0.0", "1.0.0-...", "1.0.0-a..b"):
            with self.subTest(version=invalid):
                candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
                self.declared(candidate, "landing")["renderer"]["version"] = invalid
                errors = site_surfaces.validate_declaration(candidate, self.registry)
                self.assertTrue(any("exact semantic version or full commit SHA" in error for error in errors))

        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        self.declared(candidate, "landing")["renderer"]["version"] = "1.0.0+build.7"
        self.assertEqual([], site_surfaces.validate_declaration(candidate, self.registry))

    def test_renderer_owner_must_match_contract_authority(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        self.declared(candidate, "landing")["renderer"]["owner"] = "egohygiene/unrelated"
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(
            any("owner must equal renderer authority" in error for error in errors)
        )

    def test_implemented_preview_requires_source_and_renderer(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        landing = self.declared(candidate, "landing")
        landing["source_artifact"] = None
        landing["renderer"] = None
        landing["publication"]["publication_state"] = "preview"
        landing["publication"]["canonical_url"] = None
        landing["publication"]["reason"] = "Synthetic preview."
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("implemented surfaces require a source artifact" in error for error in errors))
        self.assertTrue(any("implemented surfaces require a renderer" in error for error in errors))

    def test_source_paths_reject_traversal_and_scheme_like_shapes(self) -> None:
        for location in (
            "..\\secret.json",
            "C:/secrets/file.json",
            "https:foo",
            "git@example.com:repo/file",
        ):
            with self.subTest(location=location):
                candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
                self.declared(candidate, "landing")["source_artifact"]["location"] = location
                errors = site_surfaces.validate_declaration(candidate, self.registry)
                self.assertTrue(any("repository-relative or HTTPS" in error for error in errors))
                self.assertNotEqual(
                    [],
                    _schema_errors(
                        candidate,
                        self.declaration_schema,
                        self.declaration_schema,
                    ),
                )

    def test_non_synthetic_registry_revision_requires_external_resolution(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        candidate["synthetic"] = False
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertIn(
            "non-synthetic declarations require an externally resolved registry revision",
            errors,
        )
        errors = site_surfaces.validate_declaration(
            candidate,
            self.registry,
            expected_registry_revision="f" * 40,
        )
        self.assertIn(
            "declaration.registry.revision must match the externally resolved revision",
            errors,
        )

    def test_malformed_declaration_collections_return_errors_without_crashing(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        self.declared(candidate, "landing")["dependencies"] = 7
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("dependencies must match the registry" in error for error in errors))

    def test_malformed_enum_scalars_return_errors_without_crashing(self) -> None:
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        candidate["site"]["visibility"] = {}
        landing = self.declared(candidate, "landing")
        landing["applicability"]["freshness"] = {}
        landing["publication"]["implementation_state"] = {}
        landing["disposition"] = {}
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertIn("declaration.site.visibility is invalid", errors)
        self.assertTrue(any("applicability.freshness is invalid" in error for error in errors))
        self.assertTrue(any("publication.implementation_state is invalid" in error for error in errors))
        self.assertTrue(any("disposition is invalid" in error for error in errors))

    def test_hostile_urls_and_timezone_less_observations_are_rejected(self) -> None:
        self.assertFalse(site_surfaces._is_https("https://[bad"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_https("https://user@example.invalid"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_https("https://foo\\bar.invalid"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_https("https://example.invalid/\x00path"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_https("HTTPS://example.invalid"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_origin("https://example.invalid?"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_origin("https://example.invalid/#"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_canonical_url("https://example.invalid/path?"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_canonical_url("https://example.invalid/path#"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_datetime("2026-09-21T00:00:00+01:02:03"))  # noqa: SLF001
        self.assertFalse(site_surfaces._is_datetime("2026-09-21T00:00:00+0000"))  # noqa: SLF001
        candidate = copy.deepcopy(self.fixtures["content-small.valid.json"])
        landing = self.declared(candidate, "landing")["publication"]
        landing["canonical_url"] += "?duplicate=true"
        landing["observed_at"] = "2026-09-21T00:00:00"
        errors = site_surfaces.validate_declaration(candidate, self.registry)
        self.assertTrue(any("without query or fragment" in error for error in errors))
        self.assertTrue(any("with a timezone" in error for error in errors))
        self.assertNotEqual(
            [],
            _schema_errors(
                candidate,
                self.declaration_schema,
                self.declaration_schema,
            ),
        )

    def test_synthetic_repository_ids_follow_the_schema_pattern(self) -> None:
        for invalid_id in (
            "egohygiene/synthetic-",
            "egohygiene/synthetic--site",
        ):
            with self.subTest(invalid_id=invalid_id):
                candidate = copy.deepcopy(
                    self.fixtures["content-small.valid.json"]
                )
                candidate["site"]["id"] = invalid_id
                candidate["site"]["publication_repository"] = invalid_id
                errors = site_surfaces.validate_declaration(candidate, self.registry)
                self.assertTrue(
                    any("synthetic declarations require" in error for error in errors)
                )
                self.assertNotEqual(
                    [],
                    _schema_errors(
                        candidate,
                        self.declaration_schema,
                        self.declaration_schema,
                    ),
                )

    def test_route_schema_and_semantic_checker_reject_the_same_hostile_shapes(self) -> None:
        schema = json.loads(
            (
                ROOT / "schemas" / "public-site-surface-registry.v1.schema.json"
            ).read_text(encoding="utf-8")
        )
        pattern = schema["$defs"]["route"]["pattern"]
        import re

        for route in (
            "//docs/",
            "/Upper/",
            "/docs",
            "/bad%20path/",
            "/bad\\path/",
            "/feed.",
            "/feed.-",
        ):
            with self.subTest(route=route):
                self.assertIsNone(re.fullmatch(pattern, route))
                self.assertNotEqual([], site_surfaces._validate_route(route, "route"))  # noqa: SLF001


if __name__ == "__main__":
    unittest.main()
