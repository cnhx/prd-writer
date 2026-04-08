# Install the Codex Adapter

## Files to Copy

- `platforms/codex/AGENTS.md` -> `AGENTS.md`
- `platforms/codex/prd-workflow.md` -> keep in the workspace
- `platforms/codex/opus-prd-polish.md` -> keep in the workspace if polish is enabled
- `platforms/codex/config.example.yaml` -> copy and rename for local use
- `platforms/codex/sample-invocation.md` -> use as the first run prompt

## Recommended Setup

1. Merge `platforms/codex/AGENTS.md` into the workspace root instructions if `AGENTS.md` already exists.
2. Keep the workflow and polish files in a stable path that the workspace can reference.
3. Set the output directory before the first run.
4. Disable git publish until the target repo policy is clear.
5. Start from `platforms/codex/sample-invocation.md` and pair it with `examples/sample-input-brief.md`.

## Suggested Invocation

- load the brief and local docs
- run the question flow from `prd-workflow.md`
- write the draft to a markdown file
- run the review checklist
- run the optional polish pass
- save and optionally commit

## Notes

- Do not hardcode private vault paths.
- Prefer local files over external assumptions.
- Return `DONE_WITH_GAPS` when the PRD is usable but incomplete.
