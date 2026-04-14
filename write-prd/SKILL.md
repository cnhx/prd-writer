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

## When NOT to Use This Skill

This workflow is designed for **new product or feature PRDs** that need structured market,
scope, and math decisions. Do **not** use it for:

- **One-page lite specs** (< 200 lines) — prefer a lightweight template or freeform doc.
- **Bug-fix RFCs / technical design docs** — use an engineering design template; this
  skill's market/business sections will be dead weight.
- **Pure refinement of an existing PRD** — use `/prd-refine` instead; this skill will
  re-interrogate ground already covered.
- **Research / discovery notes** — no scope decision is being made yet.
- **Post-launch retros or changelogs** — wrong workflow direction.

If the user is in one of these cases, recommend the alternative and stop. Do not force
the 5-phase workflow onto a shape it doesn't fit.

## Phase 0 — Context Loading

Sources, in priority order:
1. Task-specific files supplied by user
2. Local project documents
3. User answers

Read all available context before asking questions.

## Phase 0.5 — Rejection Letter + Optional Grill

This phase has two parts. Part A is **mandatory** (a lightweight 10-minute exercise).
Part B is optional (deeper interrogation via `/grill-me`).

### Part A — Rejection Letter (mandatory)

Before any Phase 1 interrogation, produce `rejection-preempt.md` as a sibling file
to the planned PRD (same directory, e.g., `docs/prd/<name>-rejection-preempt.md`).
PRDs typically fail review for predictable reasons; naming them up front shapes the
entire draft.

**Steps:**

1. Identify **3 to 5 stakeholders** who will actually review this PRD. Typical
   candidates (pick the ones that apply — do not invent reviewers):
   - Leadership / business owner (ROI, strategic fit)
   - Engineering lead (effort, feasibility, tech debt)
   - Compliance / legal (regulatory, privacy, consent)
   - Finance (unit economics, budget)
   - GTM / existing product line owner (conflicts, cannibalization)

   Fewer than 3 is acceptable for internal infra PRDs with a narrow audience;
   more than 5 usually means scope is too broad — shrink the scope first.
2. For each stakeholder, draft the single most likely rejection quote.
3. For each rejection, draft a one-line **Mitigation** — the PRD section, evidence,
   or scope change that addresses it. If you cannot mitigate, mark it
   `known_gap` and note the residual risk.

**Format** (write to `rejection-preempt.md`):

```markdown
# Rejection Letter Pre-empt — <PRD name>

## Top predicted rejection reasons (3–5 entries)

1. **[Stakeholder]**: "[rejection quote]"
   - Mitigation: [PRD section / evidence / scope change]
   - Residual risk: [what remains, or `to_be_confirmed by <owner> by <date>`]

2. ...

(continue for each real stakeholder; 3 to 5 total, not padded)
```

See `../examples/sample-rejection-preempt.md` for a full example.

**Link from the PRD.** In the PRD's final Sources / Appendix section, include:
`Related: [rejection-preempt.md](./<prd-name>-rejection-preempt.md)`.

**Phase 4 review ties back.** In Phase 4, verify every rejection reason has either
a Mitigation landed in the PRD or is explicitly accepted as `known_gap`.

### Part B — Optional Grill

Trigger conditions (offer when any is true):
- User input is a vague idea (e.g., "we should do something about X")
- User explicitly requests grill (e.g., "先帮我想清楚", "grill me first")
- Input lacks a clear user problem, target user, or success metric
- Part A rejection letter uncovered gaps the user cannot immediately close

How to offer: "This idea still has open branches. Want to run `/grill-me` before
Phase 1? I'll challenge each key decision and walk the decision tree."

If user accepts:
- Invoke the `/grill-me` skill
- Walk the decision tree one question at a time, each with a recommended answer
- Focus on: pain point validity, solution necessity, scope boundaries, key tradeoffs
- After grill completes, organize consensus into structured context for Phase 1

If user skips, proceed to Phase 1 with the rejection letter in hand.

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
- 2 to 3 implementation options (each with **scope**, **effort**, **risk**)
- One recommendation with rationale that cites which assumptions drove the choice

See `examples/sample-phase2-premise.md` for a concrete format reference.

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

Drafting rules:
- **Language policy (two-tier)**: prose and section titles follow user preference (中文 / English / other); variables, states, events, config fields, and API identifiers are **always English** regardless of prose language.
- Art/design requirements stay in their own section
- Uncertain facts explicitly marked as `to_be_confirmed`
- No vague placeholders like "optimize later" without owner or condition

## Phase 4 — Review

Review checklist:
- Is the core flow implementable without guesswork?
- Are edge cases and state transitions explicit?
- Are math assumptions separated from confirmed numbers?
- Are art requirements isolated from logic requirements?
- Are compliance and market facts sourced or marked as pending?
- Are non-goals explicit?
- Is the English naming consistent?

## Phase 5 — Polish and Publish

Sequence:
1. Review draft against Phase 4 checklist
2. Optional: run `/opus-prd-polish` for a final polish pass
3. Save file to user-specified path (default: `docs/prd/`)
4. Optional: git commit
5. Report completion status:
   - `DONE` — all sections complete, no known gaps
   - `DONE_WITH_GAPS` — usable draft but has unknowns (list them as `missing_info`)
   - `BLOCKED` — cannot proceed, state what is blocking

When the draft is usable but incomplete, always return `DONE_WITH_GAPS` rather than
blocking or inventing data. Mark uncertain facts as `to_be_confirmed`.

## After Completion

Offer:
- "Want me to **tighten the scope**? I can challenge which items should really be deferred."
- "Should I **run a pre-mortem** on this PRD?"
- "Want me to **break this into user stories** for engineering?"
- "Feeling uncertain? Run `/grill-me` to **pressure-test the PRD assumptions**."

## Notes

- Be opinionated about scope — a tight PRD beats an expansive vague one
- If the idea is too big, proactively suggest phasing and spec only Phase 1
- Non-goals are as important as goals — they prevent scope creep
- Success metrics must be specific: "improve NPS" is bad, "increase NPS from 32 to 45 within 90 days of launch" is good
- Open questions should be genuinely unresolved
- If the user provides research, weave insights into the Background section with attribution
