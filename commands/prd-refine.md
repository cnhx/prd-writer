---
description: Quick polish pass on an existing PRD — edit immediately, preserve detail
argument-hint: "<path to existing PRD>"
---

# /prd-refine

Read the skill file at `skills:prd-refine` (located at `prd-refine/SKILL.md` relative to
this plugin's root) and follow its instructions exactly. The skill performs immediate
edits to an existing PRD without planning or confirmation, preserving all existing
details and depth.

Pass `$ARGUMENTS` as the path to the PRD file to refine.

If `$ARGUMENTS` is empty, ask the user which PRD file to refine.
