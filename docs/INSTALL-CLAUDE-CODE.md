# Install in Claude Code

## Recommended Setup

1. Copy `agent/PRD-AGENT.md` into your Claude Code workspace as the PRD agent definition.
2. Convert `skills/prd-workflow.md` into either:
   - a reusable prompt file, or
   - a local skill if your Claude Code setup supports it.
3. Convert `skills/opus-prd-polish.md` into a final review prompt.
4. Start from `config/prd-agent.example.yaml` and adapt paths.

## Minimum Working Mode

Set:
- knowledge_base.enabled = false
- publish.git_commit = false
- polish.enabled = true or false based on your Opus access

## Suggested Invocation Pattern

- run context loading
- ask one question at a time
- draft PRD to file
- run review checklist
- run optional Opus polish
- save and optionally commit

## Compatibility Notes

Claude Code users may not have a formal skill registry. In that case, treat the files in `/skills` as prompt modules, not installable packages.
