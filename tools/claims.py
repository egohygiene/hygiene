#!/usr/bin/env python3
"""Pure report-only claim qualification from explicit provenance and clock.

No evidence is fetched, commands executed, sources authenticated or measurements
scientifically validated. Public projections require caller-admitted repositories
and never serialize arbitrary claim statements, commands or protected locators.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "egohygiene.claim-provenance/v1"
VERSION = "1.0.0-alpha.1"
STATES = ("measured", "verified", "provider-reported", "reported", "estimated", "inferred",
          "unverified", "stale", "blocked", "unknown", "not-applicable")
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}")
REPOSITORY = re.compile(r"[a-z0-9][a-z0-9-]*/(?:\.github|[a-z0-9][a-z0-9._-]*)")
SHA = re.compile(r"[a-f0-9]{40}")
HASH = re.compile(r"[a-f0-9]{64}")


def require(condition):
    if not condition:
        raise ValueError("Claim provenance is incompatible")


def parse(raw):
    require(type(raw) is bytes and 0 < len(raw) <= 1024 * 1024)
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value)
            value[key] = item
        return value
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique,
                       parse_constant=lambda _: require(False))
    queue, count = [(value, 0)], 0
    while queue:
        item, depth = queue.pop()
        count += 1
        require(depth <= 20 and count <= 8192)
        if type(item) is dict:
            queue.extend((child, depth + 1) for child in item.values())
        elif type(item) is list:
            queue.extend((child, depth + 1) for child in item)
        elif type(item) is float:
            require(math.isfinite(item))
    return value


def closed(value, keys):
    require(type(value) is dict and set(value) == set(keys))


def text(value, maximum=2048):
    require(type(value) is str and 0 < len(value) <= maximum and value.strip()
            and not any(ord(char) < 32 or ord(char) == 127 or 0xD800 <= ord(char) <= 0xDFFF for char in value))


def identity(value):
    require(type(value) is str and IDENTIFIER.fullmatch(value))


def instant(value):
    require(type(value) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value))
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError("Claim provenance clock is incompatible") from None


def version(value):
    text(value, 128)
    require(value not in ("main", "master", "latest", "HEAD", "trunk", "develop")
            and not any(char in value for char in "*^~><= "))


def number(value):
    require(type(value) in (int, float) and abs(value) <= 1e300 and math.isfinite(value))


def source_reference(value):
    closed(value, {"id", "version", "sha256"})
    identity(value["id"])
    version(value["version"])
    require(type(value["sha256"]) is str and HASH.fullmatch(value["sha256"]))


def evidence_reference(value):
    closed(value, {"access", "locator"})
    require(value["access"] in ("public", "restricted", "unavailable"))
    locator = value["locator"]
    if value["access"] != "public":
        # Opaque caller-assigned handle: no protected URLs, paths or titles.
        require(type(locator) is str and re.fullmatch(r"evidence:[a-z0-9][a-z0-9._-]{0,127}", locator))
        return
    text(locator)
    try:
        parsed = urlsplit(locator)
        require(parsed.scheme == "https" and parsed.hostname and parsed.netloc == parsed.hostname
                and not parsed.query and not parsed.fragment and "\\" not in locator
                and not any(part in (".", "..") for part in parsed.path.split("/"))
                and not any(char in locator for char in "%<>[]()"))
    except ValueError:
        raise ValueError("Claim evidence reference is incompatible") from None


def validate(value):
    closed(value, {"schema", "version", "id", "kind", "state", "visibility", "subject", "statement",
                   "environment", "procedure", "measurement", "evidence", "verification", "valid_until",
                   "superseded_by", "limitations", "exclusions", "confounders"})
    require(value["schema"] == SCHEMA and value["version"] == VERSION and value["state"] in STATES
            and value["kind"] in ("benchmark", "compatibility", "quantitative", "support")
            and value["visibility"] in ("public", "internal", "restricted", "unknown"))
    identity(value["id"])
    text(value["statement"])
    subject = value["subject"]
    closed(subject, {"id", "repository", "component", "revision", "tag", "released_version"})
    identity(subject["id"])
    identity(subject["component"])
    require(type(subject["repository"]) is str and REPOSITORY.fullmatch(subject["repository"]))
    require(subject["revision"] is None or type(subject["revision"]) is str and SHA.fullmatch(subject["revision"]))
    for field in ("tag", "released_version"):
        if subject[field] is not None:
            version(subject[field])
    environment = value["environment"]
    closed(environment, {"id", "platform", "architecture", "runtime", "dependencies"})
    for field in ("id", "platform", "architecture"):
        identity(environment[field])
    closed(environment["runtime"], {"id", "version"})
    identity(environment["runtime"]["id"])
    version(environment["runtime"]["version"])
    require(type(environment["dependencies"]) is list and len(environment["dependencies"]) <= 64)
    dependencies = []
    for dependency in environment["dependencies"]:
        source_reference(dependency)
        dependencies.append(dependency["id"])
    require(len(dependencies) == len(set(dependencies)))
    procedure = value["procedure"]
    closed(procedure, {"id", "version", "kind", "command", "configuration", "dataset", "task", "fixture", "seed"})
    identity(procedure["id"])
    version(procedure["version"])
    require(procedure["kind"] in ("command", "workflow", "adapter", "manual")
            and type(procedure["command"]) is list and len(procedure["command"]) <= 64)
    for arg in procedure["command"]:
        text(arg)
    for field in ("configuration", "dataset", "task", "fixture"):
        if procedure[field] is not None:
            source_reference(procedure[field])
    require(procedure["seed"] is None or type(procedure["seed"]) is int and 0 <= procedure["seed"] <= 2**64 - 1)
    measurement = value["measurement"]
    if measurement is not None:
        closed(measurement, {"metric", "definition", "unit", "aggregation", "sample_count", "value", "uncertainty"})
        for field in ("metric", "unit", "aggregation"):
            identity(measurement[field])
        text(measurement["definition"])
        require(type(measurement["sample_count"]) is int and measurement["sample_count"] >= 1)
        number(measurement["value"])
        uncertainty = measurement["uncertainty"]
        if uncertainty is not None:
            closed(uncertainty, {"method", "lower", "upper", "coverage"})
            identity(uncertainty["method"])
            for field in ("lower", "upper", "coverage"):
                number(uncertainty[field])
            require(uncertainty["lower"] <= uncertainty["upper"] and 0 < uncertainty["coverage"] <= 1)
    require(type(value["evidence"]) is list and len(value["evidence"]) <= 64)
    ids = []
    for evidence in value["evidence"]:
        closed(evidence, {"id", "reference", "sha256", "captured_at", "retained_until"})
        identity(evidence["id"])
        ids.append(evidence["id"])
        evidence_reference(evidence["reference"])
        require(evidence["sha256"] is None or type(evidence["sha256"]) is str and HASH.fullmatch(evidence["sha256"]))
        for field in ("captured_at", "retained_until"):
            if evidence[field] is not None:
                instant(evidence[field])
        if evidence["retained_until"] is not None:
            require(evidence["captured_at"] is not None
                    and instant(evidence["retained_until"]) >= instant(evidence["captured_at"]))
    require(len(ids) == len(set(ids)))
    verification = value["verification"]
    closed(verification, {"at", "responsible", "method", "evidence_ids"})
    require(verification["method"] in ("measurement", "bounded-probe", "provider-report", "estimate", "none"))
    if verification["at"] is not None:
        instant(verification["at"])
    if verification["responsible"] is not None:
        identity(verification["responsible"])
    require(type(verification["evidence_ids"]) is list
            and all(type(item) is str and item in ids for item in verification["evidence_ids"])
            and len(verification["evidence_ids"]) == len(set(verification["evidence_ids"])))
    if value["valid_until"] is not None:
        instant(value["valid_until"])
        require(verification["at"] is not None and instant(value["valid_until"]) > instant(verification["at"]))
    if value["superseded_by"] is not None:
        identity(value["superseded_by"])
        require(value["superseded_by"] != value["id"])
    for field in ("limitations", "exclusions", "confounders"):
        require(type(value[field]) is list and len(value[field]) <= 64)
        for item in value[field]:
            text(item)
    require(bool(value["limitations"]))
    return value


def assess(value, *, as_of):
    validate(value)
    now = instant(as_of)
    verification = value["verification"]
    for evidence in value["evidence"]:
        if evidence["captured_at"] is not None:
            require(instant(evidence["captured_at"]) <= now)
            if evidence["id"] in verification["evidence_ids"] and verification["at"] is not None:
                require(instant(evidence["captured_at"]) <= instant(verification["at"]))
    if verification["at"] is not None:
        require(instant(verification["at"]) <= now)
    used = [item for item in value["evidence"] if item["id"] in verification["evidence_ids"]]
    codes = []
    state = value["state"]
    if state in ("measured", "verified"):
        require(value["kind"] != "benchmark" or state != "verified")
        complete = (value["subject"]["revision"] is not None and verification["at"] is not None
                    and verification["responsible"] is not None and value["valid_until"] is not None
                    and all(value["environment"][field] != "unknown" for field in ("id", "platform", "architecture"))
                    and value["environment"]["runtime"]["id"] != "unknown"
                    and value["environment"]["runtime"]["version"] != "unknown"
                    and value["procedure"]["version"] != "unknown" and bool(used)
                    and all(item["sha256"] and item["captured_at"] and item["retained_until"]
                            and item["reference"]["access"] != "unavailable" for item in used))
        if state == "measured":
            complete = (complete and value["measurement"] is not None
                        and verification["method"] == "measurement"
                        and value["procedure"]["configuration"] is not None
                        and value["procedure"]["fixture"] is not None)
        else:
            complete = complete and verification["method"] == "bounded-probe"
        if not complete:
            state = "unverified"
            codes.append("PROVENANCE_INCOMPLETE")
    if value["superseded_by"] is not None:
        state = "stale"
        codes.append("SUPERSEDED")
    if value["valid_until"] is not None and now >= instant(value["valid_until"]):
        state = "stale"
        codes.append("EXPIRED")
    if any(item["retained_until"] is not None and now >= instant(item["retained_until"]) for item in used):
        state = "stale"
        codes.append("EVIDENCE_RETENTION_EXPIRED")
    return {"id": value["id"], "declared_state": value["state"], "effective_state": state,
            "positive_evidence_label_eligible": state in ("measured", "verified"),
            "scope": value["procedure"]["id"], "diagnostics": codes,
            "qualification": "provenance-structure-only-not-independent-verification"}


def project_public(value, *, as_of, public_repositories=()):
    """Caller must independently admit public repos and review safe raw references."""
    require(type(public_repositories) in (tuple, list, set, frozenset)
            and all(type(item) is str and REPOSITORY.fullmatch(item) for item in public_repositories))
    if (type(value) is not dict or value.get("visibility") != "public"
            or type(value.get("subject")) is not dict
            or type(value["subject"].get("repository")) is not str
            or value["subject"].get("repository") not in public_repositories):
        return None
    result = assess(value, as_of=as_of)
    return {"id": value["id"], "state": result["effective_state"], "subject": value["subject"]["id"],
            "revision": value["subject"]["revision"], "procedure": result["scope"],
            "attribution": value["verification"]["responsible"],
            "verified_at": value["verification"]["at"], "valid_until": value["valid_until"],
            "evidence_references": [item["reference"]["locator"] for item in value["evidence"]],
            "qualification": result["qualification"]}


def render_public(value, *, as_of, public_repositories=()):
    projection = project_public(value, as_of=as_of, public_repositories=public_repositories)
    if projection is None:
        return None
    # All interpolated fields are bounded identifiers, hashes, clocks or safe locators.
    lines = [f"Claim {projection['id']}: **{projection['state']}**", "",
             f"Subject: {projection['subject']} at {projection['revision'] or 'unknown revision'}.",
             f"Procedure: {projection['procedure']}; verification: {projection['verified_at'] or 'unknown'}; expires: {projection['valid_until'] or 'unknown'}.",
             f"Attributed workflow/source/reviewer: {projection['attribution'] or 'unknown'}.",
             "Provenance structure only; no independent scientific verification.", "", "Evidence references:"]
    for reference in projection["evidence_references"]:
        lines.append(f"- [{reference}]({reference})" if reference.startswith("https://") else f"- Safe evidence reference: {reference}")
    if not projection["evidence_references"]:
        lines.append("- unavailable; no positive evidence label")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--as-of", required=True)
    args = parser.parse_args()
    try:
        with args.input.open("rb") as source:
            value = parse(source.read(1024 * 1024 + 1))
        result = assess(value, as_of=args.as_of)
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OSError):
        print("Claim provenance is incompatible", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
