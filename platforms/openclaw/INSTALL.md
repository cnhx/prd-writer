# Install: OpenClaw

## Prerequisites

- OpenClaw agent environment with file access
- A project directory where you want PRD output

## Step 1: Copy files to your project

Run from the prd-writer repo root:

```sh
cp platforms/openclaw/AGENT.md /path/to/your/project/
mkdir -p /path/to/your/project/.prd
cp skills/prd-workflow.md /path/to/your/project/.prd/
cp skills/opus-prd-polish.md /path/to/your/project/.prd/
cp platforms/openclaw/config.example.yaml /path/to/your/project/.prd/config.yaml
cp examples/sample-input-brief.md /path/to/your/project/.prd/
```

If your project already has agent definitions, merge the PRD agent rules into your existing config rather than replacing it.

Your project should now look like:

```
your-project/
├── AGENT.md
└── .prd/
    ├── config.yaml
    ├── prd-workflow.md
    ├── opus-prd-polish.md
    └── sample-input-brief.md
```

## Step 2: Edit config.yaml

Open `.prd/config.yaml` and update:

- `paths.output_dir` — where PRDs should be saved (default: `./docs/prd`)
- `knowledge_base.enabled` — `true` if you have an Obsidian vault
- `knowledge_base.root_path` — path to your vault (if enabled)
- `polish.enabled` — `true` or `false`
- `publish.git_commit` — `true` or `false`

## Step 3: Run it

In your OpenClaw workspace:

```
Run the prd-workflow skill against the brief in my-brief.md.
Save the PRD to docs/prd/my-prd.md.
```

Or start with the included example brief:

```
Run the prd-workflow skill against .prd/sample-input-brief.md.
Save the PRD to docs/prd/skyrush-prd.md.
```

See `sample-invocation.md` in this directory for more examples.

## Minimum working mode

Set in `.prd/config.yaml`:

- `knowledge_base.enabled: false`
- `publish.git_commit: false`
- `polish.enabled: false`

This gives you a working PRD workflow with just a model and file access.

## What "prompt module" means

This kit uses the term "prompt module" to mean a markdown file that contains instructions for the agent. It is not installed as a package. The agent reads the file content as part of its context window. If your platform has a formal skill registry (e.g., OpenClaw skills), you can register the workflow file there instead of referencing it by path.
