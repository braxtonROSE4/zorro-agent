"""Per-session mutable state. Tracks learning signals, turn counts, and review triggers.

NOT the same as zorro_state.py (which is persistent SQLite).
SessionState lives in memory for one session and is discarded at session end
(after persisting signals to session summary).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class SessionState:
    """Mutable state for one agent session."""

    turn_count: int = 0
    learning_candidates: list = field(default_factory=list)
    signal_counts: dict = field(default_factory=lambda: {
        "correction": 0, "insight": 0, "error": 0,
        "cognitive_shift": 0, "method_discovery": 0,
        "anti_pattern": 0, "profile_update": 0,
        "procedural_candidate": 0,
    })
    high_confidence_count: int = 0
    has_frustration: bool = False
    last_review_turn: int = 0
    last_rating: Optional[dict] = None
    _last_review_time: str = ""

    def add_signal(self, signal: dict) -> None:
        """Append a detected signal and update counters."""
        self.learning_candidates.append(signal)
        sig_type = signal.get("type", "")
        if sig_type in self.signal_counts:
            self.signal_counts[sig_type] += 1
        if signal.get("confidence") == "high":
            self.high_confidence_count += 1

    def add_sentiment(self, sentiment: dict) -> None:
        """Record sentiment signal."""
        if sentiment.get("sentiment") == "frustration":
            self.has_frustration = True

    def should_trigger_review(self, base_interval: int = 10) -> bool:
        """Determine if background review should fire NOW.

        Three trigger paths:
        1. Base interval: every N turns (original Zorro logic)
        2. Signal accumulation: 2+ high-confidence signals since last review
        3. Frustration: immediate review when user is frustrated
        """
        turns_since_review = self.turn_count - self.last_review_turn

        # Path 1: Base interval
        if turns_since_review >= base_interval:
            return True

        # Path 2: Signal accumulation
        recent_high = sum(
            1 for s in self.learning_candidates
            if s.get("confidence") == "high"
            and s.get("detected_at", "") > self._last_review_time
        )
        if recent_high >= 2:
            return True

        # Path 3: Frustration
        if self.has_frustration:
            return True

        return False

    def get_signals_for_review(self) -> str:
        """Format accumulated signals as text block for review prompt injection."""
        if not self.learning_candidates:
            return "No learning signals detected this session."
        lines = []
        for s in self.learning_candidates:
            lines.append(f"- [{s['type']}][{s['confidence']}] {s.get('text', s.get('match', ''))}")
        return "\n".join(lines)

    def get_memory_compaction_note(self, memory_store) -> str:
        """If memory is >90% full, return compaction instruction."""
        if not memory_store:
            return ""
        try:
            usage = memory_store._char_count("memory")
            limit = memory_store.memory_char_limit
            pct = int((usage / limit) * 100) if limit > 0 else 0
            if pct >= 90:
                return (
                    f"\n\n**Memory compaction needed** — MEMORY.md is at {pct}% ({usage}/{limit} chars).\n"
                    "Review all entries and:\n"
                    "1. Merge related entries into one\n"
                    "2. Remove entries already covered by a Skill\n"
                    "3. Remove facts not referenced in 3+ sessions\n"
                    "4. Keep all user preferences and corrections (always important)\n"
                )
        except Exception:
            pass
        return ""

    def mark_review_done(self) -> None:
        """Reset review trigger state after background review completes."""
        self.last_review_turn = self.turn_count
        self._last_review_time = datetime.now().isoformat()
        self.has_frustration = False
        self.high_confidence_count = 0
