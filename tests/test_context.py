from __future__ import annotations

import copy
import hashlib
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
            'generated-by: "egohygiene/hygiene:repository-context@2.0.0"', rendered
        )
        self.assertIn(
            'continuity-policy: "egohygiene.repository-continuity-policy/v1@1.0.0-alpha.1"',
            rendered,
        )

    def test_projection_composes_continuity_without_copying_checkpoint_state(self) -> None:
        projection = context.build_context(
            self.catalog, self.policy, "hygiene", SOURCE_REVISION
        )
        continuity = projection["continuity"]
        self.assertEqual("CONTINUITY.md", continuity["path"])
        self.assertEqual("repository-owned", continuity["ownership"])
        self.assertEqual("AGENTS.md", continuity["agent_instructions_path"])
        self.assertTrue(continuity["resume_before_work"])
        self.assertTrue(continuity["refresh_before_pull_request"])
        self.assertNotIn("objective", continuity)

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
        self.assertIn("provisional = true", rendered)
        self.assertIn('revision-kind = "git-commit"', rendered)
        self.assertIn(f'revision = "{SOURCE_REVISION}"', rendered)
        self.assertIn(context.MARKER, rendered)

    def test_context_schema_is_valid_json(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository-context.v2.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema", schema["$schema"]
        )
        self.assertEqual("2.0.0", schema["properties"]["schema_version"]["const"])
        self.assertIn("continuity", schema["required"])

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
        self.assertTrue(contract["provisional"])
        self.assertTrue((ROOT / contract["source"]["path"]).is_file())

    def test_deprecated_v1_contract_remains_available_for_pinned_consumers(self) -> None:
        legacy_path = ROOT / "contracts" / "repository-context.v1.toml"
        legacy_bytes = legacy_path.read_bytes()
        legacy = tomllib.loads(legacy_bytes.decode("utf-8"))
        self.assertEqual("1.0.0", legacy["version"])
        self.assertFalse(legacy["provisional"])
        self.assertEqual(
            ["agent-instructions", "ecosystem-context"],
            [item["id"] for item in legacy["requirements"]],
        )
        self.assertEqual(
            "85d670c094b5e72360de684bfa5b9d5332caa2868565285ddc8216f80e489cf8",
            hashlib.sha256(legacy_bytes).hexdigest(),
        )

    def test_generated_sanctuary_projection_is_current(self) -> None:
        contract = tomllib.loads(
            (ROOT / "contracts" / "repository-context.toml").read_text(
                encoding="utf-8"
            )
        )
        source_revision = contract["source"]["revision"]
        expected = context.render_markdown(
            context.build_context(
                self.catalog,
                self.policy,
                "egohygiene/sanctuary",
                source_revision,
            )
        )
        self.assertEqual(
            expected,
            (ROOT / "docs" / "generated" / "contexts" / "sanctuary.md").read_text(
                encoding="utf-8"
            ),
        )


if __name__ == "__main__":
    unittest.main()
