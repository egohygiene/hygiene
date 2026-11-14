"""Qualify the existing proposed contract; no Git rewriting or tool activation."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("change_history", ROOT / "tools/change_history.py")
history = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(history)


class ChangeHistoryTests(unittest.TestCase):
    def value(self, message="fix(parser): 🐛 preserve empty values", context="commit", parents=1):
        return {"schema": history.INPUT_SCHEMA, "visibility": "public", "context": context,
                "message": message, "parent_count": parents}

    def analyze(self, message, context="commit", parents=1):
        return history.analyze(self.value(message, context, parents))

    def test_existing_fifteen_fixtures_execute_with_documented_expectation_semantics(self):
        examples = json.loads((ROOT / "fixtures/change-history/examples.json").read_text())
        self.assertEqual(15, len(examples["cases"]))
        for case in examples["cases"]:
            result = history.analyze(copy.deepcopy(case["input"]))
            for key, expected in case["expected"].items():
                with self.subTest(case=case["id"], field=key):
                    if key == "diagnostic": self.assertIn(expected, result["diagnostics"])
                    elif key == "identity_signature_dco": self.assertEqual(expected, result["qualification"][key])
                    else: self.assertEqual(expected, result[key])

    def test_all_twelve_type_emoji_pairs_and_cross_type_mismatches(self):
        types = history.policy()["types"]
        self.assertEqual(12, len(types))
        for row in types:
            footer = "\n\nReverts: " + "a" * 40 if row["type"] == "revert" else ""
            result = self.analyze(f"{row['type']}(api): {row['emoji']} preserve bounded behavior" + footer)
            self.assertEqual("valid", result["syntax"])
            self.assertEqual(row["release_hint"], result["release_hint"])
            for other in types:
                if other["type"] == row["type"]: continue
                result = self.analyze(f"{row['type']}(api): {other['emoji']} preserve bounded behavior" + footer)
                with self.subTest(type=row["type"], emoji=other["type"]):
                    self.assertIn("EMOJI_MISMATCH", result["diagnostics"])
                    self.assertEqual("review_required", result["release_hint"])

    def test_every_type_breaks_explicitly_and_reverts_still_require_net_effect_review(self):
        for row in history.policy()["types"]:
            for marker in ("bang", "BREAKING CHANGE", "BREAKING-CHANGE"):
                subject = f"{row['type']}(api){'!' if marker == 'bang' else ''}: {row['emoji']} replace bounded behavior"
                footers = []
                if marker != "bang": footers.append(marker + ": callers must migrate the fixture")
                if row["type"] == "revert": footers.append("Reverts: " + "a" * 40)
                message = subject + ("\n\n" + "\n".join(footers) if footers else "")
                result = self.analyze(message)
                with self.subTest(type=row["type"], marker=marker):
                    self.assertEqual("valid", result["syntax"])
                    self.assertTrue(result["breaking"])
                    self.assertEqual("review_required" if row["type"] == "revert" else "major", result["release_hint"])

    def test_breaking_markers_outside_final_trailer_block_cannot_disappear(self):
        for body in ("BREAKING CHANGE: migrate\n\nLater prose.", "Prose\nBREAKING CHANGE: migrate", "BREAKING CHANGE: migrate\nnot indented"):
            result = self.analyze("docs(api): 📝 describe bounded migration\n\n" + body)
            self.assertEqual("invalid", result["syntax"])
            self.assertEqual("review_required", result["release_hint"])
            self.assertTrue({"BREAKING_MARKER_LOCATION", "TRAILER_CONTINUATION"} & set(result["diagnostics"]))

    def test_footer_continuations_and_unknown_trailers_have_bounded_meaning(self):
        result = self.analyze("feat(api): ✨ replace bounded behavior\n\nBREAKING CHANGE: migrate\n continued rationale\nADR-Ref: egohygiene/example#ADR-0001")
        self.assertEqual("valid", result["syntax"])
        self.assertEqual("major", result["release_hint"])
        result = self.analyze("fix(api): 🐛 preserve values\n\nUnregistered-Approval: synthetic")
        self.assertIn("TRAILER_UNREGISTERED", result["diagnostics"])
        self.assertEqual("review_required", result["release_hint"])

    def test_revert_requires_one_full_lowercase_target(self):
        for footers in ("", "Reverts: abc", "Reverts: " + "A" * 40, "Reverts: " + "a" * 40 + "\nReverts: " + "b" * 40):
            result = self.analyze("revert(api): ⏪ restore bounded behavior" + ("\n\n" + footers if footers else ""))
            with self.subTest(footers=footers):
                self.assertIn("REVERT_TARGET_REQUIRED", result["diagnostics"])
                self.assertEqual("review_required", result["release_hint"])

    def test_nonpublic_payload_is_not_inspected_and_never_becomes_evidence(self):
        for visibility in ("private", "internal", "unknown", None):
            result = history.analyze({"visibility": visibility, "message": object(), "parent_count": object()})
            self.assertEqual("not_admitted", result["syntax"])
            self.assertEqual(["SOURCE_NOT_ADMITTED"], result["diagnostics"])
            self.assertEqual("none", result["release_hint"])

    def test_no_message_scope_actor_or_trailer_values_escape_output(self):
        message = "fix(sensitive-fixture-scope): 🐛 preserve synthetic-message-value\n\nPrivate fixture narrative.\n\nCo-authored-by: SYNTHETIC-ACTOR-VALUE\nSigned-off-by: SYNTHETIC-SIGNOFF-VALUE\nRelease-As: 99.88.77"
        result = self.analyze(message)
        serialized = history.encoded(result).decode()
        for value in ("sensitive-fixture-scope", "synthetic-message-value", "Private fixture narrative", "SYNTHETIC-ACTOR-VALUE", "SYNTHETIC-SIGNOFF-VALUE", "99.88.77", hashlib.sha256(message.encode()).hexdigest()):
            self.assertNotIn(value, serialized)
        self.assertEqual("not-verified", result["qualification"]["identity_signature_dco"])
        self.assertEqual("not-inferred", result["qualification"]["human_approval"])
        self.assertEqual("repository-aether-authority", result["qualification"]["release_version"])
        self.assertEqual("patch", result["release_hint"])

    def test_merge_parent_metadata_never_stands_in_for_constituent_semantics(self):
        result = self.analyze("arbitrary provider merge subject", "merge", 2)
        self.assertEqual("context_only", result["syntax"])
        self.assertEqual("review_required", result["release_hint"])
        self.assertIsNone(result["type"])
        with self.assertRaises(ValueError): self.analyze("merge", "merge", 1)
        result = self.analyze("fix(api): 🐛 preserve values", parents=2)
        self.assertIn("MERGE_CONTEXT_REQUIRED", result["diagnostics"])

    def test_bot_dependency_generated_contexts_do_not_waive_grammar(self):
        for context in ("bot", "dependency", "generated"):
            result = self.analyze("fix(deps): 🐛 preserve bounded behavior", context)
            self.assertEqual("valid", result["syntax"])
            self.assertEqual("patch", result["release_hint"])
            result = self.analyze("automated update", context)
            self.assertEqual("invalid", result["syntax"])
            self.assertEqual("review_required", result["release_hint"])

    def test_release_context_prevents_release_metadata_bump_loops(self):
        result = self.analyze("chore(release): 🔧 prepare bounded release metadata", "release")
        self.assertEqual("valid", result["syntax"])
        self.assertEqual("none", result["release_hint"])
        for message in ("feat(release): ✨ prepare metadata", "chore(repo): 🔧 prepare metadata", "chore(release)!: 🔧 prepare metadata"):
            result = self.analyze(message, "release")
            self.assertIn("RELEASE_CONTEXT", result["diagnostics"])
            self.assertEqual("review_required", result["release_hint"])

    def test_pr_titles_are_single_line_and_never_normalized_to_success(self):
        for ending in ("\n", "\r\n", "\n\nbody"):
            result = self.analyze("fix(api): 🐛 preserve values" + ending, "pr_title")
            self.assertEqual("invalid", result["syntax"])
            self.assertIn("PR_TITLE_MULTILINE", result["diagnostics"])
        with self.assertRaises(ValueError): self.analyze("fix(api): 🐛 preserve\rvalues", "pr_title")

    def test_unicode_scope_placeholder_and_subject_bounds_refused(self):
        for scope in ("a/../b", "a//b", "a/./b", "scope_", "scope-", "scope."):
            result = self.analyze(f"fix({scope}): 🐛 preserve values")
            self.assertIn("SCOPE_SHAPE", result["diagnostics"])
        for description in history.policy()["subject"]["placeholder_descriptions"]:
            result = self.analyze("fix(api): 🐛 " + description)
            self.assertIn("PLACEHOLDER", result["diagnostics"])
        self.assertIn("SUBJECT_UNICODE", self.analyze("fix(api): 🐛 preserve e\u0301vidence")["diagnostics"])
        self.assertIn("EMOJI_MISMATCH", self.analyze("perf(api): ⚡ preserve values")["diagnostics"])
        self.assertIn("SUBJECT_LENGTH", self.analyze("fix(api): 🐛 " + "x" * 100)["diagnostics"])

    def test_input_types_byte_bounds_and_ambiguous_json_refused(self):
        for parents in (True, "1", -1, 33):
            with self.assertRaises(ValueError): history.analyze(self.value(parents=parents))
        with self.assertRaises(ValueError): self.analyze("fix(api): 🐛 preserve values\n\n" + "é" * 32768)
        for raw in (b'{"visibility":"public","visibility":"private"}', b'{"x":NaN}', b'{"x":1e999}', b'"\xff"', b'[' * 1000 + b'0' + b']' * 1000):
            with self.subTest(raw=raw[:40]), self.assertRaises((ValueError, UnicodeError, RecursionError)):
                history.parse(raw)

    def test_file_reader_refuses_symlinks_oversized_sources_directories_and_pipes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            valid = root / "input.json"
            raw = json.dumps(self.value()).encode()
            valid.write_bytes(raw)
            self.assertEqual(raw, history.read_input(valid))
            (root / "leaf.json").symlink_to(valid)
            (root / "alias").symlink_to(root, target_is_directory=True)
            (root / "large.json").write_bytes(b"x" * 262145)
            os.mkfifo(root / "pipe")
            for path in (root / "leaf.json", root / "alias/input.json", root / "large.json", root, root / "pipe"):
                with self.subTest(kind=path.name), self.assertRaises((ValueError, OSError)):
                    history.read_input(path)

    def test_real_cli_exit_codes_and_neutral_diagnostics(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "input.json"
            for raw, exit_code, syntax in (
                (json.dumps(self.value()).encode(), 0, "valid"),
                (json.dumps(self.value("fix(api): ✨ preserve values")).encode(), 1, "invalid"),
                (b'{"visibility":"private","message":"SYNTHETIC-PROTECTED-PAYLOAD"}', 0, "not_admitted"),
                (b'{"schema":', 2, None),
            ):
                source.write_bytes(raw)
                result = subprocess.run([sys.executable, "-I", str(ROOT / "tools/change_history.py"), str(source)],
                                        capture_output=True, timeout=5, check=False)
                self.assertEqual(exit_code, result.returncode)
                self.assertNotIn(b"SYNTHETIC-PROTECTED-PAYLOAD", result.stdout + result.stderr)
                self.assertNotIn(str(source).encode(), result.stdout + result.stderr)
                if syntax is not None:
                    self.assertEqual(syntax, json.loads(result.stdout)["syntax"])
                else:
                    self.assertEqual(b"", result.stdout)
                    self.assertEqual(b"Change-history source/profile unavailable or incompatible\n", result.stderr)

    def test_original_public_migration_map_is_complete_without_inventing_restricted_mapping(self):
        mapping = json.loads((ROOT / "fixtures/change-history/migration-map.json").read_text())
        self.assertEqual("2026-11-12T05:41:28Z", mapping["observed_at"])
        self.assertEqual({"egohygiene/egolint", "egohygiene/empathy", "egohygiene/renderflow", "egohygiene/reflector"},
                         {row["repository"] for row in mapping["sources"]})
        core = {row["type"] for row in history.policy()["types"]}
        for source in mapping["sources"]:
            actual = source["selected_type_names"]
            dispositions = source["type_disposition"]
            self.assertEqual(len(actual), len(set(actual)))
            self.assertEqual(sorted(actual), sorted(row["source_type"] for row in dispositions))
            for row in dispositions:
                self.assertEqual(row["source_type"] if row["source_type"] in core else None, row["target_core"])
                if row["target_core"] is None: self.assertEqual("review-required-no-silent-map", row["state"])
        self.assertIn("independently authorized local review", mapping["restricted_input_boundary"])
        self.assertIn("Private/local mapping and actual release effects remain independently unverified", mapping["implementation_gaps"])

    def test_policy_bytes_and_proposed_lifecycle_are_preserved(self):
        raw = (ROOT / "catalog/change-history-policy.json").read_bytes()
        self.assertEqual(history.POLICY_SHA256, hashlib.sha256(raw).hexdigest())
        policy = history.policy()
        self.assertEqual("proposed", policy["status"])
        self.assertIsNone(policy["approval"])
        self.assertEqual("observe", policy["enforcement"])
        original = history.read_input
        def only_policy(path):
            self.assertEqual(ROOT / "catalog/change-history-policy.json", path)
            return original(path)
        with patch.object(history, "read_input", only_policy):
            self.analyze("fix(api): 🐛 preserve values")


if __name__ == "__main__":
    unittest.main()
