#!/usr/bin/env bash
# 把 prd-writer 自动更新 hook 注册到 Claude Code 和 Codex 的用户配置。
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
updater="${repo_dir}/scripts/update-skill.sh"

if [ ! -x "$updater" ]; then
  chmod +x "$updater"
fi

python3 - "$repo_dir" "$updater" <<'PY'
import json
import shlex
import sys
import time
from pathlib import Path

repo_dir = Path(sys.argv[1]).resolve()
updater = Path(sys.argv[2]).resolve()
home = Path.home()
stamp = time.strftime("%Y%m%d%H%M%S")

command = f"{shlex.quote(str(updater))} --auto"
marker = str(updater)


def backup(path: Path) -> None:
    if path.exists():
        path.with_suffix(path.suffix + f".bak.{stamp}").write_bytes(path.read_bytes())


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Expected object JSON in {path}")
    return data


def has_command(items: list) -> bool:
    for group in items:
        for hook in group.get("hooks", []):
            if marker in hook.get("command", ""):
                return True
    return False


def add_session_hook(path: Path, *, codex: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = load_json(path)
    hooks = data.setdefault("hooks", {})
    session = hooks.setdefault("SessionStart", [])
    if has_command(session):
        return
    entry = {
        "matcher": "startup|resume",
        "hooks": [
            {
                "type": "command",
                "command": command,
                "timeout": 30,
            }
        ],
    }
    if codex:
        entry["hooks"][0]["statusMessage"] = "Updating prd-writer skill"
    session.append(entry)
    backup(path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def enable_codex_hooks(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text() if path.exists() else ""
    lines = text.splitlines()
    features_start = None
    features_end = len(lines)
    codex_hooks_line = None
    in_features = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            if in_features and features_end == len(lines):
                features_end = index
            in_features = stripped == "[features]"
            if in_features:
                features_start = index
                features_end = len(lines)
        elif in_features and stripped.startswith("codex_hooks"):
            codex_hooks_line = index

    if codex_hooks_line is not None:
        if lines[codex_hooks_line].strip() == "codex_hooks = true":
            return
        lines[codex_hooks_line] = "codex_hooks = true"
    elif features_start is not None:
        lines.insert(features_end, "codex_hooks = true")
    else:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(["[features]", "codex_hooks = true"])

    backup(path)
    path.write_text("\n".join(lines) + "\n")


add_session_hook(home / ".claude" / "settings.json", codex=False)
enable_codex_hooks(home / ".codex" / "config.toml")
add_session_hook(home / ".codex" / "hooks.json", codex=True)

print(f"Installed prd-writer auto-update hooks for {repo_dir}")
print("Claude Code: ~/.claude/settings.json")
print("Codex: ~/.codex/config.toml + ~/.codex/hooks.json")
PY
