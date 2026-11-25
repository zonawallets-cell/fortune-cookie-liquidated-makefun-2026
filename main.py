"""Fortune Cookie for the Liquidated Trader — make.fun entry.

Writes one fortune cookie line (at most 20 words, at most 160
characters): a fortune for a crypto trader who has just been
liquidated, to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Pure standard library only.

Why this line: it opens in the classic oracular fortune voice — "A
windfall is coming, trader" — names the loss plainly ("your liquidated
position"), and then the punchline breaks the formality with the
mundane: the windfall is exactly enough to buy this cookie. The
surprise is the last word, the cookie itself, not the obvious
liquidation pun; rueful and warm, the trader laughs with the cookie.
"""

import os

LINE = (
    "A windfall is coming, trader: your liquidated position has freed "
    "up exactly enough to buy this cookie."
)

MAX_CHARS = 160
MAX_WORDS = 20


def validate(text):
    """Enforce the RULES.txt gate and the judge brief's word cap,
    and reject control characters."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 160-char limit" % len(text))
    if len(text.split()) > MAX_WORDS:
        raise ValueError(
            "entry is %d words, over the 20-word limit" % len(text.split())
        )
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(LINE)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("chars: %d, words: %d" % (len(entry), len(entry.split())))


if __name__ == "__main__":
    main()
