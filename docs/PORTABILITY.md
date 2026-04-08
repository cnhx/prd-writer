# Portability Notes

## What Is Portable

Portable:
- agent mission and rules
- PRD workflow phases
- review checklist
- output contract
- optional configuration model

Platform-specific:
- file search tools
- knowledge base connectors
- model invocation syntax
- skill installation method
- git command execution environment
- workspace instruction file names and merge strategy

## Platform-Ready Adapters

This repository now ships platform-ready adapters under:

- `platforms/codex/`
- `platforms/claude-code/`
- `platforms/openclaw/`

Each adapter should provide:

- a platform-native agent instruction file
- a PRD workflow prompt or skill file
- an optional polish prompt
- a platform-specific config example
- an install guide that explains what to copy and what to merge

Keep these parts aligned across all adapters:

- mission and non-negotiable rules
- workflow phases
- review checklist
- output contract
- fallback handling for missing knowledge base, polish, and git publish

Adapt only the parts that are genuinely platform-specific:

- file names such as `AGENTS.md` or `CLAUDE.md`
- where the agent instructions live
- whether workflow files are imported as skills or kept as prompt modules
- how optional polish is triggered
- how git commit is described in that environment

## Minimal Cross-Platform Mode

A valid minimal setup requires only:
- one capable model
- local file access or pasted context
- markdown output

Optional modules:
- Obsidian vault access
- Opus polish
- git commit

## Release Checklist

Before publishing this kit externally, verify:
- no private file paths are hardcoded
- Obsidian is optional
- git commit is optional
- Opus is optional or has fallback
- examples do not expose internal company data
- dependency names are abstract enough to remap
- platform adapters do not contradict the portable core
