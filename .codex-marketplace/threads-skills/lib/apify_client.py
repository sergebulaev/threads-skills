"""Apify read client for the Threads (Meta) Skills bundle.

The read layer: given a niche query/hashtag or a username, pull Threads posts
with their author and engagement, and pull a profile's follower stats, so a
skill can see what is working in a niche and how an account performs. Uses the
run-sync-get-dataset-items endpoint (one HTTP request, no polling).

Auth: APIFY_TOKEN env var (or constructor arg). Get one at
https://console.apify.com/settings/integrations (free tier included).

Actors (verified live 2026-07-13):
  * Search/discovery: igview-owner/threads-search-scraper. Input searchQuery +
    sort ("top"/"recent") + maxPosts (min 20). Returns posts with username,
    isVerified, captionText, likeCount, directReplyCount, repostCount,
    quoteCount, takenAtISO, postUrl.
  * Profile: apify/threads-profile-api-scraper. Input usernames[]. Returns
    username, full_name, follower_count, biography, is_verified, bio_links,
    and latestPosts (each with caption.text, like_count, and
    text_post_app_info.{direct_reply_count, repost_count, quote_count}).

What Threads does NOT expose: the list of who LIKED or a full engager/liker
roster. That data is cookie-gated, capped at ~100, and has no public API. The
read layer here is SEARCH/DISCOVERY + PROFILE stats only. That is a platform
wall, not a client limitation. Do not promise an engager list.

Caching: in-process LRU (256 entries, 6h TTL). force_refresh=True to bypass.
Retries transient 429/5xx (3 attempts, exponential backoff + jitter).
"""
from __future__ import annotations
import os
import random
import time
from collections import OrderedDict
from typing import Any, Optional

import requests

SEARCH_ACTOR = "igview-owner~threads-search-scraper"
PROFILE_ACTOR = "apify~threads-profile-api-scraper"
RUN_SYNC = "https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"
RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
CACHE_MAX_ENTRIES = 256
CACHE_TTL_SECONDS = 6 * 60 * 60
SIGNUP_URL = "https://console.apify.com/settings/integrations"
# igview-owner~threads-search-scraper enforces a floor on maxPosts.
SEARCH_MIN_POSTS = 20


class ApifyError(RuntimeError):
    pass


class ApifyAuthError(ApifyError):
    """No token configured. Message explains the free path + paste fallback."""


def _retry(attempts: int = 3, base_delay: float = 0.6):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            last: Optional[Exception] = None
            for i in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except ApifyError as e:
                    if getattr(e, "status", None) not in RETRYABLE_STATUSES or i == attempts - 1:
                        raise
                    last = e
                    time.sleep(base_delay * (2 ** i) + random.uniform(0, 0.3))
            if last:
                raise last
        return wrapper
    return decorator


def _search_post(p: dict) -> dict:
    """Map a row from the search actor into a clean post dict."""
    return {
        "id": p.get("postId"),
        "code": p.get("postCode"),
        "text": p.get("captionText"),
        "author": p.get("username"),
        "author_verified": p.get("isVerified", False),
        "likes": p.get("likeCount", 0),
        "replies": p.get("directReplyCount", 0),
        "reposts": p.get("repostCount", 0),
        "quotes": p.get("quoteCount", 0),
        "is_reply": p.get("isReply", False),
        "created_at": p.get("takenAtISO"),
        "url": p.get("postUrl"),
    }


def _profile_post(p: dict) -> dict:
    """Map a row from latestPosts (profile actor) into a clean post dict."""
    cap = p.get("caption") or {}
    info = p.get("text_post_app_info") or {}
    user = p.get("user") or {}
    code = p.get("code")
    author = user.get("username")
    return {
        "id": p.get("pk"),
        "code": code,
        "text": cap.get("text"),
        "author": author,
        "likes": p.get("like_count", 0),
        "replies": info.get("direct_reply_count", 0),
        "reposts": info.get("repost_count", 0),
        "quotes": info.get("quote_count", 0),
        "created_at": p.get("taken_at"),
        "url": (f"https://www.threads.com/@{author}/post/{code}"
                if author and code else None),
    }


def _profile(d: dict) -> dict:
    """Map a row from the profile actor into a clean profile dict."""
    links = d.get("bio_links") or []
    return {
        "username": d.get("username"),
        "full_name": d.get("full_name"),
        "followers": d.get("follower_count"),
        "biography": d.get("biography"),
        "verified": d.get("is_verified", False),
        "is_private": d.get("is_private", False),
        "bio_links": [l.get("url") for l in links if isinstance(l, dict) and l.get("url")],
        "url": d.get("url"),
        "latest_posts": [_profile_post(p) for p in (d.get("latestPosts") or [])
                         if isinstance(p, dict)],
    }


class ApifyClient:
    def __init__(self, token: Optional[str] = None, timeout: int = 180):
        self.token = token or os.environ.get("APIFY_TOKEN")
        self.timeout = timeout
        self._cache: "OrderedDict[str, tuple[float, Any]]" = OrderedDict()

    def _require(self) -> str:
        if not self.token:
            raise ApifyAuthError(
                "No APIFY_TOKEN set. Get one free at "
                f"{SIGNUP_URL}. Or paste the posts you already have and "
                "the skill will run the same analysis on them."
            )
        return self.token

    def _cget(self, k):
        h = self._cache.get(k)
        if h and (time.time() - h[0]) < CACHE_TTL_SECONDS:
            self._cache.move_to_end(k)
            return h[1]
        return None

    def _cput(self, k, v):
        self._cache[k] = (time.time(), v)
        self._cache.move_to_end(k)
        while len(self._cache) > CACHE_MAX_ENTRIES:
            self._cache.popitem(last=False)

    @_retry()
    def _run(self, actor: str, payload: dict) -> list[dict]:
        try:
            r = requests.post(RUN_SYNC.format(actor=actor),
                              params={"token": self._require()}, json=payload,
                              timeout=self.timeout)
        except requests.RequestException as e:
            err = ApifyError(f"network error: {e}"); err.status = 503; raise err
        if r.status_code >= 400:
            err = ApifyError(f"actor returned {r.status_code}: {r.text[:200]}")
            err.status = r.status_code; raise err
        data = r.json()
        if not isinstance(data, list):
            raise ApifyError(f"unexpected response shape: {str(data)[:150]}")
        return data

    # ---- public read methods ----
    def fetch_niche_posts(self, query: str, max_items: int = 30, sort: str = "top",
                          force_refresh: bool = False) -> list[dict]:
        """Top/recent Threads posts for a niche query or hashtag.

        sort is "top" (default) or "recent". A hashtag works as the query too
        (pass it with or without the leading #). The search actor enforces a
        floor of 20 posts per run, so smaller max_items is bumped up.
        """
        q = query.strip()
        want = max(int(max_items), SEARCH_MIN_POSTS)
        ck = f"search:{q}:{want}:{sort}"
        if not force_refresh and (c := self._cget(ck)) is not None:
            return c[:max_items] if max_items < len(c) else c
        rows = self._run(SEARCH_ACTOR,
                         {"searchQuery": q, "sort": sort, "maxPosts": want})
        out = [_search_post(p) for p in rows if isinstance(p, dict) and p.get("postId")]
        self._cput(ck, out)
        return out[:max_items] if max_items < len(out) else out

    def fetch_profile(self, username: str, force_refresh: bool = False) -> Optional[dict]:
        """A Threads profile's stats (followers, bio, verified) plus its most
        recent posts with engagement. Yours or a competitor's. Returns None if
        the username is not found."""
        u = username.lstrip("@").strip()
        ck = f"profile:{u}"
        if not force_refresh and (c := self._cget(ck)) is not None:
            return c
        rows = self._run(PROFILE_ACTOR, {"usernames": [u]})
        prof = None
        for d in rows:
            if isinstance(d, dict) and d.get("username"):
                prof = _profile(d)
                break
        self._cput(ck, prof)
        return prof


if __name__ == "__main__":
    import json as _json
    c = ApifyClient()
    print("--- niche search ---")
    print(_json.dumps(c.fetch_niche_posts("AI marketing", max_items=3), indent=2)[:1200])
    print("--- profile ---")
    p = c.fetch_profile("zuck")
    if p:
        print(_json.dumps({k: v for k, v in p.items() if k != "latest_posts"}, indent=2))
        print("latest_posts:", len(p["latest_posts"]))
