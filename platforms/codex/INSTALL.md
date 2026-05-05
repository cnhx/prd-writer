# Install: Codex

## Prerequisites

- Codex CLI or workspace environment
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

## Step 2: Write a PRD

```
codex "Read .prd/prd-workflow.md. Write a PRD for [your product]. Save to docs/prd/my-prd.md. Set product_type and output_profile near the top."
```

Start with the game example brief:

```
codex "Read .prd/prd-workflow.md. Write a PRD for the product in .prd/sample-input-brief.md. Save to docs/prd/skyrush-prd.md."
```

Start with a non-game product:

```
codex "Read .prd/prd-workflow.md. Draft an ai_agent PRD for an internal support triage agent. Target output_profile: multi. Save to docs/prd/support-triage-agent.md."
```

## Step 3: Score or split an existing PRD

```
codex "Read .prd/prd-score.md. Score docs/prd/support-triage-agent.md."
```

```
codex "Read .prd/prd-split.md. Split docs/prd/support-triage-agent.md into its audience_split packs."
```

## Format targets

Ask Codex to set one of these `output_profile` values:

- `obsidian_md`: keep Markdown and Mermaid source inline.
- `word_docx`: keep headings strict, tables narrow, and diagram captions visible.
- `pdf`: keep diagrams titled and tables page-friendly.
- `confluence`: keep H1-H3 headings, simple tables, explicit links, and diagram attachment notes.
- `multi`: optimize Markdown first, then add Word/PDF/Confluence export notes.

## Minimum working mode

No config file is required. The skill files are self-contained prompt modules.
Codex reads them as part of the prompt context.

## Notes

- For OpenClaw or Hermes, use the same `.prd/` folder pattern and change only the invocation syntax.
- If Codex has access to Obsidian, Word, PDF, or Confluence export tooling in your workspace, keep Markdown as the source file and export from that file.
