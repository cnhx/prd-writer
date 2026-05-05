---
description: Write a structured PRD with product-type routing, evidence metadata, diagrams, and export profile
argument-hint: "<brief file path or product topic>"
---

# /write-prd

Read the skill file at `skills:write-prd` (located at `write-prd/SKILL.md` relative to
this plugin's root) and follow its instructions exactly. The skill defines a PRD
workflow: context loading, product-type routing, research pack, interrogation,
premise check, PRD drafting with inline Mermaid diagrams, output profile hygiene,
audience split configuration, and review/publish.

Pass `$ARGUMENTS` as the user's input (brief file path or product topic).

If `$ARGUMENTS` is empty, ask the user what they want to write a PRD for. When
drafting, record `product_type`, `output_profile`, `research_pack`,
`out_of_scope`, and `audience_split` near the top of the PRD.
