# Install: OpenClaw

## Prerequisites

- OpenClaw agent environment with file access
- A project directory where you want PRD output

## Step 1: Copy prompt modules to your project

Run from the prd-writer repo root:

```sh
mkdir -p /path/to/your/project/.prd
cp write-prd/SKILL.md /path/to/your/project/.prd/prd-workflow.md
cp opus-prd-polish/SKILL.md /path/to/your/project/.prd/opus-prd-polish.md
cp grill-me/SKILL.md /path/to/your/project/.prd/grill-me.md
cp prd-score/SKILL.md /path/to/your/project/.prd/prd-score.md
cp prd-split/SKILL.md /path/to/your/project/.prd/prd-split.md
cp examples/sample-input-brief.md /path/to/your/project/.prd/
cp examples/sample-ai-agent-prd.md /path/to/your/project/.prd/
cp examples/sample-saas-ops-prd.md /path/to/your/project/.prd/
```

## Step 2: Run it

In your OpenClaw workspace:

```
Read .prd/prd-workflow.md. Run it against my-brief.md. Save the PRD to docs/prd/my-prd.md. Record product_type, output_profile, research_pack, out_of_scope, and audience_split near the top.
```

Or start with the included example brief:

```
Run the prd-workflow skill against .prd/sample-input-brief.md. Save to docs/prd/skyrush-prd.md.
```

For a non-game product:

```
Read .prd/prd-workflow.md. Draft a b2b_saas_ops PRD for an approval queue used by finance ops. Target output_profile: obsidian_md. Save to docs/prd/finance-approval-queue.md.
```

## Step 3: Score or split

```
Read .prd/prd-score.md. Score docs/prd/finance-approval-queue.md.
```

```
Read .prd/prd-split.md. Split docs/prd/finance-approval-queue.md into its audience_split packs.
```

## Agent routing

OpenClaw does not need a prd-writer-specific adapter. Treat each `*.md` file in
`.prd/` as a prompt module:

- `prd-workflow.md`: write a new PRD or revise a brief into a PRD.
- `prd-score.md`: evaluate a PRD without editing it.
- `prd-split.md`: create audience-specific documents.
- `grill-me.md`: challenge an idea or review a PRD draft.

## Format targets

Use `output_profile: obsidian_md`, `word_docx`, `pdf`, `confluence`, or `multi`.
Markdown stays the source artifact; Word, PDF, and Confluence artifacts should be
exported from the Markdown after review.

## Minimum working mode

No config file is required. The prompt modules are self-contained.

## Note on grill-me

Reference `.prd/grill-me.md` when you want idea stress-testing before PRD drafting.
