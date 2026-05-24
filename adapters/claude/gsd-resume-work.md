<!-- skill-id: gsd-resume-work -->
<!-- source-path: gsd-resume-work -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-resume-work/SKILL.md -->
<!-- runtime: claude -->

<objective>
Restore complete project context and resume work seamlessly from previous session.

Routes to the resume-project workflow which handles:

- STATE.md loading (or reconstruction if missing)
- Checkpoint detection (.continue-here files)
- Incomplete work detection (PLAN without SUMMARY)
- Status presentation
- Context-aware next action routing
  </objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/resume-project.md
</execution_context>

<process>
Execute end-to-end.
</process>
