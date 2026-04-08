# Opus PRD Polish Skill

Use this after PRD review and before publish.

## Purpose

Improve clarity, structure, naming consistency, and readability without changing product facts.

## Language Policy

- The skill is written in English.
- Final output language is not forced.
- Follow user preference or workspace context.
- English identifiers for variables, states, events, and config fields remain mandatory.

## Must Preserve

- confirmed business facts
- explicit unknowns and pending items
- requirement scope and non-goals
- variable names unless they are inconsistent or unreadable

## Must Check

1. every variable/state/event/config item has a readable English name
2. art/design content is grouped into a dedicated section
3. feature logic is not mixed with visual direction
4. vague wording is tightened
5. duplicated requirements are merged
6. assumptions and facts are not blurred together

## Output

Return:
- polished_draft
- list_of_major_edits
- unresolved_gaps
- recommended_commit_message

## Fallback

If Opus is unavailable, run the same checklist with the best available model and mark result as `fallback_model_polish`.
