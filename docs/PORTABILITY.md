# Portability Notes

## Skill-Based Architecture

prd-writer is a skill collection. On Claude Code, install via `git clone` into `~/.claude/skills/`. On other platforms, copy the skill markdown files and use them as prompt modules.

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
