# Sample Invocation (Platform-Agnostic)

These examples show the prompt text you would give your agent. Replace the command prefix with whatever your platform uses (`claude`, `codex`, or your OpenClaw invocation method).

## From a brief file

```
Read .prd/prd-workflow.md and .prd/config.yaml.
Write a PRD for the product described in examples/sample-input-brief.md.
Save the output to docs/prd/skyrush-prd.md.
```

## From a verbal description

```
Follow .prd/prd-workflow.md to write a PRD for a mobile crash game
called SkyRush targeting Southeast Asia. Ask me questions one at a time.
Save the result to docs/prd/skyrush-prd.md.
```

## With polish and git commit

```
Read .prd/prd-workflow.md and .prd/config.yaml.
Write a PRD for the product in my-brief.md.
After the review checklist, run the polish pass from .prd/opus-prd-polish.md.
Save to docs/prd/my-prd.md and commit the result.
```
