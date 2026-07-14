# Classification Rules

How to map a Threads post or thread to one of the 13 formulas (T1-T13). Extract
features first, then score.

## Step 1: container

| Signal | Container |
|---|---|
| One self-contained post, no thread tail | single post -> T1-T6, T11-T13 |
| Multiple connected posts, or a "see more" thread tail | thread -> T7-T10 |
| A post with another post embedded above the text | quote post -> likely T4 |

## Step 2: single-post features (T1-T6)

| Feature in the text | Formula |
|---|---|
| A flat, against-the-common-belief opinion, framed warmly | T1 Warm Contrarian |
| Built around one odd-precision number (1.3s, $873.47, 2.4x) | T2 Data-Point Hook |
| A real personal metric or admission ("we did X", "i lost Y") | T3 Build-in-Public Confession |
| Quotes another post and adds a reframe or counter | T4 Quote-Post Add-Value |
| A short numbered or bulleted list, one line per item, fits one post | T5 Mini-List Post |
| A relatable shared moment with no setup, names a feeling | T6 Relatable Cold-Open |
| A flat first-person status/milestone, then a counterintuitive pivot ("I'm a millionaire. Don't start a business.") | T11 First-Person Status Flex |
| "Most {group} DON'T NEED {thing}, they need {permission}", often caps-forward | T12 Permission Reframe |
| One before/after copy swap ("Instead of X, say Y") | T13 Copy-Swap Micro-Lesson |

## Step 3: thread features (T7-T10)

| Feature in post 1 + body | Formula |
|---|---|
| "N things that Y" promise, then one teaching post per item | T7 Listicle-Thread Promise |
| Opens mid-scene at the tension, narrative beats, a turn near the end | T8 Story Thread |
| A surprising result stated, the mechanism withheld ("here is why") | T9 Curiosity-Gap Opener |
| "how i {result} in {timeframe}", then one actionable step per post | T10 How-I Teardown |

## Step 4: confidence scoring

- Count matched features per formula. The formula with the most distinctive
  matches wins.
- If two are within one feature of each other, return both with fit percentages.
- A quote post that also delivers a list is T4 by container but borrows T5's
  structure; note both.

## Step 5: primary goal

Infer what the original optimized for from its shape and its visible metrics:

| Shape | Likely goal |
|---|---|
| Sharp opinion, high reposts | reposts (T1, T2) |
| List / framework / how-to, high reposts | reposts (T5, T7, T10) |
| Personal metric / question, high replies | replies (T3, T9) |
| Story / relatable, high likes | likes (T6, T8) |
| Quote post adding a take, high quotes | quotes (T4, T8) |

## Step 6: source audit

Flag, do not copy:
- em dashes, en dashes, double dashes
- AI vocab (leverage, fundamentally, delve, etc.)
- 2+ hashtags (Threads rejects the second) or mid-sentence hashtags
- an external link in post 1
- a first line that does not stand alone
- a cold, combative X tone that reads as out of place on Threads

## Output: the blank template

Reproduce the winning formula's skeleton from
`../../references/hook-formulas.md`, swapping the original's specifics for
`{slot}` markers matched to the user's topic. Keep the open-loop mechanic intact
for threads and the warm invite for single posts.
