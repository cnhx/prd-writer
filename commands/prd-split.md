---
description: Split a PRD into audience-specific requirement documents based on product_type
argument-hint: "<path to PRD>"
---

# /prd-split

Read the skill file at `skills:prd-split` (located at `prd-split/SKILL.md` relative to
this plugin's root) and follow its instructions exactly. The skill splits a unified PRD
into audience-specific requirement documents with structured requirements tables.
Game PRDs can produce GDD/TDD/Art/BD docs; non-game PRDs use product-type packs
such as Agent Behavior Spec, Eval Plan, Workflow Spec, Permission Matrix, Metric
Dictionary, API Contract Summary, Experiment Brief, or Learning Outcome Map.

Pass `$ARGUMENTS` as the path to the PRD file to split.

If `$ARGUMENTS` is empty, ask the user which PRD file to split.
