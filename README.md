<p align="center">
  <img src="assets/banner.png?v=3" alt="Zorro Agent" width="100%">
</p>

# Zorro Agent

<p align="center">
  <a href="https://github.com/braxtonROSE4/zorro-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/braxtonROSE4/zorro-agent"><img src="https://img.shields.io/badge/Built%20by-Brax-e94560?style=for-the-badge" alt="Built by Brax"></a>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Models-200+-FFD700?style=for-the-badge" alt="200+ Models">
  <img src="https://img.shields.io/badge/Platforms-19-blue?style=for-the-badge" alt="19 Platforms">
</p>

> *"Zorro never strikes the same way twice — but he always leaves his mark."*

In the 1919 novel *The Curse of Capistrano*, a young nobleman named Diego puts on a black mask and becomes Zorro — not because he was born a fighter, but because every encounter taught him something. Each duel sharpened his blade. Each escape refined his strategy. Each mark he carved — that signature **Z** — was proof that the experience had been absorbed.

**Zorro Agent works the same way.** It starts as a blank agent. But every conversation leaves a mark — a detected signal, a distilled lesson, a new skill. It doesn't just process your requests and forget. It **evolves through use**, turning session experience into domain knowledge, and domain knowledge into executable capabilities.

---

## The Mark — How Zorro Evolves

Just like the fictional Zorro carves a Z after every encounter, Zorro Agent leaves its own mark after every session — structured knowledge that makes the next session smarter.

### ⚔️ Every Duel Teaches (Signal Detection)

Zorro didn't journal about his fights — he learned *during* them. This agent does the same: **8 types of learning signals** are detected on every single turn, at zero API cost:

- A user correction → `[correction][high]`
- A method that worked after trial and error → `[method_discovery][medium]`
- A shift in understanding → `[cognitive_shift][medium]`
- User frustration → **immediate emergency review**

No blind periodic scans. No wasted API calls when nothing happened. The agent only reflects when there's something worth reflecting on.

### 🗡️ The Z Mark (Domain Knowledge)

Zorro's signature wasn't random — he carved it in a specific place, with specific meaning. This agent's knowledge isn't dumped into a single flat file either. It's **partitioned by domain**:

```
~/.zorro/knowledge/
├── _general/lessons.md      # Cross-domain wisdom (G1, G2, ...)
├── product/lessons.md       # Product design (P1, P2, ...)
├── engineering/lessons.md   # Engineering (E1, E2, ...)
└── growth/lessons.md        # Growth strategy (H1, H2, ...)
```

Each lesson is structured: `code | lesson | source | scenario | keywords`. The agent searches the relevant domain first, then falls back to general — like a swordsman reaching for the right technique for the right opponent.

### 🎭 The Mask (Dual Identity)

Diego was an unremarkable nobleman by day. Zorro was precise and lethal by night. This agent has the same duality:

- **What users see**: a simple CLI prompt, a Telegram chat, a Teams message
- **What runs beneath**: signal detection on every turn, distill compression on every large output, session lifecycle management, domain knowledge retrieval — an evolution engine invisible to the user

The **SOUL.md** defines who the agent IS — principles, memory protocol, skill protocol, voice. Not a generic "be helpful" instruction, but a full identity that persists across sessions.

### 🏇 From Apprentice to Master (Capability Growth)

In Isabel Allende's 2005 retelling, young Diego wasn't born a master swordsman. He trained, failed, adapted, and grew. This agent follows the same arc:

```
Session 1:   Empty agent — no memory, no skills, no knowledge
Session 10:  Working memory captures user preferences and environment facts
Session 50:  Domain knowledge accumulates — product, engineering, growth
Session 100: Procedural skills crystallize — the agent handles recurring
             workflows without being told how
```

**The evolution loop:**
```
experience → signal detection → domain knowledge → executable skills → stronger agent
     ↑                                                                        |
     └────────────────────────────────────────────────────────────────────────┘
```

### 💨 Distill (The Quick Blade)

Zorro was fast — no wasted movement. When a tool returns 50,000 characters, most agents feed it all to the model (expensive) or blindly chop the middle (lossy). Zorro Agent uses a **cheap auxiliary LLM** (~$0.001) to extract only the task-relevant information:

> 50K chars of `grep` output → Distill → 5K chars of exactly what the agent needs

Two quality gates prevent degradation. When compression fails, it falls back gracefully. No downside — only upside.

---

## How Does It Compare?

Three frameworks claim to "learn" across sessions. Here's what each actually does:

| Capability | OpenClaw | Hermes Agent | **Zorro Agent** |
|---|---|---|---|
| **Memory storage** | Markdown + vector search | 2.2K flat text file | 2.2K working memory + **domain-partitioned knowledge base** |
| **Learning from experience** | None — static skills only | Blind review every 10 turns | **Signal-driven**: 8-type detection every turn (zero cost) |
| **Skill creation** | Manual only | Autonomous | Autonomous + **user confirmation** |
| **Tool output handling** | Raw truncation | Head/tail mechanical cut | **Distill**: auxiliary LLM extracts relevant signal |
| **Session boundaries** | None | None | **Structured summaries** with learning inventory |
| **Agent identity** | SOUL.md persona | One-paragraph generic | **SOUL.md** with principles, protocols, voice |
| **User sentiment** | Not detected | Not detected | **Rating + frustration detection** (triggers review) |
| **Review cost** | N/A | 1 API call / 10 turns always | **0 calls** when quiet; 1 call when warranted |
| **Platforms** | 20+ | 17 | **19** (added Teams) |
| **Models** | Limited | 200+ | 200+ |
| **Security** | Known CVEs | Pattern + LLM approval | Pattern + LLM approval + secret redaction |

### The Honest Take

- **OpenClaw**: Best platform coverage, zero learning capability, concerning security record.
- **Hermes**: Added learning loop, but blind review (same cost whether 10 corrections or zero) and flat memory.
- **Zorro**: Memory-first architecture — **signal detection → smart triggering → domain knowledge → distill compression → session lifecycle**. Gets stronger every session.

---

## Core Capabilities

<table>
<tr><td><b>Full TUI</b></td><td>prompt_toolkit terminal UI — multiline editing, slash commands, tab completion, streaming, interrupt handling, conversation branching.</td></tr>
<tr><td><b>19 Platforms</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, iMessage, Microsoft Teams, WeChat, WeCom, Feishu, DingTalk, Matrix, Mattermost, Email, SMS, Home Assistant, API Server, Webhooks.</td></tr>
<tr><td><b>100+ Tools</b></td><td>Terminal, file ops, web search, browser automation, code execution, vision, TTS, image generation, MCP servers.</td></tr>
<tr><td><b>Skills System</b></td><td>YAML+Markdown procedural knowledge. Created from experience, loaded by relevance, patched when outdated.</td></tr>
<tr><td><b>Session Search</b></td><td>FTS5 full-text search across all past conversations with LLM summarization.</td></tr>
<tr><td><b>Any Model</b></td><td>OpenRouter (200+), OpenAI, Anthropic, Gemini, Kimi, MiniMax, Mistral, Ollama, or any compatible endpoint.</td></tr>
<tr><td><b>Cron</b></td><td>Scheduled tasks in natural language, delivered to any platform.</td></tr>
<tr><td><b>Subagents</b></td><td>Isolated child agents for parallel work. Code execution via RPC.</td></tr>
<tr><td><b>6 Backends</b></td><td>Local, Docker, SSH, Daytona, Singularity, Modal. Serverless hibernation.</td></tr>
<tr><td><b>Security</b></td><td>Dangerous command detection, smart LLM approval, DM pairing, secret redaction.</td></tr>
</table>

---

## Quick Start

```bash
git clone https://github.com/braxtonROSE4/zorro-agent.git
cd zorro-agent
pip install -e ".[all]"
zorro setup    # Configure provider + model + API key
zorro          # Start chatting
```

## CLI Commands

```
zorro                # Interactive chat
zorro setup          # Setup wizard
zorro model          # Switch model
zorro gateway        # Multi-platform gateway
zorro status         # Configuration status
zorro doctor         # Diagnose issues
```

## Architecture

```
~/.zorro/
├── SOUL.md                     # Who the agent IS
├── config.yaml                 # Configuration
├── .env                        # API keys
├── state.db                    # Sessions (SQLite + FTS5)
├── memories/
│   ├── MEMORY.md               # Working memory (~2200 chars)
│   └── USER.md                 # User profile (~1375 chars)
├── knowledge/                  # Domain-partitioned lessons
│   ├── _general/lessons.md     # G-codes (cross-domain)
│   ├── product/lessons.md      # P-codes
│   ├── engineering/lessons.md  # E-codes
│   └── .../lessons.md          # Extensible
├── skills/                     # Procedural knowledge
│   └── <name>/SKILL.md
├── sessions/                   # Session summaries
└── logs/
```

## Documentation

| Guide | Description |
|-------|-------------|
| [docs/imessage.md](docs/imessage.md) | iMessage setup via BlueBubbles (macOS required) |
| [docs/teams.md](docs/teams.md) | Microsoft Teams via Azure Bot Framework |

## License

MIT
