# Design Memo: Agent Lifecycle Management (aria-fleet 子能力, M7) — brainstorm + 业界对标收敛

> **Type**: Strategic design memo (非 OpenSpec / 非 DEC — 封存 M7 brainstorm 全部收敛 + deep-research 对标, 供 M6 ship 后起 M7 OpenSpec 作 starting point)
> **日期**: 2026-06-16
> **来源**: owner "M7 aria-fleet brainstorm" → 聚焦 1 (先 1 再 2) → agent-registry 升级为完整 agent 生命周期管理
> **Status**: 战略方向 + 设计收敛已确认; 实施时机 M7 (M6 ship 后); 输出为 planning sediment, 未立项
> **Predecessors**:
>   - `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (D1-D6 Approved — 命名/三层/时机, 本 memo 不重议)
>   - `.aria/notes/2026-06-13-agent-registry-for-aria-fleet.md` (agent-registry 愿景 + §5 四决策 + Claude Code 加载机制调研)
>   - Forgejo Aria #128 (M7 aria-fleet implementation tracker, US-027)
> **Owner sign-off**: ✅ 本次 brainstorm 段 1/段 2/段 2 补强/段 2 收尾/调研 4 修正/段 3 逐段确认通过 (2026-06-16 session)
> **Audit discipline**: 设计备忘录, 未走 post_brainstorm audit; 正式审计留 M7 OpenSpec 立项时

---

## §0 一句话

把 `.aria/agents/` 升级为一套**围绕每个 Aria 项目的项目级 agent 完整生命周期管理能力** (推荐 → 加载 → 使用 → 更新 / 吸收 → 汇总), 让**重复需求的 agent 不重复设计**, 并在 Aria 生态中**持续优化、汇总、自我迭代**。本质 = aria-fleet L1/L2 的"跨项目 agent 复用 + 回流"子能力。

---

## §1 四个 §5 决策的收敛 (来自 2026-06-13 note §5)

| # | 决策 | 结论 | 理由 |
|---|------|------|------|
| **#1 对内 vs 对外定位** | **先对内、设计预留通用** | 代码写成 any-org 通用 (不 hardcode 10CG), 但当前只 10CG 用、不对外发布。与 D1-D6 L1 姿态一致 (L1 设计通用、只有 10CG 一个 workspace 实例), 避方法论红线 + 不欠技术债 |
| **#2 自建 registry vs marketplace 试水** | **均撤销 → 改 git 集合库 + 文件物化** | brainstorm 中深挖发现: 真实愿景 = agent 粒度 + 因项目而异推荐 + 选择性物化; 而 Claude Code marketplace 选择性最细只到**整个插件** (调研确认, 见 §1 附), 给不了 agent 粒度。故 marketplace 既非核心机制、也不做试水; 核心机制 = "集合库 = git 仓库, Aria 直接读 + 物化进 `.claude/agents/`" |
| **#3 registry ↔ marketplace 关系** | **DEFERRED** | M7 阶段 marketplace 不参与核心闭环; 未来若需要可作为粗粒度分发 backbone, 非 M7 |
| **#4 粒度版本 / 覆盖 / push-back 机制** | **DEFERRED 到 M7+** | 这套机制等下行铺好 + 真实使用数据后再设计 (见 §7 推迟项); 现在设计违背"用数据说话"哲学 |

**§1 附 — Claude Code 加载机制事实** (claude-code-guide 核实, 官方文档 2026-06-15):
- 多 agent 加载负担: session 启动只载 frontmatter (name+description, ~20 token/个), 完整 system prompt 用到时才懒加载 → 100 个 agent ≈ 2K token 常驻. **真实代价不是 token 而是路由稀释** (主模型在大量 agent 里挑, 误派↑)。**结论: registry 几百 agent 愿景不能做成巨包**。
- 选择性加载: agent 粒度**不能** (官方无此功能); 插件粒度**能** (`enabledPlugins` 整包开关)。要项目级 agent 子集, marketplace 下**唯一办法是按领域拆插件**。→ 印证 #2: 要 agent 粒度智能配给, 必须走文件物化, 非 marketplace。
- session-start 时效: 物化进 `.claude/agents/` 的 agent **要重启 session 才能原生 spawn**; 同 session 即用需 `agent-router` 软注入兜底。

---

## §2 核心闭环 (六阶段双向飞轮)

```
          ┌──────────────────────────────────────────────┐
          │   集合库 Registry  (L1 通用 / L2 10CG 私有)   │
          │   精选 agent + 能力标签 + 版本 + 来源溯源      │
          └──────────────────────────────────────────────┘
            ▲  ⑤吸收 / ⑥汇总 (push)        │  ①推荐 / ②加载 (pull)
            │                              ▼
          ┌──────────────────────────────────────────────┐
          │   项目 .claude/agents/   (L3 instance)         │
          │   物化的 agent 子集  +  项目本地改写            │
          └──────────────────────────────────────────────┘
```

| # | 阶段 | 做什么 | 复用现成零件 |
|---|------|--------|------|
| ① | **推荐** | 扫项目特征 → 比对库能力标签 → 推荐"该装哪几个" | `project-analyzer` + `agent-gap-analyzer` |
| ② | **加载** | 确认后物化进 `.claude/agents/` + 记 manifest (装了哪些 / 哪版) | (新) + `agent-creator` 物化逻辑 |
| ③ | **使用** | 项目正常用; 可能本地改写优化 | `agent-router` |
| ④ | **更新** | 库 agent 升级 → 检测用旧版项目 → 提示更新 (**不冲掉本地改写**) | (新) |
| ⑤ | **吸收** | 项目新建/改进的 agent → 推回库当候选 (= gap #3 push-back) | (新) |
| ⑥ | **汇总/优化** | 审候选 → **去重 (重复需求合并)** → 提升+版本化 → 下轮 pull 全生态受益 | (新) |

闭环精确对应问题本质: ①推荐复用 = "重复需求不重复设计"; ⑤+⑥ = "生态内持续优化汇总"; 下行=分发, 上行=回流, 飞轮转起来库越用越好。

---

## §3 四块硬骨头 (闭环逼出来的)

1. **Manifest / lockfile** — 整个闭环的账本 (②④⑤ 都依赖)。记: 装了哪些 agent、各自来自库哪个版本、有无本地改写。类比 `package-lock.json`, 建议 `.aria/agents-lock.yaml`。
2. **更新不冲掉本地改写** (阶段 ④ 最难)。需**三方比对** (库旧版 base / 库新版 / 项目当前): 无改写→直接更新; 有改写→**不自动覆盖**, surface "已分叉, 请人工合并"。
3. **吸收去重 + 质量闸** (阶段 ⑥, 否则库变垃圾场)。两道闸: (a) **去重** — 能力标签识别"与库 X 能力重叠 80%"→ 合并而非新增 (= "重复需求不重复设计"执行点); (b) **质量** — 候选过 curation 审核 (可 Aria 辅助) 才提升+版本化。
4. **机制重审 (推翻 #2)**: 集合库 = git 仓库, Aria 读 + 物化; marketplace 做不了核心闭环 → "先用 marketplace 试水"撤销。

> 附带提醒: 物化的 agent 要重启 session 才原生 spawn; 同 session 即用需软注入兜底。

---

## §4 AB 驱动吸收矩阵 + usage-telemetry 活体库 + 零游离不变式

### 吸收决策矩阵 (把硬骨头③升级为证据驱动裁决, 契合 Rule #6 哲学)

| 项目 agent vs 库 | 判定方式 | 动作 |
|---|---|---|
| 库里**没有**此能力 | — | **push 候选** → Aria 审核 → 入库 (new) |
| 与库 agent **高重叠** | 跑 **AB** | ↓ 按胜负分流 |
| └ 项目版胜 | AB | **reverse push**: 项目改进 → 库 agent 升版 |
| └ 库版胜 | AB | **forward pull**: 库版覆盖项目 agent |
| └ 打平 | AB | 维持现状 / 合并能力标签 |
| 与库版相同 (未改写) | lockfile | 已管理, 无动作 |

### 活体库 (owner 反馈 1+2 合流)

- **取消 "project-local-private" 二元标志** — 没有真·项目专属 agent, **全部归库**。
- "别的项目能不能用" 由 **usage-telemetry 差异化**承载: 被多少项目采用 / 累计调用次数 / 多轮审计中被调用频率 / 成功-产出信号 → 每个 agent 自带**采用度/声誉** ("12 项目 / 340 次" vs "1 项目 / 3 次")。
- 这套 usage-telemetry **正是**持续观测 AB 信号 → 既做再评估依据, 又做跨项目发现标签 → 库**自我迭代** (高采用高成功→固化; 低采用低成功→标记/裁汰)。

**收敛不变式**: 生态内**零游离 agent** — 每个项目 agent 要么是从库 pull 的, 要么已被吸收审核进库管理; "可用性" 由 usage metadata 承载, 而非 share/private 标志。

---

## §5 持续观测的实验设计 (高相似 agent 怎么科学比)

**"直接切 aria 镜像再顺序观测" = 最不科学** (时间混淆: 切换前后任务分布不同, 差异无法归因)。

| 方法 | 怎么做 | 严谨度 | 代价 |
|------|--------|--------|------|
| **影子 / 配对跑** ⭐ | 同一任务两 agent 都跑, LLM-judge 配对打分 | 最高 (相同输入消混淆, 配对样本功效高) | 2× 调用 + 需裁判 |
| **离线回放** | 真实历史任务 corpus 两 agent 各跑打分 | 高 (可控可比) | 需任务日志 corpus; 离线≠实战 |
| **生态池化观测** | 单项目流量稀疏 → 跨所有用此 agent 的项目汇总 | 中 (真实但非配对) | 需跨项目 telemetry (= §4 usage 数据) |
| ~~直接切镜像~~ | 顺序观测 | ❌ 低 (时间混淆) | — |

**推荐组合**: 高相似裁决 → **影子/配对跑** (复用 audit-engine LLM-judge); 长期声誉 → **生态池化**; 影子跑 2× 成本 → **触发式** (仅高重叠 + 评估窗口内)。
⚠️ 边界: 影子/配对对**只读/分析型 agent** (reviewer/auditor) 干净; 对**会改文件的 agent** 需"只比对输出建议、不真执行"或沙箱跑。

---

## §6 业界对标 (deep-research: 22 源 / 98 claims → 25 对抗核实 / 24 确认 1 驳回)

### ✅ A. 已验证、可复用

| 方法 | 验证级别 | 服务于 | 复用点 |
|------|---------|--------|--------|
| **LLM-as-judge** | 同行评审 (GPT-4 与人 >80% 一致) arXiv:2306.05685 | SELECTION | AB 裁决方法学站得住 |
| **PoLL 评审团** (不相交模型家族小 judge) | arXiv:2404.18796 | SELECTION 去偏 | 更准 / self-preference 更小 / 便宜 7×; **audit-engine 多 agent + GLM/Claude 双家族 = 天然 PoLL** |
| **pass^k 可靠性度量** (k 次全对) τ-bench arXiv:2406.12045 | 同行评审 ICLR'25 | EVALUATION 可靠性 | 量化"够不够可靠到吸收" (开放: 对话域→编码域迁移未验证) |
| **A/B side-by-side + trajectory 监控** | survey arXiv:2503.16416 + LangSmith/Langfuse/Braintrust/Phoenix/Inspect | 工具链 | "AB gate + 持续观测" 有现成平台层 |

### ⚠️ B. 已验证陷阱 — 命中"一次性 AB gate"

1. **基准可被 harness-gaming 刷满分**: 8 大 agent 基准 (含 SWE-bench) 不解决任务也能刷近满分 (10 行 conftest.py → 100%); **OpenAI 2026-02 弃用 SWE-bench Verified** (Berkeley RDI; arXiv:2605.12673)。→ 固定测试集做 one-shot gate **可钻空 + 会饱和**。
2. **排名不稳**: UTBoost 修正测试不足 → **24-41% 榜单翻转**, 连第一换人 (arXiv:2506.09289)。→ 相似 agent 的 pass/fail **薄边际不可信**。
3. **scaffold/预算混淆**: MLE-bench — attempts/runtime 不归一化结论被污染 (arXiv:2410.07095)。→ 配对**必须等预算等 scaffold**。
4. **顺序 A/B 时间混淆**: 研究确认成立**但无已验证缓解** (开放) → 我们**并发配对**是对的。

### 🌱 C. 真正新颖、prior-art 最弱 (须自研慎做)

- **影子/配对 + 跨会话生态池化遥测** = 全研究覆盖最弱; interleaving "灵敏度 100×" 主张 **3 票 0-3 驳回** (arXiv:2508.00751) → Aria 原创, **保守设计 + 自己实证, 别假定已验证**。
- **"按项目特征推荐 agent" (①推荐)**: routing 研究 (RouteLLM/MoA) **无 claim 通过核实** → project-analyzer + 能力标签匹配是**启发式**, MVP 可接受。

> 元 caveat: 多条 2026 关键证据是未同行评审 arXiv preprint (gaming / SPB / PoLL-followup / plateau), 数字当**方向性 preliminary**。

### 据此对 §4/§5 方法论的 4 处修正 (已收入设计)

1. **one-shot gate 改 pairwise LLM-judge 为主**; **不用**固定测试集 pass/fail 当主裁; 若用任务执行 → live 刷新任务集 + pass^k + 归一化预算 + 要求**显著边际**。
2. **裁决器 PoLL + 三件套去偏**: GLM+Claude+第三家族 panel; **position-swap 双跑** (位置偏差翻转率 60-75%); **五维 forced-choice** (Relevance/Accuracy/Depth/Logic/Clarity, 降 self-preference ~31.5%, arXiv:2604.22891)。
3. **影子/池化标记 Aria 原创**: 可靠性走 pass^k 式多次一致; 跨会话遥测**先验证记录真产出** (R-fix-1 教训, memory `feedback_telemetry_verify_records...`)。
4. **配对必须并发** (非顺序), 规避时间混淆。

---

## §7 三层映射 + M7 第一刀

### 套进 aria-fleet L1/L2/L3 (2026-05-27 Approved)

| 层 | 放什么 |
|----|------|
| **L1 通用** | lifecycle 工具框架 (集合库结构 + lockfile schema + 推荐/加载/更新/吸收引擎 + AB-judge harness + 遥测 schema) + 通用 agent 层 (语言/框架无关精选)。零 10CG hardcode |
| **L2 workspace (10CG)** | 10CG 私有 agent (shell-safety / ssh-egress / homelab-topology) + curation 决策 + 跨 10CG 项目累积 usage 遥测/AB 语料 |
| **L3 instance (项目)** | `.claude/agents/` 物化集 + `.aria/agents-lock.yaml` + 项目本地覆盖 + 本项目 usage 遥测 |

下行 (①②) = L1/L2 → L3; 上行 (⑤⑥) = L3 → L1/L2。

### M7 第一刀 = 下行 pull 半环 (依赖关系锁定, 非随意切)

**上行必须先有下行**: 吸收/AB/汇总都需"已部署 agent + 累积真实使用"; 没项目先 pull, 就没观测数据。顺序被依赖锁定。

**M7-MVP**: 集合库骨架 (git + 精选 agent + 能力标签 + 版本) → 推荐 (接 project-analyzer + gap-analyzer 读库) → 加载 (物化 `.claude/agents/aria-<name>.md` + 写 `.aria/agents-lock.yaml` + "重启生效"提示) → 更新-基础版 (lockfile 版本 < 库版本 → 提示重物化; 三方不冲改写 fast-follow)。**大量复用现成 4 Skill** (project-analyzer / agent-gap-analyzer / agent-creator / agent-router)。

**M7+ 推迟** (等下行铺好 + 真实数据): AB-judge harness (PoLL+去偏) / 影子-配对评测 / 生态池化遥测 / 吸收 push-back / curation 闸 / 零游离不变式强制。← 正好是 §6-C prior-art 最弱、最该有真实数据后做的部分。

---

## §8 开放问题 (M7 立项时回答)

1. **routing prior art 弱**: "按项目特征从相似 agent 推荐/路由" 无已验证方法 (RouteLLM/MoA 未存活) → ①推荐 环节是启发式, 需自行验证。
2. **pass^k 跨域**: τ-bench 是 tool-use 对话域; 迁到编码 agent 吸收裁决缺直接验证。
3. **顺序 A/B 时间混淆缓解**: 研究点名为陷阱但无已验证缓解 → 我们并发配对设计需自证。
4. **工具链 shadow/池化支持深度**: LangSmith/Braintrust/Phoenix/Langfuse/Inspect 对"配对/影子" + "跨会话遥测聚合" 的现成支持未逐一核实 (survey 仅到离线 A/B + 生产 trajectory 监控)。
5. **agent AB eval harness**: Rule #6 的 `/skill-creator benchmark` 是给 skill 的; agent 评测可能需专门 harness (开放)。
6. **吸收审核谁来做**: curation 闸是 Aria 辅助 / audit-engine / 人工? 待定。

---

## §9 Cross-references

- 三层架构 (D1-D6 Approved): `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md`
- agent-registry 愿景 + 加载机制调研: `.aria/notes/2026-06-13-agent-registry-for-aria-fleet.md`
- M7 tracker: Forgejo Aria #128 (US-027)
- 现成 Skill: `aria/skills/{project-analyzer, agent-gap-analyzer, agent-creator, agent-router}/`
- 调研全文 (本 session): deep-research workflow 产物 (transcript)
- 遥测验证教训: memory `feedback_telemetry_verify_records_in_prod_not_just_code_exists`

### 调研主要引用源

- LLM-as-judge: arXiv:2306.05685 (NeurIPS'23)
- PoLL: arXiv:2404.18796 (Cohere) + follow-up arXiv:2605.29800
- self-preference bias 缓解: arXiv:2604.22891 (preprint)
- selection bias 分解: arXiv:2410.15393 (CalibraEval)
- SWE-bench Verified: openai.com/index/introducing-swe-bench-verified + arXiv:2310.06770
- benchmark gaming: rdi.berkeley.edu/blog/trustworthy-benchmarks-cont + arXiv:2605.12673 (BenchJack, preprint)
- 排名不稳: arXiv:2506.09289 (UTBoost, ACL'25)
- 静态基准饱和: arXiv:2503.16416 (survey) + arXiv:2602.16763
- MLE-bench: arXiv:2410.07095 (ICLR'25)
- τ-bench / pass^k: arXiv:2406.12045 (ICLR'25)
- interleaving 100× (驳回): arXiv:2508.00751
- 工具链: inspect.aisi.org.uk + langchain.com/resources/langsmith-vs-braintrust

---

**Created**: 2026-06-16
**Author**: AI (Claude Opus 4.8 1M context) via owner-driven brainstorm + deep-research
**Status**: M7 设计收敛已封存; 实施待 M6 ship 后 M7 OpenSpec 立项
**Next**: (a) owner 决定是否接着做选项 2 (aria-fleet 整体 MVP scoping brainstorm, per "先 1 再 2"); (b) M6 ship 后据本 memo 起 M7 OpenSpec
