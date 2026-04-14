# Zorro Agent

**CLI Agent framework with persistent memory, skills, and tool calling.**

Forked from [Hermes Agent](https://github.com/NousResearch/hermes-agent) v0.8.0 by Brax.

## Features

- **Persistent Memory** — MEMORY.md / USER.md + pluggable memory providers (Honcho, Mem0, etc.)
- **Skills System** — YAML+Markdown procedural knowledge, agent-created, self-improving
- **100+ Tools** — Terminal, file ops, web search, browser, code execution, vision, TTS
- **Multi-Platform Gateway** — Telegram, Discord, Slack, WhatsApp, Signal, iMessage, Microsoft Teams, WeChat, Feishu, DingTalk, Matrix, and more
- **Session Search** — FTS5 full-text search across all past conversations
- **MCP Support** — Model Context Protocol server integration
- **Any Model** — OpenRouter, OpenAI, Anthropic, local models, or your own endpoint

## Quick Start

```bash
# Clone
git clone https://github.com/user/zorro-agent.git
cd zorro-agent

# Install
pip install -e .

# Run
zorro
```

## CLI Commands

```
zorro                    # Interactive chat (default)
zorro chat               # Interactive chat
zorro setup              # Interactive setup wizard
zorro gateway            # Run multi-platform gateway
zorro status             # Show status
zorro doctor             # Check configuration
zorro model              # Switch model
```

## Architecture

```
~/.zorro/
├── config.yaml          # Configuration
├── .env                 # API keys
├── state.db             # Session storage (SQLite + FTS5)
├── memories/
│   ├── MEMORY.md        # Agent's personal notes (~2200 chars)
│   └── USER.md          # User profile (~1375 chars)
├── skills/              # Persistent procedural knowledge
│   └── <skill-name>/
│       └── SKILL.md     # YAML frontmatter + instructions
└── logs/
```

## License

MIT
