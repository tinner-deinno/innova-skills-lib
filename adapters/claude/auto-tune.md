<!-- skill-id: auto-tune -->
<!-- source-path: auto-tune -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/auto-tune/SKILL.md -->
<!-- runtime: claude -->

# Auto-Tune Skill

## Purpose

Analyze token telemetry data (`token_log.jsonl`) to identify inefficient agents and skills, then produce actionable optimization recommendations.

## Invocation

```bash
/auto-tune                    # Analyze all agents, show optimization report
/auto-tune innova             # Focus on specific agent
/auto-tune --threshold 5000   # Flag sessions over N tokens as expensive
/auto-tune --write            # Write suggestions to agent profile memory
```

## Implementation

### STEP 1: Read Telemetry Data

Read from: `C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl`

Each line is a JSON object with:
```json
{
  "timestamp": "2026-05-23T14:24:58Z",
  "agent": "jit",
  "skill": "scrutinize",
  "model": "claude-sonnet-4-6",
  "source": "manual|mdes_ollama|skill",
  "prompt_tokens": 8500,
  "completion_tokens": 2100,
  "total_tokens": 10600,
  "duration_ms": 45000,
  "task": "description"
}
```

Parse all valid JSON lines. Skip malformed entries with a note.

### STEP 2: Identify Inefficiencies

Flag sessions based on these criteria:

#### A. Total Token Threshold
Default: 5000 tokens. Adjustable via `--threshold N`.
- Flag sessions where `total_tokens > threshold`

#### B. Agent Baseline Overage
Compare each agent's avg tokens/session against tier baseline:

| Tier | Baseline | Flag If Above |
|------|----------|---------------|
| Tier 0-1 (72b: jit, soma) | 8,000 | >15,000 |
| Tier 2 (coder: innova, lak, neta) | 3,000 | >6,000 |
| Tier 3 (9b: all others) | 2,000 | >4,000 |

Formula: `avg_tokens/session = SUM(total_tokens) / count(sessions)`

For Tier 3 agents, also flag if avg > 3,500 (moderate concern).

#### C. Repeated Skill Calls
Detect loops: same agent + skill called 3+ times within 1 hour window.
- Count occurrences in last 60 minutes
- Flag if count >= 3 with same combination

#### D. Failed Calls
Detect sessions with `completion_tokens == 0`:
- Indicates failed call or zero-length response
- Flag as potential error or retry loop

#### E. Model Mismatch
Agents using unexpected models:
- Tier 0-1 should use claude-sonnet-4-6 or claude-opus-4-5
- Tier 2 should use claude-sonnet-4-6 or claude-haiku-4-5
- Tier 3 should use MDES Ollama (gemma4:26b, qwen models)
- Flag cross-tier model usage

### STEP 3: Generate Suggestions

For each flagged inefficiency, produce specific, actionable suggestion:

#### High Prompt Tokens (prompt_tokens > 70% of total_tokens)
```
Suggestion:
→ Shorten system prompt (move static context to Oracle query)
→ Use Oracle-first principle: query existing knowledge before processing
→ Reduce input duplication (check for repeated examples)
Estimated saving: N tokens/session
Priority: HIGH
```

#### High Completion Tokens (completion_tokens > 50% of total_tokens)
```
Suggestion:
→ Add output length constraint to prompt ("Respond in under 200 words")
→ Use structured output format (JSON, markdown list)
→ Split large outputs into separate calls
Estimated saving: N tokens/session
Priority: MEDIUM
```

#### Repeated Calls (3+ in 60 minutes)
```
Suggestion:
→ Add early exit condition (check cache/Oracle before retry)
→ Implement exponential backoff between retries
→ Log reason for retry (may indicate systematic issue)
Priority: MEDIUM
```

#### Failed Calls (completion_tokens == 0)
```
Suggestion:
→ Add explicit error handling
→ Fallback to simpler prompt or alternative model
→ Check for timeout/rate-limit issues
Priority: HIGH
```

#### Model Mismatch
```
Suggestion:
→ Align [agent] to tier [X] model selection
→ Reason: Model [Y] not optimal for this agent's tier
Priority: LOW
```

### STEP 4: Generate Optimization Report

Output markdown report with:

1. **Header** (timestamp, data range, agent filter if specified)
2. **Summary Statistics**
   - Total sessions analyzed
   - Date range covered
   - Current avg tokens/session
   - Target avg (20% reduction)
   - Potential saving (%)

3. **Inefficiencies Table**
   ```
   | Agent | Skill | Sessions | Avg Tokens | Baseline | Flag |
   |-------|-------|----------|------------|----------|------|
   | jit | scrutinize | 1 | 10,600 | 8,000 | +33% over baseline |
   ```
   - Sort by: (Avg Tokens - Baseline) DESC
   - Include only flagged items
   - Show delta from baseline

4. **Optimization Suggestions** (one per flagged item)
   - Agent/Skill name as heading
   - Token count and reason for flag
   - 2-3 specific actionable suggestions (use Thai if natural)
   - Estimated token saving
   - Priority level

5. **Group by Priority**
   - HIGH (fix first)
   - MEDIUM (fix soon)
   - LOW (nice to have)

6. **Impact Summary**
   ```
   Current: [avg] tokens/session across [N] sessions
   Target: [target] tokens/session (20% reduction)
   Total potential saving: [%] of all tokens
   ```

### STEP 5: Optional — Write to Agent Profile

If `--write` flag is passed:

1. For each agent with suggestions, locate: `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[agent-name].md`
2. Append under section: `## จุดที่ต้องพัฒนา` (Points for Development)
3. Format:
   ```markdown
   ### Auto-Tune Suggestions (from 2026-05-23)

   **Skill: scrutinize**
   - Shorten system prompt via Oracle-first query
   - Add output length constraint
   Estimated saving: ~2,000 tokens/session
   ```

4. If section doesn't exist, create it
5. Report which files were updated

## Baselines & Tier System

### Agent Tiers
Defined in `/network/registry.json` and CLAUDE.md:

- **Tier 0**: Master (jit using 72b)
- **Tier 1**: Leadership (soma using 72b)
- **Tier 2**: Core engineering (innova, lak, neta using coder models)
- **Tier 3**: Specialist organs (9 agents using 9b models)

### Expected Token Usage
- **Tier 0-1**: 6,000–10,000 tokens/session (complex decisions)
- **Tier 2**: 2,000–5,000 tokens/session (focused coding)
- **Tier 3**: 1,000–3,000 tokens/session (narrow tasks)

Sessions significantly above these ranges may indicate:
- Inefficient prompts
- Unnecessary context repetition
- Failed retries
- Unoptimized output format

## Key Heuristics

1. **Oracle-First Principle**: Before extensive processing, query Oracle to avoid duplicating stored knowledge.
2. **Compressed Context**: Use references instead of full context. "See ψ/memory/patterns/x" is cheaper than including the pattern inline.
3. **Output Constraints**: Add explicit length limits ("respond in under 200 words") to reduce completion tokens.
4. **Early Exit**: Check cache/Oracle for answers before invoking expensive models.
5. **Structured Output**: JSON or markdown lists are typically cheaper than prose explanations.

## Error Handling

- If `token_log.jsonl` not found: Report file path and create stub with instructions
- If line is invalid JSON: Skip with warning, continue processing
- If agent not in registry: Use generic baseline (2,500 tokens)
- If `--threshold` value is non-numeric: Default to 5,000 and warn

## Output Example

```markdown
# Auto-Tune Report — 2026-05-23

## Summary
- **Sessions analyzed**: 12
- **Date range**: 2026-05-20 to 2026-05-23
- **Current average**: 4,137 tokens/session
- **Target average** (20% reduction): 3,310 tokens/session
- **Total potential saving**: ~10,000 tokens

## Inefficiencies Found (3 items flagged)

| Agent | Skill | Sessions | Avg Tokens | Baseline | Status |
|-------|-------|----------|------------|----------|--------|
| jit | scrutinize | 1 | 10,600 | 8,000 | ⚠️ +33% |
| lak | code-review | 1 | 7,000 | 3,000 | 🔴 +133% |
| innova | model-MDES | 3 | 1,620 | 2,000 | ✅ efficient |

## Optimization Suggestions

### HIGH Priority

**jit/scrutinize** (10,600 tokens — Tier 0 baseline: 8,000)

Problem: Prompt tokens = 8,500 (80% of total) — excessive context loading

Suggestions:
- ใส่ Oracle query ก่อนใช้ scrutinize เพื่อลด context duplication
- จำกัด output ด้วย "report under 300 words"
- Split large scrutiny tasks into 2-3 focused passes

Estimated saving: ~2,000 tokens/session (20% reduction)
Impact: If this pattern repeats 2x/week = ~4,000 tokens/week saved

---

### MEDIUM Priority

**lak/code-review** (7,000 tokens — Tier 2 baseline: 3,000)

Problem: High completion tokens (4,200 = 60% of total) — verbose explanations

Suggestions:
- Split large file reviews into smaller chunks (<500 lines each)
- Use focused review mode: specify security OR performance, not both
- Return structured findings only (issue list, not narrative explanation)

Estimated saving: ~3,000 tokens/session (43% reduction)

---

## Summary

✅ **Overall health**: GOOD (most agents within baseline)

⚠️ **Action items**:
1. Reduce jit/scrutinize prompt context (HIGH priority)
2. Structure lak/code-review output (MEDIUM priority)

**Next steps**:
- Run `/auto-tune --write` to persist suggestions to agent profiles
- Test optimized prompts with 3-5 sessions
- Re-analyze in 1 week to measure improvement
```

## Usage Notes

- Run daily or after major feature sprints to track efficiency trends
- Compare reports across weeks to measure progress
- Use suggestions as starting point; override with human judgment
- Archive reports in `ψ/memory/auto-tune/report-YYYY-MM-DD.md` for historical analysis
- Coordinate with Oracle-first principle: use `/learn` to capture successful optimizations as patterns

---

**Owned by**: soma (strategic), innova (operational)  
**Related skills**: `/scrutinize`, `/gsd-health`, `/trace`  
**Last updated**: 2026-05-23
