# PRD Writer

Skill collection for structured PRD authoring. 5-phase workflow, optional Opus polish, optional idea stress-testing.

## Install (Claude Code)

Two install patterns are supported. Pick one.

### Pattern A — clone directly into the skills directory

```sh
cd ~/.claude/skills
git clone <repo-url> prd-writer

# 子 skill symlink（绝对路径，和 setup 脚本保持一致）
ln -s ~/.claude/skills/prd-writer/write-prd       ~/.claude/skills/write-prd
ln -s ~/.claude/skills/prd-writer/prd-refine      ~/.claude/skills/prd-refine
ln -s ~/.claude/skills/prd-writer/grill-me        ~/.claude/skills/grill-me
ln -s ~/.claude/skills/prd-writer/opus-prd-polish ~/.claude/skills/opus-prd-polish
```

### Pattern B — clone elsewhere, symlink into the skills directory

```sh
git clone <repo-url> ~/path/to/prd-writer

ln -s ~/path/to/prd-writer                   ~/.claude/skills/prd-writer
ln -s ~/path/to/prd-writer/write-prd         ~/.claude/skills/write-prd
ln -s ~/path/to/prd-writer/prd-refine        ~/.claude/skills/prd-refine
ln -s ~/path/to/prd-writer/grill-me          ~/.claude/skills/grill-me
ln -s ~/path/to/prd-writer/opus-prd-polish   ~/.claude/skills/opus-prd-polish
```

### Verify

For Pattern A (repo lives at `~/.claude/skills/prd-writer`):

```sh
bash ~/.claude/skills/prd-writer/scripts/setup-dependencies.sh
```

For Pattern B, substitute your actual clone path:

```sh
bash ~/path/to/prd-writer/scripts/setup-dependencies.sh
```

The script prints exact `ln -s` commands for anything missing — copy and run them.

## Install (Other Platforms)

- Codex: see `platforms/codex/INSTALL.md`
- OpenClaw: see `platforms/openclaw/INSTALL.md`

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `/write-prd` | "write a PRD", "create product requirements" | Full 5-phase PRD workflow |
| `/prd-refine` | "refine this PRD", "polish the PRD" | Quick edit pass, preserves detail |
| `/opus-prd-polish` | "opus polish", "final polish" | Opus-grade clarity and structure pass |
| `/grill-me` | "grill me", "stress-test this" | Relentless interrogation of a plan or idea |

## Usage

```
/write-prd [brief file or topic]
```

The workflow will:
1. Load context from files or user input
2. Optionally offer `/grill-me` if the idea is vague
3. Ask one question at a time about market, users, scope, business model
4. Present assumptions and implementation options
5. Draft a structured PRD with 14 sections
6. Review against a quality checklist
7. Optionally polish with Opus and commit

## Dependencies

**Bundled**: write-prd, prd-refine, opus-prd-polish, grill-me

**External (optional)**: [gstack](https://github.com/gstackio/gstack) — for QA, design review, deployment verification

See `docs/DEPENDENCIES.md` for details.

## Design Rules

- Never fabricate RTP, odds, regulatory, or market facts
- Assumptions and confirmed facts must be visually distinct
- Every variable/state/event/config field gets a readable English identifier
- Art/design requirements stay in a dedicated section
- Output language follows user preference

## Contributing

Keep it small and portable. See `CONTRIBUTING.md`.

## License

MIT
