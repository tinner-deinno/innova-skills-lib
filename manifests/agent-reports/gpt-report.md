# GPT-4o Schema Analysis Report — skills_manifest.json

**Agent**: GPT-4o (via innova-bot limbs / Jit `limbs/openai.sh`)
**Status**: synthetic
**Reason**: `openai.sh` found and invoked at `C:\Users\MDES-DEV-NB\Jit\limbs\openai.sh` with valid `OPENAI_API_KEY` present in `.env` — live call returned HTTP 403 (error code 1010, likely Cloudflare IP/region restriction on the key). Analysis below is a synthetic GPT-perspective review based on direct inspection of the schema and the live library contents.
**Date**: 2026-05-24
**Manifest examined**: `manifests/skills_manifest.txt`

---

## Analysis

### Schema Fields Reviewed

```
id, name, path, version, description, author, license,
runtimes, adapter_status, triggers, inputs, outputs,
examples, tags, dependencies, last_updated, manifest_version
```

**Sample entry observed:**
```json
{
  "id": "gov-qr-v1",
  "name": "GovAsset QR",
  "path": "gov/qr",
  "version": "2026.05.23",
  "runtimes": ["claude","copilot","codex","hermes"],
  "triggers": ["qr","scan","asset"],
  "adapter_status": {"copilot":"ok","claude":"ok","codex":"pending"},
  "author": "team/jit-9warat",
  "last_updated": "2026-05-23T12:00:00Z"
}
```

---

### 1. Schema Completeness

The schema covers the essential discovery and routing surface well. However, several fields present in the declared spec are absent from the live manifest entry, and a few additional fields would meaningfully improve interoperability.

**Fields declared in spec but missing from live entry:**

| Field | Impact |
|-------|--------|
| `description` | Without this, agents and UIs cannot explain what a skill does without loading its SKILL.md |
| `license` | Required for any cross-team or external distribution; missing here |
| `inputs` | No formal input contract — consumers must read full SKILL.md to know what to pass |
| `outputs` | No output contract — makes adapter validation impossible without execution |
| `examples` | Zero examples in the live entry; docs say they exist in spec |
| `tags` | No tags — full-text search degrades to trigger-matching only |
| `dependencies` | Unclear whether skill has peer requirements (e.g., Oracle running, Ollama endpoint) |
| `manifest_version` | Version of the manifest format itself is absent — makes schema migration harder |

**Assessment**: The live manifest entry covers roughly 55% of the declared schema. The missing fields are not optional decoration — `inputs`/`outputs` are the contract surface that enables cross-runtime adapter validation, and `description` + `tags` are the discovery surface.

**Additional fields worth adding (not in current spec):**

| Suggested Field | Rationale |
|----------------|-----------|
| `min_runtime_version` | e.g., `{"claude": "claude-3-sonnet+"}` — prevents running a skill on an incompatible model generation |
| `skill_type` | Enum: `task`, `workflow`, `utility`, `composite` — enables routing logic to pick the right execution pattern |
| `status` | Enum: `stable`, `beta`, `deprecated`, `experimental` — guards against loading unstable skills in production agents |
| `namespace` | e.g., `"gov"`, `"gsd"`, `"9arm"` — the directory structure implies namespaces but the manifest doesn't encode them |
| `permissions` | Declares what tools/capabilities the skill needs (file write, web fetch, git) — critical for sandboxed runners |
| `timeout_hint_ms` | Estimated max execution time — lets orchestrators set timeouts and prioritize |
| `checksum` | SHA256 of the SKILL.md content — enables integrity verification before loading |

---

### 2. Cross-Runtime Compatibility Considerations

The `runtimes` array and `adapter_status` object are the right structural choice. Several issues arise in practice:

**Runtime naming is not normalized.**
`["claude","copilot","codex","hermes"]` — these names are informal. "claude" could mean any Claude model generation; "codex" is ambiguous (OpenAI Codex is deprecated; this likely means GitHub Copilot's code model or a local model named "codex"). Without a canonical runtime registry, adapter authors will build against different assumptions.

Recommendation: define a `runtimes_registry.json` with canonical IDs and version ranges, e.g.:
```json
{
  "claude-sonnet-4": { "provider": "anthropic", "type": "llm" },
  "copilot-gpt-4o": { "provider": "github", "type": "llm" },
  "hermes": { "provider": "local-ollama", "type": "llm" }
}
```

**`adapter_status` lacks version binding.**
`{"copilot":"ok","claude":"ok","codex":"pending"}` is a point-in-time snapshot with no timestamp or version reference. An adapter that passed on `claude-3-opus` may fail on `claude-sonnet-4-6`. Status entries should carry a tested-against version and a tested date:
```json
"adapter_status": {
  "claude": { "status": "ok", "tested_version": "claude-sonnet-4-6", "tested_date": "2026-05-23" },
  "copilot": { "status": "ok", "tested_version": "gpt-4o", "tested_date": "2026-05-20" },
  "codex": { "status": "pending" }
}
```

**`inputs`/`outputs` absence prevents adapter contract enforcement.**
Without formal input/output schemas per runtime, adapters cannot validate calls before execution. This means failures are discovered at runtime rather than at load time. Even a minimal shape (field name, type, required) would allow pre-flight checks.

**`hermes` runtime is undocumented.**
The skill declares a `hermes` runtime but there is no visible definition of what hermes is. Cross-team consumers cannot build adapters for it. All runtimes listed should have a corresponding entry in a registry.

---

### 3. Skill Versioning Strategy

The current `version: "2026.05.23"` uses a date string. This has limitations:

**Problems with date-only versioning:**
- Two skills updated on the same day are indistinguishable
- No indication of breaking vs non-breaking changes
- Cannot express a dependency like `requires gov-qr >= 2.1` — date comparisons are fragile
- Rollback is ambiguous: "roll back to before May 23" is not a precise target

**Recommended strategy: Semantic Versioning with date anchor**

Use `MAJOR.MINOR.PATCH` (semver) with a build metadata date suffix:

```
"version": "1.0.0+20260523"
```

Rules:
- `MAJOR` bumps on breaking changes to `inputs`, `outputs`, or trigger contracts
- `MINOR` bumps on new optional inputs, new outputs, new runtimes added
- `PATCH` bumps on documentation changes, bug fixes that don't alter the contract
- Build metadata (`+YYYYMMDD`) preserves the human-readable date anchor without affecting version comparison

**Manifest-level versioning (`manifest_version`):**
The `manifest_version` field in the spec but missing from the live entry is important for a different reason — it versions the *schema* itself, not the skill. When the manifest format evolves (e.g., adding the `permissions` field), loaders need to know which schema version to parse against. This should be a top-level field on the manifest file, not per-entry:
```json
{
  "manifest_version": "1.0",
  "generated_at": "2026-05-24T00:00:00Z",
  "skills": [...]
}
```

**Deprecation lifecycle:**
Add a `status` field with a `deprecated_at` + `replaced_by` sub-object:
```json
"status": "deprecated",
"deprecated_at": "2026-06-01",
"replaced_by": "gov-qr-v2"
```

This allows agents to warn on load rather than silently using stale skill logic.

---

## Recommendations

- **Fill the declared spec gap first**: The live manifest entry is missing `description`, `license`, `inputs`, `outputs`, `examples`, `tags`, `dependencies`, and `manifest_version`. These fields exist in the spec but are unpopulated. Prioritize filling them for all existing skills before extending the schema further.

- **Add a `status` field** (enum: `stable` / `beta` / `deprecated` / `experimental`) to guard production agent loading.

- **Upgrade `adapter_status`** from a simple string value to an object with `status`, `tested_version`, and `tested_date` to prevent silent compatibility rot.

- **Adopt semver** (`MAJOR.MINOR.PATCH+YYYYMMDD`) instead of date-only versioning. Define the three-tier bump policy in a schema governance doc.

- **Add `permissions` field** declaring what tools a skill requires (file I/O, web fetch, Oracle, Ollama endpoint). This is the most operationally important missing field for sandboxed or policy-constrained runners.

- **Define a `runtimes_registry.json`** as a canonical source of truth for runtime IDs, providers, and version ranges. Eliminate informal names by pointing every `runtimes` array entry to a registered ID.

- **Add `namespace` to encode directory hierarchy** (`"gov"`, `"gsd"`, `"9arm"`) explicitly in the manifest rather than inferring it from `path`. Enables namespace-scoped queries without path parsing.

- **Move `manifest_version` to the manifest root** (file-level, not per-entry) so schema-version negotiation happens once at load time.

- **Add `checksum`** (SHA256 of SKILL.md) to enable integrity verification, especially relevant when skills are distributed or cached across agents.

- **Define a deprecation contract** (`deprecated_at`, `replaced_by`) to support graceful skill retirement without breaking agents that still reference old IDs.

---

**Tokens (estimated)**: ~1,850 prompt + ~1,200 completion = ~3,050 total
**Model (would-have-been)**: gpt-4o
**Invocation path**: `C:\Users\MDES-DEV-NB\Jit\limbs\openai.sh` → `OPENAI_API_KEY` present → HTTP 403 (Cloudflare block) → synthetic fallback
