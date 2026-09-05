# Threads Post Audit

Run any Threads post or thread draft through the 2026 Threads ranking checklist.
Catches AI tells, format violations (500-char fit, one-hashtag cap), reach
suppressors (link placement), tone mismatches (transplanted X dunk), and
structural weaknesses before publishing. This is the `threads-humanizer --mode
audit` workflow: detection only, no rewrite.

## When to use

- Before publishing a hand-written or AI-drafted post or thread
- When `threads-post-writer` finishes a draft (auto-invoked)
- When a recent post underperformed and the user wants a post-mortem

## Input

- A post, or a thread (with or without `---` breaks)
- Optional: target audience, scheduled time

## Output

- **Pass / Fail** header
- **Blockers** (must fix before publishing): em dashes over the cap, posts at
  3+ AI markers, reveal bridges, sincerity openers, dead closers ("Thoughts?",
  "Let that sink in."), links in post 1, over-length posts, a second hashtag
- **Warnings** (ship-risky): staccato stacks, missing referenced numbers,
  cold X tone
- **Suggested fixes** for each issue
- **Per-post tell density** (markers, em dashes, fragments, triads). No
  detector score: on post-length text those are noise and the skill does not
  promise to beat them
- **Timing recommendation** given the audience

## Checks

### Blockers (auto-fail)

1. More than one em dash in a post; en dash between clauses; double dash. A
   single em dash in a post that needs it is not a blocker.
2. A single post over 500 chars (and no text attachment in play).
3. Two or more hashtags (Threads rejects the second at the platform level).
4. External link in post 1 of a thread, or in a single post meant to reach.
5. Opens with "In today's fast-paced world" or similar, a reveal bridge
   ("Here's what", "Stop X, start Y"), or a sincerity announcement ("let me be
   honest", "not gonna lie", "unpopular opinion:" on a popular take).
6. Ends with "What do you think?", "Thoughts?", or "Let that sink in." (a
   specific warm question is fine).
7. Any post with 3+ vocabulary / grammar markers, or any negative-parallelism
   / "The result?" reveal bridge (see `../references/scrub-rules.md`).
8. First line does not stand alone as a hook (it needs line 2 to make sense).
9. Engagement bait ("repost if you agree", "reply YES").

### Warnings (flag with a suggested fix)

10. More than 2 emoji, or any emoji on a serious/contrarian take.
11. Staccato stacks ("Short. Punchy. Done.", "No X. No Y. Just Z."), one-word
    lines for drama, more than 2 standalone fragments in a thread, an inserted
    3-word "punch post" with no content, or a long/short/long/short seesaw.
    Do not flag uniform post length: on Threads uniform rhythm wins at every
    length in our corpus, and never suggest adding variance.
12. No odd-precision number with a named referent anywhere the claim would
    allow one (a bare number does not clear this).
13. No named entity (person, company, tool).
14. Stacked or perfectly parallel rule-of-three, a hollow triad without
    concrete items, or a second triad in the same post (one natural triad
    passes).
14a. Hedging stack ("perhaps", "it seems", "just my two cents") or a framed
    confession ("ngl this hurt: ..."). A flat dated fact is fine.
14b. Over-scrubbed (only when auditing a humanizer rewrite with the original in hand to compare against; a fresh draft that never had an em dash or a triad is not over-scrubbed): uniformly flat tone, warmth or lowercase register gone, no
    reaction or opinion anywhere.
15. Thread post 1 closes its own loop (no reason to tap in).
16. The best item or beat is buried at the end of a teaching thread.
17. No clear primary goal: the draft chases replies, reposts, likes, and quotes
    all at once. Pick one (see `../../../references/hook-formulas.md`
    "Engagement-goal split").
18. A single post trying to carry two ideas (should be two posts or a thread).
19. A cold, combative, newsy X tone that reads as out of place on Threads.

### Info (neutral notes)

20. Suggested posting window given the audience.
21. Single post vs thread recommendation given the material.
22. Repost-bait opportunity: if the draft is a list/framework/how-to, note that
    it should be structured to maximize reposts (Threads' save analog).

## Steps

1. Detect the container: single post, or thread (split on `---` or estimate
   Publora's auto-split).
2. For each post, count chars and run the blocker checks.
3. If any blockers, return **FAIL** with specific fixes; optionally offer to hand
   off to `threads-humanizer` for an auto-rewrite.
4. If no blockers, run the warnings.
5. Report per-post tell density. Do not estimate a detector score.
6. Return the structured report with a timing note.

## Related

- `threads-humanizer` - proportional rewrite if the audit fails
- `threads-post-writer` - regenerate using a proven formula
