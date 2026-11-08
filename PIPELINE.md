# Production Pipeline

The one approved way to make an episode (HARD RULE D5). If the pipeline changes,
update this file in the same commit and get the owner's OK first.

## Toolchain (default)
- **Python 3** — scene code, frame generation (Pillow, NumPy; SVG via your own
  renderer or `cairosvg` if installed).
- **FFmpeg** — encoding, audio mixing, loudness normalisation, captions burn-in
  check, frame extraction for QA.
- **Node 22** available if a JS/HTML-based renderer is chosen later (e.g. Remotion).
  Not used by default.

> The first episode that needs a renderer should create it in `pipeline/` (shared
> code: characters as reusable drawing functions/rigs, easing, camera, scene
> composer). Episodes only contain scene scripts that call shared code — this keeps
> Molka identical across episodes.

## Folder layout per episode
```
episodes/S01S01-molka-meets-a-snail/
├── episode.md        # script, shot list, audio credits (from template)
├── upload.md         # YouTube upload details (from template)
├── scenes/           # scene scripts for this episode
├── assets/           # episode-only assets
└── render/
    ├── preview.mp4   # low-res check (git-ignored)
    ├── final.mp4     # final export (git-ignored unless LFS)
    ├── thumbnail.png
    └── captions.srt
```

## Render steps
1. Generate frames for the preview at 50 % resolution, 15 fps → `render/preview.mp4`.
2. Extract QA frames: `ffmpeg -i render/preview.mp4 -vf "select='eq(n\,0)+...'"` or
   sample at 0/25/50/75/100 % with `-ss`. Look at them with the Read tool.
3. Fix issues, then render final frames at full resolution, 30 fps.
4. Mix audio, normalise: `-af loudnorm=I=-14:TP=-1:LRA=11`.
5. Encode:
   `ffmpeg -framerate 30 -i frames/%05d.png -i audio.wav -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -shortest render/final.mp4`
6. Verify with `ffprobe` (resolution, fps, duration, audio stream present).
7. Delete temporary frame folders (they are git-ignored, but keep the disk clean).

## Large files
`*.mp4`, `*.mov`, `*.wav` and `frames/` are git-ignored by default (HARD RULE F3).
To version final videos, the owner can enable Git LFS:
`git lfs install && git lfs track "episodes/**/render/final.mp4"` — then remove the
mp4 line from `.gitignore` in the same commit.

## Known issues
_Record pipeline problems and their fixes here._
