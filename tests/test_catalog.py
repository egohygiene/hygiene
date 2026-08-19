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
        self.assertEqual(25, len(self.source["repositories"]))

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


if __name__ == "__main__":
    unittest.main()
