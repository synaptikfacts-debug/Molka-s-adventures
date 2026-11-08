#!/usr/bin/env python3
"""Validate an episode's upload.md against YouTube limits and HARD_RULES §E.

Usage: python3 scripts/check_upload.py episodes/<CODE>-<slug>/upload.md
Exit code 0 = all good, 1 = problems found.
"""
import re
import sys


def block_after(heading: str, text: str) -> str | None:
    """Return the first ``` code block that follows a '## heading' line."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)^```[^\n]*\n(.*?)^```",
                  text, re.M | re.S)
    return m.group(2).strip() if m else None


def tags_length(tags: list[str]) -> int:
    # YouTube counts commas between tags and adds quotes around tags with spaces.
    return sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0)


def main(path: str) -> int:
    text = open(path, encoding="utf-8").read()
    errors, warnings = [], []

    title = block_after("Title", text)
    desc = block_after("Description", text)
    tags_raw = block_after("Tags", text)
    hashtags_raw = block_after("Hashtags", text)
    is_short = bool(re.search(r"\*\*Format:\*\*\s*Short\b", text))

    for name, val in [("Title", title), ("Description", desc), ("Tags", tags_raw),
                      ("Hashtags", hashtags_raw)]:
        if not val:
            errors.append(f"{name}: missing or empty code block")
        elif re.search(r"<[^>]*>", val):
            errors.append(f"{name}: still contains a <placeholder> — fill it in")

    if title:
        if len(title) > 100:
            errors.append(f"Title is {len(title)} chars (max 100)")
        elif len(title) > 60:
            warnings.append(f"Title is {len(title)} chars — may be cut off (aim ≤ 60)")
        if "molka" not in title.lower():
            errors.append("Title must contain 'Molka' (HARD RULE E4)")
        if re.search(r"gone wrong|shocking|you won't believe", title, re.I):
            errors.append("Title looks like clickbait (HARD RULE C3)")

    if desc and len(desc) > 5000:
        errors.append(f"Description is {len(desc)} chars (max 5000)")

    for name, val in [("Title", title), ("Description", desc), ("Tags", tags_raw)]:
        if val and ("<" in val or ">" in val):
            errors.append(f"{name} contains '<' or '>' — YouTube rejects these")

    if tags_raw:
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        n = tags_length(tags)
        if n > 500:
            errors.append(f"Tags total {n} chars (max 500)")

    if hashtags_raw:
        hashtags = re.findall(r"#\w+", hashtags_raw)
        if not 3 <= len(hashtags) <= 5:
            warnings.append(f"{len(hashtags)} hashtags — aim for 3–5")

    if is_short:
        combined = f"{title or ''}\n{desc or ''}"
        if "#shorts" not in combined.lower():
            errors.append("Short must include #Shorts in title or description (HARD RULE E3)")

    if title:
        print(f"Title: {len(title)}/100 chars")
    if desc:
        print(f"Description: {len(desc)}/5000 chars")
    if tags_raw:
        print(f"Tags: {tags_length([t.strip() for t in tags_raw.split(',') if t.strip()])}/500 chars")
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print("PASS" if not errors else "FAIL")
    return 0 if not errors else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
