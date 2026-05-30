# PRD Writer

**English** | [中文](README.zh-CN.md)

Skill collection for structured PRD authoring across games, AI agents, SaaS/Ops tools, data products, platform products, growth products, and learning/content products. Markdown is the source of truth; Obsidian MD, Word, PDF, and HTML workflows are supported through export profiles. Includes optional HTML PRD export with Mermaid rendering and interactive HTML mockup prototype generation.

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

### Auto-update on startup

To let Claude Code and Codex update this skill when a new session starts, run:

```sh
bash ~/.claude/skills/prd-writer/scripts/install-auto-update-hooks.sh
```

For Pattern B, substitute your actual clone path. The hook runs
`scripts/update-skill.sh --auto`: it fetches the configured upstream and applies
only clean fast-forward updates. If the repo has local changes, is ahead, has
diverged, lacks an upstream, or cannot fetch, it skips and reports the reason.
Checks are throttled to once every 6 hours by default.

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
1. **First-run config**: on the first invocation, ask the user to choose the document output language (stored in `~/.prd-writer/config.json`, only asked once)
2. **Context loading**: load context from files, sibling PRDs, memory, or user input
3. **Product type detection**: detect product type and output profile (`obsidian_md`, `word_docx`, `pdf`, `confluence`, or `multi`)
4. **Research pack**: build an evidence table when the user supplies research data
5. **Optional stress-test**: offer `/grill-me` or a short Concept Lab if the idea is vague
6. **Product interrogation**: ask one question at a time about market, users, scope, business model, risk, and product-type specifics
7. **PRD drafting**: draft a structured PRD with implementation details downgraded to product contracts, complex conditions consolidated into tables, exception paths covered, and inline Mermaid diagrams when useful
8. **Review**: grill-driven review against a quality checklist
9. **Polish and publish**: optionally run `/opus-prd-polish` and `/prd-score`
10. **Audience split** (optional): auto-invoke `/prd-split` to generate audience-specific documents (GDD, TDD, Agent Spec, etc.)
11. **HTML PRD export** (optional): generate self-contained `.html` files for browser viewing. If audience split ran, generates HTML for each split document as well, with cross-navigation links between them. Includes Mermaid diagram rendering, styled metadata cards, auto-generated TOC, and print-friendly layout
12. **HTML mockup** (optional, only for multi-screen products): generate an interactive single-frame prototype with two views — an **Interactive Prototype** tab (click through the product flow in one simulated device frame) and an **All Screens Overview** tab (thumbnails of every state in a grid, clickable to jump into interactive mode)

## Format Support

- **Obsidian MD**: Markdown remains the canonical artifact. Use relative links, wiki links only when the target vault expects them, and inline Mermaid fences for diagrams.
- **Word**: Keep heading levels strict, tables simple, and Mermaid source blocks next to any exported diagram images. Do not use HTML-only layout.
- **PDF**: Use stable headings, captions, page-friendly tables, and section-level diagram titles. If Mermaid rendering is unavailable, keep source fences in the PDF appendix.
- **Confluence**: Keep headings H1-H3, tables simple, links explicit, and Mermaid diagrams paired with an exported image attachment plus the source block. Do not rely on Obsidian wiki links or raw HTML.
- **HTML** (Phase 5.6): Themed `.html` generated from the Markdown PRD by a vendored Python renderer (`scripts/prd-to-html.py`, needs `markdown` + `pyyaml` — `pip install -r scripts/requirements.txt`, Python 3.8+). Three-column editorial layout (section sidebar + body + mini-TOC), YAML metadata as styled cards, callouts, auto anchors, print-friendly. When audience split is enabled, generates HTML for each split document with cross-navigation links. Loads pinned `mermaid@11` + web fonts from CDN (renders offline with system-font fallback and no diagrams). If Python or the deps are unavailable, `/write-prd` falls back to hand-generated HTML automatically.
- **HTML Mockup** (Phase 5.7): Interactive prototype as a single `.html` file. One simulated device frame with state switching via button clicks. Dual-view: Interactive Prototype tab + All Screens Overview tab. Zero external dependencies. Only offered when the PRD describes multi-screen/multi-state products.

## Configuration

On the first run of `/write-prd`, the skill asks for the preferred document language and stores it in `~/.prd-writer/config.json`. This affects all prose output including HTML exports. Variable names, state names, and technical identifiers always stay in English regardless of this choice. The user can override per-session.

## Examples

- `examples/sample-output-prd.md`: game / interactive PRD with Mermaid state and wireframe diagrams.
- `examples/sample-ai-agent-prd.md`: AI agent PRD with autonomy boundary, tool-call sequence, eval loop, and `multi` export profile.
- `examples/sample-saas-ops-prd.md`: B2B SaaS/Ops PRD with workflow state map, role-permission map, and `obsidian_md` profile.

## Dependencies

**Bundled**: write-prd, prd-refine, opus-prd-polish, grill-me, prd-score, prd-split

**External (optional)**: [gstack](https://github.com/gstackio/gstack) — for QA, design review, deployment verification

See `docs/DEPENDENCIES.md` for details.

## Updates

- `scripts/update-skill.sh --check-only --force --verbose`: check whether the
  current clone is behind its upstream.
- `scripts/update-skill.sh --auto --force --verbose`: apply a safe
  fast-forward update immediately.
- `scripts/install-auto-update-hooks.sh`: register startup hooks in
  `~/.claude/settings.json` and `~/.codex/hooks.json`; for Codex it also enables
  `codex_hooks` in `~/.codex/config.toml`.

## Design Rules

- Never fabricate RTP, odds, regulatory, or market facts
- Assumptions and confirmed facts must be visually distinct
- Every variable/state/event/config field gets a readable English identifier
- Art/design requirements stay in a dedicated section
- Product type and output profile must be recorded near the top of every generated PRD
- PRDs default to `semantic_contract_only`; do not prescribe Redis, database schema, cache/queue design, service boundaries, framework choices, SDK choices, or deployment topology unless explicitly requested
- Avoid atomic implementation language; describe user-visible outcomes and acceptance criteria instead
- Avoid instruction-like wording in generated documents, especially flow and agent-behavior sections, so downstream AI systems do not mistake descriptive content for executable instructions
- Complex decision logic belongs in decision tables, not scattered nested bullets
- Every core flow needs normal and exception paths with recovery and user-visible messaging
- Output language follows user preference (configured on first run, stored in `~/.prd-writer/config.json`)
- HTML export generates per-split-doc files when audience split is enabled
- HTML mockup is an interactive prototype, not a static wireframe gallery

## Contributing

Keep it small and portable. See `CONTRIBUTING.md`.

## License

MIT
