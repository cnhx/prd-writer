#!/usr/bin/env python3
"""
PRD HTML 主题模板 — refined editorial（双栏 Docs 风）

布局：
  左 280px 章节侧栏（自动从 H2 抽取）+ 跨文档导航（可选）
  中 760px 正文（serif 标题 + Noto Sans SC 正文，warm ivory 底）
  右 220px mini-TOC（当前章节的 H3 / H4，IntersectionObserver 同步）

特性：
  - frontmatter 折叠卡片
  - 表格 sticky thead + scroll-shadow
  - blockquote 自动识别 ⚠️ / 📝 / ✅ 渲染成 callout
  - mermaid 块原样保留，CDN 渲染
  - 锚点 hover 显示 #
  - 响应式：<1280 隐藏右栏，<920 隐藏左栏
  - 打印优化

使用：
    from prd_html_theme import build_html

    build_html(
        md_path=Path("PRD.md"),
        html_path=Path("PRD.html"),
        brand={"crest": "...", "product": "Product Name", "ver": "v1.0 · draft"},
        badges=[
            {"text": "PRD · v1.0 draft", "accent": True},
            {"text": "..."},
        ],
        cross_doc_nav=[  # for multi-doc projects (e.g. GDD + TDD split)
            {"title": "GDD", "href": "PRD-gdd.html", "active": False},
            ...
        ],
    )
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Optional

import markdown
import yaml


# ---------------------------------------------------------------------------
# CSS — 主题样式（refined editorial）
# ---------------------------------------------------------------------------

CSS = r"""
:root {
  --font-serif: "Source Serif 4", "Source Serif Pro", "Songti SC", "STSong", Georgia, serif;
  --font-sans: "Noto Sans SC", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", "Cascadia Code", Menlo, Consolas, monospace;

  --ivory:        #fbfaf6;
  --ivory-soft:   #f5f4ee;
  --ivory-deep:   #efede2;
  --rule:         #e6e3d8;
  --rule-soft:    #ece9dd;

  --ink:          #1a1817;
  --ink-2:        #3a3733;
  --ink-3:        #6b6760;
  --ink-4:        #98948a;

  --accent:       #8b2c1f;
  --accent-soft:  #c25a4a;
  --accent-bg:    #faeae6;

  --warn-bg:      #fdf6dd;
  --warn-bd:      #d4a017;
  --info-bg:      #e7eff8;
  --info-bd:      #3a6ea5;
  --ok-bg:        #e3efe2;
  --ok-bd:        #4a7a47;
  --note-bg:      #f0eee5;
  --note-bd:      #98948a;

  --code-bg:      #f3f1e8;
  --code-bg-soft: #f7f5ed;

  --sidebar-w:    280px;
  --rail-w:       220px;
  --gutter:       48px;
  --content-w:    760px;
}

* { box-sizing: border-box; }

html, body {
  margin: 0; padding: 0;
  background: var(--ivory);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.75;
  font-feature-settings: "kern", "liga", "calt";
  -webkit-font-smoothing: antialiased;
}

body::before {
  content: "";
  position: fixed; inset: 0;
  pointer-events: none;
  background-image:
    radial-gradient(circle at 25% 30%, rgba(139,44,31,0.012) 0, transparent 50%),
    radial-gradient(circle at 75% 70%, rgba(58,55,51,0.015) 0, transparent 50%);
  z-index: 0;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px; }

/* Layout */
.layout {
  display: grid;
  grid-template-columns: var(--sidebar-w) minmax(0, 1fr) var(--rail-w);
  max-width: calc(var(--sidebar-w) + var(--content-w) + var(--rail-w) + var(--gutter) * 4);
  margin: 0 auto;
  position: relative;
  z-index: 1;
}
.sidebar-left, .sidebar-right {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  padding: 32px 24px;
}
.sidebar-left { border-right: 1px solid var(--rule); }
.sidebar-right { border-left: 1px solid var(--rule); }
.content { padding: 56px var(--gutter) 120px; min-width: 0; }

.sidebar-left::-webkit-scrollbar,
.sidebar-right::-webkit-scrollbar { width: 6px; }
.sidebar-left::-webkit-scrollbar-thumb,
.sidebar-right::-webkit-scrollbar-thumb { background: var(--rule); border-radius: 3px; }

/* Brand */
.brand {
  padding-bottom: 22px;
  margin-bottom: 18px;
  border-bottom: 1px solid var(--rule);
}
.brand .crest {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--accent);
}
.brand .product {
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 500;
  color: var(--ink);
  margin-top: 4px;
  line-height: 1.3;
}
.brand .ver {
  display: inline-block;
  margin-top: 6px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-3);
  padding: 2px 8px;
  background: var(--ivory-soft);
  border: 1px solid var(--rule);
  border-radius: 999px;
}

/* Cross-doc nav (for multi-doc projects, e.g. a GDD + TDD split) */
.cross-doc {
  padding-bottom: 18px;
  margin-bottom: 18px;
  border-bottom: 1px solid var(--rule);
}
.cross-doc-eyebrow,
.nav-eyebrow,
.rail-eyebrow {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-4);
  margin: 0 0 10px;
}
.cross-doc-nav {
  display: flex;
  flex-direction: column;
  gap: 1px;
  font-size: 13.5px;
}
.cross-doc-nav a {
  display: block;
  padding: 6px 12px;
  color: var(--ink-2);
  border-left: 2px solid transparent;
  border-radius: 0 4px 4px 0;
  transition: color 120ms ease, background 120ms ease, border-color 120ms ease;
}
.cross-doc-nav a:hover {
  color: var(--ink);
  background: var(--ivory-soft);
  text-decoration: none;
}
.cross-doc-nav a.active {
  color: var(--accent);
  font-weight: 500;
  border-left-color: var(--accent);
  background: var(--accent-bg);
  pointer-events: none;
}

/* Section nav (auto-generated from H2) */
.nav-eyebrow { margin: 18px 0 10px; }
.section-nav {
  display: flex;
  flex-direction: column;
  gap: 1px;
  font-size: 14px;
}
.section-nav a {
  display: block;
  padding: 7px 12px 7px 14px;
  color: var(--ink-2);
  border-left: 2px solid transparent;
  border-radius: 0 4px 4px 0;
  transition: color 120ms ease, background 120ms ease, border-color 120ms ease;
  line-height: 1.45;
}
.section-nav a:hover {
  color: var(--ink);
  background: var(--ivory-soft);
  text-decoration: none;
}
.section-nav a.active {
  color: var(--accent);
  font-weight: 500;
  border-left-color: var(--accent);
  background: var(--accent-bg);
}
.section-nav .num {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--ink-4);
  margin-right: 8px;
}
.section-nav a.active .num { color: var(--accent-soft); }

/* Doc header */
.doc-header {
  max-width: var(--content-w);
  margin-bottom: 40px;
  padding-bottom: 28px;
  border-bottom: 1px solid var(--rule);
}
.doc-badges {
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}
.doc-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.04em;
  padding: 4px 10px;
  border-radius: 3px;
  background: var(--ivory-soft);
  border: 1px solid var(--rule);
  color: var(--ink-3);
}
.doc-badge.accent {
  background: var(--accent-bg);
  border-color: #f0c7be;
  color: var(--accent);
}
.doc-badge .dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--accent);
  display: inline-block;
}
.doc-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 40px;
  line-height: 1.18;
  letter-spacing: -0.012em;
  color: var(--ink);
  margin: 0 0 14px;
}
.doc-meta {
  font-size: 14px;
  color: var(--ink-3);
}
.doc-meta .sep {
  display: inline-block;
  width: 4px; height: 4px;
  background: var(--ink-4);
  border-radius: 50%;
  margin: 0 10px;
  vertical-align: middle;
}

/* Frontmatter card */
.frontmatter {
  max-width: var(--content-w);
  background: var(--ivory-soft);
  border: 1px solid var(--rule);
  border-radius: 6px;
  margin: 0 0 36px;
  overflow: hidden;
}
.frontmatter summary {
  cursor: pointer;
  padding: 14px 20px;
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--ink-3);
  display: flex;
  align-items: center;
  gap: 10px;
  user-select: none;
  list-style: none;
}
.frontmatter summary::-webkit-details-marker { display: none; }
.frontmatter summary::before {
  content: "▸";
  font-family: var(--font-sans);
  font-size: 11px;
  transition: transform 150ms ease;
  color: var(--ink-4);
  width: 12px;
}
.frontmatter[open] summary::before { transform: rotate(90deg); }
.frontmatter summary .label { text-transform: uppercase; font-weight: 500; }
.frontmatter summary .preview {
  margin-left: auto;
  font-family: var(--font-sans);
  font-size: 12px;
  color: var(--ink-4);
  letter-spacing: normal;
  text-transform: none;
}
.frontmatter[open] summary .preview { opacity: 0; }
.frontmatter .fm-body { padding: 4px 20px 20px; border-top: 1px solid var(--rule-soft); }
.frontmatter dl {
  margin: 14px 0 0;
  display: grid;
  grid-template-columns: 140px 1fr;
  column-gap: 20px;
  row-gap: 8px;
  font-size: 14px;
}
.frontmatter dt {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--ink-3);
  padding-top: 2px;
}
.frontmatter dd { margin: 0; color: var(--ink-2); word-break: break-word; }
.frontmatter dd code,
.frontmatter dt code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: var(--ivory);
  padding: 1px 6px;
  border: 1px solid var(--rule);
  border-radius: 3px;
}
.frontmatter .fm-list { margin: 0; padding-left: 18px; }
.frontmatter .fm-list li { margin: 2px 0; }
.frontmatter .fm-nested {
  margin: 4px 0;
  padding-left: 14px;
  border-left: 2px solid var(--rule);
}

/* Headings */
article { max-width: var(--content-w); }

h1, h2, h3, h4 {
  font-family: var(--font-serif);
  color: var(--ink);
  font-weight: 600;
  position: relative;
  scroll-margin-top: 24px;
}
h1 { display: none; }  /* article H1 hidden; doc-title rendered separately */
h2 {
  font-size: 28px;
  letter-spacing: -0.008em;
  line-height: 1.25;
  margin: 64px 0 18px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--rule);
}
article > h2:first-of-type { margin-top: 0; }
h3 { font-size: 20px; line-height: 1.35; margin: 40px 0 12px; }
h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 28px 0 10px;
  font-family: var(--font-sans);
  color: var(--ink-2);
}

/* Anchor hover */
h2 .anchor, h3 .anchor, h4 .anchor {
  position: absolute;
  left: -22px;
  top: 50%;
  transform: translateY(-55%);
  color: var(--accent-soft);
  opacity: 0;
  font-family: var(--font-sans);
  font-weight: 400;
  font-size: 0.65em;
  transition: opacity 120ms ease;
  text-decoration: none;
}
h2:hover .anchor, h3:hover .anchor, h4:hover .anchor { opacity: 1; }

/* Body */
p { margin: 0.9em 0; color: var(--ink-2); }
strong, b { color: var(--ink); font-weight: 600; }
em, i { color: var(--ink-2); font-style: italic; }
hr {
  border: none;
  margin: 48px 0;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--rule) 20%, var(--rule) 80%, transparent);
}
ul, ol { padding-left: 22px; color: var(--ink-2); }
li { margin: 0.3em 0; }
li::marker { color: var(--ink-4); }

/* Code */
code {
  font-family: var(--font-mono);
  font-size: 0.87em;
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 3px;
  color: var(--ink);
  border: 1px solid var(--rule-soft);
}
pre {
  font-family: var(--font-mono);
  background: var(--code-bg-soft);
  border: 1px solid var(--rule);
  padding: 16px 18px;
  border-radius: 6px;
  overflow-x: auto;
  line-height: 1.55;
  font-size: 13px;
  margin: 18px 0;
  color: var(--ink);
}
pre code { background: transparent; border: none; padding: 0; border-radius: 0; font-size: inherit; color: inherit; }

/* Mermaid */
pre.mermaid {
  background: transparent;
  border: none;
  padding: 16px 0;
  text-align: center;
  font-family: inherit;
  overflow: visible;
  margin: 18px 0;
}

/* Tables */
.table-wrap {
  margin: 22px 0;
  border: 1px solid var(--rule);
  border-radius: 6px;
  overflow: auto;
  max-width: 100%;
  position: relative;
}
table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  font-size: 14px;
  color: var(--ink-2);
}
thead { position: sticky; top: 0; z-index: 2; }
thead th {
  background: var(--ivory-deep);
  font-weight: 600;
  text-align: left;
  padding: 10px 14px;
  font-size: 12.5px;
  letter-spacing: 0.02em;
  color: var(--ink);
  border-bottom: 1px solid var(--rule);
  white-space: nowrap;
}
tbody td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--rule-soft);
  vertical-align: top;
}
tbody tr:last-child td { border-bottom: none; }
tbody tr:nth-child(even) td { background: rgba(245,244,238,0.45); }
tbody td:first-child { font-weight: 500; color: var(--ink); }
tbody tr:hover td { background: var(--accent-bg); }
tbody td code { font-size: 12px; background: var(--ivory); }

/* Callouts */
blockquote {
  margin: 22px 0;
  padding: 14px 18px 14px 44px;
  background: var(--note-bg);
  border-left: 3px solid var(--note-bd);
  border-radius: 0 4px 4px 0;
  color: var(--ink-2);
  font-size: 15px;
  line-height: 1.7;
  position: relative;
}
blockquote::before {
  content: "💬";
  position: absolute;
  left: 14px;
  top: 12px;
  font-size: 16px;
  line-height: 1;
}
blockquote.warn { background: var(--warn-bg); border-color: var(--warn-bd); }
blockquote.warn::before { content: "⚠️"; }
blockquote.info { background: var(--info-bg); border-color: var(--info-bd); }
blockquote.info::before { content: "📝"; }
blockquote.ok { background: var(--ok-bg); border-color: var(--ok-bd); }
blockquote.ok::before { content: "✅"; }
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }
blockquote strong { color: inherit; }
blockquote.warn strong { color: #7a5a00; }
blockquote.info strong { color: #1f4068; }
blockquote.ok strong { color: #2d4d2b; }

/* Right rail mini-TOC */
.mini-toc {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 13px;
  line-height: 1.55;
  border-left: 1px solid var(--rule);
}
.mini-toc li { margin: 0; }
.mini-toc a {
  display: block;
  padding: 5px 12px 5px 14px;
  color: var(--ink-3);
  margin-left: -1px;
  border-left: 1px solid transparent;
  transition: color 120ms ease, border-color 120ms ease;
}
.mini-toc a.lvl4 { padding-left: 26px; font-size: 12.5px; color: var(--ink-4); }
.mini-toc a:hover { color: var(--ink); text-decoration: none; }
.mini-toc a.active {
  color: var(--accent);
  border-left-color: var(--accent);
  font-weight: 500;
}
.mini-toc .empty-hint {
  color: var(--ink-4);
  font-size: 12px;
  padding: 6px 14px;
  font-style: italic;
}

/* Footer */
.doc-footer {
  max-width: var(--content-w);
  margin-top: 80px;
  padding-top: 24px;
  border-top: 1px solid var(--rule);
  font-size: 13px;
  color: var(--ink-4);
  display: flex;
  justify-content: space-between;
}

/* Responsive */
@media (max-width: 1280px) {
  .layout { grid-template-columns: var(--sidebar-w) 1fr; }
  .sidebar-right { display: none; }
  .content { padding-right: 32px; }
}
@media (max-width: 920px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar-left { display: none; }
  .content { padding: 32px 24px 80px; }
}

/* Print */
@media print {
  body::before { display: none; }
  .sidebar-left, .sidebar-right, .doc-footer { display: none; }
  .layout { display: block; }
  .content { padding: 0; max-width: none; }
  article, .doc-header, .frontmatter { max-width: none; }
  .frontmatter summary::before { display: none; }
  details:not([open]) > *:not(summary) { display: revert; }
  h2, h3 { page-break-after: avoid; }
  table, pre, blockquote { page-break-inside: avoid; }
  a { color: var(--ink); text-decoration: none; }
}
"""


# ---------------------------------------------------------------------------
# 字体 + Mermaid CDN
# ---------------------------------------------------------------------------

HEAD_FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=Noto+Sans+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
"""

MERMAID_SNIPPET = """
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js" crossorigin="anonymous"></script>
<script>
  if (window.mermaid) {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'base',
      themeVariables: {
        fontFamily: '"Noto Sans SC", -apple-system, "PingFang SC", sans-serif',
        primaryColor: '#f5f4ee',
        primaryTextColor: '#1a1817',
        primaryBorderColor: '#8b2c1f',
        lineColor: '#6b6760',
        secondaryColor: '#e7eff8',
        tertiaryColor: '#fdf6dd',
        background: '#fbfaf6',
      },
      // 'loose' 保留：PRD 图表常在 label 内用 <br/> 换行；信任模型是单作者本地渲染自有文档
      securityLevel: 'loose',
    });
  }
</script>
"""

# JS — scroll-sync 侧栏 + smooth anchor
SCROLL_JS = r"""
<script>
(function () {
  const navItems = document.querySelectorAll('#section-nav a');
  const tocItems = document.querySelectorAll('#mini-toc a');
  const h2s = document.querySelectorAll('article h2[id]');
  const h3s = document.querySelectorAll('article h3[id], article h4[id]');

  function setActive(items, predicate) {
    items.forEach(el => el.classList.remove('active'));
    const hit = Array.from(items).find(predicate);
    if (hit) hit.classList.add('active');
  }

  function syncByScroll() {
    const y = window.scrollY + 120;
    let curH2 = h2s[0];
    h2s.forEach(h => { if (h.offsetTop <= y) curH2 = h; });
    if (curH2) setActive(navItems, el => el.getAttribute('data-section') === curH2.id);

    let curH3 = null;
    h3s.forEach(h => { if (h.offsetTop <= y + 40) curH3 = h; });
    if (curH3) setActive(tocItems, el => el.getAttribute('href') === '#' + curH3.id);
  }

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => { syncByScroll(); ticking = false; });
      ticking = true;
    }
  }, { passive: true });

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.replaceState(null, '', '#' + id);
      }
    });
  });

  syncByScroll();
})();
</script>
"""


# ---------------------------------------------------------------------------
# Frontmatter YAML 渲染
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
INLINE_YAML_RE = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
MERMAID_RE = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)


def _fmt_scalar(value) -> str:
    if value is None:
        return "<code>null</code>"
    if isinstance(value, bool):
        return f"<code>{'true' if value else 'false'}</code>"
    if isinstance(value, (int, float)):
        return f"<code>{value}</code>"
    return html.escape(str(value))


def _render_value(value) -> str:
    if isinstance(value, dict):
        if not value:
            return "<code>{}</code>"
        out = ['<dl class="fm-nested">']
        for k, v in value.items():
            out.append(f"<dt>{html.escape(str(k))}</dt>")
            out.append(f"<dd>{_render_value(v)}</dd>")
        out.append("</dl>")
        return "".join(out)
    if isinstance(value, list):
        if not value:
            return "<code>[]</code>"
        if all(not isinstance(v, (dict, list)) for v in value):
            return ", ".join(_fmt_scalar(v) for v in value)
        out = ['<ul class="fm-list">']
        for v in value:
            out.append(f"<li>{_render_value(v)}</li>")
        out.append("</ul>")
        return "".join(out)
    return _fmt_scalar(value)


def render_frontmatter_card(data: dict) -> str:
    """Render frontmatter as <details> collapsible card"""
    if not data:
        return ""
    preview_keys = [k for k in ("title", "version", "status", "date", "owner") if k in data]
    preview = " · ".join(html.escape(str(data[k])) for k in preview_keys[:3])

    parts = [
        '<details class="frontmatter">',
        '<summary>',
        '<span class="label">Frontmatter</span>',
        f'<span class="preview">{preview}</span>' if preview else '',
        '</summary>',
        '<div class="fm-body">',
        '<dl>',
    ]
    for k, v in data.items():
        parts.append(f'<dt>{html.escape(str(k))}</dt>')
        parts.append(f'<dd>{_render_value(v)}</dd>')
    parts.append('</dl></div></details>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# Markdown 预处理 / 后处理
# ---------------------------------------------------------------------------

def preprocess_markdown(text: str):
    mermaid_blocks: list[str] = []
    yaml_blocks: list[dict] = []

    def _mermaid_sub(m: re.Match) -> str:
        mermaid_blocks.append(m.group(1))
        return f"\n\n<!--MERMAID_BLOCK_{len(mermaid_blocks) - 1}-->\n\n"

    def _yaml_sub(m: re.Match) -> str:
        try:
            data = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict) and data:
            yaml_blocks.append(data)
            return f"\n\n<!--YAML_BLOCK_{len(yaml_blocks) - 1}-->\n\n"
        return m.group(0)

    text = MERMAID_RE.sub(_mermaid_sub, text)
    text = INLINE_YAML_RE.sub(_yaml_sub, text)
    return text, mermaid_blocks, yaml_blocks


CALLOUT_PREFIXES = [
    ("⚠️", "warn"),
    ("📝", "info"),
    ("✅", "ok"),
    ("🚨", "warn"),
    ("💡", "info"),
    ("ℹ️", "info"),
]


def _decorate_callouts(html_body: str) -> str:
    """Detect blockquotes starting with emoji and assign callout class."""
    def repl(m: re.Match) -> str:
        inner = m.group(1)
        # strip leading whitespace, find first text
        cls = None
        leading = re.match(r"\s*<p>\s*(.+?)(?:</p>|<br|$)", inner, re.DOTALL)
        if leading:
            first = leading.group(1)
            # also handle leading <strong> bold tags
            text_only = re.sub(r"<[^>]+>", "", first).lstrip()
            for emoji, kind in CALLOUT_PREFIXES:
                if text_only.startswith(emoji):
                    cls = kind
                    # strip emoji from rendered content (icon now in ::before)
                    inner = inner.replace(emoji, "", 1)
                    break
            if cls is None:
                # detect by leading bold keyword (e.g. **关键约束：**)
                if re.match(r"\s*<strong>(?:关键|⚠|注意|警告|警示|警惕)", first):
                    cls = "warn"
                elif re.match(r"\s*<strong>(?:原则|说明|备注|备查|参考)", first):
                    cls = "info"
                elif re.match(r"\s*<strong>(?:预期|成功|确认|完成|已通过)", first):
                    cls = "ok"
        if cls:
            return f'<blockquote class="{cls}">{inner}</blockquote>'
        return m.group(0)
    return re.sub(r"<blockquote>(.*?)</blockquote>", repl, html_body, flags=re.DOTALL)


def _wrap_tables(html_body: str) -> str:
    html_body = re.sub(r"<table>", '<div class="table-wrap"><table>', html_body)
    html_body = re.sub(r"</table>", "</table></div>", html_body)
    return html_body


def _add_heading_anchors(html_body: str) -> str:
    """Add hover-anchor links to h2/h3/h4"""
    def repl(m: re.Match) -> str:
        tag, attrs, content = m.group(1), m.group(2), m.group(3)
        id_match = re.search(r'id="([^"]+)"', attrs)
        if not id_match:
            return m.group(0)
        hid = id_match.group(1)
        return f'<{tag}{attrs}>{content}<a class="anchor" href="#{hid}">#</a></{tag}>'
    return re.sub(
        r"<(h[234])([^>]*)>(.*?)</\1>",
        repl,
        html_body,
        flags=re.DOTALL,
    )


def postprocess_html(html_body: str, mermaid_blocks: list[str], yaml_blocks: list[dict]) -> str:
    def _mermaid(m: re.Match) -> str:
        # 转义图源——mermaid.js 读 textContent 会自动还原，渲染不受影响，
        # 但能挡掉源码里 </pre> 提前闭合标签的 breakout
        src = html.escape(mermaid_blocks[int(m.group(1))])
        return f'<pre class="mermaid">\n{src}\n</pre>'

    def _yaml(m: re.Match) -> str:
        idx = int(m.group(1))
        return render_yaml_card_inline(yaml_blocks[idx])

    html_body = re.sub(r"<!--MERMAID_BLOCK_(\d+)-->", _mermaid, html_body)
    html_body = re.sub(r"<!--YAML_BLOCK_(\d+)-->", _yaml, html_body)
    html_body = _wrap_tables(html_body)
    html_body = _decorate_callouts(html_body)
    html_body = _add_heading_anchors(html_body)
    return html_body


def render_yaml_card_inline(data: dict) -> str:
    """Inline YAML block (within content) -> styled card, not collapsible"""
    parts = [
        '<div class="frontmatter" open style="margin: 18px 0;">',
        '<div class="fm-body" style="border: none;">',
        '<div style="font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.06em; color: var(--ink-3); text-transform: uppercase; margin-bottom: 10px;">YAML</div>',
        '<dl>',
    ]
    for k, v in data.items():
        parts.append(f'<dt>{html.escape(str(k))}</dt>')
        parts.append(f'<dd>{_render_value(v)}</dd>')
    parts.append('</dl></div></div>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# 自动抽 H2 章节导航
# ---------------------------------------------------------------------------

H2_HTML_RE = re.compile(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', re.DOTALL)
_ANCHOR_TAG_RE = re.compile(r'<a class="anchor".*?</a>', re.DOTALL)


def _split_num(title: str) -> tuple[str, str]:
    """把 "1. 产品概述" 拆成 ("1", "产品概述")；无编号前缀时返回 ("", title)。"""
    num_match = re.match(r'^(\d+|附录\s*[A-Z]|\w+\s*\d+)\.\s*(.+)$', title)
    if num_match:
        return num_match.group(1).strip(), num_match.group(2).strip()
    return "", title


def extract_h2_sections(html_body: str) -> list[dict]:
    """从渲染后的 HTML 抽 H2 章节做侧栏导航。

    anchor 直接取真实 ``<h2 id>``（python-markdown toc 扩展生成），
    保证侧栏链接、滚动高亮与正文锚点永远一致——不再自造 slug。
    代码块内的 ``## `` 不会变成 ``<h2 id>``，重复标题会得到 ``_2`` 去重 id，
    两种情况都被天然正确处理。
    """
    sections = []
    for m in H2_HTML_RE.finditer(html_body):
        anchor = m.group(1)
        content = _ANCHOR_TAG_RE.sub("", m.group(2))
        title = re.sub(r"<[^>]+>", "", content).strip().rstrip("#").strip()
        num, label = _split_num(title)
        sections.append({"title": label, "anchor": anchor, "num": num, "raw_title": title})
    return sections


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def split_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        fm = None
    return fm if isinstance(fm, dict) else None, text[m.end():]


UI_LABELS = {
    "zh": {
        "html_lang": "zh-CN",
        "this_doc": "本文档",
        "on_this_page": "本页内容",
        "no_subsections": "（本文档无 H3 小节）",
        "project_docs": "项目文档",
    },
    "en": {
        "html_lang": "en",
        "this_doc": "Contents",
        "on_this_page": "On this page",
        "no_subsections": "(No subsections in this document)",
        "project_docs": "Documents",
    },
}


def build_html(
    md_path: Path,
    html_path: Path,
    *,
    brand: Optional[dict] = None,
    badges: Optional[list[dict]] = None,
    cross_doc_nav: Optional[list[dict]] = None,
    cross_doc_title: Optional[str] = None,
    custom_title: Optional[str] = None,
    custom_meta_html: Optional[str] = None,
    footer_left: str = "",
    footer_right: str = "",
    lang: str = "zh",
) -> dict:
    """Convert markdown to themed HTML.

    Parameters
    ----------
    md_path : Path
        Source markdown file
    html_path : Path
        Output HTML file
    brand : dict, optional
        {"crest": "...", "product": "...", "ver": "..."} for top-left brand block
    badges : list of dict, optional
        Each: {"text": "...", "accent": bool, "dot": bool}
    cross_doc_nav : list of dict, optional
        For multi-doc projects: [{"title": "...", "href": "...", "active": bool}]
    cross_doc_title : str
        Label for cross-doc nav block ("项目文档" by default)
    custom_title : str, optional
        Override document title (default: first H1)
    custom_meta_html : str, optional
        Override meta line under title (default: auto from frontmatter)
    footer_left, footer_right : str
        Footer text

    Returns
    -------
    dict : {"mermaid": int, "yaml_blocks": int, "h2_sections": int}
    """
    labels = UI_LABELS.get(lang, UI_LABELS["zh"])
    if cross_doc_title is None:
        cross_doc_title = labels["project_docs"]

    # utf-8-sig 透明剥离 BOM——否则前导 ﻿ 会让 H1 / frontmatter 失配
    raw = md_path.read_text(encoding="utf-8-sig")
    frontmatter, body_md = split_frontmatter(raw)

    body_md, mermaid_blocks, yaml_blocks = preprocess_markdown(body_md)

    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={
            "toc": {
                "anchorlink": False,
                "permalink": False,
                "toc_depth": "2-4",
            },
        },
        output_format="html5",
    )
    html_body = md.convert(body_md)
    html_body = postprocess_html(html_body, mermaid_blocks, yaml_blocks)

    # 侧栏章节从渲染后 HTML 的真实 <h2 id> 抽取，锚点与正文永不漂移
    h2_sections = extract_h2_sections(html_body)

    # ---- doc title ----
    if custom_title is None:
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
        custom_title = (
            re.sub(r"<[^>]+>", "", h1_match.group(1)).strip() if h1_match else md_path.stem
        )

    # ---- meta line under title ----
    if custom_meta_html is None and frontmatter:
        meta_parts = []
        for k in ("date", "owner", "version", "status"):
            if k in frontmatter and frontmatter[k]:
                meta_parts.append(html.escape(str(frontmatter[k])))
        sep = '<span class="sep"></span>'
        custom_meta_html = sep.join(meta_parts)

    # ---- badges ----
    badge_html = ""
    if badges:
        badge_html = '<div class="doc-badges">'
        for b in badges:
            cls = "doc-badge accent" if b.get("accent") else "doc-badge"
            dot = '<span class="dot"></span>' if b.get("dot") else ""
            badge_html += f'<span class="{cls}">{dot}{html.escape(b["text"])}</span>'
        badge_html += '</div>'

    # ---- left sidebar ----
    cross_doc_html = ""
    if cross_doc_nav:
        cross_doc_html = (
            '<div class="cross-doc">'
            f'<div class="cross-doc-eyebrow">{html.escape(cross_doc_title)}</div>'
            '<nav class="cross-doc-nav">'
        )
        for item in cross_doc_nav:
            active = " active" if item.get("active") else ""
            href = html.escape(item.get("href", "#"))
            title = html.escape(item.get("title", ""))
            cross_doc_html += f'<a href="{href}" class="{active.strip()}">{title}</a>'
        cross_doc_html += '</nav></div>'

    section_nav_html = f'<div class="nav-eyebrow">{html.escape(labels["this_doc"])}</div><nav class="section-nav" id="section-nav">'
    for s in h2_sections:
        num_span = f'<span class="num">{html.escape(s["num"])}</span>' if s["num"] else ''
        section_nav_html += (
            f'<a href="#{s["anchor"]}" data-section="{s["anchor"]}">'
            f'{num_span}{html.escape(s["title"])}</a>'
        )
    section_nav_html += '</nav>'

    brand_html = ""
    if brand:
        brand_html = (
            '<div class="brand">'
            f'<div class="crest">{html.escape(brand.get("crest", ""))}</div>'
            f'<div class="product">{html.escape(brand.get("product", ""))}</div>'
        )
        if brand.get("ver"):
            brand_html += f'<span class="ver">{html.escape(brand["ver"])}</span>'
        brand_html += '</div>'

    # ---- right rail mini-TOC: collect H3/H4 from rendered HTML ----
    mini_toc_html = build_mini_toc(html_body, labels["no_subsections"])

    # ---- frontmatter card ----
    fm_html = render_frontmatter_card(frontmatter) if frontmatter else ""

    # ---- assemble ----
    full = f"""<!DOCTYPE html>
<html lang="{labels["html_lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(custom_title)}</title>
{HEAD_FONTS}
<style>{CSS}</style>
</head>
<body>
<div class="layout">
  <aside class="sidebar-left">
    {brand_html}
    {cross_doc_html}
    {section_nav_html}
  </aside>
  <main class="content">
    <header class="doc-header">
      {badge_html}
      <h1 class="doc-title">{html.escape(custom_title)}</h1>
      <div class="doc-meta">{custom_meta_html or ''}</div>
    </header>
    {fm_html}
    <article>
{html_body}
    </article>
    <footer class="doc-footer">
      <span>{html.escape(footer_left)}</span>
      <span>{html.escape(footer_right)}</span>
    </footer>
  </main>
  <aside class="sidebar-right">
    <div class="rail-eyebrow">{html.escape(labels["on_this_page"])}</div>
    {mini_toc_html}
  </aside>
</div>
{MERMAID_SNIPPET if mermaid_blocks else ''}
{SCROLL_JS}
</body>
</html>
"""
    html_path.write_text(full, encoding="utf-8")
    return {
        "mermaid": len(mermaid_blocks),
        "yaml_blocks": len(yaml_blocks),
        "h2_sections": len(h2_sections),
    }


def build_mini_toc(html_body: str, empty_label: str = "（本文档无 H3 小节）") -> str:
    """Extract h3/h4 from rendered html for right rail"""
    items = []
    for m in re.finditer(r'<(h3|h4)[^>]*id="([^"]+)"[^>]*>(.*?)</\1>', html_body, re.DOTALL):
        tag, hid, content = m.group(1), m.group(2), m.group(3)
        content = _ANCHOR_TAG_RE.sub("", content)
        text = re.sub(r"<[^>]+>", "", content).strip().rstrip("#").strip()
        items.append((tag, hid, text))

    if not items:
        return f'<ul class="mini-toc"><li><span class="empty-hint">{html.escape(empty_label)}</span></li></ul>'

    out = ['<ul class="mini-toc" id="mini-toc">']
    for tag, hid, text in items:
        cls = "lvl4" if tag == "h4" else "lvl3"
        out.append(f'<li><a href="#{hid}" class="{cls}">{html.escape(text)}</a></li>')
    out.append('</ul>')
    return "".join(out)
