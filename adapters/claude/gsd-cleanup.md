<!-- skill-id: gsd-cleanup -->
<!-- source-path: gsd-cleanup -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-cleanup/SKILL.md -->
<!-- runtime: claude -->

<objective>
Archive phase directories from completed milestones into `.planning/milestones/v{X.Y}-phases/`.

Use when `.planning/phases/` has accumulated directories from past milestones.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/cleanup.md
</execution_context>

<process>
Execute end-to-end.
Identify completed milestones, show a dry-run summary, and archive on confirmation.
</process>
