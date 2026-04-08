# Install in OpenClaw

The ready-to-copy OpenClaw adapter lives in `platforms/openclaw/`.

## Recommended Setup

1. Place `platforms/openclaw/AGENT.md` in the target workspace or agent definition area.
2. Import `platforms/openclaw/prd-workflow.md` as the main PRD writing workflow.
3. Import `platforms/openclaw/opus-prd-polish.md` as an optional post-review skill.
4. Copy `platforms/openclaw/config.example.yaml` and map it to your OpenClaw config style.

## Notes

- Obsidian access should be treated as optional.
- Do not hardcode private vault paths in the published version.
- git commit should only run when the project config enables it.
