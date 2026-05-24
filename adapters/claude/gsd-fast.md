<!-- skill-id: gsd-fast -->
<!-- source-path: gsd-fast -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-fast/SKILL.md -->
<!-- runtime: claude -->

<objective>
Execute a trivial task directly in the current context without spawning subagents
or generating PLAN.md files. For tasks too small to justify planning overhead:
typo fixes, config changes, small refactors, forgotten commits, simple additions.

This is NOT a replacement for /gsd:quick — use /gsd:quick for anything that
needs research, multi-step planning, or verification. /gsd:fast is for tasks
you could describe in one sentence and execute in under 2 minutes.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/fast.md
</execution_context>

<process>
Execute end-to-end.
</process>
