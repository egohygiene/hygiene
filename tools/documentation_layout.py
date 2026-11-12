#!/usr/bin/env python3
"""Pure advisory composition for proposed documentation locations.

Consumes an explicit inventory, not a filesystem crawl or transcript. Existing
Hygiene resolvers retain presentation/continuity applicability. This adapter
never moves files, edits prose, authenticates visibility/approval, publishes or
claims that declared observations prove actual file contents.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
PROFILE_SCHEMA = "egohygiene.repository-documentation-profile/v1"
INPUT_SCHEMA = "egohygiene.repository-documentation-inventory/v1"
OUTPUT_SCHEMA = "egohygiene.repository-documentation-assessment/v1"
VERSION = "1.0.0-alpha.1"
MAX_JSON_BYTES = 1024 * 1024
PROFILE_SHA256 = "c5bf0246f039b1780ba03900f894dadf099fd190ea22131d7d1728230efab0d2"


def require(value):
    if not value:
        raise ValueError("Documentation inventory/profile incompatible")


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def parse(content):
    require(type(content) is bytes and 0 < len(content) <= MAX_JSON_BYTES)
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result)
            result[key] = value
        return result
    result = json.loads(content.decode("utf-8", errors="strict"), object_pairs_hook=unique,
                        parse_constant=lambda _: require(False))
    pending, nodes = [(result, 0)], 0
    while pending:
        item, depth = pending.pop()
        nodes += 1
        require(depth <= 32 and nodes <= 16384)
        if type(item) is dict:
            pending.extend((child, depth + 1) for child in item.values())
        elif type(item) is list:
            pending.extend((child, depth + 1) for child in item)
    encoded(result)
    return result


def read_inventory(path):
    """Use a nonblocking open and reject nonregular/oversize inputs before reading."""
    require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"))
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as source:
        metadata = os.fstat(source.fileno())
        require(stat.S_ISREG(metadata.st_mode) and 0 < metadata.st_size <= MAX_JSON_BYTES)
        content = source.read(MAX_JSON_BYTES + 1)
    require(0 < len(content) <= MAX_JSON_BYTES)
    return content


def safe_path(value):
    require(type(value) is str and 0 < len(value) <= 240
            and not value.startswith("/") and "\\" not in value
            and re.match(r"^[A-Za-z]:", value) is None
            and not any(ord(char) < 32 or ord(char) == 127 for char in value)
            and all(part not in {"", ".", ".."} and part.casefold() != ".git"
                    for part in value.split("/")))
    return value


def profile():
    raw = (ROOT / "catalog/repository-documentation-profile.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PROFILE_SHA256)
    value = parse(raw)
    require(value["schema"] == PROFILE_SCHEMA and value["version"] == VERSION
            and value["status"] == "proposed" and value["approval"] is None
            and value["enforcement"] == "observe")
    return value


def composed(selected, name):
    """Import only the byte-bound local owner resolver, never inventory code."""
    pin = selected["composes"][name]
    raw = (ROOT / safe_path(pin["path"])).read_bytes()
    helper = ROOT / safe_path(pin["helper"])
    helper_bytes = helper.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == pin["sha256"]
            and hashlib.sha256(helper_bytes).hexdigest() == pin["helper_sha256"])
    # Execute the exact verified bytes, rather than rereading a mutable pathname.
    module = ModuleType("hygiene_documentation_" + name)
    module.__file__ = str(helper)
    sys.modules[module.__name__] = module
    exec(compile(helper_bytes, str(helper), "exec"), module.__dict__)
    return module, parse(raw)


def closed(value, required, optional=()):
    require(type(value) is dict and required <= set(value) <= required | set(optional))
    return value


def text(value, maximum=1024):
    require(type(value) is str and 0 < len(value) <= maximum and value.strip()
            and not any(ord(char) < 32 or ord(char) == 127 for char in value))


def path_list(value, maximum):
    require(type(value) is list and len(value) <= maximum)
    for item in value:
        safe_path(item)
    require(len(value) == len(set(value)))


def validate_inventory(value):
    """Validate the closed observation envelope without reading consumer files."""
    closed(value, {"schema", "visibility", "repository", "as_of", "layout", "layout_exception",
                   "architecture_selected", "readme_mode", "readme_justification",
                   "claude_selected", "documents"})
    require(value["schema"] == INPUT_SCHEMA and value["visibility"] == "public")
    repository = closed(value["repository"], {"name", "kind", "lifecycle", "repository_type", "presentation_lifecycle"})
    require(type(repository["name"]) is str and re.fullmatch(r"egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)", repository["name"]))
    dimensions = {
        "kind": {"standard", "mirror", "generated-only", "template", "unknown"},
        "lifecycle": {"active", "dormant", "archived", "unknown"},
        "repository_type": {"application", "collection", "control_plane", "documentation", "infrastructure",
                            "library", "publication", "template", "tool", "website", "unknown"},
        "presentation_lifecycle": {"active", "incubating", "archived", "unknown"},
    }
    for field, allowed in dimensions.items():
        require(type(repository[field]) is str and repository[field] in allowed)
    require(type(value["as_of"]) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value["as_of"]))
    date.fromisoformat(value["as_of"])
    require(type(value["layout"]) is str and value["layout"] in {"legacy-root", "nested-architecture", "repository-exception", "unknown"})
    require(type(value["readme_mode"]) is str and value["readme_mode"] in {"concise", "rich-justified", "unknown"})
    for field in ("architecture_selected", "claude_selected"):
        require(type(value[field]) is bool or value[field] is None)
    if value["readme_justification"] is not None:
        text(value["readme_justification"])
    exception = value["layout_exception"]
    require((value["layout"] == "repository-exception") == (exception is not None))
    if exception is not None:
        closed(exception, {"status", "owner", "reason", "review_trigger", "paths"})
        require(exception["status"] == "proposed" and type(exception["owner"]) is str
                and re.fullmatch(r"egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)", exception["owner"]))
        text(exception["reason"])
        text(exception["review_trigger"])
        require(type(exception["paths"]) is list and 0 < len(exception["paths"]) <= 256)
        ids, locations = set(), set()
        for mapping in exception["paths"]:
            closed(mapping, {"canonical_id", "path"})
            require(type(mapping["canonical_id"]) is str and re.fullmatch(r"[a-z][a-z0-9-]{0,63}", mapping["canonical_id"])
                    and mapping["canonical_id"] not in ids)
            safe_path(mapping["path"])
            require(mapping["path"] not in locations)
            ids.add(mapping["canonical_id"])
            locations.add(mapping["path"])
    require(type(value["documents"]) is list and len(value["documents"]) <= 256)
    required = {"id", "category", "path", "authority", "ownership", "state", "file_kind", "links"}
    optional = {"stable_id", "canonical_id", "question", "update_path", "source", "imports", "first_nonblank_line",
                "provider_content", "justification", "durable", "tracked"}
    for document in value["documents"]:
        closed(document, required, optional)
        for field in ("question", "update_path"):
            if field in document:
                text(document[field])
        if document.get("justification") is not None:
            text(document["justification"])
        for field, pattern in (("stable_id", r"[A-Za-z0-9][A-Za-z0-9._/-]{0,127}"),
                               ("canonical_id", r"[a-z][a-z0-9-]{0,63}")):
            if document.get(field) is not None:
                require(type(document[field]) is str and re.fullmatch(pattern, document[field]))
        for field in ("provider_content", "durable", "tracked"):
            if field in document:
                require(type(document[field]) is bool)
        if "first_nonblank_line" in document:
            require(type(document["first_nonblank_line"]) is str and len(document["first_nonblank_line"]) <= 256
                    and not any(ord(char) < 32 or ord(char) == 127 for char in document["first_nonblank_line"]))
        if "imports" in document:
            path_list(document["imports"], 16)
        path_list(document["links"], 128)
        if "source" in document:
            source = closed(document["source"], {"repository", "revision", "path"})
            require(type(source["repository"]) is str and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", source["repository"]))
            require(type(source["revision"]) is str and re.fullmatch(r"[a-f0-9]{40}", source["revision"]))
            safe_path(source["path"])


def assess(value):
    """Project declared location gaps without echoing prose, names or paths.

    This is a local reference, not public source authentication. Production
    validators must obtain file/visibility observations through their own
    admitted source and must validate Aether-owned content separately.
    """
    selected = profile()
    result = {"schema": OUTPUT_SCHEMA, "contract_version": VERSION,
        "policy": {"schema": PROFILE_SCHEMA, "version": VERSION, "status": "proposed", "sha256": PROFILE_SHA256},
        "publication": "local-review-only", "state": "unavailable", "layout": None,
        "continuity_requirement": "unknown", "continuity_assessment": None,
        "presentation_requirements": {}, "diagnostics": [],
        "qualification": {"input": "declared-inventory-not-filesystem-proof", "enforcement": "not-activated",
            "human_approval": "not-inferred", "aether_content_validation": "not-performed",
            "links": "declared-relative-targets-only", "provider_activation": "not-performed"}}
    if type(value) is not dict or value.get("visibility") != "public":
        result["diagnostics"] = [{"code": "SOURCE_NOT_ADMITTED", "category": None}]
        return result
    validate_inventory(value)
    repository = value["repository"]
    require(type(repository) is dict and set(repository) == {"name", "kind", "lifecycle", "repository_type", "presentation_lifecycle"})
    require(type(repository["name"]) is str and re.fullmatch(r"egohygiene/(?:\.github|[a-z0-9][a-z0-9.-]*)", repository["name"]))
    require(type(value["as_of"]) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value["as_of"]))
    observed_on = date.fromisoformat(value["as_of"])
    require(value["layout"] in selected["layout"]["supported"] and value["readme_mode"] in selected["readme"]["modes"]
            and (type(value["claude_selected"]) is bool or value["claude_selected"] is None)
            and type(value["documents"]) is list and len(value["documents"]) <= 256)
    codes = set()
    def note(code, category=None):
        codes.add((code, category))
    try:
        resolver, source = composed(selected, "continuity")
        resolved = resolver.resolve_applicability(source, repository["name"], repository["lifecycle"],
            repository["kind"], value["visibility"], as_of=observed_on)
        assessment = {key: resolved[key] for key in ("assessment_date", "assessment_mode")}
        result.update(continuity_requirement=resolved["requirement"], continuity_assessment=assessment)
    except (ValueError, KeyError, TypeError):
        note("CONTINUITY_APPLICABILITY_UNKNOWN")
    try:
        resolver, source = composed(selected, "presentation")
        result["presentation_requirements"] = resolver.resolve_requirements(source, repository["repository_type"],
            value["visibility"], repository["presentation_lifecycle"])
    except (ValueError, KeyError, TypeError):
        note("PRESENTATION_APPLICABILITY_UNKNOWN")
    categories = {row["id"] for row in selected["categories"]}
    documents, paths, stable = {}, {}, {}
    required_fields = {"id", "category", "path", "authority", "ownership", "state", "file_kind", "links"}
    optional = {"stable_id", "canonical_id", "question", "update_path", "source", "imports", "first_nonblank_line",
                "provider_content", "justification", "durable", "tracked"}
    for document in value["documents"]:
        require(type(document) is dict and required_fields <= set(document) <= required_fields | optional)
        require(type(document["id"]) is str and re.fullmatch(r"[a-z][a-z0-9-]{0,63}", document["id"])
                and document["category"] in categories and document["authority"] in {"canonical", "navigation", "derived", "historical", "scratch"}
                and document["ownership"] in {"repository", "generated"}
                and document["state"] in {"present", "missing", "unknown", "inaccessible"}
                and document["file_kind"] in {"regular", "symlink", "directory", "unknown"}
                and type(document["links"]) is list and len(document["links"]) <= 128)
        path = safe_path(document["path"])
        for target in document["links"]:
            safe_path(target)
        require(document["id"] not in documents and path not in paths)
        documents[document["id"]], paths[path] = document, document
        category = document["category"]
        if document["state"] == "present" and document["file_kind"] != "regular":
            note("REGULAR_SOURCE_REQUIRED", category)
        if document["authority"] == "canonical":
            if not document.get("question") or not document.get("update_path"):
                note("DOCUMENT_METADATA_UNKNOWN", category)
            if document["state"] != "present":
                note("CANONICAL_SOURCE_UNVERIFIED", category)
            identity = document.get("stable_id")
            if identity:
                require(type(identity) is str and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,127}", identity))
                if identity in stable:
                    note("DUPLICATE_CANONICAL_IDENTITY", category)
                stable[identity] = document
        if document["ownership"] == "generated":
            source = document.get("source")
            if (type(source) is not dict or set(source) != {"repository", "revision", "path"}
                    or type(source.get("revision")) is not str or not re.fullmatch(r"[a-f0-9]{40}", source["revision"])):
                note("GENERATED_SOURCE_UNKNOWN", category)
            if document["authority"] == "canonical":
                note("GENERATED_CANONICAL_REVIEW", category)
        if category == "temporary":
            if document.get("durable") is True:
                note("PROMOTE_DURABLE_CONTENT", category)
            if document.get("tracked") is True:
                note("TEMPORARY_TRACKED", category)
        if category == "claude" and document["state"] == "present":
            if document.get("first_nonblank_line") != "@AGENTS.md" or document.get("imports") != ["AGENTS.md"]:
                note("CLAUDE_IMPORTS", category)
            if document.get("provider_content") is True and not document.get("justification"):
                note("CLAUDE_PROVIDER_JUSTIFICATION_REQUIRED", category)
    def need(path, category, required=True, authority=None, repository_owned=False):
        item = paths.get(path)
        if item is None or item["state"] == "missing":
            note("REQUIRED_DESTINATION_MISSING" if required else "RECOMMENDED_DESTINATION_MISSING", category)
        elif item["state"] != "present":
            note("DESTINATION_UNVERIFIED", category)
        elif item["category"] != category:
            note("DESTINATION_ROLE_MISMATCH", category)
        if item is not None and item["state"] == "present":
            if authority is not None and item["authority"] != authority:
                note("DESTINATION_AUTHORITY_MISMATCH", category)
            if repository_owned and item["ownership"] != "repository":
                note("REPOSITORY_OWNERSHIP_REQUIRED", category)
    need("README.md", "readme", authority="canonical", repository_owned=True)
    if result["continuity_requirement"] == "required":
        need("AGENTS.md", "agents", authority="canonical", repository_owned=True)
        need("CONTINUITY.md", "continuity", authority="canonical", repository_owned=True)
    elif result["continuity_requirement"] == "advisory":
        need("AGENTS.md", "agents", False, authority="canonical", repository_owned=True)
        need("CONTINUITY.md", "continuity", False, authority="canonical", repository_owned=True)
    if value["claude_selected"] is True:
        need("CLAUDE.md", "claude")
        need("AGENTS.md", "agents", authority="canonical", repository_owned=True)
    elif value["claude_selected"] is None:
        note("CLAUDE_SELECTION_UNKNOWN", "claude")
    if value["readme_mode"] == "rich-justified" and not value["readme_justification"]:
        note("README_JUSTIFICATION_REQUIRED", "readme")
    if value["readme_mode"] == "unknown":
        note("README_DISPOSITION_UNKNOWN", "readme")
    if value["layout"] == "unknown":
        note("LAYOUT_UNDECLARED")
    elif value["layout"] == "repository-exception":
        note("EXCEPTION_REQUIRES_OWNER_REVIEW")
        for mapping in value["layout_exception"]["paths"]:
            canonical = documents.get(mapping["canonical_id"])
            if canonical is None or canonical["authority"] != "canonical" or canonical["path"] != mapping["path"]:
                note("EXCEPTION_PATH_MAP_MISMATCH")
    if value["architecture_selected"] is None:
        note("ARCHITECTURE_SELECTION_UNKNOWN", "architecture")
    elif value["architecture_selected"] is True:
        canonical = [row for row in documents.values() if row["category"] == "architecture" and row["authority"] == "canonical"]
        if not canonical:
            note("CANONICAL_ARCHITECTURE_MISSING", "architecture")
        if value["layout"] == "nested-architecture":
            need("ARCHITECTURE.md", "architecture_navigation", authority="navigation", repository_owned=True)
        elif value["layout"] == "legacy-root":
            need("ARCHITECTURE.md", "architecture", authority="canonical", repository_owned=True)
    for item in documents.values():
        if item["authority"] == "navigation":
            canonical = documents.get(item.get("canonical_id"))
            if canonical is None or canonical["authority"] != "canonical" or canonical["path"] not in item["links"]:
                note("CANONICAL_NAVIGATION_UNKNOWN", item["category"])
        for link in item["links"]:
            target = paths.get(link)
            if target is None or target["state"] != "present":
                note("NAVIGATION_TARGET_UNVERIFIED", item["category"])
    if any(row["path"].startswith("docs/") for row in documents.values()):
        indexes = [row for row in documents.values() if row["category"] == "documentation_index"]
        if not indexes:
            need("docs/README.md", "documentation_index", False)
        elif not any(row["state"] == "present" and row["file_kind"] == "regular" for row in indexes):
            note("DESTINATION_UNVERIFIED", "documentation_index")
    result["layout"] = value["layout"]
    result["diagnostics"] = [{"code": code, "category": category} for code, category in sorted(codes, key=lambda row: (row[0], row[1] or ""))]
    result["state"] = "review_required" if codes else "advisory"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="Explicit declared JSON observations, not an authorization or executable plan.")
    args = parser.parse_args()
    try:
        value = assess(parse(read_inventory(args.inventory)))
    except (ValueError, OSError, KeyError, TypeError, UnicodeError, RecursionError):
        print("Documentation inventory/profile unavailable or incompatible", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(encoded(value))
    return 2 if value["state"] == "unavailable" else int(value["state"] == "review_required")


if __name__ == "__main__":
    raise SystemExit(main())
