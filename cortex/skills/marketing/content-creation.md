---
name: marketing-content
title: Marketing Content Agent
description: Plans, writes, and schedules content across all your platforms. Takes one idea and outputs LinkedIn posts, X threads, newsletters, YouTube scripts.
tags: [marketing, content, social, repurposing]
triggers:
  - User asks to create content
  - User wants social media posts
  - User mentions "post ideas" or "content calendar"
---

# Marketing Content Agent

Creates platform-optimized content from any seed idea.

## What It Does

- Researches supporting data for your topic
- Writes in your brand voice (learned from past posts)
- Outputs: X thread, LinkedIn post, newsletter, YouTube script
- Each format optimized for that platform's algorithm
- Generates hashtags, hooks, and CTA variants

## Output

`/output/content-[topic]-[date]/` — 5-7 platform formats + image prompt.

## How to Run

```bash
/skill marketing-content
# or
hermes -s marketing-content -q "Create content for: [topic]"
```

## Example

Input: "AI agents replacing employees"

Output:
- `x-thread.md` — 8-tweet thread with hooks
- `linkedin-post.md` — Native LinkedIn longform
- `newsletter.md` — Newsletter version
- `youtube-script.md` — Short-form video script
- `image-prompt.txt` — For generative visuals