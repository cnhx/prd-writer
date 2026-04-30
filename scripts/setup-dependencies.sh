#!/usr/bin/env bash
# setup-dependencies.sh — 检查并安装 prd-writer 依赖
set -euo pipefail

SKILLS_DIR="${HOME}/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "=== prd-writer dependency check ==="
echo ""

# 检查 prd-writer 自身是否已安装
if [ -d "${SKILLS_DIR}/prd-writer" ] || [ -L "${SKILLS_DIR}/prd-writer" ]; then
  echo "[OK] prd-writer installed at ${SKILLS_DIR}/prd-writer"
else
  echo "[MISSING] prd-writer not found in ${SKILLS_DIR}/"
  echo "  Fix: ln -s ${REPO_DIR} ${SKILLS_DIR}/prd-writer"
  ERRORS=$((ERRORS + 1))
fi

# 检查子 skill symlink
for skill in write-prd prd-refine grill-me opus-prd-polish prd-score prd-split; do
  if [ -d "${SKILLS_DIR}/${skill}" ] || [ -L "${SKILLS_DIR}/${skill}" ]; then
    echo "[OK] ${skill} symlink exists"
  else
    echo "[MISSING] ${skill} symlink not found"
    echo "  Fix: ln -s ${SKILLS_DIR}/prd-writer/${skill} ${SKILLS_DIR}/${skill}"
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""

# 检查外部依赖
echo "=== External dependencies ==="
echo ""

if [ -d "${SKILLS_DIR}/gstack" ] || [ -L "${SKILLS_DIR}/gstack" ]; then
  echo "[OK] gstack installed"
else
  echo "[OPTIONAL] gstack not found — some features (QA, design review) unavailable"
  echo "  Install: cd ${SKILLS_DIR} && git clone <gstack-repo> gstack"
fi

echo ""

if [ $ERRORS -eq 0 ]; then
  echo "All required dependencies OK."
else
  echo "${ERRORS} issue(s) found. Run the suggested fix commands above."
  exit 1
fi
