---
name: linkedin
description: Post to LinkedIn, manage content. Use when user wants to create LinkedIn posts, schedule content, or manage their LinkedIn presence. Authenticated as Hesham Saied.
---

# LinkedIn

Post and manage LinkedIn content via the LinkedIn API.

## Script

`scripts/linkedin.py` — CLI for LinkedIn operations.

Commands:
- `linkedin.py status` — Check auth status
- `linkedin.py post --text "Your post"` — Publish a post
- `linkedin.py post --file post.txt` — Post from file
- `linkedin.py me` — Show profile info
- `linkedin.py auth --client-id X --client-secret Y` — Re-authenticate

## Posting Best Practices

- Keep posts 1200-1500 chars for best engagement
- Use line breaks for readability
- Start with a hook (first 2 lines show in feed)
- End with a question or CTA
- Use 3-5 relevant hashtags at the end
- Best times for Dubai: 8-9am, 12-1pm, 5-6pm (Sun-Thu)

## Workflow

1. User describes topic or asks for a post
2. Draft the post in LinkedIn style (hook → value → CTA → hashtags)
3. Show draft for approval
4. Post via `linkedin.py post --text "..."`
5. Confirm posted

Always confirm before posting. Never post without approval.
