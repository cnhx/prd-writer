# HTML PRD Visual Rubric

Reference for the Phase 5.6 self-review loop. A PRD page is an **editorial**
reading document: reviewers scan it, jump between sections, compare table rows,
print it, and open it on a phone in a meeting. Award-tier here means the bar set
by the best documentation and long-form reading sites (Stripe Docs, Linear
changelog, Vercel/Next.js docs, NYT long-form), judged on how fast a reader
finds, reads and trusts the content. Landing-page spectacle (hero motion,
parallax, scroll-jacking, decorative 3D) lowers that score.

Content fidelity outranks every visual dimension: the HTML carries every word,
number, table row and diagram of the Markdown source, in source order.

## Evidence

`prd-html-qa.mjs` produces both kinds of evidence for each viewport (desktop
1440, desktop dark, tablet 1024, mobile 390):

- **Hard checks** (`✗`, exit code 1): page overflow, hidden title, duplicate
  ids, broken anchors, broken images, Mermaid render errors, body contrast below
  4.5, missing navigation, console errors, and interaction smoke tests (mobile
  drawer, nav jump landing, theme toggle with Mermaid re-render).
- **Soft checks** (`△`): nav/callout contrast, line length, text under 12px,
  tables that scroll horizontally, Mermaid diagrams shrunk below 70%.
- **Screenshots**: evenly spaced frames per viewport plus one frame per flagged
  element (`*-issue-*.png`) and the open mobile drawer.

Read every `issue` screenshot and at least the first and a middle frame of each
viewport before scoring.

## Dimensions

Score each dimension **pass** or **gap**. A gap names the screenshot and the
element.

| Dimension | Pass looks like |
|---|---|
| typography | Title, H2, H3, H4 read as four distinct levels at a glance; CJK body about 36–46 characters per line, line-height ≈ 1.8; numbers in tables align (tabular figures); no orphaned single characters on heading lines |
| whitespace | Section breaks are clearly larger than paragraph breaks; tables, callouts and diagrams have breathing room above and below; nothing touches a container edge |
| visual_hierarchy | Within one screen the reader can tell where they are (active sidebar item, current-section rail), what the section number is, and which callouts are warnings versus notes |
| color | Body text ≥ 4.5 contrast in light and dark; accent reserved for wayfinding (numbers, active state, links); dark mode has no pure-black or pure-white slabs and diagrams follow the theme |
| motion | Motion only explains a change of state: drawer slide, progress bar, jump-target flash, fade of floating buttons; everything respects `prefers-reduced-motion` |
| micro_interaction | Copy-link on heading anchors, smooth jump with landing highlight, back-to-top, image and diagram zoom, horizontal-scroll shadows on wide tables, Esc closes overlays |
| responsive | No page-level horizontal scroll at any viewport; mobile has a reachable table of contents; wide tables scroll inside their frame with a visible cue; table headers stay readable while scrolling |
| originality | A consistent editorial identity (paper tone, serif headings, oxblood accent, numbered sections) instead of a generic template; identity never competes with content |

## Classifying a gap

Every gap belongs to exactly one class, and the class decides the fix:

1. **Theme gap**: the renderer handles a general pattern badly (any PRD with a
   wide table, any long LR diagram, any nested list). Fix it in
   `scripts/prd_html_theme.py` (CSS, the post-processing passes, or the page
   script) so every future PRD benefits, then re-render.
2. **Source gap**: the Markdown itself causes it (a 9-column table, an LR
   flowchart with 15 nodes, a heading level skipped). Report it to the user with
   a concrete suggestion (split the table, switch to `flowchart TD`, add the
   missing level). The Markdown changes only with the user's approval.
3. **Accepted**: a soft check that is the right trade-off for this document
   (an 8-column comparison table scrolling on a phone). Record it with one line
   of reasoning.

Fixes land in the renderer or the Markdown source, so the next render
reproduces them. The generated `.html` is always renderer output.
