# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Check immutable transport, source admission and actual recovery boundaries."""

from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("hygiene_publication", ROOT / "tools/publication.py")
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)
REVISION = "1" * 40


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.site = self.root / "site"
        publication.shell(self.site, REVISION)
        # Transport fixture only: it never claims to be a semantic Relay build.
        for relative in ("intelligence/index.html", "intelligence/decisions/index.html",
                         "intelligence/egohygiene.png", "intelligence/site.css"):
            publication.write(self.site / relative, b"fixture\n")
        publication.write(self.site / "intelligence/build-manifest.json", publication.encoded({
            "consumer": {"repository": "egohygiene/hygiene", "revision": REVISION},
            "generator": {"revision": publication.config()["relay_revision"]},
        }))
        self.manifest = publication.seal(self.site, REVISION)

    def report(self):
        return {"schema_version": "relay.repository-architecture-validation-result/v1",
                "repository": {"id": "egohygiene/hygiene", "visibility": "public", "represented_revision": REVISION},
                "coverage": {"architecture-records": "passed"},
                "bounds": {"scan_truncated": False, "findings_truncated": False}}

    def test_only_explicit_passed_complete_same_source_adr_coverage_admits(self):
        self.assertTrue(publication.admit(self.report(), REVISION))
        for status in ("failed", "partial", "unavailable", "not-applicable"):
            report = self.report()
            report["coverage"]["architecture-records"] = status
            self.assertFalse(publication.admit(report, REVISION))
        for bound in ("scan_truncated", "findings_truncated"):
            report = self.report()
            report["bounds"][bound] = True
            self.assertFalse(publication.admit(report, REVISION))
        with self.assertRaises(ValueError):
            publication.admit(self.report(), "2" * 40)
        report = self.report()
        report["repository"]["visibility"] = "private"
        with self.assertRaises(ValueError):
            publication.admit(report, REVISION)

    def test_shell_has_source_brand_favicon_and_canonical_aliases(self):
        root = (self.site / "index.html").read_text()
        for expected in ("Skip to content", "Repository source on GitHub", "/intelligence/egohygiene.png", REVISION):
            self.assertIn(expected, root)
        for alias in publication.config()["aliases"]:
            html = (self.site / alias["route"].strip("/") / "index.html").read_text()
            self.assertIn('rel="canonical"', html)
            self.assertIn('url=' + alias["target"], html)
            self.assertIn('href="' + alias["target"] + '"', html)
        with self.assertRaises(ValueError):
            publication.shell(self.site, REVISION)

    def test_handoff_rejects_changed_missing_added_symlink_or_wrong_revision(self):
        self.assertEqual(publication.check(self.site, REVISION), self.manifest)
        path = self.site / "intelligence/site.css"
        original = path.read_bytes()
        path.write_bytes(b"changed")
        with self.assertRaises(ValueError):
            publication.check(self.site, REVISION)
        path.unlink()
        with self.assertRaises(ValueError):
            publication.check(self.site, REVISION)
        path.write_bytes(original)
        extra = self.site / "extra.txt"
        extra.write_text("unexpected")
        with self.assertRaises(ValueError):
            publication.check(self.site, REVISION)
        extra.unlink()
        extra.symlink_to(path)
        with self.assertRaises(ValueError):
            publication.check(self.site, REVISION)
        extra.unlink()
        with self.assertRaises(ValueError):
            publication.check(self.site, "2" * 40)

    def test_manifest_rejects_path_traversal_duplicate_and_digest_drift(self):
        for mutation in ("path", "duplicate", "digest", "size"):
            value = deepcopy(self.manifest)
            if mutation == "path":
                value["files"][0]["path"] = "../outside"
            elif mutation == "duplicate":
                value["files"].insert(0, value["files"][0])
            elif mutation == "size":
                value["files"][0]["bytes"] = True
            else:
                value["files_sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                publication.validate_manifest(value)

    def test_seal_rejects_mismatched_relay_or_source(self):
        path = self.site / "intelligence/build-manifest.json"
        value = json.loads(path.read_bytes())
        value["generator"]["revision"] = "2" * 40
        path.write_bytes(publication.encoded(value))
        with self.assertRaises(ValueError):
            publication.seal(self.site, REVISION)

    def remote_fixture(self, path, **kwargs):
        target = self.site / (path or "index.html")
        return target.read_bytes() if target.is_file() else None

    def test_first_deployment_requires_both_manifest_and_root_missing(self):
        with patch.object(publication, "remote", return_value=None):
            result = publication.capture_recovery(self.root / "recovery")
        self.assertEqual(result["state"], "first-deployment")
        self.assertIsNone(result["previous"])
        with patch.object(publication, "remote", side_effect=[None, b"existing site"]):
            with self.assertRaises(ValueError):
                publication.capture_recovery(self.root / "blocked")

    def test_recovery_saves_verified_prior_bytes_before_a_success_receipt(self):
        with patch.object(publication, "remote", side_effect=self.remote_fixture):
            recovered = publication.capture_recovery(self.root / "recovery")
            self.assertEqual(recovered["state"], "captured")
            self.assertEqual((self.root / "recovery/site/index.html").read_bytes(), (self.site / "index.html").read_bytes())
            self.assertEqual(publication.check(self.root / "recovery/site", REVISION), self.manifest)
            with patch.dict(os.environ, {"GITHUB_RUN_ID": "123", "GITHUB_RUN_ATTEMPT": "2"}):
                receipt = publication.verify_live(self.site, REVISION, self.root / "recovery", self.root / "receipt.json")
        self.assertEqual(receipt["workflow_run_id"], 123)
        self.assertEqual(receipt["verified_public_files"], len(self.manifest["files"]) - 2)
        self.assertEqual(receipt["recovery"]["previous"]["revision"], REVISION)

    def test_live_byte_drift_does_not_produce_success_evidence(self):
        def drift(path, **kwargs):
            return b"drift" if path == "intelligence/site.css" else self.remote_fixture(path)
        with patch.object(publication, "remote", side_effect=drift):
            with self.assertRaises(ValueError):
                publication.verify_live(self.site, REVISION, self.root / "recovery", self.root / "receipt.json")
        self.assertFalse((self.root / "receipt.json").exists())


if __name__ == "__main__":
    unittest.main()
