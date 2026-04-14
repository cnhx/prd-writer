---
name: grill-me
description: |
  Interview the user relentlessly about a plan or design until reaching shared understanding,
  resolving each branch of the decision tree. Use when user wants to stress-test a plan,
  get grilled on their design, or mentions "grill me".
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Grill Me

Interview the user relentlessly about every aspect of this plan until we reach a shared
understanding. Walk down each branch of the design tree, resolving dependencies between
decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Stop Conditions

Stop grilling when any of these is true:

1. **Consensus reached** — every top-level decision branch has an explicit answer (user-chosen
   or recommended-and-accepted) and no new forks emerge from the last 3 questions.
2. **Depth cap** — you have asked 15 substantive questions on this plan. Summarize and stop.
3. **Diminishing returns** — two consecutive answers are "whatever you recommend" or "not
   important"; the user has stopped engaging at decision level. Fold remaining branches into
   "assumptions to revisit later" and stop.
4. **User exits** — user says "enough", "that's enough", "ok stop", "proceed", "够了",
   "差不多了", or equivalent. Stop immediately.
5. **Blocking unknown** — you hit a fact only the user's environment can answer (market data,
   internal tool, existing contract). Record as `blocking_unknown` and stop that branch;
   continue other branches if any.

## Editing rule: batch, don't dribble

When the user's answer to a grill round requires changes to an existing
document (e.g. a PRD under review):

- If the changes touch **≤ 3 distinct locations**, use `Edit` per location.
- If the changes touch **> 3 locations**, or span an entire section, **re-read
  the file and rewrite the affected section(s) with `Write`** instead of
  chaining many `Edit` calls.

Rationale: many small edits compound the risk of broken context (stale
line references, duplicated passes, inconsistent tone). A single rewrite per
section after a grill round is safer and clearer to the reviewer.

## Output on Stop

When stopping, produce:

- **Resolved decisions**: list each with the chosen answer.
- **Open questions**: branches left unresolved and why (user exit, blocking unknown, etc.).
- **Assumptions to revisit**: items folded into "we'll assume X for now".
- **Next step**: e.g., "ready for `/write-prd` Phase 1" or "need user input on items X, Y".
