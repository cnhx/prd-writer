# Install in Hermes

## Recommended Setup

1. Add `agent/PRD-AGENT.md` to the Hermes workspace or agent identity layer.
2. Use `skills/prd-workflow.md` as the core PRD workflow reference.
3. Use `skills/opus-prd-polish.md` as the final polish module.
4. Adapt `config/prd-agent.example.yaml` to local workspace conventions.

## Hermes Notes

- Keep platform-specific tool names outside the portable agent definition when possible.
- If an Obsidian vault exists, wire it through config. Otherwise leave it disabled.
- If the repo is dirty or not versioned, return a suggested commit message instead of forcing git commit.
