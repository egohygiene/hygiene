#!/usr/bin/env python3
"""Reference checks for proposed organization strategy; no collection or mutation."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime
import json
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "egohygiene.organization-roadmap/v1"
VERSION = "1.0.0-alpha.1"
DEFAULT = ROOT / "organization/roadmap.v1.json"
RANK = {"public": 0, "internal": 1, "private": 2}
STATES = {"proposed", "planned", "ready", "active", "blocked", "paused", "completed",
          "deferred", "superseded", "optional", "unknown"}
SOURCE_KINDS = {"roadmap", "architecture_decision", "git", "github_issue", "github_pull_request",
                "check_provider", "release", "deployment", "manual"}
REPOSITORY = re.compile(r"egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)\Z")
INITIATIVE = re.compile(r"ORG-I[0-9]{3,}\Z")


def require(value):
    if not value:
        raise ValueError("Organization roadmap incompatible; inspect the contract and source privately")


def fields(value, expected):
    require(type(value) is dict and set(value) == set(expected.split()))


def text(value):
    require(type(value) is str and 0 < len(value) <= 2048
            and not any(ord(char) < 32 or ord(char) == 127 for char in value))


def timestamp(value):
    require(type(value) is str and value.endswith("Z"))
    return datetime.fromisoformat(value[:-1] + "+00:00")


def encoded(value):
    return json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result)
            result[key] = value
        return result
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        require(stat.S_ISREG(metadata.st_mode) and 0 < metadata.st_size <= 1024 * 1024)
        raw = stream.read(1024 * 1024 + 1)
    require(len(raw) <= 1024 * 1024)
    value = json.loads(raw, object_pairs_hook=unique, parse_constant=lambda _: require(False))
    pending, count = [(value, 0)], 0
    while pending:
        item, depth = pending.pop()
        count += 1
        require(depth <= 24 and count <= 20000)
        if type(item) is dict:
            pending.extend((child, depth + 1) for child in item.values())
        elif type(item) is list:
            pending.extend((child, depth + 1) for child in item)
    return value


def unique_index(rows):
    require(type(rows) is list)
    result = {}
    for row in rows:
        require(type(row) is dict and type(row.get("id")) is str and row["id"] not in result)
        result[row["id"]] = row
    return result


def validate(data):
    fields(data, "schema contract_version status approval organization canonical_repository visibility updated_at sources initiatives events")
    require(data["schema"] == SCHEMA and data["contract_version"] == VERSION
            and data["status"] == "proposed" and data["approval"] is None
            and data["organization"] == "egohygiene" and data["canonical_repository"] == "egohygiene/hygiene"
            and data["visibility"] in RANK)
    observed = timestamp(data["updated_at"])
    sources = unique_index(data["sources"])
    initiatives = unique_index(data["initiatives"])
    for source in sources.values():
        fields(source, "id kind url repository revision observed_at visibility assertion freshness")
        text(source["url"])
        require(re.fullmatch(r"source:[a-z0-9][a-z0-9._-]*", source["id"])
                and source["kind"] in SOURCE_KINDS and REPOSITORY.fullmatch(source["repository"])
                and source["assertion"] in {"authoritative", "inferred", "unknown"}
                and source["freshness"] in {"current", "stale", "unknown", "not_applicable"}
                and source["visibility"] in RANK and RANK[source["visibility"]] <= RANK[data["visibility"]]
                and timestamp(source["observed_at"]) <= observed)
        require(source["revision"] is None or re.fullmatch(r"[0-9a-f]{40}", source["revision"]))
        url = urlsplit(source["url"])
        require(url.scheme == "https" and url.netloc == "github.com" and not url.username
                and not url.query and url.path.startswith("/" + source["repository"] + "/"))
        if source["revision"] is not None:
            require("/" + source["revision"] in url.path)

    def provenance(row):
        require(type(row["provenance"]) is list and row["provenance"]
                and len(set(row["provenance"])) == len(row["provenance"]))
        require(all(key in sources and RANK[sources[key]["visibility"]] <= RANK[row["visibility"]]
                    for key in row["provenance"]))

    for row in initiatives.values():
        fields(row, "id title outcome owner horizon state assertion freshness visibility provenance review repository_nodes links depends_on supersedes superseded_by")
        require(INITIATIVE.fullmatch(row["id"]) and REPOSITORY.fullmatch(row["owner"])
                and row["horizon"] in {"now", "next", "later", "maybe"} and row["state"] in STATES
                and row["assertion"] in {"authoritative", "inferred", "unknown"}
                and row["freshness"] in {"current", "stale", "unknown", "not_applicable"}
                and row["visibility"] in RANK and RANK[row["visibility"]] <= RANK[data["visibility"]])
        text(row["title"]); text(row["outcome"])
        # Markdown rendering treats all supplied prose as text, not markup.
        require(not any(char in row["title"] + row["outcome"] for char in "<>[]`\\"))
        provenance(row)
        if row["assertion"] == "authoritative":
            require(row["review"] in sources)
            review = sources[row["review"]]
            require(review["kind"] == "manual" and review["assertion"] == "authoritative"
                    and "#issuecomment-" in review["url"] and row["review"] in row["provenance"])
        else:
            require(row["review"] is None)
        require(type(row["repository_nodes"]) is list and type(row["links"]) is list)
        seen_nodes = set()
        for node in row["repository_nodes"]:
            fields(node, "repository key visibility applicability provenance")
            require(REPOSITORY.fullmatch(node["repository"]) and re.fullmatch(r"[A-Z][A-Z0-9-]{1,79}", node["key"])
                    and (node["repository"], node["key"]) not in seen_nodes
                    and node["visibility"] in RANK and RANK[node["visibility"]] <= RANK[data["visibility"]]
                    and node["applicability"] in {"active", "archived", "not_applicable"})
            seen_nodes.add((node["repository"], node["key"]))
            provenance(node)
            require(any(sources[key]["repository"] == node["repository"] and sources[key]["kind"] == "roadmap"
                        for key in node["provenance"]))
        for link in row["links"]:
            fields(link, "type source")
            require(link["type"] in {"tracks", "informs", "evidences", "releases"} and link["source"] in sources)
        if row["state"] == "completed" and row["assertion"] == "authoritative":
            require(any(link["type"] == "evidences" and sources[link["source"]]["kind"] in
                        {"check_provider", "release", "deployment"} for link in row["links"]))
        for key in ("depends_on", "supersedes", "superseded_by"):
            require(type(row[key]) is list and len(set(row[key])) == len(row[key])
                    and all(target in initiatives and target != row["id"] for target in row[key]))
        require((row["state"] == "superseded") == bool(row["superseded_by"]))
        for key, inverse in (("supersedes", "superseded_by"), ("superseded_by", "supersedes")):
            require(all(row["id"] in initiatives[target][inverse] for target in row[key]))
    for relation in ("depends_on", "supersedes"):
        visited, pending = set(), set()
        def visit(identity):
            require(identity not in pending)
            if identity not in visited:
                pending.add(identity)
                for target in initiatives[identity][relation]: visit(target)
                pending.remove(identity); visited.add(identity)
        for identity in initiatives: visit(identity)
    for event in unique_index(data["events"]).values():
        fields(event, "id type subject occurred_at recorded_at actor changes visibility assertion freshness provenance extensions")
        require(event["type"] in {"roadmap_step.created", "roadmap_step.status_changed"}
                and event["subject"] in {"ri:egohygiene/hygiene:roadmap-step:" + key for key in initiatives}
                and timestamp(event["occurred_at"]) <= timestamp(event["recorded_at"]) <= observed
                and event["visibility"] in RANK and RANK[event["visibility"]] <= RANK[data["visibility"]]
                and event["assertion"] in {"inferred", "unknown"} and event["actor"] is None
                and event["freshness"] in {"current", "stale", "unknown", "not_applicable"}
                and event["changes"] == [] and event["extensions"] == {})
        require(re.fullmatch(r"event:[a-z0-9][a-z0-9._-]*", event["id"]))
        provenance(event)
    return data


def validate_transition(previous, current):
    validate(previous); validate(current)
    old, new = unique_index(previous["initiatives"]), unique_index(current["initiatives"])
    require(set(old) <= set(new))  # Retire/supersede IDs; never erase or reuse them.
    for identity in old:
        if old[identity] != new[identity] and new[identity]["assertion"] == "authoritative":
            require(new[identity]["review"] != old[identity]["review"])


def public_projection(data):
    """Filter before rendering; disclose no protected names, IDs, counts or URLs."""
    validate(data)
    result = copy.deepcopy(data)
    sources = {row["id"]: row for row in result["sources"] if row["visibility"] == "public"}
    rows = {row["id"]: row for row in result["initiatives"] if row["visibility"] == "public"}
    # A hidden dependency/supersession must not turn an initiative into an
    # apparently independent or newly ready item. Omit the complete unit.
    while True:
        omitted = {key for key, row in rows.items()
                   if any(target not in rows for relation in ("depends_on", "supersedes", "superseded_by") for target in row[relation])}
        if not omitted: break
        rows = {key: row for key, row in rows.items() if key not in omitted}
    for row in rows.values():
        row["repository_nodes"] = [node for node in row["repository_nodes"] if node["visibility"] == "public"]
        row["links"] = [link for link in row["links"] if link["source"] in sources]
    result["visibility"] = "public"
    result["initiatives"] = sorted(rows.values(), key=lambda row: row["id"])
    subjects = {"ri:egohygiene/hygiene:roadmap-step:" + key for key in rows}
    result["events"] = [event for event in result["events"] if event["visibility"] == "public" and event["subject"] in subjects]
    needed = set()
    for row in result["initiatives"] + result["events"]:
        needed.update(row["provenance"])
    for row in result["initiatives"]:
        for node in row["repository_nodes"]: needed.update(node["provenance"])
        needed.update(link["source"] for link in row["links"])
    result["sources"] = sorted((row for key, row in sources.items() if key in needed), key=lambda row: row["id"])
    # An empty public view is valid output, but not a new canonical strategy.
    return result


def render(data):
    public = public_projection(data)
    lines = ["# Ego Hygiene organization roadmap", "", "<!-- Generated from roadmap.v1.json; edit that canonical source. -->", "",
             "Proposed strategy under [the organization-roadmap contract](../docs/ecosystem/ORGANIZATION_ROADMAP.md).",
             "Hygiene's [repository roadmap](../ROADMAP.md) remains separate. All initiative placement below is a reviewable proposal.",
             "The [organization execution plan](https://github.com/egohygiene/.github/tree/main/docs/coordination) owns the current issue queue.", "",
             "## Strategic context", "", "Build independently useful tools that compose through versioned contracts, preserve provenance and keep consequential choices reviewable.",
             "This is a public projection of declared strategy, not an exhaustive repository or participant inventory. Source tests and merged PRs do not ratify priority.", ""]
    for horizon in ("now", "next", "later", "maybe"):
        lines.extend(["## " + horizon.title(), ""])
        for row in public["initiatives"]:
            if row["horizon"] != horizon: continue
            lines.extend(["### " + row["id"] + " — " + row["title"], "",
                          row["outcome"], "",
                          f'Owner: `{row["owner"]}`. State: `{row["state"]}`; assertion: `{row["assertion"]}`; freshness: `{row["freshness"]}`.', "",
                          "Depends on: " + (", ".join(row["depends_on"]) or "no declared initiative dependency") + ".", ""])
            if row["repository_nodes"]:
                lines.extend(["Repository strategy:", ""])
                for node in row["repository_nodes"]:
                    lines.append(f'- [{node["repository"]} {node["key"]}](https://github.com/{node["repository"]}/blob/main/ROADMAP.md) ({node["applicability"]}).')
                lines.append("")
    lines.extend(["## Dependencies, uncertainty and review", "",
                  "Contracts and trustworthy evidence unblock qualified delivery and control-plane integration; those streams can progress independently after their shared prerequisites. Consumer proof precedes reusable fleet materialization.",
                  "Existing repository strategy IDs remain owned locally. Release acceptance, human ADR disposition, fleet adoption and source-rights clearance retain their own gates. Optional research stays optional.",
                  "Human review may change this proposed ordering. No target dates or activity-derived reprioritization are inferred. Pace's focus queue is a separate execution projection.", "",
                  "## Validation", "", "`python3 tools/organization_roadmap.py check-generated` checks this view. The contract defines identity, provenance, privacy, transitions and rollback; synthetic tests do not prove live adoption or human approval.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "public", "render", "check-generated"))
    parser.add_argument("--input", type=Path, default=DEFAULT)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    try:
        data = validate(load(args.input))
        if args.previous: validate_transition(load(args.previous), data)
        if args.command == "public": print(encoded(public_projection(data)), end="")
        elif args.command == "render": print(render(data), end="")
        elif args.command == "check-generated":
            require((ROOT / "organization/ROADMAP.md").read_text() == render(data))
        else: print("valid: proposed organization roadmap; no approval or live collection inferred")
        return 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError):
        print("invalid: organization roadmap input or generated view; source details withheld", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
