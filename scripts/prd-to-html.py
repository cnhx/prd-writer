#!/usr/bin/env python3
"""
prd-to-html — 把 PRD Markdown 渲染成自包含的主题化 HTML。

调用同目录的 prd_html_theme.build_html（refined editorial 三栏 Docs 风：
左侧章节栏 + 中央正文 + 右侧 mini-TOC，frontmatter 折叠卡片、表格 sticky
表头、callout、Mermaid CDN 渲染、响应式、打印优化）。

brand / badges 默认从文档自动推导，不硬编码任何品牌：
  - product = 第一个 H1（去掉「— 产品需求文档 / — PRD」后缀）
  - badges  = frontmatter / 首个 ```yaml 块里的 product_type、output_profile、status
  - crest   = 默认留空，仅 --crest 显式提供时才渲染

用法：
    python3 prd-to-html.py --md PRD.md
    python3 prd-to-html.py --md PRD.md --out PRD.html --crest "Acme" --ver "v1.2"
    python3 prd-to-html.py --md PRD.md --badge "P0" --badge "draft"
    # 多文档项目跨文档导航（JSON）：
    python3 prd-to-html.py --md PRD.md \
        --cross-doc '[{"title":"GDD","href":"PRD-gdd.html"},{"title":"TDD","href":"PRD-tdd.html"}]'
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from prd_html_theme import build_html
except ModuleNotFoundError as exc:  # markdown / yaml 缺失
    missing = getattr(exc, "name", str(exc))
    sys.stderr.write(
        f"[prd-to-html] 缺少 Python 依赖：{missing}\n"
        f"  安装：python3 -m pip install markdown pyyaml\n"
    )
    sys.exit(3)


H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
YAML_FENCE_RE = re.compile(r"```ya?ml\n(.*?)```", re.DOTALL)
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
TITLE_SUFFIX_RE = re.compile(r"\s*[—\-–]\s*(产品需求文档|PRD|需求文档)\s*$")
KNOWN_META_KEYS = {"product_type", "secondary_product_type", "output_profile", "status"}


def _first_h1(md_text: str) -> str | None:
    # 先抹掉 fenced 代码块，避免代码块内的 "# 注释" 被误当成 H1
    m = H1_RE.search(FENCE_RE.sub("", md_text))
    return m.group(1).strip() if m else None


def _scan_meta(md_text: str) -> dict:
    """从 leading frontmatter 或文档元数据 yaml 块抓 product_type 等字段。

    leading ``---`` frontmatter 直接信任；正文里的 ```yaml fence 仅当解析出的
    键集与已知元数据键有交集时才采纳——避免把正文中的示例 yaml 误当元数据。
    """
    import yaml

    meta: dict = {}

    def _merge(chunk: str, require_known: bool) -> None:
        try:
            data = yaml.safe_load(chunk)
        except yaml.YAMLError:
            return
        if not isinstance(data, dict):
            return
        if require_known and not (KNOWN_META_KEYS & set(data.keys())):
            return
        for k, v in data.items():
            meta.setdefault(k, v)

    fm = FRONTMATTER_RE.match(md_text)
    if fm:
        _merge(fm.group(1), require_known=False)
    # 扫描所有 yaml fence，只采纳含已知元数据键的块（跳过正文示例 yaml）
    for fence in YAML_FENCE_RE.finditer(md_text):
        _merge(fence.group(1), require_known=True)
    return meta


def _auto_badges(meta: dict) -> list[dict]:
    badges: list[dict] = []
    pt = meta.get("product_type")
    if pt and pt != "null":
        badges.append({"text": str(pt), "accent": True, "dot": True})
    spt = meta.get("secondary_product_type")
    if spt and spt != "null":
        badges.append({"text": str(spt)})
    status = meta.get("status")
    if status:
        badges.append({"text": str(status)})
    op = meta.get("output_profile")
    if op and op != "null":
        badges.append({"text": str(op)})
    return badges


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a PRD markdown file to themed HTML.")
    ap.add_argument("--md", required=True, type=Path, help="source markdown file")
    ap.add_argument("--out", type=Path, help="output html (default: <md>.html)")
    ap.add_argument("--crest", default="", help="top-left eyebrow label (default: none)")
    ap.add_argument("--product", default=None, help="brand product line (default: first H1)")
    ap.add_argument("--ver", default=None, help="version label in brand block")
    ap.add_argument("--badge", action="append", default=[], help="extra badge text (repeatable)")
    ap.add_argument("--title", default=None, help="override document title (default: first H1)")
    ap.add_argument("--footer-left", default="", help="footer left text")
    ap.add_argument("--footer-right", default="", help="footer right text")
    ap.add_argument("--cross-doc", default=None, help="JSON list of {title, href, active} for multi-doc nav")
    ap.add_argument("--cross-doc-title", default=None, help="label for cross-doc nav block (default: by --lang)")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"], help="UI chrome language (default: zh)")
    args = ap.parse_args()

    src: Path = args.md
    if not src.exists():
        sys.stderr.write(f"[prd-to-html] 源文件不存在：{src}\n")
        sys.exit(2)

    dst: Path = args.out or src.with_suffix(".html")
    md_text = src.read_text(encoding="utf-8-sig")  # 剥离 BOM，与 build_html 一致

    meta = _scan_meta(md_text)
    product = args.product
    if product is None:
        h1 = _first_h1(md_text)
        product = TITLE_SUFFIX_RE.sub("", h1) if h1 else ""

    brand = None
    if args.crest or product or args.ver:
        brand = {"crest": args.crest, "product": product or "", "ver": args.ver or ""}

    badges = _auto_badges(meta)
    badges += [{"text": b} for b in args.badge]

    cross_doc_nav = None
    if args.cross_doc:
        try:
            cross_doc_nav = json.loads(args.cross_doc)
        except json.JSONDecodeError as exc:
            sys.stderr.write(f"[prd-to-html] --cross-doc 不是合法 JSON：{exc}\n")
            sys.exit(2)
        if not (isinstance(cross_doc_nav, list) and all(isinstance(x, dict) for x in cross_doc_nav)):
            sys.stderr.write("[prd-to-html] --cross-doc 必须是对象数组 [{title, href, active}]\n")
            sys.exit(2)

    stats = build_html(
        md_path=src,
        html_path=dst,
        brand=brand,
        badges=badges or None,
        cross_doc_nav=cross_doc_nav,
        cross_doc_title=args.cross_doc_title,
        custom_title=args.title,
        footer_left=args.footer_left,
        footer_right=args.footer_right,
        lang=args.lang,
    )

    size = dst.stat().st_size
    print(f"[prd-to-html] {dst}  {size:,} bytes")
    print(
        f"  H2 章节 {stats['h2_sections']} · Mermaid {stats['mermaid']} · YAML 块 {stats['yaml_blocks']}"
    )


if __name__ == "__main__":
    main()
