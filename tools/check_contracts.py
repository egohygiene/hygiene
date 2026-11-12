#!/usr/bin/env python3
"""Run Hygiene's existing contract regressions and deterministic source checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
LOG_LIMIT = 256 * 1024
COMMAND_TIMEOUT = 60

# These are the existing reference CLI entry points, not another policy engine.
REFERENCE_CHECKS = (
    ("catalog", "catalog.py", "validate"),
    (
        "catalog-generated",
        "catalog.py",
        "check-generated",
        "--output",
        "docs/generated/REPOSITORIES.md",
    ),
    ("context-policy", "context.py", "validate"),
    ("continuity-profile", "continuity.py", "validate-profile"),
    (
        "continuity-repository",
        "continuity.py",
        "validate-repository",
        "--repository",
        ".",
    ),
    ("web-profile", "agent_ready_web.py", "validate-profile"),
    ("web-fixtures", "agent_ready_web.py", "validate-fixtures"),
    ("boundary-register", "boundaries.py", "validate"),
    (
        "boundary-generated",
        "boundaries.py",
        "check-generated",
        "--output",
        "docs/generated/DEPENDENCY_BOUNDARIES.md",
    ),
    (
        "boundary-scan",
        "boundaries.py",
        "scan",
        "--repository-root",
        ".",
        "--repository",
        "egohygiene/hygiene",
    ),
    (
        "intelligence-fixture",
        "intelligence.py",
        "validate",
        "--snapshot",
        "fixtures/repository-intelligence/complete-quest.json",
        "--vocabulary",
        "catalog/repository-intelligence-vocabulary.json",
    ),
    ("presentation-profile", "presentation.py", "validate-profile"),
    (
        "presentation-minimal",
        "presentation.py",
        "validate-evidence",
        "--evidence",
        "fixtures/repository-presentation/minimal.valid.json",
    ),
    (
        "presentation-rich",
        "presentation.py",
        "validate-evidence",
        "--evidence",
        "fixtures/repository-presentation/rich.valid.json",
    ),
    ("surface-registry", "site_surfaces.py", "validate-registry"),
    ("surface-fixtures", "site_surfaces.py", "validate-fixtures"),
    (
        "adr-fixture",
        "decisions.py",
        "decision",
        "--input",
        "fixtures/architecture-decisions/decision.proposed.valid.json",
    ),
    (
        "adr-lineage-fixtures",
        "decisions.py",
        "decision-set",
        "--input",
        "fixtures/architecture-decisions/decision.superseded.valid.json",
        "--input",
        "fixtures/architecture-decisions/decision.accepted.valid.json",
    ),
    (
        "adr-policy-reference",
        "decisions.py",
        "policy-reference",
        "--input",
        "fixtures/architecture-decisions/policy-reference.valid.json",
    ),
    ("release-profile", "releases.py", "validate-profile"),
    (
        "release-declaration",
        "releases.py",
        "validate-declaration",
        "--repository",
        ".",
        "--format",
        "json",
    ),
)


def check_plan() -> list[tuple[str, list[str]]]:
    checks = [
        (
            "unit-tests",
            [
                sys.executable,
                "-I",
                "-m",
                "unittest",
                "discover",
                "--start-directory",
                "tests",
                "--pattern",
                "test_*.py",
                "--verbose",
            ],
        )
    ]
    # -E preserves the tools directory for the existing sibling Python imports.
    # The top-level gate and unittest discovery run in isolated mode.
    checks.extend(
        (name, [sys.executable, "-E", "tools/" + tool, *args])
        for name, tool, *args in REFERENCE_CHECKS
    )
    checks.append(
        (
            "adr-review-patch",
            [
                "git",
                "apply",
                "--check",
                "--unidiff-zero",
                "docs/adr-workflow/2026-10-18-adr-0001-v1.2-review.patch",
            ],
        )
    )
    contexts = ROOT / "docs" / "generated" / "contexts"
    for path in sorted(contexts.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        repositories = re.findall(
            r'^repository: "(egohygiene/[^"\n]+)"$', text, re.MULTILINE
        )
        revisions = re.findall(
            r'^source-revision: "([0-9a-f]{40})"$', text, re.MULTILINE
        )
        if len(repositories) != 1 or len(revisions) != 1:
            raise ValueError(
                f"generated context identity/provenance is invalid: {path.relative_to(ROOT)}"
            )
        checks.append(
            (
                "context-generated-" + path.stem,
                [
                    sys.executable,
                    "-E",
                    "tools/context.py",
                    "check",
                    "--repository",
                    repositories[0],
                    "--source-revision",
                    revisions[0],
                    "--output",
                    path.relative_to(ROOT).as_posix(),
                ],
            )
        )
    contract = tomllib.loads(
        (ROOT / "contracts" / "repository-context.toml").read_text(encoding="utf-8")
    )
    revision = contract["source"]["revision"]
    if not isinstance(revision, str) or re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise ValueError(
            "generated repository-context contract source revision is invalid"
        )
    checks.append(
        (
            "context-generated-contract",
            [
                sys.executable,
                "-E",
                "tools/context.py",
                "check-contract",
                "--source-revision",
                revision,
                "--output",
                "contracts/repository-context.toml",
            ],
        )
    )
    return checks


def unit_counts(text: str) -> dict[str, int | None]:
    matches = re.findall(r"^Ran ([0-9]+) tests? in ", text, re.MULTILINE)
    counts = {
        "run": int(matches[-1]) if matches else None,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "expected_failures": 0,
        "unexpected_successes": 0,
    }
    summaries = re.findall(
        r"^(?:OK(?: \([^\n]*\))?|FAILED \([^\n]*\))$", text, re.MULTILINE
    )
    summary = summaries[-1] if summaries else ""
    for key, number in re.findall(
        r"(failures|errors|skipped|expected failures|unexpected successes)=([0-9]+)",
        summary,
    ):
        counts[key.replace(" ", "_")] = int(number)
    return counts


def run_check(name: str, command: list[str], directory: Path) -> dict:
    started = time.monotonic()
    timed_out = False
    returncode = None
    with tempfile.TemporaryFile() as spool:
        try:
            process = subprocess.Popen(
                command,
                cwd=ROOT,
                stdout=spool,
                stderr=subprocess.STDOUT,
                start_new_session=os.name == "posix",
            )
            try:
                returncode = process.wait(timeout=COMMAND_TIMEOUT)
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    if os.name == "posix":
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                except ProcessLookupError:
                    pass
                returncode = process.wait()
        except OSError as error:
            spool.write(str(error).encode("utf-8", errors="replace"))
        size = spool.seek(0, os.SEEK_END)
        spool.seek(max(0, size - 16 * 1024))
        tail = spool.read().decode("utf-8", errors="replace")
        spool.seek(0)
        output = spool.read(LOG_LIMIT)
        truncated = size > LOG_LIMIT
        if truncated:
            marker = b"\n[retained output truncated; final diagnostics follow]\n"
            suffix = tail.encode("utf-8")[-16 * 1024 :]
            output = output[: LOG_LIMIT - len(marker) - len(suffix)] + marker + suffix
    log = name + ".log"
    (directory / log).write_bytes(output)
    result = {
        "id": name,
        "command": command,
        "status": "passed" if returncode == 0 and not timed_out else "failed",
        "exit_code": returncode,
        "timed_out": timed_out,
        "seconds": round(time.monotonic() - started, 3),
        "log": log,
        "log_bytes": len(output),
        "output_bytes": size,
        "log_truncated": truncated,
    }
    if name == "unit-tests":
        result["tests"] = unit_counts(tail)
        if not result["tests"]["run"]:
            result["status"] = "failed"
            result["reason"] = "missing or empty unittest execution"
    print(
        f"{name}: {result['status']}"
        + (
            " " + json.dumps(result["tests"], sort_keys=True)
            if "tests" in result
            else ""
        ),
        flush=True,
    )
    if result["status"] != "passed":
        print(tail[-4000:], flush=True)
    return result


def git_value(*arguments: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report-directory", type=Path, default=ROOT / ".cache" / "contract-regression"
    )
    args = parser.parse_args(argv)
    args.report_directory.mkdir(parents=True, exist_ok=True)
    status = git_value("status", "--porcelain=v1")
    report = {
        "schema_version": "1.0.0",
        "repository": "egohygiene/hygiene",
        "source_revision": git_value("rev-parse", "HEAD"),
        "source_dirty": bool(status) if status is not None else None,
        "python_version": sys.version.split()[0],
        "status": "failed",
        "complete": False,
        "test_modules": sorted(
            path.name for path in (ROOT / "tests").glob("test_*.py")
        ),
        "checks": [],
        "native_admission": "not-assessed",
        "publication": "not-performed",
    }
    target = args.report_directory / "result.json"

    def save() -> None:
        target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    save()
    try:
        checks = check_plan()
    except (OSError, ValueError, KeyError, TypeError) as error:
        report["planning_error"] = str(error)
        save()
        print(f"contract gate plan failed: {error}", file=sys.stderr)
        return 1
    for name, command in checks:
        report["checks"].append(run_check(name, command, args.report_directory))
        save()
    report["complete"] = True
    report["status"] = (
        "passed"
        if all(check["status"] == "passed" for check in report["checks"])
        else "failed"
    )
    save()
    print(
        f"contract regression gate: {report['status']}; {len(checks)} checks; report {target.name}"
    )
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
