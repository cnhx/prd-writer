#!/usr/bin/env node
/**
 * prd-html-qa — 渲染后的 PRD HTML 视觉自检：截图 + 可量化检查。
 *
 * 零依赖：Node 22+（内置 WebSocket）+ 本机 Chrome / Chromium / Edge，走 CDP。
 *
 * 每个视口（桌面 1440、平板 1024、手机 390，外加桌面深色）都会：
 *   - 跑硬性检查：横向溢出、标题可见、锚点断链、图片加载、Mermaid 渲染、重复 id、控制台报错
 *   - 跑软性检查：正文对比度、每行字数、过小字号、需要横向滚动的表格
 *   - 按文档高度均匀截若干屏，另给每个问题元素单独截一张
 *
 * 用法：
 *   node prd-html-qa.mjs PRD.html
 *   node prd-html-qa.mjs PRD.html --out /tmp/qa --frames 6
 *
 * 退出码：0 无硬性问题；1 有硬性问题；2 参数或浏览器启动失败。
 * 产物：<out>/report.json + <out>/*.png，默认 out = $TMPDIR/prd-html-qa/<文件名>/
 */

import { spawn } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, extname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const VIEWPORTS = [
  { name: "desktop", width: 1440, height: 900, scheme: "light", frames: null },
  { name: "desktop-dark", width: 1440, height: 900, scheme: "dark", frames: 3 },
  { name: "tablet", width: 1024, height: 768, scheme: "light", frames: 2 },
  { name: "mobile", width: 390, height: 844, scheme: "light", frames: 4 },
];

function parseArgs(argv) {
  const args = { file: null, out: null, frames: 6, chrome: process.env.CHROME_PATH || null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--out") args.out = argv[++i];
    else if (a === "--frames") args.frames = Number(argv[++i]);
    else if (a === "--chrome") args.chrome = argv[++i];
    else if (!args.file) args.file = a;
  }
  return args;
}

function findChrome(explicit) {
  const candidates = [
    explicit,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/microsoft-edge",
  ].filter(Boolean);
  return candidates.find((p) => existsSync(p)) || null;
}

function launch(chromePath) {
  const profile = mkdtempSync(join(tmpdir(), "prd-qa-profile-"));
  const proc = spawn(
    chromePath,
    [
      "--headless=new",
      "--remote-debugging-port=0",
      `--user-data-dir=${profile}`,
      "--no-first-run",
      "--no-default-browser-check",
      "--hide-scrollbars",
      "--allow-file-access-from-files",
      "about:blank",
    ],
    { stdio: ["ignore", "ignore", "pipe"] },
  );
  return new Promise((ok, fail) => {
    let buf = "";
    const timer = setTimeout(() => fail(new Error("Chrome 启动超时")), 20000);
    proc.stderr.on("data", (d) => {
      buf += d.toString();
      const m = buf.match(/DevTools listening on (ws:\/\/\S+)/);
      if (m) {
        clearTimeout(timer);
        ok({ proc, wsUrl: m[1], profile });
      }
    });
    proc.on("exit", (code) => fail(new Error(`Chrome 提前退出（${code}）`)));
  });
}

function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let seq = 0;
  const pending = new Map();
  const listeners = new Set();
  ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    if (msg.id && pending.has(msg.id)) {
      const { ok, fail } = pending.get(msg.id);
      pending.delete(msg.id);
      msg.error ? fail(new Error(msg.error.message)) : ok(msg.result);
    } else {
      listeners.forEach((fn) => fn(msg));
    }
  };
  const send = (method, params = {}, sessionId) =>
    new Promise((ok, fail) => {
      const id = ++seq;
      pending.set(id, { ok, fail });
      ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  const once = (method, sessionId, timeout = 15000) =>
    new Promise((ok) => {
      const timer = setTimeout(() => {
        listeners.delete(fn);
        ok(null);
      }, timeout);
      const fn = (msg) => {
        if (msg.method === method && msg.sessionId === sessionId) {
          clearTimeout(timer);
          listeners.delete(fn);
          ok(msg.params);
        }
      };
      listeners.add(fn);
    });
  return new Promise((ok, fail) => {
    ws.onopen = () => ok({ ws, send, once, listeners });
    ws.onerror = () => fail(new Error("CDP 连接失败"));
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// 页面内检查，返回可序列化结果
const PAGE_CHECKS = String.raw`(() => {
  const vw = window.innerWidth;
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none" && cs.opacity !== "0";
  };
  const rgb = (c) => {
    const m = c && c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const lum = ({ r, g, b }) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const bgOf = (el) => {
    for (let n = el; n; n = n.parentElement) {
      const c = rgb(getComputedStyle(n).backgroundColor);
      if (c && c.a >= 0.5) return c;
    }
    return { r: 255, g: 255, b: 255, a: 1 };
  };
  const ratio = (el) => {
    const fg = rgb(getComputedStyle(el).color), bg = bgOf(el);
    if (!fg) return null;
    const [a, b] = [lum(fg), lum(bg)].sort((x, y) => y - x);
    return Math.round(((a + 0.05) / (b + 0.05)) * 100) / 100;
  };
  const path = (el) => {
    const parts = [];
    for (let n = el; n && n.nodeType === 1 && parts.length < 4; n = n.parentElement) {
      parts.unshift(n.tagName.toLowerCase() + (n.id ? "#" + n.id : n.className && typeof n.className === "string" ? "." + n.className.trim().split(/\s+/)[0] : ""));
    }
    return parts.join(" > ");
  };

  const hard = [], soft = [], spots = [];

  const overflow = document.documentElement.scrollWidth - vw;
  if (overflow > 1) {
    const culprits = [...document.querySelectorAll("body *")]
      .filter((el) => visible(el) && el.getBoundingClientRect().right > vw + 1 && !el.closest(".table-wrap, pre"))
      .slice(0, 5).map(path);
    hard.push({ check: "page-overflow-x", detail: "页面横向溢出 " + overflow + "px", culprits });
  }

  const title = document.querySelector(".doc-title");
  if (!title || !visible(title)) hard.push({ check: "title-hidden", detail: "文档标题不可见" });

  const ids = new Map();
  document.querySelectorAll("[id]").forEach((el) => ids.set(el.id, (ids.get(el.id) || 0) + 1));
  const dupes = [...ids].filter(([, n]) => n > 1).map(([id]) => id);
  if (dupes.length) hard.push({ check: "duplicate-id", detail: dupes.slice(0, 10).join(", ") });

  const broken = [...document.querySelectorAll('a[href^="#"]')]
    .map((a) => decodeURIComponent(a.getAttribute("href").slice(1)))
    .filter((id) => id && !document.getElementById(id));
  if (broken.length) hard.push({ check: "broken-anchor", detail: [...new Set(broken)].slice(0, 10).join(", ") });

  const badImgs = [...document.querySelectorAll("article img")].filter((img) => img.complete && img.naturalWidth === 0);
  badImgs.forEach((img, i) => { if (i < 3) spots.push({ why: "broken-image", el: img }); });
  if (badImgs.length) hard.push({ check: "broken-image", detail: badImgs.slice(0, 5).map((i) => i.getAttribute("src")).join(", ") });

  const mermaids = [...document.querySelectorAll("pre.mermaid")];
  if (mermaids.length && !window.mermaid) {
    soft.push({ check: "mermaid-offline", detail: "Mermaid 脚本未加载（离线？），" + mermaids.length + " 张图未绘制" });
  } else {
    const failed = mermaids.filter((m) => !m.querySelector("svg") || /Syntax error|Parse error/i.test(m.textContent));
    failed.forEach((m, i) => { if (i < 3) spots.push({ why: "mermaid-error", el: m }); });
    if (failed.length) hard.push({ check: "mermaid-error", detail: failed.length + " / " + mermaids.length + " 张 Mermaid 图渲染失败" });
    mermaids.forEach((m) => {
      const svg = m.querySelector("svg");
      const natural = svg && svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal.width : 0;
      if (natural && svg.getBoundingClientRect().width / natural < 0.7) {
        soft.push({ check: "mermaid-small", detail: "Mermaid 图缩到原尺寸的 " + Math.round((svg.getBoundingClientRect().width / natural) * 100) + "%，文字偏小（可点击放大；考虑改成 TD 方向或拆图）" });
        spots.push({ why: "mermaid-small", el: m });
      }
      if (svg && svg.getBoundingClientRect().width > m.getBoundingClientRect().width + 2) {
        soft.push({ check: "mermaid-overflow", detail: "Mermaid 图宽于容器" });
        spots.push({ why: "mermaid-overflow", el: m });
      }
    });
  }

  const wideTables = [...document.querySelectorAll(".table-wrap")].filter((w) => visible(w) && w.scrollWidth > w.clientWidth + 1);
  wideTables.forEach((w, i) => { if (i < 2) spots.push({ why: "wide-table", el: w }); });
  if (wideTables.length) {
    soft.push({
      check: "table-scroll",
      detail: wideTables.length + " 张表需要横向滚动（列数 " + wideTables.map((w) => w.querySelectorAll("thead th").length).join("/") + "）",
    });
  }

  const contrast = {};
  const groups = { body: "article p, article li, article td", nav: ".section-nav a, .mini-toc a, .doc-meta", callout: "blockquote p" };
  for (const [name, sel] of Object.entries(groups)) {
    const vals = [...document.querySelectorAll(sel)].filter(visible).slice(0, 60).map(ratio).filter((v) => v);
    if (!vals.length) continue;
    const min = Math.min(...vals);
    contrast[name] = min;
    if (min < 4.5) (name === "body" ? hard : soft).push({ check: "contrast-" + name, detail: name + " 最低对比度 " + min + "（要求 ≥ 4.5）" });
  }

  const paras = [...document.querySelectorAll("article > p")].filter(visible).slice(0, 30);
  let cpl = null;
  if (paras.length) {
    cpl = Math.round(paras.reduce((s, p) => s + p.clientWidth / parseFloat(getComputedStyle(p).fontSize), 0) / paras.length);
    const cjk = /[一-鿿]/.test(paras.map((p) => p.textContent).join("").slice(0, 400));
    // 中文 1 字 ≈ 1em；拉丁字母平均 ≈ 0.5em，45–80 字符 ≈ 22–40em
    const [lo, hi] = cjk ? [16, 46] : [22, 40];
    const unit = cjk ? " 字" : " em（约 " + cpl * 2 + " 字符）";
    if (vw >= 768 && (cpl < lo || cpl > hi)) soft.push({ check: "measure", detail: "正文每行约 " + cpl + unit + "（建议 " + lo + "–" + hi + (cjk ? " 字" : " em") + "）" });
  }

  const tiny = [...document.querySelectorAll("article *, nav *, aside *")]
    .filter((el) => el.childNodes.length && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && visible(el) && parseFloat(getComputedStyle(el).fontSize) < 12);
  if (tiny.length) soft.push({ check: "tiny-text", detail: tiny.length + " 处文字小于 12px，例：" + path(tiny[0]) });

  const nav = !!document.querySelector(".section-nav, .mobile-nav") && [...document.querySelectorAll(".section-nav, .mobile-nav-toggle")].some(visible);
  if (!nav) hard.push({ check: "no-navigation", detail: "当前视口没有可见的章节导航入口" });

  window.__qaSpots = spots.map((s) => s.el);
  return {
    viewport: vw,
    docHeight: document.documentElement.scrollHeight,
    hard, soft,
    spots: spots.map((s) => s.why),
    metrics: { contrast, charsPerLine: cpl, h2: document.querySelectorAll("article h2").length, tables: document.querySelectorAll("article table").length, mermaid: mermaids.length },
  };
})()`;

const DRAWER_OPEN = String.raw`(async () => {
  const b = document.querySelector(".mobile-nav-toggle");
  if (!b || getComputedStyle(b).display === "none") return null;
  window.scrollTo(0, 0);
  b.click();
  await new Promise((r) => setTimeout(r, 450));
  const rect = document.querySelector(".sidebar-left").getBoundingClientRect();
  return { left: Math.round(rect.left), open: document.body.classList.contains("nav-open") };
})()`;

const NAV_JUMP = String.raw`(async () => {
  const links = [...document.querySelectorAll("#section-nav a")];
  const a = links[Math.min(2, links.length - 1)];
  if (!a) return null;
  document.documentElement.style.scrollBehavior = "auto";
  if (!document.body.classList.contains("nav-open")) window.scrollTo(0, 0);
  a.click();
  await new Promise((r) => setTimeout(r, 2000));
  const t = document.getElementById(a.dataset.section);
  return {
    closed: !document.body.classList.contains("nav-open"),
    hashOk: decodeURIComponent(location.hash.slice(1)) === a.dataset.section,
    active: a.classList.contains("active"),
    top: t ? Math.round(t.getBoundingClientRect().top) : null,
  };
})()`;

const THEME_TOGGLE = String.raw`(async () => {
  const b = [...document.querySelectorAll(".theme-toggle")].find((el) => el.offsetParent);
  if (!b) return null;
  const before = getComputedStyle(document.body).backgroundColor;
  b.click();
  await new Promise((r) => setTimeout(r, 1800));
  const after = getComputedStyle(document.body).backgroundColor;
  const blocks = document.querySelectorAll("pre.mermaid").length;
  const svgs = document.querySelectorAll("pre.mermaid svg").length;
  b.click();
  await new Promise((r) => setTimeout(r, 300));
  try { localStorage.removeItem("prd-theme"); } catch (e) {}
  delete document.documentElement.dataset.theme;
  return { changed: before !== after, blocks, svgs, mermaidOk: !window.mermaid || svgs === blocks };
})()`;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.file) {
    console.error("用法：node prd-html-qa.mjs <file.html> [--out dir] [--frames N] [--chrome path]");
    process.exit(2);
  }
  const file = resolve(args.file);
  if (!existsSync(file)) {
    console.error(`[prd-html-qa] 文件不存在：${file}`);
    process.exit(2);
  }
  const chrome = findChrome(args.chrome);
  if (!chrome) {
    console.error("[prd-html-qa] 找不到 Chrome / Chromium / Edge，可用 --chrome 或 CHROME_PATH 指定");
    process.exit(2);
  }
  const out = resolve(args.out || join(tmpdir(), "prd-html-qa", basename(file, extname(file))));
  mkdirSync(out, { recursive: true });

  const { proc, wsUrl, profile } = await launch(chrome);
  const cdp = await connect(wsUrl);
  const report = { file, out, generatedAt: new Date().toISOString(), viewports: [] };

  try {
    for (const vp of VIEWPORTS) {
      const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" });
      const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
      const s = (m, p) => cdp.send(m, p, sessionId);

      const consoleErrors = [];
      const onMsg = (msg) => {
        if (msg.sessionId !== sessionId) return;
        if (msg.method === "Runtime.exceptionThrown") consoleErrors.push(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
        if (msg.method === "Runtime.consoleAPICalled" && msg.params.type === "error") consoleErrors.push(msg.params.args.map((a) => a.value ?? a.description).join(" "));
      };
      cdp.listeners.add(onMsg);

      await s("Page.enable");
      await s("Runtime.enable");
      await s("Emulation.setDeviceMetricsOverride", { width: vp.width, height: vp.height, deviceScaleFactor: 1, mobile: vp.width < 768 });
      await s("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: vp.scheme }] });
      const loaded = cdp.once("Page.loadEventFired", sessionId);
      await s("Page.navigate", { url: pathToFileURL(file).href });
      await loaded;
      await s("Runtime.evaluate", { expression: "document.fonts.ready.then(() => 1)", awaitPromise: true });
      // 等 Mermaid 渲染完（最多 8 秒）
      for (let i = 0; i < 40; i++) {
        const { result } = await s("Runtime.evaluate", {
          expression: "!window.mermaid || !document.querySelector('pre.mermaid:not([data-processed])')",
        });
        if (result.value) break;
        await sleep(200);
      }
      await s("Runtime.evaluate", { expression: "document.documentElement.style.scrollBehavior = 'auto'" });

      const { result } = await s("Runtime.evaluate", { expression: PAGE_CHECKS, returnByValue: true });
      const r = result.value;
      if (consoleErrors.length) r.hard.push({ check: "console-error", detail: consoleErrors.slice(0, 5).join(" | ") });

      const shots = [];
      const capture = async (name) => {
        await sleep(180);
        const { data } = await s("Page.captureScreenshot", { format: "png" });
        const p = join(out, `${vp.name}-${name}.png`);
        writeFileSync(p, Buffer.from(data, "base64"));
        shots.push(p);
      };
      const frames = Math.max(1, Math.min(vp.frames ?? args.frames, Math.ceil(r.docHeight / vp.height)));
      for (let i = 0; i < frames; i++) {
        const y = frames === 1 ? 0 : Math.round(((r.docHeight - vp.height) * i) / (frames - 1));
        await s("Runtime.evaluate", { expression: `window.scrollTo(0, ${y})` });
        await capture(String(i + 1).padStart(2, "0"));
      }
      for (let i = 0; i < r.spots.length; i++) {
        await s("Runtime.evaluate", { expression: `window.__qaSpots[${i}].scrollIntoView({ block: "center" })` });
        await capture(`issue-${i + 1}-${r.spots[i]}`);
      }

      // 交互冒烟：只在浅色桌面和手机上跑，元素不存在就跳过
      const run = async (expr) => (await s("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result.value;
      if (vp.name === "mobile") {
        const d = await run(DRAWER_OPEN);
        if (d) {
          await capture("drawer");
          if (!d.open || d.left < -1) r.hard.push({ check: "drawer", detail: `目录抽屉没有滑出（left=${d.left}）` });
        }
      }
      if (vp.name === "mobile" || vp.name === "desktop") {
        const j = await run(NAV_JUMP);
        if (j && !(j.closed && j.hashOk && j.active && j.top !== null && j.top >= -2 && j.top <= 160)) {
          r.hard.push({ check: "nav-jump", detail: `点目录跳转异常：${JSON.stringify(j)}` });
        }
      }
      if (vp.name === "desktop") {
        const t = await run(THEME_TOGGLE);
        if (t && !t.changed) r.hard.push({ check: "theme-toggle", detail: "切换深浅色后背景没变" });
        if (t && !t.mermaidOk) r.hard.push({ check: "theme-mermaid", detail: `切换主题后 Mermaid 只剩 ${t.svgs}/${t.blocks} 张` });
      }

      cdp.listeners.delete(onMsg);
      await cdp.send("Target.closeTarget", { targetId });
      report.viewports.push({ ...vp, ...r, screenshots: shots });
    }
  } finally {
    cdp.ws.close();
    proc.kill();
    await sleep(300);
    rmSync(profile, { recursive: true, force: true });
  }

  writeFileSync(join(out, "report.json"), JSON.stringify(report, null, 2));

  let hardCount = 0;
  console.log(`[prd-html-qa] ${file}`);
  for (const v of report.viewports) {
    hardCount += v.hard.length;
    const status = v.hard.length ? "FAIL" : v.soft.length ? "WARN" : "PASS";
    console.log(`  ${v.name.padEnd(13)} ${status}  截图 ${v.screenshots.length} 张`);
    v.hard.forEach((h) => console.log(`    ✗ ${h.check}: ${h.detail}${h.culprits ? " ← " + h.culprits.join(" | ") : ""}`));
    v.soft.forEach((w) => console.log(`    △ ${w.check}: ${w.detail}`));
  }
  console.log(`  报告与截图：${out}`);
  process.exit(hardCount ? 1 : 0);
}

main().catch((err) => {
  console.error(`[prd-html-qa] ${err.message}`);
  process.exit(2);
});
