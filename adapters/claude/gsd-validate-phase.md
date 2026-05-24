<!-- skill-id: gsd-validate-phase -->
<!-- source-path: gsd-validate-phase -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-validate-phase/SKILL.md -->
<!-- runtime: claude -->

<objective>
Audit Nyquist validation coverage for a completed phase. Three states:
- (A) VALIDATION.md exists — audit and fill gaps
- (B) No VALIDATION.md, SUMMARY.md exists — reconstruct from artifacts
- (C) Phase not executed — exit with guidance

Output: updated VALIDATION.md + generated test files.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/validate-phase.md
</execution_context>

<context>
Phase: $ARGUMENTS — optional, defaults to last completed phase.
</context>

<process>
Execute end-to-end.
Preserve all workflow gates.
</process>
