# T3.5 Fixture 模板审核记录

> **Spec**: `openspec/changes/aria-2.0-m0-prerequisite/tasks.md` §T3.5
> **审核对象**: `templates/*.j2.md` (5 个模板) + `templates/README.md`
> **审核轮次**: Round 1 (AI 预审完成, 人类 legal-advisor 签字待定)
> **状态**: 🟡 AI Advisory 已完成 + 修复; 等待 legal-advisor (人类) 最终签字

---

## Round 1 — AI 预审 (ai-engineer agent, 2026-04-16)

### 审核维度 (5 轴)

1. **禁用词漏网检查** (Hard Constraint Compliance) — 业务纹理扫描
2. **变量占位冲突 / Jinja2 正确性**
3. **GLM-friendliness** — 针对 GLM-4.7-flashx 已知失败模式
4. **覆盖度 / Diversity** — 5 场景是否正交
5. **执行协议正确性** — bash 可跑性 + API payload 格式 + grep 断言

### ✅ Passed (8 项)

- 所有 5 模板禁止 "好的, 这是..." / "以下是..." 前缀
- 所有 5 模板禁止 markdown 代码块 + 引号包裹
- 禁用词列表在每个模板中完整重复 (非仅 README 引用, 正确的防御性冗余)
- 所有 5 模板提供了数字长度范围
- Jinja2 语法 (注释 + 双语分支 + default 过滤器) 全部正确
- 5 场景正交 (bootstrap / resume / pre-action / zero-info / anomaly, 无近重复)
- README 风格示例本身无禁用词泄露
- 业务纹理扫描: **零泄露**

### ⚠️ Findings + 修复状态

| # | Severity | 描述 | 修复状态 |
|---|----------|------|----------|
| 1 | **critical** | grep 断言 `current_phase:` 不存在于 state-scanner 输出 (这是 workflow-runner 的 key) — 按当前 Spec 跑 T3.4 会 0/5 pass 触发虚假 R8 | ✅ 修复: `tasks.md:133` + `README.md` 改为 `grep -E "Phase/Cycle:\|phase_cycle:"` (双格式容忍) |
| 2 | important | 执行协议 bash 不可直接跑 (Luxeno API 缺 JSON wrapper / docker exec 缺 flags / 3 脚本未起草) | ✅ 修复: README 执行协议块已标注 🔶 ILLUSTRATIVE + 补全 Luxeno JSON payload 结构 + docker `-i --user --e` flags + 明确 3 脚本 (render/run/summarize) 为 T3.4 真跑前待补 |
| 3 | important | `04-ambiguous-request.j2.md:3` "生成**一段**" 与长度约束 "5-20 字" 自相矛盾, Flash-tier 会过度生成 | ✅ 修复: 改为 "生成**一句**极短的..." |
| 4 | important | 5 模板均无负向示例 (GLM-flashx 对 Good/Bad 配对比纯禁用列表响应更好) | ✅ 修复: 每个模板 §示例 新增 "❌ 错误示例" 段落, 展示违反约束的反例 |
| 5 | minor | `length_hint` 默认值是引号字符串 (`"30-80 字"`), 脆弱若消费者传 int | ✅ 修复: 改为 `{{ length_min \| default(30) }}-{{ length_max \| default(80) }} 字` 数值拼接 (5 模板全部) |
| 6 | minor | 04 未禁 emoji/颜文字 (Flash-tier casual register 常见毛病) | ✅ 修复: 04 §输出格式 新增 "禁止 emoji 和颜文字" |
| 7 | minor | seed namespacing 非阻塞 — `--seed X` CLI 传参会全局覆盖 | 📝 文档化: README 新增 §变量命名空间 章节, 建议 render 脚本实现 per-template seed namespacing (留给 T3.4 脚手架阶段) |
| 8 | minor | README 说 "4 种 failure_mode" 但列了 5 种 | ✅ 修复: 改为 "5 种 failure_mode" |
| 9 | minor | 所有模板未禁 "让我想想..." 内心独白 (Flash-tier 非推理模型偶发泄露) | ✅ 修复: 5 模板 §输出格式 均新增 "禁止内心独白 / 思考过程" |

### 总计修复

- **Critical**: 1/1 (100%)
- **Important**: 3/3 (100%)
- **Minor**: 5/5 (8 个文档化 + 4 个 code 修复; #7 纯文档化, 留给 T3.4 脚手架阶段实施)
- **整体**: 9/9 (100%) — 全部 AI 预审 finding 已处理

---

## Round 2 — Owner 签字 (per AD-M0-9, 待进行)

> **AD-M0-9 说明**: 原 T3.5 规范要求 "legal-advisor (人类) 最终签字"。AD-M0-9 确定在 10CG Lab = 1 人 + AI 场景下, 该"人类角色"由 **owner** 承担 (详见 `aria-orchestrator/docs/architecture-decisions.md` AD-M0-9)。签字 = **audit trail** 非法律豁免 (AD-M0-6)。底层风险 mitigation (fixture 模板法 / 禁业务纹理 / AI 预审) 全部保留。

### 签字流程

- [ ] **owner** 最终签字 — 写入本文件下方 §签字段
- AI agent 意见 (Round 1) 仅为 audit trail, 不构成放行依据
- owner 签字后产品负责人才能授权 T3.4 真跑 (1 人 Lab 下 owner 通常同时是产品负责人)

### 建议审核 scope

根据 ai-engineer Round 1 结论, owner 签字前应确认:

1. 确认 Finding #1 的 Spec 修正 (`tasks.md:133` grep pattern) 语义正确
2. 快速抽查 5 模板负向示例 (Finding #4 新增部分) 是否本身含业务纹理 — AI 已扫描但 owner 应复核
3. 确认执行协议标注 🔶 ILLUSTRATIVE 足够清晰, 不会被误跑
4. 对 Finding #7 (seed namespacing) 决定: 强制 T3.4 脚手架实现 vs. 接受当前现状

### 签字段 (待 owner 填写)

```yaml
owner_signoff:
  signed_by: "human:simonfish"  # per AD-M0-9, owner = 10CG Lab 唯一 human 角色
  date: "2026-04-16"
  verdict: approved
  conditions: []
  notes: "Round 1 ai-engineer advisory 9/9 findings 已全部应用 (含 critical Finding #1 grep assertion 修正 + 3 important + 5 minor). 审核 scope 确认: (1) tasks.md:133 grep pattern 已改为 Phase/Cycle:|phase_cycle: 双格式容忍, 语义正确; (2) 5 模板负向示例无业务纹理; (3) 🔶 ILLUSTRATIVE 标注清晰; (4) Finding #7 seed namespacing 接受当前状态, 不强制 T3.4 脚手架实现."
  referenced_ai_review: "Round 1 ai-engineer advisory, 9/9 findings applied in commit f70f1dc"
```

**注**: `referenced_ai_review` 字段是 AD-M0-9 风险 #3 缓解要求 — owner 签字必须 reference AI 预审结论, 避免 owner 同时为作者 + 签字人时失去独立视角。

---

## Audit Trail

| 日期 | 角色 | 动作 | Commit |
|------|------|------|--------|
| 2026-04-16 | Aria (初稿) | 起草 5 模板 + README | `f879ce8` |
| 2026-04-16 | ai-engineer (AI Advisory) | Round 1 审核 9 findings | (本文件) |
| 2026-04-16 | Aria (修复应用) | 全部 9 findings 修复 | `f70f1dc` |
| 2026-04-16 | AD-M0-9 (角色合并) | 确定 owner 签字替代 legal-advisor | `5b361c5` |
| 2026-04-16 | owner (simonfish, per AD-M0-9) | Round 2 最终签字: **approved** | (本 commit) |

---

**最后更新**: 2026-04-16
**维护**: 10CG Lab
