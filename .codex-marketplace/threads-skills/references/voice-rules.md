# Voice Rules for Threads (Meta)

These are the canonical voice rules for the whole bundle. Every skill inherits
them. Skill-local "Hard rules" sections only add format-specific overrides
(char ranges, threading rules) and point back here.

Threads is the warmer, less newsy sibling of X. Same text-first shape, but the
register is conversational and community-driven, not hot-take combat. The
platform rewards genuine back-and-forth over dunks. Write like you are talking
to people who already like you, not performing for strangers.

## Hard rules

1. **Em dashes (`—`) capped at one per post** (about 1 per 100 words in a
   long text-attachment post), and none in a post that reads fine without one.
   The character is no longer a tell (2026 models use fewer than humans); the
   density is, and on Threads em dashes are rare in top posts (7% of our
   corpus). Replace the excess with a comma, colon or `..`, never a period. No
   en dashes (`–`) between clauses, no double dashes (`--`).
2. **Use `..` as a soft pause** when you would reach for a second em dash.
   Reads human and matches how people actually type on Threads.
3. **Capitalize personal names, company names, product names** (Stripe, Claude,
   Vercel). Lowercase a brand name and it reads as careless.
4. **Sentence starts can be lowercase.** Lowercase openers are native to the
   Threads register and often outperform capitalized ones. Names inside are
   always capitalized.
5. **Specific numbers beat adjectives.** 2.4x beats "way better". $873.47 beats
   "cheap". One real number per post where the claim allows it.
6. **One idea per post.** A post with two ideas is two posts, or a thread.
7. **Don't hard-sell your own product** in a reply or a quote on someone else's
   post. Describe what you do instead.

## Vocabulary markers (density-scored)

Count these per post. One is English; two is borderline (flag it in the report, leave the words);
three in one post reads as AI and the whole post gets rewritten (see `threads-humanizer` V3).
The durable 2026 set (significant, crucial, notably, particularly,
comprehensive, insights, robust, leverage, foster, landscape, nuanced,
streamline, elevate, empower) counts alongside the older corporate words:
- leverage, utilize, facilitate, streamline, robust, seamless, delve, navigate,
  unlock, harness, foster, cultivate
- fundamentally, essentially, ultimately, crucially, notably
- landscape, ecosystem, paradigm, realm, tapestry, journey

## Always forbidden (single hit, regardless of density)

These are scrubbed on sight. They are reveal bridges, negative parallelism,
dead phrases or performed sincerity, not vocabulary:
- "It's not just X, it's Y"
- "In today's fast-paced world"
- "game-changer", "deep dive", "at the end of the day", "needle-mover"
- Sincerity announcements as an opener or pivot: "let me be honest", "I'll be
  real", "honestly?", "real talk", "not gonna lie", "unpopular opinion:" on a
  take that is actually popular. State the fact flat instead.

## Threads-native style

- **Warm beats sharp.** X rewards the contrarian one-liner; Threads rewards the
  same idea framed as an invitation to talk. "Most agents fail on retries, not
  reasoning. what broke for you?" out-performs the bare dunk.
- **Lowercase-casual is the default register.** It signals you are a person, not
  a brand account. Use it freely; only go formal for a genuinely serious take.
- **Line breaks are punctuation.** A single hard return between two short lines
  reads as a beat. Use whitespace to control pacing inside a post.
- **Emoji: 0-2 per post.** Threads tolerates a slightly warmer emoji register
  than X, but a post sprinkled with 5 still reads as a brand account or AI.
  Serious takes use zero.
- **Hashtags: 0 or 1. Threads allows only ONE per post.** A second hashtag is
  rejected by the platform, not just frowned on. If you use one, put it at the
  end.
- **Links: up to 5 per post are allowed,** but a link in the opening line still
  costs reach. Keep links out of the first post of anything you want to travel.

## Length

- **Per post: 500 characters.** Write to land the whole idea inside it. A post
  that needs 540 chars needs an edit, or it should become a thread.
- **Text attachment: up to 10,000 chars** when you attach the longer-form text,
  but a wall of text still underperforms a tight one. Length is a ceiling, not a
  target. Reach for a thread before a 2,000-char monolith.
- **Thread posts: keep each one able to stand alone.** A reader who lands on
  post 4 from a repost should still get something.

## Structure

- The **first line of a single post, or post 1 of a thread, carries the whole
  load.** Threads truncates long posts in feed with a "more" cut, so front-load
  the hook into the first line.
- **End on a landing, not a dead prompt.** "What do you think?" is dead. A
  specific question that invites a real answer, a sharp closing line, or a clean
  stop all beat it. On Threads a genuine question is stronger than on X because
  the audience actually replies.
- For threads, **the last post earns the repost.** Close with the most quotable
  line or a clear call to repost/follow, not a limp "that's it".

## Anti-patterns

- Thesis restatement of someone else's post ("so true, this changes
  everything").
- Generic praise in replies ("great thread!", "love this").
- Overused openers: "This.", "100%", "Couldn't agree more", "Unpopular opinion:"
  on a take that is actually popular.
- Stacked or hollow rule of three ("faster, cheaper, better"); one natural
  triple with concrete items is fine.
- Padding a one-line idea into a thread.
- ALL CAPS first lines for intensity. Carry intensity with word choice.
- X-transplant tone: importing a cold, newsy, dunk-heavy X voice onto Threads
  reads as out of place. Warm it up.

## Algorithmic note (NLP-level)

Threads' ranker leans hard on replies and on relationships (it surfaces posts
from accounts you and your network engage with). A post that earns real replies
(not one-word "this") and gets reposted travels further than one that only
collects likes. Before posting, check: does this give a reader a reason to
reply, repost, or quote? If it only earns a passive like, sharpen it.
