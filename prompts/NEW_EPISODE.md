# Prompt to paste into Claude Code

Copy everything in the box, replace the `<…>` parts, and paste it into a new Claude
Code session opened on this repository.

```
You are producing a new episode of "Molka's Adventures" for YouTube.

1. Read CLAUDE.md, HARD_RULES.md, bible/SERIES_BIBLE.md, PIPELINE.md and
   EPISODE_LOG.md before doing anything. HARD_RULES.md wins over everything.
2. Make this:
   - Format: <Short | Long>
   - Idea: <one or two sentences, e.g. "Molka finds a snail in the garden and
     tries to make friends with it">
   - Length: <e.g. 45 seconds | 5 minutes>  (optional)
   - Anything special: <new character, season theme, holiday…>  (optional)
3. Follow the workflow in CLAUDE.md phases 0–6 in order, with a task list.
   Make sensible creative choices yourself and state them in one line; only stop
   to ask if a bible field is TO CONFIRM or a choice breaks a hard rule.
4. Render a preview, inspect frames, fix, then render the final.
5. Run every QA check and scripts/check_upload.py until all pass.
6. Update EPISODE_LOG.md (and the bible if anything new became canon),
   commit as "<CODE>: <Title>" and push. Report the commit SHA.
7. End with the final message format from CLAUDE.md §3, including the full
   upload.md — title, description, tags, hashtags and settings — each in its own
   code block so I can copy/paste them into YouTube Studio.
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
