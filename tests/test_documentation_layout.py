"""Authored regression scenarios for the optional local documentation adapter.

These scenarios are unexecuted at the source-only policy checkpoint.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("documentation_layout", ROOT / "tools/documentation_layout.py")
assert SPEC is not None and SPEC.loader is not None
documentation_layout = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = documentation_layout
SPEC.loader.exec_module(documentation_layout)


class RepositoryDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.examples = json.loads((ROOT / "fixtures/repository-documentation/examples.json").read_text(encoding="utf-8"))
        cls.baseline = cls.examples["cases"][0]["input"]

    def test_self_contained_synthetic_dispositions(self) -> None:
        for example in self.examples["cases"]:
            with self.subTest(case=example["id"]):
                result = documentation_layout.assess(copy.deepcopy(example["input"]))
                self.assertEqual(example["expected_state"], result["state"])
                self.assertEqual(sorted(example["expected_codes"]), sorted(row["code"] for row in result["diagnostics"]))
                self.assertEqual("local-review-only", result["publication"])
                self.assertEqual("not-performed", result["qualification"]["aether_content_validation"])

    def test_profile_and_owner_inputs_remain_exact_byte_bound(self) -> None:
        profile = documentation_layout.profile()
        self.assertEqual("proposed", profile["status"])
        self.assertIsNone(profile["approval"])
        self.assertEqual("observe", profile["enforcement"])
        for owner in ("presentation", "continuity"):
            pin = profile["composes"][owner]
            for path_field, digest_field in (("path", "sha256"), ("helper", "helper_sha256")):
                self.assertEqual(pin[digest_field], hashlib.sha256((ROOT / pin[path_field]).read_bytes()).hexdigest())

    def test_nonpublic_payload_is_never_inspected_or_serialized(self) -> None:
        result = documentation_layout.assess({"visibility": "private", "payload": object()})
        self.assertEqual("unavailable", result["state"])
        self.assertEqual([{"code": "SOURCE_NOT_ADMITTED", "category": None}], result["diagnostics"])
        self.assertNotIn("payload", documentation_layout.encoded(result).decode("utf-8"))

    def test_truthy_wrong_types_cannot_supply_required_metadata(self) -> None:
        changes = [
            ("question", {"not": "text"}),
            ("update_path", ["not-text"]),
            ("source", {"repository": None, "revision": "a" * 40, "path": None}),
            ("provider_content", 1),
            ("imports", "AGENTS.md"),
        ]
        for field, value in changes:
            candidate = copy.deepcopy(self.baseline)
            candidate["documents"][0][field] = value
            with self.subTest(field=field), self.assertRaises((ValueError, TypeError)):
                documentation_layout.assess(candidate)
        candidate = copy.deepcopy(self.baseline)
        candidate["readme_mode"] = "rich-justified"
        candidate["readme_justification"] = {"not": "a justification"}
        with self.assertRaises((ValueError, TypeError)):
            documentation_layout.assess(candidate)

    def test_literal_paths_preserve_spaces_and_unicode_but_deny_escape(self) -> None:
        for path in ("docs/My Guide.md", "docs/évidence.md", "docs/日本語.md"):
            self.assertEqual(path, documentation_layout.safe_path(path))
        for path in ("../README.md", "docs/../README.md", "/README.md", "C:/README.md", "docs\\README.md",
                     "docs//README.md", "docs/", ".git/config", ".GIT/config", "docs/\x00name.md"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                documentation_layout.safe_path(path)

    def test_json_ambiguity_and_deep_input_are_not_review_evidence(self) -> None:
        for content in (b'{"visibility":"public","visibility":"private"}', b'{"x":NaN}',
                        b'{"x":1e999}', b'"\xff"', b'[' * 1000 + b'0' + b']' * 1000):
            with self.subTest(content=content[:40]), self.assertRaises((ValueError, UnicodeError, RecursionError)):
                documentation_layout.parse(content)

    def test_declared_symlink_cannot_satisfy_root_entry(self) -> None:
        candidate = copy.deepcopy(self.baseline)
        candidate["documents"][0]["file_kind"] = "symlink"
        result = documentation_layout.assess(candidate)
        self.assertIn({"code": "REGULAR_SOURCE_REQUIRED", "category": "readme"}, result["diagnostics"])
        self.assertEqual("review_required", result["state"])

    def test_missing_navigation_target_and_unknown_selection_remain_visible(self) -> None:
        candidate = copy.deepcopy(self.baseline)
        candidate["documents"] = [row for row in candidate["documents"] if row["id"] != "architecture-detail"]
        candidate["architecture_selected"] = None
        result = documentation_layout.assess(candidate)
        codes = {row["code"] for row in result["diagnostics"]}
        self.assertTrue({"CANONICAL_NAVIGATION_UNKNOWN", "NAVIGATION_TARGET_UNVERIFIED", "ARCHITECTURE_SELECTION_UNKNOWN"} <= codes)

    def test_consumer_file_paths_are_not_read(self) -> None:
        allowed = {ROOT / path for path in ("catalog/repository-documentation-profile.json",
                   "catalog/repository-presentation-profile.json", "tools/presentation.py",
                   "catalog/repository-continuity-policy.json", "tools/continuity.py")}
        original = Path.read_bytes

        def read_owned(path: Path) -> bytes:
            self.assertIn(path, allowed)
            return original(path)

        with patch.object(Path, "read_bytes", read_owned):
            result = documentation_layout.assess(copy.deepcopy(self.baseline))
        self.assertEqual("advisory", result["state"])


if __name__ == "__main__":
    unittest.main()
