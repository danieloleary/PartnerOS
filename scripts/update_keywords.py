#!/usr/bin/env python3
"""Update Markdown files with keyword front matter."""

from pathlib import Path
import csv
import re

STOPWORDS = {
    'the', 'and', 'of', 'to', 'a', 'in', 'for', 'our', 'your', 'with', 'on',
    'by', 'an', 'is', 'this', 'that', 'are', 'be', 'can', 'we', 'us', 'you',
    'from', 'or', 'as', 'at', 'it', 'its', 'into', 'these', 'those', 'their',
    'your', 'but', 'if', 'they', 'them', 'our', 'so', 'such', 'not'
}



def rake_keywords(text: str, limit: int = 6) -> list[str]:
    """Return a list of keywords using a simple RAKE algorithm."""
    # Clean and tokenize
    text = re.sub(r"[^A-Za-z ]+", " ", text.lower())
    words = text.split()

    # Build candidate phrases
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

    # limit phrase length
    phrases = [p for p in phrases if 0 < len(p) <= 3]

    # Calculate frequency and degree
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

    # Score phrases
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
    if not lines or not lines[0].startswith('---'):
        return {}, 0
    end = 1
    fm_lines = []
    for idx in range(1, len(lines)):
        line = lines[idx]
        if line.startswith('---'):
            end = idx + 1
            break
        fm_lines.append(line)
    fm = {}
    for line in fm_lines:
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    return fm, end


def format_front_matter(fm):
    lines = ['---']
    for key, value in fm.items():
        lines.append(f"{key}: {value}")
    lines.append('---\n')
    return '\n'.join(lines)


def update_file(path: Path):
    content = path.read_text().splitlines()
    fm, start_idx = parse_front_matter(content)
    body = content[start_idx:]
    if 'title' not in fm:
        # use first heading as title
        for line in body:
            if line.startswith('#'):
                fm['title'] = line.lstrip('#').strip()
                break
    text = '\n'.join(body)
    if 'title' in fm:
        text = fm['title'] + ' ' + text
    keywords = rake_keywords(text)
    quoted = ', '.join(f'"{kw}"' for kw in keywords)
    fm['keywords'] = '[' + quoted + ']'
    new_content = format_front_matter(fm) + '\n'.join(body)
    # ensure trailing newline
    if not new_content.endswith('\n'):
        new_content += '\n'
    path.write_text(new_content)


def main():
    md_files = sorted(Path('.').rglob('*.md'))
    # record inventory
    with open('markdown_inventory.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for p in md_files:
            writer.writerow([str(p)])

    for p in md_files:
        update_file(p)

    # compute word counts for analysis
    lengths = []
    for p in md_files:
        text = p.read_text()
        word_count = len(re.findall(r"\w+", text))
        lengths.append((word_count, p))
    lengths.sort()
    print("Shortest files:")
    for count, p in lengths[:4]:
        print(count, p)


if __name__ == '__main__':
    main()
