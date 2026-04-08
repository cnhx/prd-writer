# Install the OpenClaw Adapter

## Files to Copy

- `platforms/openclaw/AGENT.md` -> import into the target agent definition area
- `platforms/openclaw/prd-workflow.md` -> import as the main workflow
- `platforms/openclaw/opus-prd-polish.md` -> import if polish is enabled
- `platforms/openclaw/config.example.yaml` -> copy and rename for local use

## Recommended Setup

1. Keep the imported workflow and polish files versioned with the workspace.
2. Set the output directory before the first run.
3. Disable git publish until the target repo policy is clear.
4. Keep knowledge base access optional.

## Notes

- Do not hardcode private vault paths in shared versions.
- Keep publish behavior config-driven.
- Return `DONE_WITH_GAPS` when the draft is usable but still missing confirmed facts.
