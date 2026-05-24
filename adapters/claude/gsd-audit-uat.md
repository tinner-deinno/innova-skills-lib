<!-- skill-id: gsd-audit-uat -->
<!-- source-path: gsd-audit-uat -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/gsd-audit-uat/SKILL.md -->
<!-- runtime: claude -->

<objective>
Scan all phases for pending, skipped, blocked, and human_needed UAT items. Cross-reference against codebase to detect stale documentation. Produce prioritized human test plan.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/audit-uat.md
</execution_context>

<context>
Core planning files are loaded in-workflow via CLI.

**Scope:**
Glob: .planning/phases/*/*-UAT.md
Glob: .planning/phases/*/*-VERIFICATION.md
</context>
