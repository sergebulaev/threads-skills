---
name: threads-post-writer
description: Draft a single Threads post or a multi-post thread using a 2026 Threads hook formula (warm contrarian, data-point, build-in-public, quote-post, mini-list, relatable, listicle, story, curiosity-gap, how-I teardown), picked by goal (replies, reposts, likes, quotes). Respects the 500-char limit and one-hashtag cap, runs the humanizer pass, and publishes via Publora, which auto-splits long content into a thread. Not for auditing a draft (use threads-humanizer) or hook teardown (use threads-hook-extractor).
---

# Threads Post Writer

Ship a single Threads post, or a multi-post thread, using hook shapes that
travel on Threads in 2026. Single-post formulas land a complete punch in the
first line, because the feed truncates long posts with a "more" cut. Threads
posts run warmer and more conversational than X.

## When to use

- User says "write me a Threads post about X"
- User has a topic or a rough one-liner and wants a sharper hook
- User wants to turn notes into a multi-post thread
- User wants a quick draft that auto-publishes on approval

## Formulas this skill uses

Single-post shapes (T1-T6):

| Code | Formula | Primary goal | Best for |
|---|---|---|---|
| T1 | Warm Contrarian | reposts | a sharp, defensible take framed as an invite |
| T2 | Data-Point Hook | reposts | one odd-precision number that reframes a thing |
| T3 | Build-in-Public Confession | replies | a real metric from your own work, ugly ones included |
| T4 | Quote-Post Add-Value | quotes | adding a layer to someone else's take (quote post) |
| T5 | Mini-List Post | reposts | a scannable list that fits in one post |
| T6 | Relatable Cold-Open | likes | a specific shared moment, no setup |
| T11 | First-Person Status Flex | replies | a flat status or milestone, then a counterintuitive pivot |
| T12 | Permission Reframe | quotes | "Most {group} DON'T NEED {thing}, they need {permission}" |
| T13 | Copy-Swap Micro-Lesson | reposts | one before/after swap: weak version, then strong version |

Thread shapes (T7-T10):

| Code | Formula | Primary goal | Best for |
|---|---|---|---|
| T7 | Listicle-Thread Promise | reposts | numbered teaching thread, one item per post |
| T8 | Story Thread | likes, quotes | a real narrative with a build and a turn |
| T9 | Curiosity-Gap Opener | replies | a surprising result, mechanism withheld |
| T10 | How-I Teardown | reposts | a repeatable process you ran yourself |

Full skeletons in `../../references/hook-formulas.md`. T11-T13 were added from a
318-post corpus pull (July 2026): the status flex, permission reframe, and copy
swap topped the aspirational-warm Threads feed. They are strong hypotheses to
test, anchored on small-account examples, not yet follower-normalized.

### Pick by goal first

| Goal | Reach for |
|---|---|
| Replies | T3, T9, T1 |
| Reposts | T2, T5, T7, T10 |
| Likes | T6, T8 |
| Quotes | T4, T8 |

## Pick the container first

| If the idea is... | Container | Formulas |
|---|---|---|
| One claim, one number, one moment | single post | T1, T2, T3, T6 |
| A scannable list, one line per item | single post | T5 |
| A list where each item needs teaching | thread | T7 |
| A narrative with a build and a turn | thread | T8 |
| A surprising result with a mechanism | thread | T9 |
| A repeatable process you ran yourself | thread | T10 |

A thread on a one-line idea reads as padding. A single post trying to teach five
things should be a thread.

## How Publora splits a thread

Pass the full thread as one `content` string. Publora auto-splits it:

- at paragraph breaks (`\n\n`) first,
- then at sentence endings,
- then at word boundaries as a fallback.

Unlike X, Threads does NOT add `(1/N)` markers by default. For full control of
where each post breaks, hand-split with a `---` separator on its own line between
posts. The skill defaults to hand-splitting with `---` so the user sees exactly
how the thread will land before approving.

> If multi-post nesting is temporarily paused (Meta app reconnection), fall back
> to posting the opener as a single post and adding the rest as replies by hand.
> See `../../references/algorithm-heuristics.md`.

## Steps

1. **Gather inputs.** Topic, angle, any rough draft, target audience (builders /
   founders / a niche), and the goal (replies / reposts / likes / quotes).
2. **Pick the container.** Use the container table. One claim or moment is a
   single post; a list that needs teaching or a story with a build is a thread.
3. **Pick the formula.** Use the goal table to shortlist, then suggest 2-3 that
   also fit the topic and let the user choose.
4. **Draft.** Fill the skeleton in the user's voice. Respect the 2026 Threads
   rules:
   - First line carries the whole load (the feed truncates with "more").
   - Under 500 chars per post (10,000 only if a text attachment is in play).
   - One idea per post. Line breaks as beats.
   - 0-1 hashtag at the end (Threads allows only one), 0-2 emoji, none on a
     serious take.
   - No external link in post 1 (offer to put it in a reply).
   - Warm and conversational, not a transplanted X dunk.
5. **For a thread:** write post 1 first (the promise + open loop), front-load the
   strongest beat at position 1-2, target 4-7 posts for teaching/list threads,
   make each post stand alone, and close on the most quotable line plus one ask.
6. **Humanizer pass.** Strip em dashes, AI vocab, rule-of-three, generic openers.
   Add a specific number or named entity where the claim allows it. Vary post
   length across a thread.
7. **Optional audit.** Invoke `threads-humanizer --mode audit` for a pass-fail
   check.
8. **Approval card.** Show: formula used, full draft (thread shown post-by-post
   with per-post char counts and total post count), suggested posting window,
   primary goal. Confirm any `---` breaks.
9. **On approval.** Call `lib.publish(kind="post"` (single) or `kind="thread"`,
   `draft_text=<approved>, target_url="https://www.threads.com/",
   platforms=[<THREADS_PLATFORM_ID>], scheduled_time=<iso_or_None>,
   platform_settings=<{"threads": {"replyControl": "everyone"}} or None>)`. The
   wrapper handles Publora / manual / diy routing. If the content runs long,
   Publora auto-splits it into a connected thread.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- The first line must stop the scroll on its own. Rewrite any opener that needs
  line 2 to make sense.
- Keep each post inside 500 chars. If it does not fit, tighten it or escalate to
  a thread, never ship a truncated thought.
- One hashtag maximum. A second is rejected by Threads, not just bad style.
- One specific number where the claim allows it. 2.4x beats "way better".
- Do not hard-sell the user's product. One natural mention max.
- For a thread, post 1 must contain a real promise and an open loop. A bare
  "a thread:" label is not a hook.

## Anti-patterns (skill will refuse)

- ALL CAPS first line for intensity. Carry intensity with word choice.
- Em dashes anywhere.
- "Unpopular opinion:" on a take that is actually popular.
- Padding a one-line idea into a thread.
- Rule-of-three lists without specifics.
- "leverage", "fundamentally", "game-changer", "deep dive".
- External link in post 1.
- A second hashtag.
- Engagement bait ("repost if you agree", "reply YES").
- A thread of identical-length posts (machine rhythm).
- Importing a cold, combative X voice.

## Resources

- `../../references/hook-formulas.md` - all 10 Threads formula skeletons (T1-T6 single, T7-T10 thread)
- `../../references/algorithm-heuristics.md` - 2026 Threads ranking rules (signals, timing, limits)
- `references/single-post-checklist.md` - the per-post scrub and fit list
- `references/thread-structure.md` - per-position pacing and the closer playbook

## Related skills

- `threads-humanizer` - aggressive AI-tell scrubber, plus `--mode audit` for review
- `threads-hook-extractor` - reverse-engineer a hook from a post you admire
- `threads-content-planner` - schedule posts and threads into a weekly cadence
