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

## How Dependencies Are Declared

The root `SKILL.md` frontmatter includes a `dependencies` field listing external skill names. This follows the same convention used by gstack and other Claude Code skill projects.

```yaml
dependencies:
  - gstack
```

Claude Code does not resolve these automatically. The `scripts/setup-dependencies.sh` script checks whether dependencies are installed and prints fix commands for anything missing.

## Adding a New Dependency

1. Add the skill name to the `dependencies` list in `SKILL.md` frontmatter
2. Add a check for it in `scripts/setup-dependencies.sh`
3. Document it in this file
