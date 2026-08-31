from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import releases  # noqa: E402


class RepositoryReleasePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = releases.load_json(
            ROOT / "catalog" / "repository-release-policy.json"
        )

    def test_contract_schema_is_a_json_schema_document(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "repository-release-policy.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
        self.assertEqual(
            "https://egohygiene.io/schemas/hygiene/repository-release-policy.v1.schema.json",
            schema["$id"],
        )

    def test_checked_in_profile_is_valid_and_pins_aether_immutably(self) -> None:
        self.assertEqual([], releases.validate_profile(self.profile))
        self.assertEqual(releases.AETHER_REVISION, self.profile["aether_contract"]["revision"])
        self.assertNotIn("main", self.profile["aether_contract"]["authoring_skill"]["url"])

    def test_profile_is_registered_as_a_proposed_hygiene_contract(self) -> None:
        contracts = releases.load_json(ROOT / "catalog" / "contracts.yaml")["contracts"]
        registered = {contract["id"]: contract for contract in contracts}
        contract = registered[releases.POLICY_SCHEMA]
        self.assertEqual("egohygiene/hygiene", contract["owner"])
        self.assertEqual("proposed", contract["status"])
        self.assertEqual("schemas/repository-release-policy.v1.schema.json", contract["source"])

    def test_mutable_or_wrong_aether_pin_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.profile)
        candidate["aether_contract"]["revision"] = "a" * 40
        errors = releases.validate_profile(candidate)
        self.assertIn(
            "profile.aether_contract.revision must pin the Aether #61 merge commit",
            errors,
        )

    def test_archived_and_advisory_resolution_remain_honest(self) -> None:
        archived = releases.resolve_requirements(
            self.profile, "contract", "archived", "public", "required"
        )
        self.assertEqual("not_applicable", archived["requirements"]["task_handoffs"])
        self.assertEqual("required", archived["requirements"]["changelog"])
        advisory = releases.resolve_requirements(
            self.profile, "cli-library", "active", "public", "advisory"
        )
        self.assertEqual("advisory", advisory["requirements"]["aether_declaration"])
        self.assertEqual("advisory", advisory["requirements"]["version_authority"])

    def test_profile_examples_cover_required_repository_classes(self) -> None:
        examples = {example["id"]: example for example in self.profile["examples"]}
        self.assertEqual(releases.EXAMPLE_IDS, set(examples))
        self.assertEqual("advisory", examples["legacy-advisory-migration"]["adoption_state"])
        self.assertEqual("archived", examples["archived-repository"]["lifecycle"])
        self.assertEqual("private", examples["private-repository"]["visibility"])

    def test_hygiene_dogfood_declaration_and_handoffs_are_valid(self) -> None:
        declaration = releases.validate_declaration(ROOT, self.profile)
        self.assertEqual("egohygiene/hygiene", declaration["repository"]["id"])
        self.assertEqual("contract", declaration["repository"]["release_profile"])
        plan = releases.render_plan(declaration, self.profile)
        self.assertIn("Create or review a release PR", plan)
        self.assertNotIn("publish a package", plan.lower())

    def test_workflow_is_manual_and_task_handoffs_are_non_publishing(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release-policy.yml").read_text(
            encoding="utf-8"
        )
        taskfile = (ROOT / ".tasks" / "release.yml").read_text(encoding="utf-8").lower()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("\n  push:", workflow)
        self.assertIn("release:plan:", taskfile)
        self.assertIn("release:prepare:", taskfile)
        self.assertIn("release:verify:", taskfile)
        self.assertIn("release:publish:", taskfile)
        self.assertNotIn("gh release", taskfile)
        self.assertNotIn("git tag", taskfile)


if __name__ == "__main__":
    unittest.main()
