#!/usr/bin/env python3
"""
PII Redaction Script for Claude Memory System

Reads global-memory.md and replaces PII markers with redacted versions
for safe transmission to AI systems.

Usage:
    python redact-pii.py [input_file] [output_file]

    Default:
    input  = ~/.claude-memory/global-memory.md
    output = ~/.claude-memory/global-memory.safe.md

Markers format:
    Input:  [PII:TYPE]value[/PII:TYPE]
    Output: [REDACTED:TYPE]

Supported PII types:
    NAME, EMAIL, LOCATION, COMPANY, PROJECT,
    CREDENTIAL, API, DOCUMENT
"""

import re
import sys
from pathlib import Path


def redact_pii(content):
    """
    Replace all PII markers with redacted versions.

    Args:
        content (str): Original content with PII markers

    Returns:
        str: Content with PII redacted
    """
    # Pattern: [PII:TYPE]value[/PII:TYPE] -> [REDACTED:TYPE]
    pattern = r'\[PII:(\w+)\](.*?)\[/PII:\1\]'

    def replace_match(match):
        pii_type = match.group(1)
        # Original value is in match.group(2) but we discard it
        return f'[REDACTED:{pii_type}]'

    return re.sub(pattern, replace_match, content, flags=re.DOTALL)


def get_default_paths():
    """Get default input/output paths."""
    home = Path.home()
    input_path = home / '.claude-memory' / 'global-memory.md'
    output_path = home / '.claude-memory' / 'global-memory.safe.md'
    return input_path, output_path


def main():
    # Parse arguments or use defaults
    if len(sys.argv) >= 3:
        input_path = Path(sys.argv[1])
        output_path = Path(sys.argv[2])
    elif len(sys.argv) == 2:
        input_path = Path(sys.argv[1])
        output_path = input_path.parent / f"{input_path.stem}.safe{input_path.suffix}"
    else:
        input_path, output_path = get_default_paths()

    # Validate input exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Read input
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Redact PII
    redacted_content = redact_pii(content)

    # Write output
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(redacted_content)
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

    # Success
    print(f"[OK] PII redacted: {input_path} -> {output_path}")

    # Stats (optional)
    original_pii = len(re.findall(r'\[PII:\w+\]', content))
    redacted_pii = len(re.findall(r'\[REDACTED:\w+\]', redacted_content))

    if original_pii > 0:
        print(f"  Redacted {original_pii} PII markers")
    else:
        print(f"  No PII markers found")


if __name__ == '__main__':
    main()
