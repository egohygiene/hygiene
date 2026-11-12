from __future__ import annotations

import copy
import contextlib
import io
import json
import os
import shutil
import shlex
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import releases  # noqa: E402


class RepositoryReleasePolicyTests(unittest.TestCase):
    def owner_source(self) -> Path:
        source = Path(os.environ.get("HYGIENE_AETHER_SOURCE", str(ROOT / ".cache/release/aether")))
        if not source.is_dir():
            self.skipTest("Exact Aether source unavailable; native declaration qualification is not executed")
        return source

    def copy_baseline(self, target: Path) -> None:
        for relative in [".egohygiene/release.json", "CHANGELOG.md", "Taskfile.yml", "AGENTS.md", ".tasks/release.yml", ".github/workflows/release-policy.yml", "docs/ecosystem/REPOSITORY_RELEASE.md", "catalog/repository-release-policy.json"]:
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, path)

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
        declaration, evidence = releases.validate_declaration_with_evidence(ROOT, self.profile, aether_source=self.owner_source())
        self.assertEqual("egohygiene/hygiene", declaration["repository"]["id"])
        self.assertEqual("contract", declaration["repository"]["release_profile"])
        plan = releases.render_plan(declaration, self.profile, evidence)
        self.assertIn("Create or review a release PR", plan)
        self.assertNotIn("publish a package", plan.lower())
        self.assertEqual("passed", evidence["status"])
        self.assertEqual(releases.AETHER_REVISION, evidence["owner"]["revision"])
        self.assertEqual("jsonschema.Draft202012Validator", evidence["owner"]["engine"])
        self.assertEqual(plan, releases.render_plan(declaration, self.profile, evidence))

    def test_manual_trigger_structure_handles_flow_quotes_comments_and_duplicates(self) -> None:
        valid = [
            "on:\n  workflow_dispatch:\n",
            "'on': {workflow_dispatch: null}\n",
            '"on": ["workflow_dispatch"]\n',
            "on: workflow_dispatch\n# push: {branches: [main]}\n",
            "on: {workflow_dispatch: {inputs: {tag: {required: true}}}}\n",
        ]
        invalid = [
            "on:\n  workflow_dispatch:\n  push:\n",
            "on: {workflow_dispatch: null, push: {branches: [main]}}\n",
            "on: [workflow_dispatch, pull_request]\n",
            "on: push\n# workflow_dispatch:\n",
            'name: "workflow_dispatch:"\n# on:\n#   workflow_dispatch:\n',
            "on: workflow_dispatch\non: push\n",
            "on: {workflow_dispatch: null, workflow_dispatch: null}\n",
        ]
        for text in valid:
            with self.subTest(valid=text):
                releases._manual_workflow(text)
        for text in invalid:
            with self.subTest(invalid=text), self.assertRaises(ValueError):
                releases._manual_workflow(text)

    def test_task_names_are_structural_and_comment_tokens_cannot_fabricate_handoffs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            taskfile = root / "Taskfile.yml"
            taskfile.write_text('version: "3"\ntasks:\n  check: {cmds: [true]}\n# release:plan:\n# release:prepare:\n# release:verify:\n# release:publish:\n')
            self.assertEqual({"check"}, releases._task_handoff_names(root, taskfile))

    def test_schema_invalid_and_duplicate_required_data_fail_through_native_composition(self) -> None:
        source = self.owner_source()
        for mutation in ["wrong-task", "empty-authority", "unknown-field", "duplicate-json"]:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.copy_baseline(root)
                path = root / ".egohygiene/release.json"
                declaration = json.loads(path.read_text())
                if mutation == "wrong-task":
                    declaration["automation"]["tasks"]["plan"] = "release:wrong"
                elif mutation == "empty-authority":
                    declaration["components"][0]["version_authority"] = {}
                elif mutation == "unknown-field":
                    declaration["undeclared"] = True
                if mutation == "duplicate-json":
                    path.write_text(path.read_text().replace('"schema_version":', '"schema_version": "ignored", "schema_version":', 1))
                else:
                    path.write_text(json.dumps(declaration))
                with self.assertRaises(ValueError):
                    releases.validate_declaration_with_evidence(root, self.profile, aether_source=source)

    def test_missing_owner_source_is_explicit_unavailable_and_cli_is_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            with self.assertRaises(releases.OwnerValidationUnavailable):
                releases.validate_declaration(ROOT, self.profile, aether_source=missing)
            output, error = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                status = releases.main(["--profile", str(ROOT / "catalog/repository-release-policy.json"), "validate-declaration", "--repository", str(ROOT), "--aether-source", str(missing), "--format", "json"])
            self.assertNotEqual(0, status)
            self.assertEqual("", output.getvalue())
            self.assertIn("validation unavailable", error.getvalue())

    def test_plan_without_a_validation_receipt_does_not_claim_owner_success(self) -> None:
        declaration = releases.load_json(ROOT / ".egohygiene/release.json")
        plan = json.loads(releases.render_plan(declaration, self.profile))
        self.assertEqual("unavailable", plan["validation"]["status"])

    def test_owner_fallback_cannot_be_reported_as_full_validation(self) -> None:
        source = self.owner_source()
        with mock.patch.dict(sys.modules, {"jsonschema": None}):
            with self.assertRaises(releases.OwnerValidationUnavailable):
                releases.validate_declaration(ROOT, self.profile, aether_source=source)

    def test_modified_owner_payload_is_rejected_before_execution(self) -> None:
        source = self.owner_source()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            lock = releases.load_json(ROOT / "tools/release-owner.lock.json")
            for relative in lock["files"]:
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / relative, path)
            validator = target / releases.OWNER_VALIDATOR
            validator.write_bytes(validator.read_bytes() + b"\n# harmless modified payload\n")
            with self.assertRaises(releases.OwnerValidationUnavailable):
                releases.validate_declaration(ROOT, self.profile, aether_source=target)

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
        parsed = releases._yaml_mapping(taskfile, "release Taskfile")["tasks"]
        for name in ["release:plan", "release:prepare", "release:verify"]:
            command = shlex.split(parsed[name]["cmds"][0])
            self.assertIn("validate-declaration", command)
            self.assertEqual(".cache/release/aether", command[command.index("--aether-source") + 1])
        self.assertEqual("release:verify", parsed["release:publish"]["cmds"][0]["task"])
        releases._manual_workflow(workflow)


if __name__ == "__main__":
    unittest.main()
