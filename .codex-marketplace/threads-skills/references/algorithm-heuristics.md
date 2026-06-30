# 2026 Threads (Meta) Posting Heuristics

Synthesized from public statements by Adam Mosseri and the Threads team, Meta's
documented ranking principles, the Threads API publishing limits, and observed
creator data. Numbers marked "reported" are community-measured, not officially
confirmed.

## Signal weights (relative reach impact)

Threads' ranker predicts engagement and surfaces posts from accounts you and
your network interact with. The engagement types are not equal. Reported
relative weights from creator testing and Meta's stated priorities:

| Signal | Relative weight | Note |
|---|---|---|
| **Reply** (esp. with author reply back) | highest positive | Threads is conversation-first; a real back-and-forth is the strongest signal |
| **Repost** | high | re-injects into a new network and is the closest thing to a save |
| **Quote** | high | a new post on the quoter's timeline embedding yours, with their take |
| **Profile click then follow** | high | "this account is worth following" signal |
| **Long dwell / "more" expand** | medium-high | reading the whole thing counts |
| **Video completion** | medium-high | for video posts |
| **Like** | low | cheap affirmation, light reach |
| **Negative: "Not interested", mute, block, report** | heavy penalty | one report outweighs many likes |

Takeaway: optimize the first post for **replies, reposts, and quotes**, not
likes. Likes are social proof for the next reader but barely move distribution.
Threads weights replies even more heavily than X does.

## The first 30-60 minutes

- The opening window sets the trajectory. Early replies and reposts tell the
  ranker to widen distribution.
- **Reply to early replies fast.** Author engagement back on a reply is a strong
  signal and pulls the conversation up. Threads rewards the author who actually
  talks back.
- A handful of substantive replies in the first 30 minutes earns a second
  distribution test.

## Reach suppressors (avoid)

- **External links in the opening post** cost reach. Up to 5 links per post are
  allowed by the platform, but a link in post 1 still suppresses distribution.
  Put the link in a reply to your own post, or in post 2+ of a thread.
- **Engagement bait** ("repost if you agree", "reply YES") is downranked, not
  rewarded.
- **Repeated near-duplicate posts** (same post reworded) trip a similarity
  penalty.
- **High mute/block/report rate** collapses distribution fast and is slow to
  recover from.
- **More than one hashtag.** Threads allows ONE hashtag (tag) per post; a second
  is rejected by the platform.
- **A transplanted combative X voice.** Threads' audience skews warmer and
  flags dunk-heavy content as not-interested faster.

## Reach amplifiers

- **Replies you seed and sustain.** A post where the author keeps the
  conversation alive compounds reach over hours.
- **Native media** is favored. Upload images or video directly; a single image
  or short video lifts a text post.
- **Threads that get fully read** (deep tap-through) signal quality.
- **Cross-network gravity.** Threads can surface your posts to your Instagram
  graph, so an account with an engaged Instagram following gets an early lift.

## Character and format limits

| Item | Value |
|---|---|
| Post text | 500 chars (10,000 with a text attachment) |
| Hashtags | 1 per post (platform hard limit) |
| Links | up to 5 per post |
| Images per post | 10 (carousel) |
| Image size | 8 MB (JPEG, PNG; WebP auto-converted) |
| Video length | 5 min |
| Video size | 500 MB (MP4, MOV) |

- Publora auto-splits long `content` into a connected multi-post thread at
  paragraph breaks first, then sentence endings, then word boundaries. Unlike X,
  **no `(1/N)` markers are added by default.** Add them yourself in the text if
  you want them.

## Threads (multi-post)

- **Post 1 is the entire funnel.** It must promise a payoff and open a loop.
  Everything else only matters if post 1 earns the tap.
- **Front-load the value.** Tap-through decays with depth, so the strongest item
  or beat goes at position 1 or 2, not saved for the finale.
- **Optimal thread length: 4-7 posts** for a teaching or list thread. Longer
  works for a strong story but tap-through keeps dropping.
- **Each post should stand alone** enough that a reader landing mid-thread from a
  repost still gets value.
- **The last post earns the repost and the follow.** Close with the most quotable
  line, then a single clear ask (repost, follow, or "reply with yours"), not
  both.
- **Each post in a thread counts toward your posting quota** (see rate limits).
  A 5-post thread uses 5 of your daily 250.

> **Note on nested multi-post threads:** Publora's auto-split into a connected
> thread is documented but, as of mid-2026, multi-post nesting can be
> temporarily unavailable while Meta works through Threads app reconnection.
> Single posts and standalone posts always publish. When multi-post is paused,
> write the thread as separate single posts, or post the opener and add the rest
> as replies by hand.

## Rate limits

| Limit | Value |
|---|---|
| Posts per 24 hours | 250 |
| Posts per hour | 50 |
| Replies per 24 hours | 1,000 |

- Each post in a thread counts toward the post quota.
- Space posts out rather than bulk-posting; implement backoff on rate-limit
  errors. Publora queues and distributes posts to help stay inside the limits.

## Reply vs quote post

- **Reply** stays inside the original conversation. Use it to add to a thread,
  answer a question, or engage a creator. Lower reach, higher intimacy. Threads
  surfaces good replies prominently, so a sharp reply can out-travel a mediocre
  post.
- **Quote post** creates a new post on your own timeline with the original
  embedded. Use it when your addition deserves its own reach and your followers
  should see the original for context. Higher reach, more public.
- Replying to another user's post is a separate post on Threads. Publora's
  `create-post` cannot target someone else's post, so a reply or quote on
  another account is drafted here and posted by hand.

## Timing

| Audience | Best windows (local) |
|---|---|
| US tech / builders / founders | weekday mornings 8-11 AM, and a lunch bump 12-1 PM |
| Global mixed | weekday mornings in the audience timezone |
| Evening / lifestyle crowd | 7-10 PM performs for relatable and story content |

- Threads skews more evening-and-weekend friendly than X for personal and
  relatable content, because the audience treats it as a calmer, off-the-clock
  feed.
- Threads moves fast like X: a post's active life is hours, not a day. Posting
  2-3 times a day is normal for an active account.

## Reposts are the underrated lever

- Threads has no separate bookmark. The **repost is the save**: it is how readers
  keep and re-surface reference-worthy content.
- A repost is a stronger quality signal than a like because it puts the post in
  front of a new network.
- Design repost-bait deliberately: the Mini-List (T5), Listicle-Thread (T7),
  How-I Teardown (T10), and Data-Point (T2) formulas all target reposts.

## Pre-publish checklist

- [ ] First line stops the scroll on its own (the feed truncates with "more").
- [ ] No em dashes (`—`), en dashes (`–`), or double dashes (`--`).
- [ ] No AI vocabulary blacklist words (leverage, fundamentally, delve, etc.).
- [ ] At least one specific number where the claim allows it.
- [ ] No external link in post 1 (move it to a reply or post 2+).
- [ ] 0 or 1 hashtag (Threads allows only one), at the end.
- [ ] 0-2 emoji, and only if each earns its place. None on a serious take.
- [ ] Single post under 500 chars, or a deliberate thread.
- [ ] Thread post 1 opens a loop; the body closes it.
- [ ] Close is a landing or a specific invite, not "what do you think?".
- [ ] A clear primary goal (replies / reposts / likes / quotes), not all at once.
- [ ] The tone is warm and conversational, not a transplanted X dunk.
