# Pre-Publish Audit Checklist (Threads)

The thresholds the `--mode audit` pass applies. Mirror of the root
`references/algorithm-heuristics.md` checklist, with the humanizer's blocker
distinctions.

## Blockers (auto-fail)

- [ ] No em dash (`—`), en dash (`–`), or double dash (`--`).
- [ ] Single post within 500 chars (10,000 only with a text attachment).
- [ ] At most one hashtag (Threads rejects a second).
- [ ] No external link in post 1 (single post or thread opener).
- [ ] No "In today's fast-paced world" or equivalent opener.
- [ ] No "What do you think?" / "Thoughts?" dead closer.
- [ ] No AI vocabulary blacklist words.
- [ ] First line stands alone as a hook (the feed truncates with "more").
- [ ] No engagement bait ("repost if you agree", "reply YES").

## Warnings (flag with fix)

- [ ] 0 or 1 hashtag, at the end.
- [ ] 0-2 emoji, none on a serious take.
- [ ] Thread posts vary in length (not all within ~30 chars).
- [ ] At least one specific number where the claim allows.
- [ ] At least one named entity.
- [ ] No rule-of-three list without concrete items.
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
| Teaching/list thread length | 4-7 posts |

## Scoring

- Any blocker -> **FAIL**, return fixes, offer auto-rewrite via `threads-humanizer`.
- No blockers, any warnings -> **PASS with warnings**, list each with a fix.
- Clean -> **PASS**, add the timing note and a single post vs thread sanity check.
