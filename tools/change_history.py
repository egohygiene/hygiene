#!/usr/bin/env python3
"""Pure advisory reference for the proposed Hygiene change-history contract.

No Git access, repository mutation, version selection, enforcement, signature
verification or publication occurs. Diagnostics never echo message prose,
actor/trailer values, scope names or input digests. Production lint belongs to
EgoLint and operational preview/apply belongs to Relay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
POLICY_SCHEMA = "egohygiene.change-history-policy/v1"
INPUT_SCHEMA = "egohygiene.change-history-input/v1"
OUTPUT_SCHEMA = "egohygiene.change-history-analysis/v1"
VERSION = "1.0.0-alpha.1"
POLICY_SHA256 = "0a0076e9f80787fc4660cf522ea9f3068ace4525eaca0e175bd8cc21a755a014"
CONTEXTS = {"commit", "pr_title", "bot", "dependency", "generated", "release", "merge"}
HEADER = re.compile(r"([a-z][a-z0-9-]*)\(([a-z0-9][a-z0-9._/-]{0,63})\)(!)?: (\S+) (.+)")
TRAILER = re.compile(r"(BREAKING CHANGE|[A-Za-z][A-Za-z0-9.-]*): (.+)")


def require(condition):
    if not condition:
        raise ValueError("Change-history input is incompatible")


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def parse(content):
    require(type(content) is bytes and 0 < len(content) <= 262144)
    def unique(items):
        value = {}
        for key, item in items:
            require(key not in value)
            value[key] = item
        return value
    value = json.loads(content.decode("utf-8", errors="strict"), object_pairs_hook=unique,
                       parse_constant=lambda _: require(False))
    encoded(value)
    return value


def read_input(path):
    """Bound local source reads before allocation; pipes and links are not input."""
    require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"))
    path = path.absolute()
    require(not any(item.is_symlink() for item in (path, *path.parents)))
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        metadata = os.fstat(descriptor)
        require(stat.S_ISREG(metadata.st_mode) and 0 < metadata.st_size <= 262144)
        with os.fdopen(descriptor, "rb") as source:
            descriptor = None
            content = source.read(262145)
        require(0 < len(content) <= 262144)
        return content
    finally:
        if descriptor is not None:
            os.close(descriptor)


def policy():
    raw = read_input(ROOT / "catalog/change-history-policy.json")
    require(hashlib.sha256(raw).hexdigest() == POLICY_SHA256)
    value = parse(raw)
    require(value["schema"] == POLICY_SCHEMA and value["version"] == VERSION
            and value["status"] == "proposed" and value["approval"] is None
            and value["enforcement"] == "observe")
    return value


def footer_block(lines):
    """Read the bounded final trailer block, preserving all values privately."""
    while lines and lines[-1] == "":
        lines = lines[:-1]
    start = max((index + 1 for index, line in enumerate(lines) if line == ""), default=0)
    block = lines[start:]
    if not block or not TRAILER.fullmatch(block[0]):
        return [], []
    trailers, errors = [], []
    for line in block:
        match = TRAILER.fullmatch(line)
        if match:
            trailers.append((match[1], match[2]))
        elif line.startswith((" ", "\t")) and trailers:
            name, value = trailers[-1]
            trailers[-1] = (name, value + "\n" + line.lstrip())
        else:
            errors.append("TRAILER_CONTINUATION")
    return trailers, errors


def analyze(value):
    """Return text-free syntax and release hints; caller still owns release truth.

    Protected/unknown source claims are omitted before inspecting messages,
    lengths, context, scope or trailers. A public flag is not provider admission;
    this local reference is not a public fleet evidence producer.
    """
    selected = policy()
    result = {"schema": OUTPUT_SCHEMA, "contract_version": VERSION,
        "policy": {"schema": POLICY_SCHEMA, "version": VERSION, "status": "proposed", "sha256": POLICY_SHA256},
        "publication": "local-review-only", "syntax": "not_admitted", "type": None,
        "scope_state": "not_inspected", "breaking": None, "release_hint": "none", "trailers": [],
        "diagnostics": [], "qualification": {"enforcement": "not-activated", "human_approval": "not-inferred",
            "identity_signature_dco": "not-verified", "release_version": "repository-aether-authority"}}
    if type(value) is not dict or value.get("visibility") != "public":
        result["diagnostics"] = ["SOURCE_NOT_ADMITTED"]
        return result
    require(set(value) == {"schema", "visibility", "context", "message", "parent_count"}
            and value["schema"] == INPUT_SCHEMA and value["context"] in CONTEXTS
            and type(value["message"]) is str and len(value["message"].encode("utf-8")) <= 65536
            and type(value["parent_count"]) is int and 0 <= value["parent_count"] <= 32)
    message = value["message"].replace("\r\n", "\n")
    require(message and "\r" not in message and "\x00" not in message)
    if value["context"] == "merge":
        require(value["parent_count"] >= 2)
        result.update(syntax="context_only", release_hint="review_required", diagnostics=["MERGE_CONTEXT_ONLY"])
        return result
    errors = []
    if value["context"] == "pr_title" and "\n" in message:
        errors.append("PR_TITLE_MULTILINE")
    if value["parent_count"] > 1:
        errors.append("MERGE_CONTEXT_REQUIRED")
    lines = message.rstrip("\n").split("\n")
    subject, body = lines[0], lines[1:]
    if value["context"] == "pr_title" and body:
        errors.append("PR_TITLE_MULTILINE")
    if body and body[0] != "":
        errors.append("BODY_SEPARATOR")
    if len(subject) > selected["subject"]["maximum_code_points"]:
        errors.append("SUBJECT_LENGTH")
    if unicodedata.normalize("NFC", subject) != subject:
        errors.append("SUBJECT_UNICODE")
    if any(ord(character) < 32 or ord(character) == 127 for character in subject):
        errors.append("SUBJECT_CONTROL")
    match = HEADER.fullmatch(subject)
    types = {row["type"]: row for row in selected["types"]}
    trailers, trailer_errors = footer_block(body)
    errors.extend(trailer_errors)
    names = [name for name, unused in trailers]
    unknown = set(names) - set(selected["trailers"]["allowed_tokens"])
    if unknown:
        errors.append("TRAILER_UNREGISTERED")
    # A recognized breaking line outside the selected final block is rejected,
    # rather than silently yielding a no-breaking release hint.
    breaking_lines = [line for line in body if line.startswith(("BREAKING CHANGE:", "BREAKING-CHANGE:"))]
    breaking_values = [item for name, item in trailers if name in selected["breaking"]["footer_tokens"]]
    if len(breaking_lines) != len(breaking_values):
        errors.append("BREAKING_MARKER_LOCATION")
    result["trailers"] = sorted(set(names) & set(selected["trailers"]["allowed_tokens"]))
    hint, breaking = "review_required", bool(breaking_values)
    if match is None:
        errors.append("SUBJECT_SHAPE")
        result["scope_state"] = "invalid"
    else:
        type_name, scope, marker, emoji, description = match.groups()
        result["scope_state"] = "present"
        if any(part in selected["subject"]["scope_forbidden_segments"] for part in scope.split("/")) or scope.endswith(tuple(selected["subject"]["scope_forbidden_suffixes"])):
            errors.append("SCOPE_SHAPE")
        if type_name not in types:
            errors.append("TYPE_UNREGISTERED")
        else:
            row = types[type_name]
            result["type"] = type_name
            hint = row["release_hint"]
            if emoji != row["emoji"]:
                errors.append("EMOJI_MISMATCH")
        if not re.match(r"[a-z]", description):
            errors.append("DESCRIPTION_INITIAL")
        if description != description.strip() or description.endswith(".") or "  " in description:
            errors.append("DESCRIPTION_SHAPE")
        if description.lower() in selected["subject"]["placeholder_descriptions"]:
            errors.append("PLACEHOLDER")
        breaking = breaking or marker is not None
        if type_name == "revert":
            targets = [item for name, item in trailers if name == "Reverts"]
            if len(targets) != 1 or not re.fullmatch(selected["revert"]["target_pattern"], targets[0]):
                errors.append("REVERT_TARGET_REQUIRED")
            hint = "review_required"
        if value["context"] == "release" and (type_name != "chore" or scope != "release" or breaking):
            errors.append("RELEASE_CONTEXT")
    if breaking and result["type"] != "revert":
        hint = "major"
    if value["context"] == "release":
        hint = "none"
    result["breaking"] = breaking
    result["diagnostics"] = sorted(set(errors))
    result["syntax"] = "invalid" if errors else "valid"
    result["release_hint"] = "review_required" if errors else hint
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Explicit local UTF-8 JSON input envelope; never Git history.")
    args = parser.parse_args()
    try:
        result = analyze(parse(read_input(args.input)))
    except (ValueError, OSError, KeyError, TypeError, UnicodeError, RecursionError, OverflowError):
        print("Change-history source/profile unavailable or incompatible", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(encoded(result))
    return 1 if result["syntax"] == "invalid" else 0


if __name__ == "__main__":
    raise SystemExit(main())
