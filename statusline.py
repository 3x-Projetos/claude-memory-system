#!/usr/bin/env python3
"""
Claude Code Status Line with Context Window & Token Tracking
Shows real-time context usage, tokens, cost, model, and git branch
"""

import json
import sys
import os
import subprocess
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_git_branch():
    """Get current git branch if in a git repo"""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            check=False,
            timeout=1
        )
        if result.returncode == 0 and result.stdout.strip():
            return f" | GIT:{result.stdout.strip()}"
    except:
        pass
    return ""

def format_tokens(num):
    """Format token count for display (k for thousands)"""
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)

def get_context_bar(percent):
    """Create a visual progress bar for context usage"""
    bar_length = 10
    filled = int(bar_length * percent / 100)
    
    # Use simple ASCII characters for Windows compatibility
    bar = '=' * filled + '-' * (bar_length - filled)
    
    # Color based on usage
    if percent >= 80:
        indicator = '!'  # Critical
    elif percent >= 60:
        indicator = '*'  # Warning
    else:
        indicator = ' '  # OK
    
    return f"[{bar}]{indicator}"

def main():
    try:
        # Debug: Log that script was called
        with open(os.path.expanduser('~/.claude/statusline-debug.log'), 'a', encoding='utf-8') as f:
            import datetime
            f.write(f"Script called at {datetime.datetime.now()}\n")

        # Read JSON input from stdin
        data = json.load(sys.stdin)
        
        # Extract data
        model = data.get('model', {}).get('display_name', 'Unknown')
        current_dir = os.path.basename(data.get('workspace', {}).get('current_dir', ''))
        
        # Cost tracking
        cost = data.get('cost', {})
        total_cost = cost.get('total_cost_usd', 0)
        
        # Context window tracking
        ctx = data.get('context_window', {})
        ctx_size = ctx.get('context_window_size', 200000)
        total_input = ctx.get('total_input_tokens', 0)
        total_output = ctx.get('total_output_tokens', 0)
        
        # Current usage (from latest API call)
        current_usage = ctx.get('current_usage')
        
        if current_usage:
            # Calculate actual context usage
            input_tok = current_usage.get('input_tokens', 0)
            cache_create = current_usage.get('cache_creation_input_tokens', 0)
            cache_read = current_usage.get('cache_read_input_tokens', 0)
            
            # Total tokens in current context
            current_tokens = input_tok + cache_create + cache_read
            percent_used = int((current_tokens / ctx_size) * 100)
            
            # Context bar
            ctx_bar = get_context_bar(percent_used)
            ctx_display = f"CTX:{ctx_bar}{percent_used}%"
        else:
            ctx_display = "CTX:[----------] 0%"
        
        # Token tracking
        total_tokens = total_input + total_output
        tokens_display = f"TOK:{format_tokens(total_tokens)}(I:{format_tokens(total_input)}/O:{format_tokens(total_output)})"
        
        # Cost display
        cost_display = f"${total_cost:.3f}" if total_cost > 0 else "$0.000"
        
        # Git branch
        git_branch = get_git_branch()
        
        # Build status line (compact, ASCII-safe)
        status = f"[{model}] {ctx_display} | {tokens_display} | COST:{cost_display} | DIR:{current_dir}{git_branch}"
        
        print(status)
        
    except Exception as e:
        # Fallback on error
        print(f"[Claude] Error: {str(e)}")

if __name__ == "__main__":
    main()
