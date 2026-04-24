# Install: Claude Cowork

## Option A — Install as plugin (recommended)

In Claude Desktop, switch to the **Cowork** tab:

1. Click **Customize** in the left sidebar
2. Click **Add plugin** → **From GitHub**
3. Paste the repository URL and confirm

Cowork will install the plugin and register all commands automatically.

### Available commands after install

| Command | Description |
|---------|-------------|
| `/write-prd` | Full 5-phase PRD workflow |
| `/prd-refine` | Quick edit pass, preserves detail |
| `/opus-prd-polish` | Top-tier clarity and structure pass |
| `/grill-me` | Stress-test a plan or idea |
| `/prd-score` | Score PRD readiness (Green / Yellow / Red) |

Type `/` in the Cowork input to see all available commands from your installed plugins.

## Option B — Install manually

If you prefer manual setup or your organization restricts plugin sources:

1. Clone the repo to any local directory:

```sh
git clone <repo-url> ~/prd-writer
```

2. In Claude Desktop → Cowork → Customize → Add skills, point to the cloned directory.

Cowork discovers skills from any directory you grant file access to.

## Granting file access

Cowork needs read/write access to the directories where you want PRDs saved. When prompted, grant access to your project folder or documents directory.

## Notes

- No terminal or symlinks required — Cowork handles plugin discovery automatically
- No external connectors (`.mcp.json`) needed — prd-writer is self-contained
- Diagrams use inline Mermaid code fences, rendered natively in the Cowork output
- The optional `/opus-prd-polish` command works best with Opus-class models; it degrades gracefully on other tiers
