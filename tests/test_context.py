from __future__ import annotations

import copy
import json
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import catalog  # noqa: E402
import context  # noqa: E402


SOURCE_REVISION = "a" * 40


class RepositoryContextContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = catalog.load_catalog(ROOT / "catalog" / "repositories.yaml")
        cls.policy = context.load_json(ROOT / "catalog" / "repository-context.json")

    def test_policy_covers_every_catalog_input(self) -> None:
        self.assertEqual([], context.validate_policy(self.catalog, self.policy))

    def test_empathy_projection_has_owned_boundaries_and_neighbors(self) -> None:
        projection = context.build_context(
            self.catalog, self.policy, "empathy", SOURCE_REVISION
        )
        self.assertEqual("egohygiene/empathy", projection["repository"])
        self.assertEqual(
            [
                "egohygiene/egolint",
                "egohygiene/mantle",
                "egohygiene/realm",
                "egohygiene/relay",
            ],
            projection["neighbors"]["upstream"],
        )
        self.assertIn("golden consumer", projection["ownership"]["owns"])
        self.assertIn(
            "Do not absorb or claim ownership of permanent sibling component source.",
            projection["constraints"],
        )

    def test_external_inputs_remain_visible_without_fake_repository_owner(self) -> None:
        projection = context.build_context(
            self.catalog, self.policy, "store", SOURCE_REVISION
        )
        self.assertEqual(["commerce provider API"], projection["dependencies"]["external_inputs"])
        self.assertEqual(["egohygiene/identity"], projection["neighbors"]["upstream"])

    def test_projection_and_markdown_are_byte_deterministic(self) -> None:
        first = context.build_context(self.catalog, self.policy, "hygiene", SOURCE_REVISION)
        second = context.build_context(
            copy.deepcopy(self.catalog), copy.deepcopy(self.policy), "hygiene", SOURCE_REVISION
        )
        self.assertEqual(first, second)
        self.assertEqual(context.render_markdown(first), context.render_markdown(second))

    def test_markdown_carries_machine_verifiable_markers(self) -> None:
        projection = context.build_context(
            self.catalog, self.policy, "egolint", SOURCE_REVISION
        )
        rendered = context.render_markdown(projection)
        self.assertTrue(rendered.startswith(context.MARKER + "\n---\n"))
        self.assertIn('architecture-release: "architecture-v0.1.0"', rendered)
        self.assertIn(f'source-revision: "{SOURCE_REVISION}"', rendered)
        self.assertIn(
            'generated-by: "egohygiene/hygiene:repository-context@1.0.0"', rendered
        )

    def test_invalid_revision_and_stale_policy_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "40-character"):
            context.build_context(self.catalog, self.policy, "hygiene", "main")
        stale = copy.deepcopy(self.policy)
        stale["architecture_release"] = "architecture-v0.0.0"
        self.assertIn(
            "context architecture_release must match the repository catalog",
            context.validate_policy(self.catalog, stale),
        )

    def test_egolint_contract_is_canonical_and_immutable(self) -> None:
        rendered = context.render_egolint_contract(self.policy, SOURCE_REVISION)
        self.assertIn('id = "hygiene-repository-context"', rendered)
        self.assertIn("provisional = false", rendered)
        self.assertIn('revision-kind = "git-commit"', rendered)
        self.assertIn(f'revision = "{SOURCE_REVISION}"', rendered)
        self.assertIn(context.MARKER, rendered)

    def test_context_schema_is_valid_json(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository-context.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema", schema["$schema"]
        )
        self.assertEqual("1.0.0", schema["properties"]["schema_version"]["const"])

    def test_checked_in_hygiene_projection_and_egolint_contract_are_current(self) -> None:
        contract_path = ROOT / "contracts" / "repository-context.toml"
        contract = tomllib.loads(contract_path.read_text(encoding="utf-8"))
        source_revision = contract["source"]["revision"]
        expected_context = context.render_markdown(
            context.build_context(
                self.catalog,
                self.policy,
                "egohygiene/hygiene",
                source_revision,
            )
        )
        self.assertEqual(
            expected_context,
            (ROOT / "docs" / "ecosystem" / "CONTEXT.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            context.render_egolint_contract(self.policy, source_revision),
            contract_path.read_text(encoding="utf-8"),
        )
        self.assertFalse(contract["provisional"])
        self.assertTrue((ROOT / contract["source"]["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
