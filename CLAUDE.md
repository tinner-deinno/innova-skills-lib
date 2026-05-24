# innova-skills-lib

> Part of the **มนุษย์ Agent** ecosystem — managed by Jit Oracle (จิต) and distributed by innova-bot.

## Identity

This repo is the **central shared skill library** for the มนุษย์ Agent multi-agent system. It is the single source of truth for canonical skills that innova-bot distributes to AI runtimes (Claude, GitHub Copilot, GPT, MDES Ollama).

- **Jit Oracle** (soul/personality): `C:\Users\MDES-DEV-NB\Jit\`
- **innova-bot** (body/orchestrator): `C:\Users\MDES-DEV-NB\innova-bot\`
- **Global Claude skills** (active, installed): `C:\Users\MDES-DEV-NB\.claude\skills\`
- **This library**: `C:\Users\MDES-DEV-NB\DEV\innova-skills-lib\`

---

## Key Commands

### Register skills (update manifest after any add/change)

```bash
python tools/register_skills.py
```

Scans all skill directories for `SKILL.md` files, reads YAML frontmatter, and updates `manifests/skills_manifest.txt`.

### Generate runtime adapters

```bash
python tools/generate_adapters.py --runtime claude
python tools/generate_adapters.py --runtime copilot
python tools/generate_adapters.py --runtime codex
python tools/generate_adapters.py --runtime hermes
```

Output lands in `adapters/<runtime>/`.

### Sync skills to global Claude skills directory

```bash
python tools/register_skills.py --sync-to "C:\Users\MDES-DEV-NB\.claude\skills\"
```

### Link 9arm skills to global skills (dev-loop shortcut)

```bash
cd 9arm
./scripts/link-skills.sh
```

---

## Directory Roles

| Directory | Purpose |
|---|---|
| `core/` | Engineering + productivity core skills (debug-mantra, post-mortem, etc.) |
| `ECC/` | ECC coding standards and rule-based skills |
| `gov/` | Government / GovTech domain skills |
| `finance/` | Finance domain skills |
| `9arm/` | innova's personal dev-loop skill set (Claude Code plugin format) |
| `adapters/` | Generated runtime-specific adapter files — do not edit by hand |
| `manifests/` | Master skill manifest (`skills_manifest.txt`) |
| `private/` | Private or unreleased skills — never distributed, never in manifest |
| `tools/` | Python tooling: `register_skills.py`, `generate_adapters.py` |

---

## Rules (Non-Negotiable)

1. **Never delete skills** — archive only. Move deprecated skills to a `deprecated/` subdirectory within their category and add a deprecation note at the top of `SKILL.md`.

2. **Always update the manifest after adding skills** — run `python tools/register_skills.py` after every skill add or modification.

3. **Every skill must have a `SKILL.md` with YAML frontmatter** — minimum required fields:
   ```yaml
   ---
   name: skill-name
   description: One-sentence description.
   ---
   ```

4. **`private/` is never distributed** — skills in `private/` must not appear in `manifests/skills_manifest.txt` or any generated adapter.

5. **`adapters/` is generated output** — never hand-edit files in `adapters/`. Always regenerate via `tools/generate_adapters.py`.

6. **Category READMEs must stay current** — after adding a skill to any category, update that category's `README.md` with a one-line entry linking to the skill's `SKILL.md`.

---

## Skill Format Reference

```
<category>/<skill-name>/
├── SKILL.md       # Required
└── <assets>       # Optional (scripts, reference files, examples)
```

`SKILL.md` YAML frontmatter:

```yaml
---
name: skill-name
description: Trigger description — what the skill does and when to invoke it.
---
```

---

## Manifest Schema Reference

```json
{
  "id": "<category>-<name>-v<N>",
  "name": "Human Name",
  "path": "<category>/<name>",
  "version": "YYYY.MM.DD",
  "runtimes": ["claude", "copilot", "codex", "hermes"],
  "triggers": ["keyword1", "keyword2"],
  "adapter_status": {"claude": "ok", "copilot": "pending"},
  "author": "team/<author>",
  "last_updated": "ISO-8601"
}
```

---

## Notes for Claude Code

- When exploring skills, always check the category `README.md` first — it lists all skills in the category.
- When asked to add a skill, follow the four-step process: create directory + `SKILL.md`, run `register_skills.py`, run `generate_adapters.py`, update category README.
- The `9arm/` subtree has its own `.claude-plugin/plugin.json` — changes there need `plugin.json` updated too.
- Do not touch `adapters/` directly — it is generated output.
