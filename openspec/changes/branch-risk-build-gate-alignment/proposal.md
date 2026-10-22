# branch-risk-build-gate-alignment — branch-manager 风险误判修复 + branch-finisher 构建门对齐 config

> **Level**: Full (Level 3 Spec)
> **Status**: **Approved (owner 2026-10-22, 全套 ①②③④)** — ready for Phase B
> **Created**: 2026-10-22
> **Linked Issue**: `10CG/Aria#231`
> **执行轨**: interactive

## Why

#231 (prompt-audit 2026-10-08, 审 aria 1.74.1, 2026-10-10 复核 master 成立; 本轨 2026-10-22 在 v1.77.0 `f2e801d` 再核仍成立) 报两处 prose 指令面缺陷:

1. **branch-manager 裸 `api` 子串判 high → 单项即 worktree**。`skills/branch-manager/SKILL.md:133` 关键词表 `refactor, architecture, api, breaking` + `internal/MODE_DECISION_LOGIC.md:104-108` 伪码 `any(kw in desc_lower)` 子串匹配: 描述里只要含 "api" (如 SilkNode 实例「修 API key 列表分页」) 即判 high (+3) ≥ 3 分阈值 → 强制 worktree。评分表本意 (`:67`) 是「高 (重构, **API 变更**)」— 关键词检测把「API 变更」偷换成了「提到 API」。对 API 聚合平台类项目 (SilkNode 拓扑 B: 每容器一分支、**禁容器内 worktree**) 这是系统性误判。
2. **branch-finisher 把「本地构建成功」列为无条件阻塞项** (`skills/branch-finisher/SKILL.md:115`), 而 `config-loader` 的 `phase_b_developer.framework_build_check.enabled` 默认 **false** (`:175-181`, Aria #95) — branch-finisher 读 config 却不消费这个开关。构建交给 CI 的项目 (SilkNode 明文规定本机禁 `npm run build`) 按现文永远过不了这一关。

另经本轨 recon 发现的**双源不一致** (同一缺陷类, 一并修): SKILL.md 表与 MODE_DECISION_LOGIC.md 伪码表本就不同步 (伪码多 `rewrite`/`重构`/`架构`/`破坏性`/`核心`), 其中裸 `核心` 与裸 `api` 同病灶 (「修核心模块 typo」会因 high 优先匹配而判 high)。

## What Changed

### 1. branch-manager 风险检测 (SKILL.md:126-136 + MODE_DECISION_LOGIC.md 伪码段, 双源同改)

**判定规则重排** (对齐评分表语义):

- 从 flat 高风险表中**移除裸 `api`** (与裸 `核心`)。
- 新增**共现规则** (api 专用): 描述同时出现 **api 类词** (`api`/`接口`/`endpoint`) 与**变更类词** (`变更`/`change`/`breaking`/`重构`/`重写`/`迁移`/`删除`/`移除`/`deprecat`) 才判 high; 仅出现 api 类词判 medium。例:「修 API key 列表分页」→ medium (Branch); 「API 接口变更」「变更了 API」「breaking api」→ high。
- 统一双源基准表: `refactor, rewrite, architecture, breaking, 重构, 架构, 破坏性` (flat 表, 两处逐字一致; 裸 `api`/`核心` 出表)。SKILL.md 表加中英对照完整版, MODE_DECISION_LOGIC.md 伪码同步改写 (含共现函数)。
- 评分表 `:67` 行措辞不变 (本就写「API 变更」, 修复后检测才真正兑现它)。

### 2. 项目级关键词覆盖 (新 config 键, 覆盖非合并)

- `branch_manager.high_risk_keywords: string[] | null` (default `null` = 内置表)
- `branch_manager.low_risk_keywords: string[] | null` (default `null` = 内置表)
- 语义: 项目提供即**整体覆盖**内置对应表 (与 issue-groomer labels.yaml 裁定-① 同型); 覆盖后 flat 子串语义由项目自负精度; 共现规则仅作用于内置表 (覆盖 high 表 = 项目自管全部 high 判定)。SilkNode 类项目可 `high_risk_keywords: []` 关掉关键词误判面。
- 落点: `config-loader/SKILL.md` schema 段 + `config.template.json` 键同步 (custom check `config-template-key-currency` 机械兜底) + branch-manager SKILL.md 增「配置 (config-loader)」节 (现无, branch-finisher:37 同型)。

### 3. branch-finisher 构建验证跟随 `framework_build_check` (SKILL.md:105-165)

验证表 `:115` 构建验证行阻塞级别改为跟随 config:

| `phase_b_developer.framework_build_check` | 构建验证行为 |
|---|---|
| `enabled=false` (默认) | **跳过** — 非阻塞, 输出注明 `build: skipped (framework_build_check disabled — 构建归属: CI 或未配置)` |
| `enabled=true, mode=advisory` | 执行; 失败 → **警告** |
| `enabled=true, mode=blocking` | 执行; 失败 → **阻塞** |

验证流程 yaml (`:121-139`) 与成功/失败输出示例 (`:141-165`) 三态同步 (success / failed / skipped)。

### 4. Rule #6 基准 (Skill 变更触发)

- **branch-manager / branch-finisher SKILL.md 指令面变更** → 场景 1 AB 照跑 (零裁量): 定向用例须含 #231 原例「修 API key 列表分页」(期望 Branch/medium)、「API 接口变更」(期望 high)、`high_risk_keywords: []` 覆盖生效、`framework_build_check` 三态。`description` 不变 → 4b 不触发。
- **config-loader SKILL.md** 仅描述性 schema 新键 → substitute: `config-template-key-currency` 检查覆盖新键 (baseline-failing 结构化替代, 判据表第一行)。
- MODE_DECISION_LOGIC.md 为指令面参考文档, 随主面同改、同 AB 范围。

## rule6_note

```yaml
decision_table_row: 2   # 处方性·运行时指令面 (SOT §2 第二行)
scenario1: ab-results/2026-10-22-branch-risk-build-gate/ PASS   # 8 evals × 2 臂 16/16; 判别 4 精确翻转, 回归 4 零退化
scenario4b: not_required   # description (frontmatter) 零变动
exemption_reason: null    # 无豁免; config-loader 描述性 hunk 的 substitute = branch-manager/tests/test_risk_keyword_consistency.py (7 SC, 改前基线 6/7 红, 反事实自证) + config-template-key-currency 机械兜底
notes: >
  双 skill (branch-manager + branch-finisher) 指令面变更; AB 用 skill-creator 子代理双臂法
  (with=feature 树 / old=v1.77.0 archive 快照), 断言机械判分。附带修复: internal/MODE_DECISION_LOGIC.md
  与 internal/TEST_PRE_VALIDATION.md 双源同步 (后者由 eval-7 with 臂暴露的漂移)。
```

## Key Deliverables

- `aria/skills/branch-manager/SKILL.md` (风险检测节 + 新配置节)
- `aria/skills/branch-manager/internal/MODE_DECISION_LOGIC.md` (伪码同步)
- `aria/skills/branch-finisher/SKILL.md` (构建验证三态)
- `aria/skills/config-loader/SKILL.md` + 主仓 `config.template.json` (2 新键)
- Rule #6 场景 1 AB 结果 (双 skill) + `rule6_note`
- 发版 v1.77.1 (PATCH) 五文件同步面 + 主仓 gitlink/README badge/arch 版本行

## Constraints

| 类型 | 约束 | 来源 |
|------|------|------|
| 行为 | 修复不得放掉真高风险: 「breaking api」「API 重构」仍须 high | #231 建议 |
| 兼容 | 新 config 键 default null = 现行为 (除裸 api/核心 出表) — 无强制迁移 | 向后兼容原则 |
| 双源 | SKILL.md 与 MODE_DECISION_LOGIC.md 关键词表逐字一致 | 本轨 recon 发现 |
| 流程 | Level 3 全周期; AB 未过不 ship | Rule #6 |

## Impact

| 面 | 影响 |
|----|------|
| 消费方 | 所有经 branch-manager --mode auto 的项目 (误判面收窄); 用 branch-finisher 的项目 (构建门从恒阻塞 → 跟随 config, 默认跳过 = **行为放宽**, 与 Aria #95 开关本意对齐) |
| 版本 | aria-plugin v1.77.0 → **v1.77.1** (bug 修复 = PATCH) |
| 关联 | #230 A-F51 (整套积分制模型直判重设计) 不在本轨 — 本轨是窄修, 重设计另立 | #231 转述 |

## Open Questions (owner 批 spec 时一并裁)

无 — 设计按 #231 建议双取 (共现收紧 + config 覆盖), `核心` 出表为同类窄修。若 owner 对「核心」出表有异议, 可保留但降为 medium。
