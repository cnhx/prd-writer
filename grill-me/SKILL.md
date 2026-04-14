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
  - Edit
  - Write
---

# Grill Me

`/grill-me` operates in two modes. Choose the mode based on how you are invoked.

## Mode selection

- **Default / conversational invocation** ("grill me on X", "先帮我想清楚")
  → **Interview mode** (below).
- **Review invocation from another skill** (e.g. `/write-prd` Phase 4 says "run
  `/grill-me` in review mode on `<path>`"), or the user explicitly says "grill
  the draft at `<path>`"
  → **Review mode** (below).

If the mode is ambiguous, default to Interview mode and ask the user to confirm.

## Interview mode (default)

Interview the user relentlessly about every aspect of this plan until we reach a shared
understanding. Walk down each branch of the design tree, resolving dependencies between
decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Review mode (autonomous draft critique)

Input: a path to an existing draft (typically a PRD). The draft *is* the answer
to the decision tree — you are no longer interviewing the author.

Each round:

1. **Read** the draft end-to-end. If it's long, take notes of section headings.
2. **Put on one reviewer hat at a time**. Typical hats for PRD review:
   engineering lead, finance, legal / compliance, GTM, leadership. Rotate through
   them across rounds.
3. **Find 2–3 concrete weaknesses** per round, each anchored to a specific line
   or section (cite file + line). No vague complaints ("could be clearer").
4. **Apply remediations directly** using `Edit` (≤ 3 locations) or `Write`
   (section rewrite; see Editing rule below). Do **not** hand back unresolved
   critiques — fix them, or if a fix requires user input, mark the exact
   location with `to_be_confirmed` and a one-line note explaining what's needed.
5. **At the end of the round**, emit a short summary:
   - Reviewer hat used
   - Weaknesses found (location + one line each)
   - Remediations applied (file:line OR "noted `to_be_confirmed`")
   - Round verdict: `round_N_done` or `user_input_required`

Review mode does **not** ask the user questions unless step 4 genuinely requires
external knowledge (real numbers, real stakeholder quotes, compliance facts).

## Stop Conditions (Interview mode)

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

## Stop Conditions (Review mode)

Stop when any of these is true:

1. **Round cap reached** — the caller specified a round count (typically 2–3
   from `/write-prd` Phase 4); you have completed that count.
2. **No more findings** — a round produces zero anchored weaknesses from a
   fresh reviewer hat. Record "round N: no findings" and stop.
3. **Caller-supplied budget exhausted** — if the caller set a time or token
   budget, respect it.
4. **Blocking unknown** — same as interview mode; mark the location with
   `to_be_confirmed` and stop that thread.

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

### Interview mode

- **Resolved decisions**: list each with the chosen answer.
- **Open questions**: branches left unresolved and why (user exit, blocking unknown, etc.).
- **Assumptions to revisit**: items folded into "we'll assume X for now".
- **Next step**: e.g., "ready for `/write-prd` Phase 1" or "need user input on items X, Y".

### Review mode

- **Rounds completed**: N
- **Reviewer hats used**: list (engineering, finance, …)
- **Findings + remediations applied**: table of `location → finding → fix`
- **Still needs user input**: lines marked `to_be_confirmed`, grouped by owner
- **Verdict**: `review_clean` (no open findings) or `review_partial` (user input required, listed above)
