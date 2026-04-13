"""Language-aware signal pattern loader."""
import os


def load_patterns(lang: str = None) -> dict:
    """Return all patterns for the given language.

    Auto-detect from LANG env var if not specified.
    """
    if lang is None:
        lang = "zh" if "zh" in os.getenv("LANG", "") else "en"

    if lang.startswith("zh"):
        from . import zh as mod
    else:
        from . import en as mod

    return {
        "correction": mod.CORRECTION_PATTERNS,
        "insight": mod.INSIGHT_PATTERNS,
        "error": mod.ERROR_PATTERNS,
        "cognitive_shift": mod.COGNITIVE_SHIFT_PATTERNS,
        "method_discovery": mod.METHOD_DISCOVERY_PATTERNS,
        "anti_pattern": mod.ANTI_PATTERN_PATTERNS,
        "profile_update": mod.PROFILE_UPDATE_PATTERNS,
        "completion": mod.COMPLETION_SIGNALS,
        "correction_sequence": mod.CORRECTION_SEQUENCE_PATTERNS,
        "framework_signal": mod.FRAMEWORK_SIGNAL_PATTERNS,
        "decision_rationale": mod.DECISION_RATIONALE_PATTERNS,
        "retry": mod.RETRY_PATTERNS,
        "explicit_lesson": mod.EXPLICIT_LESSON_PATTERNS,
        "score": mod.SCORE_PATTERNS,
        "score_exclude_after": mod.SCORE_EXCLUDE_AFTER,
        "frustration": mod.FRUSTRATION_SIGNALS,
        "satisfaction": mod.SATISFACTION_SIGNALS,
    }
