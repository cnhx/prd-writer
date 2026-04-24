# SkyRush — Sample PRD Output

Status: DONE_WITH_GAPS

```yaml
out_of_scope:
  - tech_stack
  - payment_channels
  - infra_deployment
```

```yaml
diagrams_generated:
  - section: 4
    type: mermaid
    subtype: stateDiagram
    location: inline
  - section: 6
    type: excalidraw
    subtype: wireframe
    location: "skyrush-wireframe-main.md"
```

## Summary
SkyRush is a mobile-first crash game designed to convert short-session traffic into repeat betting behavior. The MVP prioritizes fast entry, low-friction betting, and visible cash-out tension.

## Gameplay Flow

### Core Game Loop

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> betting : round_start
    betting --> countdown : bets_locked
    countdown --> climbing : countdown_end
    climbing --> crashed : boom_event
    climbing --> cashed_out : player_cashout
    crashed --> settling : settle_start
    cashed_out --> settling : settle_start
    settling --> idle : settle_done
```

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

### Main Screen Wireframe

![[skyrush-wireframe-main]]

## Known Gaps
- RTP pending math table
- max multiplier pending risk review
- jurisdiction-specific compliance pending legal confirmation
