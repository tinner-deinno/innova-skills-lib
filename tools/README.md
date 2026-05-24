# innova-skills-lib / tools

Maintenance and deployment utilities for the innova-skills-lib skill library.

---

## sync_to_project.ps1

Syncs every skill from the global `~/.claude/skills/` directory into any project's
`.claude/skills/` folder via Windows Directory Junctions (default) or full recursive
copies.

### Behaviour

| Source entry | Destination entry | Notes |
|---|---|---|
| `~/.claude/skills/<name>/` | `<project>/.claude/skills/<name>` | Direct junction / copy |
| `~/.claude/skills/ecc/<subname>/` | `<project>/.claude/skills/ecc-<subname>` | Flattened with `ecc-` prefix |

### Usage

```powershell
# Basic — junction all skills into a project
.\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\innova-bot"

# Preview every action without touching the filesystem
.\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\my-project" -DryRun

# Copy instead of junction (useful for CI or network paths)
.\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\my-project" -Mode copy

# Force-recreate all entries (overwrite existing junctions / copies)
.\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\innova-bot" -Force

# Custom source root
.\sync_to_project.ps1 -ProjectPath "C:\..." -SourceRoot "D:\alt-skills"

# Combine flags
.\sync_to_project.ps1 -ProjectPath "C:\Users\MDES-DEV-NB\innova-bot" -Mode copy -Force -DryRun
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `-ProjectPath` | string | **required** | Absolute path to the project root |
| `-SourceRoot` | string | `~/.claude/skills` | Override the global skills source |
| `-Mode` | `junction` / `copy` | `junction` | Link strategy |
| `-DryRun` | switch | off | Preview only — no filesystem changes |
| `-Force` | switch | off | Overwrite / recreate existing entries |

### Exit codes

| Code | Meaning |
|---|---|
| `0` | All entries processed without errors |
| `1` | One or more entries failed (see ERROR lines in output) |

---

## sync-global-skills.ps1  (innova-bot convenience wrapper)

Located at: `C:\Users\MDES-DEV-NB\innova-bot\.claude\skills\sync-global-skills.ps1`

Thin wrapper that calls `sync_to_project.ps1` with `-ProjectPath` pre-set to
`innova-bot`.  Run from innova-bot's `.claude/skills/` directory and pass any flags
straight through.

```powershell
# From innova-bot/.claude/skills/
.\sync-global-skills.ps1              # sync (junction mode)
.\sync-global-skills.ps1 -DryRun      # dry run
.\sync-global-skills.ps1 -Force       # recreate all junctions
.\sync-global-skills.ps1 -Mode copy   # copy mode
```

---

## Adding new tools

Drop new `.ps1` scripts in this directory and document them in this README under a
new `## <script-name>` section following the same format above.
