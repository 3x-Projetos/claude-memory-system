#!/usr/bin/env python3
"""
PII Redaction Script for Claude Memory System

Reads global-memory.md and generates:
1. global-memory.safe.md (full, PII redacted)
2. global-memory.quick.md (condensed, safe for frequent use)

Usage:
    python redact-pii.py [input_file] [output_file]

    Default:
    input  = ~/.claude-memory/global-memory.md
    output = ~/.claude-memory/global-memory.safe.md
    quick  = ~/.claude-memory/global-memory.quick.md (auto-generated)

Markers format:
    Input:  [PII:TYPE]value[/PII:TYPE]
    Output: [REDACTED:TYPE]

Supported PII types:
    NAME, EMAIL, LOCATION, COMPANY, PROJECT,
    CREDENTIAL, API, DOCUMENT

M010.1 Update: Now generates quick version for fast startup
"""

import re
import sys
from pathlib import Path
from datetime import datetime


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


def generate_quick_memory(safe_content):
    """
    Generate condensed quick-start memory from safe content.

    Args:
        safe_content (str): Full safe memory content

    Returns:
        str: Condensed quick memory (~50 lines)
    """
    lines = safe_content.split('\n')

    # Extract key sections
    quick_lines = []
    quick_lines.append("# Global Memory - Quick Profile")
    quick_lines.append(f"**Última atualização**: {datetime.now().strftime('%Y-%m-%d')}")
    quick_lines.append("**Versão**: 1.1 (quick - M010.1)")
    quick_lines.append("")
    quick_lines.append("---")
    quick_lines.append("")

    # Parse sections we want in quick version
    in_section = None
    section_lines = []
    include_sections = {
        '## User Profile': 'essentials',
        '## Collaboration Patterns': 'workflow',
        '## Projects Context': 'projects'
    }

    for line in lines:
        # Check if entering a section we care about
        for section_header in include_sections:
            if line.startswith(section_header):
                if in_section:
                    # Process previous section
                    quick_lines.extend(process_section_for_quick(in_section, section_lines))
                in_section = include_sections[section_header]
                section_lines = [line]
                break
        else:
            if in_section:
                section_lines.append(line)
                # Check if leaving section
                if line.startswith('## ') and line not in include_sections:
                    quick_lines.extend(process_section_for_quick(in_section, section_lines))
                    in_section = None
                    section_lines = []

    # Process last section if any
    if in_section and section_lines:
        quick_lines.extend(process_section_for_quick(in_section, section_lines))

    # Add footer
    quick_lines.append("")
    quick_lines.append("---")
    quick_lines.append("")
    quick_lines.append("*Versão resumida para inicialização rápida (~50 linhas vs ~165 linhas completas)*")
    quick_lines.append("*Use `global-memory.safe.md` para contexto completo quando necessário*")

    return '\n'.join(quick_lines)


def process_section_for_quick(section_type, lines):
    """Extract essential info from section for quick version."""
    result = []

    if section_type == 'essentials':
        # User Profile essentials
        result.append("## User Profile (Essentials)")
        result.append("")
        # Extract just the key points
        for line in lines:
            if line.startswith('**Working Style'):
                result.append(line)
            elif line.startswith('**Language'):
                result.append(line)
                result.append("")
            elif line.startswith('**Tech Stack') or line.startswith('**Technical Preferences'):
                result.append("**Tech Stack**: Python, Git, Obsidian, Claude CLI")
                result.append("")
                break
        result.append("---")
        result.append("")

    elif section_type == 'workflow':
        # Collaboration essentials
        result.append("## Collaboration Patterns")
        result.append("")
        result.append("**Expectations**: Proatividade, detalhes técnicos, context awareness, privacidade")
        result.append("**Workflow**: Planejamento → Validação → Documentação → Versionamento")
        result.append("")
        result.append("---")
        result.append("")

    elif section_type == 'projects':
        # Active projects (top 3)
        result.append("## Active Projects (Top 3)")
        result.append("")
        project_count = 0
        in_project = False
        for line in lines:
            if line.startswith('### ') and 'Current Project' not in line:
                in_project = True
                project_count += 1
                if project_count <= 3:
                    # Extract project name and status
                    result.append(line.replace('### ', ''))
                else:
                    break
            elif in_project and project_count <= 3:
                if line.startswith('**Status'):
                    result.append(line)
                    result.append("")
                    in_project = False
        result.append("---")
        result.append("")

    return result


def get_default_paths():
    """Get default input/output paths."""
    home = Path.home()
    input_path = home / '.claude-memory' / 'global-memory.md'
    output_path = home / '.claude-memory' / 'global-memory.safe.md'
    quick_path = home / '.claude-memory' / 'global-memory.quick.md'
    return input_path, output_path, quick_path


def main():
    # Parse arguments or use defaults
    if len(sys.argv) >= 3:
        input_path = Path(sys.argv[1])
        output_path = Path(sys.argv[2])
        quick_path = input_path.parent / f"{input_path.stem}.quick{input_path.suffix}"
    elif len(sys.argv) == 2:
        input_path = Path(sys.argv[1])
        output_path = input_path.parent / f"{input_path.stem}.safe{input_path.suffix}"
        quick_path = input_path.parent / f"{input_path.stem}.quick{input_path.suffix}"
    else:
        input_path, output_path, quick_path = get_default_paths()

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

    # Generate quick version
    quick_content = generate_quick_memory(redacted_content)

    # Write safe output
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(redacted_content)
    except Exception as e:
        print(f"Error writing safe output file: {e}", file=sys.stderr)
        sys.exit(1)

    # Write quick output
    try:
        with open(quick_path, 'w', encoding='utf-8') as f:
            f.write(quick_content)
    except Exception as e:
        print(f"Error writing quick output file: {e}", file=sys.stderr)
        sys.exit(1)

    # Success
    print(f"[OK] PII redacted: {input_path} -> {output_path}")
    print(f"[OK] Quick memory: {input_path} -> {quick_path}")

    # Stats (optional)
    original_pii = len(re.findall(r'\[PII:\w+\]', content))
    redacted_pii = len(re.findall(r'\[REDACTED:\w+\]', redacted_content))

    if original_pii > 0:
        print(f"  Redacted {original_pii} PII markers")
    else:
        print(f"  No PII markers found")

    # Quick version stats
    safe_lines = len(redacted_content.split('\n'))
    quick_lines = len(quick_content.split('\n'))
    economy_pct = int((1 - quick_lines / safe_lines) * 100) if safe_lines > 0 else 0
    print(f"  Quick version: {quick_lines} lines (vs {safe_lines} in full) - {economy_pct}% shorter")


if __name__ == '__main__':
    main()
