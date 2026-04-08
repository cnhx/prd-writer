# Claude Code PRD Workflow

Use this file as a prompt module or local skill for PRD writing in Claude Code.

## Phase 0 — Context Loading

Sources, in priority order:
1. task-specific files supplied by the user
2. local repository documents
3. optional knowledge base path from config
4. user answers

If the knowledge base is disabled, continue without error.

## Phase 1 — Product Interrogation

Ask one key question at a time.

Required question themes:
1. market truth
2. current alternatives
3. target player or user profile
4. minimum viable scope
5. business and math intuition
6. differentiation and defensibility

## Phase 2 — Premise Check and Option Selection

Produce:
- 3 to 5 core assumptions to confirm
- 2 to 3 implementation options
- one recommendation with rationale

Do not start drafting until the recommendation is accepted.

## Phase 3 — PRD Drafting Structure

Write the draft to a markdown file instead of returning the full document in chat.

Required sections:
1. summary
2. project positioning
3. market strategy
4. gameplay or product flow
5. functional requirements
6. art and design requirements
7. math or business model
8. compliance and risk
9. technical considerations
10. KPI and success metrics
11. milestones
12. assumptions
13. non-goals
14. sources

## Phase 4 — Review

Review checklist:
- is the core flow implementable without guesswork?
- are edge cases and state transitions explicit?
- are math assumptions separated from confirmed numbers?
- are art requirements isolated from logic requirements?
- are compliance and market facts sourced or marked as pending?
- are non-goals explicit?
- is the English naming consistent?

## Phase 5 — Polish and Publish

Sequence:
1. review the saved draft
2. run optional `opus-prd-polish.md`
3. save the final file
4. optionally commit with git
5. return the output contract
