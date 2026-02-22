#!/usr/bin/env python3
"""
Update Markdown files with keyword front matter using RAKE algorithm.

This script scans all .md files and adds/updates the 'keywords' front matter field
using a Rapid Automatic Keyword Extraction (RAKE) algorithm.

Usage:
    python update_keywords.py

Note: This is a utility for template maintenance. Run on a copy of your files first.
"""

from pathlib import Path
import csv
import re

STOPWORDS = {
    "the",
    "and",
    "of",
    "to",
    "a",
    "in",
    "for",
    "our",
    "your",
    "with",
    "on",
    "by",
    "an",
    "is",
    "this",
    "that",
    "are",
    "be",
    "can",
    "we",
    "us",
    "you",
    "from",
    "or",
    "as",
    "at",
    "it",
    "its",
    "into",
    "these",
    "those",
    "their",
    "your",
    "but",
    "if",
    "they",
    "them",
    "our",
    "so",
    "such",
    "not",
}


def rake_keywords(text: str, limit: int = 6) -> list:
    """Return a list of keywords using a simple RAKE algorithm."""
    text = re.sub(r"[^A-Za-z ]+", " ", text.lower())
    words = text.split()

    phrases = []
    current = []
    for word in words:
        if word in STOPWORDS:
            if current:
                phrases.append(current)
                current = []
        else:
            current.append(word)
    if current:
        phrases.append(current)

    phrases = [p for p in phrases if 0 < len(p) <= 3]

    freq = {}
    degree = {}
    for phrase in phrases:
        degree_val = len(phrase) - 1
        for word in phrase:
            freq[word] = freq.get(word, 0) + 1
            degree[word] = degree.get(word, 0) + degree_val
    for word in freq:
        degree[word] += freq[word]

    word_score = {w: degree[w] / freq[w] for w in freq}

    scores = {}
    for phrase in phrases:
        score = sum(word_score[w] for w in phrase)
        text_phrase = " ".join(phrase)
        scores[text_phrase] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    keywords = []
    for phrase, _ in ranked:
        if phrase not in keywords:
            keywords.append(phrase)
        if len(keywords) >= limit:
            break
    return keywords


def parse_front_matter(lines):
    if not lines or not lines[0].startswith("---"):
        return {}, 0
    end = 1
    fm_lines = []
    for idx in range(1, len(lines)):
        line = lines[idx]
        if line.startswith("---"):
            end = idx + 1
            break
        fm_lines.append(line)
    fm = {}
    for line in fm_lines:
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm, end


def format_front_matter(fm):
    lines = ["---"]
    for key, value in fm.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def update_file(path: Path):
    content = path.read_text().splitlines()
    fm, start_idx = parse_front_matter(content)
    body = content[start_idx:]

    # Skip leading empty lines in body
    while body and not body[0].strip():
        body = body[1:]

    if "title" not in fm:
        for line in body:
            if line.startswith("#"):
                fm["title"] = line.lstrip("#").strip()
                break
    text = "\n".join(body)
    if "title" in fm:
        text = fm["title"] + " " + text
    keywords = rake_keywords(text)
    quoted = ", ".join(f'"{kw}"' for kw in keywords)
    fm["keywords"] = "[" + quoted + "]"
    new_content = format_front_matter(fm) + "\n".join(body)
    # Ensure single newline at end
    new_content = new_content.rstrip("\n") + "\n"
    path.write_text(new_content)


def main():
    md_files = sorted(Path("docs").rglob("*.md"))

    if not md_files:
        print("No markdown files found in docs/")
        return

    print(f"Processing {len(md_files)} markdown files...")

    for p in md_files:
        update_file(p)

    print(f"Updated keywords in {len(md_files)} files.")


if __name__ == "__main__":
    main()
