# SkyRush — Sample PRD Output

Status: DONE_WITH_GAPS

## Summary
SkyRush is a mobile-first crash game designed to convert short-session traffic into repeat betting behavior. The MVP prioritizes fast entry, low-friction betting, and visible cash-out tension.

## Functional Requirements
- `bet_amount`: player stake entered before round start
- `auto_cashout_multiplier`: optional automatic cashout threshold
- `round_state`: `countdown | active | crashed | settled`
- `cashout_state`: `pending | success | failed`

## Art and Design Requirements
- modern neon visual direction with strong contrast
- clear multiplier focus at center stage
- separate animation treatment for countdown, climb, and crash
- win/loss audio layers kept distinct from core game logic requirements

## Known Gaps
- RTP pending math table
- max multiplier pending risk review
- jurisdiction-specific compliance pending legal confirmation
