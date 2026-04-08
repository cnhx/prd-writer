# Install the Claude Code Adapter

## Files to Copy

- `platforms/claude-code/CLAUDE.md` -> `CLAUDE.md`
- `platforms/claude-code/prd-workflow.md` -> keep as a prompt module or local skill
- `platforms/claude-code/opus-prd-polish.md` -> keep if polish is enabled
- `platforms/claude-code/config.example.yaml` -> copy and rename for local use

## Recommended Setup

1. Merge `platforms/claude-code/CLAUDE.md` into the workspace root if a `CLAUDE.md` already exists.
2. Keep the workflow and polish files in a stable prompt path.
3. Set the output directory before the first run.
4. Disable git publish until the target repo policy is clear.

## Notes

- Treat the workflow files as prompt modules if no formal skill registry exists.
- Do not hardcode private paths in shared versions.
- Return `DONE_WITH_GAPS` when the PRD is actionable but incomplete.
