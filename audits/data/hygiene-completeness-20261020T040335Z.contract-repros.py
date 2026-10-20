"""Bounded source-read-only proofs for Hygiene aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d.

Run with Python's standard library from a Hygiene checkout, or pass
--repository-root. All generated inputs and outputs are confined to disposable
temporary parent directories. The deliberate output escape remains inside that
temporary parent; no real secret, host file, provider write or policy change is
used. Results are synthetic counterexamples, not exploit or release evidence.
"""
from __future__ import annotations

import argparse
import copy
import importlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.repository_root.resolve()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / "tools"))
    catalog = importlib.import_module("catalog")
    context = importlib.import_module("context")
    boundaries = importlib.import_module("boundaries")
    source = catalog.load_catalog(root / "catalog/repositories.yaml")
    policy = context.load_json(root / "catalog/repository-context.json")
    schema = json.loads((root / "schemas/repository-catalog.v1.schema.json").read_text())
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True,
        capture_output=True, check=True,
    ).stdout.strip()
    results = {
        "audited_revision": revision,
        "baseline": {
            "catalog_diagnostics": catalog.validate_catalog(source),
            "context_policy_diagnostics": context.validate_policy(source, policy),
        },
    }

    # The declared repository-name schema rejects this value, but the actual
    # dependency-free validator admits it and render-all uses it as a path.
    candidate = copy.deepcopy(source)
    repository = copy.deepcopy(candidate["repositories"][0])
    repository.update({
        "name": "../escaped",
        "full_name": "egohygiene/../escaped",
        "source_url": "https://github.com/egohygiene/../escaped",
        "consumes": [],
        "domains": [],
    })
    candidate["repositories"].append(repository)
    candidate["repository_count"] += 1
    with tempfile.TemporaryDirectory(prefix="hygiene-audit-context-") as temporary:
        parent = Path(temporary)
        catalog_path = parent / "catalog.json"
        policy_path = parent / "policy.json"
        output_root = parent / "selected-output"
        catalog_path.write_text(json.dumps(candidate), encoding="utf-8")
        policy_path.write_text(json.dumps(policy), encoding="utf-8")
        catalog_run = subprocess.run(
            [sys.executable, str(root / "tools/catalog.py"), "--catalog",
             str(catalog_path), "validate"],
            text=True, capture_output=True,
        )
        context_run = subprocess.run(
            [sys.executable, str(root / "tools/context.py"), "--catalog",
             str(catalog_path), "--policy", str(policy_path), "render-all",
             "--source-revision", "a" * 40, "--output-directory", str(output_root)],
            text=True, capture_output=True,
        )
        results["AUDIT-002"] = {
            "synthetic_repository_name": repository["name"],
            "schema_name_pattern_accepts": re.fullmatch(
                schema["$defs"]["name"]["pattern"], repository["name"]
            ) is not None,
            "catalog_diagnostics": catalog.validate_catalog(candidate),
            "context_policy_diagnostics": context.validate_policy(candidate, policy),
            "catalog_cli_exit_code": catalog_run.returncode,
            "render_all_exit_code": context_run.returncode,
            "file_written_outside_selected_output_root": (parent / "escaped.md").is_file(),
            "escaped_file_remains_inside_temporary_parent": True,
        }

    # Compare scalar spellings of the same workflow input. No remote workflow
    # is invoked: this exercises the local scanner only.
    reference = "egohygiene/relay/.github/workflows/repository-architecture-validation.yml@main"
    spellings = {
        "plain": reference,
        "double_quoted": "\"" + reference + "\"",
        "single_quoted": "'" + reference + "'",
        "pinned_double_quoted": "\"" + reference.removesuffix("main") + "a" * 40 + "\"",
    }
    scans = {}
    with tempfile.TemporaryDirectory(prefix="hygiene-audit-boundary-") as temporary:
        target = Path(temporary)
        workflow = target / ".github/workflows/synthetic.yml"
        workflow.parent.mkdir(parents=True)
        for label, spelling in spellings.items():
            workflow.write_text(
                "name: Synthetic audit fixture\non: workflow_dispatch\njobs:\n"
                "  proof:\n    uses: " + spelling + "\n", encoding="utf-8",
            )
            run = subprocess.run(
                [sys.executable, str(root / "tools/boundaries.py"),
                 "--catalog", str(root / "catalog/repositories.yaml"),
                 "--register", str(root / "catalog/dependency-boundaries.yaml"),
                 "--contracts", str(root / "catalog/contracts.yaml"), "scan",
                 "--repository-root", str(target), "--repository", "egohygiene/hygiene",
                 "--format", "json"], text=True, capture_output=True,
            )
            scans[label] = {
                "exit_code": run.returncode,
                "findings": json.loads(run.stdout),
            }
    results["AUDIT-003"] = scans
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
