---
name: prd-writer
version: 0.5.0
description: |
  PRD writing toolkit. Structured 5-phase workflow, optional top-tier polish, optional grill-me
  stress-test. Use to write new PRDs, refine existing ones, or pressure-test product ideas.
  Trigger: write PRD, PRD workflow, product requirements document, 写 PRD, 产品需求文档.
dependencies:
  - gstack
---

# PRD Writer

Skill collection for structured PRD authoring.

## Sub-skills

| Skill | Description |
|-------|-------------|
| `/write-prd` | 5-phase PRD workflow: context loading, product interrogation, premise check, drafting, review |
| `/prd-refine` | Quick PRD polish — edit immediately, preserve detail, no planning |
| `/opus-prd-polish` | Final top-tier polish pass before publish (uses highest-reasoning model available) |
| `/grill-me` | Stress-test a plan or idea via relentless interrogation |

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

## Artifact flow

Explicit view of what each skill produces and consumes. Mirrors the handoff table
convention used in EvoSkills.

**Persistence levels:**
- **file** — written to disk, survives session restart and platform switch
- **embedded** — stored inside the PRD file itself (a section of `docs/prd/<name>.md`)
- **session** — lives only in the current conversation context; to hand off across
  sessions or platforms, promote to a file (see Cross-session handoff below)

| Artifact | Produced by | Consumed by | Persistence | Location |
|---|---|---|---|---|
| Rejection-preempt letter (3–5 predicted rejections + mitigations) | `/write-prd` Phase 0.5 Part A | `/write-prd` Phase 4.1 content check | **file** | `<prd-dir>/<name>-rejection-preempt.md`, linked from PRD |
| Grill-me consensus log (resolved branches + open questions) | `/grill-me` (optional) | `/write-prd` Phase 1.x | **session** | Conversation context only |
| Story summary (contribution / insight / challenge / framing) | `/write-prd` Phase 1.0 reverse-story | `/write-prd` Phase 3 §1 + §2 | **session → embedded** | Conversation during drafting, then embedded into PRD §1/§2 |
| Phase 2 premise output (3–5 assumptions + 2–3 options + recommendation) | `/write-prd` Phase 2 | `/write-prd` Phase 3 Drafting | **session → embedded** | Conversation during drafting, then embedded into PRD §1/§3/§12; see `examples/sample-phase2-premise.md` |
| Feature Trinity rows (user job / mechanism / success signal per feature) | `/write-prd` Phase 3 §5 | `/write-prd` Phase 4 Trinity check | **embedded** | Inside PRD §5, see `examples/sample-feature-trinity.md` |
| Full PRD draft | `/write-prd` Phase 3 | `/prd-refine`, `/opus-prd-polish` | **file** | `docs/prd/<name>.md` |
| Polished PRD + edit list + unresolved gaps | `/opus-prd-polish` | human review / commit | **file + session** | File overwrites `docs/prd/<name>.md`; edit list returned inline |

### Cross-session handoff

Artifacts marked **session** do **not** survive a new conversation or a platform
switch. If you pause between sub-skills or hand the work to a different agent,
promote the session artifact to a file first. Suggested locations:

- Grill-me consensus → `<prd-dir>/<name>-grill-log.md`
- Story summary → embed into an early draft of PRD §1 before pausing

Sub-skills are composable: `/grill-me` can run standalone for any plan, not just
PRDs. `/prd-refine` and `/opus-prd-polish` accept any PRD, not just ones produced
by `/write-prd`.

## Dependencies

**Bundled** (included in this repo):
- write-prd, prd-refine, opus-prd-polish, grill-me

**External** (install separately):
- [gstack](https://github.com/gstackio/gstack) — headless browser QA, design review, deployment verification
