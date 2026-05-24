<!-- skill-id: gsd-ui-review -->
<!-- source-path: gsd-ui-review -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-ui-review/SKILL.md -->
<!-- runtime: claude -->

<objective>
Conduct a retroactive 6-pillar visual audit. Produces UI-REVIEW.md with
graded assessment (1-4 per pillar). Works on any project.
Output: {phase_num}-UI-REVIEW.md
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/ui-review.md
@$HOME/.claude/get-shit-done/references/ui-brand.md
</execution_context>

<context>
Phase: $ARGUMENTS — optional, defaults to last completed phase.
</context>

<process>
Execute end-to-end.
Preserve all workflow gates.
</process>
