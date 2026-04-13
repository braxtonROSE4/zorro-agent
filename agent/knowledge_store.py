"""Domain-partitioned knowledge store.

Lessons are stored in ~/.zorro/knowledge/<domain>/lessons.md using G-code
table format. Supports:
- Domain-scoped search (keyword matching within a specific domain)
- Cross-domain search (_general/ always included)
- Adding new lessons with auto-incrementing codes
- Summary generation (count + categories) for system prompt injection
"""

import re
import logging
from pathlib import Path
from typing import Optional

from zorro_constants import get_zorro_home

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = "knowledge"
GENERAL_DOMAIN = "_general"
KNOWN_DOMAINS = ["_general", "product", "growth", "engineering", "investment"]

DOMAIN_PREFIX = {
    "_general": "G",
    "product": "P",
    "growth": "H",
    "engineering": "E",
    "investment": "I",
}


def get_knowledge_dir() -> Path:
    return get_zorro_home() / KNOWLEDGE_DIR


def _parse_lessons(path: Path) -> list[dict]:
    """Parse a single lessons.md file into structured entries."""
    if not path.exists():
        return []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return []

    entries = []
    current_category = ""
    for line in content.split("\n"):
        if line.startswith("## "):
            current_category = line[3:].strip()
            continue
        if not re.match(r'^\|\s*[A-Z]\d+', line):
            continue
        if "待补充" in line:
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if len(cells) < 4:
            continue
        keywords_raw = cells[4] if len(cells) >= 5 else ""
        entries.append({
            "code": cells[0],
            "lesson": cells[1],
            "source": cells[2] if len(cells) >= 3 else "",
            "scenario": cells[3],
            "keywords": [kw.strip().lower() for kw in keywords_raw.split(",") if kw.strip()],
            "category": current_category,
            "domain": path.parent.name,
        })
    return entries


def search_lessons(query: str, domain: str = None) -> list[dict]:
    """Search lessons by keyword matching.

    If domain is specified, search that domain + _general.
    If domain is None, search all domains.
    """
    kdir = get_knowledge_dir()
    if not kdir.exists():
        return []

    domains_to_search = [domain, GENERAL_DOMAIN] if domain else KNOWN_DOMAINS

    query_lower = query.lower()
    query_tokens = set(re.split(r'[\s,，。.!?]+', query_lower))
    query_tokens.discard("")

    results = []
    seen_codes = set()
    for d in domains_to_search:
        path = kdir / d / "lessons.md"
        for entry in _parse_lessons(path):
            if entry["code"] in seen_codes:
                continue
            entry_keywords = set(entry["keywords"])
            # Match: any keyword overlap OR substring match in lesson text
            if entry_keywords & query_tokens:
                results.append(entry)
                seen_codes.add(entry["code"])
            elif any(tok in entry["lesson"].lower() for tok in query_tokens if len(tok) >= 2):
                results.append(entry)
                seen_codes.add(entry["code"])
    return results


def get_knowledge_summary() -> str:
    """Return a compact summary for system prompt injection.

    e.g. 'Knowledge base: 28 lessons (general: 12, product: 8, growth: 5, investment: 3)'
    """
    kdir = get_knowledge_dir()
    if not kdir.exists():
        return ""

    counts = {}
    for d in KNOWN_DOMAINS:
        entries = _parse_lessons(kdir / d / "lessons.md")
        if entries:
            counts[d] = len(entries)
    if not counts:
        return ""

    total = sum(counts.values())
    parts = [f"{d}: {n}" for d, n in counts.items()]
    return f"Knowledge base: {total} lessons ({', '.join(parts)})"


def add_lesson(domain: str, lesson: str, source: str = "",
               scenario: str = "", keywords: str = "") -> dict:
    """Add a new lesson to the specified domain. Auto-assigns the next code."""
    kdir = get_knowledge_dir()
    domain_dir = kdir / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    path = domain_dir / "lessons.md"

    prefix = DOMAIN_PREFIX.get(domain, "X")
    existing = _parse_lessons(path)
    max_num = 0
    for e in existing:
        m = re.match(r'[A-Z](\d+)', e["code"])
        if m:
            max_num = max(max_num, int(m.group(1)))
    new_code = f"{prefix}{max_num + 1}"

    new_line = f"| {new_code} | {lesson} | {source} | {scenario} | {keywords} |"

    if path.exists():
        content = path.read_text(encoding="utf-8")
        if not content.endswith("\n"):
            content += "\n"
        content += new_line + "\n"
    else:
        content = (
            f"# {domain.replace('_', '').title()} Lessons\n\n"
            "| 编号 | 经验 | 来源 | 适用场景 | 关键词 |\n"
            "|------|------|------|---------|--------|\n"
            f"{new_line}\n"
        )

    path.write_text(content, encoding="utf-8")
    return {"success": True, "code": new_code, "domain": domain}
