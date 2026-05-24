<!-- skill-id: gsd-ai-integration-phase -->
<!-- source-path: gsd-ai-integration-phase -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-ai-integration-phase/SKILL.md -->
<!-- runtime: claude -->

<objective>
Create an AI design contract (AI-SPEC.md) for a phase involving AI system development.
Orchestrates gsd-framework-selector → gsd-ai-researcher → gsd-domain-researcher → gsd-eval-planner.
Flow: Select Framework → Research Docs → Research Domain → Design Eval Strategy → Done
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/ai-integration-phase.md
@$HOME/.claude/get-shit-done/references/ai-frameworks.md
@$HOME/.claude/get-shit-done/references/ai-evals.md
</execution_context>

<context>
Phase number: $ARGUMENTS — optional, auto-detects next unplanned phase if omitted.
</context>

<process>
Execute end-to-end.
Preserve all workflow gates.
</process>
