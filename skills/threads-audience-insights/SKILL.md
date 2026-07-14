---
name: threads-audience-insights
description: Read your Threads (Meta) audience and niche from real data. Scan a niche query or hashtag for the top posts right now with likes, replies, reposts, and quotes, and pull a profile (yours or a competitor) for follower count, bio, verified status, and recent posts with engagement. Powered by Apify, no login. Triggers on "analyze Threads", "what is working on Threads", "top posts for", "competitor Threads profile", "niche scan", "follower count". Not for writing posts (use threads-post-writer).
---

# Threads Audience Insights

Turn real Threads data into a read on what is working: which posts in your niche are landing right now and why, and how an account performs (its follower count, its recent posts, the engagement each one pulls). This is the read layer, so the skill sees actual numbers instead of guessing.

One honest limit: Threads does not expose a usable list of who **liked** or engaged with a post. That data is cookie-gated, capped at around 100, and has no public API. So there is no engager roster here. The signal is **niche discovery + profile stats + per-post engagement counts** (likes, replies, reposts, quotes), which on Threads is what tells you whether a post traveled. A reply is the heaviest ranking signal on Threads, so replies matter more than raw likes when you read a winner.

## When to use

- "What is working on Threads for [topic]" / "scan the niche for top posts"
- "Analyze [my / a competitor's] Threads profile"
- "How many followers does [account] have, and what are they posting"
- "Which hooks and formats are traveling on Threads right now"

Not for writing a post or a thread (use `threads-post-writer`) or reverse-engineering one hook (use `threads-hook-extractor`).

## Setup (optional)

The read layer uses **Apify** (no login, no cookies). Get a free token at `https://console.apify.com/settings/integrations` and set `APIFY_TOKEN` in `.env`. No token? Paste the posts you already have and the skill runs the same analysis on them.

## Input

- A niche query or hashtag (e.g. "AI marketing", "#buildinpublic"), or
- A username (yours or a competitor's), or
- Both, plus the goal (niche scan / profile read)

## Output

1. **Niche scan** - top posts for the query ranked by engagement, with the pattern behind the winners (hook shape, length, single vs thread, reply-bait vs statement)
2. **Profile read** - the account's follower count, bio, verified status, and its recent posts ranked by engagement
3. **Action list** - what to write more of, which accounts to watch, which formats travel now. Route drafts to `threads-post-writer`.

## Steps

1. **Pull the data.** For a niche: `lib.ApifyClient().fetch_niche_posts(query, max_items=30, sort="top")`. For a profile: `fetch_profile(username)`. Falls back to pasted data if no token.
2. **Rank by engagement.** Sort by a blend of replies + likes + reposts + quotes. Weight **replies highest** (heaviest Threads ranking signal). Normalize against the author's follower count when you have it, so a small account's breakout is not buried under a big account's baseline.
3. **Extract the pattern.** For the top posts, name what they share: the hook shape (one-liner, confession, list, question), the length, single vs thread, whether it opens a reply loop. That is the repeatable part.
4. **Read the profile.** From `fetch_profile`, report follower count, bio, verified status, and which of its recent posts pulled the most engagement. Note the format mix.
5. **Build the action list.** Write-more-of (the winning pattern), watch (specific accounts), formats-that-travel. Route drafts to `threads-post-writer`.
6. **Deliver the report** in the Output shape, with the raw ranked posts attached.

## What the read layer exposes

| Method | Returns |
|---|---|
| `fetch_niche_posts(query, max_items, sort)` | top/recent posts for a niche query or hashtag: text, likes, replies, reposts, quotes, author, verified, url |
| `fetch_profile(username)` | profile stats: username, full_name, followers, biography, verified, bio_links, plus recent posts with engagement |

There is intentionally no engager/liker method. Threads walls that data; do not imply otherwise.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific rules:

- Be honest that there is **no engager or liker list** on Threads (cookie-gated, ~100 cap, no public API). The read is discovery + profile stats + per-post counts, not a roster of who engaged.
- **Weight replies over likes.** A reply is the heaviest ranking signal on Threads, so a post with many replies beats one with many likes at the same total.
- **Normalize engagement by follower count** before calling a post a winner, or you extract "big account" effects, not "good post" effects.
- Never invent a post, a number, or a pattern. If the search returns thin, say so and pull a known account's profile instead.
- A pattern is only a pattern if it recurs across several top posts, not one.
- `fetch_niche_posts` runs a minimum of 20 posts per Apify run even when you ask for fewer (actor floor); it trims the return to `max_items`.

## Related skills

- `threads-post-writer` - write more of what the data shows is working
- `threads-hook-extractor` - reverse-engineer a hook from a top-performing post
- `threads-reply-drafter` - reply to a high-traction post the scan surfaced
- `threads-content-planner` - feed the winning patterns into a weekly plan
