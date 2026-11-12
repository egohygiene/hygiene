#!/usr/bin/env python3
"""Project reviewed public catalog identities and compare an offline discovery.

This adapter never discovers repositories, authorizes a provider operation,
promotes role declarations or emits protected input metadata.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile


PUBLIC_SCHEMA = "egohygiene.repository-public-catalog/v1"
DISCOVERY_SCHEMA = "egohygiene.repository-public-discovery/v1"
REPORT_SCHEMA = "egohygiene.repository-public-drift/v1"
NAME = re.compile(r"(?:\.github|[a-z0-9][a-z0-9.-]*)")
TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
LIMIT = 8 * 1024 * 1024
SOURCE_URL = "https://api.github.com/orgs/egohygiene/repos?type=public&per_page=100"
SENSITIVE = re.compile(r"(?:github_pat_|gh[pousr]_|(?:token|password|secret)\s*[:=]|[\w.+-]+@[\w.-]+\.[a-z]{2,}|/(?:home|Users|workspace|tmp)/|[A-Za-z]:\\|\\\\)", re.I)


def require(condition):
    if not condition:
        raise ValueError("PUBLIC_INVENTORY_INVALID")


def plain(value):
    require(isinstance(value, dict) and not getattr(value, "duplicate_keys", set()))
    return value


def text(value, maximum=2048):
    require(isinstance(value, str) and 0 < len(value) <= maximum
        and not any(ord(c) < 32 or ord(c) == 127 for c in value) and not SENSITIVE.search(value))
    return value


def strings(value, maximum=256):
    require(isinstance(value, list) and len(value) <= maximum)
    result = [text(item) for item in value]
    require(len(set(result)) == len(result))
    return result


def instant(value):
    require(isinstance(value, str) and TIME.fullmatch(value))
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    require(result.strftime("%Y-%m-%dT%H:%M:%SZ") == value)
    return result


def full_name(value):
    value = text(value, 140)
    require(value.startswith("egohygiene/") and NAME.fullmatch(value.removeprefix("egohygiene/")))
    return value


def identity(raw):
    value = plain(raw)
    name = full_name(value.get("full_name"))
    require(type(value.get("repository_id")) is int and 0 < value["repository_id"] <= 9007199254740991
        and value.get("visibility") == "public" and type(value.get("archived")) is bool)
    branch = text(value.get("default_branch"), 255)
    require(not branch.startswith(("/", "-")) and not branch.endswith(("/", "."))
        and ".." not in branch and "//" not in branch and "@{" not in branch
        and not any(c in branch for c in " ~^:?*[\\"))
    return {"name": name.split("/", 1)[1], "full_name": name,
        "repository_id": value["repository_id"], "visibility": "public",
        "source_url": "https://github.com/" + name,
        "default_branch": branch, "archived": value["archived"]}


def source(value):
    value = plain(value)
    require(set(value) == {"provider", "scope", "completeness", "url"}
        and value["provider"] == "github" and value["scope"] == "public"
        and value["completeness"] in {"complete", "partial"} and value["url"] == SOURCE_URL)
    return dict(value)


class ParsedObject(dict):
    """Retain ambiguity locally until public visibility has been selected."""

    def __init__(self):
        super().__init__()
        self.duplicate_keys = set()


def pairs(items):
    result = ParsedObject()
    for key, value in items:
        if key in result:
            result.duplicate_keys.add(key)
        result[key] = value
    return result


def read(path):
    path = path.absolute()
    require(".." not in path.parts and not any(item.is_symlink() for item in (path, *path.parents))
        and path.is_file() and path.stat().st_size <= LIMIT)
    with path.open("rb") as handle:
        content = handle.read(LIMIT + 1)
    require(len(content) <= LIMIT)
    return plain(json.loads(content, object_pairs_hook=pairs,
        parse_constant=lambda _value: require(False)))


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def write(path, content):
    path = path.absolute()
    require(".." not in path.parts and ".git" not in path.parts
        and not any(item.is_symlink() for item in (path, *path.parents)))
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".public-inventory-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def selected_public_rows(value):
    require(isinstance(value, list) and len(value) <= 100000)
    # Do not inspect protected identities, malformed fields or duplicate claims.
    result = [item for item in value if isinstance(item, dict) and item.get("visibility") == "public"
        and "visibility" not in getattr(item, "duplicate_keys", set())]
    require(len(result) <= 1024)
    return result


def uniqueness(rows):
    names = [row["full_name"] for row in rows]
    identifiers = [row["repository_id"] for row in rows]
    require(len(names) == len(set(names)) and len(identifiers) == len(set(identifiers)))


def evidence_url(value, allowed):
    # Visibility/admission precedes text diagnostics for a cited repository.
    if not isinstance(value, str):
        return None
    match = re.match(r"^https://github\.com/([^/]+/[^/]+)/", value)
    if not match or match.group(1) not in allowed:
        return None
    value = text(value)
    require(re.fullmatch(r"https://github\.com/egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)/blob/[a-f0-9]{40}/[A-Za-z0-9._/-]+", value)
        and all(part not in {".", ".."} for part in value.split("/")))
    return value


def project(catalog):
    """Visibility precedes validation, aliases, role text, counts and hashing."""
    require(catalog.get("schema_version") == "1.0.0" and catalog.get("organization") == "egohygiene")
    boundary = plain(catalog.get("public_inventory"))
    observed = boundary.get("observed_at")
    instant(observed)
    public_source = source(boundary.get("source"))
    selected = selected_public_rows(catalog.get("repositories"))
    allowed = {full_name(raw.get("full_name")) for raw in selected}
    rows = []
    for raw in selected:
        plain(raw)
        observation = plain(raw.get("public_observation"))
        require(observation.get("observed_at") == observed)
        row = identity({**observation, "full_name": raw.get("full_name"), "visibility": "public"})
        require(raw.get("name") == row["name"] and raw.get("source_url") == row["source_url"]
            and observation.get("source_url") == "https://api.github.com/repos/" + row["full_name"])
        aliases = strings(raw.get("aliases", []))
        require(all(NAME.fullmatch(alias) and alias != row["name"] for alias in aliases))
        gate = plain(raw.get("next_gate"))
        require(set(gate) == {"state", "description", "source_url", "source_observed_at"})
        gate_source = evidence_url(gate.get("source_url"), allowed)
        if gate.get("state") == "unknown":
            require(all(gate.get(key) is None for key in ("description", "source_url", "source_observed_at")))
            next_gate = dict(gate)
        elif gate_source is None:
            next_gate = {"state": "unknown", "description": None, "source_url": None, "source_observed_at": None}
        else:
            require(gate.get("state") == "source-declared")
            date = text(gate.get("source_observed_at"), 10)
            datetime.strptime(date, "%Y-%m-%d")
            next_gate = {"state": "source-declared", "description": text(gate.get("description")),
                "source_url": gate_source, "source_observed_at": date}
        role = {"plane": text(raw.get("plane"), 128), "lifecycle": text(raw.get("lifecycle"), 128),
            "maturity": text(raw.get("maturity"), 128), "owns": strings(raw.get("owns")),
            "excludes": strings(raw.get("excludes")), "outputs": strings(raw.get("outputs")),
            "evidence": []}
        raw_evidence = raw.get("role_evidence", [])
        require(isinstance(raw_evidence, list) and len(raw_evidence) <= 32)
        for url in raw_evidence:
            admitted = evidence_url(url, allowed)
            if admitted is not None:
                require(admitted not in role["evidence"])
                role["evidence"].append(admitted)
        rows.append({**row, "aliases": sorted(aliases), "role": role, "next_gate": next_gate})
    uniqueness(rows)
    names = {row["name"] for row in rows}
    aliases = [alias for row in rows for alias in row["aliases"]]
    require(len(aliases) == len(set(aliases)) and not names.intersection(aliases))
    return {"schema": PUBLIC_SCHEMA, "organization": "egohygiene", "observed_at": observed,
        "source": public_source, "repositories": sorted(rows, key=lambda row: row["full_name"])}


def discovery(value):
    require(value.get("schema") == DISCOVERY_SCHEMA and value.get("organization") == "egohygiene")
    observed = value.get("observed_at")
    instant(observed)
    public_source = source(value.get("source"))
    rows = [identity(row) for row in selected_public_rows(value.get("repositories"))]
    uniqueness(rows)
    return {"schema": DISCOVERY_SCHEMA, "organization": "egohygiene", "observed_at": observed,
        "source": public_source, "repositories": sorted(rows, key=lambda row: row["full_name"])}


def compare(catalog, captured, as_of, maximum_age_seconds):
    baseline, live = project(catalog), discovery(captured)
    now = instant(as_of)
    require(type(maximum_age_seconds) is int and 1 <= maximum_age_seconds <= 2678400)
    require(instant(baseline["observed_at"]) <= now and instant(live["observed_at"]) <= now)
    before = {row["repository_id"]: row for row in baseline["repositories"]}
    after = {row["repository_id"]: row for row in live["repositories"]}
    missing = sorted(before[key]["full_name"] for key in before.keys() - after.keys())
    extra = sorted(after[key]["full_name"] for key in after.keys() - before.keys())
    renamed, changed = [], []
    for identifier in sorted(before.keys() & after.keys()):
        left, right = before[identifier], after[identifier]
        if left["full_name"] != right["full_name"]:
            renamed.append({"repository_id": identifier, "from": left["full_name"], "to": right["full_name"]})
        fields = [key for key in ("archived", "default_branch") if left[key] != right[key]]
        if fields:
            changed.append({"repository": right["full_name"], "fields": fields})
    complete = baseline["source"]["completeness"] == live["source"]["completeness"] == "complete"
    stale = any((now - instant(item["observed_at"])).total_seconds() > maximum_age_seconds for item in (baseline, live))
    status = "incomplete" if not complete else "stale" if stale else "drift" if missing or extra or renamed or changed else "current"
    # Hash only admitted public fields. Raw capture/catalog hashes, hidden-row
    # counts and discarded data never enter a public report.
    return {"schema": REPORT_SCHEMA, "organization": "egohygiene", "as_of": as_of,
        "maximum_age_seconds": maximum_age_seconds, "status": status,
        "catalog_observed_at": baseline["observed_at"], "discovery_observed_at": live["observed_at"],
        "catalog_public_sha256": digest(baseline), "discovery_public_sha256": digest(live),
        "missing_public": missing if complete else [], "extra_public": extra,
        "renamed_public": renamed, "changed_public": changed,
        "publication": "not-authorized", "role_admission": "independent"}


def parser():
    value = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    value.add_argument("--catalog", type=Path, default=Path("catalog/repositories.yaml"))
    sub = value.add_subparsers(dest="operation", required=True)
    for operation in ("project", "check-generated"):
        selected = sub.add_parser(operation, allow_abbrev=False)
        selected.add_argument("--output", type=Path, default=Path("catalog/public-repositories.json"))
    check = sub.add_parser("check", allow_abbrev=False)
    check.add_argument("--discovery", type=Path, required=True)
    check.add_argument("--as-of", required=True)
    check.add_argument("--maximum-age-seconds", type=int, default=604800)
    return value


def main():
    try:
        args = parser().parse_args()
        catalog = read(args.catalog)
        if args.operation == "check":
            report = compare(catalog, read(args.discovery), args.as_of, args.maximum_age_seconds)
            sys.stdout.buffer.write(encoded(report))
            return 0 if report["status"] == "current" else 1
        content = encoded(project(catalog))
        if args.operation == "project":
            requested, canonical = args.output.absolute(), args.catalog.absolute()
            require(requested != canonical and not (requested.exists() and canonical.exists()
                and os.path.samefile(requested, canonical)))
            write(args.output, content)
        else:
            require(args.output.is_file() and not args.output.is_symlink() and args.output.read_bytes() == content)
        print("Public catalog: admitted public projection prepared")
        return 0
    except Exception:
        print("Public catalog: input, projection or freshness request denied", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
