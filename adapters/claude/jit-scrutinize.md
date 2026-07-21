<!-- skill-id: jit-scrutinize -->
<!-- source-path: jit-scrutinize -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/jit-scrutinize/SKILL.md -->
<!-- runtime: claude -->

# jit-scrutinize

Every-30-minutes self-correcting loop for the Jit multi-agent system.

## Purpose
Look back 1 hour across Jit, URL-Checker, and innova-bot; detect mistakes, stale state, or unclosed work; write a retrospective; emit a correction task to the responsible organ; verify the correction closes.

## Triggers
- Cron/scheduler every 30 minutes
- On uncaught error / non-zero exit in an organ run
- Bus message subjects: `alert:mistake`, `report:failure`
- After commit when tests fail or diff touches `core/`, `limbs/`, `network/`

## Inputs
- Git log/status of last 1 hour
- Test output artifacts
- Bus messages: `/tmp/manusat-bus/<agent>/`
- Hermes bridge: `network/inbox/hermes/`
- Provider status snapshot
- `ψ/memory/retrospectives/`

## Outputs
- `ψ/memory/retrospectives/YYYY-MM-DD_mistake-<hash>.md`
- Bus message `task:correct` to responsible organ
- `logs/scrutinize-report.json`
- Broadcast `learn:pattern` if generic

## Self-correct loop
1. Detect — tail logs, parse tests, scan bus alerts
2. Remember — write retrospective + pattern bank entry
3. Correct — emit `task:correct` to responsible organ
4. Verify — re-run test/command
5. Close — mark pattern verified or escalate `alert:stuck-correction` to soma

## Runtime adaptation
- Healthy: `mdes_ollama` (unlimited) for analysis
- Credit-limited: `cmdc`, `agy` only for high-confidence fix generation
- Fallback: queue corrections in `network/inbox/hermes/queued-corrections/` when providers offline
- Degraded mode: do not spawn remote agents; update local memory + bus only

## Commands
- `python -m jit_scrutinize.scrutinize --since 1h` — run once
- `python -m jit_scrutinize.scrutinize --daemon --interval 1800` — run loop
