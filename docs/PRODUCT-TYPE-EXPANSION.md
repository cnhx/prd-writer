# PRD-writer 产品类型扩展探索

本文用于规划 PRD-writer 的下一阶段产品方向。重点放在产品类型、创意框架、调研证据进入 PRD 的方式，不展开技术实现。

## 当前判断

PRD-writer 目前更像一个“高质量 PRD 写作工作流包”，而不是完整的产品管理平台。它的强项是：

- 先做边界扫描，再写需求，能减少 PRD 越权。
- 用 Rejection Letter、kill criteria、premise check 逼迫需求回到可验证范围。
- 支持游戏/互动类 PRD，且能拆出 GDD、TDD、Art & Audio、BD & Marketing。
- 用 Mermaid 把流程、交互、线框、架构意图留在同一份 Markdown 中。
- 文件优先、可迁移、可审查，适合 agent、Obsidian、Git、Confluence 等工作流。

主要空白是：

- 现有结构偏游戏和互动产品；SaaS、AI agent、数据产品、平台型产品、消费增长产品还缺少专门提问和模板。
- 市场、竞品、用户反馈等调研证据还只是“Sources”一节，没有形成明确的 evidence-to-decision 机制。
- 输出拆分目前按游戏/研发协作 discipline 设计，其他行业的受众包还不够自然。

## 产品调研摘录

以下观察来自本次对公开产品资料的快速调研。

| 产品 | 观察 | 对 PRD-writer 的启发 |
|---|---|---|
| Jira Product Discovery | 主打收集、组织、优先级排序、roadmap，并把 idea 连接到 Jira delivery。AI 能在 idea 描述和评论中生成、总结、缩短内容、提取 action items。 | PRD-writer 不应只写 PRD，还要保留“why behind the work”：idea、insight、delivery item 之间的可追踪链路。 |
| Productboard | 强调反馈、insight、feature hierarchy、roadmap。AI 功能包括基于 linked insights 生成 feature specs、总结反馈 note、搜索相关 insights、识别 themes、自动把 insights 连接到 feature ideas。 | 下一步应该把“source evidence coverage”变成一等公民：没有足够 evidence 的 PRD 要主动降级或标记。 |
| Aha! Roadmaps | AI assistant 覆盖市场/竞品/用户画像调研、反馈主题总结、solution exploration、原型生成、roadmap planning、release notes、进度风险总结。 | PRD-writer 可以把“创意探索”和“正式 PRD”分成两层，先跑 concept lab，再进入 write-prd。 |
| Miro AI PRD | 从白板、便签、wireframe、已有 discovery board 生成 PRD，并留在协作画布中给设计、工程和 stakeholder 评论。 | PRD-writer 可以支持“混合输入”：文字 brief、研究摘录、线框图说明、用户旅程、竞品截图说明。 |
| Dovetail | 把访谈、工单、评论、NPS/CSAT 等反馈集中，AI 做主题、报告、问答、source-backed insight。 | PRD 里的调研不应只写结论，要保留支持 quote、来源类型、时间范围和证据强度。 |
| ChatPRD | 定位为 PM 的 AI 平台，强调团队上下文、历史、custom personas、给工程/设计生成 specs、权限控制。 | PRD-writer 的差异点可放在“本地/文件优先 + 强审查 + 多 agent 可迁移”，而不是做一个 SaaS 平台。 |

## 建议支持的新产品类型

### 1. AI agent / 工作流自动化产品

适合：AI 助手、内部 agent、自动化运营、知识检索、代码/设计/客服 agent。

PRD 重点：

- 用户把哪些判断交给 agent，哪些必须 human-in-the-loop。
- agent 的输入、输出、可拒绝边界、可恢复路径。
- 错误类型：幻觉、越权、遗漏、重复执行、权限误用、上下文陈旧。
- 质量评估：golden tasks、人工抽检、失败样例、回滚标准。
- 信任设计：引用来源、confidence、操作前确认、审计日志。

可新增输出：

- Agent Behavior Spec
- Eval Plan
- Human Review Playbook

### 2. B2B SaaS / 内部运营工具

适合：CRM、项目管理、审批流、BI 后台、运营平台、企业内部工具。

PRD 重点：

- 角色、权限、任务流、状态流转、异常处理。
- 信息密度和重复使用效率，而不是营销式页面。
- 审批、通知、导入导出、历史记录、权限边界。
- 当前替代方案：表格、群聊、Jira、Notion、手工同步。
- 成功指标：节省时间、错误率下降、处理吞吐、协作等待时间下降。

可新增输出：

- Role & Permission Matrix
- Workflow State Map
- Ops Runbook

### 3. 数据 / 分析 / 决策支持产品

适合：dashboard、报表、监控、实验平台、数据洞察、经营分析。

PRD 重点：

- 具体决策场景，而不是“看数据”。
- 指标定义、口径、刷新频率、数据质量、异常解释。
- 从数据到行动：用户看到信号后要做什么。
- 防误读设计：置信度、样本量、数据延迟、不可比较条件。
- 受众差异：高管看趋势，运营看动作，分析师看明细。

可新增输出：

- Metric Dictionary
- Decision Loop Map
- Data Quality Checklist

### 4. 平台 / Marketplace / 集成型产品

适合：开放平台、API、插件市场、支付/聚合渠道、B2B2C、供需撮合。

PRD 重点：

- 多边参与者：供给侧、需求侧、平台运营、合作伙伴。
- 信任、审核、准入、违规处理。
- partner onboarding、API contract、版本兼容、迁移路径。
- 冷启动策略和流动性指标。
- 平台收益模型：抽成、订阅、增值服务、交易费。

可新增输出：

- Actor Incentive Map
- Partner Onboarding Brief
- Trust & Safety Requirements

### 5. 消费级移动 / 增长产品

适合：App、小游戏、内容产品、社区、会员、推荐、通知、裂变。

PRD 重点：

- 首次体验、激活时刻、留存循环、召回机制。
- 情绪曲线和反馈节奏。
- 通知、分享、邀请、成就、会员权益的边界。
- 实验假设和防打扰原则。
- 成功指标：activation、D1/D7、repeat action、share rate、conversion。

可新增输出：

- Onboarding Narrative
- Growth Loop Map
- Experiment Brief

### 6. 内容 / 教育 / 知识产品

适合：课程、知识库、学习工具、内容社区、AI tutor、企业培训。

PRD 重点：

- 学习目标、内容颗粒度、路径、练习、反馈。
- 内容质量标准和更新机制。
- 适应不同水平用户的分层体验。
- 评估方式：完成率、掌握度、复习行为、实际任务迁移。

可新增输出：

- Learning Outcome Map
- Content Rubric
- Feedback Loop Spec

## 基础功能框架建议

### A. Product Type Router

在 `/write-prd` Phase 0 前增加轻量判断：这个 brief 属于哪种产品类型，是否需要混合类型。

建议首批类型：

- game_interactive
- ai_agent
- b2b_saas_ops
- data_analytics
- platform_marketplace
- consumer_growth
- content_learning

每种类型只影响提问、章节重点和输出包，不改变 PRD-writer 的核心流程。

### B. Research Pack

把调研输入做成 PRD 前置材料，而不是散落在 Sources。

建议字段：

- evidence_type：interview、support_ticket、sales_call、competitor_page、analytics、market_report、internal_note。
- source_ref：文件路径、URL、issue、Slack/Confluence/Jira 引用。
- freshness：时间范围。
- confidence：high / medium / low。
- product_decision_link：这条证据支持或反驳了哪个 PRD 决策。

最有价值的变化：PRD 可以明确说“这个需求是证据驱动、假设驱动，还是 stakeholder request”。

### C. Concept Lab

正式写 PRD 前先给 3 个创意方向，每个方向都包含：

- 产品承诺：用户为什么会在意。
- 关键体验：用户第一次感到“有用”的时刻。
- 反直觉设计：一个不常见但有机会的设计选择。
- Kill criteria：什么信号出现就砍掉。
- 最小验证：用什么低成本方式判断是否值得进入 PRD。

这能把 PRD-writer 从“写文档工具”推进到“帮产品成型的工具”。

### D. Audience Pack

把 `/prd-split` 从游戏 discipline 扩展成按产品类型拆输出。

建议映射：

- AI agent：Agent Spec、Eval Plan、Reviewer Playbook、Risk Brief。
- SaaS/Ops：Workflow Spec、Permission Matrix、Support Runbook、Release Brief。
- Data/Analytics：Metric Dictionary、Decision Guide、Data Quality Checklist。
- Platform：Partner Brief、API Contract Summary、Trust & Safety Brief。
- Consumer Growth：Experiment Brief、Lifecycle Messaging Brief、Design Brief。

### E. Evidence Score

在 `/prd-score` 中新增一个不影响 Ready-to-Dev 主分的证据视图：

- coverage：关键需求中有多少条有证据。
- freshness：证据是否过期。
- contradiction：是否存在互相冲突的证据。
- unvalidated leap：从证据到需求是否跳太远。

这会让 PRD-writer 与普通 AI PRD 生成器拉开距离：不是只写得像，而是能说明为什么该写。

## 推荐优先级

1. 先做 Product Type Router 和 3 个产品类型包：AI agent、B2B SaaS/Ops、Data/Analytics。
2. 同步做 Research Pack 的最小格式，让任何 PRD 都能引用调研证据。
3. 再做 Concept Lab，用于 PRD 前的创意探索和方向对比。
4. 最后扩展 Audience Pack，把 `/prd-split` 从游戏 discipline 拓展到行业输出包。

这个顺序的好处是：先提升 PRD 起草质量，再提升创意探索，最后提升协作交付。核心 workflow 不需要推翻，只需要加“产品类型镜头”和“证据镜头”。

## 下一步可落地的 v0.9 目标

v0.9 可以定义为“Product Type Packs”版本：

- 新增产品类型识别规则。
- 新增 `ai_agent`、`b2b_saas_ops`、`data_analytics` 三个类型包。
- 每个类型包提供：触发信号、Phase 1 追加问题、Section 4/5/6/7/8/10 的写作重点、推荐输出包。
- README 增加一张支持类型表。
- 示例增加一份 AI agent PRD 和一份 SaaS/Ops PRD。

暂不建议在 v0.9 做复杂集成、数据库、网页 UI 或多工具同步。PRD-writer 当前的优势是轻、准、可审查，先把产品思维做深，再考虑平台化。

## 调研来源

- Jira Product Discovery：<https://support.atlassian.com/jira-product-discovery/docs/what-is-jira-product-discovery/>
- Jira Product Discovery AI：<https://support.atlassian.com/organization-administration/docs/atlassian-intelligence-features-in-jira-product-discovery/>
- Productboard AI：<https://support.productboard.com/hc/en-us/articles/15113485128467-Productboard-AI>
- Productboard 概览：<https://support.productboard.com/hc/en-us/articles/360058147693-What-is-Productboard>
- Aha! Roadmaps AI Assistant：<https://www.aha.io/roadmaps/ai-assistant>
- Miro AI PRD：<https://miro.com/ai/product-development/ai-prd/>
- Dovetail AI：<https://docs.dovetail.com/help/dovetail-ai/>
- ChatPRD：<https://www.chatprd.ai/>
