# Codex PRD Polish

Use this after PRD review and before publish.

## Purpose

Improve clarity, structure, naming consistency, and readability without changing product facts.

## Must Preserve

- confirmed business facts
- explicit unknowns and pending items
- requirement scope and non-goals
- variable names unless they are inconsistent or unreadable

## Must Check

1. every variable, state, event, and config item has a readable English name
2. art and design content is grouped into a dedicated section
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

If a higher-tier review pass is unavailable, run the same checklist with the best available model and mark the result as `fallback_model_polish`.
