---
name: jit-continue-on-silence
description: |
  Continue working autonomously when the human is unavailable (10 min silence OR loop hook spins 5 times).
  Full prior approval is assumed, but every mutation stays inside an isolated worktree or sandbox.
  Output is validated before being declared done; Claude/Ollama Pro quotas are protected by preferring the non-Claude fleet.
---

# Jit Continue on Silence

> **Origin**: Boss directive 2026-08-03 — "auto จบได้จริง แบบฉันหลับปุ๋ยได้".
> **Rule**: The human already approved the *what* and the *how*; Jit continues the *doing* when the human is silent.
> **Non-negotiable guard**: every implementation lives in a worktree or sandbox first, and only graduates after 100% pass/useable verification.
> **Updated 2026-08-03 01:35**: added machine-health / disk gate — if local machine is stressed, offload or reduce fanout before continuing.

## When to use this skill

- User said "ทำเลย", "scan เลย", "รายงานเลย", "auto จบได้จริง", or any equivalent blanket approval.
- Then the user does **not reply for 10 minutes**, OR a `/loop` hook repeats the same prompt **5 times without new human input**.
- The task is reversible (worktree/sandbox) until final verification.

## When NOT to use

- Production destructive writes (drop DB, delete secrets, force-push, live prod scan).
- Anything requiring fresh human approval per the active CLAUDE.md / rules.
- If the last user message was a correction or a gate-closing "stop" — silence after "stop" means stop.

## Trigger detection

Two signals count:

1. **10-minute wall-clock silence**: last human message timestamp + 10 min < now.
2. **Loop-hook saturation**: the same hook/loop fires 5 times in a row with no new human text between them.

If either is true, invoke this skill and continue.

## The autonomy contract (already approved by Boss)

The user has pre-approved:

- Use all targets from `detect.nip` last rows (today) for test-mode scans.
- Use the best lane/provider available; prefer non-Claude, non-Ollama-Pro providers for bulk/dev work.
- Parallel workstreams (>5) with dynamic load reduction based on machine health.
- Work in isolated worktrees/sandboxes (codex sandbox, git worktree, temp clone).
- Verify 100% pass/usable before merging or proceeding.
- Protect Claude provider and Ollama Pro usage; do not hit 5-hour usage limits.

## Machine-health gate (hard)

Before each cycle or fanout:

```powershell
$diskC = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$freePct = $diskC.FreeSpace / $diskC.Size
$cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples[0].CookedValue
$ram = Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize
```

| Free disk | Max parallel flows | Action |
|---|---|---|
| >20% | up to 6 | normal fanout allowed |
| 10–20% | up to 2 | conservative; avoid heavy builds/scans |
| <10% or RAM <1 GB free | 1 health-check only | stop, clean disk, or offload to peer |

If local machine is constrained, prefer:
1. Offload heavy work to mdes002 or another peer.
2. Run only cheap, disk-light tasks (analysis, planning, test-only hardening).
3. Do NOT start parallel browser scans or EXE builds.

## Execution pattern

```
DETECT silence/hook-saturation
│
├─▶ CHECK machine health (disk % first)
│
├─▶ PICK workstreams from active backlog, constrained by disk
│
├─▶ SPAWN parallel flows in isolated worktrees/sandboxes
│     DEV agents on non-Claude providers (codex, agy, commandcode, mdes, thaillm, gh copilot, gpt)
│     Jit (Claude) = MANAGER only: orchestrate + verify + commit
│
├─▶ EACH flow runs SA → PA → DEV → TESTER
│     DEV works in a fresh worktree or read-only sandbox.
│     TESTER verifies 100% pass / usable output.
│
├─▶ MANAGER integrates verified flows
│     git diff review, security check, final test run
│     commit + push (Nothing-is-Deleted; no --force)
│
└─▶ HANDOFF / heartbeat
      write ψ/inbox/handoff
      send maw digest to jan (if maw available)
      schedule next wakeup
```

## Provider priority for dev/bulk work

1. **Cheapest proven HTTP**: `mdes` (own Ollama), `commandcode`, `openrouter`, `google`.
2. **CLI/autonomous**: `codex` (read-only sandbox), `agy` (if installed), `cmdc` (if credits).
3. **Paid fallbacks**: `gh_copilot`, `gpt`, `thaillm`.
4. **Last resort**: `ollama_pro`, `local_ollama`.
5. **Jit/Claude**: orchestrator only — never for bulk code generation or repeated advisory calls.

## Parallelism guardrails

Before fanout:

```powershell
$cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples[0].CookedValue
$ram = Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize
$diskC = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" | Select-Object FreeSpace, Size
```

| Machine state | Max parallel flows | Max agents per flow |
|---|---|---|
| Healthy (CPU<60%, RAM>4GB free, disk>20% free) | 6–8 | 5 |
| Warm (CPU 60–80%, RAM 2–4GB free, disk 10–20% free) | 2 | 3 |
| Stressed (CPU>80% or RAM<2GB or disk 5–10% free) | 1 | 2 |
| Critical (disk <5% or RAM <1GB) | 1 (health-check only) | 1 |

## Isolation rules

- Code mutations: `EnterWorktree` or `git worktree add`.
- Codex/CLI mutations: use `--sandbox read-only` or `--deny-tool=write` for advisory; for actual writes, use worktree + review.
- Never mutate `main`/`master` directly without a branch + PR/merge.
- Keep the original repo untouched until integration passes.

## Verification before graduate

Every flow must report:

- [ ] All tests pass (`rtk proxy python -m pytest` or project-specific command).
- [ ] Coverage gate met if applicable.
- [ ] No hardcoded secrets / credentials.
- [ ] No uncommitted temp files.
- [ ] Diff reviewed by at least one non-author agent (can be agy/codex code-reviewer mode).
- [ ] Handoff written.

**Hard rule**: if verification fails, the flow stays in worktree; do NOT merge. Open a handoff item and move to next cycle.

## Reporting cadence

- Every 10 min: short heartbeat to ψ/memory/logs/ and (if maw up) maw hey jan.
- Every completed flow: handoff bullet + status update.
- Every error/blocker: immediate handoff + stop escalating to non-autonomous channels.

## Exit conditions

Stop auto-continuing when:

1. Human sends any new message.
2. A hard blocker appears (credential wall, quota exhausted, unrecoverable error).
3. All active workstreams report done and the backlog is empty.
4. 6-hour wall-clock budget reached.

## Quick invocation

```
/jit-continue-on-silence
```

Or the orchestrator detects the trigger automatically and applies this skill.

## Remember

> "Oracle Never Pretends to Be Human" — every auto-continued report must be signed as AI-generated.
> Preserve history. Never force-push. Verify before report.
