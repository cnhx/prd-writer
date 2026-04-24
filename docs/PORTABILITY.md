# Portability Notes

## Skill-Based Architecture

prd-writer is a skill collection and Cowork-compatible plugin. On Claude Code, install via `git clone` into `~/.claude/skills/`. On Claude Cowork, install as a plugin from the Customize menu. On other platforms, copy the skill markdown files and use them as prompt modules.

## What Is Portable

Portable:
- PRD workflow phases and question themes
- Review checklist
- Drafting rules (English identifiers, art/design separation, uncertainty marking)
- Skill content (standard markdown with YAML frontmatter)

Platform-specific:
- Installation method (clone + symlink vs. manual copy)
- Tool names and invocation syntax
- Skill discovery mechanism
- Git execution environment

## Cross-Platform Usage

### Claude Code

Clone to `~/.claude/skills/prd-writer/` and create symlinks. Skills are discovered automatically. See `README.md` for install commands.

### Claude Cowork

Install as a plugin via Claude Desktop → Cowork → Customize → Add plugin. The repo includes `.claude-plugin/plugin.json` for plugin discovery and `commands/` for Cowork slash commands. Skills and commands share the same SKILL.md files — no duplication. See `platforms/cowork/INSTALL.md`.

### Codex

Copy skill markdown files into your project as prompt modules. See `platforms/codex/INSTALL.md`.

### OpenClaw

Copy skill markdown files into your agent workspace. See `platforms/openclaw/INSTALL.md`.

## YAML Frontmatter

Each skill file starts with YAML frontmatter (`---name: ...---`). On Claude Code this is parsed for skill discovery. On other platforms it is harmless metadata that can be ignored or stripped.

## Release Checklist

Before publishing:
- No private file paths are hardcoded
- All optional dependencies degrade gracefully if missing
- Examples do not expose internal company data
- Skill content is written in English (output language not forced)
