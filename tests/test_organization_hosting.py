from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import organization_hosting as hosting  # noqa: E402
import site_surfaces  # noqa: E402
from test_site_surfaces import _schema_errors  # noqa: E402


class OrganizationHostingTests(unittest.TestCase):
    """Authored contract cases, never actual publication or approval evidence."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads((ROOT / site_surfaces.REGISTRY_PATH).read_text())
        cls.schema = json.loads((ROOT / "schemas/public-site-surface-declaration.v2.schema.json").read_text())
        cls.registry_revision = "a" * 40

    def declaration(self) -> dict:
        # These example.invalid observations and repeated SHAs are synthetic
        # test inputs. No complete declaration is published as observed facts.
        value = json.loads((ROOT / "fixtures/public-site-surfaces/organization-hybrid.valid.json").read_text())
        previous = value["site"]["id"]
        value.update(schema=hosting.DECLARATION_SCHEMA,
                     contract_version=hosting.CONTRACT_VERSION,
                     hosting_profile=hosting.HOSTING_PROFILE,
                     synthetic=False)
        value["registry"]["revision"] = self.registry_revision
        value["site"].update(id="egohygiene/.github",
                             publication_repository="egohygiene/.github",
                             origin="https://egohygiene.github.io",
                             base_path="/.github/")
        for row in value["surfaces"]:
            if row["owner"] == previous:
                row["owner"] = "egohygiene/.github"
            row["publication_owner"] = "egohygiene/.github"
            if row["source_artifact"] and row["source_artifact"]["owner"] == previous:
                row["source_artifact"]["owner"] = "egohygiene/.github"
            if row["renderer"]:
                if row["id"] in hosting.EXPORT_SURFACES:
                    row["renderer"] = {
                        "owner": hosting.RENDERER_OWNER,
                        "contract": hosting.RENDERER_CONTRACT,
                        "implementation": "https://github.com/egohygiene/egohygiene.io/blob/"
                            + "b" * 40 + "/scripts/build-intelligence-export.mts",
                        "version": "b" * 40,
                    }
                elif row["renderer"]["owner"] == previous:
                    row["renderer"]["owner"] = "egohygiene/.github"
            if row["publication"]["canonical_url"]:
                row["publication"]["canonical_url"] = (
                    "https://egohygiene.github.io/.github" + row["canonical_route"]
                )
        return value

    @staticmethod
    def row(value: dict, surface_id: str) -> dict:
        return next(row for row in value["surfaces"] if row["id"] == surface_id)

    def errors(self, value: dict) -> list[str]:
        return hosting.validate_declaration(value, self.registry, self.registry_revision)

    def test_complete_organization_export_names_actual_website_renderer(self) -> None:
        value = self.declaration()
        original = copy.deepcopy(value)
        self.assertEqual(36, len(value["surfaces"]))
        self.assertEqual([], self.errors(value))
        self.assertEqual([], _schema_errors(value, self.schema, self.schema))
        self.assertEqual(original, value)
        self.assertEqual(hosting.canonical_digest(original), hosting.canonical_digest(value))
        self.assertEqual("egohygiene/egohygiene.io", self.row(value, "landing")["renderer"]["owner"])

    def test_all_legacy_fixtures_preserve_original_validator_results(self) -> None:
        for path in sorted((ROOT / "fixtures/public-site-surfaces").glob("*.valid.json")):
            with self.subTest(path=path.name):
                value = json.loads(path.read_text())
                original = site_surfaces.validate_declaration(value, self.registry)
                self.assertEqual([], original)
                self.assertEqual(original, hosting.validate_declaration(value, self.registry))

    def test_legacy_declaration_cannot_claim_export_renderer(self) -> None:
        value = self.declaration()
        value.pop("hosting_profile")
        value.update(schema=site_surfaces.DECLARATION_SCHEMA,
                     contract_version=site_surfaces.CONTRACT_VERSION)
        self.assertTrue(self.errors(value))

    def test_profile_cannot_move_to_repository_or_another_publisher(self) -> None:
        for key, invalid in [("route_profile", "repository"),
                             ("id", "egohygiene/identity"),
                             ("publication_repository", "egohygiene/egohygiene.io"),
                             ("base_path", "/other/"),
                             ("origin", "https://other.example.invalid")]:
            with self.subTest(key=key):
                value = self.declaration()
                value["site"][key] = invalid
                self.assertTrue(self.errors(value))
                self.assertTrue(_schema_errors(value, self.schema, self.schema))

    def test_actual_website_renderer_cannot_be_relabelled_relay(self) -> None:
        value = self.declaration()
        renderer = self.row(value, "intelligence")["renderer"]
        renderer.update(owner="egohygiene/relay", contract="relay-compatible")
        self.assertTrue(self.errors(value))
        self.assertTrue(_schema_errors(value, self.schema, self.schema))

    def test_renderer_revision_and_implementation_are_one_exact_producer(self) -> None:
        for key, invalid in [("version", "1.0.0"),
                             ("owner", "egohygiene/relay"),
                             ("implementation", "https://github.com/egohygiene/egohygiene.io/blob/"
                              + "c" * 40 + "/scripts/build-intelligence-export.mts")]:
            with self.subTest(key=key):
                value = self.declaration()
                self.row(value, "landing")["renderer"][key] = invalid
                self.assertTrue(self.errors(value))

    def test_export_renderer_is_not_a_general_site_renderer_override(self) -> None:
        value = self.declaration()
        self.row(value, "privacy")["renderer"] = copy.deepcopy(self.row(value, "landing")["renderer"])
        self.assertTrue(self.errors(value))
        self.assertTrue(_schema_errors(value, self.schema, self.schema))

    def test_one_sealed_export_cannot_mix_renderer_revisions(self) -> None:
        value = self.declaration()
        self.row(value, "intelligence")["renderer"].update(
            version="c" * 40,
            implementation="https://github.com/egohygiene/egohygiene.io/blob/"
                + "c" * 40 + "/scripts/build-intelligence-export.mts",
        )
        self.assertIn("organization export renderers must name one exact producer revision",
                      self.errors(value))

    def test_omissions_registry_pin_and_source_ownership_still_fail_closed(self) -> None:
        value = self.declaration()
        value["surfaces"].pop()
        self.assertTrue(self.errors(value))
        value = self.declaration()
        self.row(value, "landing")["source_artifact"]["owner"] = "egohygiene/egohygiene.io"
        self.assertTrue(self.errors(value))
        value = self.declaration()
        value["registry"]["sha256"] = "0" * 64
        self.assertTrue(self.errors(value))
        self.assertTrue(hosting.validate_declaration(self.declaration(), self.registry))

    def test_new_renderer_does_not_supply_missing_publication_evidence(self) -> None:
        value = self.declaration()
        self.row(value, "landing")["publication"]["evidence_url"] = None
        self.assertTrue(self.errors(value))
        self.assertTrue(_schema_errors(value, self.schema, self.schema))

    def test_unknown_dialect_profile_and_extra_fields_are_denied(self) -> None:
        for key, invalid in [("schema", "egohygiene.public-site-surface-declaration/v3"),
                             ("hosting_profile", "arbitrary-renderer"),
                             ("synthetic", True), ("deployment_authorized", True)]:
            with self.subTest(key=key):
                value = self.declaration()
                value[key] = invalid
                self.assertTrue(self.errors(value))
                self.assertTrue(_schema_errors(value, self.schema, self.schema))


if __name__ == "__main__":
    unittest.main()
