#!/bin/sh
set -eu

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

require_file() {
  [ -f "$1" ] || fail "missing file $1"
}

require_contains() {
  grep -F "$2" "$1" >/dev/null 2>&1 || fail "$1 does not contain: $2"
}

require_not_contains() {
  if grep -F "$2" "$1" >/dev/null 2>&1; then
    fail "$1 should not contain: $2"
  fi
}

require_absent() {
  if [ -f "$1" ]; then
    fail "$1 should have been removed"
  fi
}

cd "$(dirname "$0")/.."

# Core files
require_file "README.md"
require_file "agent/PRD-AGENT.md"
require_file "skills/prd-workflow.md"
require_file "skills/opus-prd-polish.md"
require_file "config/prd-agent.example.yaml"
require_file "docs/PORTABILITY.md"

# README references
require_contains "README.md" "platforms/codex/"
require_contains "README.md" "platforms/claude-code/"
require_contains "README.md" "platforms/openclaw/"
require_contains "README.md" "skills/prd-workflow.md"
require_not_contains "README.md" "hermes"
require_not_contains "README.md" "CODE_OF_CONDUCT"

# Skills are canonical
require_contains "skills/prd-workflow.md" "Phase 0"
require_contains "skills/prd-workflow.md" "Phase 5"
require_contains "skills/opus-prd-polish.md" "Must Preserve"

# No Hermes remnants
require_not_contains "config/prd-agent.example.yaml" "hermes"

# Platform adapters — instruction file, config, install, sample invocation only
for platform in codex claude-code openclaw; do
  require_file "platforms/$platform/INSTALL.md"
  require_file "platforms/$platform/config.example.yaml"
  require_file "platforms/$platform/sample-invocation.md"

  # Workflow/polish should NOT exist in platform dirs
  require_absent "platforms/$platform/prd-workflow.md"
  require_absent "platforms/$platform/opus-prd-polish.md"

  # Config paths should use the installed .prd/ layout, not repo-internal paths
  require_contains "platforms/$platform/config.example.yaml" ".prd/prd-workflow.md"
  require_contains "platforms/$platform/config.example.yaml" ".prd/opus-prd-polish.md"

  # Install guide should reference sample-invocation
  require_contains "platforms/$platform/INSTALL.md" "sample-invocation.md"
done

# Platform-specific instruction files
require_file "platforms/codex/AGENTS.md"
require_file "platforms/claude-code/CLAUDE.md"
require_file "platforms/openclaw/AGENT.md"

# Deleted files should not exist
require_absent "docs/INSTALL-CODEX.md"
require_absent "docs/INSTALL-CLAUDE-CODE.md"
require_absent "docs/INSTALL-OPENCLAW.md"
require_absent "docs/INSTALL-HERMES.md"
require_absent "config/hermes.example.yaml"
require_absent "config/claude-code.example.yaml"
require_absent "config/openclaw.example.yaml"
require_absent "CODE_OF_CONDUCT.md"
require_absent "SECURITY.md"

echo "platform adapter verification passed"
