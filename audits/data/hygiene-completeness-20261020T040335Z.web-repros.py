"""Bounded ARW URL counterexamples for Hygiene aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d.

Reads repository sources; all input writes occur in disposable temp directories.
Does not fetch URLs, run browser tools, publish evidence, or alter source.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repository-root", type=Path, default=Path.cwd())
root = parser.parse_args().repository_root.resolve()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("audit_agent_ready_web", root / "tools/agent_ready_web.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
profile = module.load_json(root / "catalog/agent-ready-web-profile.json")
original = module.load_json(root / "fixtures/agent-ready-web/site.application.valid.json")["conformance"]
results = {"baseline_errors": module.validate_conformance(original, profile), "evidence_locations": [], "origins": []}
locations = [
    "https://",
    "https://synthetic-user:synthetic-password@example.invalid/evidence",
    "https://exa mple.invalid/evidence",
    "https://example.invalid\\path",
    "https://example.invalid\t",
]
origins = [
    "https://example.invalid\\path",
    "https://example.invalid\t",
    "https://exa mple.invalid",
    "https://example.invalid:0",
]
for location in locations:
    value = copy.deepcopy(original)
    value["evidence"][0]["location"] = location
    results["evidence_locations"].append({"value": location, "errors": module.validate_conformance(value, profile)})
for origin in origins:
    value = copy.deepcopy(original)
    value["subject"]["origin"] = origin
    results["origins"].append({"value": origin, "errors": module.validate_conformance(value, profile)})

with tempfile.TemporaryDirectory(prefix="hygiene-arw-audit-") as temporary:
    value = copy.deepcopy(original)
    value["subject"]["origin"] = "https://exa mple.invalid"
    value["evidence"][0]["location"] = "https://"
    input_path = Path(temporary) / "conformance.json"
    input_path.write_text(json.dumps(value), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(root / "tools/agent_ready_web.py"), "--profile", str(root / "catalog/agent-ready-web-profile.json"), "validate-conformance", "--input", str(input_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    results["cli"] = {"exit_code": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))
