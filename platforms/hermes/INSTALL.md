# Install: Hermes

Hermes support uses the same prompt-module pattern as Codex and OpenClaw. No
Hermes-specific manifest is required by prd-writer.

## Prerequisites

- Hermes agent or workspace that can read local Markdown files
- A project directory where PRD output should be saved

## Step 1: Copy prompt modules

Run from the prd-writer repo root:

```sh
mkdir -p /path/to/your/project/.prd
cp write-prd/SKILL.md /path/to/your/project/.prd/prd-workflow.md
cp grill-me/SKILL.md /path/to/your/project/.prd/grill-me.md
cp opus-prd-polish/SKILL.md /path/to/your/project/.prd/opus-prd-polish.md
cp prd-score/SKILL.md /path/to/your/project/.prd/prd-score.md
cp prd-split/SKILL.md /path/to/your/project/.prd/prd-split.md
cp examples/sample-ai-agent-prd.md /path/to/your/project/.prd/
cp examples/sample-saas-ops-prd.md /path/to/your/project/.prd/
```

## Step 2: Write a PRD

Use a Hermes prompt that first loads the workflow module:

```text
Read .prd/prd-workflow.md.
Write a PRD for an internal agent that triages customer support tickets.
Set product_type: ai_agent.
Set output_profile: multi.
Save the file to docs/prd/support-triage-agent.md.
```

For a SaaS or operations product:

```text
Read .prd/prd-workflow.md.
Write a PRD for a finance approval queue used by operations managers.
Set product_type: b2b_saas_ops.
Set output_profile: obsidian_md.
Save the file to docs/prd/finance-approval-queue.md.
```

## Step 3: Score or split

```text
Read .prd/prd-score.md.
Score docs/prd/support-triage-agent.md.
```

```text
Read .prd/prd-split.md.
Split docs/prd/support-triage-agent.md into its audience_split packs.
```

## Format targets

Use one of these `output_profile` values:

- `obsidian_md`: keep relative links and Mermaid source inline.
- `word_docx`: keep heading levels strict and tables narrow.
- `pdf`: add diagram titles and page-friendly tables.
- `confluence`: keep H1-H3 headings, simple tables, explicit links, and diagram attachment notes.
- `multi`: keep Markdown canonical, then add Word/PDF/Confluence export notes.

## Minimum working mode

If Hermes cannot execute shell commands, copy the files manually into `.prd/`.
The workflow still works as long as Hermes can read the Markdown module before
drafting, scoring, or splitting.
