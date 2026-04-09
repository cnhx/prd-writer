# PRD Writer

Skill collection for structured PRD authoring. 5-phase workflow, optional Opus polish, optional idea stress-testing.

## Install (Claude Code)

```sh
cd ~/.claude/skills
git clone <repo-url> prd-writer

# 创建子 skill symlink
ln -s prd-writer/write-prd write-prd
ln -s prd-writer/prd-refine prd-refine
ln -s prd-writer/grill-me grill-me
ln -s prd-writer/opus-prd-polish opus-prd-polish
```

Verify installation:

```sh
bash ~/.claude/skills/prd-writer/scripts/setup-dependencies.sh
```

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
