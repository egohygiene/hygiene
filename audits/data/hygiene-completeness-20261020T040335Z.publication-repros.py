"""Bounded Hygiene publication/release audit reproductions.

Read source from --repository-root; all writes use temporary directories.
No workflow, remote origin, tag, release, credential or staged file is used.
Synthetic transport manifests do not claim a semantic Relay build.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile


sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repository-root", type=Path, default=Path.cwd())
root = parser.parse_args().repository_root.resolve()


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, root / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


publication = load("audit_hygiene_publication", "tools/publication.py")
releases = load("audit_hygiene_releases", "tools/releases.py")
source_revision = "aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d"
workflow = (root / ".github/workflows/publish-pages.yml").read_text()
workflow_pins = sorted(set(re.findall(r"uses: egohygiene/relay/[^\s]+@([0-9a-f]{40})", workflow)))
assert len(workflow_pins) == 1
workflow_pin = workflow_pins[0]
config_pin = publication.config()["relay_revision"]
results = {}

with tempfile.TemporaryDirectory(prefix="hygiene-publication-audit-") as temporary:
    site = Path(temporary) / "site"
    publication.shell(site, source_revision)
    manifest_path = site / "intelligence/build-manifest.json"
    manifest = {
        "consumer": {"repository": "egohygiene/hygiene", "revision": source_revision},
        "generator": {"revision": workflow_pin},
    }
    publication.write(manifest_path, publication.encoded(manifest))
    try:
        publication.seal(site, source_revision)
    except ValueError as error:
        current_error = str(error)
    else:
        current_error = None
    current_manifest_written = (site / "publication.json").exists()
    manifest["generator"]["revision"] = config_pin
    publication.write(manifest_path, publication.encoded(manifest))
    publication.seal(site, source_revision)
    results["publication_selection_parity"] = {
        "workflow_relay_revision": workflow_pin,
        "publication_config_relay_revision": config_pin,
        "actual_workflow_pin_rejected": current_error,
        "publication_manifest_written_for_actual_workflow_pin": current_manifest_written,
        "config_pin_transport_fixture_seals": (site / "publication.json").is_file(),
        "fixture_limit": "minimal synthetic transport input, not a real Relay semantic build or live deployment",
    }

profile = releases.load_json(root / "catalog/repository-release-policy.json")
fixture_paths = (
    ".egohygiene/release.json", ".tasks/release.yml", "Taskfile.yml", "CHANGELOG.md", "AGENTS.md",
    "docs/ecosystem/REPOSITORY_RELEASE.md", ".github/workflows/release-policy.yml",
)
with tempfile.TemporaryDirectory(prefix="hygiene-release-audit-") as temporary:
    target = Path(temporary)
    for relative in fixture_paths:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / relative, destination)
    declaration_path = target / ".egohygiene/release.json"
    baseline = json.loads(declaration_path.read_text())
    baseline_accepted = releases.validate_declaration(target, profile) == baseline

    def mutate_and_check(mutation):
        value = json.loads(json.dumps(baseline))
        mutation(value)
        declaration_path.write_text(json.dumps(value))
        try:
            releases.validate_declaration(target, profile)
        except (OSError, ValueError) as error:
            return {"accepted": False, "error": str(error)}
        return {"accepted": True, "error": None}

    task_result = mutate_and_check(lambda value: value["automation"]["tasks"].update(plan="missing:plan"))
    authority_result = mutate_and_check(lambda value: value["components"][0].update(version_authority={}))
    declaration_path.write_text(json.dumps(baseline))
    workflow_path = target / ".github/workflows/release-policy.yml"
    original_workflow = workflow_path.read_text()
    workflow_path.write_text(original_workflow.replace("on:\n", "on:\n  push: {branches: [main]}\n", 1))
    try:
        releases.validate_declaration(target, profile)
    except (OSError, ValueError) as error:
        inline_push = {"accepted": False, "error": str(error)}
    else:
        inline_push = {"accepted": True, "error": None}
    results["release_baseline_composition"] = {
        "baseline_accepted": baseline_accepted,
        "schema_invalid_declared_task_value": task_result,
        "schema_invalid_empty_version_authority": authority_result,
        "inline_push_trigger_against_manual_only_guard": inline_push,
        "limit": "current declaration is valid; these are temporary negative cases, not a live publication claim",
    }

print(json.dumps(results, indent=2, sort_keys=True))
