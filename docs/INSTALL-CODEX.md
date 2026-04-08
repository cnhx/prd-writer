# Install in Codex

The ready-to-copy Codex adapter lives in `platforms/codex/`.

## Recommended Setup

1. Copy `platforms/codex/AGENTS.md` into the target workspace root as `AGENTS.md`, or merge it into an existing workspace instructions file.
2. Keep `platforms/codex/prd-workflow.md` in the workspace as the reusable PRD workflow prompt.
3. Keep `platforms/codex/opus-prd-polish.md` as the optional final polish prompt.
4. Copy `platforms/codex/config.example.yaml` and adapt the paths, knowledge base settings, and publish policy.

## Minimum Working Mode

Set:
- `knowledge_base.enabled = false`
- `publish.git_commit = false`
- `polish.enabled = false` if you do not want a second polish pass

## Suggested Invocation Pattern

- read the brief and local project docs
- ask one key question at a time
- write the PRD draft to a file instead of chat
- run the review checklist
- run the optional polish pass
- save and optionally commit

## Compatibility Notes

If the target workspace already has strong global instructions, merge the PRD-specific parts instead of replacing them wholesale.
