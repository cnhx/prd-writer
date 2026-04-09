# PRD Writer

Portable PRD writer kit for teams that want structured, reusable, cross-platform PRD workflows.

This repo gives you a clean PRD-writing system that can be adapted to Codex, Claude Code, OpenClaw, or other agent environments with file access and a capable model.

It is built around three layers:

1. agent definition — stable behavior, rules, dependencies, output contract
2. workflow skills — question flow, PRD structure, review checklist, save/publish sequence
3. config — knowledge base, polish mode, publish policy, platform mapping

## Glossary

**Prompt module** — A markdown file that contains instructions for the agent. It is not installed as a software package. The agent reads the file and follows the instructions as part of its context window. If your platform has a formal skill registry, you can register the file there; otherwise reference it by path in your invocation or config.

## What this is for

Use this when you want PRDs that are:
- structured enough for product, design, and engineering handoff
- honest about unknowns instead of faking certainty
- portable across different agent stacks
- configurable instead of hardcoded to one workspace

Typical use cases:
- game product PRDs
- feature PRDs for SaaS or internal tools
- growth funnel specs
- launch-scoped MVP requirement docs
- structured product exploration before implementation

## Core design choices

- Obsidian is optional, not required
- Opus polish is recommended, not mandatory
- git commit is configurable, not mandatory
- output language is not forced
- variables, states, events, and config fields still require readable English identifiers
- art and design requirements live in a dedicated section and must not be mixed into functional requirements

## Repository structure

- `agent/PRD-AGENT.md` — portable agent definition and output contract
- `skills/prd-workflow.md` — main PRD workflow (canonical, used by all platforms)
- `skills/opus-prd-polish.md` — final polish pass (canonical, used by all platforms)
- `config/prd-agent.example.yaml` — base config for portable-core mode
- `platforms/codex/` — Codex adapter (AGENTS.md, config, install guide, sample invocation)
- `platforms/claude-code/` — Claude Code adapter (CLAUDE.md, config, install guide, sample invocation)
- `platforms/openclaw/` — OpenClaw adapter (AGENT.md, config, install guide, sample invocation)
- `examples/` — sample brief, sample PRD output, sample invocation
- `scripts/verify-platform-adapters.sh` — adapter verification
- `tests/verify-platform-adapters.sh` — test entrypoint
- `docs/PORTABILITY.md` — portability boundaries and release checklist

## Fast start (Claude Code)

```sh
git clone <repo-url> prd-writer
mkdir -p my-project/.prd
cp prd-writer/platforms/claude-code/CLAUDE.md my-project/
cp prd-writer/skills/prd-workflow.md my-project/.prd/
cp prd-writer/skills/opus-prd-polish.md my-project/.prd/
cp prd-writer/platforms/claude-code/config.example.yaml my-project/.prd/config.yaml
cp prd-writer/examples/sample-input-brief.md my-project/.prd/
```

```
cd my-project
claude "Read .prd/prd-workflow.md and .prd/config.yaml.
Write a PRD for [your product]. Save to docs/prd/my-prd.md."
```

For other platforms:
- `platforms/codex/INSTALL.md`
- `platforms/openclaw/INSTALL.md`

## Portable core mode

If you prefer to start from the shared core instead of a platform adapter:

1. Copy `agent/PRD-AGENT.md` into your agent workspace
2. Copy the files under `skills/` into your platform's prompt or skill format
3. Start from `config/prd-agent.example.yaml`
4. Decide whether to enable knowledge base access, Opus polish, and git commit

## Validation

Run the adapter verification test before opening a PR:

```sh
sh tests/verify-platform-adapters.sh
```

## Minimal mode

If you want the smallest possible setup, this repo still works with:
- no Obsidian
- no git publishing
- no Opus
- just one model plus local file access

That is deliberate. Good systems degrade gracefully.

## Output contract

The intended final output includes:
- status
- draft path
- context source
- assumptions
- missing info
- review status
- polish metadata
- publish metadata
- next actions

See `agent/PRD-AGENT.md` for the full contract.

## Design rules

- Never invent RTP, odds, regulatory facts, or market data
- Keep assumptions separate from confirmed facts
- Give every variable and state a readable English identifier
- Keep art requirements in their own section
- Write long PRDs to file instead of dumping them into chat
- Use `DONE_WITH_GAPS` when the draft is usable but incomplete

## Portability notes

Portable:
- the agent definition
- the workflow phases
- the review checklist
- the config model
- the output contract

Platform-specific:
- tool names
- file system conventions
- model invocation syntax
- skill installation method
- git execution environment

Read `docs/PORTABILITY.md` before publishing your own variant or adding another platform adapter.

## Recommended next steps

If you plan to extend this repo, the best additions are:
- more example PRDs
- domain-specific overlays for gaming, fintech, SaaS, or internal tools
- install helpers for individual platforms
- tests or lint rules for PRD structure validation

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

## License

MIT
