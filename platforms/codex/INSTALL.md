# Install: Codex

## Prerequisites

- Codex CLI or workspace environment
- A project directory where you want PRD output

## Step 1: Copy the skill tree to your project

v0.6 introduces cross-file references (`../examples/...`, `../references/...`) that
only resolve if the installed layout **mirrors the repo structure**. The cleanest
install is a single `cp -R` of all skill directories:

```sh
mkdir -p /path/to/your/project/.prd
cp -R SKILL.md \
      write-prd \
      prd-refine \
      opus-prd-polish \
      grill-me \
      examples \
      references \
   /path/to/your/project/.prd/
```

After this, `.prd/` looks like a scaled-down copy of the repo:

```
.prd/
├── SKILL.md                       # overview: Counterintuitive rules + Artifact flow
├── write-prd/SKILL.md             # 5-phase workflow
├── prd-refine/SKILL.md
├── opus-prd-polish/SKILL.md
├── grill-me/SKILL.md
├── examples/                      # sample artifacts
│   ├── sample-input-brief.md
│   ├── sample-output-prd.md
│   ├── sample-phase2-premise.md
│   ├── sample-rejection-preempt.md
│   └── sample-feature-trinity.md
└── references/
    └── counterintuitive-prd.md
```

All relative references (`../examples/...`, `../references/...`) inside skill
files resolve correctly in this layout.

## Step 2: Run it

Read the overview first, then the workflow:

```
codex "Read .prd/SKILL.md (overview + Counterintuitive rules + Artifact flow), then read .prd/write-prd/SKILL.md (the 5-phase workflow). Write a PRD for [your product]. Save the PRD to docs/prd/my-prd.md and the rejection-preempt letter to docs/prd/my-prd-rejection-preempt.md."
```

Or start with the included example brief:

```
codex "Read .prd/SKILL.md then .prd/write-prd/SKILL.md. Write a PRD for the product described in .prd/examples/sample-input-brief.md. Save outputs under docs/prd/."
```

## Minimum working mode

No config file needed. The skill tree is self-contained. The agent reads the files
as part of its context window.

## Note on grill-me

`/grill-me` is already included in the tree above at `.prd/grill-me/SKILL.md`.
Reference it in your prompt when you want deep idea stress-testing before PRD
drafting:

```
codex "Read .prd/grill-me/SKILL.md and interview me about this idea until we reach consensus."
```
