---
name: write-prd
description: |
  5-phase PRD writing workflow: context loading, product interrogation, premise check,
  PRD drafting, review and publish. Optionally integrates /grill-me for idea stress-testing.
  Use when asked to write a PRD, create product requirements, or draft a product spec.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Write PRD

Structured 5-phase PRD workflow. Accepts anything from a vague idea to a detailed brief.

## Phase 0 — Context Loading

Sources, in priority order:

1. Task-specific files supplied by user
2. Local project documents (`docs/`, `references/`, sibling PRDs)
3. Memory / knowledge base (if available in the environment)
4. User answers

### 0.1 Mandatory history alignment

**Before asking any question**, sweep for prior context:

```bash
# Sibling PRDs in the repo
ls docs/prd/ 2>/dev/null

# Memory store (if nmem or equivalent is available in the environment)
nmem --json m search "<product name>" 2>/dev/null
nmem --json m search "<product series / code>" 2>/dev/null
```

Goal: never ask the user what the system already knows. Skip this step only if
the product is genuinely new and no similar work exists.

### 0.2 Product code / series anchor

If the codebase uses internal product codes (e.g. `SS0-*`, `CG01`, `Project Alpha`),
ask early for:

- Product code naming rule for this project
- Which series / product line this belongs to
- Pointer to the series' past PRDs or internal wiki (if any)

Do not invent placeholders like `PRD-001` without confirming the naming rule.

### 0.3 Out-of-Scope boundary scan (MANDATORY)

**Before Phase 1**, run a one-shot checklist to fence off owner-overreach. Ask
the user to explicitly mark which categories are **not** in this PRD's decision
scope:

```
Which of the following are OUT of this PRD's scope? (mark all that apply)

□ Tech-stack selection (engine, framework, protocol, perf thresholds)
□ Payment / deposit / withdrawal channels
□ Distributor / aggregator / partner-specific integration specs
□ Licensing & regulatory jurisdiction
□ Deployment architecture & infra
□ Pricing / commercial terms
□ Org / staffing / vendor selection
□ Analytics / BI dashboard implementation
```

Items marked OUT must not appear as concrete prescription in the PRD; if
relevant, describe them only at semantic-contract level. This is the single
biggest cause of first-draft rejection.

**Persistence (mandatory)**: record the user's choices into the PRD itself so
`/prd-score` and later reviewers can enforce the boundary. At the top of the
PRD file, immediately after the H1 title, insert a fenced YAML block:

```yaml
out_of_scope:
  - tech_stack             # one line per category the user marked OUT
  - payment_channels
  - infra_deployment
  # ...
```

Use the category slugs from the checklist (`tech_stack`, `payment_channels`,
`distributor_specs`, `licensing_jurisdiction`, `infra_deployment`, `pricing`,
`org_staffing`, `analytics_bi`). Include categories the user explicitly kept
IN by omitting them — the block lists OUT items only. If the user marked none
out, emit `out_of_scope: []` so the scoring skill has an unambiguous signal
that the scan ran.

## Phase 0.5 — Rejection Letter + Optional Stress-Test

### Part A: Rejection Letter (mandatory)

Before Phase 1 ends, list the 3–5 reasons this PRD would realistically be
rejected by senior stakeholders. Draft each bullet as if you were the reviewer.

Each bullet needs a **concrete preemption** the PRD will implement. Save in
`rejection-preempt.md` next to the PRD (or inline as Section 11 if lightweight).

Common reviewers and rejection axes:

- **Engineering lead**: scope, effort, technical debt
- **Finance**: ROI, cost model
- **Legal / Compliance**: PII, consent, jurisdictional risk
- **GTM / Marketing**: positioning, launch readiness
- **Leadership**: strategic fit, opportunity cost

This is Counterintuitive Rule 1 — see `references/counterintuitive-prd.md`.

### Part B (optional): grill the idea with `/grill-me`

**Trigger conditions** (offer when any is true):

- User input is a vague idea (e.g., "we should do something about X")
- User explicitly requests grill (e.g., "先帮我想清楚", "grill me first")
- Input lacks a clear user problem, target user, or success metric

**How to offer**: "This idea is still forming. Want to run `/grill-me` first? I'll
challenge each key decision before we start the formal PRD."

If user accepts, invoke `/grill-me`, walk the decision tree one question at a
time, each with a recommended answer. Focus on pain validity, solution
necessity, scope boundaries, key tradeoffs.

If user skips, proceed to Phase 1.

## Phase 1 — Product Interrogation

Ask one question at a time.

Required question themes:

1. Market truth — is there real demand?
2. Current alternatives — what do users do today?
3. Target player/user profile — who exactly?
4. Minimum viable scope — what is the smallest useful version?
5. Business and math intuition — how does this make money or create value?
6. Differentiation and defensibility — why us, why now?

## Phase 2 — Premise Check and Option Selection

Produce:

- 3 to 5 core assumptions to confirm
- 2 to 3 implementation options
- One recommendation with rationale

### 2.1 Re-apply counterintuitive rules here

Before recommending options, run:

- **Rule 2 narrow MVP**: does the recommendation define the smallest verifiable
  scope? If it sprawls, trim.
- **Rule 3 kill criteria**: for each feature, name the kill condition. If a
  feature cannot be cut cleanly, rethink.
- **Rule 4 decisive evidence**: does the recommendation spend budget on
  answering the hypothesis, or on polish? Reallocate if polish-heavy.

## Phase 3 — PRD Drafting

Required sections:

1. Summary
2. Project positioning
3. Market strategy
4. Gameplay or product flow
5. Functional requirements
6. Art and design requirements
7. Math or business model
8. Compliance and risk
9. Technical considerations
10. KPI and success metrics
11. Milestones
12. Assumptions
13. Non-goals
14. Sources

### 3.1 Drafting rules

- All variables and states get readable English names (see Language Policy in root SKILL.md)
- Art/design requirements stay in their own section
- Uncertain facts explicitly marked as `to_be_confirmed`
- No vague placeholders like "optimize later" without owner or condition

### 3.2 Terminology-with-example rule (MANDATORY)

Any non-standard term, self-coined method, or evaluation framework introduced
in the PRD **must be paired with a concrete example at first use**. Preferably:

- One **failure scenario** (what it looks like when the thing goes wrong)
- One **remediation path** (what to do about it)

Reviewers cannot evaluate abstract processes. A 2-line example beats a
paragraph of definition. Example:

> **Visual-Math Weight Alignment Evaluation**: verify each symbol's culturally
> perceived value rank matches its mathematical pay tier.
>
> *Failure example*: in a Filipino reskin of a slot game, the highest-paying
> symbol maps to a 1-peso coin while a lower-paying symbol maps to a whole
> roasted pig (Lechon — a fiesta centerpiece). Players hit Lechon ×3, expect
> the biggest win, receive a mid payout, feel cheated.
>
> *Remediation*: swap the mapping, OR visually exaggerate the rare symbol with
> particle effects and a bespoke jingle, OR give the high-pay symbol a
> dedicated Big Win voiceover.

Apply to: evaluation procedures, named workflows, scoring criteria,
internal-jargon tools. Do NOT apply to industry-standard terms (RTP, Volatility,
Jackpot Wheel).

### 3.3 Assumption vs Open Question (distinct)

| Type | Meaning | Owner duty |
|---|---|---|
| **Assumption** | "We *choose to assume* X is true" (active stance) | Confirm or reject within 48h; sign off |
| **Open Question** | "X is unresolved; we need external input" (passive dependency) | Supply the answer or escalate |

If a line reads like "we don't know yet", it's an Open Question, not an
Assumption. Mixing them makes cleanup harder at publish time.

## Phase 3.5 — Diagram Generation (optional)

After Phase 3 produces the text draft, assess whether visual diagrams would
strengthen the PRD. This phase is optional — skip for lightweight, policy, or
pricing PRDs that have no multi-state flows or UI layouts.

**All diagrams are inline Mermaid**, written directly into the PRD as
` ```mermaid ` code fences. Mermaid renders natively in GitHub, Obsidian,
and VS Code, so no external skill, rendering server, or companion file is
required. Raw Mermaid syntax is also diffable, which keeps PRDs reviewable.

### Trigger conditions (offer when any is true)

- §4 describes a multi-state flow with 3+ states or decision branches
- §6 describes a UI layout, screen structure, or spatial arrangement
- §9 describes a multi-component system architecture
- User explicitly requests diagrams ("加流程图", "generate wireframes", "画线框图")

### How to offer

> "The draft has [a multi-state product flow / UI layout descriptions / a
> multi-component architecture]. Want me to generate inline Mermaid diagrams?
> Type `skip` to proceed without diagrams."

### Diagram routing

| PRD section | Diagram intent | Mermaid syntax |
|---|---|---|
| §4 Product / gameplay flow | State machine or user journey | `stateDiagram-v2`, `journey`, or `flowchart` |
| §5 Functional requirements | Interaction / API sequence | `sequenceDiagram` |
| §6 Art / design requirements | UI layout / screen wireframe | `block-beta` (preferred) or `flowchart` with subgraphs |
| §9 Technical considerations | System architecture | `flowchart LR` / `graph` with subgraphs |

All go in ` ```mermaid ` code fences inline in the relevant section.

### Wireframe guidance (§6)

`block-beta` is the cleanest Mermaid syntax for screen layouts. Use `columns`
to define a grid, nest `block:` groups to represent areas (header, content,
footer, FAB). Label blocks with the UI element name plus one line of state
or copy. Keep to 8–15 blocks per screen — anything more should be split into
sub-wireframes or described in prose.

When `block-beta` cannot express the layout (e.g. free-positioned overlays),
fall back to `flowchart TB` with labeled subgraphs. Do not attempt to simulate
pixel layout in Mermaid — the goal is intent, not fidelity.

### Execution steps

1. Present a diagram plan: one line per proposed diagram with target section
   and Mermaid subtype. Wait for user confirmation (all / partial / skip).
2. For each accepted diagram, write the Mermaid source directly inline in the
   target section via `Edit`.
3. Record generated diagrams in the PRD metadata (after the `out_of_scope`
   block):

```yaml
diagrams_generated:
  - section: 4
    subtype: stateDiagram-v2
  - section: 6
    subtype: block-beta
  - section: 9
    subtype: flowchart
```

All entries are inline Mermaid, so no `location` or `type` field is needed.

### When Mermaid is not enough

For wireframes too complex for `block-beta` (free-positioned overlays,
pixel-exact mockups, detailed visual mocks), **do not invent an external
dependency**. Instead:

- Reduce the wireframe to a simplified block layout that captures intent
- Describe visual details in prose next to the Mermaid block
- Note `wireframe_fidelity: intent_only` in the `diagrams_generated` entry so
  reviewers know a higher-fidelity mock is still needed later

## Phase 4 — Review (Grill-driven, not self-review)

Self-review on your own draft is confirmation bias. Instead:

### 4.1 Mandatory grill rounds

Invoke `/grill-me` in **Review mode** on the draft file. Explicit prompt:

> "Run `/grill-me` in review mode on `<path-to-PRD>` for N rounds. Rotate
> reviewer hats (engineering → finance → compliance → GTM → leadership).
> Apply fixes directly via Edit or Write; only escalate to the user for
> `blocking_unknown` items."

Round count:

- **N = 2** for PRDs ≤ 300 lines and no compliance / money topics.
- **N = 3** for PRDs > 300 lines, or that touch compliance, money, or
  jurisdictional risk.

Review mode applies remediations autonomously per round (see `grill-me/SKILL.md`
Review mode). Any unresolved items come back as `to_be_confirmed` markers for
the user to answer in Phase 5.

Do **not** invoke Interview mode here — it will re-interview the author and
waste cycles on decisions the PRD has already made.

### 4.2 Targeted grill angles

Use these as directed grill prompts, not as a sign-off checklist:

- Is the core flow implementable without guesswork?
- Are edge cases and state transitions explicit?
- Are math assumptions separated from confirmed numbers?
- Are art requirements isolated from logic requirements?
- Are compliance and market facts sourced or marked as pending?
- Are non-goals explicit?
- Is the English naming consistent?
- Did any section sneak across the out-of-scope boundaries from Phase 0.3?
- Does every self-coined term have the example required by §3.2?
- Are Assumptions and Open Questions cleanly separated per §3.3?

## Phase 5 — Polish and Publish

Sequence:

1. Resolve any open issues surfaced in Phase 4 grill rounds
2. Optional: run `/opus-prd-polish` for a final polish pass
3. Optional: run `/prd-score` to quantify Ready-to-Dev status
4. Save file to user-specified path (default: `docs/prd/`)
5. Optional: git commit
6. Report completion status:
   - `DONE` — all sections complete, no known gaps
   - `DONE_WITH_GAPS` — usable draft but has unknowns (list them as `missing_info`)
   - `BLOCKED` — cannot proceed, state what is blocking

When the draft is usable but incomplete, always return `DONE_WITH_GAPS` rather
than blocking or inventing data. Mark uncertain facts as `to_be_confirmed`.

## After Completion

Offer:

- "Want me to **tighten the scope**? I can challenge which items should really be deferred."
- "Should I **run a pre-mortem** on this PRD?"
- "Want me to **break this into user stories** for engineering?"
- "Run `/grill-me` again to **pressure-test the PRD assumptions**."
- "Run `/prd-score` to quantify Ready-to-Dev readiness."

## Notes

- Be opinionated about scope — a tight PRD beats an expansive vague one
- If the idea is too big, proactively suggest phasing and spec only Phase 1
- Non-goals are as important as goals — they prevent scope creep
- Success metrics must be specific: "improve NPS" is bad, "increase NPS from 32
  to 45 within 90 days of launch" is good
- Open questions should be genuinely unresolved
- If the user provides research, weave insights into the Background section with
  attribution
