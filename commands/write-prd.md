---
description: Write a structured PRD from a brief, topic, or vague idea using a 5-phase workflow
argument-hint: "<brief file path or product topic>"
---

# /write-prd

Read the skill file at `skills:write-prd` (located at `write-prd/SKILL.md` relative to
this plugin's root) and follow its instructions exactly. The skill defines a 5-phase
PRD workflow: context loading, product interrogation, premise check, PRD drafting with
optional inline Mermaid diagrams, and review/publish.

Pass `$ARGUMENTS` as the user's input (brief file path or product topic).

If `$ARGUMENTS` is empty, ask the user what they want to write a PRD for.
