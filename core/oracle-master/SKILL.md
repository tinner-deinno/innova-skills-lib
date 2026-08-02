# /oracle-master — Master Oracle Console

**Purpose**: One skill to see, probe, feed, and sync every Oracle layer that Jit owns.

**Scope**:
- `arra-oracle-v3` memory server on `localhost:47778`
- `innova-bot` body/bridge on `localhost:7010`
- `maw-js` federation on `localhost:3456`
- Local Ollama on `localhost:11434`
- Jit repo `ψ/` brain tree
- `~/.claude/skills` sync via `jit_bootstrap.py`

**Usage**:

```bash
/oracle-master                  # summary: identity, principles, ports
/oracle-master --health         # probe all live services
/oracle-master --search "Jit"   # search Oracle memory
/oracle-master --ingest "fact text" --source "BigBoss" --tags ["Jit","rule"]
/oracle-master --handoff        # list latest handoffs
/oracle-master --sync            # run jit_bootstrap.py (skills + health checks)
/oracle-master --agents         # show agent/organs registry summary
/oracle-master --vault          # list ψ/ vault / outbox / resonance
/oracle-master --federation      # show maw peers + test mdes002 reachability
```

**Implementation**: This skill runs `python Jit/tools/oracle_master_cli.py <args>`.

## Rules invoked by this skill

1. **Nothing is Deleted**: `--ingest` appends; `--handoff` creates a new file with timestamp.
2. **External Brain, Not Command**: every probe reports options, human decides.
3. **Verify before report**: health checks hit real ports; failures are shown, not hidden.
4. **Privacy**: no data leaves BigBoss's own machines (`tinner-deinno/Jit`, local endpoints).

## Output conventions

- Always print `mdes-001 (NB1-Jit)` machine signature at end.
- Report exact HTTP status / latency.
- If a service is down, show the one-line fix command.
