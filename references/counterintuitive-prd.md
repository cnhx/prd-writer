# Counterintuitive PRD Rules — Before / After

Five rules that cut most common PRD rejection reasons. Each has a concrete
before/after pair. Rules are counterintuitive because the obvious thing (more
features, bigger vision, more polish) is usually the wrong thing.

---

## Rule 1 — Write the Rejection Letter first

**Why.** Most PRDs get rejected for predictable reasons: ROI unclear, MVP too large,
compliance gap, conflicts with existing roadmap, engineering effort underestimated.
Writing these out *before* drafting forces the PRD to address them structurally,
not defensively in review.

**Before**
> Section 11: *Risks.* "There may be delivery risks. We will monitor and mitigate."

**After**
> Section 11: *Rejection-preempt summary.*
> - **Engineering lead**: "Scope is 14 weeks but you budgeted 8." → Phase 1 scope
>   explicitly cut to 6 engineer-weeks; everything above is Phase 2 conditional.
> - **Finance**: "ROI not modeled." → Assumption #3 is the revenue driver;
>   `to_be_confirmed` with Finance by 2026-04-20.
> - **Legal**: "Consent flow not covered." → Section 7 routes all PII through
>   existing `consent_gateway`; no new consent logic.
> - (etc.)

Full letter lives in `rejection-preempt.md` next to the PRD.

---

## Rule 2 — Narrow MVP claim before broad vision

**Why.** Broad claims attract broad scrutiny. A narrow claim ("ship X, learn Y,
then decide") passes review because it is falsifiable and bounded.

**Before**
> "Phase 1: launch feature. Phase 2: add personalization. Phase 3: monetize.
> Phase 4: international."
> (Four phases, no gates, all committed.)

**After**
> "Phase 1 (committed, 6 engineer-weeks): launch baseline feature to measure
> `primary_kpi >= target`. Phase 2+ are `conditional_on_phase_1_learnings` and
> will be re-scoped after Phase 1 data, not committed today."

---

## Rule 3 — Design kill criteria before features

**Why.** If removing a feature from scope feels impossible because "the PRD would
lose its point," the PRD's point is the feature, not the user value. That is a
failure mode. Every feature should survive the question "what happens if we cut
this?" with a clean answer.

**Before**
> Feature list: A, B, C, D, E. All marked "must have."

**After**
> Feature list:
> - A (**core**): without this, primary KPI is untestable. Kill criteria: N/A.
> - B (**core**): gates A. Kill criteria: N/A.
> - C (**conditional**): nice-to-have. Kill criteria: drop if Phase 1 engineering
>   budget exceeds 6 weeks.
> - D, E: cut to Phase 2, reason logged in Non-Goals.

If the "core" list is more than 2–3 items in a lean PRD, re-examine.

---

## Rule 4 — Allocate budget to decisive evidence, not polish

**Why.** Three polished features that don't test the core assumption produce a
beautiful PRD with no signal at the end. One crude experiment that settles the
core assumption produces a decision.

**Before**
> 8 weeks: fully styled UI, animation polish, localized copy, complete settings
> surface.

**After**
> 8 weeks: functional-but-ugly core flow covering exactly the hypothesis; design
> system reused; copy in one language. Polish budget explicitly deferred to
> post-validation.

The question: at the end of the budget, can we answer yes/no to the central
question? If not, the budget was misallocated.

---

## Rule 5 — Predefine fallback narrative

**Why.** Primary KPIs underperform all the time. Without a predefined fallback,
the project is retroactively judged a failure even when it produced real value
(retention, cost savings, learnings). Predefining the fallback makes the work
non-binary.

**Before**
> "Success = 15% lift in `primary_conversion_rate` within 60 days."

**After**
> "Primary success = 15% lift in `primary_conversion_rate`. If primary misses,
> fallback values recognized at review:
> - Retention: `d7_return_rate` uplift >= 3pt
> - Cost: infrastructure cost per session down >= 10%
> - Learning: at least 3 hypotheses settled (documented in post-launch memo).
> Review judges on primary + best fallback."

Predefining this is not hedging. It converts "did it hit the number" into a
two-level check: did we meet the bar, and did we produce evidence the team can
use next quarter?

---

## How these rules interact

- Rule 1 (Rejection Letter) drives Rule 2 (narrow MVP) and Rule 5 (fallback).
- Rule 3 (kill criteria) surfaces the features that Rule 4 (decisive evidence)
  should keep.
- All five together typically shrink a first-draft PRD by 30–50% while making
  its core claim sharper.

Apply them in Phase 0.5 and Phase 2. Revisit in Phase 4 review.
