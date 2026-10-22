# T5 重判 dogfood — 分类修订对历史三轮 4b 数据的门效果

> **数据源** (只读): `ab-results/2026-10-19-issue-groomer-trigger/{real-v1-prefix,real-v2-broad,real}/run_eval.json` (六臂中三个被评臂; 三个 negctrl 臂 valid, 不涉分类)。
> **重判脚本**: 同目录 `rejudge.py` (随 spec 提交; 路径自解析, 任意 CWD 可复跑; 输出 idx = 套件条目行号, should-not 为 10-19)。
> **语境**: 三臂历史门判定均为 FAIL — 第一轮 FAIL 根因 = SilkNode narrate 缺 tool_use (环境故障), 第三轮 FAIL 根因 = 沙箱伪影 (Aria#243 立项根因); owner 2026-10-21 终裁选项 a 放行 v1.77.0 ship, SOT 修订另立本轨。**本轮重判 ≠ 新跑 4b**, 是「修订后判据对同一数据集的判定变化」演示; 套件标注未经 owner 审阅前不作 production 门。

## 分类清单 (should-not 10 条, idx = 套件行 10-19)

| idx | query 要义 | type | rationale |
|-----|-----------|------|-----------|
| 10 | 核对 #235 是否真修好 (版本→复现→in-flight) | **routing** | issue-triage 的活 (单条核对) |
| 11 | 新 bug report triage + cannot-reproduce 草稿 | **routing** | issue-triage |
| 12 | 看项目状态 + 推荐下一步阶段 | **routing** | state-scanner (proposal 点名的「纯状态查询」证据条) |
| 13 | Forgejo 建 issue + label | **capability** | 写操作, description 明示「建单不做」; 无兄弟承接手动建单 |
| 14 | 项目板挪列 + 打 P2 标签 | **capability** | 写操作, 无兄弟承接 |
| 15 | 7 条疑似已修直接关掉 | **capability** | groomer 只建议关单; 执行面无兄弟 |
| 16 | openspec 归档 + 落点校验 | **routing** | openspec-archive |
| 17 | scratchpad/ 目录整理 | **capability** | 基线有效先例 (能力外) |
| 18 | 上月 issue 汇总 changelog | **capability** | 基线有效先例 (能力外) |
| 19 | 查 #200 状态/label/评论时间 | **capability** | **两可从严**: issue-triage 可勉强承接, 但其语义是「核对验证」非「状态查询」; 计门 (防放水原则) |

**裁量原则**: 修订者与误触受益方同体 (issue-groomer 曾被 9/10 误触卡 ship), 两可条目一律 `capability` (计门) — 分类不得成为过门捷径。标注待 owner 审阅 (AB 手册: 改套件须经 owner 审阅后作门)。

## 重判结果 (idx = 套件行 10-19)

| 臂 | 旧门 fail 集 (全量 should-not) | 新门 fail 集 | 观察面 routing | 门布尔值 |
|----|------|------|------|------|
| real-v1-prefix | {11, 13, 15} | {13, 15} | {11} | FAIL → FAIL |
| real-v2-broad | {10,11,12,13,14,15,16,18,19} | {13,14,15,18,19} | {10,11,12,16} | FAIL → FAIL |
| real | {10,11,12,13,14,15,16,18,19} | {13,14,15,18,19} | {10,11,12,16} | FAIL → FAIL |

- **SC-2 GREEN**: 三臂 fail 集合均实际缩小 (v1-prefix 3→2; v2-broad/real 9→5), 分类分流真实发生。
- **门布尔值不变 (如实报告)**: 三臂在新门下仍 FAIL — capability 面残留 5 条误触 (建单/挪列/关单/changelog/单条查询)。这是修订后**新暴露的信号**: description 的「不写回 tracker (建单/关单/打标/挪列均不做)」边界在单技能沙箱下同样未守住。解读候选 (未裁): (a) description 能力边界措辞弱 (真问题); (b) 唯一技能在场时模型的接活倾向 (沙箱伪影的 capability 面延伸 — 但本轨结构性论证只覆盖 routing 类, 此解读**不在本修订承诺内**, 留观察面)。issue-groomer 后续若再动 description, 4b 门将如实卡这 5 条 — 修订没有为它开后门。
