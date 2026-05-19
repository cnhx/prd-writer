#!/usr/bin/env bash
# prd-writer 启动更新器：只在干净 worktree 上执行 fast-forward 更新。
set -uo pipefail

MODE="auto"
FORCE=0
VERBOSE=0
TTL_SECONDS="${PRD_WRITER_UPDATE_TTL_SECONDS:-21600}"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --auto)
      MODE="auto"
      ;;
    --check-only)
      MODE="check"
      ;;
    --force)
      FORCE=1
      ;;
    --ttl-seconds)
      shift
      TTL_SECONDS="${1:-21600}"
      ;;
    --verbose)
      VERBOSE=1
      ;;
    -h|--help)
      cat <<'HELP'
Usage: scripts/update-skill.sh [--auto|--check-only] [--force] [--ttl-seconds N] [--verbose]

Checks origin for prd-writer updates. In --auto mode it applies only clean
fast-forward updates. Dirty, ahead, or diverged worktrees are never modified.
HELP
      exit 0
      ;;
    *)
      echo "prd-writer update: unknown option $1" >&2
      exit 2
      ;;
  esac
  shift
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "${script_dir}/.." && pwd)"
state_root="${PRD_WRITER_UPDATE_STATE_DIR:-${XDG_STATE_HOME:-${HOME}/.local/state}/prd-writer}"
state_file="${state_root}/last-update-check"

say() {
  printf '%s\n' "$1"
}

debug() {
  if [ "$VERBOSE" -eq 1 ]; then
    say "$1"
  fi
}

mtime() {
  if stat -f %m "$1" >/dev/null 2>&1; then
    stat -f %m "$1"
  else
    stat -c %Y "$1" 2>/dev/null || printf '0\n'
  fi
}

now_epoch() {
  date +%s
}

write_state() {
  mkdir -p "$state_root" 2>/dev/null || return 0
  printf '%s\n' "$(now_epoch)" > "$state_file" 2>/dev/null || true
}

if ! git -C "$repo_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  debug "prd-writer update: ${repo_dir} is not a git worktree; skipped."
  exit 0
fi

if [ "$FORCE" -ne 1 ] && [ -f "$state_file" ]; then
  last_check="$(mtime "$state_file")"
  now="$(now_epoch)"
  if [ "$last_check" -gt 0 ] && [ $((now - last_check)) -lt "$TTL_SECONDS" ]; then
    debug "prd-writer update: checked recently; skipped."
    exit 0
  fi
fi

upstream="$(git -C "$repo_dir" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
if [ -z "$upstream" ]; then
  if git -C "$repo_dir" rev-parse --verify --quiet origin/main >/dev/null; then
    upstream="origin/main"
  else
    say "prd-writer update: no upstream branch found; skipped."
    write_state
    exit 0
  fi
fi

remote="${upstream%%/*}"
if [ -z "$remote" ] || [ "$remote" = "$upstream" ]; then
  remote="origin"
fi

if ! git -C "$repo_dir" fetch --quiet "$remote"; then
  say "prd-writer update: failed to fetch ${remote}; skipped."
  write_state
  exit 0
fi

write_state

local_sha="$(git -C "$repo_dir" rev-parse HEAD 2>/dev/null || true)"
remote_sha="$(git -C "$repo_dir" rev-parse "$upstream" 2>/dev/null || true)"

if [ -z "$local_sha" ] || [ -z "$remote_sha" ]; then
  say "prd-writer update: could not resolve local or upstream revision; skipped."
  exit 0
fi

if [ "$local_sha" = "$remote_sha" ]; then
  debug "prd-writer update: already current at ${local_sha:0:8}."
  exit 0
fi

base_sha="$(git -C "$repo_dir" merge-base HEAD "$upstream" 2>/dev/null || true)"

if [ "$base_sha" = "$remote_sha" ]; then
  say "prd-writer update: local branch is ahead of ${upstream}; skipped."
  exit 0
fi

if [ "$base_sha" != "$local_sha" ]; then
  say "prd-writer update: local branch diverged from ${upstream}; skipped."
  exit 0
fi

short_local="$(git -C "$repo_dir" rev-parse --short HEAD)"
short_remote="$(git -C "$repo_dir" rev-parse --short "$upstream")"

if [ "$MODE" = "check" ]; then
  say "prd-writer update: update available ${short_local} -> ${short_remote}. Run scripts/update-skill.sh --auto --force to apply."
  exit 0
fi

if [ -n "$(git -C "$repo_dir" status --porcelain)" ]; then
  say "prd-writer update: update available ${short_local} -> ${short_remote}, but local worktree has changes; skipped."
  exit 0
fi

if git -C "$repo_dir" pull --ff-only --quiet; then
  new_sha="$(git -C "$repo_dir" rev-parse --short HEAD)"
  say "prd-writer update: updated ${short_local} -> ${new_sha}."
else
  say "prd-writer update: fast-forward pull failed; skipped."
fi
