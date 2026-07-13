---
name: threads-repurposer
description: Repurpose existing content into a native Threads post or thread. Take a LinkedIn post, X thread, blog, YouTube script, or newsletter and rewrite it for Threads: warm the tone, de-corporate it, refit to a short post or light thread, rebuild the hook to clear the soft fold, strip off-platform artifacts, run the humanizer, publish via Publora on approval. Not for writing from scratch (use threads-post-writer), auditing a draft (use threads-humanizer), or a hook teardown (use threads-hook-extractor).
---

# Threads Repurposer

Turn something you already made into a Threads post or thread that reads like it
was born on Threads. Repurposing is not copy-paste. A post that killed on
LinkedIn or landed on X will read wrong on Threads if you paste it: too polished,
too cold, wrong length, and artifacts ("link in bio", hashtag walls, "smash
subscribe") that scream off-platform.

This skill transforms, it does not generate. It reads your source, keeps the
idea, and rebuilds the delivery for Threads: warmer, lowercase-casual,
reply-driven.

## When to use

- "Turn this LinkedIn post into a Threads post / thread"
- "Repurpose my blog post / newsletter / YouTube script for Threads"
- "This X thread did well, adapt it for Threads"
- "I have a rough idea in another format, make it native here"

Not for a blank-page draft (use `threads-post-writer` for a post or thread), not
for reviewing an already-Threads draft (use `threads-humanizer`, plus
`--mode audit`), and not for reverse-engineering a hook (use
`threads-hook-extractor`).

## How it works

1. **Take the source.** Any format: a post, a paragraph, a script, a caption, a
   transcript, a bullet list, a link to read. Ask for the source and the goal
   (replies / reposts / likes / quotes) if not given.
2. **Extract the spine.** Strip the source platform's shell and pull out the one
   claim, the one story, or the one number worth keeping. Most repurposing fails
   because it keeps the words instead of the point.
3. **Choose the container.** One claim or number -> single post. A teach or a
   build -> a light thread (hand structure to `threads-post-writer`'s shapes). A
   LinkedIn carousel or a listicle -> a short thread, one item per post, hook
   rebuilt. A long video -> a thread that delivers the payoff, not a summary.
   Threads leans short: prefer one warm post over a long thread when the idea
   fits.
4. **Warm the tone.** Threads is conversational and lowercase-casual. De-corporate
   a LinkedIn source (cut the polish and the humble-brag frame), and turn a
   transplanted X dunk into an invitation to talk. The register is a person
   talking, not a brand broadcasting.
5. **Rebuild the hook.** Threads has a soft fold (the feed truncates long posts
   with a "more" cut), so line one must land the whole punch and stand alone. The
   source's hook almost never survives; write a new first line using a 2026
   Threads formula (see `../../references/hook-formulas.md`), picked by the goal.
6. **Refit the format.** Under 500 chars per post (10,000 only with a text
   attachment). One idea per post, line breaks as beats. Cut the source's
   connective tissue. For a thread, hand-split with `---` so the user sees the
   breaks before approving.
7. **Strip off-platform artifacts.** Remove "link in bio", "smash subscribe",
   "read more below", hashtag walls (Threads allows one hashtag max), @-handles
   that only exist elsewhere, and any "as I wrote on LinkedIn" throat-clearing. A
   repurposed post should not admit it was repurposed.
8. **Humanizer pass.** Run `threads-humanizer`: strip em dashes, AI vocab,
   rule-of-three, generic openers. Keep the user's real numbers and named
   entities from the source. Vary post length across a thread.
9. **Approval card.** Show: source -> Threads mapping (what became what), the
   container (single post or N-post thread with per-post char counts), formula
   used, warmed-tone note, primary goal. Confirm any `---` breaks.
10. **On approval.** Publish via `lib.publish(kind="post"` (single) or
    `kind="thread"`, `draft_text=<approved>,
    target_url="https://www.threads.com/", platforms=[<THREADS_PLATFORM_ID>],
    scheduled_time=<iso_or_None>)`. The wrapper handles Publora / manual / diy
    routing. Publora auto-splits an over-length draft into a connected thread at
    paragraph then sentence boundaries.

## Native-fit rules (source -> Threads)

- **LinkedIn post -> Threads:** warm it, cut the polish. Drop the corporate frame
  and the humble-brag. The LinkedIn hook is too long and too formal; rewrite it
  lowercase-casual as a person talking.
- **X thread -> Threads:** soften the combat tone. A sharp dunk becomes an
  invitation to talk. Keep the point, lose the edge that reads cold here.
- **Blog / newsletter -> Threads:** pick the one human take, lead with it, and end
  on a question. Do not summarize the whole piece.
- **YouTube script -> Threads:** lead with the payoff, not the intro. "here's what
  surprised me" beats "in this video".
- **Carousel / listicle -> thread:** one item per post, each with its own
  micro-hook, not a wall.
- **Instagram / TikTok caption -> Threads:** strip emoji density and hashtag
  blocks; Threads reads them as noise and caps hashtags at one.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Keep the source's **claim and facts** intact. Repurposing changes the delivery,
  never the meaning or the numbers.
- The new first line must stop the scroll on its own, past the soft fold. If it
  needs line two to make sense, rewrite it.
- Never paste the source verbatim and trim. Rebuild the hook and rhythm from the
  spine.
- Warm the tone every time. A cold, combative import is the most common failure.
- One specific number where the source offers one. Keep it.
- One hashtag maximum. A second is rejected by Threads, not just bad style.
- Do not hard-sell the user's product. One natural mention max.

## Anti-patterns (skill will refuse)

- Copy-pasting the source with light edits (that is not repurposing).
- Keeping the source platform's artifacts ("link in bio", "smash subscribe",
  hashtag walls, off-platform @-handles).
- Importing a cold, combative X voice instead of warming it.
- ALL CAPS first line for intensity. Carry it with word choice.
- Em dashes anywhere.
- Rule-of-three lists without specifics.
- "leverage", "fundamentally", "game-changer", "deep dive".
- An external link in post 1 (offer a reply).
- A second hashtag.
- Meta throat-clearing ("I originally posted this on...").

## Resources

- `../../references/hook-formulas.md` - the 10 Threads formula skeletons to re-hook with (T1-T6 single, T7-T10 thread)
- `../../references/algorithm-heuristics.md` - 2026 Threads ranking rules (signals, timing, limits)

## Related skills

- `threads-post-writer` - write a fresh post or thread from scratch (repurposer hands long builds to its shapes)
- `threads-humanizer` - scrub AI tells, plus `--mode audit` to review the result
- `threads-hook-extractor` - reverse-engineer a hook from a post you admire
