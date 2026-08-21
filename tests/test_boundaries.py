from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import boundaries  # noqa: E402


class DependencyBoundaryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.register = boundaries.load_object(
            ROOT / "catalog" / "dependency-boundaries.yaml"
        )
        cls.catalog = boundaries.load_object(ROOT / "catalog" / "repositories.yaml")
        cls.contract_index = boundaries.load_object(
            ROOT / "catalog" / "contracts.yaml"
        )

    def test_current_register_is_valid(self) -> None:
        self.assertEqual(
            [],
            boundaries.validate_register(
                self.register, self.catalog, self.contract_index
            ),
        )
        self.assertEqual(17, len(self.register["relationships"]))

    def test_duplicate_rule_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.register)
        candidate["rules"].append(copy.deepcopy(candidate["rules"][0]))
        errors = boundaries.validate_register(
            candidate, self.catalog, self.contract_index
        )
        self.assertIn("duplicate rule id: BOUNDARY-001", errors)

    def test_unknown_producer_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.register)
        candidate["relationships"][0]["producer"] = "egohygiene/unknown"
        errors = boundaries.validate_register(
            candidate, self.catalog, self.contract_index
        )
        self.assertIn(
            "relationships[0].producer references unknown repository egohygiene/unknown",
            errors,
        )

    def test_wildcard_consumer_is_allowed(self) -> None:
        candidate = copy.deepcopy(self.register)
        candidate["relationships"][0]["consumers"] = ["egohygiene/*"]
        self.assertEqual(
            [],
            boundaries.validate_register(
                candidate, self.catalog, self.contract_index
            ),
        )

    def test_active_contract_requires_an_identifier(self) -> None:
        candidate = copy.deepcopy(self.register)
        candidate["relationships"][0]["contract"] = None
        errors = boundaries.validate_register(
            candidate, self.catalog, self.contract_index
        )
        self.assertIn(
            "relationships[0].contract is required when contract_status is active",
            errors,
        )

    def test_approved_exception_requires_approval_and_expiry(self) -> None:
        candidate = copy.deepcopy(self.register)
        candidate["exceptions"] = [
            {
                "id": "EXCEPTION-001",
                "rule": "BOUNDARY-002",
                "owner": "egohygiene/relay",
                "reason": "Migration fixture",
                "status": "approved",
                "approval": None,
                "expires_on": None,
                "affected_repositories": ["egohygiene/relay"],
            }
        ]
        errors = boundaries.validate_register(
            candidate, self.catalog, self.contract_index
        )
        self.assertIn("exceptions[0].approval is required when approved", errors)
        self.assertIn("exceptions[0].expires_on is required", errors)

    def test_media_sibling_prohibitions_are_complete(self) -> None:
        candidate = copy.deepcopy(self.register)
        candidate["forbidden_dependencies"].pop()
        errors = boundaries.validate_register(
            candidate, self.catalog, self.contract_index
        )
        self.assertTrue(
            any(error.startswith("media sibling prohibitions missing:") for error in errors)
        )

    def test_active_relationship_contract_must_resolve(self) -> None:
        candidate = copy.deepcopy(self.register)
        candidate["relationships"][0]["contract"] = "egohygiene.unknown/v1"
        errors = boundaries.validate_register(
            candidate, self.catalog, self.contract_index
        )
        self.assertIn(
            "relationships[0].contract must resolve to an active organization contract",
            errors,
        )

    def test_render_is_deterministic(self) -> None:
        first = boundaries.render_markdown(self.register)
        second = boundaries.render_markdown(copy.deepcopy(self.register))
        self.assertEqual(first, second)
        self.assertIn("BOUNDARY-001", first)
        self.assertIn("RELATIONSHIP-017", first)


class DependencyBoundaryScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = boundaries.load_object(ROOT / "catalog" / "repositories.yaml")

    def scan(self, files: dict[str, str]) -> list[boundaries.Finding]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative_path, content in files.items():
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return boundaries.scan_repository(root, "egohygiene/hygiene", self.catalog)

    def test_mutable_reusable_action_is_rejected(self) -> None:
        findings = self.scan(
            {
                ".github/workflows/ci.yml": (
                    "steps:\n  - uses: egohygiene/relay/actions/test@main\n"
                )
            }
        )
        self.assertEqual(1, len(findings))
        self.assertEqual("BOUNDARY-002", findings[0].rule)
        self.assertIn("egohygiene/relay", findings[0].message)

    def test_immutable_reusable_action_is_allowed(self) -> None:
        findings = self.scan(
            {
                ".github/workflows/ci.yml": (
                    "steps:\n"
                    "  - uses: egohygiene/relay/actions/test@"
                    "2d9e7c4ff5de4f832d28b3ce105b2a4da8382dd7\n"
                )
            }
        )
        self.assertEqual([], findings)

    def test_raw_default_branch_reference_is_rejected(self) -> None:
        findings = self.scan(
            {
                "config/tool.yaml": (
                    "source: https://raw.githubusercontent.com/egohygiene/"
                    "aether/main/spec.json\n"
                )
            }
        )
        self.assertEqual(1, len(findings))
        self.assertEqual("BOUNDARY-002", findings[0].rule)

    def test_path_dependency_escaping_repository_is_rejected(self) -> None:
        findings = self.scan(
            {"pyproject.toml": 'mantle = { path = "../mantle" }\n'}
        )
        self.assertEqual(1, len(findings))
        self.assertEqual("BOUNDARY-001", findings[0].rule)

    def test_sibling_source_under_staging_is_rejected(self) -> None:
        findings = self.scan({".staging/mantle/runtime.sh": "true\n"})
        self.assertEqual(1, len(findings))
        self.assertEqual("BOUNDARY-001", findings[0].rule)

    def test_markdown_discussion_is_not_scanned_as_a_dependency(self) -> None:
        findings = self.scan(
            {
                "README.md": (
                    "Do not use egohygiene/relay/actions/test@main in production.\n"
                )
            }
        )
        self.assertEqual([], findings)

    def test_current_hygiene_checkout_is_clean(self) -> None:
        findings = boundaries.scan_repository(
            ROOT, "egohygiene/hygiene", self.catalog
        )
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
