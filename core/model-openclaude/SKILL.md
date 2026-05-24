# /model-openclaude — เปิด OpenClaude ด้วย provider ที่เลือก

เปิด openclaude TUI หรือรันคำสั่งแบบ non-interactive ผ่าน provider ที่ต้องการ  
รองรับ 5 providers: mdes, github, openai, thaillm, local

**Trigger**: `/model-openclaude`, `/oc`, "เปิด openclaude", "openclaude [provider]", "oc [mdes|github|openai|thai|local]"

---

## Providers

| Provider | Alias | Default Model | Endpoint |
|----------|-------|---------------|----------|
| `mdes` | oc-mdes | gemma4:26b | ollama.mdes-innova.online/v1 ← DEFAULT |
| `github` | oc-github | gpt-4o | models.inference.ai.azure.com |
| `openai` | oc-openai | gpt-4o | api.openai.com/v1 |
| `thaillm` | oc-thai | Typhoon-S-ThaiLLM-8B-Instruct | thaillm.or.th/api/v1 |
| `local` | oc-local | qwen2.5-coder:7b | localhost:11434/v1 |

## วิธีปฏิบัติ

### เปิด TUI

```powershell
# Windows PowerShell — ใช้ switch-provider.ps1 แล้วรัน openclaude
. C:\Users\MDES-DEV-NB\DEV\openclaude\switch-provider.ps1 mdes
openclaude

# หรือใช้ PS profile shortcuts
oc-mdes; openclaude
oc-github; openclaude
oc-thai; openclaude
```

```bash
# Bash (Linux/WSL/Git Bash)
bash ~/Jit/limbs/openclaude.sh tui --provider mdes
bash ~/Jit/limbs/openclaude.sh tui --provider github
bash ~/Jit/limbs/openclaude.sh tui --provider thaillm
```

### ถามแบบ non-interactive (single prompt)

```powershell
. C:\Users\MDES-DEV-NB\DEV\openclaude\switch-provider.ps1 mdes
openclaude -p "อธิบาย quantum entanglement ภาษาไทย"
```

```bash
bash ~/Jit/limbs/openclaude.sh ask "อธิบาย quantum entanglement" --provider mdes
bash ~/Jit/limbs/openclaude.sh ask "write a hello world in Go" --provider github --model gpt-4o
```

### เปลี่ยน model ใน provider เดียวกัน

```powershell
. C:\Users\MDES-DEV-NB\DEV\openclaude\switch-provider.ps1 mdes qwen2.5:72b
```

```bash
bash ~/Jit/limbs/openclaude.sh tui --provider mdes --model qwen2.5:72b
```

### ดูรายการโมเดลทั้งหมด

```bash
bash ~/Jit/limbs/openclaude.sh models
```

### ทดสอบ connection

```bash
bash ~/Jit/limbs/openclaude.sh test mdes
bash ~/Jit/limbs/openclaude.sh test github
bash ~/Jit/limbs/openclaude.sh test thaillm
```

---

## Models per Provider

### MDES Ollama Cloud [mdes] ← DEFAULT

- `gemma4:26b` — ภาษาไทยดี, งานทั่วไป
- `qwen2.5:72b` — deep reasoning, ซับซ้อน
- `qwen2.5-coder` — code เชี่ยวชาญ
- `gemma2:9b` — เร็ว, ประหยัด
- `qwen3:8b` — qwen gen3
- `llama3.2` — Meta general

### GitHub Models [github]

- `gpt-4o` — OpenAI flagship
- `gpt-4o-mini` — ประหยัด, เร็ว
- `gpt-4.1` / `gpt-4.1-mini`
- `claude-3-5-sonnet-20241022` — Anthropic via GitHub
- `o1` / `o3-mini` — reasoning models
- `meta-llama-3.3-70b-instruct`

### OpenAI [openai]

- `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `o1`, `o3-mini`, `o4-mini`

### ThaiLLM [thaillm]

- `Typhoon-S-ThaiLLM-8B-Instruct` — สนทนาไทย
- `OpenThaiGPT-ThaiLLM-8B-Instruct-v7.2` — ไทยทั่วไป
- `Pathumma-ThaiLLM-qwen3-8b-think-3.0.0` — thinking mode ไทย
- `THaLLE-0.2-ThaiLLM-8B-fa` — Thai academic

### Ollama Local [local]

```bash
bash ~/Jit/limbs/openclaude.sh models  # ดูโมเดลที่ install ไว้
```

---

## GitHub Models routing (สำคัญ)

`CLAUDE_CODE_USE_GITHUB=1` ใช้ Copilot OAuth token (อาจหมดอายุ)  
ต้องใช้ OpenAI-compat route แทน:

```
CLAUDE_CODE_USE_OPENAI=1
OPENAI_BASE_URL=https://models.inference.ai.azure.com
OPENAI_API_KEY=<github_pat_token>
OPENAI_MODEL=gpt-4o
```

switch-provider.ps1 ทำ routing นี้อัตโนมัติ ไม่ต้องตั้งเอง

---

## Config Files

| File | Purpose |
|------|---------|
| `C:\Users\MDES-DEV-NB\DEV\openclaude\.env` | Default env: MDES + context window overrides |
| `C:\Users\MDES-DEV-NB\DEV\openclaude\switch-provider.ps1` | PS switcher script |
| `C:\Users\MDES-DEV-NB\Jit\limbs\openclaude.sh` | Bash agent control script |
| `D:\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1` | PS shortcuts |

---

## เมื่อ user ขอเปิด openclaude

1. ถามว่า provider ไหน (ถ้าไม่ระบุ ใช้ `mdes`)
2. ถามว่า TUI หรือ single prompt
3. แนะนำคำสั่งที่เหมาะกับ shell ที่ใช้ (PS หรือ Bash)
4. ถ้า provider ไม่ response → แนะนำ fallback (mdes → github → local)
