---
description: Score a PRD against a Ready-to-Dev rubric — Structure, Owner Closure, Open Questions, verdict
argument-hint: "<path to PRD>"
---

# /prd-score

Read the skill file at `skills:prd-score` (located at `prd-score/SKILL.md` relative to
this plugin's root) and follow its instructions exactly. The skill scores a PRD against
a Ready-to-Dev rubric, producing Structure Completeness %, Owner Closure %,
Open-Question residue, and a Green / Yellow / Red verdict.

Pass `$ARGUMENTS` as the path to the PRD file to score.

If `$ARGUMENTS` is empty, ask the user which PRD file to score.
