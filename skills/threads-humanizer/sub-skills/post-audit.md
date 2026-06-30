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
- **Blockers** (must fix before publishing)
- **Warnings** (ship-risky)
- **Suggested fixes** for each issue
- **Timing recommendation** given the audience

## Checks

### Blockers (auto-fail)

1. Em dash / en dash / double dash present.
2. A single post over 500 chars (and no text attachment in play).
3. Two or more hashtags (Threads rejects the second at the platform level).
4. External link in post 1 of a thread, or in a single post meant to reach.
5. Opens with "In today's fast-paced world" or similar.
6. Ends with "What do you think?" or "Thoughts?".
7. Contains AI vocabulary blacklist words (see `../references/scrub-rules.md`).
8. First line does not stand alone as a hook (it needs line 2 to make sense).
9. Engagement bait ("repost if you agree", "reply YES").

### Warnings (flag with a suggested fix)

10. More than 2 emoji, or any emoji on a serious/contrarian take.
11. Uniform post length across a thread (all within ~30 chars of each other).
12. No specific number anywhere the claim would allow one.
13. No named entity (person, company, tool).
14. Rule-of-three list without concrete items.
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
5. Return the structured report with a timing note.

## Related

- `threads-humanizer` - aggressive rewrite if the audit fails
- `threads-post-writer` - regenerate using a proven formula
