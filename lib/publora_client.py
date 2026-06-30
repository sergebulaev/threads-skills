"""Thin Publora REST client for the Threads (Meta) Skills project.

Wraps the Publora API endpoints this bundle uses. As of 2026-06 Publora exposes:
- POST /create-post              (publish or schedule a post / thread)
- GET  /platform-connections     (list connected accounts + token health)

Threads has no comment- or reaction-specific endpoint on Publora (those are
LinkedIn-only). On Threads a "reply" to someone else's post is a separate post,
but `create-post` does not expose a reply target, so replying to another user is
draft-only in this bundle. Posts and self-threads both flow through
`create-post`: pass long `content` and Publora auto-splits it into a connected
multi-post thread at paragraph then sentence boundaries.

Base URL: https://api.publora.com/api/v1
Auth header: x-publora-key: sk_...  (NOT Bearer)
Content-Type: application/json. Server-to-server only (custom headers are not
in the CORS allowlist, so browser calls fail preflight).

Threads-specific: Publora recognizes a `platformSettings.threads` object. The
only documented field is `replyControl` (who can reply). Pass it through
`platform_settings={"threads": {"replyControl": "everyone"}}`.

Design note: this client is deliberately minimal. Skills call exactly one
method per action, after the user has approved a draft rendered via
`lib/approval.py`. Write methods retry on transient 408/429/5xx via the
shared retry decorator.
"""
from __future__ import annotations
import os
import time
import random
from typing import Any, Optional

import requests


class PubloraError(RuntimeError):
    pass


RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}


def _retry(attempts: int = 3, base_delay: float = 0.6):
    """Retry decorator for HTTP methods. Triggers on 408/429/5xx and on
    transient network errors. Exponential backoff with jitter."""

    def decorator(fn):
        def wrapper(*args, **kwargs):
            last_exc: Optional[Exception] = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except PubloraError as e:
                    msg = str(e)
                    retryable = any(f"HTTP {s}" in msg for s in RETRYABLE_STATUSES)
                    if not retryable or attempt == attempts - 1:
                        raise
                    last_exc = e
                except (requests.ConnectionError, requests.Timeout) as e:
                    if attempt == attempts - 1:
                        raise
                    last_exc = e
                time.sleep(base_delay * (2**attempt) + random.uniform(0, 0.25))
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


# Platform IDs must match Publora's regex: /^[a-z]+-[a-zA-Z0-9_-]+$/
# For Threads the prefix is `threads-` (e.g. "threads-17841412345678").
PLATFORM_ID_PREFIX = "threads-"


class PubloraClient:
    BASE_URL = "https://api.publora.com/api/v1"

    def __init__(self, api_key: Optional[str] = None, timeout: float = 30.0):
        self.api_key = api_key or os.getenv("PUBLORA_API_KEY")
        if not self.api_key:
            raise PubloraError(
                "PUBLORA_API_KEY not set. Export it or pass api_key= explicitly."
            )
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-publora-key": self.api_key,
                "Content-Type": "application/json",
            }
        )

    # ---- Posts and threads ------------------------------------------------

    def create_post(
        self,
        *,
        content: str,
        platforms: list[str],
        scheduled_time: Optional[str] = None,
        platform_settings: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Create a single Threads post, a multi-post thread, or a cross-post.

        Args:
            content: Post text. Under 500 chars it ships as one post. Longer
                content (or content with `---` separators or `\\n\\n` paragraph
                breaks) is auto-split by Publora into a connected multi-post
                thread at paragraph then sentence boundaries. Unlike X, Threads
                does NOT add `(1/N)` markers by default. A text attachment lifts
                the per-post ceiling to 10,000 chars.
            platforms: List of platform connection IDs, e.g.
                ["threads-17841412345678"]. Each must match
                /^[a-z]+-[a-zA-Z0-9_-]+$/. Add more IDs to cross-post (e.g.
                ["threads-123", "twitter-456"]).
            scheduled_time: ISO 8601 UTC datetime. If omitted, the post is
                created as a draft. A past time is silently set to now.
            platform_settings: Optional per-platform settings object. Publora
                recognizes a `threads` key with `replyControl` (who can reply).
                Example: {"threads": {"replyControl": "everyone"}}. Keys for
                platforms other than tiktok/instagram/youtube/threads/telegram
                are silently dropped.

        Returns:
            { "success": true, "postGroupId": "..." } on HTTP 200.

        Note: each post in a thread counts toward your Threads API quota (250
        posts / 24h, 50 / hour). On a partial failure Publora returns status
        "partially_published" with the IDs that did post.
        """
        if not content or not content.strip():
            raise PubloraError("content is required (cannot be empty or whitespace)")
        if not platforms:
            raise PubloraError("at least one platform ID is required")
        payload: dict[str, Any] = {
            "content": content,
            "platforms": platforms,
        }
        if scheduled_time:
            payload["scheduledTime"] = scheduled_time
        if platform_settings:
            payload["platformSettings"] = platform_settings
        return self._post("/create-post", payload)

    # ---- Connections (read) -----------------------------------------------

    def list_connections(self) -> list[dict[str, Any]]:
        """List connected social accounts with token health.

        Returns the `connections` array from GET /platform-connections. Each
        entry has platformId, username, displayName, tokenStatus, lastError,
        etc. Use it to confirm a Threads account is connected and which
        `threads-<id>` to pass to `create_post`.
        """
        r = self._session.get(
            self.BASE_URL + "/platform-connections", timeout=self.timeout
        )
        data = self._handle(r)
        return data.get("connections", [])

    def threads_connections(self) -> list[dict[str, Any]]:
        """Convenience filter: only the connected Threads accounts."""
        return [
            c
            for c in self.list_connections()
            if str(c.get("platformId", "")).startswith(PLATFORM_ID_PREFIX)
        ]

    # ---- Internals --------------------------------------------------------

    @_retry()
    def _post(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        r = self._session.post(
            self.BASE_URL + path, json=json_body, timeout=self.timeout
        )
        return self._handle(r)

    @staticmethod
    def _handle(r: requests.Response) -> dict[str, Any]:
        if r.status_code >= 400:
            try:
                body = r.json()
            except Exception:
                body = {"error": r.text[:500]}
            raise PubloraError(f"HTTP {r.status_code}: {body}")
        return r.json()
