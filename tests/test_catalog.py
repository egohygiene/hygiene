from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import catalog  # noqa: E402


class CatalogContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = catalog.load_catalog(ROOT / "catalog" / "repositories.yaml")

    def test_current_catalog_is_valid(self) -> None:
        self.assertEqual([], catalog.validate_catalog(self.source))
        self.assertEqual(27, len(self.source["repositories"]))

    def test_duplicate_repository_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.source)
        candidate["repositories"].append(copy.deepcopy(candidate["repositories"][0]))
        candidate["repository_count"] += 1
        self.assertIn("repository names must be unique", catalog.validate_catalog(candidate))

    def test_incomplete_ownership_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.source)
        candidate["repositories"][0]["owns"] = []
        errors = catalog.validate_catalog(candidate)
        self.assertIn("repositories[0].owns must not be empty", errors)

    def test_unknown_plane_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.source)
        candidate["repositories"][0]["plane"] = "unknown"
        errors = catalog.validate_catalog(candidate)
        self.assertIn("repositories[0].plane is not declared", errors)

    def test_proposed_current_overlap_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.source)
        candidate["proposed_repositories"][0]["name"] = "realm"
        candidate["proposed_repositories"][0]["target_full_name"] = "egohygiene/realm"
        errors = catalog.validate_catalog(candidate)
        self.assertIn("proposed repositories already exist: realm", errors)

    def test_render_is_deterministic(self) -> None:
        first = catalog.render_markdown(self.source)
        second = catalog.render_markdown(copy.deepcopy(self.source))
        self.assertEqual(first, second)
        self.assertIn("architecture-v0.1.0", first)

    def test_json_compatible_yaml_needs_no_yaml_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "catalog.yaml"
            target.write_text("{\"schema_version\": \"1.0.0\"}\n", encoding="utf-8")
            self.assertEqual("1.0.0", catalog.load_catalog(target)["schema_version"])

    def test_current_and_proposed_names_reject_path_and_noncanonical_identities(self) -> None:
        for name in ("../escaped", "/absolute", "nested/repo", "..", "name\\child", "Upper", "name\n", "name_underscore"):
            for collection in ("repositories", "proposed_repositories"):
                with self.subTest(name=name, collection=collection):
                    candidate = copy.deepcopy(self.source)
                    repository = candidate[collection][0]
                    repository["name"] = name
                    if collection == "repositories":
                        repository["full_name"] = f"egohygiene/{name}"
                        repository["source_url"] = f"https://github.com/egohygiene/{name}"
                    else:
                        repository["target_full_name"] = f"egohygiene/{name}"
                    self.assertTrue(
                        any(f"{collection}[0].name" in error for error in catalog.validate_catalog(candidate))
                    )

    def test_rename_target_uses_the_same_identity_grammar(self) -> None:
        for name in ("../escaped", "/absolute", "name\\child", "Upper", "name\n"):
            with self.subTest(name=name):
                candidate = copy.deepcopy(self.source)
                candidate["repositories"][0]["target_name"] = name
                self.assertTrue(
                    any("repositories[0].target_name" in error for error in catalog.validate_catalog(candidate))
                )

    def test_schema_valid_name_forms_remain_valid(self) -> None:
        for name in (".github", "repo-name", "egohygiene.io", "a", "1", "a..b"):
            with self.subTest(name=name):
                candidate = copy.deepcopy(self.source)
                candidate["repositories"][0]["target_name"] = name
                self.assertEqual([], catalog.validate_catalog(candidate))


if __name__ == "__main__":
    unittest.main()
