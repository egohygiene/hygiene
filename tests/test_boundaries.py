from __future__ import annotations

import copy
import json
import subprocess
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
        self.assertEqual(27, len(self.register["relationships"]))

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
        candidate["relationships"][0]["contract_status"] = "active"
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
        candidate["relationships"][0]["contract_status"] = "active"
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
        self.assertIn("RELATIONSHIP-026", first)


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
                    "jobs:\n  check:\n    steps:\n"
                    "      - uses: egohygiene/relay/actions/test@main\n"
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
                    "jobs:\n  check:\n    steps:\n"
                    "      - uses: egohygiene/relay/actions/test@"
                    "2d9e7c4ff5de4f832d28b3ce105b2a4da8382dd7\n"
                )
            }
        )
        self.assertEqual([], findings)

    def test_mutable_uses_quote_and_workflow_forms_are_equivalent(self) -> None:
        for reference in (
            "egohygiene/relay/actions/test@main",
            "egohygiene/relay/.github/workflows/check.yml@master",
        ):
            prefix = (
                "jobs:\n  check:\n    steps:\n      - name: Check\n        "
                if "/actions/" in reference
                else "jobs:\n  check:\n    "
            )
            for quote in ("", "'", '"'):
                with self.subTest(reference=reference, quote=quote):
                    findings = self.scan(
                        {".github/workflows/check.yml": (
                            f"{prefix}uses :  {quote}{reference}{quote}  # pinned later\n"
                        )}
                    )
                    self.assertEqual(
                        [boundaries.Finding(
                            "BOUNDARY-002", ".github/workflows/check.yml",
                            prefix.count("\n") + 1,
                            "mutable default-branch dependency on egohygiene/relay",
                        )],
                        findings,
                    )

    def test_pinned_and_versioned_uses_remain_allowed(self) -> None:
        for ref in ("2d9e7c4ff5de4f832d28b3ce105b2a4da8382dd7", "v1.5.0"):
            for quote in ("", "'", '"'):
                with self.subTest(ref=ref, quote=quote):
                    self.assertEqual([], self.scan({".github/workflows/check.yaml": (
                        "jobs:\n  check:\n    steps:\n"
                        f"      - uses: {quote}egohygiene/relay/actions/test@{ref}{quote}\n"
                    )}))

    def test_composite_action_uses_values_are_scanned(self) -> None:
        for filename in ("action.yml", ".github/actions/check/action.yaml"):
            for quote in ("", "'", '"'):
                with self.subTest(filename=filename, quote=quote):
                    findings = self.scan({filename: (
                        "runs:\n  using: composite\n  steps:\n"
                        f"    - uses: {quote}egohygiene/relay/actions/test@trunk{quote}\n"
                    )})
                    self.assertEqual(1, len(findings))
                    self.assertEqual(("BOUNDARY-002", filename, 4), (
                        findings[0].rule, findings[0].path, findings[0].line
                    ))

    def test_public_cli_preserves_quote_rule_path_line_and_exit(self) -> None:
        forms = (
            (".github/workflows/check.yml", "jobs:\n  check:\n    ",
             "egohygiene/relay/.github/workflows/check.yml@develop"),
            (".github/workflows/check.yaml", "jobs:\n  check:\n    steps:\n      - ",
             "egohygiene/relay/actions/test@main"),
            (".github/actions/check/action.yml", "runs:\n  using: composite\n  steps:\n    - ",
             "egohygiene/relay/actions/test@trunk"),
        )
        for filename, prefix, reference in forms:
            for quote in ("", "'", '"'):
                with self.subTest(filename=filename, quote=quote), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    path = root / filename
                    path.parent.mkdir(parents=True)
                    path.write_text(
                        f"{prefix}uses: {quote}{reference}{quote} # note\n",
                        encoding="utf-8",
                    )
                    arguments = [
                        sys.executable, "-I", str(ROOT / "tools/boundaries.py"),
                        "scan", "--repository-root", str(root),
                        "--repository", "egohygiene/hygiene",
                    ]
                    result = subprocess.run(
                        [*arguments, "--format", "json"], cwd=ROOT,
                        capture_output=True, text=True, check=False, timeout=10,
                    )
                    self.assertEqual(1, result.returncode, result.stderr)
                    line = prefix.count("\n") + 1
                    self.assertEqual([{
                        "rule": "BOUNDARY-002", "path": filename, "line": line,
                        "message": "mutable default-branch dependency on egohygiene/relay",
                    }], json.loads(result.stdout))
                    result = subprocess.run(
                        arguments, cwd=ROOT, capture_output=True, text=True,
                        check=False, timeout=10,
                    )
                    self.assertEqual(1, result.returncode)
                    self.assertIn(f"BOUNDARY-002 {filename}:{line}:", result.stderr)

    def test_comments_strings_and_non_action_surfaces_are_not_uses(self) -> None:
        reference = "egohygiene/relay/actions/test@main"
        self.assertEqual([], self.scan({
            "README.md": f"uses: '{reference}'\n[Source](https://github.com/egohygiene/relay/tree/main)\n",
            "config/tool.yaml": f"uses: {reference}\n",
            "config/data.json": json.dumps({"uses": reference}),
            ".github/workflows/check.yml": (
                f"# uses: {reference}\n"
                "jobs:\n  check:\n    env:\n"
                f"      uses: {reference}\n"
                "    steps:\n"
                f"      - run: echo 'uses: {reference}'\n"
                "      - run: |\n"
                f"          uses: {reference}\n"
                "      - run: >-\n"
                f"          uses: {reference}\n"
                "      - run: '\n"
                f"          uses: {reference}\n"
                "        '\n"
                '      - run: "\n'
                f"          uses: {reference}\n"
                '        "\n'
                "      - env:\n"
                f"          uses: {reference}\n"
                "        run: true\n"
            ),
        }))

    def test_uses_after_run_scalar_and_separate_sequence_item_is_found(self) -> None:
        findings = self.scan({".github/workflows/check.yml": (
            "jobs:\n  check:\n    steps:\n      - run: |\n"
            "          echo harmless\n      - name: Next\n"
            "        uses: 'egohygiene/relay/actions/test@HEAD'\n"
        )})
        self.assertEqual(1, len(findings))
        self.assertEqual(7, findings[0].line)

    def test_quoted_keys_and_json_compatible_escapes_are_supported(self) -> None:
        findings = self.scan({".github/workflows/check.yml": (
            "jobs:\n  check:\n    steps:\n      -\n"
            '        "uses": "egohygiene/relay/actions/test@\\u006dain" # note\n'
        )})
        self.assertEqual(1, len(findings))
        self.assertEqual(5, findings[0].line)

    def test_unsupported_uses_shapes_do_not_fabricate_a_violation(self) -> None:
        self.assertEqual([], self.scan({".github/workflows/check.yml": (
            "jobs:\n  check:\n    steps:\n"
            "      - uses: ${{ inputs.action }}\n"
            "      - uses: &action egohygiene/relay/actions/test@main\n"
            "      - uses: *action\n"
            "      - uses: |\n"
            "          egohygiene/relay/actions/test@main\n"
            "      - uses:egohygiene/relay/actions/test@main\n"
            "      - run: true\n"
        )}))

    def test_indentless_steps_and_sequence_separator_whitespace(self) -> None:
        for prefix in ("jobs:\n  check:\n    steps:\n", "runs:\n  steps:\n"):
            for separator in (" ", "   ", "\t"):
                with self.subTest(prefix=prefix, separator=separator):
                    indent = "    " if prefix.startswith("jobs") else "  "
                    findings = self.scan({
                        "action.yml" if prefix.startswith("runs") else ".github/workflows/check.yml": (
                            prefix
                            + f"{indent}-{separator}uses: 'egohygiene/relay/actions/test@main'\n"
                        )
                    })
                    self.assertEqual(1, len(findings))

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
