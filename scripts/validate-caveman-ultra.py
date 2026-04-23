#!/usr/bin/env python3
"""Heuristic checker for caveman ultra style drift.

Flags common regressions:
- conversational openers
- filler/connective words
- long sentence chains
- high average words per sentence
- missing fragment/pattern style
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BANNED_PHRASES = [
    "got it",
    "understood",
    "perfecto",
    "genial",
    "correcto",
    "entiendo",
    "claro",
    "por supuesto",
    "voy a",
    "ya tengo",
    "he ",
    "i will",
    "i'll",
    "we will",
    "we'll",
    "done",
    "fixed",
    "great",
    "good news",
    "luego",
    "entonces",
    "además",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w/-]+\b", text, flags=re.UNICODE))


def analyze(text: str) -> list[str]:
    issues: list[str] = []
    compact = normalize(text)
    lower = compact.lower()
    sentences = split_sentences(text)

    if not compact:
        issues.append("empty text")
        return issues

    for phrase in BANNED_PHRASES:
        if phrase in lower:
            issues.append(f"contains filler/connective: {phrase!r}")

    if len(sentences) > 5:
        issues.append(f"too many sentences/lines: {len(sentences)} > 5")

    long_sentences = [s for s in sentences if word_count(s) > 10]
    if long_sentences:
        issues.append(
            f"contains long sentence(s): {len(long_sentences)} over 10 words"
        )

    avg_words = sum(word_count(s) for s in sentences) / max(len(sentences), 1)
    if avg_words > 8:
        issues.append(f"average words per sentence too high: {avg_words:.1f} > 8")

    if "," in text and "->" not in text:
        issues.append("comma-heavy prose without terse separator like '->'")

    if len(sentences) >= 2:
        short_count = sum(1 for s in sentences if word_count(s) <= 7)
        if short_count < len(sentences) / 2:
            issues.append("too few short fragment-style lines")

    starts = [s.split()[0].lower() for s in sentences if s.split()]
    if any(token in {"i", "yo", "we", "nosotros"} for token in starts):
        issues.append("starts like narrative prose, not terse state/update")

    if re.search(r"\b(es|está|estoy|son|fue|eran)\b.+\bporque\b", lower):
        issues.append("explanatory prose chain detected")

    if len(sentences) >= 4 and lower.count(".") >= 3 and "->" not in text:
        issues.append("too many prose sentences without terse separators")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text to validate")
    group.add_argument("--file", help="File containing text to validate")
    args = parser.parse_args()

    text = args.text if args.text is not None else Path(args.file).read_text(encoding="utf-8")
    issues = analyze(text)

    if issues:
        print("FAIL caveman-ultra")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("PASS caveman-ultra")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
