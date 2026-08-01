# Jit Orchestrate — SA→PA→TESTER Workflow

> **Origin**: Session `2fddc76a` workflow `wv81iklcz` + Oracle Pattern ancestors (the-oracle-pattern, hermes-book-oracle, maw lifecycle).  
> **Philosophy**: Many bodies, one soul; evidence before claims; human as keeper.

## When to use this skill

- User says: "ทำ backlog ให้เสร็จ", "จัดหนัก", "fanout", "ให้ fleet ช่วย", "SA/PA/Tester"
- There are multiple independent workstreams (GitHub issues, `ψ/outbox` pending, modules to harden).
- Each workstream needs analysis → planning → implementation → verification.
- You need automatic resource monitoring and cleanup so the machine stays healthy.

## When NOT to use

- Single-file/one-line fixes (overhead too high).
- Work requiring production writes or irreversible actions (keep human approval gates).
- The user explicitly asked for a specific agent or direct execution without orchestration.

## Roles

| Role | Responsibility | Typical agent count | Output |
|---|---|---|---|
| **MANAGER** | You (main agent) + user. Define workstreams, scope, approval gates. | 1 | workstream list + final integration |
| **SA** | System Analyst. Read relevant paths, identify gaps/risks, produce spec. | 1 per flow | structured analysis (schema) |
| **PA** | Project Architect / Planner. Convert SA analysis into file changes + test strategy. | 1 per flow | implementation plan (schema) |
| **DEV** | Developer. Implement in isolated worktree, run tests, return results. | 1–3 per flow | changed files + test results |
| **TESTER** | QA. Verify completeness, run tests, give PASS/FAIL/CONDITIONAL verdict. | 1 per flow | verdict + gaps |

## Feedback loops

- **TESTER → DEV**: code-level bug or missing test
- **TESTER → PA**: plan incomplete / file missing
- **TESTER → SA**: spec does not match requirement / design gap
- **DEV → PA**: implementation blocked by design ambiguity
- **PA/SA → MANAGER**: scope conflict, risk, or approval needed

## Execution pattern

```
MANAGER defines workstreams
    │
    ▼
parallel flows (1 flow = 1 workstream)
    │
    ├── SA analyzes
    │
    ▼
    ├── PA plans
    │
    ▼
    ├── DEV implements (parallel 1–3 agents)
    │
    ▼
    └── TESTER verifies
    │
    ▼
MANAGER synthesizes → integrate → commit/push (human-gated)
```

## Resource guardrails

Before launching a large workflow:

1. **Check machine health** (PowerShell):
   ```powershell
   Get-CimInstance Win32_Processor | Select-Object LoadPercentage
   Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize
   Get-CimInstance Win32_LogicalDisk | Select-Object Caption, FreeSpace, Size
   ```
2. **Abort if**:
   - Free RAM < 1.5 GB
   - Any disk > 95% full
   - CPU already pinned >80% for 60s
3. **Limit fanout**:
   - Normal load: 4 flows × 5 agents = 20 agents
   - Heavy machine: 6 flows × 5 agents = 30 agents (max)
   - Low-resource machine: 2 flows × 4 agents = 8 agents
4. **Always use worktree isolation** for flows that mutate files.

## Cleanup after workflow

```bash
# Remove leftover worktrees from stopped workflows
cd <repo>
for wt in $(git worktree list | grep 'wf_' | awk '{print $1}'); do
  git worktree remove --force "$wt"
done
```

Also clean:
- Old subagent transcripts in `~/.claude/projects/*/subagents/`
- Temp build dirs older than 7 days
- `.coverage`, `__pycache__`, `.pytest_cache` if disk >90%

## Lightweight version (≤8 agents)

For small backlogs or constrained machines, collapse SA+PA into one "Architect" agent and use one DEV:

```
MANAGER → Architect (SA+PA) → DEV → TESTER
```

Use this when:
- Only 2–3 workstreams
- Each workstream is well-scoped (<5 files)
- Machine free RAM <2 GB

## Prompt templates

### SA prompt

```
You are the System Analyst for workstream "{title}" in {repo} (branch {branch}).
Read the relevant paths: {paths}.
Identify current state, gaps, concrete deliverables, and risks.
Return structured JSON with: findings[], workstream_scope, risks[].
Do not implement.
```

### PA prompt

```
You are the Project Architect. Based on the SA analysis, produce an implementation plan.
SA analysis: {sa_result}
Deliverables: {deliverables}
Return structured JSON with: plan, file_changes[{path, action, rationale}], test_strategy.
```

### DEV prompt

```
You are a Developer for "{title}".
Plan: {pa_result}
Implement your assigned portion in the isolated worktree. Run relevant tests.
Return structured JSON with: files_changed[], tests_run, test_result, errors[].
```

### TESTER prompt

```
You are the Tester for "{title}".
Dev results: {dev_results}
Verify completeness, run tests if applicable, and provide PASS/FAIL/CONDITIONAL verdict.
Return structured JSON with: verdict, gaps[], integration_notes.
```

## Workflow script skeleton

Use Claude Code `Workflow` tool with this shape:

```javascript
export const meta = {
  name: 'jit-orchestrate-example',
  description: 'Example SA→PA→TESTER orchestration',
  phases: [
    { title: 'Architecture', detail: 'SA analysis' },
    { title: 'Planning', detail: 'PA planning' },
    { title: 'Execution', detail: 'DEV + TESTER' },
    { title: 'Synthesis', detail: 'Integrate results' },
  ],
};

const flows = [ /* {key, title, paths, deliverables} */ ];

async function runFlow(flow) {
  const sa = await agent('SA prompt...', { schema: SA_SCHEMA, phase: 'Architecture' });
  const pa = await agent('PA prompt...', { schema: PA_SCHEMA, phase: 'Planning' });
  const dev = await agent('DEV prompt...', { schema: DEV_SCHEMA, phase: 'Execution' });
  const tester = await agent('TESTER prompt...', { schema: TESTER_SCHEMA, phase: 'Execution' });
  return { flow, sa, pa, dev, tester };
}

phase('Architecture');
const results = await parallel(flows.map(f => () => runFlow(f)));
phase('Synthesis');
const synthesis = await agent('Synthesize...', { phase: 'Synthesis' });
return { results, synthesis };
```

## Human gates

Never let the workflow autonomously:
- push to shared branches without explicit approval
- delete production data or secrets
- open real-evidence / prod-upload gates
- merge PRs
- run `rm -rf` without backup

The workflow returns results to the MANAGER (you). You decide commit/push/deploy.

## Real-world validation

First live run on 2026-08-02 (session `2fddc76a`) targeted `csoc_boi/evidence_probe.py` unit tests:

- **Workstream**: add unit tests for evidence_probe dry-run behavior.
- **Flow**: MANAGER → Architect (SA+PA) → DEV (tdd-guide) → TESTER (e2e-runner).
- **Result**: 36 tests (29 new), 92% branch coverage, all green.
- **Commit/push**: `5168988` on `csoc/master` after literal-password placeholder fix.

Lessons captured:
1. Collapsing SA+PA into one Architect agent is faster for a single well-scoped workstream.
2. The DEV agent should run tests immediately and report pass/fail; do not assume green from implementation.
3. Secret guards can block test fixtures. Use short placeholders (`password="x"`) or computed strings (`"x" * 6`) for fake credentials.
4. On machines with the `rtk` hook, run pytest as `rtk proxy python -m pytest ...` to avoid the "No tests collected" rewrite bug.
5. `pythonw` subprocess stdin handle can flake; prefer `python.exe` or `rtk proxy` for test runs.

## Windows / PowerShell cleanup

On Windows, the bash worktree cleanup may fail. Use PowerShell:

```powershell
# List and remove leftover workflow worktrees
$repo = "C:\Users\MDES-DEV-NB\Jit"  # adjust per repo
foreach ($wt in (git -C $repo worktree list --porcelain | Select-String "^worktree ")) {
  $path = $wt -replace "^worktree ", ""
  if ($path -match "wf_") {
    git -C $repo worktree remove --force $path
  }
}

# Remove transient artifacts when disk >90%
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue `
  "C:\Users\MDES-DEV-NB\DEV\URL-Checker\coverage.json",
  "C:\Users\MDES-DEV-NB\DEV\URL-Checker\.pytest_cache",
  "C:\Users\MDES-DEV-NB\.claude\projects\*\subagents\*.jsonl"
```

## Known traps

- **Skill not registered yet**: Until `jit-orchestrate` is in Claude's skill registry, invoke it manually with the `Agent` tool using the role prompts above. Do not rely on `Skill({skill:"jit-orchestrate"})` returning success.
- **Large workflow warning**: If Claude shows "Large workflow", stop the workflow ID, remove leftover worktrees, and reduce fanout before restarting.
- **Resource pressure**: If free RAM drops below 1.5 GB during a run, pause new agents and clean temp/artifact files before continuing.

## /forward integration

At session end, write a `ψ/outbox/YYYY-MM-DD_orchestrate-result.md` with:
- workstreams attempted
- agent fanout size
- results per flow
- blockers requiring human decision
- cleanup status

This lets the next session resume without re-running discovery.
