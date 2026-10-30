from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "check_contracts.py"


class ContractRegressionGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(RUNNER.is_file(), "the complete contract gate is missing")
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repository = Path(self.temporary.name) / "repository"
        shutil.copytree(
            ROOT,
            self.repository,
            ignore=shutil.ignore_patterns(
                ".git", ".cache", "__pycache__", "*.pyc", "dist",
                "test_contract_regression.py",
            ),
        )

    def run_gate(self) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            [sys.executable, "-I", "tools/check_contracts.py"],
            cwd=self.repository,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=90,
            check=False,
        )
        report = self.repository / ".cache" / "contract-regression" / "result.json"
        self.assertTrue(report.is_file(), result.stdout)
        return result, json.loads(report.read_text(encoding="utf-8"))

    def check_result(self, report: dict, name: str) -> dict:
        return next(check for check in report["checks"] if check["id"] == name)

    def test_valid_source_discovers_new_tests_and_records_real_skips(self) -> None:
        (self.repository / "tests" / "test_new_family.py").write_text(
            "import unittest\n"
            "class NewFamily(unittest.TestCase):\n"
            "    def test_pass(self): self.assertEqual(2, 2)\n"
            "    @unittest.skip('explicit fixture skip')\n"
            "    def test_skip(self): pass\n",
            encoding="utf-8",
        )
        result, report = self.run_gate()
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual("passed", report["status"])
        self.assertTrue(report["complete"])
        suite = self.check_result(report, "unit-tests")
        self.assertGreaterEqual(suite["tests"]["run"], 196)
        self.assertEqual(1, suite["tests"]["skipped"])
        self.assertIn("test_new_family.py", report["test_modules"])
        self.assertEqual(
            {path.name for path in (self.repository / "tests").glob("test_*.py")},
            set(report["test_modules"]),
        )
        self.assertIn("skipped=1", result.stdout)

    def test_invalid_catalog_fails_the_actual_gate(self) -> None:
        target = self.repository / "catalog" / "repositories.yaml"
        value = json.loads(target.read_text(encoding="utf-8"))
        value["repository_count"] += 1
        target.write_text(json.dumps(value), encoding="utf-8")
        result, report = self.run_gate()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("failed", report["status"])
        self.assertEqual("failed", self.check_result(report, "catalog")["status"])
        self.assertTrue(report["complete"])

    def test_invalid_profile_fails_the_actual_gate(self) -> None:
        target = self.repository / "catalog" / "repository-continuity-policy.json"
        value = json.loads(target.read_text(encoding="utf-8"))
        value["version"] = "0.0.0-invalid"
        target.write_text(json.dumps(value), encoding="utf-8")
        result, report = self.run_gate()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            "failed", self.check_result(report, "continuity-profile")["status"]
        )

    def test_stale_generated_output_fails_while_unit_tests_still_pass(self) -> None:
        target = self.repository / "docs" / "generated" / "DEPENDENCY_BOUNDARIES.md"
        target.write_text(target.read_text(encoding="utf-8") + "stale\n", encoding="utf-8")
        result, report = self.run_gate()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("passed", self.check_result(report, "unit-tests")["status"])
        self.assertEqual(
            "failed", self.check_result(report, "boundary-generated")["status"]
        )

    def test_failure_in_a_new_test_family_keeps_the_gate_failed(self) -> None:
        (self.repository / "tests" / "test_new_failure.py").write_text(
            "import unittest\n"
            "class NewFailure(unittest.TestCase):\n"
            "    def test_failure(self): self.fail('synthetic gate control')\n",
            encoding="utf-8",
        )
        result, report = self.run_gate()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("failed", self.check_result(report, "unit-tests")["status"])
        self.assertEqual(1, self.check_result(report, "unit-tests")["tests"]["failures"])
        self.assertEqual("passed", self.check_result(report, "catalog")["status"])

    def test_empty_test_discovery_cannot_be_a_success(self) -> None:
        shutil.rmtree(self.repository / "tests")
        (self.repository / "tests").mkdir()
        result, report = self.run_gate()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("failed", self.check_result(report, "unit-tests")["status"])
        self.assertEqual(0, self.check_result(report, "unit-tests")["tests"]["run"])

    def test_retained_command_diagnostics_are_bounded(self) -> None:
        (self.repository / "tools" / "catalog.py").write_text(
            "import sys\nprint('x' * (1024 * 1024))\nsys.exit(1)\n", encoding="utf-8"
        )
        result, report = self.run_gate()
        self.assertNotEqual(0, result.returncode)
        check = self.check_result(report, "catalog")
        self.assertTrue(check["log_truncated"])
        log = self.repository / ".cache" / "contract-regression" / check["log"]
        self.assertLessEqual(log.stat().st_size, 256 * 1024)


if __name__ == "__main__":
    unittest.main()
