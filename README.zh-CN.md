# PRD Writer

[English](README.md) | **中文**

一套用于结构化撰写 PRD 的 skill，覆盖游戏、AI agent、SaaS/运营工具、数据产品、平台产品、增长产品、内容学习产品等品类。Markdown 是唯一的事实来源；通过导出 profile 支持 Obsidian MD、Word、PDF、HTML 等工作流。可选地把 PRD 导出成带 Mermaid 渲染的 HTML，也能生成可交互的 HTML 原型。

## 安装（Claude Code）

支持两种安装方式，任选其一。

### 方式 A —— 直接 clone 进 skills 目录

```sh
cd ~/.claude/skills
git clone <repo-url> prd-writer

# 子 skill symlink（绝对路径，和 setup 脚本保持一致）
ln -s ~/.claude/skills/prd-writer/write-prd       ~/.claude/skills/write-prd
ln -s ~/.claude/skills/prd-writer/prd-refine      ~/.claude/skills/prd-refine
ln -s ~/.claude/skills/prd-writer/grill-me        ~/.claude/skills/grill-me
ln -s ~/.claude/skills/prd-writer/opus-prd-polish ~/.claude/skills/opus-prd-polish
ln -s ~/.claude/skills/prd-writer/prd-score       ~/.claude/skills/prd-score
ln -s ~/.claude/skills/prd-writer/prd-split       ~/.claude/skills/prd-split
```

### 方式 B —— clone 到别处，再 symlink 进 skills 目录

```sh
git clone <repo-url> ~/path/to/prd-writer

ln -s ~/path/to/prd-writer                   ~/.claude/skills/prd-writer
ln -s ~/path/to/prd-writer/write-prd         ~/.claude/skills/write-prd
ln -s ~/path/to/prd-writer/prd-refine        ~/.claude/skills/prd-refine
ln -s ~/path/to/prd-writer/grill-me          ~/.claude/skills/grill-me
ln -s ~/path/to/prd-writer/opus-prd-polish   ~/.claude/skills/opus-prd-polish
ln -s ~/path/to/prd-writer/prd-score         ~/.claude/skills/prd-score
ln -s ~/path/to/prd-writer/prd-split         ~/.claude/skills/prd-split
```

### 校验

方式 A（仓库位于 `~/.claude/skills/prd-writer`）：

```sh
bash ~/.claude/skills/prd-writer/scripts/setup-dependencies.sh
```

方式 B 把路径换成你实际的 clone 位置：

```sh
bash ~/path/to/prd-writer/scripts/setup-dependencies.sh
```

脚本会为任何缺失项打印对应的 `ln -s` 命令，复制执行即可。

### 会话启动时自动更新

想让 Claude Code 和 Codex 在新会话开始时更新这个 skill，运行：

```sh
bash ~/.claude/skills/prd-writer/scripts/install-auto-update-hooks.sh
```

方式 B 把路径换成你实际的 clone 位置。这个 hook 执行 `scripts/update-skill.sh --auto`：拉取配置好的上游，只应用干净的 fast-forward 更新。如果仓库有本地改动、领先于上游、已分叉、没有上游、或拉取失败，它会跳过并说明原因。默认每 6 小时最多检查一次。

## 安装（Claude Cowork）

在 Claude Desktop → Cowork → Customize → Add plugin → From GitHub 里作为插件安装，所有命令会自动注册。细节见 `platforms/cowork/INSTALL.md`。

## 安装（其他平台）

- Claude Cowork：见 `platforms/cowork/INSTALL.md`
- Codex：见 `platforms/codex/INSTALL.md`
- OpenClaw：见 `platforms/openclaw/INSTALL.md`
- Hermes：见 `platforms/hermes/INSTALL.md`

## Skills

| Skill | 触发语 | 说明 |
|-------|---------|-------------|
| `/write-prd` | "write a PRD"、"create product requirements" | 完整 PRD 流程：产品类型路由、证据包、实现细节边界、异常路径覆盖、图表、导出 profile |
| `/prd-refine` | "refine this PRD"、"polish the PRD" | 快速打磨，保留细节 |
| `/opus-prd-polish` | "opus polish"、"final polish" | 顶配清晰度与结构打磨（用当前可用的最强推理模型） |
| `/grill-me` | "grill me"、"stress-test this" | 对方案或想法的连环追问 |
| `/prd-score` | "score this PRD"、"readiness check" | 给结构、责任人闭环、范围边界、实现细节泄漏、条件合并、异常覆盖、证据、图表、导出就绪度打分 |
| `/prd-split` | "split PRD"、"generate GDD"、"audience docs" | 把 PRD 拆成面向不同受众的文档。游戏项目用 GDD/TDD/美术/BD；非游戏项目用对应产品类型的文档包 |

## 支持的产品类型

| 类型 | 适用场景 | 额外输出文档包 |
|---|---|---|
| `game_interactive` | 老虎机、crash 游戏、社交游戏、互动体验 | GDD、TDD、美术与音频、BD 与市场 |
| `ai_agent` | 内部 agent，编码/设计/客服 agent，工作流自动化 | Agent 行为规格、评测计划、人工审核 Playbook、风险简报 |
| `b2b_saas_ops` | CRM、审批流、管理后台、内部工具 | 工作流规格、角色与权限矩阵、支持 Runbook、发布简报 |
| `data_analytics` | 看板、报表、实验、监控 | 指标字典、决策指南、数据质量清单 |
| `platform_marketplace` | API、插件市场、合作伙伴网络、B2B2C 平台 | 合作伙伴简报、API 契约摘要、信任与安全简报 |
| `consumer_growth` | 移动 App、社区、生命周期、裂变、会员 | 实验简报、生命周期触达简报、设计简报 |
| `content_learning` | 课程、知识库、AI 辅导、培训工具 | 学习成果图、内容评分卡、反馈闭环规格 |

## 用法

```
/write-prd [brief 文件或主题]
```

流程会：
1. **首次运行配置**：第一次调用时，让用户选择文档输出语言（存到 `~/.prd-writer/config.json`，只问一次）
2. **加载上下文**：从文件、同目录 PRD、记忆或用户输入加载上下文
3. **识别产品类型**：判定产品类型和输出 profile（`obsidian_md`、`word_docx`、`pdf`、`confluence` 或 `multi`）
4. **证据包**：当用户提供调研数据时，整理成证据表
5. **可选压力测试**：想法还模糊时，提供 `/grill-me` 或一段简短的 Concept Lab
6. **产品追问**：围绕市场、用户、范围、商业模式、风险，以及该产品类型的专属问题，一次只问一个
7. **起草 PRD**：把实现细节降级为产品契约，复杂条件合并进表格，覆盖异常路径，必要时内联 Mermaid 图
8. **评审**：用质量清单做追问式评审
9. **打磨发布**：可选地跑 `/opus-prd-polish` 和 `/prd-score`
10. **受众拆分**（可选）：自动调用 `/prd-split` 生成面向不同受众的文档（GDD、TDD、Agent 规格等）
11. **HTML PRD 导出**（可选）：生成可在浏览器直接打开的自包含 `.html`。如果做了受众拆分，每个拆分文档也各自生成 HTML，相互之间带跳转链接。包含 Mermaid 图渲染、样式化的元数据卡片、自动生成的目录、对打印友好的版式
12. **HTML 原型**（可选，仅多屏产品）：生成可交互的单帧原型，带两个视图——**Interactive Prototype** 标签页（在一个模拟设备框里点击走完产品流程）和 **All Screens Overview** 标签页（所有状态的缩略图网格，点击任一可跳进交互模式）

## 格式支持

- **Obsidian MD**：Markdown 是规范产物。用相对链接，仅当目标 vault 需要时才用 wiki 链接，图表用内联 Mermaid 代码块。
- **Word**：标题层级严格，表格简单，导出的图表图片旁保留 Mermaid 源码块。不要用纯 HTML 排版。
- **PDF**：标题稳定，配图带说明，表格适配页面，图表带章节级标题。若无法渲染 Mermaid，把源码块保留在 PDF 附录里。
- **Confluence**：标题用 H1-H3，表格简单，链接显式写出，Mermaid 图配一张导出的图片附件外加源码块。不要依赖 Obsidian wiki 链接或裸 HTML。
- **HTML**（Phase 5.6）：由 vendor 进来的 Python 渲染器（`scripts/prd-to-html.py`，需要 `markdown` + `pyyaml`——`pip install -r scripts/requirements.txt`，Python 3.8+）从 Markdown PRD 生成主题化 `.html`。三栏 editorial 版式（章节侧栏 + 正文 + mini-TOC），YAML 元数据渲染成样式化卡片，callout、自动锚点、对打印友好。开启受众拆分时，每个拆分文档各生成一份 HTML 并相互带跳转链接。从 CDN 加载固定版本的 `mermaid@11` 和 Web 字体（离线也能打开，字体回退到系统字体、图表不绘制）。如果 Python 或依赖不可用，`/write-prd` 会自动回退到手工生成 HTML。
- **HTML 原型**（Phase 5.7）：单个 `.html` 的可交互原型。一个模拟设备框，通过点击按钮切换状态。双视图：Interactive Prototype 标签页 + All Screens Overview 标签页。零外部依赖。仅当 PRD 描述多屏/多状态产品时才提供。

## 配置

首次运行 `/write-prd` 时，skill 会询问首选的文档语言并存进 `~/.prd-writer/config.json`。这会影响所有正文输出，包括 HTML 导出。无论怎么选，变量名、状态名和技术标识符始终保持英文。用户可按会话临时覆盖。

## 示例

- `examples/sample-output-prd.md`：游戏 / 互动类 PRD，带 Mermaid 状态图和线框图。
- `examples/sample-ai-agent-prd.md`：AI agent PRD，带自主边界、工具调用时序、评测闭环，以及 `multi` 导出 profile。
- `examples/sample-saas-ops-prd.md`：B2B SaaS/运营 PRD，带工作流状态图、角色权限图，以及 `obsidian_md` profile。

## 依赖

**内置**：write-prd、prd-refine、opus-prd-polish、grill-me、prd-score、prd-split

**外部（可选）**：[gstack](https://github.com/gstackio/gstack)，用于 QA、设计评审、部署验证

细节见 `docs/DEPENDENCIES.md`。

## 更新

- `scripts/update-skill.sh --check-only --force --verbose`：检查当前 clone 是否落后于上游。
- `scripts/update-skill.sh --auto --force --verbose`：立即应用一次安全的 fast-forward 更新。
- `scripts/install-auto-update-hooks.sh`：在 `~/.claude/settings.json` 和 `~/.codex/hooks.json` 里注册启动 hook；对 Codex 还会在 `~/.codex/config.toml` 里启用 `codex_hooks`。

## 设计规则

- 绝不编造 RTP、赔率、监管或市场事实
- 假设和已确认事实在视觉上必须可区分
- 每个变量/状态/事件/配置字段都要有可读的英文标识符
- 美术/设计需求单独成节
- 产品类型和输出 profile 必须记录在每份生成 PRD 的开头附近
- PRD 默认 `semantic_contract_only`；除非明确要求，不规定 Redis、数据库 schema、缓存/队列设计、服务边界、框架选型、SDK 选型或部署拓扑
- 避免原子化的实现措辞；改为描述用户可见的结果和验收标准
- 生成文档里避免指令式措辞，尤其是流程和 agent 行为章节，以免下游 AI 系统把描述性内容误读为可执行指令
- 复杂决策逻辑放进决策表，而不是散落的嵌套要点
- 每条核心流程都要有正常路径和异常路径，并带恢复手段和用户可见的提示
- 输出语言跟随用户偏好（首次运行配置，存于 `~/.prd-writer/config.json`）
- 开启受众拆分时，HTML 导出为每个拆分文档各生成一份文件
- HTML 原型是可交互原型，而非静态线框图集

## 贡献

保持小而可移植。见 `CONTRIBUTING.md`。

## 许可证

MIT
