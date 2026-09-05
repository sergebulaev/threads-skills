# Scrub Rules (V3, 2026-09)

Tiered catalogs the humanizer applies. Load this file when actually executing a
scrub. Two tiers: forensic (always on) and strict (default on), plus the
Threads-format scrubs and tone warming. V3: vocabulary is scored by **density
per post**, not deleted per word. Em dashes are **capped** (one per post), not
banned. Forced rhythm is a tell, not a fix; on Threads uniform rhythm wins at
every length. See SKILL.md "What changed in V3" for the evidence.

## Contents

- Density scoring (how every vocabulary rule is applied)
- FORENSIC tier (always on)
- STRICT tier (default on)
- Threads-format scrubs (always apply)
- Tone warming (Threads-specific)
- Pass 2 - Rhythm (never force)
- Pass 3 - Forbidden insertions (sincerity markers, hedges)
- Preserve these (user voice, do not scrub)

---

## Density scoring (how every vocabulary rule is applied)

The cluster principle: readers spot AI text from clusters of markers, not from
any single word. One "notably" in a post is English. "Notably",
"comprehensive" and a nominalisation in the same 500 chars is a signature.

```python
def score_unit(text: str, markers: dict) -> dict:
    """Count marker hits per unit (one post; one paragraph in a long text-attachment post).
    Returns hits and the action to take."""
    hits = []
    for name, pattern in markers.items():
        for m in re.finditer(pattern, text, flags=re.I):
            hits.append((name, m.group(0)))
    n = len(hits)
    forced = [h for h in hits if h[0] in ("reveal_bridge", "neg_parallel", "sincerity_marker")]
    if n >= 3:
        action = "REWRITE_UNIT"        # 3+ markers = signal. Rewrite the post, not word-by-word.
    elif forced:
        action = "REPLACE"             # a reveal bridge / negative parallelism / sincerity marker is scrubbed on a
                                       # single hit at ANY density; any other marker beside it follows the count rule
    elif n == 2:
        action = "FLAG_ONLY"           # 2 = borderline. Report it, leave the words: the audit allows 0-2 per unit.
    else:
        action = "LEAVE"               # a single common word is not a verdict
    return {"hits": hits, "count": n, "action": action}
```

Rules of application:
- Score forensic markers separately: one hit = delete, no density threshold.
- Two patterns carry a count rule: triads (at most one natural triad per post;
  keep the first, rewrite any later one in the same post; threads are not
  pooled) and standalone fragments (more than 2 across a thread = merge back,
  see Pass 2).
- Never replace a word with a synonym from the same list. "Leverage" to
  "harness" is not a fix.
- When you rewrite a post, rewrite it in the author's register (warm
  lowercase stays warm lowercase), not in "plain" register. Plainness at
  uniform temperature is itself a fingerprint.

---

## FORENSIC tier (always on)

Real model leakage no human types. Delete or flag on sight.

| Pattern | Action |
|---|---|
| `oaicite`, `contentReference`, `turn0search0`, `attached_file`, `grok_card` | delete the marker |
| "As of my last update", "As of my knowledge cutoff", "I cannot browse" | delete the disclaimer line |
| `[Your Name]`, `[Company]`, `[insert X here]`, `YYYY-MM-DD` template blanks | flag, ask the user to fill |
| Em dashes above the cap (see below) | replace the excess with a comma, colon, `..`, or a rewrite; never a period |

### Em dash cap (one per post)

The character is not a tell: GPT-5.4 emits 1.43 em dashes per 1,000 words,
below the human 3.23. On Threads, though, em dashes are rare in top posts (7%
of our corpus) and those posts earn 0.33x the median engagement (plausibly a
formal-register confound), so the cap is tight here.

```python
def em_dash_excess(post: str) -> int:
    """Em dashes above the cap. Threads cap: 1 per post, and 0 if the post reads fine without it.
    Returns how many to replace. 0 = leave the one alone."""
    return max(0, post.count("—") - 1)

# Replacement order for the EXCESS ones (keep the one doing the most work):
#   1. comma   if the dash joins a clause to the main sentence
#   2. colon   if the dash introduces a reveal, a list, or a consequence
#   3. ".."    the Threads-native soft pause
#   4. rewrite if none of the above reads naturally
# NEVER a period. "X. Y." from a split dash creates fragment stacking, which is a worse tell than the dash.
```

---

## STRICT tier (default on)

What expert human readers cite when they spot AI text (vocabulary 53%,
sentence structure 36%). All vocabulary and grammar lists go through
`score_unit()`; reveal bridges, negative parallelism and sincerity markers are
scrubbed on a single hit.

### Punctuation

- Curly quotes -> straight quotes.
- `--` -> a comma or `..` (not a period: a period here stacks fragments).
- En dash (`–`) between clauses -> a comma. Number ranges (7-9) stay.
- Em dashes are handled by `em_dash_excess()` above, not stripped.

### Vocabulary: durable 2026 markers (density-scored)

The 2023-24 list (delve, tapestry, realm) is decaying because humans now avoid
those words. The durable markers are common words LLMs over-select at 2-5x the
human rate across 2026 frontier models. They are ordinary English, so one per
post is fine. Three in a post is a signature. On Threads the whole set is
nearly absent from top posts (1.3%), so a cluster reads as a brand account.

| Marker | Preferred replacement when the post is over threshold |
|---|---|
| significant | a number ("31% growth", not "significant growth"; ask if none exists) |
| crucial | delete, or "the" |
| notably, particularly | delete |
| comprehensive, holistic | full |
| insight(s) | say what was learned |
| robust | solid (keep if a term of art) |
| leverage | use |
| foster | build |
| landscape | field |
| nuanced | specific |
| multifaceted | delete |
| streamline | simplify |
| elevate | improve |
| empower | let |
| utilize, harness | use |
| facilitate | help |
| unlock | find |
| navigate (figurative) | handle |
| seamless | smooth |
| ecosystem | space |

Filler adverbs (each counts as one marker; delete when over threshold):
fundamentally, essentially, ultimately, crucially, notably, particularly,
arguably, certainly, definitely, undoubtedly.

### Grammar markers (density-scored; the 2026 structural signature)

```python
GRAMMAR_MARKERS = {
    # Present-participial clause openers: 5.3x the human rate.
    # "Leveraging our data, we..." / "Building on this, ..."
    "ing_opener": r"(?m)^[\s>*\-]*[A-Z][a-z]+ing\b[^.]{0,60},",
    # Nominalisations: verb-turned-noun that hides the actor. "the implementation of"
    "nominalisation": r"\bthe (\w+(?:tion|sion|ment|ance|ence|ization|isation)) of\b",
    # Stacked abstract nouns
    "abstract_stack": r"\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b.{0,40}\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b",
}
# Fix for ing_opener: put the actor first. "Leveraging our data, we cut churn" -> "we cut churn with our data."
# Fix for nominalisation: use the verb. "the implementation of the new flow" -> "when we shipped the new flow"
```

### 2026 model-idiom layer (density-scored)

Phrases that were human short-form idiom in 2024 and are model idiom in 2026.
Each counts as one marker; "let that sink in" and "that's the real story" are
scrubbed on a single hit as closers.

```python
IDIOM_LAYER_2026 = [
    r"\bquietly\b",                          # "quietly shipped"
    r"(?m)^\w+ matters\.$",                  # "distribution matters." as a line
    r"\bcompound(s|ing)?\b",
    r"\ba signal\b|\bthe signal\b",
    r"\bthe work\b",
    r"\bbuilt different\b",
    r"\bload-bearing\b",
    r"\bdoing the heavy lifting\b",
    r"\blet that sink in\b",
    r"\bthat's the real story\b",
]
```

### Reveal bridges (single hit = replace)

```python
REVEAL_BRIDGES = [
    (r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?\s*", ""),   # "The result?"
    (r"(?i)\bit'?s not \w[^,.]{0,40}, it'?s \b", None),                          # "It's not X, it's Y" (rewrite as paired declaratives)
    (r"(?i)^stop \w[^,.]{0,40}\. start \b|^stop \w[^,.]{0,40}, start \b", None),  # "Stop X, start Y"
    (r"(?im)^here'?s (what|how|why|the thing)\b[^:.\n]{0,40}[:.]\s*", ""),      # "Here's what/how"
    (r"(?im)^(plot twist|spoiler|the twist)[:?]\s*", ""),
]
# Fix: delete the bridge and let the next sentence stand. It was the point anyway.
# Named 2026 tells on every reader list; measured reach-negative on LinkedIn (vendor data).
```

### Negative parallelism (single hit = rewrite)

Strip the "not X, but Y" / "it isn't about X, it's about Y" constructions and
every sibling form ("The question isn't X, it's Y", "This isn't X. This is
Y."). Rewrite as paired declaratives, not by auto-substitution, and flag for
the user since meaning preservation needs judgement. Zero top Threads posts in
our corpus use one.

### Rule of three (strict at density; one natural triad is allowed)

Tricolon runs at 2x the expert-human rate across 2026 models. On Threads it is
rare in top posts (8%) and engagement-negative (0.28x), so the bar is a second
triad in a post, a stacked or perfectly parallel one, or a hollow one.

```python
def detect_triads(text: str) -> list:
    patterns = [
        r"(\w+), (\w+),? and (\w+)",                       # word triplets
        r"(\w+ \w+), (\w+ \w+),? and (\w+ \w+)",           # short-phrase triplets
        r"(?m)^(\w+)\. (\w+)\. (\w+)\.$",                  # "Simple. Effective. Easy." (also a Pass 2 staccato hit)
        r"\b(no \w+)[,.] (no \w+)[,.] (just|only) \w+",    # "No X. No Y. Just Z." (also a Pass 2 hit)
    ]
    return [m for p in patterns for m in re.finditer(p, text, flags=re.I)]

HOLLOW_ADJECTIVES = {"dynamic", "vibrant", "innovative", "faster", "cheaper", "better", "simple",
                     "effective", "easy", "bold", "clear", "focused", "scalable", "powerful"}
ABSTRACT_NOUNS = {"growth", "impact", "value", "alignment", "innovation", "efficiency", "results", "success",
                  "clarity", "freedom", "scale", "momentum", "consistency", "mindset", "strategy", "vision"}

def hollow(items) -> bool:
    """A triad is hollow when its items are interchangeable: every item is an abstract adjective or an
    abstract noun, and none carries a receipt (a proper name, a number, a $ or %). Equal word counts are
    NOT a tell on their own: "Stripe invoices, Vercel logs, and GitHub alerts" is a natural concrete triad."""
    def has_receipt(items) -> bool:
        for i, x in enumerate(items):
            for j, w in enumerate(x.split()):
                if re.search(r"[0-9$%]", w):
                    return True
                if w[:1].isupper() and not (i == 0 and j == 0):   # a sentence-initial capital is not a name
                    return True
        return False
    all_abstract = all(x.lower().strip() in HOLLOW_ADJECTIVES or x.lower().strip() in ABSTRACT_NOUNS
                       or x.lower().split()[-1] in ABSTRACT_NOUNS for x in items)
    return (not has_receipt(items)) and all_abstract

def triad_action(triads: list) -> list:
    """Call once per post with that post's triads. Scrub any hollow triad on sight. Of the natural
    (concrete, non-interchangeable) ones keep only the FIRST; every later triad in the same post is rewritten,
    so each post ends with at most one natural triad. Threads are not pooled: the threshold is per post."""
    actions = []
    kept_one = False
    for t in triads:
        items = t.groups()
        if hollow(items) or kept_one:
            actions.append((t, "REWRITE_AS_TWO_OR_FOUR"))   # 2 items, or 4 with one that breaks the pattern
        else:
            actions.append((t, "LEAVE"))
            kept_one = True
    return actions
```

### Dead phrases (delete or rewrite)

- "in today's fast-paced world", "in the age of AI"
- "at the end of the day"
- "game-changer", "deep dive", "move the needle", "needle-mover", "paradigm shift"
- "the world of {thing}"
- "the hard truth is" / "the uncomfortable reality is"

### Dead closers (rewrite to a landing or a specific invite)

- "What do you think?"
- "Thoughts?"
- "Let me know in the replies."
- "Tag someone who needs this."
- "Let that sink in."
- A one-word closing line ("Still.")

A specific, warm question ("what changed it for you?") is not a dead closer;
it is the reply invitation Threads ranks on.

## Threads-format scrubs (always apply)

- A single post over 500 chars (no attachment): flag and tighten, or escalate to
  a thread.
- 2+ hashtags: cut to 0 or 1 (Threads rejects the second), move to the end.
- More than 2 emoji, or any emoji on a serious take: cut.
- External link in post 1: move to a reply or post 2+.
- First line that needs line 2 to make sense: rewrite so it stands alone.
- A thread with an inserted 3-word "punch post" that carries no content: fold
  it into its neighbour (see Pass 2).

## Tone warming (Threads-specific)

Threads is warmer than X. Soften an imported X voice:

- A bare dunk -> the same claim plus a warm invitation to talk.
- A cold, newsy declaration -> a first-person, conversational framing.
- Keep the edge of a contrarian take, lose the contempt.
- Warming is not hedging. Add a question or an invitation, never "I might be
  wrong but" or "just my two cents" (inserted hedges are a Pass 3 tell).

---

## Pass 2 - Rhythm (never force)

Replaces V2's "BREAK (force burstiness)". Detectors do not score burstiness
(GPTZero dropped it in 2023). On Threads our own corpus (n=311,
length-controlled) says uniform rhythm wins at every length: Spearman -0.31
between sentence-length variance and engagement, and the low-variance half
ahead in the short, mid and long terciles. Mechanical long/short alternation
is also a learnable humanizer fingerprint. So: never force variance on any
post or thread, and remove manufactured variance everywhere.

```python
STACCATO_TELLS = [
    r"(?m)^\w+\.$",                                              # one-word line for drama: "Still." "Exactly."
    r"(?m)^(\w+\. ){2,}\w+\.$",                                  # "Short. Punchy. Done." / "Simple. Effective. Easy."
    r"(?i)\bno \w+\. no \w+\. (just|only) \w+",                  # "No X. No Y. Just Z."
    r"(?i)\ball (of )?the \w+\. none of the \w+",                # "All the X. None of the Y."
    r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?",  # "The result?" reveal (also a strict reveal bridge)
    r"(?i)\b(why|how|what happened)\? (because|simple|easy)\b",  # pseudo-Socratic Q&A
    r"(?i)\b(that's it|that's all|that's the post|full stop|period)\.$",
]

def restore_rhythm(units: list[str]) -> list[str]:
    """V3, Threads. units = posts in order. Remove staged variance only. Never manufacture variance,
    never un-flatten a uniform post (uniform rhythm wins on Threads at every length),
    never reorder or duplicate a post."""
    fragments_in_thread = 0
    for i, p in enumerate(units):
        # 1. Kill staged rhythm. Merge staccato runs into one full sentence with a real clause.
        for pat in STACCATO_TELLS:
            if re.search(pat, p):
                p = merge_into_sentence(p, pat)     # "No meetings. No decks. Just code." -> "we skipped the meetings and the decks and shipped code."

        # 2. Cap standalone fragments (<4 words): 1 per post AND 2 per thread. Both counters apply.
        fragments_in_post = 0
        for s in split_sentences(p):
            if len(s.split()) < 4:
                fragments_in_post += 1
                fragments_in_thread += 1
                if fragments_in_post > 1 or fragments_in_thread > 2:
                    p = attach_to_neighbor(p, s)    # fold into the previous sentence with a comma or colon

        units[i] = p

    # 3. A 3-word "punch post" inserted for rhythm carries no content: fold it into the post BEFORE it,
    #    or, when it is post 1, into the post AFTER it. Never wrap around; thread order is preserved.
    #    Every fold here and in step 4 is gated by fits() (500-char cap), so no merge can produce an
    #    over-length post; a punch post that fits nowhere is left in place and reported as a tell.
    if len(units) > 1:
        merged = []
        for i, p in enumerate(units):
            if len(p.split()) < 4 and not carries_content(p):
                if merged and fits(merged[-1] + " " + p):
                    merged[-1] = merged[-1] + " " + p
                elif i == 0 and fits(p + " " + units[1]):   # post 1 only folds forward; len(units) > 1 here
                    units[i + 1] = p + " " + units[i + 1]
                else:
                    merged.append(p)                        # nothing it can fold into under 500 chars: leave it
            else:
                merged.append(p)
        units = merged

    # 4. No un-flattening step on Threads: a post or thread of same-length sentences is how top Threads
    #    posts read. The one remaining check is the seesaw: if post lengths now alternate (4+ posts flipping
    #    between short <80 chars and long >=160), fold the SECOND short post into the post before it.
    lengths = [len(u) for u in units]
    if len(lengths) >= 4 and all((lengths[k] < 80) != (lengths[k + 1] < 80) for k in range(len(lengths) - 1)) \
            and all(n < 80 or n >= 160 for n in lengths):
        k = [j for j, n in enumerate(lengths) if n < 80][1]
        if fits(units[k - 1] + " " + units[k]):
            units[k - 1] = units[k - 1] + " " + units[k]
            del units[k]
    return units

def fits(post: str, limit: int = 500) -> bool:
    """Platform limit check used by every merge above: 500 chars per post (10,000 only with a text
    attachment). A merge that would not fit is skipped; the tell is left and reported instead."""
    return len(post) <= limit
```

Layout vs rhythm: a hard return between two short lines inside a post is
native Threads pacing and is **not** touched by this pass (more short lines
correlate with higher engagement in our corpus). "we cut deploy time from 40
min to 6 min." on its own line is layout. "Still." on its own line is
fragment-for-drama. The pass edits sentences, never the line breaks.

## Pass 3 - Forbidden insertions (sincerity markers, hedges)

Pass 3 adds concreteness only (a referenced odd-precision number, a named
entity, a flat dated fact, a warm question). It never adds these, and Pass 1
strict removes them when the draft already has them as an opener or pivot:

```python
SINCERITY_MARKERS = [
    r"(?im)^(let me be (honest|real|direct|clear)|i'?ll be (honest|real|direct)|honestly\?|honest (caveat|version|answer)|the honest (version|answer|truth) is|to be (direct|honest|fair|transparent)|real talk|full transparency|can i be (honest|vulnerable)|i'?ll say the quiet part|not gonna lie|ngl|unpopular opinion)[:,.]?\s*",
    r"(?i)\b(i (might|may|could) be wrong,? but|perhaps|it seems (to me )?that|in my humble opinion|i think it'?s fair to say|just my two cents)\b",  # inserted hedges: only scrub if NOT in the author's voice samples
]
# Fix: delete the marker and keep the sentence that follows. If the sentence that follows is not
# a specific fact, the marker was doing the work of vulnerability. Ask the author for the fact.
# Evidence: performed hesitancy 2x more common in LLM than expert human text; "false vulnerability"
# is a named 2026 tell. The rule is: never manufacture one, and never wrap a fact in one.
# Warmth is not a hedge: a closing question is an invitation, "I might be wrong but" is a tell.
```

## Preserve these (user voice, do not scrub)

- The warm, lowercase-casual register if that is how the user types
- `..` as a soft pause
- One or two sentence fragments used intentionally across a thread ("every
  time.") - the cap is 2 per thread, not 0
- One em dash in a post that needs it. Do not push a long text-attachment post
  to zero; zero across 300+ words is below the human baseline
- One natural rule-of-three with concrete, non-interchangeable items
- Uniform rhythm. That is how top Threads posts read, at every length
- A closing question or invitation to talk (Threads ranks on replies)
- Contractions (don't, it's, you're)
- Specific numbers with referents and named entities (add MORE, never remove)
- The author's reactions and opinions, including a blunt one. Flat tone across
  a whole thread is a humanizer fingerprint
- A single common-word marker in a post ("notably", "robust" as a term of
  art). One is not a verdict
- Their actual story. Never invent a detail to make a post land
