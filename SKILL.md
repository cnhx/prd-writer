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
- Every variable, state, event, config field gets a readable English identifier
- Art/design requirements stay in their own section
- Write long PRDs to file, not chat
- Uncertain facts marked `to_be_confirmed` or `pending_math_table`
- Output language follows user preference, not forced

## Dependencies

**Bundled** (included in this repo):
- write-prd, prd-refine, opus-prd-polish, grill-me

**External** (install separately):
- [gstack](https://github.com/gstackio/gstack) — headless browser QA, design review, deployment verification
