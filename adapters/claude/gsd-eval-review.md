<!-- skill-id: gsd-eval-review -->
<!-- source-path: gsd-eval-review -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-eval-review/SKILL.md -->
<!-- runtime: claude -->

<objective>
Conduct a retroactive evaluation coverage audit of a completed AI phase.
Checks whether the evaluation strategy from AI-SPEC.md was implemented.
Produces EVAL-REVIEW.md with score, verdict, gaps, and remediation plan.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/eval-review.md
@$HOME/.claude/get-shit-done/references/ai-evals.md
</execution_context>

<context>
Phase: $ARGUMENTS — optional, defaults to last completed phase.
</context>

<process>
Execute end-to-end.
Preserve all workflow gates.
</process>
