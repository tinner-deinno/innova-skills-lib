<!-- skill-id: auto-model-switch -->
<!-- source-path: auto-model-switch -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/auto-model-switch/SKILL.md -->
<!-- runtime: claude -->

# /auto-model-switch — Smart Model Router

> ออกแบบโดย ThaiLLM Typhoon | ใช้คนให้ถูกงาน ใช้โมเดลให้ถูกเวลา

Auto-selects the best AI model for the task — saves tokens, optimizes quality.

**Trigger**: `/auto-model-switch <task>` หรือ `/ams <task>`

---

## Routing Matrix (designed by ThaiLLM Typhoon)

| Priority | Keywords | Model | Provider | Cost |
|----------|----------|-------|----------|------|
| 1 | reasoning, complex, analysis, math, logic, deep, architecture | claude-sonnet | Anthropic | 💰💰💰 |
| 2 | code, โค้ด, debug, algorithm, function, syntax, implement | openthaigpt | ThaiLLM | 💰 |
| 3 | สรุป, ย่อ, summarize, translate, แปล, เขียน, draft | typhoon | ThaiLLM | 💰 |
| 4 | ไทย, thai, ภาษาไทย, พูดคุย, ทั่วไป, อธิบาย | gemma4:26b | MDES | 💰💰 |
| 5 | เร็ว, fast, quick, simple, เบา, ตรวจ, check | llama3.1:8b | MDES | 💰 |
| DEFAULT | anything else | gemma4:26b | MDES | 💰💰 |

---

## Step 1: Analyze the task

Look at the task/prompt keywords and match against the routing matrix above.
Pick the FIRST matching rule. If no match, use DEFAULT (gemma4:26b MDES).

Output your reasoning:
```
🎯 Task analysis: [type of task]
📌 Matched rule: [rule number + keywords matched]  
🤖 Selected: [model] ([provider])
💡 Reason: [why this model]
```

## Step 2: Execute with selected model

### If model = openthaigpt or typhoon or pathumma or thalle (ThaiLLM):
```bash
set -a; source C:\Users\MDES-DEV-NB\Jit\.env; set +a
CURRENT_AGENT=[model] bash C:\Users\MDES-DEV-NB\Jit\limbs\thaillm.sh ask [model] "[task]"
```

### If model = gemma4:26b or gemma2:9b or qwen2.5:72b or qwen2.5-coder (MDES):
```bash
set -a; source C:\Users\MDES-DEV-NB\Jit\.env; set +a
# Edit the model line in ollama.sh or use direct curl:
JSON=$(python3 -c "import json,sys; print(json.dumps({'model':'[model]','prompt':sys.argv[1],'stream':False}))" "[task]")
curl -s --max-time 60 "https://ollama.mdes-innova.online/api/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OLLAMA_TOKEN" \
  --data "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('response',''))"
```

### If model = claude-sonnet (current session):
Just answer directly — you ARE claude-sonnet. Note: "Using Claude (current session)"

## Step 3: Log the routing decision

Append to `C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\routing_log.jsonl`:
```json
{"timestamp": "ISO", "task_type": "...", "keywords_matched": [...], "model_selected": "...", "provider": "..."}
```

## Step 4: Show result with attribution

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 [Model Name] ([Provider])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[response]

— ตอบโดย [model] | เวลา: [elapsed]ms
```

---

## Override flags

- `/auto-model-switch --force-mdes <task>` → always use gemma4:26b (MDES)
- `/auto-model-switch --force-thai <task>` → always use ThaiLLM gang (auto-route within gang)
- `/auto-model-switch --force-claude <task>` → always use current Claude session
- `/auto-model-switch --compare <task>` → run task on top 3 matching models, compare results (calls /model-compare)

---

## Token Budget Guide

| Provider | Cost per 1K tokens | Best For |
|----------|-------------------|---------|
| gemma2:9b MDES | Free (self-hosted) | Fast checks, simple tasks |
| ThaiLLM (8B) | Free (public API) | Thai language, code, summaries |
| gemma4:26b MDES | Free (self-hosted) | General Thai, medium complexity |
| Claude-haiku | ~$0.001 | Quick tasks needing Claude quality |
| Claude-sonnet | ~$0.01 | Main work, orchestration |
| Claude-opus | ~$0.075 | Architecture, deep reasoning only |

**Goal**: Use free models (MDES + ThaiLLM) for 80%+ of tasks, reserve Claude for the 20% that truly needs it.
