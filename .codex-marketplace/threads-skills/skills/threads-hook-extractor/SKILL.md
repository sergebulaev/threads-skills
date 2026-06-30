---
name: threads-hook-extractor
description: Reverse-engineer the hook from a viral Threads post or thread URL. Identifies which of the 10 canonical 2026 Threads formulas it uses (warm contrarian, data-point, build-in-public, quote-post, mini-list, relatable, listicle, story, curiosity-gap, how-I teardown), explains why it worked, and returns a blank template mapped to your topic with its primary goal (replies, reposts, likes, quotes). Use to learn from a post you admire. Not for writing your own (use threads-post-writer).
---

# Threads Hook Extractor

Paste a viral Threads post or thread URL. Get back: which hook formula it uses,
the exact structure, why it worked, and a blank template you can fill with your
own voice.

## When to use

- User finds a viral post or thread they want to study
- User wants to replicate a specific creator's pattern
- Before `threads-post-writer`, to seed a draft with a proven shape

## Input

A Threads post or thread URL (`threads.net` or `threads.com`, `/@handle/post/`).
For a thread, the URL of the first post is best.

## Output

- **Formula identified** (T1-T10 from `../../references/hook-formulas.md`) with a
  confidence score
- **Container:** single post vs thread, and why that container fit the idea
- **Structural breakdown:**
  - The hook line (and for a thread, how post 1 opens the loop)
  - Body architecture (per-post roles for a thread)
  - The close (what earns the repost or the reply)
  - Reaction-triggering devices (numbers, named entities, the open loop, the warm
    invite)
- **Primary goal** the original chased (replies / reposts / likes / quotes)
- **Why it worked** psychologically and algorithmically
- **Blank template** with `{slot}` markers matched to the original, ready for the
  user's topic
- **Cautions:** anything in the original that would fail a 2026 audit (em dashes,
  AI vocab, 2+ hashtags, link in post 1, a cold X tone)

## Steps

1. **Parse the URL.** `lib.url_parser.parse_threads_url(url)` returns `handle`,
   `post_id`, `url_type`.
2. **Get the text.** This bundle has no built-in post reader, so ask the user to
   paste the post or the full thread text. (If they later wire an Apify
   post-read actor, read it automatically.)
3. **Detect the container.** One self-contained post, or a multi-post thread.
4. **Classify against the 10 formulas** using features:
   - Single post: a warm contrarian claim (T1)? one hard number (T2)? a personal
     metric/confession (T3)? a quote post adding a layer (T4)? a one-line-per-item
     list (T5)? a relatable shared moment (T6)?
   - Thread: a numbered teaching promise (T7)? a story starting at the tension
     (T8)? a surprising result with the mechanism withheld (T9)? a first-person
     "how I" teardown (T10)?
5. **Score confidence.** If two formulas fit, return the top 2 with fit scores.
6. **Extract structure.** Label each part by its role. For a thread, map post 1
   (the loop), the front-loaded payoff, the body beats, and the closer.
7. **Name the primary goal** the original optimized for.
8. **Generate a blank template** with `{slot}` markers matched to the original
   shape and the user's topic.
9. **Audit the source.** Flag any AI tells in the original so the user does not
   copy them.

## Example

See `references/examples.md` for worked teardowns.

## Formulas reference

See `../../references/hook-formulas.md` for the 10 canonical Threads formulas
with full skeletons and goal tags.

## Files

- `SKILL.md` - this file
- `references/classification-rules.md` - feature extraction + scoring heuristics
- `references/examples.md` - worked teardowns (single post and thread)

## Related skills

- `threads-post-writer` - use the extracted template to draft your own post or thread
- `threads-humanizer --mode audit` - audit your draft before shipping
