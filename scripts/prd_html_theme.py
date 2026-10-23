#!/usr/bin/env python3
"""
PRD HTML 主题模板 — refined editorial（三栏 Docs 风）

布局：
  左 272px 章节侧栏（自动从 H2 抽取）+ 跨文档导航（可选）+ 深浅色切换
  中 720px 正文（serif 标题 + Noto Sans SC 正文，暖白底，中文每行约 42 字）
  右 240px mini-TOC（只列当前章节的 H3 / H4，随滚动切换）
  <920px 收成单栏：顶部条 + 抽屉式目录

特性：
  - frontmatter 与首个 H2 前的 yaml 元数据默认隐藏，show_meta=True 时渲染成折叠卡片
  - 深色模式：跟随系统，可手动切换并记住；Mermaid 随主题重绘
  - 中文锚点（#3-功能需求）；点标题旁的 # 复制链接
  - 表格：短列不折行、数字列右对齐、表头吸顶、横向滚动阴影
  - blockquote 自动识别 ⚠️ / 📝 / ✅ 渲染成 callout
  - 阅读进度条、回到顶部、图片点击放大、跳转目标高亮
  - prefers-reduced-motion 下关闭全部动效；打印强制浅色、去掉界面元素

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
import math
import re
from pathlib import Path
from typing import Optional

import markdown
import yaml


# ---------------------------------------------------------------------------
# CSS — 颜色 token 各只定义一次，深色与打印按需复用
# ---------------------------------------------------------------------------

LIGHT_TOKENS = """
  --paper:        #fbfaf6;
  --paper-soft:   #f4f2ea;
  --paper-deep:   #ece9de;
  --rule:         #e3dfd2;
  --rule-soft:    #ebe8dc;
  --ink:          #1a1817;
  --ink-2:        #36332f;
  --ink-3:        #5c5850;
  --ink-4:        #6f6b62;
  --accent:       #8b2c1f;
  --accent-soft:  #b0503f;
  --accent-bg:    #f8e8e3;
  --accent-line:  #ecc5bb;
  --warn-bg:      #fbf3d9;
  --warn-bd:      #c9971a;
  --warn-ink:     #6e5200;
  --info-bg:      #e8eff7;
  --info-bd:      #3a6ea5;
  --info-ink:     #1f4068;
  --ok-bg:        #e5efe3;
  --ok-bd:        #4a7a47;
  --ok-ink:       #2d4d2b;
  --note-bg:      #f1efe6;
  --note-bd:      #a19c90;
  --code-bg:      #f1eee4;
  --pre-bg:       #f6f4ec;
  --row-alt:      rgba(236, 233, 222, 0.35);
  --row-hover:    rgba(248, 232, 227, 0.45);
  --shade:        rgba(26, 24, 23, 0.07);
  --shadow:       0 12px 32px -12px rgba(26, 24, 23, 0.18);
  --scrim:        rgba(26, 24, 23, 0.32);
  --bar-bg:       rgba(251, 250, 246, 0.86);
  color-scheme: light;
"""

DARK_TOKENS = """
  --paper:        #16140f;
  --paper-soft:   #1e1b16;
  --paper-deep:   #27241e;
  --rule:         #36322b;
  --rule-soft:    #2c2923;
  --ink:          #ede7da;
  --ink-2:        #d2cbbd;
  --ink-3:        #aaa396;
  --ink-4:        #948d80;
  --accent:       #e8907c;
  --accent-soft:  #c9735f;
  --accent-bg:    #2e1f1a;
  --accent-line:  #5a352b;
  --warn-bg:      #2b2412;
  --warn-bd:      #b98a1e;
  --warn-ink:     #f0d58a;
  --info-bg:      #172231;
  --info-bd:      #5b8cc4;
  --info-ink:     #b9d2ee;
  --ok-bg:        #18241a;
  --ok-bd:        #5f9a5b;
  --ok-ink:       #bfe0bb;
  --note-bg:      #211e19;
  --note-bd:      #6f695e;
  --code-bg:      #24211b;
  --pre-bg:       #1c1a15;
  --row-alt:      rgba(255, 255, 255, 0.025);
  --row-hover:    rgba(232, 144, 124, 0.07);
  --shade:        rgba(0, 0, 0, 0.35);
  --shadow:       0 16px 40px -12px rgba(0, 0, 0, 0.6);
  --scrim:        rgba(0, 0, 0, 0.55);
  --bar-bg:       rgba(22, 20, 15, 0.85);
  color-scheme: dark;
"""

BASE_CSS = r"""
:root {
  --font-serif: "Source Serif 4", "Noto Serif SC", "Songti SC", "STSong", Georgia, serif;
  --font-sans: "Noto Sans SC", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", "Cascadia Code", Menlo, Consolas, monospace;

  --sidebar-w:    272px;
  --rail-w:       240px;
  --content-w:    720px;
  --gutter:       56px;
  --bar-h:        0px;
  --ease:         cubic-bezier(0.2, 0.8, 0.2, 1);
}

/* 拉丁字母比汉字窄一半，英文正文收窄到约 75 字符一行 */
:root:lang(en) { --content-w: 660px; }

* { box-sizing: border-box; }

html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.8;
  font-feature-settings: "kern", "liga", "calt";
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

::selection { background: var(--accent-bg); color: var(--ink); }

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px; }
a:focus-visible, button:focus-visible, summary:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 3px;
}

/* Reading progress */
.progress {
  position: fixed; top: 0; left: 0; right: 0;
  height: 2px; z-index: 80; pointer-events: none;
}
.progress span {
  display: block; height: 100%;
  background: var(--accent);
  transform-origin: 0 50%;
  transform: scaleX(0);
}

/* Layout */
.layout {
  display: grid;
  grid-template-columns: var(--sidebar-w) minmax(0, 1fr) var(--rail-w);
  max-width: calc(var(--sidebar-w) + var(--content-w) + var(--gutter) * 2 + var(--rail-w));
  margin: 0 auto;
}
.sidebar-left, .sidebar-right {
  position: sticky;
  top: 0;
  height: 100vh;
}
.sidebar-left {
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--rule);
}
.sidebar-scroll { flex: 1; overflow-y: auto; padding: 36px 24px 24px; overscroll-behavior: contain; }
.sidebar-foot {
  padding: 14px 24px 18px;
  border-top: 1px solid var(--rule-soft);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: var(--ink-4);
}
.sidebar-right { overflow-y: auto; padding: 40px 24px; border-left: 1px solid var(--rule); }
.content { padding: 72px var(--gutter) 128px; min-width: 0; }
.content-inner { max-width: var(--content-w); margin: 0 auto; }

.sidebar-scroll::-webkit-scrollbar,
.sidebar-right::-webkit-scrollbar { width: 6px; }
.sidebar-scroll::-webkit-scrollbar-thumb,
.sidebar-right::-webkit-scrollbar-thumb { background: var(--rule); border-radius: 3px; }

/* Brand */
.brand {
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--rule);
}
.brand .crest {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 4px;
}
.brand .crest:empty { display: none; }
.brand .product {
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.35;
  text-wrap: balance;
}
.brand .ver {
  display: inline-block;
  margin-top: 8px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--ink-3);
  padding: 1px 8px;
  background: var(--paper-soft);
  border: 1px solid var(--rule);
  border-radius: 999px;
}

/* Eyebrows */
.cross-doc-eyebrow,
.nav-eyebrow,
.rail-eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-4);
  margin: 0 0 10px;
}

/* Cross-doc nav (for multi-doc projects, e.g. a GDD + TDD split) */
.cross-doc {
  padding-bottom: 18px;
  margin-bottom: 18px;
  border-bottom: 1px solid var(--rule);
}
.cross-doc-nav, .section-nav { display: flex; flex-direction: column; gap: 2px; }
.cross-doc-nav { font-size: 14px; }
.section-nav { font-size: 14.5px; }
.cross-doc-nav a, .section-nav a {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 7px 12px;
  color: var(--ink-2);
  border-left: 2px solid transparent;
  border-radius: 0 6px 6px 0;
  line-height: 1.45;
  transition: color 160ms var(--ease), background-color 160ms var(--ease), border-color 160ms var(--ease);
}
.cross-doc-nav a:hover, .section-nav a:hover {
  color: var(--ink);
  background: var(--paper-soft);
  text-decoration: none;
}
.cross-doc-nav a.active, .section-nav a.active {
  color: var(--accent);
  font-weight: 500;
  border-left-color: var(--accent);
  background: var(--accent-bg);
}
.cross-doc-nav a.active { pointer-events: none; }
.section-nav .num {
  flex: none;
  min-width: 1.4em;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--ink-4);
  font-variant-numeric: tabular-nums;
}
.section-nav a.active .num { color: var(--accent-soft); }

/* Icon buttons */
.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 34px;
  min-width: 34px;
  padding: 0 9px;
  border: 1px solid var(--rule);
  border-radius: 8px;
  background: transparent;
  color: var(--ink-3);
  font: inherit;
  font-size: 13px;
  cursor: pointer;
  transition: color 160ms var(--ease), background-color 160ms var(--ease), border-color 160ms var(--ease);
}
.icon-btn:hover { color: var(--ink); background: var(--paper-soft); border-color: var(--ink-4); }
.icon-btn svg { width: 16px; height: 16px; flex: none; }
.theme-toggle .i-sun { display: none; }
:root[data-theme="dark"] .theme-toggle .i-sun { display: block; }
:root[data-theme="dark"] .theme-toggle .i-moon { display: none; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) .theme-toggle .i-sun { display: block; }
  :root:not([data-theme="light"]) .theme-toggle .i-moon { display: none; }
}

/* Mobile bar + drawer (hidden on wide screens) */
.mobile-bar { display: none; }
.scrim {
  position: fixed; inset: 0;
  background: var(--scrim);
  opacity: 0;
  pointer-events: none;
  z-index: 55;
  transition: opacity 240ms var(--ease);
}

/* Doc header */
.doc-header {
  position: relative;
  margin-bottom: 56px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--rule);
}
.doc-header::after {
  content: "";
  position: absolute;
  left: 0; bottom: -1px;
  width: 56px; height: 2px;
  background: var(--accent);
}
.doc-badges { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.doc-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.02em;
  padding: 3px 10px;
  border-radius: 4px;
  background: var(--paper-soft);
  border: 1px solid var(--rule);
  color: var(--ink-3);
}
.doc-badge.accent { background: var(--accent-bg); border-color: var(--accent-line); color: var(--accent); }
.doc-badge .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); display: inline-block; }
.doc-title {
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: clamp(30px, 3.6vw, 46px);
  line-height: 1.15;
  letter-spacing: -0.015em;
  color: var(--ink);
  margin: 0 0 18px;
  text-wrap: balance;
}
.doc-meta { font-size: 14px; color: var(--ink-3); display: flex; flex-wrap: wrap; align-items: center; row-gap: 4px; }
.doc-meta .sep {
  display: inline-block;
  width: 3px; height: 3px;
  background: var(--ink-4);
  border-radius: 50%;
  margin: 0 10px;
}

/* Frontmatter card */
.frontmatter {
  background: var(--paper-soft);
  border: 1px solid var(--rule);
  border-radius: 8px;
  margin: 0 0 40px;
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
  font-size: 12px;
  transition: transform 160ms var(--ease);
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
.frontmatter dt { font-family: var(--font-mono); font-size: 12px; color: var(--ink-3); padding-top: 2px; }
.frontmatter dd { margin: 0; color: var(--ink-2); word-break: break-word; }
.frontmatter dd code,
.frontmatter dt code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: var(--paper);
  padding: 1px 6px;
  border: 1px solid var(--rule);
  border-radius: 3px;
}
.frontmatter .fm-list { margin: 0; padding-left: 18px; }
.frontmatter .fm-list li { margin: 2px 0; }
.frontmatter .fm-nested { margin: 4px 0; padding-left: 14px; border-left: 2px solid var(--rule); }

/* Headings */
h1, h2, h3, h4 {
  font-family: var(--font-serif);
  color: var(--ink);
  font-weight: 600;
  position: relative;
  scroll-margin-top: calc(var(--bar-h) + 28px);
  text-wrap: balance;
}
article h1, article h2 {
  font-size: 30px;
  line-height: 1.25;
  letter-spacing: -0.01em;
  margin: 88px 0 20px;
  padding-top: 28px;
  border-top: 1px solid var(--rule);
}
article > h2:first-child { margin-top: 0; padding-top: 0; border-top: 0; }
article h3 { font-size: 21px; line-height: 1.4; margin: 48px 0 14px; }
article h4 {
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.5;
  margin: 32px 0 10px;
  color: var(--ink);
}
.h-num { color: var(--accent); font-variant-numeric: tabular-nums lining-nums; }
article h4 .h-num { color: var(--ink-3); }

h2 .anchor, h3 .anchor, h4 .anchor {
  position: absolute;
  left: -1.1em;
  bottom: 0.08em;
  padding-right: 0.3em;
  color: var(--accent-soft);
  opacity: 0;
  font-family: var(--font-sans);
  font-weight: 400;
  font-size: 0.8em;
  transition: opacity 160ms var(--ease);
  text-decoration: none;
}
h2:hover .anchor, h3:hover .anchor, h4:hover .anchor, .anchor:focus-visible { opacity: 1; }

@keyframes target-flash {
  from { background-color: var(--accent-bg); box-shadow: 0 0 0 10px var(--accent-bg); }
  to   { background-color: transparent; box-shadow: 0 0 0 10px transparent; }
}
.is-target { animation: target-flash 1.6s var(--ease); border-radius: 2px; }

/* Body */
p { margin: 1em 0; color: var(--ink-2); text-wrap: pretty; }
strong, b { color: var(--ink); font-weight: 600; }
em, i { color: var(--ink-2); }
.wikilink { color: var(--ink); border-bottom: 1px dashed var(--ink-4); }
hr {
  border: none;
  margin: 56px 0;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--rule) 20%, var(--rule) 80%, transparent);
}
/* 章节前的 --- 与 H2 自带的分割线重复，只留 H2 那条 */
article hr:has(+ h2, + h1) { display: none; }
ul, ol { padding-left: 1.4em; color: var(--ink-2); }
li { margin: 0.35em 0; text-wrap: pretty; }
li > ul, li > ol { margin: 0.2em 0; }
li::marker { color: var(--ink-4); }
ol > li::marker { font-variant-numeric: tabular-nums; }

/* Images */
article img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 8px auto;
  border-radius: 8px;
  border: 1px solid var(--rule);
  background: var(--paper-soft);
}
article img.zoomable { cursor: zoom-in; }
.lightbox {
  position: fixed; inset: 0;
  z-index: 90;
  display: grid;
  place-items: center;
  padding: 4vh 4vw;
  background: var(--scrim);
  backdrop-filter: blur(6px);
  opacity: 0;
  transition: opacity 180ms var(--ease);
  cursor: zoom-out;
}
.lightbox.show { opacity: 1; }
.lightbox img { max-width: 100%; max-height: 92vh; border-radius: 8px; box-shadow: var(--shadow); background: var(--paper); }
.lightbox-figure {
  max-width: 100%;
  max-height: 92vh;
  overflow: auto;
  padding: 24px;
  border-radius: 10px;
  background: var(--paper);
  box-shadow: var(--shadow);
}
.lightbox-figure svg { display: block; height: auto; max-width: none; }
pre.mermaid.zoomable { cursor: zoom-in; }

/* Code */
code {
  font-family: var(--font-mono);
  font-size: 0.86em;
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--ink);
  border: 1px solid var(--rule-soft);
  overflow-wrap: anywhere;
}
pre {
  font-family: var(--font-mono);
  background: var(--pre-bg);
  border: 1px solid var(--rule);
  padding: 16px 18px;
  border-radius: 8px;
  overflow-x: auto;
  line-height: 1.6;
  font-size: 13.5px;
  margin: 20px 0;
  color: var(--ink);
}
pre code { background: transparent; border: none; padding: 0; border-radius: 0; font-size: inherit; color: inherit; overflow-wrap: normal; }

/* Mermaid */
pre.mermaid {
  background: transparent;
  border: none;
  padding: 16px 0;
  text-align: center;
  font-family: inherit;
  overflow-x: auto;
  margin: 24px 0;
}

/* Tables */
.table-frame { position: relative; margin: 24px 0; }
.table-wrap {
  overflow-x: auto;
  border: 1px solid var(--rule);
  border-radius: 8px;
  background: var(--paper);
}
.table-wrap.fits { overflow: visible; }
/* 表格自己横向滚动时，吸顶只能相对滚动容器，偏移归零 */
.table-wrap:not(.fits) th { top: 0; }
.table-frame::before, .table-frame::after {
  content: "";
  position: absolute;
  top: 1px; bottom: 1px;
  width: 20px;
  pointer-events: none;
  opacity: 0;
  z-index: 3;
  transition: opacity 160ms var(--ease);
}
.table-frame::before { left: 1px; border-radius: 8px 0 0 8px; background: linear-gradient(to right, var(--shade), transparent); }
.table-frame::after { right: 1px; border-radius: 0 8px 8px 0; background: linear-gradient(to left, var(--shade), transparent); }
.table-frame.shade-l::before, .table-frame.shade-r::after { opacity: 1; }
table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  font-size: 14.5px;
  line-height: 1.65;
  color: var(--ink-2);
  font-variant-numeric: tabular-nums;
}
th {
  position: sticky;
  top: var(--bar-h);
  z-index: 2;
  background: var(--paper-deep);
  font-weight: 600;
  text-align: left;
  padding: 10px 14px;
  font-size: 13px;
  letter-spacing: 0.02em;
  color: var(--ink);
  border-bottom: 1px solid var(--rule);
  white-space: nowrap;
  vertical-align: bottom;
}
th:first-child { border-top-left-radius: 7px; }
th:last-child { border-top-right-radius: 7px; }
td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--rule-soft);
  vertical-align: top;
}
tbody tr:last-child td { border-bottom: none; }
tbody tr:nth-child(even) td { background: var(--row-alt); }
tbody tr:hover td { background: var(--row-hover); }
td:first-child { font-weight: 500; color: var(--ink); }
td code { font-size: 12.5px; background: var(--paper); }
td { min-width: 4.5em; }
td.long { min-width: 13em; }
td.nw, th.nw { white-space: nowrap; }
td.num, th.num { text-align: right; }
td.nw, td.num { min-width: 0; }
td > p:first-child { margin-top: 0; }
td > p:last-child { margin-bottom: 0; }

/* Callouts */
blockquote {
  margin: 24px 0;
  padding: 14px 18px 14px 46px;
  background: var(--note-bg);
  border-left: 3px solid var(--note-bd);
  border-radius: 0 8px 8px 0;
  color: var(--ink-2);
  font-size: 15.5px;
  line-height: 1.75;
  position: relative;
}
blockquote::before {
  content: "💬";
  position: absolute;
  left: 15px;
  top: 15px;
  font-size: 16px;
  line-height: 1;
}
blockquote.warn { background: var(--warn-bg); border-color: var(--warn-bd); }
blockquote.warn::before { content: "⚠️"; }
blockquote.info { background: var(--info-bg); border-color: var(--info-bd); }
blockquote.info::before { content: "📝"; }
blockquote.ok { background: var(--ok-bg); border-color: var(--ok-bd); }
blockquote.ok::before { content: "✅"; }
blockquote p { color: inherit; }
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }
blockquote strong { color: var(--ink); }
blockquote.warn strong { color: var(--warn-ink); }
blockquote.info strong { color: var(--info-ink); }
blockquote.ok strong { color: var(--ok-ink); }

/* Right rail mini-TOC */
.rail-section {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--ink);
  margin: 0 0 12px;
}
.rail-section:empty { display: none; }
.mini-toc {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 13.5px;
  line-height: 1.5;
  border-left: 1px solid var(--rule);
}
.mini-toc li { margin: 0; }
.mini-toc a {
  display: block;
  padding: 5px 12px 5px 14px;
  color: var(--ink-3);
  margin-left: -1px;
  border-left: 2px solid transparent;
  transition: color 160ms var(--ease), border-color 160ms var(--ease);
}
.mini-toc a.lvl4 { padding-left: 26px; font-size: 13px; color: var(--ink-4); }
.mini-toc a:hover { color: var(--ink); text-decoration: none; }
.mini-toc a.active { color: var(--accent); border-left-color: var(--accent); font-weight: 500; }
.mini-toc .empty-hint { display: block; color: var(--ink-4); font-size: 13px; padding: 6px 14px; }

/* Footer */
.doc-footer {
  margin-top: 96px;
  padding-top: 24px;
  border-top: 1px solid var(--rule);
  font-size: 13px;
  color: var(--ink-4);
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

/* Floating helpers */
.to-top {
  position: fixed;
  right: 24px; bottom: 24px;
  z-index: 40;
  width: 40px; height: 40px;
  border-radius: 50%;
  background: var(--paper);
  box-shadow: var(--shadow);
  opacity: 0;
  transform: translateY(8px);
  pointer-events: none;
  transition: opacity 200ms var(--ease), transform 200ms var(--ease), color 160ms var(--ease), background-color 160ms var(--ease);
}
.to-top.show { opacity: 1; transform: none; pointer-events: auto; }
.toast {
  position: fixed;
  left: 50%; bottom: 32px;
  z-index: 95;
  padding: 8px 16px;
  border-radius: 999px;
  background: var(--ink);
  color: var(--paper);
  font-size: 13px;
  opacity: 0;
  transform: translate(-50%, 8px);
  pointer-events: none;
  transition: opacity 200ms var(--ease), transform 200ms var(--ease);
}
.toast.show { opacity: 1; transform: translate(-50%, 0); }

/* Responsive */
@media (max-width: 1279px) {
  .layout { grid-template-columns: var(--sidebar-w) minmax(0, 1fr); }
  .sidebar-right { display: none; }
  .content { padding-left: 48px; padding-right: 48px; }
}
@media (max-width: 919px) {
  :root { --bar-h: 52px; }
  body { font-size: 16px; line-height: 1.78; }
  .mobile-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 50;
    height: var(--bar-h);
    padding: 0 12px;
    background: var(--bar-bg);
    backdrop-filter: saturate(1.4) blur(10px);
    border-bottom: 1px solid var(--rule);
  }
  .mobile-title {
    flex: 1;
    min-width: 0;
    font-family: var(--font-serif);
    font-weight: 600;
    font-size: 15px;
    color: var(--ink);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .layout { grid-template-columns: minmax(0, 1fr); }
  .sidebar-left {
    position: fixed;
    top: 0; bottom: 0; left: 0;
    width: min(86vw, 320px);
    height: auto;
    z-index: 60;
    background: var(--paper);
    box-shadow: var(--shadow);
    transform: translateX(-102%);
    visibility: hidden;
    transition: transform 260ms var(--ease), visibility 0s linear 260ms;
  }
  .nav-open .sidebar-left { transform: none; visibility: visible; transition-delay: 0s; }
  .nav-open .scrim { opacity: 1; pointer-events: auto; }
  .nav-open { overflow: hidden; }
  .sidebar-foot { display: none; }
  .section-nav a { padding-top: 9px; padding-bottom: 9px; }
  .content { padding: 32px 20px 96px; }
  .doc-header { margin-bottom: 40px; padding-bottom: 24px; }
  article h1, article h2 { font-size: 24px; margin-top: 64px; padding-top: 22px; }
  article h3 { font-size: 19px; margin-top: 36px; }
  article h4 { font-size: 16px; }
  h2 .anchor, h3 .anchor, h4 .anchor { display: none; }
  table { font-size: 14px; }
  td { min-width: 5.5em; }
  td.long { min-width: 8.5em; }
  td.nw, td.num { min-width: 0; }
  blockquote { padding-left: 42px; font-size: 15px; }
  .to-top { right: 16px; bottom: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    transition-delay: 0s !important;
  }
}

/* Print */
@media print {
  .progress, .mobile-bar, .scrim, .sidebar-left, .sidebar-right, .doc-footer, .to-top, .toast, .lightbox { display: none !important; }
  body { font-size: 11pt; line-height: 1.65; }
  .layout { display: block; max-width: none; }
  .content { padding: 0; }
  .content-inner { max-width: none; }
  .frontmatter summary::before { display: none; }
  details:not([open]) > *:not(summary) { display: revert; }
  h2, h3, h4 { break-after: avoid; }
  article h1, article h2 { margin-top: 32pt; }
  table, pre, blockquote, img { break-inside: avoid; }
  .table-wrap { overflow: visible; }
  .table-frame::before, .table-frame::after { display: none; }
  th { position: static; }
  a { color: var(--ink); text-decoration: none; }
}
"""

CSS = (
    ":root {" + LIGHT_TOKENS + "}\n"
    '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {' + DARK_TOKENS + "} }\n"
    ':root[data-theme="dark"] {' + DARK_TOKENS + "}\n"
    + BASE_CSS
    + '@media print { :root, :root[data-theme="dark"] {' + LIGHT_TOKENS + "} }\n"
)


# ---------------------------------------------------------------------------
# 字体 + Mermaid CDN
# ---------------------------------------------------------------------------

HEAD_FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Noto+Serif+SC:wght@600;700&family=Noto+Sans+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
"""

# 在首屏绘制前套用记住的主题，避免闪一下浅色
HEAD_THEME_JS = """<script>try{var t=localStorage.getItem('prd-theme');if(t==='dark'||t==='light')document.documentElement.dataset.theme=t;}catch(e){}</script>"""

MERMAID_SNIPPET = """
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js" crossorigin="anonymous"></script>
"""

ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg>'
ICON_MOON = '<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
ICON_SUN = '<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/></svg>'
ICON_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg>'

# JS — 滚动同步、主题、抽屉目录、表格阴影、复制锚点、图片放大
PAGE_JS = r"""
<script>
(function () {
  const root = document.documentElement;
  const body = document.body;
  const $$ = (sel, el) => Array.from((el || document).querySelectorAll(sel));
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const darkMq = matchMedia('(prefers-color-scheme: dark)');
  const T = body.dataset;

  const resolvedTheme = () => root.dataset.theme || (darkMq.matches ? 'dark' : 'light');

  // Mermaid 颜色直接取 CSS token，保证与主题同源
  function renderMermaid() {
    const blocks = $$('pre.mermaid');
    if (!window.mermaid || !blocks.length) return;
    blocks.forEach((b) => {
      if (b.dataset.src === undefined) b.dataset.src = b.textContent;
      else { b.removeAttribute('data-processed'); b.textContent = b.dataset.src; }
    });
    const cs = getComputedStyle(root);
    const v = (name) => cs.getPropertyValue(name).trim();
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      darkMode: resolvedTheme() === 'dark',
      themeVariables: {
        fontFamily: '"Noto Sans SC", -apple-system, "PingFang SC", sans-serif',
        background: v('--paper'),
        primaryColor: v('--paper-soft'),
        primaryTextColor: v('--ink'),
        primaryBorderColor: v('--accent'),
        secondaryColor: v('--info-bg'),
        tertiaryColor: v('--warn-bg'),
        lineColor: v('--ink-3'),
        textColor: v('--ink'),
        titleColor: v('--ink'),
        edgeLabelBackground: v('--paper'),
        clusterBkg: v('--paper-soft'),
        clusterBorder: v('--rule'),
        noteBkgColor: v('--warn-bg'),
        noteTextColor: v('--ink'),
        noteBorderColor: v('--warn-bd'),
      },
      // 'loose' 保留：PRD 图表常在 label 内用 <br/> 换行；信任模型是单作者本地渲染自有文档
      securityLevel: 'loose',
    });
    mermaid.run({ nodes: blocks }).then(markZoomableDiagrams, () => {});
  }

  // 被缩小超过 15% 的图允许点开看原尺寸
  function markZoomableDiagrams() {
    $$('pre.mermaid').forEach((pre) => {
      const svg = pre.querySelector('svg');
      const natural = svg && svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal.width : 0;
      pre.classList.toggle('zoomable', !!natural && natural > svg.getBoundingClientRect().width * 1.15);
    });
  }

  $$('.theme-toggle').forEach((btn) => btn.addEventListener('click', () => {
    const next = resolvedTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('prd-theme', next); } catch (e) {}
    renderMermaid();
  }));
  darkMq.addEventListener('change', () => { if (!root.dataset.theme) renderMermaid(); });

  // 抽屉目录（窄屏）
  const navToggle = document.querySelector('.mobile-nav-toggle');
  function closeNav() {
    if (!body.classList.contains('nav-open')) return;
    body.classList.remove('nav-open');
    navToggle && navToggle.setAttribute('aria-expanded', 'false');
  }
  navToggle && navToggle.addEventListener('click', () => {
    const open = body.classList.toggle('nav-open');
    navToggle.setAttribute('aria-expanded', String(open));
    if (open) { const a = document.querySelector('#section-nav a.active, #section-nav a'); a && a.focus({ preventScroll: true }); }
  });
  document.querySelector('.scrim').addEventListener('click', closeNav);

  // 滚动同步：左栏章节、右栏当前章节的小节、进度条、回到顶部
  const h2s = $$('article h2[id]');
  const subs = $$('article h3[id], article h4[id]');
  const navLinks = $$('#section-nav a');
  const tocLinks = $$('#mini-toc a');
  const railTitle = document.getElementById('rail-section');
  const navBox = document.querySelector('.sidebar-scroll');
  const rail = document.querySelector('.sidebar-right');
  const bar = document.querySelector('.progress span');
  const toTop = document.querySelector('.to-top');
  const topOf = (el) => el.getBoundingClientRect().top + window.scrollY;
  let current;

  function keepVisible(box, el) {
    const b = box.getBoundingClientRect(), r = el.getBoundingClientRect();
    if (r.top < b.top + 60 || r.bottom > b.bottom - 60) box.scrollTop += r.top - b.top - b.height / 3;
  }

  function sync() {
    const y = window.scrollY + (parseFloat(getComputedStyle(root).getPropertyValue('--bar-h')) || 0) + 100;
    let h2 = h2s[0] || null;
    for (const h of h2s) { if (topOf(h) <= y) h2 = h; else break; }
    const id = h2 ? h2.id : null;
    if (id !== current) {
      current = id;
      navLinks.forEach((a) => {
        const on = a.dataset.section === id;
        a.classList.toggle('active', on);
        on ? a.setAttribute('aria-current', 'location') : a.removeAttribute('aria-current');
        if (on && navBox && !body.classList.contains('nav-open')) keepVisible(navBox, a);
      });
      tocLinks.forEach((a) => { a.parentElement.hidden = a.dataset.section !== id; });
      const label = navLinks.find((a) => a.dataset.section === id);
      if (railTitle) railTitle.textContent = label ? label.querySelector('.label').textContent : '';
    }
    let sub = null;
    for (const h of subs) { if (topOf(h) <= y + 8) sub = h; else break; }
    tocLinks.forEach((a) => {
      const on = !!sub && a.getAttribute('href') === '#' + sub.id;
      if (on && !a.classList.contains('active') && rail) keepVisible(rail, a);
      a.classList.toggle('active', on);
    });

    const max = root.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ')';
    if (toTop) toTop.classList.toggle('show', window.scrollY > window.innerHeight * 1.2);
  }

  // 表格：放得下就取消横向滚动容器（表头才能贴住视口），放不下就显示边缘阴影
  const frames = $$('.table-frame');
  function edges(f) {
    const w = f.firstElementChild;
    f.classList.toggle('shade-l', w.scrollLeft > 2);
    f.classList.toggle('shade-r', w.scrollLeft + w.clientWidth < w.scrollWidth - 2);
  }
  function fitTables() {
    frames.forEach((f) => {
      const w = f.firstElementChild;
      w.classList.remove('fits');
      w.classList.toggle('fits', w.scrollWidth <= w.clientWidth + 1);
      edges(f);
    });
  }
  frames.forEach((f) => f.firstElementChild.addEventListener('scroll', () => edges(f), { passive: true }));

  // 跳转：平滑滚动 + 目标高亮；点标题旁的 # 复制链接
  const toast = document.querySelector('.toast');
  let toastTimer;
  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 1600);
  }
  function copyLink(url) {
    const done = () => showToast(T.copied);
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(done, () => {});
    } else {
      const t = document.createElement('textarea');
      t.value = url;
      body.appendChild(t);
      t.select();
      try { document.execCommand('copy'); done(); } catch (e) {}
      t.remove();
    }
  }
  function flash(el) {
    el.classList.remove('is-target');
    void el.offsetWidth;
    el.classList.add('is-target');
    setTimeout(() => el.classList.remove('is-target'), 1700);
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = decodeURIComponent(a.getAttribute('href').slice(1));
    const target = id && document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    closeNav();
    target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    history.replaceState(null, '', '#' + encodeURIComponent(id));
    flash(target);
    if (a.classList.contains('anchor')) copyLink(location.href);
  });
  toTop && toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));

  // 图片：原图比显示尺寸大时可点击放大
  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox';
  lightbox.hidden = true;
  body.appendChild(lightbox);
  function openLightbox(node) {
    lightbox.replaceChildren(node);
    lightbox.hidden = false;
    requestAnimationFrame(() => lightbox.classList.add('show'));
  }
  function closeLightbox() {
    if (lightbox.hidden) return;
    lightbox.classList.remove('show');
    setTimeout(() => { lightbox.hidden = true; }, reduceMotion ? 0 : 180);
  }
  lightbox.addEventListener('click', closeLightbox);
  $$('article img').forEach((img) => {
    const mark = () => img.classList.toggle('zoomable', !img.closest('a') && img.naturalWidth > img.clientWidth + 8);
    img.complete ? mark() : img.addEventListener('load', mark);
    img.addEventListener('click', () => {
      if (!img.classList.contains('zoomable')) return;
      const big = document.createElement('img');
      big.src = img.currentSrc || img.src;
      big.alt = img.alt;
      openLightbox(big);
    });
  });
  document.addEventListener('click', (e) => {
    const pre = e.target.closest('pre.mermaid.zoomable');
    if (!pre) return;
    const svg = pre.querySelector('svg').cloneNode(true);
    svg.removeAttribute('style');
    svg.style.width = svg.viewBox.baseVal.width + 'px';  // 原尺寸，放不下就在灯箱里滚动
    const box = document.createElement('div');
    box.className = 'lightbox-figure';
    box.appendChild(svg);
    openLightbox(box);
  });

  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeNav(); closeLightbox(); } });

  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { sync(); ticking = false; });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', () => { fitTables(); markZoomableDiagrams(); onScroll(); });

  renderMermaid();
  fitTables();
  sync();
  if (location.hash) {
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target) flash(target);
  }
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


_TABLE_RE = re.compile(r"<table>(.*?)</table>", re.DOTALL)
_ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
_CELL_RE = re.compile(r"<(td|th)([^>]*)>(.*?)</\1>", re.DOTALL)
_NUMERIC_RE = re.compile(r"^[\s\d.,%+\-–~×xX/:¥$€]*\d[\s\d.,%+\-–~×xX/:¥$€]*$")
NOWRAP_MAX_WIDTH = 7  # 全列最长不超过约 7 个汉字宽，就整列不折行
LONG_AVG_WIDTH = 16   # 列平均超过约 16 个汉字宽，算长文本列，给最小宽度防止被挤成窄条


def _cell_text(cell_html: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", cell_html)).strip()


def _text_width(text: str) -> float:
    """粗估显示宽度：CJK / 全角记 1，其余记 0.55。"""
    return sum(1 if ord(c) > 0x2E7F else 0.55 for c in text)


def _add_class(attrs: str, cls: str) -> str:
    if 'class="' in attrs:
        return attrs.replace('class="', f'class="{cls} ', 1)
    return f'{attrs} class="{cls}"'


def _tune_tables(html_body: str) -> str:
    """短列整列不折行，数字列右对齐。按列统计，只加 class，不动单元格内容。"""
    def one(m: re.Match) -> str:
        rows = [_CELL_RE.findall(r) for r in _ROW_RE.findall(m.group(1))]
        ncol = max((len(r) for r in rows), default=0)
        if ncol < 2:
            return m.group(0)
        widths = [0.0] * ncol
        totals = [[0.0, 0] for _ in range(ncol)]  # [td 宽度合计, 非空 td 数]
        numeric = [[0, 0] for _ in range(ncol)]  # [数字单元格数, 非空 td 数]
        for r in rows:
            for i, (tag, _, content) in enumerate(r):
                text = _cell_text(content)
                widths[i] = max(widths[i], _text_width(text))
                if tag == "td" and text:
                    totals[i][0] += _text_width(text)
                    totals[i][1] += 1
                    numeric[i][1] += 1
                    numeric[i][0] += bool(_NUMERIC_RE.match(text))
        col_cls = {}
        for i in range(ncol):
            classes = []
            if widths[i] <= NOWRAP_MAX_WIDTH:
                classes.append("nw")
            hits, total = numeric[i]
            if total and hits / total >= 0.8:
                classes.append("num")
            elif totals[i][1] and totals[i][0] / totals[i][1] >= LONG_AVG_WIDTH:
                classes.append("long")
            if classes:
                col_cls[i] = " ".join(classes)
        if not col_cls:
            return m.group(0)

        def row_sub(rm: re.Match) -> str:
            col = 0

            def cell_sub(cm: re.Match) -> str:
                nonlocal col
                tag, attrs, content = cm.groups()
                cls = col_cls.get(col, "")
                if tag == "th":
                    cls = cls.replace("long", "").strip()
                if cls:
                    attrs = _add_class(attrs, cls)
                col += 1
                return f"<{tag}{attrs}>{content}</{tag}>"

            return "<tr>" + _CELL_RE.sub(cell_sub, rm.group(1)) + "</tr>"

        return "<table>" + _ROW_RE.sub(row_sub, m.group(1)) + "</table>"

    return _TABLE_RE.sub(one, html_body)


_WIKILINK_RE = re.compile(r"\[\[([^\[\]|<>]+?)(?:\|([^\[\]<>]+?))?\]\]")
_CODE_SEGMENT_RE = re.compile(r"(<pre\b.*?</pre>|<code\b.*?</code>)", re.DOTALL)


def _render_wikilinks(html_body: str) -> str:
    """[[目标|别名]] → 别名（无别名时取目标名，去掉 #小节），代码块内不动。"""
    def one(m: re.Match) -> str:
        target, alias = m.group(1).strip(), m.group(2)
        text = alias.strip() if alias else target.split("#")[0].strip() or target
        return f'<span class="wikilink" title="{target.replace(chr(34), "&quot;")}">{text}</span>'
    parts = _CODE_SEGMENT_RE.split(html_body)
    return "".join(p if i % 2 else _WIKILINK_RE.sub(one, p) for i, p in enumerate(parts))


def _wrap_tables(html_body: str) -> str:
    html_body = re.sub(r"<table>", '<div class="table-frame"><div class="table-wrap"><table>', html_body)
    html_body = re.sub(r"</table>", "</table></div></div>", html_body)
    return html_body


def _decorate_heading_numbers(html_body: str) -> str:
    """把 "3. 功能需求" / "3.2 弹窗" 的编号包进 .h-num，纯文本不变（侧栏抽取不受影响）。"""
    def repl(m: re.Match) -> str:
        tag, attrs, inner = m.groups()
        inner = re.sub(
            r"^(\s*)(\d+\.(?:\d+\.?)*)(\s+)",
            lambda n: f'{n.group(1)}<span class="h-num">{n.group(2)}</span>{n.group(3)}',
            inner,
            count=1,
        )
        return f"<{tag}{attrs}>{inner}</{tag}>"
    return re.sub(r"<(h[1234])([^>]*)>(.*?)</\1>", repl, html_body, flags=re.DOTALL)


def _add_heading_anchors(html_body: str) -> str:
    """Add hover-anchor links to h2/h3/h4"""
    def repl(m: re.Match) -> str:
        tag, attrs, content = m.group(1), m.group(2), m.group(3)
        id_match = re.search(r'id="([^"]+)"', attrs)
        if not id_match:
            return m.group(0)
        hid = id_match.group(1)
        return f'<{tag}{attrs}><a class="anchor" href="#{hid}" aria-hidden="true" tabindex="-1">#</a>{content}</{tag}>'
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
    html_body = _render_wikilinks(html_body)
    html_body = _tune_tables(html_body)
    html_body = _wrap_tables(html_body)
    html_body = _decorate_callouts(html_body)
    html_body = _decorate_heading_numbers(html_body)
    html_body = _add_heading_anchors(html_body)
    return html_body


def render_yaml_card_inline(data: dict) -> str:
    """Inline YAML block (within content) -> styled card, not collapsible"""
    parts = [
        '<div class="frontmatter" style="margin: 20px 0;">',
        '<div class="fm-body" style="border: none;">',
        '<div style="font-family: var(--font-mono); font-size: 12px; letter-spacing: 0.06em; color: var(--ink-3); text-transform: uppercase; margin-top: 12px;">YAML</div>',
        '<dl>',
    ]
    for k, v in data.items():
        parts.append(f'<dt>{html.escape(str(k))}</dt>')
        parts.append(f'<dd>{_render_value(v)}</dd>')
    parts.append('</dl></div></div>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# 自动抽 H2 章节导航 / 右栏小节
# ---------------------------------------------------------------------------

H2_HTML_RE = re.compile(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', re.DOTALL)
HEADING_HTML_RE = re.compile(r'<(h[234])[^>]*\bid="([^"]+)"[^>]*>(.*?)</\1>', re.DOTALL)
_ANCHOR_TAG_RE = re.compile(r'<a class="anchor".*?</a>', re.DOTALL)


def _heading_text(content: str) -> str:
    content = _ANCHOR_TAG_RE.sub("", content)
    return html.unescape(re.sub(r"<[^>]+>", "", content)).strip().rstrip("#").strip()


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
        title = _heading_text(m.group(2))
        num, label = _split_num(title)
        sections.append({"title": label, "anchor": m.group(1), "num": num, "raw_title": title})
    return sections


def build_mini_toc(html_body: str, empty_label: str = "（本文档无 H3 小节）") -> str:
    """右栏：H3 / H4 按所属 H2 打上 data-section，前端只显示当前章节那一组。"""
    items = []
    section = ""
    for m in HEADING_HTML_RE.finditer(html_body):
        tag, hid, content = m.groups()
        if tag == "h2":
            section = hid
            continue
        items.append((tag, hid, _heading_text(content), section))

    if not items:
        return f'<ul class="mini-toc"><li><span class="empty-hint">{html.escape(empty_label)}</span></li></ul>'

    out = ['<ul class="mini-toc" id="mini-toc">']
    for tag, hid, text, sec in items:
        cls = "lvl4" if tag == "h4" else "lvl3"
        out.append(
            f'<li><a href="#{html.escape(hid)}" class="{cls}" data-section="{html.escape(sec)}">{html.escape(text)}</a></li>'
        )
    out.append('</ul>')
    return "".join(out)


def _reading_minutes(html_body: str) -> int:
    text = re.sub(r'<pre class="mermaid">.*?</pre>', "", html_body, flags=re.DOTALL)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    cjk = len(re.findall(r"[一-鿿]", text))
    words = len(re.findall(r"[A-Za-z0-9]+", text))
    return max(1, math.ceil(cjk / 400 + words / 220))


def slugify_github(value: str, separator: str) -> str:
    """GitHub / Obsidian 同款锚点：小写、去标点、每个空格换一个连字符（不合并）。

    PRD 里手写的目录链接（如 #4-游戏机制规格--double-bet--50-cash-out）按这个规则写，
    用同一规则生成 id 才能对上；中文保留。
    """
    return re.sub(r"[^\w\- ]", "", value.strip().lower()).replace(" ", separator)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

_ANY_FENCE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
_FIRST_H2_RE = re.compile(r"^## ", re.MULTILINE)


def strip_leading_meta_yaml(text: str) -> str:
    """去掉首个 H2 之前的 ```yaml 块——它们是给 prd-score / prd-split 用的工具链元数据，
    读者不需要看。首个 H2 之后的 yaml 视为正文内容，原样保留。"""
    # 把代码块整段替换成等长空白再找 H2，避免代码块里的 "## " 被误判
    masked = _ANY_FENCE_RE.sub(lambda m: " " * len(m.group(0)), text)
    h2 = _FIRST_H2_RE.search(masked)
    cut = h2.start() if h2 else len(text)
    head = re.sub(r"\n{3,}", "\n\n", INLINE_YAML_RE.sub("", text[:cut]))
    return head + text[cut:]


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
        "no_subsections": "本节没有小节",
        "project_docs": "项目文档",
        "toc": "目录",
        "theme": "切换深浅色",
        "theme_hint": "深浅色",
        "to_top": "回到顶部",
        "copied": "已复制本节链接",
        "stats": "{n} 节 · 约 {m} 分钟读完",
    },
    "en": {
        "html_lang": "en",
        "this_doc": "Contents",
        "on_this_page": "On this page",
        "no_subsections": "No subsections",
        "project_docs": "Documents",
        "toc": "Contents",
        "theme": "Toggle dark mode",
        "theme_hint": "Theme",
        "to_top": "Back to top",
        "copied": "Link copied",
        "stats": "{n} sections · {m} min read",
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
    show_meta: bool = False,
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
        Override meta line under title (default: auto from frontmatter + 章节数 / 阅读时长)
    footer_left, footer_right : str
        Footer text
    show_meta : bool
        展示 frontmatter 卡片与首个 H2 之前的 yaml 元数据块（默认隐藏）

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
    if not show_meta:
        body_md = strip_leading_meta_yaml(body_md)

    body_md, mermaid_blocks, yaml_blocks = preprocess_markdown(body_md)

    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={
            "toc": {
                "anchorlink": False,
                "permalink": False,
                "toc_depth": "2-4",
                "slugify": slugify_github,
            },
        },
        output_format="html5",
    )
    # Obsidian 里常写 \~ 防删除线，python-markdown 默认不认这个转义
    md.ESCAPED_CHARS.append("~")
    html_body = md.convert(body_md)
    html_body = postprocess_html(html_body, mermaid_blocks, yaml_blocks)

    # 侧栏章节从渲染后 HTML 的真实 <h2 id> 抽取，锚点与正文永不漂移
    h2_sections = extract_h2_sections(html_body)

    # ---- doc title：首个 H1 移到页头，正文里不再重复 ----
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body, re.DOTALL)
    if custom_title is None:
        custom_title = _heading_text(h1_match.group(1)) if h1_match else md_path.stem
    if h1_match:
        html_body = html_body[: h1_match.start()] + html_body[h1_match.end():]

    # ---- meta line under title ----
    if custom_meta_html is None:
        meta_parts = []
        for k in ("date", "owner", "version", "status"):
            if frontmatter and frontmatter.get(k):
                meta_parts.append(f"<span>{html.escape(str(frontmatter[k]))}</span>")
        stats = labels["stats"].format(n=len(h2_sections), m=_reading_minutes(html_body))
        meta_parts.append(f"<span>{html.escape(stats)}</span>")
        custom_meta_html = '<span class="sep"></span>'.join(meta_parts)

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
            active = ' class="active" aria-current="page"' if item.get("active") else ""
            href = html.escape(item.get("href", "#"))
            title = html.escape(item.get("title", ""))
            cross_doc_html += f'<a href="{href}"{active}>{title}</a>'
        cross_doc_html += '</nav></div>'

    section_nav_html = (
        f'<div class="nav-eyebrow">{html.escape(labels["this_doc"])}</div>'
        f'<nav class="section-nav" id="section-nav" aria-label="{html.escape(labels["this_doc"])}">'
    )
    for s in h2_sections:
        num_span = f'<span class="num">{html.escape(s["num"])}</span>'
        anchor = html.escape(s["anchor"])
        section_nav_html += (
            f'<a href="#{anchor}" data-section="{anchor}">'
            f'{num_span}<span class="label">{html.escape(s["title"])}</span></a>'
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

    short_title = (brand or {}).get("product") or custom_title

    # ---- right rail mini-TOC: collect H3/H4 from rendered HTML ----
    mini_toc_html = build_mini_toc(html_body, labels["no_subsections"])

    # ---- frontmatter card ----
    fm_html = render_frontmatter_card(frontmatter) if frontmatter and show_meta else ""

    footer_html = ""
    if footer_left or footer_right:
        footer_html = (
            '<footer class="doc-footer">'
            f'<span>{html.escape(footer_left)}</span><span>{html.escape(footer_right)}</span>'
            '</footer>'
        )

    theme_label = html.escape(labels["theme"])
    theme_btn = f'<button class="icon-btn theme-toggle" type="button" aria-label="{theme_label}" title="{theme_label}">{ICON_MOON}{ICON_SUN}</button>'

    # ---- assemble ----
    full = f"""<!DOCTYPE html>
<html lang="{labels["html_lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{html.escape(custom_title)}</title>
{HEAD_THEME_JS}
{HEAD_FONTS}
<style>{CSS}</style>
</head>
<body data-copied="{html.escape(labels["copied"])}">
<div class="progress" aria-hidden="true"><span></span></div>
<header class="mobile-bar">
  <button class="icon-btn mobile-nav-toggle" type="button" aria-expanded="false" aria-controls="sidebar">{ICON_MENU}<span>{html.escape(labels["toc"])}</span></button>
  <span class="mobile-title">{html.escape(short_title)}</span>
  {theme_btn}
</header>
<div class="layout">
  <aside class="sidebar-left" id="sidebar">
    <div class="sidebar-scroll">
      {brand_html}
      {cross_doc_html}
      {section_nav_html}
    </div>
    <div class="sidebar-foot"><span>{html.escape(labels["theme_hint"])}</span>{theme_btn}</div>
  </aside>
  <main class="content">
    <div class="content-inner">
      <header class="doc-header">
        {badge_html}
        <h1 class="doc-title">{html.escape(custom_title)}</h1>
        <div class="doc-meta">{custom_meta_html or ''}</div>
      </header>
      {fm_html}
      <article>
{html_body}
      </article>
      {footer_html}
    </div>
  </main>
  <aside class="sidebar-right" aria-label="{html.escape(labels["on_this_page"])}">
    <div class="rail-eyebrow">{html.escape(labels["on_this_page"])}</div>
    <div class="rail-section" id="rail-section"></div>
    {mini_toc_html}
  </aside>
</div>
<div class="scrim" aria-hidden="true"></div>
<button class="icon-btn to-top" type="button" aria-label="{html.escape(labels["to_top"])}" title="{html.escape(labels["to_top"])}">{ICON_UP}</button>
<div class="toast" role="status" aria-live="polite"></div>
{MERMAID_SNIPPET if mermaid_blocks else ''}
{PAGE_JS}
</body>
</html>
"""
    html_path.write_text(full, encoding="utf-8")
    return {
        "mermaid": len(mermaid_blocks),
        "yaml_blocks": len(yaml_blocks),
        "h2_sections": len(h2_sections),
    }
