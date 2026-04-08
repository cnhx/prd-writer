# Install in Claude Code

The ready-to-copy Claude Code adapter lives in `platforms/claude-code/`.

## Recommended Setup

1. Copy `platforms/claude-code/CLAUDE.md` into the target workspace root, or merge it into an existing `CLAUDE.md`.
2. Keep `platforms/claude-code/prd-workflow.md` available as a reusable prompt module or local skill.
3. Keep `platforms/claude-code/opus-prd-polish.md` as the optional final polish prompt.
4. Copy `platforms/claude-code/config.example.yaml` and adapt the paths and publish settings.

## Minimum Working Mode

Set:
- `knowledge_base.enabled = false`
- `publish.git_commit = false`
- `polish.enabled = false` if you do not have a higher-tier review pass

## Suggested Invocation Pattern

- run context loading
- ask one question at a time
- draft PRD to file
- run review checklist
- run optional Opus polish
- save and optionally commit

## Compatibility Notes

Claude Code users may not have a formal skill registry. In that case, treat the files in `platforms/claude-code/` as prompt modules, not installable packages.
