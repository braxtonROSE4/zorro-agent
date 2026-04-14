"""Distill — task-aware compression of large tool outputs using auxiliary LLM.

Instead of mechanically truncating tool results (head/tail split), distill
uses a cheap auxiliary model (Gemini Flash, Haiku, etc.) to extract only the
information relevant to the agent's current task.

Inspired by github.com/samuelfaj/distill. The key insight: a $0.001 call to
a small model can replace 50K chars of raw output with 2K chars of signal,
saving $0.05+ on the main model's context window per turn.

Two entry points:
  - distill_tool_output(): For tool_result_storage Layer 2 (before disk persist)
  - distill_terminal_output(): For terminal_tool (before head/tail truncation)

Both fall back to None if auxiliary model is unavailable or compression fails,
letting the caller proceed with its existing truncation logic.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Don't bother compressing below this threshold — not worth the latency
MIN_INPUT_CHARS = 8_000

# Target output size — should be well under the per-result persistence threshold
DEFAULT_TARGET_CHARS = 5_000

# If compressed output is >= this ratio of input, compression failed
MAX_COMPRESSION_RATIO = 0.8

_SYSTEM_PROMPT = (
    "You are a tool output compressor for an AI agent. Your job is to distill "
    "large command outputs into only the information the agent needs for its "
    "current task.\n\n"
    "Rules:\n"
    "1. Preserve ALL error messages, stack traces, and warnings verbatim\n"
    "2. Preserve ALL file paths, command names, function names, and URLs\n"
    "3. Preserve ALL numeric results, counts, sizes, and key data points\n"
    "4. Remove redundant lines (repeated log entries, verbose progress bars)\n"
    "5. Remove boilerplate headers, footers, and decoration\n"
    "6. Use the original format (don't convert to prose — keep structure)\n"
    "7. If the output is a list, keep all unique entries but remove duplicates\n"
    "8. Never add commentary or explanation — output ONLY the compressed result\n"
    "9. Never use markdown formatting — plain text only"
)


def distill_tool_output(
    content: str,
    tool_name: str,
    task_context: str = "",
    target_chars: int = DEFAULT_TARGET_CHARS,
) -> Optional[str]:
    """Compress a tool result using the auxiliary LLM.

    Synchronous — blocks until the auxiliary model responds.
    Returns compressed text, or None if compression is unavailable or fails.
    The caller should fall back to its existing truncation logic on None.

    Args:
        content: Raw tool output to compress.
        tool_name: Name of the tool (terminal, search_files, etc.)
        task_context: The user's current task / question (improves relevance).
        target_chars: Target output size in characters.
    """
    if len(content) < MIN_INPUT_CHARS:
        return None

    try:
        from agent.auxiliary_client import call_llm, extract_content_or_reasoning
    except ImportError:
        return None

    user_prompt = _build_user_prompt(content, tool_name, task_context, target_chars)

    try:
        response = call_llm(
            task="compression",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=target_chars // 3,  # ~3 chars per token
        )
        result = extract_content_or_reasoning(response)
    except Exception as e:
        logger.debug("Distill compression failed (auxiliary model error): %s", e)
        return None

    if not result or not result.strip():
        return None

    result = result.strip()

    # Quality gate: if compression didn't actually compress, it failed
    if len(result) >= len(content) * MAX_COMPRESSION_RATIO:
        logger.debug(
            "Distill compression rejected: output %d chars >= %.0f%% of input %d chars",
            len(result), MAX_COMPRESSION_RATIO * 100, len(content),
        )
        return None

    # Quality gate: if result looks like a refusal or meta-commentary
    lower = result[:200].lower()
    if any(phrase in lower for phrase in [
        "please provide", "i cannot", "the output shows", "here is a summary",
        "the command output", "based on the output",
    ]):
        logger.debug("Distill compression rejected: looks like meta-commentary")
        return None

    original_len = len(content)
    compressed_len = len(result)
    saved_pct = (1 - compressed_len / original_len) * 100
    logger.info(
        "Distill: %s output compressed %d -> %d chars (%.0f%% saved)",
        tool_name, original_len, compressed_len, saved_pct,
    )
    return result


def _build_user_prompt(
    content: str, tool_name: str, task_context: str, target_chars: int
) -> str:
    """Build the user prompt for the compression request."""
    # Cap what we send to the auxiliary model — no point sending 500K to a small model
    max_input = 100_000
    if len(content) > max_input:
        half = max_input // 2
        content = (
            content[:half]
            + f"\n\n... [{len(content) - max_input:,} chars omitted] ...\n\n"
            + content[-half:]
        )

    parts = [f"Tool: {tool_name}"]
    if task_context:
        parts.append(f"Agent's current task: {task_context}")
    parts.append(f"Target size: ~{target_chars} characters")
    parts.append(f"\nOriginal output ({len(content):,} chars):\n{content}")

    return "\n".join(parts)
