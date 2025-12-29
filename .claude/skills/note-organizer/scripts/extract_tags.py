#!/usr/bin/env python3
"""Extract and analyze tags from text content.

Usage:
    python extract_tags.py < input.txt
    cat file.md | python extract_tags.py
    echo "[decision] text [action] more" | python extract_tags.py
"""

import re
import sys
from collections import Counter

def extract_tags(text):
    """Extract all [tag] patterns from text."""
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, text)

    # Filter out PII tags (they have /PII: in them)
    tags = [tag for tag in matches if not tag.startswith('PII:') and not tag.startswith('/PII:')]

    return tags

def categorize_tag(tag):
    """Categorize tag by type."""
    tag_lower = tag.lower()

    # Document state
    if tag_lower in ['raw', 'prompt', 'organized', 'session-log']:
        return 'state'

    # Content
    if tag_lower.startswith('decision'):
        return 'decision'
    if tag_lower.startswith('action'):
        return 'action'
    if tag_lower.startswith('question'):
        return 'question'
    if tag_lower in ['insight', 'pattern']:
        return 'insight'
    if tag_lower in ['reference', 'link']:
        return 'reference'
    if tag_lower in ['blocker', 'risk', 'issue', 'bug']:
        return 'problem'

    # Priority
    if tag_lower in ['urgent', 'high', 'medium', 'low']:
        return 'priority'

    # Project
    if tag_lower.startswith('project:') or tag_lower.startswith('category:'):
        return 'project'

    # Unknown/custom
    return 'custom'

def main():
    # Read from stdin
    text = sys.stdin.read()

    # Extract tags
    tags = extract_tags(text)

    if not tags:
        print("No tags found")
        return

    # Count occurrences
    tag_counts = Counter(tags)

    # Categorize
    categorized = {}
    for tag in tag_counts.keys():
        category = categorize_tag(tag)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append((tag, tag_counts[tag]))

    # Display results
    print(f"Total tags found: {len(tags)} ({len(tag_counts)} unique)\n")

    # Sort categories for consistent output
    category_order = ['state', 'decision', 'action', 'question', 'insight',
                      'reference', 'problem', 'priority', 'project', 'custom']

    for category in category_order:
        if category in categorized:
            print(f"{category.upper()}:")
            for tag, count in sorted(categorized[category]):
                if count > 1:
                    print(f"  - [{tag}] ({count}x)")
                else:
                    print(f"  - [{tag}]")
            print()

if __name__ == "__main__":
    main()
