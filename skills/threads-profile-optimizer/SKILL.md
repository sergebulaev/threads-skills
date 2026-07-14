---
name: threads-profile-optimizer
description: 'Audit and rewrite a Threads (Meta) profile end-to-end for 2026: profile photo, name with a searchable keyword, @handle, bio (150 chars, warm and specific), link, pinned post, and the connected-Instagram cross-pull that feeds Threads discovery. Triggers on "review my Threads profile", "fix my Threads bio", "what to pin on Threads", and "profile audit". Turns a default profile into one that converts visitors into followers. Not for writing posts (use threads-post-writer).'
---

# Threads Profile Optimizer

Audit the parts of a Threads profile (photo, name, @handle, bio, link, pinned
post) against what actually converts a profile-visitor into a follower in 2026,
then rewrite each part that needs it. On Threads the whole decision happens in a
couple of seconds on the profile card: name, bio, pinned post. Threads runs
warmer than X, so the bio should read like a person, not a company. And because a
Threads account is stapled to an Instagram account, a strong Instagram presence
feeds Threads discovery, so this skill checks that cross-pull too.

## When to use

- User pastes their Threads profile or handle and asks for an audit
- "Fix my Threads bio", "rewrite my bio", "what should I pin on Threads"
- User is starting to post seriously and wants the profile to match
- Any of: "review my Threads profile", "profile audit", "what to pin on Threads"

Not for writing posts (use `threads-post-writer`) or auditing a single draft
(use `threads-humanizer`).

## Input

- Profile URL / handle (or a screenshot of the profile card)
- Goal: **grow a following** / **drive signups** / **land clients** / **build
  authority**. The bio close and the pinned post change by goal.
- Optional: their best-performing posts, to pick a pin
- Optional: the connected Instagram handle, to score the cross-pull

## Output

1. **Scorecard** (each part: pass / needs-work / fail)
2. **Priority fixes** ranked by impact (bio and pin first, always)
3. **Before -> After** rewrites for each failing part
4. **Pinned-post pick** with the reason
5. **Instagram cross-pull note**: what to fix on IG so it feeds Threads

## Steps

1. **Intake.** Collect the profile state, the goal, and the connected Instagram
   handle if they want the cross-pull scored.
2. **Score each part** against the scorecard below.
3. **Rewrite the bio (150 chars).** Shape: `who you help or what you post about +
   one specific + a warm human line`. Lead with the value, not a job title. Write
   it like you talk. No "I help X do Y" cliche opener unless the rest is specific.
   Fit inside 150 chars, tight wins.
4. **Fix the name.** Real name plus a searchable keyword people actually type
   (e.g. "Sam Rivera, AI agents"). The name field is searchable; the @handle
   mostly is not, so the keyword belongs in the name.
5. **Check the @handle.** Short, memorable, matches the Instagram handle if
   possible (Threads and Instagram share the handle, so consistency helps
   discovery). No stray numbers or underscores if avoidable.
6. **Pick the pinned post.** Their single best proof of what a new follower gets:
   a top post, a mini-thread that teaches, or a clear offer matched to the goal.
   You can pin up to 3 on Threads; lead with the strongest. An empty pin slot
   wastes the most valuable real estate on the card.
7. **Set the link.** One link matched to the goal (newsletter / offer / site). If
   they need several, a single link-hub, not a bare homepage.
8. **Photo check.** Clear face, fills the frame, recent, high contrast. It renders
   as a small circle for most viewers, so detail is wasted but contrast is not.
   Match the Instagram photo so the two profiles read as one person.
9. **Score the Instagram cross-pull.** A connected, active Instagram with an
   aligned name, photo, and bio feeds Threads suggestions and "who to follow".
   Flag a dormant or mismatched IG as a discovery leak, and name the one fix.
10. **Deliver the before/after diff** plus the two-second test: read only name,
    bio, and pin, and ask "would a stranger follow from this alone?"

## Scorecard

| # | Part | Pass criteria (2026) |
|---|------|----------------------|
| 1 | **Photo** | Clear face filling the frame, recent, high contrast at small size, matches the Instagram photo |
| 2 | **Name** | Real name plus a searchable keyword, reads human, inside the name limit |
| 3 | **@handle** | Short, memorable, matches the Instagram handle, no stray numbers/underscores |
| 4 | **Bio** | Value plus one specific plus a warm line, inside 150 chars, no cliche opener, leads with what a follower gets |
| 5 | **Link** | One, goal-matched; a link-hub if several are needed |
| 6 | **Pinned post** | Present (up to 3), and the lead pin is their best proof matched to the goal, not a random recent post |
| 7 | **Instagram cross-pull** | Connected IG is active, with an aligned name, photo, and bio, so it feeds Threads discovery |

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- The bio must pass the two-second test: a stranger reading only name plus bio
  plus pin should know who this is for and want to follow.
- Lead the bio with the reader's benefit, not the user's job title.
- Keep the bio warm and human, not corporate. It reads like the person talks.
- One specific or one number in the bio where the account allows it.
- Keep every rewrite inside the platform limits (bio 150 chars). Never ship a
  truncated bio.
- Treat the connected Instagram as part of the profile, not a separate thing. A
  dormant or mismatched IG is a discovery leak worth flagging.
- No em dashes. No "leverage", "fundamentally", "game-changer".

## Related skills

- `threads-post-writer` - write the posts and threads the optimized profile hosts
- `threads-hook-extractor` - find a pin-worthy hook in a post that already worked
- `threads-content-planner` - plan the cadence that keeps the profile active
