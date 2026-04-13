"""Session lifecycle hooks for Zorro Agent.

Handles session-end summary generation. Writes structured markdown
summaries to ~/.zorro/sessions/ for long-term recall.
"""

import logging
from datetime import datetime
from pathlib import Path

from zorro_constants import get_zorro_home

logger = logging.getLogger(__name__)


def write_session_summary(
    session_id: str,
    turn_count: int,
    learning_candidates: list,
    final_response: str = "",
    original_user_message: str = "",
) -> None:
    """Write a structured session summary to ~/.zorro/sessions/."""
    sessions_dir = get_zorro_home() / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    filename = now.strftime("%Y%m%d-%H%M") + ".md"
    path = sessions_dir / filename

    parts = [
        f"## Session Summary — {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**Session ID:** {session_id}",
        f"**Turns:** {turn_count}",
        f"**Date:** {now.strftime('%Y-%m-%d')}",
        "",
        "## First User Request",
        original_user_message[:500] if original_user_message else "(none)",
        "",
    ]

    # Learning signals section
    parts.append("## Detected Learning Signals")
    if learning_candidates:
        for c in learning_candidates:
            parts.append(
                f"- [{c.get('type', '?')}][{c.get('confidence', '?')}] "
                f"{c.get('text', c.get('match', '—'))}"
            )
    else:
        parts.append("(none detected)")

    # Closing checklist
    parts.extend([
        "",
        "## Closing Checklist",
        f"- {'✅' if learning_candidates else '❌'} "
        f"Learning signals: {len(learning_candidates)} detected",
    ])

    try:
        path.write_text("\n".join(parts), encoding="utf-8")
        logger.debug("Session summary written to %s", path)
    except Exception as e:
        logger.warning("Failed to write session summary: %s", e)

    # Prune old summaries (keep last 30)
    try:
        summaries = sorted(sessions_dir.glob("*.md"), reverse=True)
        for old in summaries[30:]:
            old.unlink()
    except Exception:
        pass
