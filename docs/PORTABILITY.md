# Portability Notes

## Skill-Based Architecture

prd-writer is a skill collection and Cowork-compatible plugin. On Claude Code,
install via `git clone` into `~/.claude/skills/`. On Claude Cowork, install as a
plugin from the Customize menu. On Codex, OpenClaw, Hermes, and similar agents,
copy the skill markdown files and use them as prompt modules.

## What Is Portable

Portable:
- PRD workflow phases and question themes
- Product-type router (`game_interactive`, `ai_agent`, `b2b_saas_ops`,
  `data_analytics`, `platform_marketplace`, `consumer_growth`, `content_learning`)
- Research pack metadata and evidence labels
- Review checklist
- Drafting rules (English identifiers, art/design separation, uncertainty marking)
- Inline Mermaid diagram source
- Audience split pack definitions
- Output profile rules for Obsidian MD, Word, and PDF
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

### Hermes

Copy skill markdown files into your Hermes workspace as prompt modules. See
`platforms/hermes/INSTALL.md`.

## Format Portability

Markdown stays the canonical artifact. Use `output_profile` to tune the same PRD
for downstream review:

| output_profile | Portable behavior |
|---|---|
| `obsidian_md` | Relative links, inline Mermaid, no raw HTML dependency |
| `word_docx` | Strict heading levels, narrow tables, diagram captions |
| `pdf` | Page-friendly tables, titled diagrams, Mermaid source kept if rendering is unavailable |
| `confluence` | H1-H3 headings, simple tables, explicit links, diagram attachment notes plus Mermaid source |
| `multi` | Markdown first, with Word/PDF/Confluence export notes where needed |

## YAML Frontmatter

Each skill file starts with YAML frontmatter (`---name: ...---`). On Claude Code this is parsed for skill discovery. On other platforms it is harmless metadata that can be ignored or stripped.

## Release Checklist

Before publishing:
- No private file paths are hardcoded
- All optional dependencies degrade gracefully if missing
- Examples do not expose internal company data
- Skill content is written in English (output language not forced)
- Product-type, evidence, diagram, and export-profile metadata are present in samples
