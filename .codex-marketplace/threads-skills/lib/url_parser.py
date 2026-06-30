"""Threads (Meta) URL parser.

Handles the common shapes for posts and profiles on both hosts:

1. Post URL (from "Copy link"):
   https://www.threads.net/@HANDLE/post/POSTCODE
   https://www.threads.com/@HANDLE/post/POSTCODE
   ...with optional query params (?xmt=...) or a trailing /media.

2. Profile URL:
   https://www.threads.net/@HANDLE
   https://www.threads.com/@HANDLE

Returns a normalized dict:
    {
      "handle": "<username>" | None,    # without the leading @
      "post_id": "<shortcode>" | None,  # Threads post shortcode, not numeric
      "url_type": "post" | "profile" | "unknown",
      "canonical_url": "https://www.threads.com/..." | None,
    }

Note: Threads migrated its primary domain from threads.net to threads.com in
2025; both still resolve. The parser normalizes the canonical URL to
threads.com. A Threads post id is a base64-style shortcode (letters, digits,
underscores, hyphens), NOT a numeric tweet id. A quote post is just a post URL;
the parser does not distinguish it (the reply-drafter skill decides reply vs
quote based on user intent, not the URL).
"""
from __future__ import annotations
import re
from typing import Optional, TypedDict
from urllib.parse import urlparse


class ParsedThreadsUrl(TypedDict, total=False):
    handle: Optional[str]
    post_id: Optional[str]
    url_type: str
    canonical_url: Optional[str]


_THREADS_HOSTS = {
    "threads.net",
    "threads.com",
}

# Subdomain prefixes we tolerate before the registrable host (mobile variants).
_STRIP_HOST_PREFIXES = ("www.", "m.", "mobile.")


def _host_is_threads(text: str) -> bool:
    """Return True only if the URL's host is a genuine Threads host.

    Parses the host with urlparse (so a substring like ``threads.com`` buried in
    a spoofed path or in ``threads.com.evil.example`` cannot pass), strips a
    leading ``www.`` / ``m.`` / ``mobile.`` and checks membership in
    ``_THREADS_HOSTS``.
    """
    candidate = text.strip()
    # urlparse needs a scheme to populate netloc; add one if the user pasted a
    # bare host like "threads.com/@zuck/post/...".
    if "://" not in candidate:
        candidate = "https://" + candidate
    host = urlparse(candidate).hostname or ""
    host = host.lower()
    for prefix in _STRIP_HOST_PREFIXES:
        if host.startswith(prefix):
            host = host[len(prefix):]
            break
    return host in _THREADS_HOSTS

# /@HANDLE/post/POSTCODE   (handle 1-30 chars; postcode is a shortcode)
_POST_RE = re.compile(
    r"(?:https?://)?(?:www\.)?threads\.(?:net|com)/"
    r"@(?P<handle>[A-Za-z0-9_.]{1,30})"
    r"/post/(?P<code>[A-Za-z0-9_-]{5,40})",
    re.IGNORECASE,
)
# Profile URL: /@HANDLE  (no /post)
_PROFILE_RE = re.compile(
    r"(?:https?://)?(?:www\.)?threads\.(?:net|com)/"
    r"@(?P<handle>[A-Za-z0-9_.]{1,30})/?(?:\?.*)?$",
    re.IGNORECASE,
)


def parse_threads_url(url: str) -> ParsedThreadsUrl:
    """Parse any Threads post or profile URL into structured fields.

    >>> p = parse_threads_url("https://www.threads.net/@zuck/post/C8H9abcDEf_")
    >>> p["handle"]
    'zuck'
    >>> p["post_id"]
    'C8H9abcDEf_'
    >>> p["url_type"]
    'post'
    """
    out: ParsedThreadsUrl = {
        "handle": None,
        "post_id": None,
        "url_type": "unknown",
        "canonical_url": None,
    }
    if not url:
        return out

    text = url.strip()

    # Gate on the real host: reject spoofed URLs whose netloc is not a Threads
    # host even if the path contains a "threads.com/@.../post/..." substring.
    if not _host_is_threads(text):
        return out

    m = _POST_RE.search(text)
    if m:
        handle = m.group("handle")
        code = m.group("code")
        out["handle"] = handle
        out["post_id"] = code
        out["url_type"] = "post"
        out["canonical_url"] = f"https://www.threads.com/@{handle}/post/{code}"
        return out

    m = _PROFILE_RE.search(text)
    if m:
        handle = m.group("handle")
        out["handle"] = handle
        out["url_type"] = "profile"
        out["canonical_url"] = f"https://www.threads.com/@{handle}"
        return out

    return out


def build_thread_url(handle: str, post_id: str) -> str:
    """Format a canonical threads.com post URL from a handle and post id."""
    handle = handle.lstrip("@")
    return f"https://www.threads.com/@{handle}/post/{post_id}"


if __name__ == "__main__":
    import json
    import sys

    examples = sys.argv[1:] or [
        "https://www.threads.net/@zuck/post/C8H9abcDEf_",
        "https://www.threads.com/@mosseri/post/Ct1bQ2xYz-9?xmt=abc",
        "https://www.threads.net/@levelsio",
        "https://www.threads.com/@natalie",
        # Mobile host should still parse.
        "https://m.threads.com/@dami/post/Abc12_de-fg",
        # Spoof hosts must return unknown (host not in _THREADS_HOSTS).
        "https://evil.example/threads.com/@zuck/post/C8H9abcDEf_",
        "https://threads.com.evil.example/@zuck/post/C8H9abcDEf_",
    ]
    for u in examples:
        print(u)
        print(json.dumps(parse_threads_url(u), indent=2))
        print()

    # Inline assertions: real URLs parse, spoofs return unknown.
    assert parse_threads_url(
        "https://www.threads.net/@zuck/post/C8H9abcDEf_"
    )["url_type"] == "post"
    assert parse_threads_url("https://www.threads.com/@natalie")["url_type"] == "profile"
    assert parse_threads_url(
        "https://m.threads.com/@dami/post/Abc12_de-fg"
    )["url_type"] == "post"
    assert parse_threads_url(
        "https://evil.example/threads.com/@zuck/post/C8H9abcDEf_"
    )["url_type"] == "unknown"
    assert parse_threads_url(
        "https://threads.com.evil.example/@zuck/post/C8H9abcDEf_"
    )["url_type"] == "unknown"
    print("self-test: OK")
