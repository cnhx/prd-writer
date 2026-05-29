# Changelog

## 0.13.0
- added `instruction_safety_policy: descriptive_not_executable` to new PRD metadata so generated documents can distinguish descriptive process text from executable prompt language
- added instruction-safety drafting rules for flow, agent-behavior, reviewer, and Mermaid sections
- added a mandatory Phase 4 Instruction Safety Pass that rewrites command-like process text into product-contract language before publish
- expanded `/prd-score` with an Instruction-like Content Leakage pass/fail check
- updated root design rules and README guidance for downstream AI safety

## 0.12.0
- added first-run language configuration: `/write-prd` asks for document output language on first invocation, stores in `~/.prd-writer/config.json`, skips silently on subsequent runs
- added Phase 5.6 HTML PRD export: generates self-contained `.html` files with Mermaid rendering, styled metadata cards, auto-generated TOC, and print-friendly layout
- added split-aware HTML generation: when audience split is enabled, produces HTML for each split document (GDD, TDD, etc.) with cross-navigation links between them
- added Phase 5.7 interactive HTML mockup: single-frame prototype with state switching via button clicks, timed transitions, and live data simulation
- added dual-view mockup layout: Interactive Prototype tab (click through product flow) + All Screens Overview tab (thumbnail grid, clickable to jump into interactive mode)
- added HTML PRD and interactive mockup examples in `examples/`
- updated README with full workflow documentation covering all new phases
- updated "After Completion" menu with conditional HTML mockup offer (only shown for multi-screen products)

## 0.11.0
- added `scripts/update-skill.sh`, a safe startup updater that fetches upstream and applies only clean fast-forward updates
- added `scripts/install-auto-update-hooks.sh` to register Claude Code and Codex startup hooks from a manual skill install
- added Claude Code plugin hook metadata via `hooks/hooks.json`
- added Codex project-local hook template in `.codex/hooks.json`
- documented manual update checks, forced safe updates, and hook installation paths

## 0.10.0
- added mandatory implementation-detail policy in `/write-prd`; new PRDs default to `semantic_contract_only`
- downgraded technical implementation details into product contracts by default, including Redis, database schema, cache/queue design, service boundaries, framework choices, SDK choices, and deployment topology
- changed Phase 2 option selection from implementation options to product solution options, with engineering follow-up questions for feasibility unknowns
- added condition normalization rules so complex decision logic is consolidated into decision tables instead of scattered nested bullets
- added mandatory exception flow coverage for core flows, including failure, recovery, and user-visible messaging
- added Phase 4 cleanup passes for tech leakage, condition consolidation, and exception coverage
- expanded `/prd-score` with implementation leakage, atomic pressure, condition consolidation, and exception coverage pass/fail gates
- updated README and root skill rules to make product-contract-only PRD writing the default behavior

## 0.9.0
- added product-type routing for `game_interactive`, `ai_agent`, `b2b_saas_ops`, `data_analytics`, `platform_marketplace`, `consumer_growth`, `content_learning`, and `mixed`
- added `output_profile` support for `obsidian_md`, `word_docx`, `pdf`, `confluence`, and `multi`
- added `research_pack` metadata and evidence labels for evidence-backed, assumption-backed, and stakeholder-request decisions
- expanded Phase 3.5 into Diagram Studio with product-type diagram defaults and Mermaid quality rules
- expanded `/prd-split` from game-only discipline documents into audience packs for AI agents, SaaS/Ops, data products, platform products, growth products, and learning products
- added Evidence Score and export readiness checks to `/prd-score`
- added Hermes installation guide and refreshed Codex/OpenClaw prompt-module guides
- added AI agent and SaaS/Ops sample PRDs with Mermaid diagrams and export metadata

## 0.8.0
- added `/prd-split` sub-skill: split a unified PRD into discipline-specific requirement documents (GDD, TDD, Art & Audio, BD & Marketing) with structured requirements tables and INDEX.md summary
- added Phase 0.4 Discipline split configuration (default: ON) in `/write-prd` — user confirms discipline selection before interrogation
- added Phase 5.5 auto-generation of discipline documents after PRD save
- discipline mapping: 14 PRD sections classified as primary, secondary, or crosscutting per discipline
- requirements extraction: paragraph/key-point granularity with auto-assigned IDs (`GDD-4-001`), priority inference, and `to_be_confirmed` flagging
- added sample GDD output in `examples/sample-split-gdd.md`

## 0.7.0
- added Phase 3.5 optional inline-Mermaid diagram generation (zero external dependencies)
- diagram routing: §4 product flow → `stateDiagram-v2`, §5 interactions → `sequenceDiagram`, §6 UI → `block-beta` (fallback `flowchart`), §9 architecture → `flowchart`/`graph`
- all diagrams inline in ` ```mermaid ` code fences — no companion files, no external renderer
- added `diagrams_generated` YAML metadata block in PRD for traceability
- added prd-score §7 Diagram integrity (informational, does not affect verdict)
- expanded sample-output-prd.md with inline Mermaid stateDiagram and block-beta wireframe examples

## 0.6.0
- added Phase 0.1 mandatory history alignment (scan `docs/prd/` + memory store before interrogation)
- added Phase 0.2 product code / series anchor (no invented placeholders)
- added Phase 0.3 Out-of-Scope boundary scan (checklist of owner-overreach categories)
- added §3.2 terminology-with-example rule (every self-coined term pairs with failure + remediation example at first use)
- added §3.3 Assumption vs Open Question distinction (active stance vs passive dependency)
- replaced Phase 4 self-review with mandatory grill-driven review (≥ 2 rounds)
- added grill-me "batch, don't dribble" editing rule (>3 edits → re-read + Write section)
- added /prd-score sub-skill: Structure Completeness %, Owner Closure %, Open-Question residue, Green/Yellow/Red verdict
- bumped root skill version to 0.6.0
- kept v0.6 counterintuitive rules (Rejection Letter / narrow MVP / kill criteria / decisive evidence / fallback narrative) from prior iteration

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
