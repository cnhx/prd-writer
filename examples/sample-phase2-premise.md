# Example — Phase 2 Premise Check Output

This is a concrete example of what `/write-prd` Phase 2 should produce **before**
it starts drafting the full PRD. Use it as a format reference.

Context for this example: a small casino game studio is scoping a new slot title.
Phase 1 interrogation already established the core idea (a "stacked wild" slot for
LATAM markets) and user profile.

---

## Core assumptions to confirm

1. **Target market demand** — LATAM mobile slot players prefer short-session, medium-volatility
   titles over the US-style long-session high-vol ones. `to_be_confirmed` via operator data.
2. **RTP expectation** — LATAM regulated markets accept `rtp_target ∈ [94.5%, 96.5%]`;
   outside this window, operator certification fails. `pending_math_table` from compliance.
3. **Device mix** — ≥ 80% of active players are on mid-tier Android (3 GB RAM, GPU tier 2);
   the build must ship under `bundle_size_mb < 80`. Source: 2025 Q4 internal analytics.
4. **Monetization model** — revenue comes from GGR share with operators, **not** in-game
   IAP; we do not need a storefront module.
5. **Certification timeline** — GLI-19 certification takes 10–14 weeks; this sets the
   latest feature-freeze date backward from target launch.

## Implementation options

### Option A — Stacked Wild on a single reel
- Wilds only appear on `reel_3`, stacking up to `stack_height = 3`.
- Scope: 5 reels × 3 rows, 20 fixed paylines, 1 bonus game.
- Est. effort: 14 engineer-weeks + 10 art-weeks.
- Risk: low. Proven mechanic.

### Option B — Stacked Wild with respin trigger
- Option A plus: landing a full stack triggers `respin_mode` with locked wilds.
- Scope: Option A + 1 feature state, additional math tuning.
- Est. effort: 18 engineer-weeks + 12 art-weeks.
- Risk: medium. Math tuning is sensitive; RTP window narrower.

### Option C — Multi-reel stacked wilds + respin + free-spin bonus
- Option B plus: 3-scatter trigger for a `free_spin_bonus` round (10 spins with
  guaranteed stacked wilds).
- Scope: full feature set of a premium title.
- Est. effort: 26 engineer-weeks + 18 art-weeks.
- Risk: high. Two feature states interact; certification math table is larger;
  timeline is tight against GLI-19 window.

## Recommendation

**Option B.** Rationale:

- Option A alone won't differentiate in an already crowded stacked-wild category.
- Option C's respin + free-spin interaction adds math-tuning risk that threatens the
  certification deadline (assumption #5).
- Option B hits the "one extra mechanic" sweet spot for LATAM short-session players
  (assumption #1) while staying inside the proven-math envelope.
- If Option B ships well, Option C becomes a straightforward content sequel, not a
  rewrite.

**Proceed to Phase 3 drafting on Option B, pending user confirmation.**

---

## Notes on using this example

- Keep assumptions numbered so they can be referenced in the final PRD's Assumptions section.
- Each option should state **scope**, **effort**, and **risk** — not just a description.
- The recommendation must cite **which assumptions** drive the choice. A recommendation
  without this is just a preference.
- If all three options feel equivalent, Phase 1 interrogation was incomplete — go back.
