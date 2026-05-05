---
name: prd-score
description: |
  Score a PRD against a Ready-to-Dev rubric. Produces Structure Completeness %,
  Owner Closure %, Open-Question residue, Evidence Score, export readiness,
  and a Green / Yellow / Red verdict.
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

Also read `product_type` near the top of the PRD. If it is missing, flag
`product_type_missing`. If a non-game PRD uses game-only headings without a
clear reason, list that under remediation.

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

Look for a fenced YAML block at the top of the PRD (immediately after the H1)
shaped like:

```yaml
out_of_scope:
  - tech_stack
  - payment_channels
```

Behavior:

- **Block missing** → fail this dimension with reason `boundary_scan_not_run`.
  `/write-prd` Phase 0.3 is mandatory; a missing block means the scan was
  skipped and the PRD's scope is undefined.
- **Block present, `[]`** → pass; record `boundary_scan_empty`.
- **Block present with entries** → scan the rest of the PRD for prescriptive
  language that violates each OUT category (e.g. specific payment SDK names if
  `payment_channels` is OUT). Report each violation with file:line. Fail if
  any found.

### 5. Terminology-with-example compliance (pass/fail)

For each non-standard term introduced (use grep for bold-first-use patterns,
self-coined names, or evaluation frameworks), check an example is paired per
`write-prd` §3.2. Fail if any term lacks one.

### 6. Rejection-Letter compliance (pass/fail, if applicable)

If the project uses `rejection-preempt.md` or an inline rejection-preempt
section, verify 3–5 rejection bullets exist, each with a concrete preemption.
Fail if missing or vague ("we will monitor").

### 7. Evidence Score (0–100%, informational unless evidence is claimed)

Check for a `research_pack` YAML block near the top of the PRD.

- **Block absent** → report `evidence: not_recorded`.
- **Block present as `[]`** → report `evidence: none_supplied`; no penalty if
  the PRD clearly marks decisions as assumptions or stakeholder requests.
- **Block present with entries** → score:
  - coverage: key decisions linked to evidence (40)
  - freshness: evidence has a usable time range/date (20)
  - confidence: each entry has high/medium/low (20)
  - contradiction handling: conflicting evidence is named or marked absent (20)

If a PRD says a decision is evidence-backed but no research entry supports it,
flag `unsupported_evidence_claim`.

### 8. Diagram integrity (informational, does not affect verdict)

Check for a `diagrams_generated` YAML block near the top of the PRD.

- **Block absent** → report `diagrams: skipped` (no penalty — diagrams are
  optional per `/write-prd` Phase 3.5).
- **Block present** → for each entry, verify a ` ```mermaid ` code fence
  exists in the stated section (all Phase 3.5 diagrams are inline Mermaid).
  Report each section claimed in the metadata but missing its fence.

### 9. Export readiness (informational, does not affect verdict)

Check for an `output_profile` value: `obsidian_md`, `word_docx`, `pdf`,
`confluence`, or `multi`.

- `obsidian_md`: links should be relative when they point to local files;
  Mermaid fences should remain inline.
- `word_docx`: headings should not skip levels; wide tables should be called out
  for cleanup; diagrams need captions or short titles.
- `pdf`: long tables need review; diagrams need titles; unresolved Mermaid
  rendering should be preserved as source in an appendix or nearby block.
- `confluence`: links should be explicit; tables should be narrow; diagrams
  should have a named attachment/export note plus the Mermaid source block.
- `multi`: apply all relevant checks above.

Report `export_profile_missing` if no profile is recorded.

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
- Diagram integrity: present / skipped / missing-fences (<sections missing mermaid fences>) — informational only, not part of the pass/fail aggregate
- Evidence Score: NN% / not_recorded / none_supplied (<key issues>)
- Export readiness: pass / warning / missing-profile (<target profile>)

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
