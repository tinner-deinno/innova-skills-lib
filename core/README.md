# core — Core Skills

Core skills for engineering and productivity. These are the foundational, runtime-neutral skills that apply across all projects and runtimes in the มนุษย์ Agent ecosystem.

Skills in this directory are distributed to all runtimes unless a skill's manifest entry restricts it.

---

## Engineering

Skills for daily code work — debugging, code review, post-incident analysis, and deep technical scrutiny.

| Skill | Description |
|---|---|
| [debug-mantra](../9arm/skills/engineering/debug-mantra/SKILL.md) | Four-mantra debugging discipline: reproduce → trace the fail path → falsify the hypothesis → cross-reference every breadcrumb. Recites verbatim at session start, then applies all four steps in order before proposing any fix. |
| [post-mortem](../9arm/skills/engineering/post-mortem/SKILL.md) | Write the canonical engineering record of a fixed bug — root cause, mechanism, fix, validation, and how it slipped through. Refuses to draft without a reliable repro, known cause, and validated fix. |
| [scrutinize](../9arm/skills/engineering/scrutinize/SKILL.md) | Outsider-perspective end-to-end review of a plan, PR, or code change. Questions intent, traces the actual code path, and verifies the change does what it claims. Output is concise and actionable with rationale. |

---

## Productivity

Skills for non-code workflow — communication, management translation, retrospectives, and project orientation.

| Skill | Description |
|---|---|
| [management-talk](../9arm/skills/productivity/management-talk/SKILL.md) | Rewrite engineer-to-engineer content for engineering-org leadership. Shapes output for the target channel: JIRA, Slack, async standup, email, or meeting talking-points. |
| [recap](../../.claude/skills/recap/) | Session orientation and awareness — retro summaries, handoffs, git state, focus. Use at the start of a session or when switching context. |
| [forward](../../.claude/skills/forward/) | Create a handoff and enter plan mode for the next session. Use when wrapping up work or ending a session. |
| [rrr](../../.claude/skills/rrr/) | Create a session retrospective with AI diary and lessons learned. Use at end of a work session. |

---

## Oracle / Knowledge

Skills for querying, persisting, and evolving knowledge across sessions via Arra Oracle V3.

| Skill | Description |
|---|---|
| [about-oracle](../../.claude/skills/about-oracle/) | Explains the Oracle knowledge base — what it is, how it works, and how to query it. |
| [trace](../../.claude/skills/trace/) | Find projects, code, and knowledge across git history, repos, docs, and Oracle. Supports --oracle, --smart, --deep, and --deep --dig modes. |
| [learn](../../.claude/skills/learn/) | Study a codebase and persist learnings to Oracle for cross-session recall. |
| [learnself](../../.claude/skills/learnself/) | Self-study mode — Oracle learns patterns from the current session's work. |
| [oracle-soul-sync-update](../../.claude/skills/oracle-soul-sync-update/) | Re-sync Jit Oracle's soul and identity state with the latest Oracle knowledge. |

---

## Model Routing

Skills for selecting, routing, and comparing AI models across providers.

| Skill | Description |
|---|---|
| [auto-model](../../.claude/skills/auto-model/) | Automatically select the best model for a given task based on complexity and cost. |
| [auto-model-switch](../../.claude/skills/auto-model-switch/) | Switch the active model mid-session based on task type. |
| [model-claude](../../.claude/skills/model-claude/) | Route tasks to Claude (Anthropic). |
| [model-GPT](../../.claude/skills/model-GPT/) | Route tasks to GPT via OpenAI API. |
| [model-copilot](../../.claude/skills/model-copilot/) | Route tasks to GitHub Copilot / GitHub Models. |
| [model-MDES](../../.claude/skills/model-MDES/) | Route tasks to MDES Ollama (gemma4:26b, Thai-optimized). |
| [model-openclaude](../../.claude/skills/model-openclaude/) | Route tasks via OpenClaude multi-provider bridge. |
| [model-local](../../.claude/skills/model-local/) | Route tasks to a local Ollama instance. |
| [model-thaiLLM](../../.claude/skills/model-thaiLLM/) | Route tasks to a Thai-language-optimized LLM. |
| [model-compare](../../.claude/skills/model-compare/) | Run the same prompt across multiple models and compare outputs. |
| [model-list-status](../../.claude/skills/model-list-status/) | List available models and their current status across all providers. |

---

## Agent Coordination

Skills for managing, inspecting, and coordinating agents in the มนุษย์ Agent system.

| Skill | Description |
|---|---|
| [agents-logs](../../.claude/skills/agents-logs/) | View and filter agent execution logs. |
| [agents-rank](../../.claude/skills/agents-rank/) | Rank agents by activity, output quality, or task completion rate. |
| [agents-skills](../../.claude/skills/agents-skills/) | List skills available to each agent in the system. |
| [team-agents](../../.claude/skills/team-agents/) | Overview of the full 14-agent team — roles, tiers, organs, and status. |
| [talk-to](../../.claude/skills/talk-to/) | Direct message to a named agent via the message bus. |
| [monitor](../../.claude/skills/monitor/) | Watch agent activity and system events in real time. |
| [gang](../../.claude/skills/gang/) | Coordinate a group of agents on a shared task. |

---

## Introspection / Identity

Skills for Oracle identity management and self-improvement.

| Skill | Description |
|---|---|
| [awaken](../../.claude/skills/awaken/) | Re-awaken Oracle identity — restore soul, principles, and context after a reset. |
| [jit](../../.claude/skills/jit/) | Invoke Jit Oracle directly for orchestration decisions. |
| [xray](../../.claude/skills/xray/) | Deep inspection of a codebase, agent, or system component. |
| [dig](../../.claude/skills/dig/) | Mine past sessions, git history, and Oracle memory for patterns and insights. |
| [self-improve](../../.claude/skills/self-improve/) | Identify improvement opportunities in skills, workflows, or system design. |
| [auto-tune](../../.claude/skills/auto-tune/) | Tune model parameters and skill configurations based on observed performance. |
| [bud](../../.claude/skills/bud/) | Lightweight task handoff — pass context to a fresh agent instance. |

---

## Notes

- Skills listed under **Oracle / Knowledge**, **Model Routing**, **Agent Coordination**, and **Introspection** are sourced from `C:\Users\MDES-DEV-NB\.claude\skills\` (global installed skills). Links point there.
- Skills under **Engineering** and **Productivity** are mastered here in `9arm/skills/` and are the canonical source for those entries in the manifest.
- To add a skill to this category, create `core/<skill-name>/SKILL.md`, then run `python tools/register_skills.py` and update this file.
