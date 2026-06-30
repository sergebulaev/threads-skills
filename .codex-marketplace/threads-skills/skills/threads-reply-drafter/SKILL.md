---
name: threads-reply-drafter
description: Draft a reply or a value-add quote post for a specific Threads (Meta) post from its URL. Use to reply in a conversation, answer a creator, or quote-post with added value. Parses the post URL, reads pasted context, decides reply vs quote post, and drafts 1-3 warm variants in your voice. A reply to another user is a separate post and Publora cannot target it, so the draft is returned as a copy-paste block to post yourself. Not for top-level posts (use threads-post-writer).
---

# Threads Reply Drafter

Drafts a reply in a conversation, or a quote post, for a specific Threads post.
On Threads a reply to another user is a separate post that references the
original. Replies nest naturally: there is no LinkedIn-style 2-level flattening
and no parent-comment URN to resolve.

## When to use

- User pastes a Threads post URL and says "reply to this"
- A creator replied to the user and they want to continue the conversation
- User wants to quote-post a take and add value (not a cheap dunk)

## Input

A Threads post URL (`threads.net/@HANDLE/post/CODE` or the threads.com
equivalent), plus the post text (and any conversation context) pasted by the
user, since this bundle has no built-in post reader.

## Output

- 1-3 reply or quote-post drafts, each under 500 chars
- A **reply vs quote post** recommendation with the reason
- A short context summary (who said what)
- An approval card. On approval the draft is returned as a copy-paste block.

## Reply vs quote post

| Use a reply when | Use a quote post when |
|---|---|
| You are adding to the conversation in place | Your addition deserves its own reach |
| You are answering a question or engaging a creator | Your followers should see the original for context |
| You want intimacy over reach | You want reach and a take on your own timeline |

Default to a **reply** for direct engagement and a **quote post** when the user's
point is strong enough to stand as its own post. Never quote-dunk on a small
account; add value or skip it. Keep the tone warm, this is Threads.

## Steps

1. **Parse the URL.** `lib.url_parser.parse_threads_url(url)` returns `handle`,
   `post_id`, `canonical_url`.
2. **Read the context.** Ask the user to paste the target post and the relevant
   conversation above it. If the user is already in the thread, include their
   prior post.
3. **Decide reply vs quote post** using the table above. Recommend one, but let
   the user override.
4. **Draft 1-3 variants** using `references/reply-templates.md`. If the
   counterpart asked a question, answer it plainly with one real detail. If they
   pushed back, concede then sharpen. Keep it warm.
5. **Humanizer pass.** Strip em dashes, AI vocab. Keep each variant under 500
   chars and one hashtag max. One idea per reply.
6. **Approval card.** Show the conversation context, the variants, the
   reply-vs-quote recommendation, and the target URL.
7. **On approval.** Call `lib.publish(kind="reply", draft_text=<approved>,
   target_url=<canonical_url>)` for a reply, or `kind="quote"` for a quote post.
   A reply to another user has no Publora endpoint (`create-post` cannot target
   someone else's post), so `kind="reply"` always returns a copy-paste block. A
   `kind="quote"` could in principle post a new post containing the original URL
   via Publora, but the default is still copy-paste so the user controls the
   embed. Paste it on Threads yourself.

## The no-flattening note

Unlike LinkedIn (which flattens reply threads to 2 levels and needs the top-level
comment URN as the parent), Threads nests replies naturally. There is no
parent-comment URN to compute. A reply is simply a new post you publish while
replying to the target post. This skill therefore does not walk any comment tree;
it just drafts the text and hands it back for you to post as the reply.

## Templates (`references/reply-templates.md`)

- **R1 Answer-Their-Question** - they asked, you answer plainly plus one real detail
- **R2 Concede-Then-Sharpen** - "fair, and the part i would push on is Y"
- **R3 Extend-Their-Point** - take their point one layer deeper with a new framing
- **R4 Share-Lived-Experience** - "we hit this last quarter, here is what broke"
- **R5 Value-Add Quote** - quote post that adds the missing nuance (T4 shape)

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Under 500 chars, one hashtag max. Replies are tighter than posts.
- Never paste a canned "great point!". Respond with content or do not reply.
- Do not hard-sell the user's product in a reply on someone else's post.
  Describe what they do instead.
- Never quote-dunk on a small account. Add value or skip it.
- Keep it warm and conversational. Threads is not the place for a cold X dunk.

## Example

> User: "Reply to this: https://www.threads.net/@somebuilder/post/C8H9abcDEf_"
>
> Skill: parses -> handle somebuilder, post C8H9abcDEf_. Asks the user to paste
> the post. User pastes a take about pricing. Skill recommends a reply (direct
> engagement), drafts an R2 Concede-Then-Sharpen variant and an R3
> Extend-Their-Point variant, each under 500 chars. Shows the approval card.
>
> User: "post the first one"
>
> Skill: returns the copy-paste block with the target URL for the user to post as
> a reply on Threads.

## Files

- `SKILL.md` - this file
- `references/reply-templates.md` - 5 reply/quote templates with examples

## Related skills

- `threads-post-writer` - for a standalone post or a multi-post response
- `threads-humanizer` - scrub the reply before posting
