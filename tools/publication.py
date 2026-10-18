# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Compose Hygiene's host shell and verify its consumer-owned Pages handoff.

Relay owns collection, semantics, rendering and composition validation. This
module owns only this repository's origin, aliases, transport and recovery.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html import escape
import json
import os
from pathlib import Path, PurePosixPath
import re
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "publication/site.json"
SCHEMA = "hygiene.pages-transport/v1"
CONTROL_FILES = {"CNAME", ".nojekyll"}
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_SITE_BYTES = 64 * 1024 * 1024
MAX_FILES = 2000


def encoded(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def revision(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("a full lowercase source revision is required")
    return value


def config() -> dict:
    value = json.loads(CONFIG.read_bytes())
    if value["repository"] != "egohygiene/hygiene" or value["origin"] != "https://hygiene.egohygiene.io":
        raise ValueError("publication identity or canonical origin changed")
    revision(value["relay_revision"])
    return value


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def inventory(site: Path) -> list[dict]:
    if not site.is_dir() or site.is_symlink():
        raise ValueError("site must be a regular directory")
    records = []
    total = 0
    for path in sorted(site.rglob("*")):
        if path.is_symlink():
            raise ValueError("site contains a symbolic link")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError("site contains a special file")
        relative = path.relative_to(site).as_posix()
        if relative == "publication.json":
            continue
        size = path.stat().st_size
        total += size
        if size > MAX_FILE_BYTES or total > MAX_SITE_BYTES or len(records) >= MAX_FILES:
            raise ValueError("site exceeds transport bounds")
        records.append({"path": relative, "bytes": size, "sha256": sha256(path.read_bytes())})
    if not records:
        raise ValueError("site is empty")
    return records


def shell(site: Path, source_revision: str) -> None:
    selected = config()
    revision(source_revision)
    if site.exists() and any(site.iterdir()):
        raise ValueError("compose into an empty site directory")
    origin = selected["origin"]
    icon = "/intelligence/egohygiene.png"
    body = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hygiene · Ego Hygiene</title><link rel="canonical" href="{origin}/">
<link rel="icon" type="image/png" href="{icon}"><link rel="stylesheet" href="/intelligence/site.css"></head>
<body><a href="#main">Skip to content</a><main id="main">
<nav aria-label="Global navigation"><a href="https://github.com/egohygiene" aria-label="Ego Hygiene"><img src="{icon}" alt="" width="44" height="44"></a>
<a href="https://github.com/egohygiene/hygiene">Repository source on GitHub</a></nav>
<h1>Hygiene</h1><p>Ecosystem architecture, contracts and policy for Ego Hygiene.</p>
<ul><li><a href="/intelligence/">Explore Repository Intelligence</a></li>
<li><a href="/intelligence/decisions/">Read architecture decisions</a></li>
<li><a href="https://github.com/egohygiene/hygiene/tree/{source_revision}/docs/ecosystem">Browse architecture and policy sources</a></li></ul>
</main></body></html>
"""
    write(site / "index.html", body.encode())
    write(site / "CNAME", (urlsplit(origin).hostname + "\n").encode())
    write(site / ".nojekyll", b"")
    for alias in selected["aliases"]:
        target = escape(alias["target"], quote=True)
        page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hygiene decisions</title><link rel="canonical" href="{origin}{target}">
<link rel="icon" type="image/png" href="{icon}"><meta http-equiv="refresh" content="0; url={target}"></head>
<body><main><h1>Hygiene decisions</h1><a href="{target}">Continue to the decision ledger</a></main></body></html>
"""
        write(site / alias["route"].strip("/") / "index.html", page.encode())


def seal(site: Path, source_revision: str) -> dict:
    selected = config()
    manifest = json.loads((site / "intelligence/build-manifest.json").read_bytes())
    if manifest["consumer"] != {"repository": selected["repository"], "revision": revision(source_revision)}:
        raise ValueError("Relay build does not represent this consumer revision")
    if manifest["generator"]["revision"] != selected["relay_revision"]:
        raise ValueError("Relay build revision differs from the reviewed selection")
    files = inventory(site)
    value = {"schema": SCHEMA, "repository": selected["repository"],
             "revision": source_revision, "origin": selected["origin"],
             "relay_revision": selected["relay_revision"], "files": files,
             "files_sha256": sha256(encoded(files))}
    write(site / "publication.json", encoded(value))
    return value


def validate_manifest(value: dict) -> None:
    selected = config()
    if (set(value) != {"schema", "repository", "revision", "origin", "relay_revision", "files", "files_sha256"}
            or value["schema"] != SCHEMA or value["repository"] != selected["repository"]
            or value["origin"] != selected["origin"]):
        raise ValueError("publication manifest identity mismatch")
    revision(value["revision"])
    revision(value["relay_revision"])
    records = value["files"]
    if not isinstance(records, list) or not 1 <= len(records) <= MAX_FILES:
        raise ValueError("publication file inventory is missing or exceeds bounds")
    previous = ""
    total = 0
    for item in records:
        if not isinstance(item, dict) or set(item) != {"path", "bytes", "sha256"}:
            raise ValueError("invalid publication file record")
        path, size, digest = item["path"], item["bytes"], item["sha256"]
        if (not isinstance(path, str) or not path or path <= previous or path == "publication.json"
                or str(PurePosixPath(path)) != path or path.startswith("/")
                or any(part in {".", ".."} for part in path.split("/"))
                or not re.fullmatch(r"[A-Za-z0-9._/-]+", path)
                or not isinstance(size, int) or isinstance(size, bool) or not 0 <= size <= MAX_FILE_BYTES
                or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            raise ValueError("unsafe publication file record")
        previous = path
        total += size
    if total > MAX_SITE_BYTES or value["files_sha256"] != sha256(encoded(records)):
        raise ValueError("publication inventory digest or size mismatch")


def check(site: Path, source_revision: str) -> dict:
    value = json.loads((site / "publication.json").read_bytes())
    validate_manifest(value)
    if (value["revision"] != revision(source_revision) or value["relay_revision"] != config()["relay_revision"]
            or value["files"] != inventory(site)):
        raise ValueError("downloaded site differs from the selected immutable handoff")
    return value


def admit(report: dict, source_revision: str) -> bool:
    # The shared report's overall architecture result may be incomplete because
    # other domains are unknown. Only its explicit ADR coverage selects this
    # publisher; the strict shared builder independently revalidates admission.
    if (report["schema_version"] != "relay.repository-architecture-validation-result/v1"
            or report["repository"]["id"] != config()["repository"]
            or report["repository"]["visibility"] != "public"
            or report["repository"]["represented_revision"] != revision(source_revision)):
        raise ValueError("architecture report belongs to a different source")
    return (report["coverage"]["architecture-records"] == "passed"
            and not report["bounds"]["scan_truncated"]
            and not report["bounds"]["findings_truncated"])


def remote(path: str, *, missing: bool = False) -> bytes | None:
    url = config()["origin"] + "/" + path
    for attempt in range(3):
        try:
            with urlopen(url, timeout=15) as response:
                if response.geturl() != url:
                    raise ValueError("publication request redirected away from its exact URL")
                data = response.read(MAX_FILE_BYTES + 1)
                if len(data) > MAX_FILE_BYTES:
                    raise ValueError("remote file exceeds transport bounds")
                return data
        except HTTPError as error:
            if error.code == 404 and missing:
                return None
            if attempt == 2:
                raise
        except OSError:
            if attempt == 2:
                raise
        time.sleep(2)
    raise ValueError("publication request exhausted retries")


def verify_remote(value: dict, *, destination: Path | None = None) -> int:
    validate_manifest(value)
    count = 0
    for item in value["files"]:
        path = item["path"]
        if path in CONTROL_FILES:
            # GitHub Pages control files are transported, but not public routes.
            data = (urlsplit(config()["origin"]).hostname + "\n").encode() if path == "CNAME" else b""
        else:
            data = remote(path)
            count += 1
        if data is None or len(data) != item["bytes"] or sha256(data) != item["sha256"]:
            raise ValueError("deployed bytes do not match the publication inventory")
        if destination is not None:
            write(destination / path, data)
    return count


def capture_recovery(destination: Path) -> dict:
    data = remote("publication.json", missing=True)
    if data is None:
        if remote("", missing=True) is not None:
            raise ValueError("an existing site has no verifiable recovery manifest")
        value = {"state": "first-deployment", "previous": None,
                 "recovery": "Unpublish the first deployment in GitHub Pages; there is no prior site to restore."}
    else:
        prior = json.loads(data)
        count = verify_remote(prior, destination=destination / "site")
        write(destination / "site/publication.json", data)
        value = {"state": "captured", "previous": prior, "verified_public_files": count,
                 "recovery": "Restore the retained recovery/site artifact through the reviewed Pages publisher."}
    write(destination / "recovery.json", encoded(value))
    return value


def verify_live(site: Path, source_revision: str, recovery: Path, output: Path) -> dict:
    value = check(site, source_revision)
    deployed = remote("publication.json")
    if deployed != (site / "publication.json").read_bytes():
        raise ValueError("deployed publication manifest differs from the handoff")
    count = verify_remote(value)
    recovered = json.loads((recovery / "recovery.json").read_bytes())
    run = os.environ.get("GITHUB_RUN_ID", "")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "")
    if not run.isdigit() or not attempt.isdigit() or int(run) < 1 or int(attempt) < 1:
        raise ValueError("a provider workflow run and attempt are required for a deployment receipt")
    receipt = {"schema": "hygiene.pages-deployment/v1", "publication": value,
               "workflow_run_id": int(run), "workflow_run_attempt": int(attempt),
               "verified_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
               "verified_public_files": count, "excluded_provider_control_files": sorted(CONTROL_FILES),
               "recovery": recovered}
    write(output, encoded(receipt))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("shell", "seal", "check", "admit", "capture-recovery", "verify-live"))
    parser.add_argument("--site", type=Path, default=Path("dist"))
    parser.add_argument("--revision", default=os.environ.get("GITHUB_SHA", ""))
    parser.add_argument("--report", type=Path)
    parser.add_argument("--recovery", type=Path, default=Path(".cache/publication/recovery"))
    parser.add_argument("--output", type=Path, default=Path(".cache/publication/deployment.json"))
    args = parser.parse_args()
    if args.operation == "admit":
        ready = admit(json.loads(args.report.read_bytes()), args.revision)
        with Path(os.environ["GITHUB_OUTPUT"]).open("a") as stream:
            stream.write("ready=" + str(ready).lower() + "\n")
        with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a") as stream:
            stream.write("## Hygiene Decisions admission\n\n" + ("Shared ADR coverage passed; the strict builder will revalidate the source.\n"
                         if ready else "**Publication blocked.** Shared ADR coverage has not passed; no site artifact or deployment is selected. Review the retained architecture report.\n"))
    elif args.operation == "capture-recovery":
        capture_recovery(args.recovery)
    elif args.operation == "verify-live":
        verify_live(args.site, args.revision, args.recovery, args.output)
    else:
        {"shell": shell, "seal": seal, "check": check}[args.operation](args.site, args.revision)


if __name__ == "__main__":
    main()
