---
name: prd-writer
version: 0.10.0
description: |
  PRD writing toolkit for games, AI agents, SaaS/Ops tools, data products, platform products,
  growth products, and learning/content products. Structured workflow with mandatory
  out-of-scope boundary scan, implementation-detail boundary, product-type router, research
  evidence pack, condition consolidation, exception coverage, terminology-with-example rule,
  grill-driven review, inline Mermaid diagram studio, export profiles for Obsidian MD / Word /
  PDF, and a scoring skill for Ready-to-Dev readiness.
  Use to write new PRDs, refine existing ones, split audience-specific docs, or pressure-test ideas.
  Trigger: write PRD, PRD workflow, product requirements document, 写 PRD, 产品需求文档.
  Compatible with Claude Code, Claude Cowork, Codex, OpenClaw, and Hermes prompt-module workflows.
dependencies:
  - gstack
---

# PRD Writer

Skill collection for structured PRD authoring.

## Counterintuitive rules (prioritize before regular rules)

These five rules, applied early, preempt the most common reasons PRDs get rejected in
real review cycles. They override the temptation to jump straight into feature lists.

1. **Write the Rejection Letter first.** Before drafting, list the 3–5 reasons
   real stakeholders (leadership, engineering lead, compliance, finance, GTM)
   would reject this PRD. Design the PRD to address each one explicitly. This is
   operationalized in `/write-prd` Phase 0.5 Part A.
2. **Narrow MVP claim before broad vision.** Define the smallest verifiable scope
   first. Later phases are `conditional_on_phase_1_learnings`, not promises.
3. **Design kill criteria before features.** If a feature cannot be cleanly cut
   from scope without destroying the PRD's point, its value claim is probably weak.
4. **Allocate engineering budget to decisive evidence, not polish.** One crude
   prototype that answers "is our hypothesis true?" beats three finely-crafted
   features that don't touch the core assumption.
5. **Predefine a fallback narrative.** If the primary KPI underperforms, name the
   secondary value (retention, cost reduction, learning) in advance, so the work is
   not retroactively judged a failure.

See [references/counterintuitive-prd.md](references/counterintuitive-prd.md) for
before/after examples of each rule.

## Sub-skills

| Skill | Description |
|-------|-------------|
| `/write-prd` | 5-phase PRD workflow: context loading, product-type routing, evidence pack, implementation-detail boundary, interrogation, premise check, drafting (with condition tables, exception coverage, inline diagrams, and export profile), grill-driven review |
| `/prd-refine` | Quick PRD polish — edit immediately, preserve detail, no planning |
| `/opus-prd-polish` | Final top-tier polish pass before publish (uses highest-reasoning model available) |
| `/grill-me` | Stress-test a plan or idea via relentless interrogation |
| `/prd-score` | Score a PRD against Ready-to-Dev rubric, implementation leakage, atomic pressure, condition consolidation, exception coverage, evidence coverage, diagram integrity, and export readiness |
| `/prd-split` | Split a PRD into audience-specific requirement documents. Game projects can use GDD/TDD/Art/BD; non-game projects use packs such as Agent Spec, Eval Plan, Workflow Spec, Permission Matrix, Metric Dictionary, API Contract Summary, or Experiment Brief |

## Design rules

- Never invent RTP, odds, regulatory facts, or market data
- Keep assumptions separate from confirmed facts
- Art/design requirements stay in their own section
- Write long PRDs to file, not chat
- Uncertain facts marked `to_be_confirmed` or `pending_math_table`
- PRDs describe product contracts, not implementation designs. Default to
  `semantic_contract_only`; avoid Redis, database schema, cache/queue design,
  service boundaries, framework choices, SDK choices, and deployment topology
  unless the user explicitly confirms they belong in this artifact.
- Avoid atomic implementation language. Describe the user-visible outcome,
  decision rule, or acceptance criterion instead of forcing internal task
  decomposition.
- Consolidate complex judgment logic into decision tables. Do not scatter the
  same condition across nested bullets or multiple sections.
- Every core flow needs normal and exception paths, including failure, recovery,
  and user-visible messaging.
- Detect and record `product_type` before drafting. Supported first-class types:
  `game_interactive`, `ai_agent`, `b2b_saas_ops`, `data_analytics`,
  `platform_marketplace`, `consumer_growth`, `content_learning`, and `mixed`.
- Record a `research_pack` when the user supplies interviews, tickets, analytics,
  market notes, competitor pages, screenshots, Confluence/Jira/Slack refs, or other evidence.
- Diagrams are inline Mermaid only. Flows, sequences, wireframes, architectures,
  journey maps, permission maps, decision loops, evaluation loops, and growth loops
  all go in ` ```mermaid ` code fences; no external diagram tools required.
- Record `output_profile` as `obsidian_md`, `word_docx`, `pdf`, `confluence`,
  or `multi`. Markdown remains the source of truth; exports must preserve
  headings, tables, Mermaid source blocks, and source references.

### Language policy (two-tier)

1. **Prose + section titles** — follow user preference (中文 / English / other). Not forced.
2. **Variables, states, events, config fields, API identifiers** — **always English**, regardless of prose language. This is non-negotiable; it keeps the PRD implementable across teams.

Example in a Chinese PRD:
> ## 功能需求
> - 状态机：`idle` → `spinning` → `settling` → `payout`
> - 事件：`on_spin_start`、`on_reel_stop`
> - 配置字段：`reel_count`、`rtp_target`

## Dependencies

**Bundled** (included in this repo):
- write-prd, prd-refine, opus-prd-polish, grill-me, prd-score

**External** (install separately):
- [gstack](https://github.com/gstackio/gstack) — headless browser QA, design review, deployment verification

Phase 3.5 diagrams use only inline Mermaid (rendered natively by GitHub, Obsidian,
and VS Code). Word/PDF/Confluence users can export rendered diagrams from
Obsidian or keep the Mermaid source next to exported static images. No external
diagram skill is required.
