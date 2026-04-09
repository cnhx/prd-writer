# Claude Code: Sample Invocation

## Quick start

With `CLAUDE.md` and `.prd/` already set up in your project:

```
claude "Read .prd/prd-workflow.md and .prd/config.yaml.
Then write a PRD for the product described in examples/sample-input-brief.md.
Save the output to docs/prd/skyrush-prd.md."
```

## Minimal invocation (no brief file)

```
claude "Follow .prd/prd-workflow.md to write a PRD for a mobile crash game
called SkyRush targeting Southeast Asia. Ask me questions one at a time.
Save the result to docs/prd/skyrush-prd.md."
```

## With polish enabled

```
claude "Read .prd/prd-workflow.md and .prd/config.yaml.
Write a PRD for the product in my-brief.md.
After the review checklist, run the polish pass from .prd/opus-prd-polish.md.
Save to docs/prd/my-prd.md."
```

## With git commit

```
claude "Read .prd/prd-workflow.md and .prd/config.yaml.
Write a PRD for the product in my-brief.md.
Save to docs/prd/my-prd.md and commit the result."
```
