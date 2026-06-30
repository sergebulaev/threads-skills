# Scrub Rules

Tiered catalogs the humanizer applies. Load this file when actually executing a
scrub. Two tiers: forensic (always on) and strict (default on).

## FORENSIC tier (always on)

Real model leakage no human types. Delete or flag on sight.

| Pattern | Action |
|---|---|
| `oaicite`, `contentReference`, `turn0search0`, `attached_file`, `grok_card` | delete the marker |
| "As of my last update", "As of my knowledge cutoff", "I cannot browse" | delete the disclaimer line |
| `[Your Name]`, `[Company]`, `[insert X here]`, `YYYY-MM-DD` template blanks | flag, ask the user to fill |
| 3+ em dashes in a single post or short thread | replace each with `..`, a period, or a line break |

## STRICT tier (default on)

Bad Threads style regardless of who wrote it.

### Punctuation

- Curly quotes -> straight quotes.
- `--` -> a period or a line break.
- Em dash (`—`) / en dash (`–`) -> `..`, a comma, or two sentences.

### Vocabulary swaps

| AI word | Swap to |
|---|---|
| leverage | use |
| utilize | use |
| facilitate | help |
| streamline | simplify |
| harness | use |
| foster | build |
| delve | look at |
| navigate (figurative) | handle |
| unlock | open up |
| robust | solid |
| seamless | smooth |
| cultivate | grow |

### Filler adverbs (delete)

fundamentally, essentially, ultimately, crucially, notably, simply, just (as a
hedge), really (as a hedge).

### Dead phrases (delete or rewrite)

- "in today's fast-paced world"
- "at the end of the day"
- "game-changer", "deep dive", "move the needle", "needle-mover"
- "it's not just X, it's Y"
- "the world of {thing}"

### Dead closers (rewrite to a landing or a specific invite)

- "What do you think?"
- "Thoughts?"
- "Let me know in the replies."
- "Tag someone who needs this."

## Threads-format scrubs (always apply)

- A single post over 500 chars (no attachment): flag and tighten, or escalate to
  a thread.
- 2+ hashtags: cut to 0 or 1 (Threads rejects the second), move to the end.
- More than 2 emoji, or any emoji on a serious take: cut.
- External link in post 1: move to a reply or post 2+.
- First line that needs line 2 to make sense: rewrite so it stands alone.
- A thread of uniform-length posts: break at least one into a short punch.

## Tone warming (Threads-specific)

Threads is warmer than X. Soften an imported X voice:

- A bare dunk -> the same claim plus a warm invitation to talk.
- A cold, newsy declaration -> a first-person, conversational framing.
- Keep the edge of a contrarian take, lose the contempt.

## Negative parallelism

Strip the "not X, but Y" / "it isn't about X, it's about Y" constructions. They
are an AI rhythm tell. Rewrite to a direct claim.
