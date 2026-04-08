# Contributing

Thanks for contributing to PRD Writer.

This repo is intentionally small and portable. Please keep it that way.

## What good contributions look like

Good contributions usually do one of these:
- improve portability across agent platforms
- improve PRD structure, review quality, or publish flow
- add examples that make the repo easier to adopt
- clarify docs without bloating the system
- fix incorrect assumptions or stale guidance

Bad contributions usually do one of these:
- hardcode one private workspace layout
- add platform-specific behavior to the portable core without guardrails
- force one output language
- turn optional dependencies into mandatory ones
- add complexity without a clear user benefit

## Contribution principles

1. Keep the portable core portable.
2. Prefer config over hardcoding.
3. Preserve graceful degradation.
4. Keep skills written in English.
5. Do not force final output language.
6. Keep English identifiers for variables, states, events, and config fields.
7. Keep art/design requirements separated from functional requirements.
8. Do not invent market, legal, math, or compliance facts in examples.

## Repository areas

- `agent/` — stable agent definition and output contract
- `skills/` — reusable workflow modules
- `config/` — example configs by platform
- `docs/` — install and portability guidance
- `examples/` — example inputs and outputs
- `scripts/` — repository maintenance and verification helpers
- `tests/` — lightweight validation entrypoints
- `assets/` — visual assets such as banner/social preview

## Before opening a PR

Please check:
- Is this change portable?
- Is this change still useful without Obsidian?
- Is Opus still optional?
- Is git commit still optional?
- Does this introduce a private path, credential assumption, or internal dependency?
- Does this keep the repo understandable for first-time adopters?

## Suggested workflow

1. Fork the repo
2. Create a branch
3. Make focused changes
4. Update docs or examples if behavior changed
5. Open a PR with a short explanation of:
   - what changed
   - why it matters
   - what platforms were considered
6. Run:
   - `sh tests/verify-platform-adapters.sh`

## PR style

Please keep pull requests small and sharp.

Include:
- one-sentence summary
- important tradeoffs
- affected files
- any backward-compatibility concerns

## Example commit messages

- `docs: improve Claude Code install guide`
- `feat: add fallback publish config example`
- `fix: clarify output contract for non-opus polish`
- `refactor: simplify platform mapping language`

## Security and privacy

Never commit:
- private vault paths that identify a real environment
- secrets or tokens
- internal company documents used as examples
- personal data inside sample PRDs

## License

By contributing, you agree that your contributions will be licensed under the MIT License used by this repository.
