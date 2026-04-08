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
