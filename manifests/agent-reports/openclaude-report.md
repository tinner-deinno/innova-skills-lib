# OpenClaude Agent Report

**Agent**: OpenClaude (limbs/openclaude.sh)
**Date**: 2026-05-24
**Task**: Analyze architecture for a central skills library shared between multiple AI agents

---

## Invocation

```bash
bash "C:\Users\MDES-DEV-NB\Jit\limbs\openclaude.sh" ask \
  "What is the best architecture for a central skills library shared between multiple AI agents \
  (Claude, GPT, Copilot, Ollama)? Answer in 3-5 sentences."
```

---

## Result

**Status**: success

**Provider used**: MDES Ollama Cloud (`https://ollama.mdes-innova.online/v1`)
**Model**: `gemma4:26b`
**Source**: Default profile from `~/.claude/.openclaude-profile.json`

**Time**: ~36.2 seconds (36,246 ms)

**Tokens**: not reported (provider does not expose token counts via this interface)

---

## Response

> The best architecture is a **decoupled, API-first centralized repository** accessible via standard protocols (REST or GraphQL) that serves structured data such as JSON-schema or Markdown. By storing skills as modular, versioned assets in a single source of truth (like a Git-backed database), you ensure that various agents—regardless of their underlying LLM—can fetch, parse, and execute the same logic. This approach should utilize a **"Router-Executor" pattern**, where a lightweight gateway handles authentication and agent-specific context injection, while the core library remains agnostic of the calling client.

---

## Key Architecture Recommendations (Extracted)

1. **Decoupled API-first design** — REST or GraphQL endpoint, not direct file access
2. **Standard data format** — JSON-schema or Markdown for cross-agent compatibility
3. **Single source of truth** — Git-backed database with versioned, modular skill assets
4. **Router-Executor pattern** — Gateway handles auth + context injection; library stays client-agnostic
5. **LLM-agnostic core** — Skills work regardless of the calling agent (Claude, GPT, Copilot, Ollama)

---

## Provider Config

From `~/.claude/.openclaude-profile.json`:

```json
{
  "profile": "openai",
  "env": {
    "CLAUDE_CODE_USE_OPENAI": "1",
    "OPENAI_BASE_URL": "https://ollama.mdes-innova.online/v1",
    "OPENAI_API_KEY": "9e34679b9d60d8b984005ec46508579c",
    "OPENAI_MODEL": "gemma4:26b"
  }
}
```

**Note**: The profile name is `"openai"` but it routes to MDES Ollama (custom OpenAI-compatible endpoint). The `CLAUDE_CODE_USE_OPENAI=1` flag enables the OpenAI-compatible API path in Claude Code.

---

## Notes

- `openclaude` binary found at `/d/AppData/Roaming/npm/openclaude`
- The shell script (`limbs/openclaude.sh`) sets provider env vars then calls `openclaude -p "<prompt>"`
- Default provider is `mdes` (MDES Ollama Cloud) with `gemma4:26b`
- Token counts are not surfaced by this provider's API response
- Response time was ~36s, reflecting a large 26B model on a remote inference endpoint
