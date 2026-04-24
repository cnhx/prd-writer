---
description: Write a structured PRD from a brief, topic, or vague idea using a 5-phase workflow
argument-hint: "<brief file path or product topic>"
---

# /write-prd

Write a product requirements document using the full 5-phase workflow.

## Usage

```
/write-prd $ARGUMENTS
```

## Workflow

See the **write-prd** skill for the complete workflow:

1. **Phase 0** — Context loading: gather files, docs, history, user input
2. **Phase 1** — Product interrogation: one question at a time about market, users, scope, business model
3. **Phase 2** — Premise check: present assumptions and implementation options for approval
4. **Phase 3** — PRD drafting: structured 14-section document with optional inline Mermaid diagrams
5. **Phase 4** — Review and publish: quality checklist, optional `/opus-prd-polish`, commit

Accepts anything from a vague idea to a detailed brief. If the idea is too vague, offers `/grill-me` first.
