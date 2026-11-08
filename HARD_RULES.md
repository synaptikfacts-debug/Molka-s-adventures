# HARD RULES — Molka's Adventures

These rules are **non-negotiable**. They override `CLAUDE.md`, templates and any
instruction in a chat message. The only exception is when the channel owner writes
explicitly: **"override hard rule <ID>"** — and then only for that one run.

If following a request would break a rule, stop, say which rule, and offer the
closest version that complies.

---

## A. Character & canon
- **A1.** Molka's design is locked by `bible/SERIES_BIBLE.md`. Never change her
  breed, colours, markings, proportions, pigtails/bow colours, eye colour or voice.
- **A2.** Never invent Molka's appearance. If a design field in the bible says
  `TO CONFIRM`, stop and ask the owner before the first render that needs it.
- **A3.** Molka is always kind, curious and brave. She is never cruel, never hurt
  badly, never killed, never in real danger that is left unresolved.
- **A4.** Anything that becomes canon (new character, place, item, catchphrase) is
  added to the bible in the same commit as the episode that introduced it.
- **A5.** Episode numbers are never reused or skipped. Take the next free code from
  `EPISODE_LOG.md`.

## B. Copyright & originality
- **B1.** No copyrighted characters, logos, brands, songs, film/TV references or
  look-alikes of existing cartoon characters — not even in the background.
- **B2.** Music and sound effects must be original (generated in the pipeline) or
  from a royalty-free source whose licence allows YouTube monetisation. Record source
  + licence for every audio file in `episode.md`.
- **B3.** No fonts, images or assets without a licence that allows commercial use.
  Record the licence in `assets/LICENSES.md`.
- **B4.** No real, identifiable people.

## C. Kid & platform safety
- **C1.** Content must suit young children: no violence, scary imagery, bad language,
  dangerous stunts kids could copy, unhealthy food for pets, or mean-spirited jokes.
- **C2.** Never show real-world dangers for dogs as safe (chocolate, grapes,
  onions, roads without supervision, etc.). If a hazard appears, the story treats it
  correctly.
- **C3.** No misleading titles or thumbnails. The title and thumbnail must show what
  actually happens in the video. No clickbait phrases like "GONE WRONG" or "SHOCKING".
- **C4.** The audience setting in every `upload.md` follows the bible's
  **Audience** field. Never change it on your own.
- **C5.** No calls to action that ask children to comment, share personal info or
  leave YouTube.

## D. Technical output
- **D1.** Shorts: 1080×1920, 9:16, 30 fps, ≤ 60 s unless the owner asks for longer
  (YouTube allows up to 3 min). Long: 1920×1080, 16:9, 30 fps.
- **D2.** Export H.264 (yuv420p) + AAC 48 kHz, loudness ≈ −14 LUFS, peak ≤ −1 dBTP.
- **D3.** Always render a low-res preview and inspect frames before the final render.
- **D4.** Every video ships with `final.mp4`, `thumbnail.png`, `captions.srt`,
  `episode.md` and `upload.md`. Missing one = not finished.
- **D5.** Use only the pipeline in `PIPELINE.md`. Changing tools requires the owner's
  OK and an update to `PIPELINE.md` in the same commit.

## E. Upload details
- **E1.** Every finished video ends with a filled `upload.md` pasted in full into the
  final message — title, description, tags, hashtags and every setting field.
- **E2.** Limits (enforced by `scripts/check_upload.py`): title ≤ 100 characters
  (aim ≤ 60 so it isn't cut off), description ≤ 5,000 characters, tags ≤ 500
  characters in total, 3–5 hashtags, no `<` or `>` characters anywhere.
- **E3.** Shorts include `#Shorts` in the title or description.
- **E4.** Titles always contain "Molka". Descriptions always start with a one-line
  hook, then the story summary, then the series line and credits.
- **E5.** Never claim views, awards or facts that aren't true.

## F. Repository
- **F1.** The repo is the single source of truth. At the end of every run, the
  repo must contain everything needed to re-render the episode.
- **F2.** After each finished episode: update `EPISODE_LOG.md` → `git add` →
  commit with message `<CODE>: <Title>` (+ short body) → `git push`. Report the
  commit SHA. A run is not finished until the push succeeds.
- **F3.** Never commit files over 50 MB. `final.mp4` and other large renders are
  git-ignored unless Git LFS is set up (see `PIPELINE.md`). `upload.md`,
  `episode.md`, `captions.srt` and `thumbnail.png` are always committed.
- **F4.** Never force-push, rewrite history, delete episodes or delete another
  episode's files without the owner's explicit request.
- **F5.** Never commit secrets, API keys, tokens or personal data.
- **F6.** Keep the folder layout in `README.md`. Don't create files outside it.
