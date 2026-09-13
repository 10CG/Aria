---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-13T17:47:25.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [qa-engineer]
---

## Findings

- [critical] testing/trigger-eval-openspec-archive.json (issue): 10 条 should-not query 在 v1/v2/v3 三轮、四臂 (new/old/negctrl/poscontrol) 全部组合下 trigger_rate 恒为 0/30, 从未观测到任何非零值。D2「全部 should-not query < threshold」这条门槛在本次实证里是一条只见 PASS、从未见过 FAIL 分支的判据, 其拒绝能力 (是否真的能抓到误触发) 尚未被证伪验证过, 不能算「地板守卫已验证有效」。
- [major] testing/RESULT.md §记分 (risk): 结论按 n=30 (10 query × 3 run) 算 Fisher 精确检验, 但 v3 原始数据显示 30 个 arm-query 单元里 27 个是全 0/3 或全 3/3 (仅 negctrl 3 条部分命中), 3 次同 query 的 run 并非独立样本 (伪重复/pseudo-replication), 真实独立单元是 n=10 (query 级)。按 query 级重算: new vs old 仍 p=1.0 (「零区分力」结论稳健, 未受伪重复影响), 但 new vs negctrl 从 RESULT.md 报的 p=8.3e-10 (n=30) 掉到 p=0.0031 (n=10 正确单元), 显著性余量骤降约 3 个数量级。D3 rule4 的「显著」门槛在更小、更现实的未来套件上可能因此不再稳过。
- [major] testing/RESULT.md §负控设计 (issue): 负控 8/30 命中并非均匀噪声, 而集中在 3 条含「核对/检查/校验+归档后结果或路径」语义的 should-trigger query (query index 5 = 3/3, index 7 = 2/3, index 9 = 3/3; 其余 7 条全 0)。说明负控只删净了「归档/OpenSpec/Spec」领域词, 未删净「收尾」「核对处理结果」这类被 eval set 里 3 条 query 复用的通用动作语义, 负控并非「干净」的地板参照。另外 RESULT.md 正文称「两条 query 3/3」, 漏计了 index 7 那条 2/3 命中, 与原始 json 数字不符 (应为 3 条参与, 8/30 = 3+2+3)。
- [major] documentation/proposal.md §D3 rule4 (issue): 「负控必须显著低于被评 description, 否则本轮数字作废」未给出「显著」的可操作判据 (无 alpha 值、无检验方法、无最小 query 数/最小差值), 且负控本身受上一条「未删净」问题污染。未来每个 skill 各自跑一次同规模小样本时, 边界情形下「显著」全凭执行者临场判断, 与 Rule #6 本条判据表要求的「零裁量」直接相悖 —— 这正是本 Spec 起草的原因之一 (照跑却测不到), 不应在新判据里重新引入同类模糊性。
- [major] architecture/proposal.md §OQ-4 (decision): 本变更同批修改 Aria 主仓 `CLAUDE.md` 十条不可协商规则之一 (Rule #6) + `standards` 子模块 SOT + `aria-plugin-benchmarks` 手册, 跨 3 个仓库/子模块, 且改的是约束全部 43 个 skill 未来合规判断的方法论核心治理文本。`LEVEL_GUIDE.md` 明文「跨模块条件 (满足任一): 影响多个子模块 → 自动提升为 Level 3」。自判 Level 2 (Minimal) 与该判据字面冲突; OQ-4 不应停留在「owner 裁」的开放问题而 Spec 正文同时已按 Level 2 结构 (只有 proposal.md, 无 tasks.md) 推进 —— 应先决 Level 再定稿产出物形状, 否则若 owner 事后裁定 Level 3, 需要回头补 tasks.md 重新过一轮审计。
- [minor] documentation/proposal.md §SC-3 (risk): 检索 `standards/conventions/skill-benchmark-exemption.md` 与 `AB_TEST_OPERATIONS.md` 全文, `rule6_note` 目前只是一句「须引用本规范」的自由文本要求, 没有既有结构化模板可供「加两栏」。SC-3 的反事实测试只验证「文字上能不能判出不合规」, 不要求任何机械闸门 (如 phase-a/phase-d 的 custom check) 校验两栏非空 —— 容易重蹈本 Spec 本身在解决的「自证合规、无人复核」问题 (呼应 Rule #10 精神)。
- [minor] testing/run_arms_v3.sh (risk): 三份运行脚本路径写死到本 session 的 scratchpad (`/tmp/claude-1000/-home-dev-Aria/e91a9d6a.../scratchpad`), RESULT.md 自陈「重跑时改 S=」; 并钉死插件缓存 hash `bb335391eb83` (随 skill-creator 插件更新会漂移, 项目已有 `feedback_plugin_cache_stale_via_stale_marketplace_clone` 先例) 与显式模型 `claude-fable-5-1` (未写弃用后备), 也未记录采样温度/随机种子。Key Deliverables 未包含一份参数化、可复用的运行脚本模板, 未来每个 skill 跑场景 4 时需照 D3 前置从散文重新拼装脚本, 存在实现漂移风险。
- [minor] documentation/proposal.md §SC-1 (risk): grep 判据允许「或 owner 定稿的同义句」, 但未定义由谁 / 如何判定「同义」; `CLAUDE.md`、SOT、手册三处未来由不同人各自编辑时核心句易措辞漂移, SC-1 有滑向「永红需人工复议」检查的风险。
- [minor] documentation/trigger-eval-openspec-archive.json (issue): 20 条 query 未经 owner 审阅 (OQ-3 待裁, skill-creator Step 2 明确要求 HTML 审阅), 但 proposal Key Deliverables T4 已计划将其「原样搬入」`ab-suite/trigger/`, 若 owner 后续要求改动套件内容, 已跑通的基线数字 (RESULT.md) 将与套件文本脱节, 需要重跑而非仅回填审阅意见。

## Verdict

FAIL — critical: 1, major: 4, minor: 4 (共 9 条)

## Vote

REVISE

## 复算记录

```bash
# 逐 arm/version 抽取每 query 命中数 (跨 v1/v2/v3, 四臂), 核对是否有全 0 / 全 3 零信息 query
python3 - <<'EOF'
import json, os
base = "/home/dev/Aria/aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline"
for version in ["v1-shared-root-4workers","v2-isolated-root-1worker","v3-isolated-root-1worker-neutral-name"]:
    for arm in ["new","old","negctrl","poscontrol"]:
        path = os.path.join(base, version, arm+".json")
        d = json.load(open(path))
        results = d["results"]
        should_trigger_hits = [r["triggers"] for r in results if r["should_trigger"]]
        should_not_hits = [r["triggers"] for r in results if not r["should_trigger"]]
        print(version, arm, "should_trigger=", should_trigger_hits, "should_not=", should_not_hits)
EOF
```
输出关键行 (v3, 有效轮): `new should_trigger=[3,3,3,3,3,3,3,3,3,3]`；`old` 同；`negctrl=[0,0,0,0,0,3,0,2,0,3]`；`poscontrol` 同 new/old；四臂 `should_not` 全部 `[0,0,0,0,0,0,0,0,0,0]`。三轮 (v1/v2/v3) should_not 全 0, 印证 finding 1。negctrl 命中集中在 index 5/7/9, 印证 finding 3。

```bash
# 按正确统计单元 (query 级, n=10) 重算 Fisher 精确检验, 对照 RESULT.md 按 run 级 (n=30) 的报告值
python3 - <<'EOF'
from scipy.stats import fisher_exact
# run-level (RESULT.md 口径): new 30/30, negctrl 8/30
print("run-level n=30 new vs negctrl:", fisher_exact([[30,0],[8,22]]))
# query-level (正确单元): new 10/10 触发 (trigger_rate=1.0); negctrl 触发 (>=2/3) 的 query 数 = 3 (index5,7,9)
print("query-level n=10 new vs negctrl:", fisher_exact([[10,0],[3,7]]))
# new vs old, 两种单元皆打平
print("run-level new vs old:", fisher_exact([[30,0],[30,0]]))
print("query-level new vs old:", fisher_exact([[10,0],[10,0]]))
EOF
```
结果: run-level new vs negctrl p ≈ 8.27e-10；query-level (正确单元) p ≈ 0.0031 —— 仍显著, 但余量降了约 3 个数量级。new vs old 两种单元下都是 p=1.0, 「对本次真实 description 变动零区分力」结论在纠正伪重复后依然成立, 未被推翻; 但 RESULT.md 报告的置信强度 (p<0.0001) 本身是统计口径错误的产物, 需要在 Spec/手册里改正措辞或改用正确单元重算。
