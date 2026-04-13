"""
Qwen 2.5 tool call parser.

Uses the same <tool_call> format as Zorro.
Registered as a separate parser name for clarity when using --tool-parser=qwen.
"""

from environments.tool_call_parsers import register_parser
from environments.tool_call_parsers.zorro_parser import ZorroToolCallParser


@register_parser("qwen")
class QwenToolCallParser(ZorroToolCallParser):
    """
    Parser for Qwen 2.5 tool calls.
    Same <tool_call>{"name": ..., "arguments": ...}</tool_call> format as Zorro.
    """

    pass  # Identical format -- inherits everything from Zorro
