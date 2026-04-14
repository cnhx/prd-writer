# Install: OpenClaw

## Prerequisites

- OpenClaw agent environment with file access
- A project directory where you want PRD output

## Step 1: Copy skill files to your project

Run from the prd-writer repo root:

```sh
mkdir -p /path/to/your/project/.prd
# Core skill files
cp write-prd/SKILL.md /path/to/your/project/.prd/prd-workflow.md
cp opus-prd-polish/SKILL.md /path/to/your/project/.prd/opus-prd-polish.md
cp grill-me/SKILL.md /path/to/your/project/.prd/grill-me.md
cp prd-refine/SKILL.md /path/to/your/project/.prd/prd-refine.md
# Root overview + references (v0.6: Counterintuitive Rules live here)
cp SKILL.md /path/to/your/project/.prd/prd-overview.md
cp -R references /path/to/your/project/.prd/
# Example artifacts (v0.6 references these by name)
cp examples/sample-input-brief.md /path/to/your/project/.prd/
cp examples/sample-output-prd.md /path/to/your/project/.prd/
cp examples/sample-phase2-premise.md /path/to/your/project/.prd/
cp examples/sample-rejection-preempt.md /path/to/your/project/.prd/
cp examples/sample-feature-trinity.md /path/to/your/project/.prd/
```

## Step 2: Run it

In your OpenClaw workspace:

```
Run the prd-workflow skill against my-brief.md. Save the PRD to docs/prd/my-prd.md.
```

Or start with the included example brief:

```
Run the prd-workflow skill against .prd/sample-input-brief.md. Save to docs/prd/skyrush-prd.md.
```

## Minimum working mode

No config file needed. The skill files are self-contained prompt modules.

## Note on grill-me

Copy `grill-me/SKILL.md` to your workspace and reference it when you want idea stress-testing before PRD drafting.
