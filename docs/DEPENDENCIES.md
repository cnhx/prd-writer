# Dependencies

## Dependency Model

prd-writer uses a simple dependency model with two categories:

### Bundled

Skills included in this repo. After cloning, create symlinks to expose them to Claude Code (see README for commands).

| Skill | Purpose |
|-------|---------|
| write-prd | 5-phase PRD workflow |
| prd-refine | Quick PRD editing |
| opus-prd-polish | Final top-tier polish pass (uses highest-reasoning model available) |
| grill-me | Idea and plan stress-testing |

### External

Skills that live in separate repos. Install them independently.

| Skill | Purpose | Required? |
|-------|---------|-----------|
| gstack | Headless browser QA, design review, deployment verification | Optional |
| excalidraw-diagram | UI wireframe generation in Obsidian Excalidraw format (Phase 3.5) | Optional |
| mermaid-visualizer | Syntax-validated Mermaid diagram generation (Phase 3.5) | Optional |

## How Dependencies Are Declared

The root `SKILL.md` frontmatter includes a `dependencies` field listing external skill names. This follows the same convention used by gstack and other Claude Code skill projects.

```yaml
dependencies:
  - gstack
optional-dependencies:
  - excalidraw-diagram
  - mermaid-visualizer
```

Claude Code does not resolve these automatically. The `scripts/setup-dependencies.sh` script checks whether dependencies are installed and prints fix commands for anything missing.

## Adding a New Dependency

1. Add the skill name to the `dependencies` list in `SKILL.md` frontmatter
2. Add a check for it in `scripts/setup-dependencies.sh`
3. Document it in this file

## Model-Selection Frontmatter Keys (optional)

Individual skill `SKILL.md` files may declare preferred models via two optional keys:

```yaml
preferred-tier: top-reasoning    # semantic tier — future-proof, preferred selector
preferred-models:                # concrete IDs known to satisfy the tier today
  - claude-opus-4-6
  - claude-opus-4-5
```

- `preferred-tier` is the canonical selector. Harnesses that don't understand the tier
  name should fall back to `preferred-models`.
- Neither key is a hard dependency — they are hints. Any model in the stated tier is
  acceptable. Skills that use these keys must also define a graceful fallback path
  (see `opus-prd-polish/SKILL.md` for the reference implementation).
- Defined tiers: `top-reasoning` (Opus-class / equivalent frontier). Add new tiers here
  as the repo adopts them.
