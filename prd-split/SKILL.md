---
name: prd-split
description: |
  Split a unified PRD into audience-specific requirement documents with
  structured requirements tables. Game PRDs can produce GDD, TDD, Art & Audio,
  and BD & Marketing documents. Non-game PRDs use product-type packs such as
  Agent Behavior Spec, Eval Plan, Workflow Spec, Permission Matrix, Metric
  Dictionary, API Contract Summary, Experiment Brief, and Learning Outcome Map.
  Works standalone on any existing PRD, or auto-triggered from /write-prd Phase 5.5.
  Trigger: split PRD, audience docs, discipline docs, generate GDD, generate TDD,
  拆分 PRD, 生成需求表, audience 拆分, discipline 拆分.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# PRD Split

Split a unified PRD into audience-specific requirement documents. Each output
gets relevant sections extracted, structured requirements tables, and a
completeness summary.

## Audience Packs

The splitter first reads PRD metadata:

```yaml
product_type: ai_agent
audience_split:
  enabled: true
  packs: [agent_behavior_spec, eval_plan, human_review_playbook, risk_brief]
```

If a PRD only has the old `discipline_split` block, treat it as
`product_type: game_interactive` and preserve the older behavior.

### Game / Interactive Pack

| Discipline | Prefix | Owner label | Focus |
|---|---|---|---|
| GDD (Game Design Document) | `GDD` | Game Design | Gameplay flow, mechanics, math model, player experience |
| TDD (Technical Design Document) | `TDD` | Engineering | System architecture, API specs, data models, performance |
| Art & Audio | `ART` | Art Team | Visual art, animation, sound design, UI layout |
| BD & Marketing | `BDM` | BD/Marketing | Market strategy, positioning, compliance, KPIs |

### Product-Type Packs

| product_type | Pack | Prefix | Owner label | Focus |
|---|---|---|---|---|
| `ai_agent` | Agent Behavior Spec | `AGS` | Agent/Product | autonomy boundary, tools, inputs, outputs, refusal, recovery |
| `ai_agent` | Eval Plan | `EVL` | AI Evaluation | golden tasks, test sets, pass/fail criteria, sampling |
| `ai_agent` | Human Review Playbook | `HRP` | Operations/Review | approval paths, reviewer actions, escalation, rollback |
| `ai_agent` | Risk Brief | `RSK` | Risk/Compliance | hallucination, permission misuse, audit, stale context |
| `b2b_saas_ops` | Workflow Spec | `WFS` | Product/Ops | task flow, states, exceptions, notifications |
| `b2b_saas_ops` | Role & Permission Matrix | `RPM` | Admin/Security | roles, permissions, audit, data visibility |
| `b2b_saas_ops` | Support Runbook | `SRB` | Support/Ops | common failures, triage, user recovery |
| `b2b_saas_ops` | Release Brief | `RLB` | GTM/Release | rollout, migration, training, enablement |
| `data_analytics` | Metric Dictionary | `MTD` | Data | definitions, source tables, refresh, caveats |
| `data_analytics` | Decision Guide | `DCG` | Business Owner | signals, actions, thresholds, owner response |
| `data_analytics` | Data Quality Checklist | `DQC` | Data Engineering | freshness, completeness, lineage, alerting |
| `platform_marketplace` | Partner Brief | `PTB` | Partnerships | onboarding, incentives, requirements, launch |
| `platform_marketplace` | API Contract Summary | `API` | Engineering | endpoints/contracts at semantic level, versioning, migration |
| `platform_marketplace` | Trust & Safety Brief | `TST` | Trust/Safety | policy, abuse, review, enforcement |
| `consumer_growth` | Experiment Brief | `EXB` | Growth | hypothesis, cohort, guardrails, success metrics |
| `consumer_growth` | Lifecycle Messaging Brief | `LMB` | Lifecycle/GTM | triggers, channels, copy constraints, frequency |
| `consumer_growth` | Design Brief | `DSB` | Design | onboarding, activation, feedback, emotional beats |
| `content_learning` | Learning Outcome Map | `LOM` | Learning Design | outcomes, levels, activities, assessment |
| `content_learning` | Content Rubric | `CTR` | Content | quality bar, style, review, update cadence |
| `content_learning` | Feedback Loop Spec | `FLS` | Product/Learning | practice, feedback, remediation, retention |

## Game Section Mapping

| PRD Section | GDD | TDD | Art&Audio | BD&Mkt | Type |
|---|---|---|---|---|---|
| 1. Summary | ✓ | ✓ | ✓ | ✓ | crosscutting |
| 2. Project positioning | primary | — | — | primary | — |
| 3. Market strategy | — | — | — | primary | — |
| 4. Gameplay/product flow | primary | secondary | — | — | — |
| 5. Functional requirements | primary | secondary | — | — | — |
| 6. Art and design reqs | — | — | primary | — | — |
| 7. Math/business model | primary | — | — | secondary | — |
| 8. Compliance and risk | — | secondary | — | primary | — |
| 9. Technical considerations | — | primary | — | — | — |
| 10. KPI and success metrics | primary | — | — | primary | shared |
| 11. Milestones | ✓ | ✓ | ✓ | ✓ | crosscutting |
| 12. Assumptions | ✓ | ✓ | ✓ | ✓ | crosscutting |
| 13. Non-goals | ✓ | ✓ | ✓ | ✓ | crosscutting |
| 14. Sources | ✓ | ✓ | ✓ | ✓ | crosscutting |

Treatment by type:

- **primary**: full content + structured requirements table
- **secondary**: one-paragraph summary + reference to source PRD
- **crosscutting**: reproduced verbatim, no requirement extraction

## Phase 0 — Input and Configuration

1. Accept path to source PRD (required). If empty, ask for it.
2. Read the source PRD end-to-end.
3. Detect `product_type`, `audience_split`, and older `discipline_split`
   metadata. If missing, infer from headings/content and ask the user to confirm.
4. Detect the PRD's prose language (Chinese / English / other). All output
   prose follows source language; identifier columns (ID, Priority, Status)
   are always English.
5. Ask which packs to generate. Default comes from `audience_split.packs`; if
   unavailable, use the product-type default from the table above.
6. Ask for output directory (default: same directory as source PRD, in an
   `audience/` subdirectory; existing game-only projects may choose `disciplines/`).

When invoked from `/write-prd` Phase 5.5, the configuration comes from the
`audience_split` YAML block already recorded in Phase 0.4. Skip
interactive prompts — use the stored config directly.

## Phase 1 — Section Identification

1. Match H2 headers in the source PRD against the 14 known section names.
   Use fuzzy matching to handle variations:
   - "Tech Requirements" → "Technical considerations"
   - "Game Flow" → "Gameplay or product flow"
   - "美术需求" → "Art and design requirements"
2. Sections that cannot be matched: report to user and ask for manual
   classification to a pack (or skip).
3. Extract Mermaid code fences within each section. Route each diagram to
   the pack that owns the section as primary.
4. Detect `out_of_scope`, `research_pack`, `output_profile`, and
   `diagrams_generated` YAML blocks for propagation into output documents.

## Phase 2 — Requirements Extraction

For each selected pack's **primary** sections:

### 2.1 Extraction rules

Read the section prose and extract individual requirement statements.
A requirement is any of:

- An imperative or constraint ("must", "should", "players can")
- A state, event, or config declaration (`round_state`, `on_spin_start`)
- A quantitative target or threshold ("< 200ms", "≥ 95% uptime")
- An acceptance criterion or named flow step
- A visual/audio specification (color, layout, animation, SFX cue)

One requirement per row. Merge closely related sub-bullets into a single
row if they describe the same concern.

### 2.2 ID assignment

Pattern: `{PREFIX}-{SECTION_NUMBER}-{SEQ}`

- `GDD-4-001`, `GDD-4-002`, `GDD-5-001`
- `TDD-9-001`, `TDD-9-002`
- `ART-6-001`, `ART-6-002`
- `BDM-2-001`, `BDM-3-001`
- `AGS-5-001`, `EVL-10-001`, `RPM-5-001`, `MTD-7-001`

Sequence resets per section within a pack.

### 2.3 Priority inference

Infer from language in the source PRD:

| Source language signals | Priority |
|---|---|
| must, required, mandatory, critical, 必须, 强制 | P0 |
| should, expected, important, 应该, 建议 | P1 |
| may, optional, nice-to-have, conditional, 可选 | P2 |
| ambiguous or no signal | `to_be_confirmed` |

### 2.4 Default fields

- **Owner**: owner label from the selected pack table above
- **Status**: `draft`
- **Description**: use the source PRD's prose language

### 2.5 Requirements table format

```markdown
| ID | Section | Description | Priority | Owner | Status |
|---|---|---|---|---|---|
| GDD-4-001 | Gameplay flow | ... | P0 | Game Design | draft |
```

### 2.6 Ambiguous prose handling

If a section's prose is too narrative to extract structured requirements,
still attempt extraction but add a note:

```markdown
> ⚠ 本节内容为叙述性描述，需求提取为 best-effort，建议人工审核。
```

## Phase 3 — Document Assembly

For each selected pack:

### 3.1 YAML metadata block

```yaml
audience_split:
  pack: agent_behavior_spec
  product_type: ai_agent
  source_prd: <relative path to source PRD>
  source_prd_title: <H1 title from source>
  generated_at: <ISO 8601 timestamp>
  sections_primary: [4, 5, 7]
  sections_crosscutting: [1, 11, 12, 13, 14]
  sections_secondary: [8]
  requirements_extracted: <count>
  requirements_tbc: <count with to_be_confirmed fields>
```

### 3.2 Document structure

```markdown
# {Source PRD Title} — {Pack Name}

{YAML metadata block}

## Overview
{Summary section verbatim from source PRD}

## {Primary Section Title}
{Full content from source PRD, including Mermaid diagrams}

### Requirements
{Structured requirements table for this section}

## {Another Primary Section Title}
{Same treatment}

## Reference: {Secondary Section Title}
{One-paragraph summary} — See [source PRD](<path>) §{N} for full details.

## Context
### Milestones
{Verbatim from source}

### Assumptions
{Verbatim from source}

### Non-goals
{Verbatim from source}

### Sources
{Verbatim from source}

## Consolidated Requirements Table
{All requirement rows from all primary sections, merged into one table}

## Completeness Summary
- Requirements extracted: N
- to_be_confirmed items: M
- Mermaid diagrams carried: K
- Sections included: P primary + C crosscutting + S secondary
```

### 3.3 Propagation rules

- If source PRD has `out_of_scope` YAML, propagate it into each output
  document after the `audience_split` block.
- If source PRD has `research_pack`, propagate relevant evidence entries.
- If source PRD has `output_profile`, preserve it and add export notes only
  when the pack needs special handling for Word/PDF.
- If source PRD has `diagrams_generated` YAML, route each entry to the pack
  that owns that section as primary.
- If source PRD status is `DONE_WITH_GAPS`, carry the Known Gaps section
  into the relevant output document(s).

### 3.4 INDEX.md

```markdown
# Audience Split — {Source PRD Title}

Source: {path}
Generated: {timestamp}

| Pack | File | Requirements | TBC | Primary Sections |
|---|---|---|---|---|
| GDD | {name}-gdd.md | N | M | §4, §5, §7 |
| TDD | {name}-tdd.md | N | M | §9 |
| Art & Audio | {name}-art-audio.md | N | M | §6 |
| BD & Marketing | {name}-bd-marketing.md | N | M | §2, §3, §8, §10 |
| Agent Behavior Spec | {name}-agent-behavior-spec.md | N | M | §4, §5, §8, §9 |
```

### 3.5 File naming

Output files use the source PRD filename (without extension) as prefix:

- `{source-name}-gdd.md`
- `{source-name}-tdd.md`
- `{source-name}-art-audio.md`
- `{source-name}-bd-marketing.md`
- `{source-name}-agent-behavior-spec.md`
- `{source-name}-eval-plan.md`
- `{source-name}-permission-matrix.md`
- `{source-name}-metric-dictionary.md`
- `INDEX.md`

All placed in `{output-dir}/` (default: `audience/` next to source PRD). For
backward compatibility, older game-only workflows may still use `disciplines/`.

## Phase 4 — Output and Report

1. Write all selected pack documents and INDEX.md.
2. Report completion:
   - Files generated (full paths)
   - Per-pack requirement count
   - Total `to_be_confirmed` items
3. Suggest next steps:
   - "Review each output document with the corresponding owner."
   - "Resolve `to_be_confirmed` priority/owner fields."
   - "Use `/prd-refine` on individual output documents for further editing."

## Design Rules

- **Read-only on source PRD.** Never modify the original.
- **Language follows source.** Prose in the source language; ID/Priority/Status
  columns always English.
- If a section is empty or marked N/A in the source, carry that status into
  the output document — do not silently drop it.
- Requirements extraction is best-effort. When prose is ambiguous, extract
  what you can and flag for manual review.
- Do not invent requirements that are not in the source PRD.
- Do not duplicate the full source PRD into every output document. Primary
  sections get full content; secondary sections get summaries only.
- Follow the root SKILL.md Language Policy: variables, states, events, and
  config fields always in English regardless of prose language.
