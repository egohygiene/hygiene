"""Shared, offline HTTPS syntax rules for Hygiene's reference checkers.

These checks neither resolve a host nor certify a live endpoint. Reject raw
ambiguities before urllib can normalize them; callers report field paths only.
"""

from __future__ import annotations

import ipaddress
import re
from typing import Any
from urllib.parse import SplitResult, urlsplit


HOST_LABEL_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"
)


def is_hostname(value: str) -> bool:
    # URI-scoped IPv6 and encoded authorities are not part of this contract.
    if "%" in value:
        return False
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        labels = value.removesuffix(".").split(".")
        return (
            len(value) <= 253
            and bool(labels)
            and all(HOST_LABEL_RE.fullmatch(label) is not None for label in labels)
        )


def parse_https(value: Any) -> SplitResult | None:
    if (
        not isinstance(value, str)
        or not value.startswith("https://")
        or "\\" in value
        or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value)
    ):
        return None
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return None
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or not is_hostname(parsed.hostname)
        or parsed.username is not None
        or parsed.password is not None
        or (port is not None and not 1 <= port <= 65535)
    ):
        return None

    # urlsplit accepts an empty port and junk after a bracketed literal.
    # Require the entire authority to be host[:decimal-port].
    if parsed.netloc.startswith("["):
        try:
            ipaddress.IPv6Address(parsed.hostname)
        except ValueError:
            return None
        suffix = parsed.netloc[parsed.netloc.index("]") + 1:]
    else:
        _, separator, digits = parsed.netloc.partition(":")
        suffix = separator + digits
    if suffix and re.fullmatch(r":[0-9]+", suffix) is None:
        return None
    return parsed


def is_https(value: Any) -> bool:
    return parse_https(value) is not None


def is_origin(value: Any) -> bool:
    parsed = parse_https(value)
    return (
        parsed is not None
        and parsed.path in {"", "/"}
        and "?" not in value
        and "#" not in value
    )
