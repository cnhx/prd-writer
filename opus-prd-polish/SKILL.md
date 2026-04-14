---
name: opus-prd-polish
description: |
  Final polish pass for a PRD using the highest-reasoning model available.
  Improves clarity, structure, naming consistency, and readability without changing product facts.
  Use after PRD review and before publish.
preferred-models:
  - claude-opus-4-6
  - claude-opus-4-5
  - any high-reasoning tier model
---

# Final PRD Polish

Use this after PRD review and before publish.

## Purpose

Improve clarity, structure, naming consistency, and readability without changing product facts.

## Model Selection

- Prefer the highest-reasoning model available in the current environment.
- The `preferred-models` list in frontmatter is a hint, not a hard dependency — treat it as "top-tier Claude Opus or equivalent"; any model in that tier is acceptable.
- If no top-tier model is available, run the same checklist with the best available model and note `polish_tier: fallback` in the output.

> The skill name is retained as `opus-prd-polish` for backward compatibility. It refers to a polish *tier*, not a specific model version.

## Language Policy

- Final output language is not forced.
- Follow user preference or workspace context.
- English identifiers for variables, states, events, and config fields remain mandatory regardless of prose language.

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
- `polish_tier`: `top` (preferred model used) or `fallback` (best-available used)
