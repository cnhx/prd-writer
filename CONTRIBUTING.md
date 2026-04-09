# Contributing

Thanks for contributing to PRD Writer.

This repo is a small skill collection. Please keep it that way.

## Good contributions

- Improve PRD structure, review quality, or workflow
- Add examples that make the repo easier to adopt
- Clarify docs without bloating
- Fix incorrect assumptions or stale guidance
- Improve cross-platform portability

## Bad contributions

- Hardcode one private workspace layout
- Force one output language
- Turn optional dependencies into mandatory ones
- Add complexity without clear user benefit

## Principles

1. Skills are self-contained markdown files with YAML frontmatter
2. External dependencies degrade gracefully if missing
3. Output language follows user preference, not forced
4. English identifiers for variables, states, events, and config fields
5. Art/design requirements separated from functional requirements
6. Never invent market, legal, math, or compliance facts in examples

## Structure

- Root `SKILL.md` — main entry point and sub-skill index
- `write-prd/`, `prd-refine/`, `opus-prd-polish/`, `grill-me/` — individual skills
- `docs/` — portability and dependency documentation
- `examples/` — sample inputs and outputs
- `platforms/` — install guides for non-Claude-Code platforms
- `scripts/` — setup and verification helpers

## Before opening a PR

- Is this change portable?
- Does it still work without gstack?
- Does it keep the repo understandable for first-time adopters?

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
