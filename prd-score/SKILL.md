---
name: prd-score
description: |
  Score a PRD against a Ready-to-Dev rubric. Produces Structure Completeness %,
  Owner Closure %, Open-Question residue, and a Green / Yellow / Red verdict.
  Use after /write-prd completes, or on any existing PRD before submitting for review.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# PRD Score

Quantify a PRD's readiness. Produces a short report the PM can hand to reviewers.

## Inputs

- **Required**: path to the PRD markdown file
- **Optional**: path to a `rejection-preempt.md` if the project uses one

## Scoring dimensions

### 1. Structure Completeness (0–100%)

Required sections present and non-empty. Weighted:

| Section | Weight |
|---|---|
| Summary | 5 |
| Project positioning | 5 |
| Market / target user | 8 |
| Product or gameplay flow | 12 |
| Functional requirements | 12 |
| Art / design (if applicable) | 6 |
| Math / business model | 10 |
| Compliance & risk | 8 |
| Technical considerations | 6 |
| KPI & success metrics | 10 |
| Milestones | 6 |
| Assumptions | 5 |
| Non-goals | 5 |
| Sources | 2 |

A section counts as present only if it contains substantive content (more than
a header + placeholder). A section marked "N/A — not applicable" with a brief
justification counts as present.

### 2. Owner Closure (0–100%)

Of all `Assumption` entries, what fraction have:

- A named owner (role or person)
- A deadline or clear trigger for resolution

Missing owner or deadline on any Assumption drops the number.

### 3. Open-Question residue (count + severity)

- Count remaining Open Questions
- Flag any whose unanswered state **blocks** a milestone (mark severity `P0`)

A PRD with many Open Questions can still pass as `DONE_WITH_GAPS`, but P0
blockers force Yellow / Red.

### 4. Out-of-Scope compliance (pass/fail)

Scan for language that prescribes items marked OUT in Phase 0.3 (if the
`out_of_scope` note exists near the top of the PRD). Fail if found.

### 5. Terminology-with-example compliance (pass/fail)

For each non-standard term introduced (use grep for bold-first-use patterns,
self-coined names, or evaluation frameworks), check an example is paired per
`write-prd` §3.2. Fail if any term lacks one.

### 6. Rejection-Letter compliance (pass/fail, if applicable)

If the project uses `rejection-preempt.md` or an inline rejection-preempt
section, verify 3–5 rejection bullets exist, each with a concrete preemption.
Fail if missing or vague ("we will monitor").

## Verdict

- **Green (Ready to Dev)**: Structure ≥ 90%, Owner Closure ≥ 80%, no P0 Open
  Questions, all pass/fail dimensions pass.
- **Yellow (Ready with caveats)**: Structure ≥ 75%, Owner Closure ≥ 60%, at
  most 1 P0 Open Question with an explicit owner + deadline, all pass/fail
  dimensions pass.
- **Red (Not Ready)**: any other state. Produce specific remediation list.

## Output format

```
## PRD Score — <PRD title>

**Verdict**: Green / Yellow / Red

- Structure Completeness: NN% (missing: <list of sections>)
- Owner Closure: NN% (<X> of <Y> Assumptions fully owned)
- Open Questions: <N> total, <M> marked P0
- Out-of-Scope compliance: pass / fail (<reason if fail>)
- Terminology-with-example: pass / fail (<terms lacking examples>)
- Rejection-Letter compliance: pass / fail / N/A

### Top 3 remediation items
1. …
2. …
3. …
```

## Notes

- This skill is read-only: it reports, does not mutate the PRD.
- If the PRD is < 100 lines, scoring is advisory; the rubric is tuned for
  substantive PRDs (200+ lines).
- Call after Phase 5 of `/write-prd`, or standalone against any existing PRD.
