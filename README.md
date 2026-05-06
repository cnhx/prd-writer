# PRD Writer

Skill collection for structured PRD authoring across games, AI agents, SaaS/Ops tools, data products, platform products, growth products, and learning/content products. Markdown is the source of truth; Obsidian MD, Word, and PDF workflows are supported through export profiles.

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
ln -s ~/.claude/skills/prd-writer/prd-score       ~/.claude/skills/prd-score
ln -s ~/.claude/skills/prd-writer/prd-split       ~/.claude/skills/prd-split
```

### Pattern B — clone elsewhere, symlink into the skills directory

```sh
git clone <repo-url> ~/path/to/prd-writer

ln -s ~/path/to/prd-writer                   ~/.claude/skills/prd-writer
ln -s ~/path/to/prd-writer/write-prd         ~/.claude/skills/write-prd
ln -s ~/path/to/prd-writer/prd-refine        ~/.claude/skills/prd-refine
ln -s ~/path/to/prd-writer/grill-me          ~/.claude/skills/grill-me
ln -s ~/path/to/prd-writer/opus-prd-polish   ~/.claude/skills/opus-prd-polish
ln -s ~/path/to/prd-writer/prd-score         ~/.claude/skills/prd-score
ln -s ~/path/to/prd-writer/prd-split         ~/.claude/skills/prd-split
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

## Install (Claude Cowork)

Install as a plugin in Claude Desktop → Cowork → Customize → Add plugin → From GitHub. All commands are registered automatically. See `platforms/cowork/INSTALL.md` for details.

## Install (Other Platforms)

- Claude Cowork: see `platforms/cowork/INSTALL.md`
- Codex: see `platforms/codex/INSTALL.md`
- OpenClaw: see `platforms/openclaw/INSTALL.md`
- Hermes: see `platforms/hermes/INSTALL.md`

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `/write-prd` | "write a PRD", "create product requirements" | Full PRD workflow with product-type router, evidence pack, implementation-detail boundary, exception coverage, diagrams, and export profile |
| `/prd-refine` | "refine this PRD", "polish the PRD" | Quick edit pass, preserves detail |
| `/opus-prd-polish` | "opus polish", "final polish" | Top-tier clarity and structure pass (uses highest-reasoning model available) |
| `/grill-me` | "grill me", "stress-test this" | Relentless interrogation of a plan or idea |
| `/prd-score` | "score this PRD", "readiness check" | Score structure, owner closure, scope boundaries, implementation leakage, condition consolidation, exception coverage, evidence, diagrams, and export readiness |
| `/prd-split` | "split PRD", "generate GDD", "audience docs" | Split PRD into audience-specific docs. Game projects use GDD/TDD/Art/BD; non-game projects use product-type packs |

## Supported Product Types

| Type | Use for | Extra output packs |
|---|---|---|
| `game_interactive` | slots, crash games, social games, interactive experiences | GDD, TDD, Art & Audio, BD & Marketing |
| `ai_agent` | internal agents, coding/design/support agents, workflow automation | Agent Behavior Spec, Eval Plan, Human Review Playbook, Risk Brief |
| `b2b_saas_ops` | CRM, approval flows, admin consoles, internal tools | Workflow Spec, Role & Permission Matrix, Support Runbook, Release Brief |
| `data_analytics` | dashboards, reports, experiments, monitoring | Metric Dictionary, Decision Guide, Data Quality Checklist |
| `platform_marketplace` | APIs, plugin markets, partner networks, B2B2C platforms | Partner Brief, API Contract Summary, Trust & Safety Brief |
| `consumer_growth` | mobile apps, communities, lifecycle, referrals, memberships | Experiment Brief, Lifecycle Messaging Brief, Design Brief |
| `content_learning` | courses, knowledge bases, AI tutors, training tools | Learning Outcome Map, Content Rubric, Feedback Loop Spec |

## Usage

```
/write-prd [brief file or topic]
```

The workflow will:
1. Load context from files or user input
2. Detect product type and output profile (`obsidian_md`, `word_docx`, `pdf`, `confluence`, or `multi`)
3. Build a research pack when evidence is supplied
4. Optionally offer `/grill-me` or a short Concept Lab if the idea is vague
5. Ask one question at a time about market, users, scope, business model, risk, and product-type specifics
6. Draft a structured PRD with implementation details downgraded to product contracts, complex conditions consolidated into tables, exception paths covered, and inline Mermaid diagrams when useful
7. Review against a quality checklist, then optionally run `/opus-prd-polish`, `/prd-score`, and `/prd-split`

## Format Support

- **Obsidian MD**: Markdown remains the canonical artifact. Use relative links, wiki links only when the target vault expects them, and inline Mermaid fences for diagrams.
- **Word**: Keep heading levels strict, tables simple, and Mermaid source blocks next to any exported diagram images. Do not use HTML-only layout.
- **PDF**: Use stable headings, captions, page-friendly tables, and section-level diagram titles. If Mermaid rendering is unavailable, keep source fences in the PDF appendix.
- **Confluence**: Keep headings H1-H3, tables simple, links explicit, and Mermaid diagrams paired with an exported image attachment plus the source block. Do not rely on Obsidian wiki links or raw HTML.

## Examples

- `examples/sample-output-prd.md`: game / interactive PRD with Mermaid state and wireframe diagrams.
- `examples/sample-ai-agent-prd.md`: AI agent PRD with autonomy boundary, tool-call sequence, eval loop, and `multi` export profile.
- `examples/sample-saas-ops-prd.md`: B2B SaaS/Ops PRD with workflow state map, role-permission map, and `obsidian_md` profile.

## Dependencies

**Bundled**: write-prd, prd-refine, opus-prd-polish, grill-me, prd-score, prd-split

**External (optional)**: [gstack](https://github.com/gstackio/gstack) — for QA, design review, deployment verification

See `docs/DEPENDENCIES.md` for details.

## Design Rules

- Never fabricate RTP, odds, regulatory, or market facts
- Assumptions and confirmed facts must be visually distinct
- Every variable/state/event/config field gets a readable English identifier
- Art/design requirements stay in a dedicated section
- Product type and output profile must be recorded near the top of every generated PRD
- PRDs default to `semantic_contract_only`; do not prescribe Redis, database schema, cache/queue design, service boundaries, framework choices, SDK choices, or deployment topology unless explicitly requested
- Avoid atomic implementation language; describe user-visible outcomes and acceptance criteria instead
- Complex decision logic belongs in decision tables, not scattered nested bullets
- Every core flow needs normal and exception paths with recovery and user-visible messaging
- Output language follows user preference

## Contributing

Keep it small and portable. See `CONTRIBUTING.md`.

## License

MIT
