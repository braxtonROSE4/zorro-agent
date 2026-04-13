"""Zero-cost learning signal detection. Runs every turn via regex, no API calls.

8 signal types for per-message detection:
  correction, insight, error, cognitive_shift,
  method_discovery, anti_pattern, profile_update, procedural_candidate

3 sentiment types:
  score (explicit 1-10), frustration (implicit), satisfaction (implicit)

Confidence levels:
  "high" — correction, insight, error, user-originated signals
  "medium" — cognitive_shift, method_discovery, anti_pattern, profile_update
"""

import re
from datetime import datetime
from typing import Optional

from agent.signal_patterns import load_patterns

_CONFIDENCE = {
    "correction": "high",
    "insight": "high",
    "error": "high",
    "cognitive_shift": "medium",
    "method_discovery": "medium",
    "anti_pattern": "medium",
    "profile_update": "medium",
    "procedural_candidate": "medium",
}

_SIGNAL_TYPES = list(_CONFIDENCE.keys())

_SCORE_EXCLUDE_BEFORE = [r"\d{4}[-/]", r"[vV]", r"[#]", r"第"]


class SignalDetector:
    """Stateless signal detector. Create one per session, call on every turn."""

    def __init__(self, lang: str = None):
        self._patterns = load_patterns(lang)

    def detect_signals(self, text: str, source: str = "assistant") -> list[dict]:
        """Detect learning signals in a single message.

        source: "assistant" or "user". User signals override confidence to "high".
        Returns list of {type, match, text, confidence, source, detected_at}.
        """
        if not text:
            return []
        results = []
        for signal_type in _SIGNAL_TYPES:
            if signal_type == "procedural_candidate":
                continue
            for pattern in self._patterns.get(signal_type, []):
                m = re.search(pattern, text, re.IGNORECASE)
                if m:
                    conf = "high" if source == "user" else _CONFIDENCE.get(signal_type, "medium")
                    results.append({
                        "type": signal_type,
                        "match": m.group(),
                        "text": self._extract_context(text, m.group()),
                        "confidence": conf,
                        "source": source,
                        "detected_at": datetime.now().isoformat(),
                    })
                    break  # One hit per category
        return results

    def detect_procedural(self, tool_call_count: int, had_strategy_change: bool,
                          user_msg: str) -> Optional[dict]:
        """Detect procedural knowledge candidate from turn-level metadata."""
        if tool_call_count >= 3 and had_strategy_change:
            return {
                "type": "procedural_candidate",
                "match": f"{tool_call_count} tool calls with strategy change",
                "text": f"Agent used {tool_call_count} tools and changed approach mid-task",
                "confidence": "medium",
                "source": "system",
                "detected_at": datetime.now().isoformat(),
            }
        workflow_patterns = [
            r"(?:don't|never|stop|别|不要)\s*(?:do|use|run|try|这样|这么)",
            r"(?:instead|rather|better to|应该|正确的做法)\s*(?:do|use|run|是)",
            r"(?:the right way|correct way|should|正确的流程)\s*(?:is|be|是)",
        ]
        if user_msg:
            for p in workflow_patterns:
                m = re.search(p, user_msg, re.IGNORECASE)
                if m:
                    return {
                        "type": "procedural_candidate",
                        "match": m.group(),
                        "text": self._extract_context(user_msg, m.group()),
                        "confidence": "high",
                        "source": "user",
                        "detected_at": datetime.now().isoformat(),
                    }
        return None

    def detect_rating(self, text: str) -> Optional[dict]:
        """Detect explicit score (1-10) in text."""
        if not text or len(text) > 500:
            return None
        for pattern in self._patterns.get("score", []):
            m = re.search(pattern, text)
            if not m:
                continue
            score_str = next((g for g in m.groups() if g is not None), None)
            if score_str is None:
                continue
            score = int(score_str)
            if score < 1 or score > 10:
                continue
            before = text[max(0, m.start() - 5):m.start()]
            if any(re.search(p + r"\s*$", before) for p in _SCORE_EXCLUDE_BEFORE):
                continue
            after = text[m.end():min(len(text), m.end() + 3)].lstrip()
            if any(re.match(p, after) for p in self._patterns.get("score_exclude_after", [])):
                continue
            return {"score": score, "raw_match": m.group()}
        return None

    def detect_sentiment(self, text: str) -> Optional[dict]:
        """Detect implicit frustration or satisfaction."""
        if not text or len(text) > 500:
            return None
        for p in self._patterns.get("frustration", []):
            m = re.search(p, text, re.IGNORECASE)
            if m:
                return {"sentiment": "frustration", "raw_match": m.group()}
        for p in self._patterns.get("satisfaction", []):
            m = re.search(p, text, re.IGNORECASE)
            if m:
                return {"sentiment": "satisfaction", "raw_match": m.group()}
        return None

    @staticmethod
    def _extract_context(text: str, match_str: str, window: int = 1) -> str:
        """Extract matched sentence + surrounding sentences."""
        sentences = re.split(r'[.!?\n。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        for i, sent in enumerate(sentences):
            if match_str in sent:
                start = max(0, i - window)
                end = min(len(sentences), i + window + 1)
                return " | ".join(sentences[start:end])[:300]
        return match_str[:200]
