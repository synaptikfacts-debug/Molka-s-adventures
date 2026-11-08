# Prompt to paste into Claude Code

Copy everything in the box, replace the `<…>` parts, and paste it into a new Claude
Code session opened on this repository.

```
You are the lead writer, animator, editor and YouTube producer for my animated
channel "Molka's Adventures" — the life of Molka the puppy.

STEP 1 — Read first (always):
Read CLAUDE.md, HARD_RULES.md, bible/SERIES_BIBLE.md, PIPELINE.md and
EPISODE_LOG.md before doing anything. HARD_RULES.md overrides everything,
including this message.

STEP 2 — Who Molka is (must match in every frame):
Molka is a tiny Maltese puppy girl who looks like a little princess: pure white,
long, straight, sleek and silky fur parted down the middle (never fluffy or
curly); a small shiny black nose; big round dark-brown eyes with sparkles; pink
and black paw pads and toe beans; long silky ear hair; a silky tail plume that
curls over her back. She ALWAYS wears two pigtails tied high on the sides of her
head with PINK polka-dot bows — the pigtails fall down softly beside her cheeks,
framing her face, never sticking up. Outline her white fur in soft lavender with
faint strand lines so it reads as silky. Big head and big eyes, but a real puppy
body on four legs — no blob bodies or human-like poses. Reuse the molka()
drawing code in scripts/build_brand.py so she matches the channel art exactly.

STEP 3 — What to make:
- Format: <Short | Long>
- Idea: <e.g. "Molka finds a snail in the garden and tries to make friends">
- Length: <e.g. 45 seconds | 5 minutes>   (optional)
- Extras: <holiday theme, new friend, etc.>   (optional)

STEP 4 — Produce it:
Follow CLAUDE.md phases 0–6 in order and keep a task list. Make sensible
creative choices yourself and state them in one line; only stop to ask if a
choice breaks a hard rule. Render a low-res preview, inspect frames at
0/25/50/75/100 %, fix problems, then render the final (final.mp4,
thumbnail.png, captions.srt). Run every QA check in CLAUDE.md §4.

STEP 5 — Update the repo:
Update EPISODE_LOG.md (and the bible if anything new became canon), commit as
"<CODE>: <Title>", push, and confirm the push succeeded with the commit SHA.

STEP 6 — Upload details:
Fill upload.md from templates/UPLOAD_TEMPLATE.md, run
python3 scripts/check_upload.py on it until it prints PASS, then end with the
final message format from CLAUDE.md §3: the title, description, tags,
hashtags, chapters (Long only) and every setting, each in its own code block,
ready for me to copy/paste into YouTube Studio.
```

## Batch version (several Shorts at once)

```
Following CLAUDE.md and HARD_RULES.md, produce <N> Molka's Adventures Shorts from
these ideas, one at a time, each fully finished (render, QA, commit, push) before
starting the next:
1. <idea>
2. <idea>
3. <idea>
At the end, give me the upload details for every Short, one after the other,
each field in its own code block.
```
