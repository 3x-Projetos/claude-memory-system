#!/usr/bin/env python3
"""
Orchestrator Model Selection UI
Implements "Star & Stat" pattern for Claude model selection
Based on AGENT-INTERFACE-STANDARD.md v4.0
"""

from dataclasses import dataclass
from typing import Literal, Optional
import json

@dataclass
class ModelOption:
    """Model specification with cost/speed/quality trade-offs"""
    key: str
    name: str
    capabilities: str
    cost_input: float  # per 1M tokens
    cost_output: float  # per 1M tokens
    speed: Literal["⚡⚡⚡", "⚡⚡", "⚡"]
    quality: Literal["🧠", "🧠🧠", "🧠🧠🧠"]
    use_cases: list[str]

# Model catalog (as of 2026-01-06)
MODELS = [
    ModelOption(
        key="haiku",
        name="Claude 3.5 Haiku",
        capabilities="Routine Tasks",
        cost_input=0.25,
        cost_output=1.25,
        speed="⚡⚡⚡",
        quality="🧠",
        use_cases=["research", "data_extraction", "simple_code", "formatting"]
    ),
    ModelOption(
        key="sonnet",
        name="Claude 3.5 Sonnet",
        capabilities="Reasoning/Code",
        cost_input=3.00,
        cost_output=15.00,
        speed="⚡⚡",
        quality="🧠🧠",
        use_cases=["complex_code", "analysis", "refactoring", "multi_step_tasks"]
    ),
    ModelOption(
        key="opus",
        name="Claude 3 Opus",
        capabilities="Complex Architecture",
        cost_input=15.00,
        cost_output=75.00,
        speed="⚡",
        quality="🧠🧠🧠",
        use_cases=["system_design", "critical_decisions", "deep_debugging"]
    )
]

def display_model_table() -> str:
    """Generate formatted model selection table"""

    header = """
+-------------------------------------------------------------+
|         Available Models - Select Execution Strategy       |
+---+---------------------+------+------+--------------------+
| # | Model               | IQ   | Spd  | Cost (In/Out)      |
+---+---------------------+------+------+--------------------+"""

    rows = []
    for i, model in enumerate(MODELS, 1):
        cost_str = f"${model.cost_input:.2f} / ${model.cost_output:.2f}"
        # Use ASCII alternatives for emoji
        quality_ascii = "***" if model.quality == "🧠🧠🧠" else "**" if model.quality == "🧠🧠" else "*"
        speed_ascii = "+++" if model.speed == "⚡⚡⚡" else "++" if model.speed == "⚡⚡" else "+"
        row = f"| {i} | {model.name:19} | {quality_ascii:4} | {speed_ascii:4} | {cost_str:18} |"
        rows.append(row)

    footer = """+---+---------------------+------+------+--------------------+
|  [A] Auto-Select (Let system decide based on complexity)  |
+-------------------------------------------------------------+
"""

    return "\n".join([header] + rows + [footer.strip()])

def auto_select_model(
    prompt: str,
    context_length: int,
    user_preferences: Optional[dict] = None
) -> tuple[str, str]:
    """
    Auto-select model based on task complexity

    Returns:
        (model_key, reasoning)
    """

    complexity_score = 0
    reasoning_parts = []

    # Keyword analysis
    complex_triggers = ['architect', 'refactor', 'debug', 'security', 'compare', 'design']
    matched_triggers = [t for t in complex_triggers if t in prompt.lower()]
    if matched_triggers:
        complexity_score += 2
        reasoning_parts.append(f"Complex keywords detected: {', '.join(matched_triggers)}")

    # Length analysis
    if context_length > 15000:
        complexity_score += 2
        reasoning_parts.append(f"Large context: {context_length:,} tokens")
    elif context_length > 5000:
        complexity_score += 1
        reasoning_parts.append(f"Medium context: {context_length:,} tokens")

    # Multi-step analysis
    multi_step_markers = ['then', 'after', 'next', 'finally', 'step']
    if sum(1 for m in multi_step_markers if m in prompt.lower()) >= 2:
        complexity_score += 1
        reasoning_parts.append("Multi-step task detected")

    # User preference override
    if user_preferences and user_preferences.get("default_model"):
        default = user_preferences["default_model"]
        reasoning_parts.append(f"User default: {default}")
        return default, " | ".join(reasoning_parts)

    # Selection logic
    if complexity_score >= 3:
        return "opus", " | ".join(reasoning_parts + ["-> Opus (High complexity)"])
    elif complexity_score >= 2 or context_length > 5000:
        return "sonnet", " | ".join(reasoning_parts + ["-> Sonnet (Balanced)"])
    else:
        return "haiku", " | ".join(reasoning_parts + ["-> Haiku (Fast/cheap)"])

def estimate_cost(
    model_key: str,
    estimated_input_tokens: int,
    estimated_output_tokens: int
) -> dict:
    """Calculate estimated cost for task execution"""

    model = next(m for m in MODELS if m.key == model_key)

    input_cost = (estimated_input_tokens / 1_000_000) * model.cost_input
    output_cost = (estimated_output_tokens / 1_000_000) * model.cost_output
    total_cost = input_cost + output_cost

    return {
        "model": model.name,
        "input_tokens": estimated_input_tokens,
        "output_tokens": estimated_output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost
    }

def prompt_user_selection() -> str:
    """
    Interactive CLI prompt for model selection

    Returns:
        Selected model key (haiku/sonnet/opus/auto)
    """

    print(display_model_table())

    while True:
        choice = input("\nSelect model [1-3] or [A]uto: ").strip().upper()

        if choice == "A":
            return "auto"

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MODELS):
                return MODELS[idx].key
        except ValueError:
            pass

        print("Invalid selection. Please try again.")

# Example usage
if __name__ == "__main__":
    print(display_model_table())

    # Test auto-selection
    test_cases = [
        ("Summarize this article", 500),
        ("Refactor this codebase using SOLID principles", 8000),
        ("Design a distributed system architecture for 1M users", 12000)
    ]

    print("\n" + "="*60)
    print("AUTO-SELECTION TEST SCENARIOS")
    print("="*60)

    for prompt, context_len in test_cases:
        model, reasoning = auto_select_model(prompt, context_len)
        cost_est = estimate_cost(model, context_len, 1500)

        print(f"\nPrompt: {prompt}")
        print(f"Context: {context_len:,} tokens")
        print(f"Selected: {model.upper()} | {reasoning}")
        print(f"Est. Cost: ${cost_est['total_cost']:.4f}")
