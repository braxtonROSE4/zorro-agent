# Zorro Agent

**The CLI agent that actually remembers.**

Built on [Hermes Agent](https://github.com/NousResearch/hermes-agent) v0.8.0, then rebuilt with a memory architecture that doesn't just store text — it detects what's worth remembering, decides when to act on it, and compresses what it passes to the model. The result: an agent that learns faster, forgets less, and costs less to run.

---

## How Does It Compare?

Three open-source agent frameworks claim to "learn" across sessions. Here's what each one actually does:

| Capability | OpenClaw | Hermes Agent | **Zorro Agent** |
|---|---|---|---|
| **Memory storage** | Markdown files + vector search | 2.2K char flat text (MEMORY.md) | 2.2K working memory + **domain-partitioned knowledge base** (G-code structured entries per domain) |
| **Learning from experience** | None — skills are static, manually maintained | Background agent reviews every 10 turns (blind, no signal detection) | **Signal-driven**: 8-type regex detection every turn (zero cost) → only reviews when signals accumulate |
| **Skill creation** | Manual only | Agent can create/patch skills autonomously | Agent creates/patches skills + **asks user to confirm** before saving procedural knowledge |
| **Tool output handling** | Raw truncation | Head 40% + tail 60% (mechanical cut) | **Distill compression**: auxiliary LLM extracts task-relevant information before truncation |
| **Session boundaries** | No end-of-session processing | No end-of-session processing | **Structured session summaries** with learning signal inventory + closing checklist |
| **Agent identity** | SOUL.md (persona file) | One-paragraph generic identity | **SOUL.md** with principles, memory protocol, skill protocol, and voice guidelines |
| **User sentiment** | Not detected | Not detected | **Rating capture** (explicit 1-10) + **frustration/satisfaction detection** (implicit, triggers emergency review) |
| **Review cost** | N/A (no review) | 1 API call every 10 turns regardless | **0 API calls** when nothing detected; 1 call when signals warrant it |
| **Platform adapters** | 20+ (gateway-first architecture) | 17 adapters | **19 adapters** (added Microsoft Teams) |
| **Model support** | Claude, GPT, Gemini, Ollama | 200+ via OpenRouter + direct | 200+ via OpenRouter + direct (same) |
| **Security** | Known vulnerabilities (ClawJacked, session isolation failures, 40K+ exposed instances) | Pattern-based approval + smart LLM screening | Pattern-based approval + smart LLM screening (same as Hermes) |
| **Architecture** | Node.js Gateway (hub-and-spoke) | Python agent-first | Python agent-first (same as Hermes) |

### The Honest Take

- **OpenClaw** has the best multi-platform coverage (20+ adapters) and a mature gateway architecture, but **zero learning capability** — every skill must be hand-written, and its security track record is concerning.
- **Hermes** added autonomous skill creation and a background review loop — real progress over OpenClaw — but the review is **blind** (same cost whether there are 10 corrections or zero) and memory is **flat** (one 2.2K file for everything).
- **Zorro** keeps everything Hermes does well (tools, skills, session search, any-model) and rebuilds the memory layer: **signal detection → smart triggering → domain knowledge → distill compression → session lifecycle**.

---

## What Zorro Does Differently (In Detail)

### Signal-Driven Memory (not blind review)

Hermes reviews the conversation every N turns with a generic prompt: *"did the user reveal preferences?"* — whether or not anything happened.

Zorro runs **zero-cost regex detection on every turn** (8 signal types, bilingual EN/ZH), accumulates signals with confidence levels, and triggers review **only when there's something to review**:

| Trigger | Hermes | Zorro |
|---------|--------|-------|
| Fixed interval (every 10 turns) | Yes | Yes (baseline) |
| 2+ high-confidence learning signals | No | **Yes** — early trigger |
| User frustration detected | No | **Yes** — immediate review |
| Nothing detected in 10 turns | Wastes an API call anyway | Skips review, saves money |

The review agent doesn't read blindly — it receives **pre-filtered signals** with type and confidence:

```
Detected Signals:
- [correction][high] User said: "don't mock the database"
- [method_discovery][medium] Agent changed strategy after 3 failed attempts
```

This makes the review more precise and the resulting memory writes more relevant.

### Domain-Partitioned Knowledge (not a flat text file)

Hermes stores everything in one 2,200-character file. When it's full, the agent has to manually merge or delete entries.

Zorro organizes knowledge **by domain** — each domain gets its own experience library with structured entries:

```
~/.zorro/knowledge/
├── _general/lessons.md      # Cross-domain (G1, G2, ...)
├── product/lessons.md       # Product design (P1, P2, ...)
├── engineering/lessons.md   # Engineering (E1, E2, ...)
└── growth/lessons.md        # Growth/marketing (H1, H2, ...)
```

Each entry is structured: `code | lesson | source | scenario | keywords`. The agent searches the relevant domain first, then falls back to general — not a linear scan of a flat file.

### Distill Compression (not mechanical truncation)

When a tool returns 50,000+ characters, Hermes cuts the middle and keeps head/tail. What if the answer was in the middle?

Zorro tries **task-aware compression first**: it sends the output to a cheap auxiliary model (Gemini Flash, ~$0.001) with the agent's current task as context, and asks it to extract only the relevant information. Two quality gates prevent degradation:

- If compressed output is ≥80% of input → compression failed → fall back to head/tail
- If output looks like meta-commentary ("here is a summary") → rejected → fall back

When it works (and it usually does), 50K chars becomes 5K chars of pure signal. When it doesn't, you get the same head/tail truncation Hermes uses. No downside.

### Session Lifecycle (not just "while True: chat()")

Hermes has no concept of session boundaries. When a conversation ends, everything is in the database but nothing is summarized or checked.

Zorro writes a **structured session summary** at the end of every conversation:

```markdown
## Session Summary — 2026-04-14 15:30
Turns: 23
First request: "Debug the authentication flow"

## Detected Learning Signals
- [correction][high] User corrected approach to token refresh
- [method_discovery][medium] Agent found workaround for CORS issue

## Closing Checklist
- ✅ 2 learning signals detected
```

### Soul System (not "be helpful and direct")

Hermes has a one-paragraph identity: *"You are Hermes Agent, an intelligent AI assistant... You are helpful, knowledgeable, and direct."*

Zorro has a **SOUL.md** — a full identity document with principles, memory protocol, skill protocol, and voice guidelines. It defines who the agent IS, not just what it does. Users can replace `~/.zorro/SOUL.md` to create a completely different agent personality.

---

## Everything Else (Inherited from Hermes, Working as-Is)

Zorro isn't a rewrite — it's Hermes with a better brain. Everything below works exactly as it does in Hermes:

<table>
<tr><td><b>Full TUI</b></td><td>prompt_toolkit-based terminal UI with multiline editing, slash commands, tab completion, streaming output, interrupt handling, and conversation branching.</td></tr>
<tr><td><b>18 Platform Adapters</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, iMessage, Microsoft Teams, WeChat, WeCom, Feishu, DingTalk, Matrix, Mattermost, Email, SMS, Home Assistant, API Server, Webhooks.</td></tr>
<tr><td><b>100+ Tools</b></td><td>Terminal, file operations, web search, browser automation, code execution, vision, TTS, image generation, MCP servers.</td></tr>
<tr><td><b>Skills System</b></td><td>YAML+Markdown procedural knowledge. Agent creates skills from experience, loads them by task relevance, patches them when outdated. Skills Hub for community sharing.</td></tr>
<tr><td><b>Session Search</b></td><td>FTS5 full-text search across all past conversations with LLM-powered summarization. The agent can recall any past interaction.</td></tr>
<tr><td><b>Any Model</b></td><td>OpenRouter (200+ models), OpenAI, Anthropic, Google Gemini, z.ai/GLM, Kimi, MiniMax, Mistral, Ollama, or any OpenAI-compatible endpoint. Switch with <code>zorro model</code>.</td></tr>
<tr><td><b>Cron Scheduling</b></td><td>Natural-language scheduled tasks with delivery to any platform. Daily reports, nightly backups, weekly audits.</td></tr>
<tr><td><b>Subagent Delegation</b></td><td>Spawn isolated child agents for parallel workstreams. Code execution via RPC for zero-context-cost tool chains.</td></tr>
<tr><td><b>6 Terminal Backends</b></td><td>Local, Docker, SSH, Daytona, Singularity, Modal. Serverless options hibernate when idle.</td></tr>
<tr><td><b>Security</b></td><td>Pattern-based dangerous command detection, smart LLM approval, DM pairing for messaging platforms, secret redaction in logs.</td></tr>
</table>

---

## Quick Start

```bash
git clone https://github.com/user/zorro-agent.git
cd zorro-agent
pip install -e ".[all]"
zorro setup    # Configure provider + model + API key
zorro          # Start chatting
```

## CLI Commands

```
zorro                # Interactive chat
zorro setup          # Setup wizard
zorro model          # Switch model (interactive picker)
zorro gateway        # Run multi-platform gateway
zorro status         # Show configuration status
zorro doctor         # Diagnose issues
```

## Architecture

```
~/.zorro/
├── SOUL.md                     # Agent identity and principles
├── config.yaml                 # Configuration
├── .env                        # API keys
├── state.db                    # Session storage (SQLite + FTS5)
├── memories/
│   ├── MEMORY.md               # Working memory (~2200 chars, auto-compacted)
│   └── USER.md                 # User profile (~1375 chars)
├── knowledge/                  # Domain-partitioned experience library
│   ├── _general/lessons.md     # Cross-domain lessons (G-codes)
│   ├── product/lessons.md      # Product domain (P-codes)
│   ├── engineering/lessons.md  # Engineering domain (E-codes)
│   └── .../lessons.md          # Extensible per domain
├── skills/                     # Procedural knowledge
│   └── <skill-name>/
│       └── SKILL.md            # YAML frontmatter + instructions
├── sessions/                   # Structured session summaries
│   └── 20260414-1530.md
└── logs/
```

## Memory Architecture

```
Every turn (zero cost):
  signal_detector → 8 types × bilingual → session_state.learning_candidates

Triggered by signals (not by timer):
  background_review → reads pre-filtered signals → writes memory/skills

Large tool outputs:
  distill → auxiliary LLM compression → 50K chars → 5K chars of signal

Session end:
  session_lifecycle → structured summary → ~/.zorro/sessions/
```

## Documentation

| Guide | Description |
|-------|-------------|
| [docs/imessage.md](docs/imessage.md) | iMessage setup via BlueBubbles (macOS required) |
| [docs/teams.md](docs/teams.md) | Microsoft Teams setup via Azure Bot Framework |

## License

MIT
