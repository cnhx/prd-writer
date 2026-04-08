#!/bin/sh

set -eu

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

require_file() {
  path="$1"
  [ -f "$path" ] || fail "missing file $path"
}

require_contains() {
  path="$1"
  pattern="$2"
  grep -F "$pattern" "$path" >/dev/null 2>&1 || fail "$path does not contain: $pattern"
}

require_not_contains() {
  path="$1"
  pattern="$2"
  if grep -F "$pattern" "$path" >/dev/null 2>&1; then
    fail "$path should not contain: $pattern"
  fi
}

cd "$(dirname "$0")/.."

require_file "README.md"
require_file "agent/PRD-AGENT.md"
require_file "config/prd-agent.example.yaml"
require_file "docs/INSTALL-CODEX.md"
require_file "docs/INSTALL-CLAUDE-CODE.md"
require_file "docs/INSTALL-OPENCLAW.md"
require_file "docs/PORTABILITY.md"

require_contains "README.md" "platforms/codex/"
require_contains "README.md" "platforms/claude-code/"
require_contains "README.md" "platforms/openclaw/"
require_contains "README.md" "docs/INSTALL-CODEX.md"
require_contains "README.md" "platforms/codex/sample-invocation.md"
require_not_contains "README.md" "feature: 02-Projects/Tools/prd-writer/assets/banner.svg"

require_contains "agent/PRD-AGENT.md" "### Codex"
require_contains "config/prd-agent.example.yaml" "codex:"

for platform in codex claude-code openclaw; do
  require_file "platforms/$platform/INSTALL.md"
  require_file "platforms/$platform/config.example.yaml"
  require_file "platforms/$platform/prd-workflow.md"
  require_file "platforms/$platform/opus-prd-polish.md"
  require_file "platforms/$platform/sample-invocation.md"
  require_contains "platforms/$platform/INSTALL.md" "sample-invocation.md"
  require_contains "platforms/$platform/INSTALL.md" "examples/sample-input-brief.md"
done

require_file "platforms/codex/AGENTS.md"
require_file "platforms/claude-code/CLAUDE.md"
require_file "platforms/openclaw/AGENT.md"

require_contains "platforms/codex/config.example.yaml" "workflow_file: platforms/codex/prd-workflow.md"
require_contains "platforms/claude-code/config.example.yaml" "workflow_file: platforms/claude-code/prd-workflow.md"
require_contains "platforms/openclaw/config.example.yaml" "workflow_file: platforms/openclaw/prd-workflow.md"

echo "platform adapter verification passed"
