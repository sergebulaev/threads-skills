---
name: threads-content-planner
description: Generate a weekly Threads (Meta) content plan from a theme, audience, and content pillars. Produces per-day recommendations (single post vs thread, Threads hook formula, angle, posting time, primary goal), a single-to-thread mix, daily reply and quote-post targets, and a goal-mix balance check across replies, reposts, likes, and quotes. Use when the user wants to plan a week of Threads content instead of ad-hoc posting. Not for drafting one post or thread (use threads-post-writer).
---

# Threads Content Planner

Produce a weekly Threads plan built around a pillar discipline and the warm,
conversation-first cadence Threads rewards. Threads moves fast like X and rewards
posting multiple times a day, so the plan mixes single posts, threads, and
reply/quote-post targets.

## When to use

- User asks "plan my week on Threads" or "what should I post this week"
- User wants to escape ad-hoc posting and establish a rhythm
- Before a launch week (the plan aligns a product pillar)

## Input

- **Theme** (optional): e.g. "shipping our AI agent in public"
- **Audience description:** e.g. "indie builders, AI engineers, early founders"
- **Pillar mix** (optional): defaults to 40% Build-in-Public / 30% Insight /
  20% Engagement / 10% Promotion
- **Posting cadence** (optional): defaults to 2 posts/day on weekdays
- **Voice samples** (optional): past posts for voice calibration

## Output

A markdown plan with:

### 7-day calendar

| Day | Slot | Type | Pillar | Formula | 1-line angle | Goal | Time |
|---|---|---|---|---|---|---|---|
| Mon | AM | single | Insight | T1 Warm Contrarian | "speed is a revenue line item" | reposts | 9:30 AM |
| Mon | PM | reply block | Engagement | R-templates | 5 builder conversations | replies | 12:30 PM |
| Tue | AM | thread | Build-in-Public | T10 How-I Teardown | "how we cut deploy 40m to 6m" | reposts | 8:30 AM |
| Tue | PM | single | Insight | T2 Data-Point | "1.3s page = 2.4x conversion" | reposts | 12:30 PM |
| Wed | AM | thread | Insight | T7 Listicle-Thread | "9 landing-page mistakes" | reposts | 9:00 AM |
| Thu | AM | single | Build-in-Public | T3 Confession | "the metric we hid for a month" | replies | 8:30 AM |
| Fri | AM | single | Engagement | T6 Relatable | "friday deploy energy" | likes | 9:00 AM |

(The skill fills real angles from the theme. Weekends are optional and skew to
story threads or relatable singles, which travel well on Threads off-hours.)

### Daily reply and quote-post targets

For each day:
- **5-10 accounts to engage** (names or archetypes: "peer builders at 2-20k",
  "AI founders shipping in public", "the creators whose threads you repost")
- **Template to apply** (R1 answer, R2 concede-sharpen, R3 extend, R5 value-add quote)
- **Target:** 5-10 substantive replies per day. On Threads, replies on other
  people's posts drive more profile visits and follows than your own posts early
  on, and replies are the heaviest ranking signal.

### Weekly balance check

- [ ] Single-to-thread mix roughly 65/35 (singles for cadence, threads for depth)
- [ ] At least 1 build-in-public post (real number from your work)
- [ ] At least 1 repost-bait post (list, framework, or how-to)
- [ ] At least 1 engagement/reply-heavy day
- [ ] No pillar over 60% of the week's posts
- [ ] No formula repeated more than twice in the week
- [ ] Goal mix spread (see below): not every post chases the same signal

## Goal mix (balance the week)

Every formula earns a primary signal. A week that is all repost-bait or all
reply-bait reads as engineered. Spread the goals:

| Goal | Formulas | Weekly target |
|---|---|---|
| Replies | T3, T9, T1 | at least 2 (Threads is conversation-first) |
| Reposts | T2, T5, T7, T10 | at least 2 (reposts are the save analog) |
| Likes | T6, T8 | at least 1 |
| Quotes | T4, T8 | at least 1 |

## Rules

- **2-3 posts/day is fine on Threads.** It moves fast and rewards conversation,
  but quality still gates: do not pad to hit a count.
- **Single-to-thread mix ~65/35.** Singles keep you present daily; threads earn
  the reposts and follows.
- **Replies are a content type, not an afterthought.** Block reply time daily;
  early growth on Threads comes more from replies than from posts, and replies
  are the heaviest signal.
- **Weekday mornings (8-11 AM local) and a 12-1 PM lunch bump** are the primary
  windows; 7-10 PM works for relatable and story content.
- **Promotion pillar max 1-2 posts/week.** Overuse kills trust fast on a
  community-first platform.
- **One formula per slot, varied across the week.** Do not stack three T7 threads.
- **Keep the tone warm.** Threads punishes a transplanted combative X voice.

## Formula -> pillar mapping

| Pillar | Preferred formulas |
|---|---|
| Build-in-Public | T3 Confession, T10 How-I Teardown, T8 Story Thread |
| Insight | T1 Contrarian, T2 Data-Point, T7 Listicle-Thread, T9 Curiosity-Gap |
| Engagement | T6 Relatable, T4 Quote-Post, reply templates |
| Promotion | T10 (results that imply the product), T2 (your own data) |

## Steps

1. Gather inputs. Ask for theme, audience, pillar preferences if not provided.
2. Validate the pillar mix sums to 100%; warn if any pillar is over 60%.
3. For each day and slot, pick: type (single/thread/reply block), pillar, formula
   (do not over-repeat), angle, posting time (audience timezone), goal.
4. Add daily reply/quote-post targets with a suggested template.
5. Run the weekly balance check and the goal-mix check; flag anything missing.
6. Return as markdown, plus optional JSON for import.

## Example

See `references/example-week.md` for a filled-in 7-day plan.

## Files

- `SKILL.md` - this file
- `references/example-week.md` - worked 7-day plan
- `references/pillars-framework.md` - the Threads pillar discipline explained

## Related skills

- `threads-post-writer` - draft each single post or thread from the plan
- `threads-reply-drafter` - execute the daily reply targets
- `threads-hook-extractor` - study competitors' posts while planning
