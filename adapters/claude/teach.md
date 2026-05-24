<!-- skill-id: teach -->
<!-- source-path: teach -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/teach/SKILL.md -->
<!-- runtime: claude -->

# /teach — Agent Feedback & Development Tracking

Claude closes the teaching gap in the Mentorship System by recording BigBoss feedback directly into agent profiles.

## Invocation Patterns

```bash
# Session review (default) — append note to BigBoss บันทึก section
/teach innova 4 "สร้าง 21 agent profiles ครบ parallel agents work well"

# Skill tracking (--track flag) — update Skill Level table
/teach soma --track "system design" 4 "architecture clear but verbose"

# Detailed logging (--log flag) — add row to Track Record table
/teach vaja --log "2026-05-23" "report drafting" "sent to BigBoss" 3 "2.1s" 980
```

---

## Implementation Steps

### STEP 1: Parse Input Arguments

Extract arguments in this order:

```
Position 0: agent-name (required)
Position 1+: Depends on flags

No flag (default):
  - arg[1] = score (1-5)
  - arg[2+] = note (can be multiple words)

--track flag:
  - arg[1] = "--track" (keyword)
  - arg[2] = skill-name
  - arg[3] = score (1-5)
  - arg[4+] = note (optional)

--log flag:
  - arg[1] = "--log" (keyword)
  - arg[2] = date (YYYY-MM-DD)
  - arg[3] = task (short description)
  - arg[4] = outcome (one-line result)
  - arg[5] = score (1-5)
  - arg[6] = time (e.g., "2.1s")
  - arg[7] = tokens (numeric)
```

**Validation**:
- agent-name must be valid (check against available agents in `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\`)
- score must be 1-5 (numeric)
- date must be YYYY-MM-DD format (if --log flag)
- If agent file doesn't exist: show error with list of available agents

### STEP 2: Read Agent Profile File

Path: `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[agent-name].md`

If file missing:
```
Error: Agent profile not found for "[agent-name]"
Available agents:
  - chamu
  - innova
  - jit
  - karn
  - lak
  - [... etc ...]

Tip: Check spelling or use /teach -list to see all agents
```

Otherwise, read the entire file and locate the appropriate section to modify.

### STEP 3: Append or Update Content

#### Case 1: Default (No Flag) — Session Review

Append to **"## บันทึก BigBoss"** section as a new subsection:

```markdown
### [YYYY-MM-DD] Session Review
**ทำได้ดี**: [note]
**คะแนน**: [score]/5 ⭐
**งานถัดไป**: ติดตามพัฒนาการในเซสชันถัดไป
```

If "## บันทึก BigBoss" section doesn't exist, create it:

```markdown
## บันทึก BigBoss
### [YYYY-MM-DD] Session Review
**ทำได้ดี**: [note]
**คะแนน**: [score]/5 ⭐
**งานถัดไป**: ติดตามพัฒนาการในเซสชันถัดไป
```

#### Case 2: --track Flag — Skill Level Update

Update the **"## ระดับทักษะ (Skill Level)"** table.

**If the skill already exists in the table**: Update the row in place.

**If the skill is new**: Add a new row:
```markdown
| [skill-name] | ⭐ x [score] | [note] |
```

Stars rendering:
- Score 1 = ⭐
- Score 2 = ⭐⭐
- Score 3 = ⭐⭐⭐
- Score 4 = ⭐⭐⭐⭐
- Score 5 = ⭐⭐⭐⭐⭐

**If the Skill Level table doesn't exist**, create it after Core Strengths:

```markdown
## ระดับทักษะ (Skill Level)
| ทักษะ | ระดับ (1-5) | หมายเหตุ |
|-------|------------|---------|
| [skill-name] | ⭐ x [score] | [note] |
```

#### Case 3: --log Flag — Track Record Update

Append a row to the **"## Track Record (ประวัติการทำงาน)"** table.

Format:
```markdown
| [date] | [task] | [outcome] | ⭐ x [score] | [time] | [tokens] |
```

**If the Track Record table doesn't exist**, create it:

```markdown
## Track Record (ประวัติการทำงาน)
| วันที่ | งาน | ผลลัพธ์ | คะแนน | เวลา | Token |
|--------|-----|---------|-------|------|-------|
| [date] | [task] | [outcome] | ⭐ x [score] | [time] | [tokens] |
```

Append rows at the end of the table (most recent at top or as appropriate).

### STEP 4: Log to Telemetry (if available)

If the telemetry script exists at `~/Jit/limbs/telemetry.sh`, invoke it:

```bash
bash ~/Jit/limbs/telemetry.sh log "[agent-name]" "teach" "human-feedback" 0 0 "[note]"
```

**Do not block if script is missing** — this is optional instrumentation.

### STEP 5: Confirm & Show What Was Written

After updating the file, show what was appended/updated:

```markdown
✅ Updated agent profile: [agent-name]

**Section**: [Section Name]
**Action**: [Added/Updated]
**Content**:
[Show the exact lines that were written]
```

---

## Special Behaviors

### Available Agents

The system tracks 24 agents (including external models). When listing, show:

```
jit, soma, innova, lak, neta, vaja, chamu, rupa, pada, netra, karn, mue, 
pran, sayanprasathan, gemma4, nemotron, openthaigpt, pathumma, thalle, 
typhoon, lung, and others
```

Use `ls C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\` to dynamically list available profiles.

### Skill Name Flexibility

The --track flag should accept skill names with spaces (e.g., "system design"). Wrap in quotes if needed:

```bash
/teach soma --track "system design" 4 "clear architecture"
```

### Date Handling

- If no date provided in --log, use today's date (current system date)
- Format always as YYYY-MM-DD

### Multiple Word Notes

Notes in default and --track modes can span multiple arguments:
```bash
/teach innova 5 "สร้าง" "21" "agent" "profiles" "ครบ"
# Joins as: "สร้าง 21 agent profiles ครบ"
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Agent not found | List available agents, show path checked |
| Score invalid (not 1-5) | Reject, ask for numeric 1-5 |
| File read error | Show filesystem error, suggest check path exists |
| Cannot append to file | Report I/O error, do not overwrite |
| Malformed table (--track/--log) | Create new table section instead of updating |

---

## Files Modified

- `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[agent-name].md` — Agent profile (appended/updated)
- `~/Jit/limbs/telemetry.sh` — (optional, only if invoked and exists)

---

## Example Workflows

### Workflow 1: Quick Session Feedback
```bash
# innova did great work today
/teach innova 5 "integrated soul-sync identity across all 14 organs successfully"

# What happens:
# 1. Reads innova.md
# 2. Appends under "## บันทึก BigBoss":
#    ### 2026-05-23 Session Review
#    **ทำได้ดี**: integrated soul-sync identity across all 14 organs successfully
#    **คะแนน**: 5/5 ⭐
#    **งานถัดไป**: ติดตามพัฒนาการในเซสชันถัดไป
# 3. Logs to telemetry
# 4. Shows confirmation
```

### Workflow 2: Skill Development Tracking
```bash
# soma's architectural capability improved
/teach soma --track "system design" 4 "architecture diagrams clearer than before"

# What happens:
# 1. Reads soma.md
# 2. Finds or creates Skill Level table
# 3. Updates row for "system design" to ⭐⭐⭐⭐ with note
# 4. Shows what was updated
```

### Workflow 3: Detailed Work Log
```bash
# Log vaja's report drafting work
/teach vaja --log "2026-05-23" "report drafting" "sent to BigBoss" 3 "2.1s" 980

# What happens:
# 1. Reads vaja.md
# 2. Finds or creates Track Record table
# 3. Adds row: | 2026-05-23 | report drafting | sent to BigBoss | ⭐⭐⭐ | 2.1s | 980 |
# 4. Shows confirmation with row inserted
```

---

## Philosophy

This skill bridges the gap between system monitoring and human mentorship. BigBoss provides **real feedback** — observations from live work, not abstract scores. The feedback closes a loop: agents work → BigBoss observes → records feedback → agents see patterns across sessions → improve.

The three modes serve different purposes:
- **Session Review** — Immediate, in-moment feedback (captures vibe)
- **--track** — Skill development over time (shows growth trajectory)
- **--log** — Detailed work metrics (efficiency & performance)

Together, they create a **learning profile** for each agent that captures both performance and human judgment.
