# Molka's Adventures 🐾

Animated series about the life of Molka the puppy, made with Claude Code for YouTube.

## How to make a new episode
Open this repo in Claude Code and paste the prompt from
[`prompts/NEW_EPISODE.md`](prompts/NEW_EPISODE.md). Claude reads `CLAUDE.md`
automatically and follows `HARD_RULES.md`.

## Before the first episode
Fill in every **TO CONFIRM** field in [`bible/SERIES_BIBLE.md`](bible/SERIES_BIBLE.md)
— above all Molka's look (breed, colours, eyes, collar) and the audience setting.

## Layout
```
CLAUDE.md                 Operating prompt for Claude Code (auto-loaded)
HARD_RULES.md             Non-negotiable rules
PIPELINE.md               How video is built and rendered
EPISODE_LOG.md            Every episode ever made + next free code
bible/SERIES_BIBLE.md     Characters, world, style, audience
templates/                episode.md and upload.md templates
prompts/NEW_EPISODE.md    Copy/paste prompts for new episodes
scripts/check_upload.py   Validates YouTube upload details
scripts/build_brand.py    Draws Molka + channel art (avatar, banner, watermark)
channel/                  Channel description, settings, bios + brand/ images
pipeline/                 Shared rendering code (created with the first episode)
assets/                   Shared characters, backgrounds, fonts, audio + LICENSES.md
episodes/<CODE>-<slug>/   One folder per episode
```
