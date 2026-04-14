# Install: OpenClaw

## Prerequisites

- OpenClaw agent environment with file access
- A project directory where you want PRD output

## Step 1: Copy the skill tree to your project

v0.6 introduces cross-file references (`../examples/...`, `../references/...`) that
only resolve if the installed layout **mirrors the repo structure**. Use a single
`cp -R`:

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

After this, `.prd/` mirrors the repo (see codex INSTALL.md for the full tree
diagram). All `../examples/...` and `../references/...` references inside skill
files resolve in this layout.

## Step 2: Run it

In your OpenClaw workspace:

```
Read .prd/SKILL.md (overview), then .prd/write-prd/SKILL.md (5-phase workflow).
Write a PRD for [product idea or brief]. Save the PRD to docs/prd/my-prd.md and
the rejection-preempt letter to docs/prd/my-prd-rejection-preempt.md.
```

Or with the example brief:

```
Read .prd/SKILL.md then .prd/write-prd/SKILL.md. Run the workflow against the
brief at .prd/examples/sample-input-brief.md. Save outputs under docs/prd/.
```

## Minimum working mode

No config file needed. The skill tree is self-contained prompt modules.

## Note on grill-me

`/grill-me` is included in the tree at `.prd/grill-me/SKILL.md`. Reference it
when you want idea stress-testing before PRD drafting.
