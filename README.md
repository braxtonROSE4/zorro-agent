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

**A self-evolving CLI agent.** Most agents treat memory as an afterthought — a flat text file that grows until it's useless. Zorro was designed around a different idea: that the real value of an agent isn't what it can do on day one, but how much stronger it gets by day one hundred.

The name comes from the fictional swordsman who carved a **Z** after every encounter — not out of vanity, but as proof that the experience had been absorbed. This agent does something similar. Every session leaves a mark: a detected learning signal, a lesson filed into the right domain, a workflow crystallized into a reusable skill. Over time, these marks compound. The agent that helped you debug authentication last month now *knows* your codebase's auth patterns and applies them without being told.

Use any model — [OpenRouter](https://openrouter.ai) (200+ models), OpenAI, Anthropic, Gemini, Kimi, MiniMax, Ollama, or your own endpoint. Talk to it from the terminal, Telegram, Discord, Teams, iMessage, or 14 other platforms. Switch models with `zorro model` — no code changes, no lock-in.

---

## How the Evolution Works

The framework is built around a single loop:

```
experience → signal detection → domain knowledge → executable skills → stronger agent
     ↑                                                                        |
     └────────────────────────────────────────────────────────────────────────┘
```

This isn't a metaphor — it's the actual data flow. Here's each stage:

### 1. Signal Detection

On every turn, a lightweight regex engine scans both the user's message and the agent's response for 8 types of learning signals — corrections, insights, errors, cognitive shifts, method discoveries, anti-patterns, profile updates, and procedural candidates. Bilingual (EN/ZH). Zero API cost.

These signals accumulate in session state with confidence levels (`high` / `medium`). The agent doesn't stop to think about whether it learned something — the detection is automatic and invisible.

```
User: "Don't mock the database in tests — we got burned by that last quarter"
       → [correction][high] detected, queued for review
```

### 2. Smart Review Trigger

Other frameworks run a background review every N turns regardless — same cost whether the conversation had ten corrections or zero. Zorro uses three trigger paths:

| Condition | What happens |
|-----------|-------------|
| Base interval (every 10 turns) | Standard review, same as others |
| 2+ high-confidence signals accumulated | **Early review** — don't wait for the timer |
| User frustration detected | **Immediate review** — something went wrong, learn from it now |
| Nothing detected in 10 turns | **Skip entirely** — save the API call |

When review fires, it's not blind. The background agent receives the pre-filtered signals with types and confidence levels, so it knows exactly what to look for in the conversation.

### 3. Domain Knowledge

Lessons don't go into a single file. They're partitioned by domain, each with structured entries:

```
~/.zorro/knowledge/
├── _general/lessons.md      # Cross-domain (G1, G2, ...)
├── product/lessons.md       # Product design (P1, P2, ...)
├── engineering/lessons.md   # Engineering (E1, E2, ...)
└── growth/lessons.md        # Growth/marketing (H1, H2, ...)
```

Format: `code | lesson | source | scenario | keywords`. When the agent encounters a new task, it searches the relevant domain first, then falls back to general knowledge. This is why a product question doesn't surface engineering lessons — the knowledge is organized the way an expert's mind is organized.

### 4. Skill Crystallization

When the review agent identifies a reusable workflow — not just a fact, but a *procedure* — it proposes saving it as a Skill. The agent asks the user first:

> "I noticed that when debugging auth flows, you always check token refresh before looking at CORS. Want me to save this as a reusable skill?"

If confirmed, the workflow becomes a YAML+Markdown skill file that loads automatically on future matching tasks. This is the moment experience becomes capability.

### 5. Distill Compression

Alongside the evolution loop, there's a practical optimization: when any tool returns more than 8K characters, a cheap auxiliary model (~$0.001 per call) compresses the output to only what's relevant to the current task. A 50K-char `grep` result becomes 5K chars of pure signal. Two quality gates reject bad compressions and fall back to traditional head/tail truncation. The main model never sees noise it doesn't need.

### 6. Session Lifecycle

At the end of every conversation, the agent writes a structured summary — what was asked, what signals were detected, what's unresolved. This isn't stored in the model's context (which would be expensive). It's a Markdown file in `~/.zorro/sessions/` that future sessions can search via FTS5 when context is needed.

### What This Looks Like Over Time

```
Session 1:   Blank slate — no memory, no skills, no knowledge
Session 10:  Preferences captured. Knows your tools, your style, your stack.
Session 50:  Domain knowledge grows. Product, engineering, growth — each with
             its own lesson library, searchable by keyword.
Session 100: Skills crystallize. Recurring workflows run without instruction.
             The agent handles your patterns because it learned them from you.
```

The agent on session 100 is not the same agent as session 1. That's the point.

---

## The Mask — What's Underneath

Like the fictional Zorro — an unremarkable nobleman by day, precise and dangerous by night — the interface is deceptively simple. Users see a CLI prompt or a chat message. Underneath:

- **SOUL.md** defines who the agent is — not "be helpful" but a full identity with principles, memory protocol, skill protocol, and voice guidelines. Users can replace `~/.zorro/SOUL.md` to reshape the agent entirely.
- **Signal detection** runs on every turn without the user knowing.
- **Distill compression** fires on every large tool output automatically.
- **Session summaries** are written silently at conversation end.
- **Domain knowledge** is searched before every response.

The user just talks. The evolution happens behind the mask.

---

## Comparison

| Capability | OpenClaw | Hermes Agent | **Zorro Agent** |
|---|---|---|---|
| **Memory** | Markdown + vector search | 2.2K flat text | Working memory + **domain-partitioned knowledge** |
| **Learning** | None (static skills) | Blind review / 10 turns | **Signal-driven** (8 types, zero cost) |
| **Skills** | Manual only | Autonomous | Autonomous + **user confirmation** |
| **Tool output** | Raw truncation | Head/tail cut | **Distill** (auxiliary LLM extraction) |
| **Sessions** | No boundaries | No boundaries | **Structured summaries** |
| **Identity** | SOUL.md | One paragraph | **SOUL.md** (principles + protocols + voice) |
| **Sentiment** | Not detected | Not detected | **Rating + frustration → triggers review** |
| **Review cost** | N/A | 1 call / 10 turns always | **0 when quiet**, 1 when warranted |
| **Platforms** | 20+ | 17 | **19** |
| **Models** | Limited | 200+ | 200+ |

- **OpenClaw**: Broad platform coverage, zero learning, security concerns.
- **Hermes**: Added a learning loop — but blind (same cost whether there's signal or not) with flat memory.
- **Zorro**: Memory-first. Signal detection → smart review → domain knowledge → skills → lifecycle.

---

## Capabilities

<table>
<tr><td><b>Full TUI</b></td><td>prompt_toolkit — multiline editing, slash commands, tab completion, streaming, interrupt handling, conversation branching.</td></tr>
<tr><td><b>19 Platforms</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, iMessage, Teams, WeChat, WeCom, Feishu, DingTalk, Matrix, Mattermost, Email, SMS, Home Assistant, API Server, Webhooks.</td></tr>
<tr><td><b>100+ Tools</b></td><td>Terminal, file ops, web search, browser, code execution, vision, TTS, image gen, MCP.</td></tr>
<tr><td><b>Skills</b></td><td>YAML+Markdown procedural knowledge. Created from experience, loaded by relevance, patched when outdated.</td></tr>
<tr><td><b>Session Search</b></td><td>FTS5 full-text across all past conversations, with LLM summarization.</td></tr>
<tr><td><b>Any Model</b></td><td>OpenRouter (200+), OpenAI, Anthropic, Gemini, Kimi, MiniMax, Mistral, Ollama, any compatible endpoint.</td></tr>
<tr><td><b>Cron</b></td><td>Natural-language scheduled tasks, delivered to any platform.</td></tr>
<tr><td><b>Subagents</b></td><td>Isolated child agents for parallel work. Code execution via RPC.</td></tr>
<tr><td><b>6 Backends</b></td><td>Local, Docker, SSH, Daytona, Singularity, Modal.</td></tr>
<tr><td><b>Security</b></td><td>Dangerous command detection, smart LLM approval, DM pairing, secret redaction.</td></tr>
</table>

---

## Quick Start

```bash
git clone https://github.com/braxtonROSE4/zorro-agent.git
cd zorro-agent
pip install -e ".[all]"
zorro setup    # Provider + model + API key
zorro          # Start
```

## Architecture

```
~/.zorro/
├── SOUL.md                     # Agent identity
├── config.yaml
├── .env
├── state.db                    # SQLite + FTS5
├── memories/
│   ├── MEMORY.md               # Working memory (~2200 chars)
│   └── USER.md                 # User profile (~1375 chars)
├── knowledge/                  # Domain-partitioned lessons
│   ├── _general/lessons.md
│   ├── product/lessons.md
│   ├── engineering/lessons.md
│   └── .../lessons.md
├── skills/
│   └── <name>/SKILL.md
├── sessions/                   # Summaries
└── logs/
```

## Docs

| Guide | Description |
|-------|-------------|
| [docs/imessage.md](docs/imessage.md) | iMessage via BlueBubbles (macOS required) |
| [docs/teams.md](docs/teams.md) | Microsoft Teams via Azure Bot Framework |

## License

MIT
