# PRD Writer

Portable PRD writer kit for teams that want structured, reusable, cross-platform PRD workflows.

This repo gives you a clean PRD-writing system that can be adapted to Hermes, OpenClaw, Claude Code, or any agent environment with file access and a decent model.

It is built around three layers:

1. agent definition — stable behavior, rules, dependencies, output contract
2. workflow skills — question flow, PRD structure, review checklist, save/publish sequence
3. config — knowledge base, polish mode, publish policy, platform mapping

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

- `agent/PRD-AGENT.md` — portable agent definition
- `skills/prd-workflow.md` — main PRD workflow
- `skills/opus-prd-polish.md` — final polish pass
- `config/prd-agent.example.yaml` — base config example
- `config/claude-code.example.yaml` — Claude Code-oriented config
- `config/openclaw.example.yaml` — OpenClaw-oriented config
- `config/hermes.example.yaml` — Hermes-oriented config
- `docs/PORTABILITY.md` — portability boundaries and release checklist
- `docs/INSTALL-CLAUDE-CODE.md` — Claude Code setup notes
- `docs/INSTALL-OPENCLAW.md` — OpenClaw setup notes
- `docs/INSTALL-HERMES.md` — Hermes setup notes
- `examples/sample-input-brief.md` — sample brief
- `examples/sample-output-prd.md` — sample PRD output
- `examples/sample-invocation.md` — sample invocation prompt

## Fast start

1. Copy `agent/PRD-AGENT.md` into your agent workspace
2. Copy or translate the files under `skills/` into your platform's prompt or skill format
3. Start from `config/prd-agent.example.yaml`
4. Decide whether to enable:
   - knowledge base access
   - Opus polish
   - git commit
5. Run the workflow against `examples/sample-input-brief.md`

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

Read `docs/PORTABILITY.md` before publishing your own variant.

## Recommended next steps

If you plan to extend this repo, the best additions are:
- more example PRDs
- domain-specific overlays for gaming, fintech, SaaS, or internal tools
- install helpers for individual platforms
- tests or lint rules for PRD structure validation

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

## Project governance

- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`SECURITY.md`](SECURITY.md)
- [`.github/release-template.md`](.github/release-template.md)

## License

MIT
