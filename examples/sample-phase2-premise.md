# Example — Phase 2 Premise Check Output

> ⚠️ **All numbers, ranges, timelines, and regulatory references below are FICTIONAL**
> placeholder data for format illustration only. They are **not** real market figures,
> real regulatory requirements, or real certification timelines. When you write a real
> Phase 2, mark every such datum as `to_be_confirmed` and sourced from operator /
> compliance / analytics owners — see the repo's core rule: *"Never invent RTP, odds,
> regulatory facts, or market data."*

This is a concrete example of what `/write-prd` Phase 2 should produce **before**
it starts drafting the full PRD. Use it as a **format reference**, not a data source.

Context for this fictional example: a small game studio is scoping a new casual
puzzle title for a regional mobile market. Phase 1 interrogation already established
the core idea and user profile.

---

## Core assumptions to confirm

1. **Target market demand** — regional mobile players prefer short-session, low-commitment
   titles over long-session progression ones. `to_be_confirmed` via partner analytics.
   *(Placeholder — confirm with a real market research source.)*
2. **Monetization constraint** — target market's regulated advertising rules cap
   rewarded-ad frequency at `ads_per_session <= N` (N is `to_be_confirmed` with
   compliance). Outside this window, publisher submission fails.
   *(Placeholder — confirm with real regulator or publisher rules.)*
3. **Device mix** — majority of active players on mid-tier Android (approximate specs
   `pending_verification`); the build must ship under a bundle-size budget that is
   `to_be_confirmed` with the platform team. Source: **placeholder, not a real analytics
   dataset.**
4. **Monetization model** — revenue from rewarded video + optional cosmetic IAP. Assume
   no loot-box style mechanics until compliance confirms jurisdiction.
5. **Certification timeline** — publisher review window estimated at `T` weeks, where `T`
   is `to_be_confirmed` with the publisher relations owner. This sets the latest
   feature-freeze date backward from target launch.

## Implementation options

Each option below uses **fictional effort numbers** to illustrate the scope / effort / risk
format. Real efforts come from your engineering lead's estimate.

### Option A — Single core mechanic
- Core puzzle loop only, 30 hand-crafted levels.
- Scope: one game mode, one progression system, no meta layer.
- Est. effort: small (placeholder).
- Risk: low. Proven mechanic.

### Option B — Core mechanic + daily challenge loop
- Option A plus a rotating daily challenge with a separate `daily_reward_track`.
- Scope: Option A + 1 meta-layer state.
- Est. effort: medium (placeholder).
- Risk: medium. Meta layer adds tuning surface.

### Option C — Core + daily + social / leaderboard
- Option B plus social leaderboards with weekly seasons.
- Scope: full feature set of a retention-oriented title.
- Est. effort: large (placeholder).
- Risk: high. Three systems interact; season scheduling adds operational load.

## Recommendation

**Option B.** Rationale:

- Option A alone is unlikely to differentiate in a crowded casual-puzzle category.
- Option C's social layer adds operational cost that threatens the certification
  deadline (assumption #5).
- Option B hits the "one extra retention hook" sweet spot for the short-session
  player profile (assumption #1) while staying inside the proven-scope envelope.
- If Option B ships well, Option C becomes a content sequel, not a rewrite.

**Proceed to Phase 3 drafting on Option B, pending user confirmation.**

---

## Notes on using this example

- **Do not copy the placeholder numbers.** They exist to show shape, not substance.
- Keep assumptions numbered so they can be referenced in the final PRD's Assumptions section.
- Each option should state **scope**, **effort**, and **risk** — not just a description.
- The recommendation must cite **which assumptions** drive the choice. A recommendation
  without this is just a preference.
- Every regulatory, RTP, market-size, or timeline figure in a real PRD must be sourced
  or marked `to_be_confirmed` / `pending_math_table`. Inventing them is a core violation.
- If all three options feel equivalent, Phase 1 interrogation was incomplete — go back.
