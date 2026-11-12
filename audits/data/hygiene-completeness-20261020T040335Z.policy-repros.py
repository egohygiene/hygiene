#!/usr/bin/env python3
"""Reproduce bounded policy-reference gaps at Hygiene aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d.

Loads first-party reference tools. Mutations stay in memory or disposable files;
no repository source, live resource, credential or publication is changed.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repository-root", type=Path, default=Path.cwd())
parser.add_argument("--as-of", default="2026-10-20")
arguments = parser.parse_args()
root = arguments.repository_root.resolve()
as_of = date.fromisoformat(arguments.as_of)

def load_tool(name):
    spec = importlib.util.spec_from_file_location("audit_policy_" + name, root / "tools" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def load_json(relative):
    return json.loads((root / relative).read_text(encoding="utf-8"))

results = {"source_revision": "aa6a5e25ea3ef80e4dcc15570a1ea166b9f4af3d", "as_of": as_of.isoformat()}
presentation = load_tool("presentation")
profile = load_json("catalog/repository-presentation-profile.json")
evidence = load_json("fixtures/repository-presentation/rich.valid.json")
baseline = presentation.validate_evidence(evidence, profile)
for slot in evidence["slots"]:
    for record in slot["evidence"]:
        record["freshness"] = "stale"
        record["assertion"] = "unknown"
results["presentation_stale_unknown_passing"] = {
    "baseline_errors": baseline,
    "mutated_errors": presentation.validate_evidence(evidence, profile),
    "derived_state": presentation.derive_state(evidence["slots"]),
    "asserted_assessment": evidence["assessment"]["state"],
    "all_records_mutated": True,
}

continuity = load_tool("continuity")
profile = load_json("catalog/repository-continuity-policy.json")
profile["exceptions"]["records"] = [{
    "repository": "egohygiene/hygiene",
    "owner": "egohygiene/hygiene",
    "reason": "Synthetic bounded expiry reproduction.",
    "approval": "https://github.com/egohygiene/hygiene/issues/45#issuecomment-1",
    "expires_on": "2026-10-01",
    "review_trigger": "Reconcile against the declared assessment instant.",
    "validation_state": "approved",
    "exit_criteria": "Remove the synthetic exception.",
}]
call_arguments = (profile, "egohygiene/hygiene", "active", "standard", "public")
with tempfile.TemporaryDirectory(prefix="hygiene-policy-repro-") as temporary:
    candidate = Path(temporary) / "profile.json"
    candidate.write_text(json.dumps(profile), encoding="utf-8")
    cli = subprocess.run(
        [sys.executable, str(root / "tools/continuity.py"), "--profile", str(candidate),
         "resolve", "--repository", "egohygiene/hygiene", "--lifecycle", "active",
         "--repository-kind", "standard", "--visibility", "public"],
        text=True, capture_output=True, check=False,
    )
    results["continuity_expiry_clock"] = {
        "profile_updated": profile["updated"],
        "synthetic_expiry": "2026-10-01",
        "profile_errors": continuity.validate_profile(profile),
        "default_requirement": continuity.resolve_applicability(*call_arguments)["requirement"],
        "explicit_as_of_requirement": continuity.resolve_applicability(*call_arguments, as_of=as_of)["requirement"],
        "cli_exit_code": cli.returncode,
        "cli_requirement": json.loads(cli.stdout)["requirement"] if cli.returncode == 0 else None,
    }

decisions = load_tool("decisions")
old = load_json("fixtures/architecture-decisions/decision.superseded.valid.json")
new = load_json("fixtures/architecture-decisions/decision.accepted.valid.json")
old["status"] = "accepted"
old["superseded_by"] = []
new["status"] = "proposed"
new["approval"] = None
new["evidence"] = []
results["decision_pending_supersession"] = {
    "predecessor_errors": decisions.validate_decision(old),
    "proposed_replacement_errors": decisions.validate_decision(new),
    "set_errors": decisions.validate_decision_set([old, new]),
    "predecessor_status": old["status"],
    "replacement_status": new["status"],
}
verified = copy.deepcopy(old)
verified["implementation_status"] = "verified"
results["decision_approval_only_verification"] = {
    "evidence_types": [record["type"] for record in verified["evidence"]],
    "errors": decisions.validate_decision(verified),
}
dangling = copy.deepcopy(old)
dangling["related"] = ["ADR-999"]
legacy = decisions.validate_decision_set([dangling])
dangling["related"] = ["ADR-0999"]
results["decision_legacy_reference_resolution"] = {
    "three_digit_dangling_errors": legacy,
    "four_digit_dangling_errors": decisions.validate_decision_set([dangling]),
}
zero_id = load_json("fixtures/architecture-decisions/decision.proposed.valid.json")
zero_id["id"] = "ADR-0000"
results["decision_zero_identifier"] = {"errors": decisions.validate_decision(zero_id)}
print(json.dumps(results, indent=2, sort_keys=True))

