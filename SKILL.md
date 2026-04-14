---
name: prd-writer
version: 0.6.0
description: |
  PRD writing toolkit. Structured 5-phase workflow with mandatory out-of-scope boundary scan,
  history alignment, terminology-with-example rule, grill-driven review, and a scoring skill
  for Ready-to-Dev readiness. Use to write new PRDs, refine existing ones, or pressure-test
  product ideas.
  Trigger: write PRD, PRD workflow, product requirements document, 写 PRD, 产品需求文档.
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
| `/write-prd` | 5-phase PRD workflow: context loading (with history + boundary scan), product interrogation, premise check, drafting, grill-driven review |
| `/prd-refine` | Quick PRD polish — edit immediately, preserve detail, no planning |
| `/opus-prd-polish` | Final top-tier polish pass before publish (uses highest-reasoning model available) |
| `/grill-me` | Stress-test a plan or idea via relentless interrogation |
| `/prd-score` | Score a PRD against Ready-to-Dev rubric (Structure, Owner Closure, Open Questions, verdict Green / Yellow / Red) |

## Design rules

- Never invent RTP, odds, regulatory facts, or market data
- Keep assumptions separate from confirmed facts
- Art/design requirements stay in their own section
- Write long PRDs to file, not chat
- Uncertain facts marked `to_be_confirmed` or `pending_math_table`

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
