---
name: threads-humanizer
description: Scrub AI tells from any Threads post or thread draft, or audit a finished draft against the 2026 Threads checklist. Strips em dashes, AI vocabulary (leverage, fundamentally, delve, harness), rule-of-three lists, and uniform post rhythm, then adds human fingerprints. Includes a --mode audit pre-publish check (500-char fit, hook, one-hashtag cap, link placement, warm tone). Triggers on humanize, de-AI Threads post, audit before posting. Not for writing from scratch (use threads-post-writer).
---

# Threads Humanizer

Rewrites any Threads post or thread to remove AI tells, and audits a finished
draft against the 2026 Threads ranking checklist. Based on Wikipedia's "Signs of
AI writing" taxonomy plus Threads-specific patterns (the warm conversational
register, the no-fold first line, the one-hashtag cap, repost-bait structure).

## When to use

- Before publishing any AI-drafted post or thread (rewrite mode)
- Pre-publish review of a finished draft (audit mode, see `sub-skills/post-audit.md`)
- When a draft feels off and you cannot pinpoint why

## Input

Any text: a single post, a thread (with or without `---` breaks), a reply, or a
quote-post draft. Optional: target voice samples (the user's past posts).

## Output

- Rewritten text with AI tells removed
- A diff showing what changed and why
- Per-post char count (flagging anything over 500)
- Confidence: "human", "mixed", "AI-likely"

## Modes

```bash
# Default: scrub AI tells and fix Threads-format issues
threads-humanizer <text>

# Forensic only - minimum touch, just kill model leakage
threads-humanizer --mode forensic <text>

# Audit - detection-only pass-fail review, no rewrite
# Runs the 2026 Threads checklist: 500-char fit, first-line hook, one-hashtag
# cap, emoji limit, link placement, thread tap-through, warm tone, goal clarity.
# Returns Blockers + Warnings + suggested fixes. See sub-skills/post-audit.md.
threads-humanizer --mode audit <text>
```

## The three passes

### Pass 1 - SCRUB (delete or replace)

Apply the tiered catalogs in `references/scrub-rules.md`:

- **Forensic** (always on): real model leakage no human types. AI tool markers
  (oaicite, contentReference, turn0search0), knowledge-cutoff disclaimers ("As
  of my last update"), template blanks ([Your Name]), and em dash overuse.
- **Strict** (default on): bad Threads style regardless of origin. Vocabulary
  swaps (leverage -> use, delve -> look, harness -> use, foster -> build),
  filler adverbs (fundamentally, essentially, ultimately), phrase cleanups ("in
  today's fast-paced world", "game-changer", "deep dive"), and dead closers
  ("what do you think?").

### Pass 2 - BREAK (force burstiness)

- Vary post length across a thread. If every post is 400-450 chars, break at
  least one into a short punch post.
- Add a sentence fragment where it fits ("Every time.").
- Break perfect parallel structures with one asymmetric line.

### Pass 3 - ADD (human fingerprints)

Require where the content allows:
- 1 specific number (replace "many", "a lot", "massive")
- 1 named entity (real person, company, tool)
- the warm, lowercase-casual register if the voice calls for it
- 1 first-person concrete detail

If the input lacks these, ask the user for a number or anecdote. Do not
fabricate.

## Non-negotiable rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Preserve the user's actual claim. Humanizing does not change meaning.
- Never introduce facts that were not in the input. If a number is missing, ask.
- Keep the user's voice quirks (lowercase starts, `..` soft pauses).
- Respect the container: do not silently merge a thread into one post or split a
  single post into a thread without flagging it.
- Warm up a transplanted X dunk into a Threads-native invitation to talk.

## Threads-specific tells this skill catches

- A first line that needs the second line to make sense (the feed truncates with
  "more").
- A "post" that is 540 chars and needs a trim or a thread.
- 2+ hashtags (Threads rejects the second), or hashtags mid-sentence.
- An external link in post 1 of a thread meant to reach.
- A thread of identical-length posts (machine rhythm).
- ALL CAPS openers reaching for intensity.
- "A thread:" with no actual promise in the words.
- A cold, combative, newsy X voice that reads as out of place on Threads.

## Example

See `references/examples.md` for worked before/after rewrites.

## Files

- `SKILL.md` - this file (rewrite scrubber + audit-mode entry)
- `references/scrub-rules.md` - vocabulary swaps and regex by tier
- `references/examples.md` - worked before/after rewrites for posts and threads
- `references/audit-checklist.md` - the pre-publish checklist with thresholds
- `sub-skills/post-audit.md` - pre-publish audit workflow (detection-only, no rewrite)

## Related skills

- `threads-post-writer` - generates posts and threads that already pass the humanizer
