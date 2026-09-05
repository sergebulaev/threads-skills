# Pre-Publish Audit Checklist (Threads)

The thresholds the `--mode audit` pass applies. Mirror of the root
`references/algorithm-heuristics.md` checklist, with the humanizer's blocker
distinctions. V3 (2026-09): AI tells are scored by density per post; em dashes
are capped at one per post, not banned; forced rhythm is a tell and uniform
rhythm is fine at every length on Threads.

## Blockers (auto-fail)

- [ ] No post with more than one em dash (`—`); no en dash (`–`) between
      clauses; no double dash (`--`). A single em dash in a post that needs it
      is not a blocker.
- [ ] Single post within 500 chars (10,000 only with a text attachment).
- [ ] At most one hashtag (Threads rejects a second).
- [ ] No external link in post 1 (single post or thread opener).
- [ ] No "In today's fast-paced world" or equivalent opener; no reveal-bridge
      opener ("Here's what", "Stop X, start Y"); no sincerity announcement
      opener ("let me be honest", "not gonna lie", "unpopular opinion:" on a
      popular take).
- [ ] No "What do you think?" / "Thoughts?" / "Let that sink in." dead closer
      (a specific warm question is fine and wanted).
- [ ] No post with 3+ vocabulary / grammar markers (one marker per post is
      fine); no "It's not X, it's Y" negative parallelism; no "The result?"
      reveal bridge.
- [ ] First line stands alone as a hook (the feed truncates with "more").
- [ ] No engagement bait ("repost if you agree", "reply YES").

## Warnings (flag with fix)

- [ ] 0 or 1 hashtag, at the end.
- [ ] 0-2 emoji, none on a serious take.
- [ ] No staccato stacks ("Short. Punchy. Done.", "No X. No Y. Just Z."),
      no one-word lines for drama, at most 2 standalone fragments per thread,
      no inserted 3-word "punch post" that carries no content, no
      long/short/long/short seesaw across a thread.
- [ ] Do NOT flag uniform post or sentence length. On Threads uniform rhythm
      wins at every length in our corpus; never suggest adding variance.
- [ ] At least one odd-precision number WITH a named referent where the claim
      allows (a bare number does not clear this).
- [ ] At least one named entity.
- [ ] At most one natural rule-of-three per post; no stacked or perfectly
      parallel triads, no hollow triads without concrete items.
- [ ] No hedging stack ("perhaps", "it seems", "I might be wrong but", "just
      my two cents") and no framed confession ("ngl this hurt: ..."). A flat
      dated fact is fine.
- [ ] Only when auditing a humanizer rewrite with the original in hand, not a fresh draft: not over-scrubbed, i.e. the author's warmth, reactions, lowercase register
      and one natural triad survived.
- [ ] Thread post 1 opens a loop and does not close it.
- [ ] Best item/beat is front-loaded, not buried at the end.
- [ ] One clear primary goal (replies / reposts / likes / quotes).
- [ ] One idea per post.
- [ ] Warm, conversational tone (not a transplanted X dunk).

## Thresholds quick reference

| Metric | Value |
|---|---|
| Per-post char limit | 500 (10,000 with text attachment) |
| Hashtags | 0-1 (platform hard cap is 1) |
| Links | up to 5 per post, none in post 1 |
| Emoji per post | 0-2 |
| Em dashes per post | 0-1 (about 1 per 100 words in a long text-attachment post) |
| Vocabulary / grammar markers per post | 0-2 |
| Standalone fragments | 1 per post, 2 per thread |
| Teaching/list thread length | 4-7 posts |

## Scoring

- Any blocker -> **FAIL**, return fixes, offer auto-rewrite via `threads-humanizer`.
- No blockers, any warnings -> **PASS with warnings**, list each with a fix.
- Clean -> **PASS**, add the timing note and a single post vs thread sanity check.
- Report per-post tell density (markers, em dashes, fragments, triads). Do
  not estimate a detector score: on post-length text those are noise and this
  skill does not promise to beat them.
