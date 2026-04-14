# Changelog

## 0.6.0 — EvoSkills-inspired flow upgrades

Inspired by [EvoScientist/EvoSkills](https://github.com/EvoScientist/EvoSkills)'s
paper-planning and paper-writing workflows. Non-academic; adapted to PRD review
failure modes.

### Added
- **Counterintuitive rules** (root SKILL.md + write-prd/SKILL.md). Five rules:
  (1) Rejection Letter first, (2) narrow MVP before vision, (3) kill criteria
  before features, (4) budget decisive evidence over polish, (5) predefine
  fallback narrative. References: `references/counterintuitive-prd.md`.
- **Phase 0.5 Part A — mandatory Rejection Letter** (write-prd). Produces
  `rejection-preempt.md` as a sibling file to the PRD. Sample:
  `examples/sample-rejection-preempt.md`. Part B (`/grill-me`) remains optional.
- **Phase 1.0 reverse-story** (write-prd). Four reverse questions
  (Contribution / Insight / Challenge / Framing) before the forward 6 themes.
  Stops Phase 1 if author cannot answer the first three crisply.
- **Feature Trinity** (write-prd Phase 3 §5). Each user-facing feature requires
  User job + Mechanism + Success signal. `trinity_na` allowed for pure infra
  requirements with reason. Sample: `examples/sample-feature-trinity.md`.
- **Reverse-outlining structural check** (write-prd Phase 4.0). Runs before
  content checklist; catches jumps, repetition, missing connectors, buried lede.
- **Artifact Flow table** (root SKILL.md). Explicit what-produces-what across
  the four sub-skills.
- **New files**:
  - `references/counterintuitive-prd.md` (before/after for all 5 rules)
  - `examples/sample-rejection-preempt.md`
  - `examples/sample-feature-trinity.md`
- **Platform sync**: `platforms/codex/INSTALL.md` and
  `platforms/openclaw/INSTALL.md` now copy the full v0.6 skill + references +
  examples set.

### Changed
- write-prd Phase 4 split into Step 4.0 (structural) + Step 4.1 (content). Step
  4.1 adds Rejection Letter closure check and Trinity completeness check.

### Not changed (intentional, v0.7 candidates)
- `/write-prd` remains a single skill covering both planning and writing.
  Splitting into `/prd-planning` + `/prd-writing` deferred to v0.7.
- No timeline / N-day countdown template (PRD deadlines too heterogeneous).
- No mandatory pipeline-figure sketch (tool chains vary too much).

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
