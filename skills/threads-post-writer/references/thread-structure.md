# Thread Structure: Pacing and the Closer

A Threads thread is a funnel. Each post's only job is to earn the tap to the next
one. Design for the drop-off, not the ideal reader who reads every post.

## Per-position roles

| Position | Role | Rule |
|---|---|---|
| Post 1 | The hook. Promise + open loop. | Carries 80% of the outcome. Must stop the scroll alone, under 500 chars. |
| Post 2 | The strongest payoff or first beat. | Front-load value here; do not save it. Tap-through is highest at 2. |
| Posts 3 to N-1 | The body. One item or beat each. | Each stands alone. Concrete examples, real numbers. |
| Post N | The closer. | Most quotable line + one clear ask. Earns the repost and follow. |

## Tap-through decay

Readers leak out at every post. Reported pattern: a meaningful share drop by
post 3, and again by post 6. Consequences:

- Put the best item at position 1 or 2, never the finale.
- 4-7 posts is the sweet spot for teaching and list threads.
- A story thread can run longer if every beat raises the stakes, but tap-through
  still falls, so the turn should not be buried at post 12.

## Opening a loop (post 1 patterns)

- A count with a catch: "7 X that Y. most people get 3 wrong."
- A withheld mechanism: "{result}. i did not expect why."
- A first-person result: "how i {number result} in {timeframe}. the exact steps."
- A story tension: "{the moment it nearly broke}. here is what happened."

The loop must stay open. If post 1 answers itself, nobody taps in.

## The closer playbook

The last post does two things and stops:

1. The single most quotable line of the whole thread (this is what gets
   screenshotted and reposted).
2. One ask, not three. Pick one:
   - "if this was useful, repost it and follow for more like this."
   - "reply with the one you would add."
   - "repost the first post if it helped someone."

Never stack all three asks. Never end on "that's it" or "hope this helps".

## Per-post scrub (apply to every post)

- [ ] Under 500 chars.
- [ ] At most one em dash per post (replace the excess with a comma, colon
      or `..`, never a period). No en dashes between clauses, no double dashes.
- [ ] No cluster of 2026 AI vocab (3+ markers in one post = rewrite it; one
      is fine): significant, crucial, notably, comprehensive, insights,
      robust, leverage, foster, landscape, nuanced, streamline, elevate,
      fundamentally, essentially; "-ing" clause openers; nominalisations.
- [ ] No reveal bridge ("The result?", "Here's what"), no "It's not X, it's
      Y", no sincerity opener ("not gonna lie", "let me be honest").
- [ ] Stands alone if read in isolation.
- [ ] At least one concrete detail (a number with a referent, a name, an
      example) in the body posts.
- [ ] At most one hashtag anywhere in the post.

## Rhythm across the thread

Let post length follow the material. A teaching post runs long because it
teaches; a transition runs short because it transitions. Do not engineer
variance on top of that: on Threads uniform rhythm wins at every length in our
corpus (Spearman -0.31 between sentence-length variance and engagement), and a
manufactured seesaw with a 3-word "punch post" dropped in for rhythm is the
humanizer fingerprint. A thread of similar-length posts is fine. Never insert
a punch post, never pad a short one, never alternate long/short on purpose.

## Hand-splitting with `---`

Default to hand-splitting so the user approves the exact breaks:

```
Post 1 text here, the hook.

---

Post 2 text, the strongest payoff.

---

Post 3 text, the next beat.
```

Publora treats each `---`-delimited block as one post in the connected thread.
If you instead pass flowing prose with no separators, Publora auto-splits at
paragraph then sentence boundaries. It does not add `(1/N)` markers, so add them
yourself in the text if you want numbering.
