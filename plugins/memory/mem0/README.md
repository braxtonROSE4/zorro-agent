# Mem0 Memory Provider

Server-side LLM fact extraction with semantic search, reranking, and automatic deduplication.

## Requirements

- `pip install mem0ai`
- Mem0 API key from [app.mem0.ai](https://app.mem0.ai)

## Setup

```bash
zorro memory setup    # select "mem0"
```

Or manually:
```bash
zorro config set memory.provider mem0
echo "MEM0_API_KEY=your-key" >> ~/.zorro/.env
```

## Config

Config file: `$ZORRO_HOME/mem0.json`

| Key | Default | Description |
|-----|---------|-------------|
| `user_id` | `zorro-user` | User identifier on Mem0 |
| `agent_id` | `zorro` | Agent identifier |
| `rerank` | `true` | Enable reranking for recall |

## Tools

| Tool | Description |
|------|-------------|
| `mem0_profile` | All stored memories about the user |
| `mem0_search` | Semantic search with optional reranking |
| `mem0_conclude` | Store a fact verbatim (no LLM extraction) |
