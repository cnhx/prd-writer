---
name: opus-prd-polish
description: |
  Final Opus-grade polish pass for a PRD. Improves clarity, structure, naming consistency,
  and readability without changing product facts. Use after PRD review and before publish.
---

# Opus PRD Polish

Use this after PRD review and before publish.

## Purpose

Improve clarity, structure, naming consistency, and readability without changing product facts.

## Language Policy

- Final output language is not forced.
- Follow user preference or workspace context.
- English identifiers for variables, states, events, and config fields remain mandatory.

## Must Preserve

- Confirmed business facts
- Explicit unknowns and pending items
- Requirement scope and non-goals
- Variable names unless they are inconsistent or unreadable

## Must Check

1. Every variable/state/event/config item has a readable English name
2. Art/design content is grouped into a dedicated section
3. Feature logic is not mixed with visual direction
4. Vague wording is tightened
5. Duplicated requirements are merged
6. Assumptions and facts are not blurred together

## Output

Return:
- Polished draft (written to file)
- List of major edits
- Unresolved gaps
- Recommended commit message

## Fallback

If Opus is unavailable, run the same checklist with the best available model and note that fallback polish was applied.
