---
description: Split a PRD into discipline-specific requirement documents (GDD, TDD, Art & Audio, BD & Marketing)
argument-hint: "<path to PRD>"
---

# /prd-split

Read the skill file at `skills:prd-split` (located at `prd-split/SKILL.md` relative to
this plugin's root) and follow its instructions exactly. The skill splits a unified PRD
into discipline-specific requirement documents with structured requirements tables.

Pass `$ARGUMENTS` as the path to the PRD file to split.

If `$ARGUMENTS` is empty, ask the user which PRD file to split.
