# HTML PRD Export & HTML Mockup — Design Spec

## Summary

Add two optional post-publish steps to the `write-prd` workflow:

1. **Phase 5.6 — HTML PRD Export**: convert the Markdown PRD into a self-contained `.html` file for browser viewing
2. **Phase 5.7 — HTML Mockup Export**: generate a wireframe-style `.html` file with flow overview, screen layouts, and clickable navigation between screens

Both are defined as Phase 5.6/5.7 in `write-prd/SKILL.md` for structural identity, but are user-triggered — offered as choices in the "After Completion" menu after Phase 5 finishes, not auto-executed. Neither changes the PRD source of truth (always Markdown).

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Implementation approach | Pure skill instructions (方案 A) | Zero dependencies, consistent with existing skill style, portable across all platforms |
| Trigger timing | After Phase 5 completion, as optional offers | Non-blocking; user opts in only when needed |
| Output profile impact | None — `output_profile` unchanged | HTML export is post-processing, not a drafting format; Markdown remains source of truth |
| New files/skills | None created | Keeps repo lean; instructions live in `write-prd/SKILL.md` |
| External dependencies | Mermaid.js CDN only (HTML PRD) | Minimal; mockup uses zero external deps |

## Phase 5.6 — HTML PRD Export

### Trigger

Offered as a choice in the "After Completion" menu:
> "Want me to generate an **HTML version** of this PRD? Opens directly in any browser."

### Generation Rules

1. Read the saved Markdown PRD file
2. Output `{prd-name}.html` in the same directory
3. Self-contained: all CSS inlined in `<style>`, no external CSS framework
4. Mermaid rendering: include `<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js">` and initialize on page load; Mermaid code fences become `<pre class="mermaid">` blocks
5. YAML metadata blocks (product_type, out_of_scope, research_pack, etc.) render as styled info cards with key-value layout
6. Table of contents: auto-generated from H2 headings as anchor links at the top of the page
7. Typography: clean sans-serif, heading hierarchy with size/weight differentiation, adequate line-height and margins
8. Tables: bordered, striped rows, responsive horizontal scroll on narrow viewports
9. Code blocks: monospace with background shading
10. Print-friendly: `@media print` rules for clean paper output
11. Agent reports the file path after generation

### Constraints

- No external CSS framework (Bootstrap, Tailwind, etc.)
- Single external dependency: mermaid.js CDN
- Must render correctly when opened as a local `file://` URL
- Preserve all PRD content — no summarization or omission

## Phase 5.7 — HTML Mockup Export

### Trigger

Offered as a choice in the "After Completion" menu, only when the PRD contains multi-screen or multi-state content (§4 product flow, §5 functional requirements, or §6 design requirements describe screens/pages/states):
> "This PRD describes multiple screens/states. Want me to generate an **HTML mockup** showing an interactive walkthrough of the product flow?"

If the PRD is purely strategic/data/policy with no UI flows, this option is not offered.

### Pre-generation Step

Before generating, the agent:
1. Extracts a screen/page/state list from §4, §5, §6
2. Presents the list to the user for confirmation or amendment
3. Proceeds only after user confirms the screen list

### Core Principle — Single Frame, State Switching

The mockup is an interactive single-frame prototype, NOT a gallery of side-by-side screens. One simulated device frame contains all states as stacked layers. The user clicks buttons and CTAs inside the frame to transition between states, experiencing the product flow as the real app would behave.

### Generation Rules

1. Read PRD §4 (product flow), §5 (functional requirements), §6 (design requirements)
2. Output `{prd-name}-mockup.html` in the same directory
3. Self-contained: HTML + inlined CSS + vanilla JS, zero external dependencies

### Content Structure

| Element | Implementation |
|---|---|
| Device frame | Fixed-size container simulating target device (340×600 mobile, 960×600 desktop). Includes status bar, notch/chrome if mobile. |
| Screen layers | One absolutely-positioned div per state, sharing the same frame. Only active state is visible (opacity + pointer-events). |
| State transitions | CTA buttons call `go(stateName)` to hide current screen and show target. CSS opacity transitions for smooth switching. |
| Timed transitions | Auto-transitions (countdown, timers) use setInterval/setTimeout. |
| Live data simulation | Real-time values (climbing multiplier, counters) animate with JS intervals. |
| Flow bar | Horizontal bar above device frame showing all states as clickable nodes with arrows. Current state highlighted. Allows direct jump to any state for review. |
| Info panel | Below device frame: current state variables (from PRD §5) and source reference (PRD section number). |
| Tab switching | Two tabs: Interactive Prototype (single-frame walkthrough, default) and All Screens Overview (mini device thumbnails in grid). Clicking a thumbnail switches to Interactive at that state. |

### Dual-View Layout

The HTML file has two tab-switched views in one page:

1. **Interactive Prototype** (default): single-frame device with flow bar, state transitions, info panel.
2. **All Screens Overview**: every state as a scaled-down mini device frame (~60% size) in a grid. Each mini frame is a static snapshot, clickable to jump to Interactive mode at that state. A flow bar above the grid provides navigation context.

### Layout Rules

- Reproduce spatial structure from §6 wireframes or infer from §4/§5 flow
- Realistic proportions: top bar, main content, controls, bottom bar occupy proportional space as in a real app
- Interactive elements (buttons, toggles, inputs) visually distinguishable with hover/active states
- Disabled/locked states visually muted (reduced opacity, gray)
- State badges display PRD-defined variables (round_state, cashout_state, etc.)

### Visual Style

- Dark or light theme appropriate to product context
- Clean, minimal UI — looks like a real app in development, not wireframe gray blocks and not polished art
- Blue accent for primary interactive elements; green/red for success/failure
- Sans-serif system font stack

### Constraints

- Zero external dependencies (no JS frameworks, no CSS frameworks, no CDN)
- Must work as a local `file://` URL
- Vanilla JS only for state switching and animations
- If PRD screen descriptions are insufficient, agent asks user to supplement before generating

## Files Modified

| File | Change |
|---|---|
| `write-prd/SKILL.md` | Add Phase 5.6 and 5.7 sections; update "After Completion" offers |
| `SKILL.md` (root) | Add HTML export capability to description and sub-skills note |
| `commands/write-prd.md` | Add HTML-related trigger words to description |

## Files NOT Modified

- `prd-score/SKILL.md` — scoring unrelated
- `prd-refine/SKILL.md` — refinement is Markdown-only
- `prd-split/SKILL.md` — splitting is Markdown-only
- `examples/` — no new example files (HTML is dynamically generated)
- No new skill directories or template files created
