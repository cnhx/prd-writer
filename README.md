# PRD Writer

Portable PRD writer kit for structured product requirement writing.

This package separates three layers:

1. agent definition — stable behavior, rules, dependencies, output contract
2. workflow skills — question flow, PRD template, review checklist, save/publish sequence
3. platform config — knowledge base, model preference, publish policy, capability mapping

Goals:
- portable across Hermes, OpenClaw, and Claude Code
- Obsidian knowledge base is optional, not required
- Opus polish is recommended but configurable
- git commit is configurable, not mandatory
- output language is not forced; follow user preference or runtime context

## Included Files

- `agent/PRD-AGENT.md`
- `skills/prd-workflow.md`
- `skills/opus-prd-polish.md`
- `config/prd-agent.example.yaml`
- `config/claude-code.example.yaml`
- `config/openclaw.example.yaml`
- `config/hermes.example.yaml`
- `docs/PORTABILITY.md`
- `docs/INSTALL-CLAUDE-CODE.md`
- `docs/INSTALL-OPENCLAW.md`
- `docs/INSTALL-HERMES.md`
- `examples/sample-input-brief.md`
- `examples/sample-output-prd.md`
- `examples/sample-invocation.md`
- `LICENSE`
- `CHANGELOG.md`

## Fast Start

1. Copy `agent/PRD-AGENT.md` into your agent workspace
2. Copy the workflow skills or translate them into your platform's prompt/skill format
3. Start from `config/prd-agent.example.yaml`
4. Decide whether to enable:
   - knowledge base
   - Opus polish
   - git commit

## Design Principles

- Never invent RTP, odds, or regulatory facts
- Variables and states must have readable English names
- Art requirements live in a dedicated section, never mixed into feature requirements
- Long PRDs should be written to file, not dumped into chat
- Missing info should produce `DONE_WITH_GAPS`, not fiction
- Output language should remain configurable and user-led

## Release Checklist

Before publishing:
- remove private vault paths
- keep Obsidian optional
- keep git commit optional
- provide a fallback when Opus is unavailable
- avoid platform-exclusive dependency names
