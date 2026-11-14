#!/usr/bin/env python3
"""Advisory diagnosis-capability declarations; never parse records or crawl paths.

Inputs are caller-declared observations, not authenticated repository evidence.
Public projection excludes private/unknown visibility before inspecting payloads.
No output establishes health, diagnosis truth, remediation or publication authority.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "egohygiene.repository-diagnosis-capability/v1"
VERSION = "1.0.0-alpha.1"
CAPABILITY = "repository.diagnosis-records"
STATES = ("optional", "recommended", "required", "not-applicable", "unknown", "blocked")
OBSERVATIONS = ("not-collected", "no-records", "no-recent-records", "available", "unavailable")
PUBLIC_FIELDS = ("capability", "applicability", "adoption", "freshness")
SHA = re.compile(r"[0-9a-f]{40}")
HASH = re.compile(r"[0-9a-f]{64}")


def require(condition):
    if not condition:
        raise ValueError("Diagnosis capability declaration is incompatible")


def parse(content):
    require(type(content) is bytes and 0 < len(content) <= 1024 * 1024)
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value)
            value[key] = item
        return value
    value = json.loads(content.decode("utf-8"), object_pairs_hook=unique,
                       parse_constant=lambda _: require(False))
    pending = [(value, 0)]
    count = 0
    while pending:
        item, depth = pending.pop()
        count += 1
        require(depth <= 20 and count <= 4096)
        if type(item) is dict:
            pending.extend((child, depth + 1) for child in item.values())
        elif type(item) is list:
            pending.extend((child, depth + 1) for child in item)
        elif type(item) is float:
            require(False)
    return value


def closed(value, keys):
    require(type(value) is dict and set(value) == set(keys))


def text(value, maximum=512):
    require(type(value) is str and 0 < len(value) <= maximum and value.strip()
            and not any(ord(char) < 32 or ord(char) == 127 or 0xD800 <= ord(char) <= 0xDFFF
                        for char in value))


def instant(value):
    require(type(value) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value))
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError("Diagnosis capability timestamp is incompatible") from None


def safe_path(value):
    text(value, 240)
    require(not value.startswith("/") and "\\" not in value and ":" not in value
            and not any(char in value for char in "%*?[]#")
            and all(part not in ("", ".", "..") and part.casefold() != ".git"
                    for part in value.split("/")))
    return value


def policy():
    value = parse((ROOT / "catalog/repository-diagnosis-policy.json").read_bytes())
    require(value["schema"] == "egohygiene.repository-diagnosis-policy/v1"
            and value["version"] == VERSION and value["status"] == "proposed"
            and value["approval"] is None and value["enforcement"] == "observe")
    return value


def validate(value):
    """Validate only this Hygiene declaration, not Aether front matter or records."""
    selected = policy()
    closed(value, {"schema", "version", "capability", "repository", "visibility", "represented_revision",
                   "applicability", "adoption", "record_contract", "records_path", "alternative_path_reason",
                   "privacy", "retention", "index", "observation"})
    require(value["schema"] == SCHEMA and value["version"] == VERSION and value["capability"] == CAPABILITY)
    require(type(value["repository"]) is str and re.fullmatch(r"[a-z0-9][a-z0-9-]*/(?:\.github|[a-z0-9][a-z0-9._-]*)", value["repository"]))
    require(value["visibility"] in ("public", "internal", "private", "unknown"))
    require(type(value["represented_revision"]) is str and SHA.fullmatch(value["represented_revision"]))
    for field, states in (("applicability", STATES), ("adoption", ("enabled", "opted-out", "undecided"))):
        closed(value[field], {"state", "reason"})
        require(value[field]["state"] in states)
        text(value[field]["reason"])
    require(value["record_contract"] == selected["upstream"])
    safe_path(value["records_path"])
    if value["records_path"] == selected["canonical_path"]:
        require(value["alternative_path_reason"] is None)
    else:
        text(value["alternative_path_reason"])
    privacy = value["privacy"]
    closed(privacy, {"default_sensitivity", "publication", "public_fields"})
    require(privacy["default_sensitivity"] in ("internal", "restricted")
            and privacy["publication"] in ("none", "allowlisted-metadata"))
    fields = privacy["public_fields"]
    require(type(fields) is list and all(type(item) is str and item in PUBLIC_FIELDS for item in fields)
            and len(fields) == len(set(fields)))
    require((privacy["publication"] == "none" and not fields)
            or (privacy["publication"] == "allowlisted-metadata" and bool(fields)
                and value["visibility"] == "public"))
    retention = value["retention"]
    closed(retention, {"days", "disposition", "reason"})
    require(retention["days"] is None or type(retention["days"]) is int and 1 <= retention["days"] <= 36500)
    require(retention["disposition"] == "review-before-delete")
    text(retention["reason"])
    index = value["index"]
    closed(index, {"mode", "owner", "max_age_days"})
    require(index["mode"] in ("none", "ephemeral", "tracked") and index["owner"] == value["repository"]
            and type(index["max_age_days"]) is int and 1 <= index["max_age_days"] <= 365)
    observation = value["observation"]
    closed(observation, {"state", "observed_at", "source_revision", "index_generated_at", "source_digest"})
    require(observation["state"] in OBSERVATIONS)
    if observation["state"] in ("not-collected", "unavailable"):
        require(all(observation[field] is None for field in ("observed_at", "source_revision", "index_generated_at", "source_digest")))
    else:
        instant(observation["observed_at"])
        require(type(observation["source_revision"]) is str and SHA.fullmatch(observation["source_revision"])
                and type(observation["source_digest"]) is str and HASH.fullmatch(observation["source_digest"]))
        if index["mode"] == "none":
            require(observation["index_generated_at"] is None)
        else:
            require(instant(observation["index_generated_at"]) >= instant(observation["observed_at"]))
    return value


def assess(value, *, as_of):
    """Return local review metadata from an explicit clock; never a health pass."""
    validate(value)
    now = instant(as_of)
    observation = value["observation"]
    codes = []
    freshness = "unavailable"
    if observation["observed_at"] is not None:
        clock = instant(observation["observed_at"])
        require(clock <= now)
        if observation["index_generated_at"] is not None:
            require(instant(observation["index_generated_at"]) <= now)
        freshness = "fresh" if (now - clock).total_seconds() <= value["index"]["max_age_days"] * 86400 else "stale"
        if observation["source_revision"] != value["represented_revision"]:
            freshness = "source-mismatch"
        if freshness != "fresh":
            codes.append("INDEX_" + freshness.upper().replace("-", "_"))
    if value["applicability"]["state"] == "required" and value["adoption"]["state"] != "enabled":
        codes.append("REQUIRED_ADOPTION_REVIEW")
    if value["applicability"]["state"] in ("unknown", "blocked"):
        codes.append("APPLICABILITY_" + value["applicability"]["state"].upper())
    return {"capability": CAPABILITY, "applicability": value["applicability"]["state"],
            "adoption": value["adoption"]["state"], "observation": observation["state"],
            "freshness": freshness, "health": "unknown", "diagnostics": codes,
            "qualification": "caller-declared-structural-review-only"}


def public_projection(value, *, as_of):
    """No protected identity, filenames, counts, clocks, reasons or placeholders."""
    if type(value) is not dict or value.get("visibility") != "public":
        return None
    result = assess(value, as_of=as_of)
    if value["privacy"]["publication"] != "allowlisted-metadata":
        return None
    return {key: result[key] for key in value["privacy"]["public_fields"]}


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
        print("Diagnosis capability declaration is incompatible", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
