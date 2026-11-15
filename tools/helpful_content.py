#!/usr/bin/env python3
"""Reference metadata checks for proposed editorial policy; no quality scoring.

No network, source fetching, publication, clock reads or review authentication.
Callers independently verify actual content bytes, sources and human judgments.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "catalog/helpful-content-profile.json"
VERSION = "1.0.0-alpha.1"
MAX_BYTES = 1024 * 1024


class ContentError(ValueError):
    """Generic diagnostic intentionally withholds rejected source data."""


def require(condition):
    if not condition:
        raise ContentError("Content profile/evidence is incompatible or unavailable")


def load(path):
    require(all(hasattr(os, name) for name in ("O_NOFOLLOW", "O_NONBLOCK")))
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result)
            result[key] = value
        return result
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        require(stat.S_ISREG(metadata.st_mode) and 0 < metadata.st_size <= MAX_BYTES)
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES)
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ContentError("Nonfinite JSON")))


def validate_schema(value, name):
    schema = load(ROOT / "schemas" / name)
    require(Draft202012Validator(schema, format_checker=FormatChecker()).is_valid(value))


def reference(value):
    require(isinstance(value, str) and value and "\\" not in value
            and not any(ord(c) < 32 or ord(c) == 127 for c in value))
    parsed = urlsplit(value)
    if parsed.scheme:
        require(parsed.scheme == "https" and parsed.hostname
                and parsed.username is None and parsed.password is None)
    else:
        require(parsed.path and not parsed.path.startswith("/")
                and all(part not in {"", ".", ".."} for part in parsed.path.split("/")))


def timestamp(value):
    require(isinstance(value, str) and value.endswith("Z"))
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None and result.utcoffset().total_seconds() == 0)
    return result.astimezone(timezone.utc)


def validate_profile(profile):
    validate_schema(profile, "helpful-content-profile.v1.schema.json")
    sources = {source["id"]: source for source in profile["sources"]}
    require(len(sources) == len(profile["sources"]))
    for source in sources.values():
        reference(source["url"])
        timestamp(source["observed_at"])
    rules = {rule["id"]: rule for rule in profile["rules"]}
    require(len(rules) == 18 and set(rules) == {f"HC-{index:03d}" for index in range(1, 19)})
    schema = load(ROOT / "schemas/content-quality-evidence.v1.schema.json")
    fields = schema["properties"]["evidence"]["properties"]
    for rule in rules.values():
        require(set(rule["sources"]) <= sources.keys()
                and set(rule["evidence_fields"]) <= fields.keys())
    return profile


def references(value):
    if isinstance(value, dict):
        if "reference" in value and "visibility" in value:
            yield value
        for item in value.values():
            yield from references(item)
    elif isinstance(value, list):
        for item in value:
            yield from references(item)


def validate_evidence(data, profile):
    validate_schema(data, "content-quality-evidence.v1.schema.json")
    rules = {rule["id"]: rule for rule in profile["rules"]}
    ids = set()
    for claim in data["reviewer_claims"]:
        require(claim["rule_id"] in rules and rules[claim["rule_id"]]["verification"] == "human"
                and claim["rule_id"] not in ids)
        ids.add(claim["rule_id"])
    for source in references(data):
        reference(source["reference"])
        require(data["visibility"] != "public" or source["visibility"] == "public")
    corrections = {item["id"]: item for item in data["evidence"]["corrections"]}
    require(len(corrections) == len(data["evidence"]["corrections"]))
    pending, visited = set(), set()
    def visit(identity):
        require(identity in corrections and identity not in pending)
        if identity not in visited:
            pending.add(identity)
            for prior in corrections[identity]["supersedes"]:
                visit(prior)
            pending.remove(identity)
            visited.add(identity)
    for identity in corrections:
        visit(identity)
    return data


def applicability(rule, subject):
    kind = rule["applicability"]
    if kind == "all":
        return "required"
    if kind == "current":
        return "not-applicable" if subject["lifecycle"] == "archived" else "required"
    if kind == "archived":
        return "required" if subject["lifecycle"] == "archived" else "not-applicable"
    if kind == "high-stakes":
        return "unknown" if subject["risk_profile"] == "unknown" else (
            "required" if subject["risk_profile"] == "high-stakes" else "not-applicable")
    value = subject["ai_assisted" if kind == "ai-assisted" else "localized"]
    return "unknown" if value is None else "required" if value else "not-applicable"


def assess(data, profile, *, as_of, public_output=False):
    validate_profile(profile)
    validate_evidence(data, profile)
    require(not public_output or data["visibility"] == "public")
    now = timestamp(as_of)
    subject, evidence = data["subject"], data["evidence"]
    claims = {item["rule_id"]: item for item in data["reviewer_claims"]}
    results = []
    for rule in profile["rules"]:
        applies = applicability(rule, subject)
        state = "present"
        reason = "declared-metadata-only"
        if applies != "required":
            state = applies
        elif any(evidence[field] is None or evidence[field] == ""
                 or (field == "source_refs" and not evidence[field]) for field in rule["evidence_fields"]):
            state = "missing"
        elif rule["id"] == "HC-006":
            if any(source["observed_at"] is not None and timestamp(source["observed_at"]) > now
                   for source in evidence["source_refs"]):
                state = "blocked"
            elif any(source["observed_at"] is None or source["sha256"] is None
                     for source in evidence["source_refs"]):
                state = "partial"
        elif rule["id"] in {"HC-010", "HC-015"}:
            review = evidence["content_review" if rule["id"] == "HC-010" else "specialist_review"]
            if review["content_revision"] != subject["content_revision"] or timestamp(review["reviewed_at"]) > now:
                state = "blocked"
            elif rule["id"] == "HC-010" and (now - timestamp(review["reviewed_at"])).total_seconds() > review["interval_days"] * 86400:
                state = "stale"
        elif rule["id"] == "HC-011":
            if subject["lifecycle"] == "superseded" and evidence["superseded_by"] is None:
                state = "missing"
            elif any(timestamp(event["recorded_at"]) > now for event in evidence["corrections"]):
                state = "blocked"
        elif rule["id"] == "HC-012" and timestamp(evidence["archive"]["archived_at"]) > now:
            state = "blocked"
        human = rule["verification"] == "human" and applies == "required"
        claim = claims.get(rule["id"])
        reported = "absent"
        if claim and human:
            reported = "reported-" + claim["judgment"]
            if claim["content_revision"] != subject["content_revision"] or timestamp(claim["reviewed_at"]) > now:
                reported = "stale-or-unbound-claim"
            elif evidence["content_review"] is not None and (
                    now - timestamp(claim["reviewed_at"])).total_seconds() > evidence["content_review"]["interval_days"] * 86400:
                reported = "stale-or-unbound-claim"
        results.append({"rule_id": rule["id"], "applicability": applies, "metadata_state": state,
                        "reason": reason, "human_review": "independent-review-required" if human else "not-applicable",
                        "reported_judgment": reported, "review_authenticity": "not-verified" if human else "not-assessed"})
    states = {item["metadata_state"] for item in results}
    metadata_state = ("blocked" if "blocked" in states else "stale" if "stale" in states
                      else "partial" if states & {"missing", "partial"} else "unknown" if "unknown" in states
                      else "intentionally-archived" if subject["lifecycle"] == "archived" else "metadata-ready")
    return {"profile": "egohygiene.helpful-content-profile/v1", "contract_version": VERSION,
            "evaluation_scope": "metadata-reference-only",
            "policy_status": "proposed", "visibility": data["visibility"], "subject": subject["id"],
            "content_revision": subject["content_revision"], "as_of": as_of, "metadata_state": metadata_state,
            "human_review_required": any(row["human_review"] == "independent-review-required" for row in results),
            "publication_decision": "not-supplied", "source_truth": "not-verified", "rules": results}


def validate_fixtures(profile):
    expectations = load(ROOT / "fixtures/helpful-content/expectations.json")
    for name, expected in expectations["cases"].items():
        data = load(ROOT / f"fixtures/helpful-content/{name}.json")
        result = assess(data, profile, as_of=expectations["as_of"], public_output=True)
        require(result["metadata_state"] == expected and result["human_review_required"]
                and result["publication_decision"] == "not-supplied")
    return len(expectations["cases"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate-profile", "validate-fixtures", "assess"))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--as-of")
    parser.add_argument("--public-output", action="store_true")
    args = parser.parse_args()
    try:
        profile = validate_profile(load(PROFILE))
        if args.command == "assess":
            require(args.input is not None and args.as_of is not None)
            print(json.dumps(assess(load(args.input), profile, as_of=args.as_of,
                                   public_output=args.public_output), sort_keys=True))
        else:
            count = validate_fixtures(profile) if args.command == "validate-fixtures" else len(profile["rules"])
            print(json.dumps({"status": "pass", "checked": count, "scope": "proposed reference source only; no content/review certification"}))
    except (OSError, ValueError, TypeError, KeyError, RecursionError):
        print("Content profile/evidence unavailable or incompatible; source content withheld")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
