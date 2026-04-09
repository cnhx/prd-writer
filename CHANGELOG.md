# Changelog

## 0.5.0
- restructured as a skill collection (following gstack pattern)
- each skill is a self-contained directory with SKILL.md and frontmatter
- bundled grill-me as a sub-skill for idea stress-testing
- added /write-prd skill with integrated grill-me optional step (Phase 0.5)
- added /prd-refine and /opus-prd-polish as standalone skills
- added dependency declaration via SKILL.md frontmatter (gstack as external dep)
- added scripts/setup-dependencies.sh for installation verification
- added docs/DEPENDENCIES.md documenting the dependency model
- removed agent/PRD-AGENT.md (rules folded into individual skills)
- removed config/ directory (skills are self-contained, no external config needed)
- removed platforms/claude-code/ adapter (direct clone replaces it)
- simplified platforms/codex/ and platforms/openclaw/ install guides
- removed tests/ and assets/ directories

## 0.4.0
- eliminated workflow and polish duplication: skills/ is now the single source of truth
- rewrote all INSTALL.md files with concrete shell commands, directory trees, and invocation examples
- rewrote all sample-invocation.md files with actual copy-paste prompts
- fixed config paths to work after copying to a target project
- removed Hermes platform (no adapter existed)
- removed redundant docs/INSTALL-*.md files (consolidated into platforms/*/INSTALL.md)
- removed redundant config/claude-code.example.yaml and config/openclaw.example.yaml
- removed CODE_OF_CONDUCT.md, SECURITY.md, and .github/ governance files
- added Glossary section to README defining "prompt module"
- added Fast Start section to README with actual shell commands
- updated test script to verify new structure and catch regressions

## 0.3.0
- added platform-ready adapters for Codex, Claude Code, and OpenClaw
- fixed README rendering by removing repo-specific frontmatter
- added platform-specific invocation examples
- added a repository validation script for adapter consistency

## 0.2.0
- added example input, output, and invocation files
- added platform-specific config examples for Claude Code, OpenClaw, and Hermes
- clarified that output language is not forced
- strengthened portable release guidance

## 0.1.0
- initial portable PRD writer kit
- added agent definition, workflow skill, polish skill, and install docs
