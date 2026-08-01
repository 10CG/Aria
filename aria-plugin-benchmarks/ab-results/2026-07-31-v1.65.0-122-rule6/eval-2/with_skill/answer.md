# Phase C C.2 合并冲突处理推演 — feature/oauth2-social-login → main

> 产出形态: descriptive (按场景前提推演, 未实跑任何 git 命令)
> 依据: phase-c-integrator SKILL.md v1.65.0 (C.1-C.2 编排 + C.2.4/C.2.4.5/C.2.5 gate 链) + branch-manager 职责边界

---

## 1. 冲突定位: 它发生在流程的哪一环

按 SKILL 的层次边界 (§C.2.4 Naming 命名空间澄清):

| 层 | 步骤 | 职责 |
|----|------|------|
| branch-manager (implementation tier) | C.2.1 sync rebase → C.2.2 push → C.2.3 create PR → C.2.4 wait-approval → C.2.5 merge | 实际 git 操作 |
| phase-c-integrator (orchestrator tier) | C.2.4 pre-merge gate → C.2.4.5 submodule gate → C.2.5 multi-remote push | 三态判定与放行 |

`backend/config/settings.py` 的冲突最可能在两个时点暴露:

- **时点 A — C.2.1 sync rebase**: branch-manager 在 push 前把 feature 分支 rebase 到最新 main, rebase 中 settings.py 冲突。这是最常见形态 (main 在本分支开发期间被其他 PR 推进了)。
- **时点 B — merge API call**: PR 已建, gate 已 green, Forgejo/GitHub merge API 返回 "merge conflict, not mergeable"。语义相同: feature 分支落后于 main 且改了同一文件。

两个时点的处置收敛到同一条恢复路径 (下 §3), 差别只是时点 B 需要额外把已过的 gate 判定作废重跑 (§4)。

## 2. Graceful 的第一原则: 停下, 不自作聪明

对照 SKILL 错误处理表 (`推送失败 | 远程冲突 | 提示拉取最新代码`) 与 Rule #10, 冲突瞬间的行为:

1. **立即停止 C.2 流程** — 不调用 merge, 不 force push, 不动 main。phase-c-integrator 返回 failure 态, `success: false`, 保留已完成步骤的输出 (C.1 的 commit_sha 仍有效)。
2. **不自动解决冲突** — 尤其 settings.py 这类配置文件:
   - OAuth2 social login 变更几乎必然在 settings.py 新增配置块 (OAUTH2_PROVIDERS / client_id / redirect_uri / INSTALLED_APPS 追加等); main 侧冲突意味着别的变更也动了同一区域。配置合并错误是运行时炸弹 (import 顺序、middleware 顺序、双方各加了同名 key), 不是文本层 `ours/theirs` 能裁决的。
   - **Rule #7 secret 卫生**: 处理 settings.py 冲突时, 若冲突块附近出现疑似 secret 字面量 (client_secret 硬编码), 冲突展示与后续命令输出不得把 secret 值回显进 chat 可见通道; 同时这本身要标记为独立问题 (secret 不该硬编码在 settings.py, 应走环境变量/secret store)。
3. **输出结构化冲突报告**, 让人/上层 workflow 有完整决策信息:

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION (BLOCKED)                 ║
╚══════════════════════════════════════════════════════════════╝

  C.1 完成 → Commit: <sha> (feature/oauth2-social-login)
  C.2 阻塞 → 合并冲突

  冲突详情
  ─────────────────────────────────────────────
  branch:    feature/oauth2-social-login → main
  冲突文件:  backend/config/settings.py (1 文件)
  时点:      C.2.1 sync rebase (或 merge API not-mergeable)
  原因:      main 在本分支开发期间推进, 双方修改了 settings.py 同一区域

  建议路径: 本地同步 main → 手工解决 settings.py → 重跑验证 → 重新推送
```

## 3. 恢复路径 (我会引导执行的命令序列)

前提: 工作区干净 (C.1 已提交)。若有未提交改动先处理, 且**不用 `git stash pop` 走 race recovery** (stash+rebase+pop 有 conflict 二次叠加的坑, memory 已记)。

```bash
# (1) 取最新远程状态
git fetch origin

# (2) 站在 feature 分支, rebase 到最新 main
git checkout feature/oauth2-social-login
git rebase origin/main
# → 停在 backend/config/settings.py 冲突

# (3) 手工解决 settings.py — 逐块审读, 不整段取舍:
#     - 双方新增的配置块通常都要保留 (OAuth2 块 + main 侧新增块并存)
#     - 注意 list 型配置 (INSTALLED_APPS / MIDDLEWARE) 的顺序语义
#     - 检查双方是否引入同名 key → 语义裁决, 拿不准升级问人 (owner)
#     - 冲突标记 <<<<<<< ======= >>>>>>> 清干净
git add backend/config/settings.py
git rebase --continue

# (4) 冲突解决 ≠ 集成完成 — Phase B 的 test_results 已作废 (基底变了),
#     必须在新基底上重跑测试套件, 重点覆盖配置加载 + OAuth2 flow
<项目测试命令>   # 例: pytest backend/

# (5) rebase 改写了历史, 重推用 force-with-lease (非裸 force):
#     且遵守 memory: force-with-lease 前先做前置核验 (确认远程分支无他人新提交)
git push --force-with-lease origin feature/oauth2-social-login
```

分叉路线说明: 若项目策略偏好 merge 而非 rebase (`git merge origin/main` 到 feature 分支), 冲突解决与验证义务完全相同, 只是不需要 force push。选择跟随 `.aria/config.json` / 项目既有分支策略, 不临场发明。

## 4. 解决后: gate 链必须重走, 不得沿用旧判定

这是 "graceful" 里最容易被省掉、但 Rule #8 / Rule #10 不允许省的部分。rebase/重推后 PR 的 head SHA 变了, 此前任何 gate 结果对新 SHA 无效:

- **C.2.4 Pre-Merge Precondition Gate 重跑** (`pre_merge_gate.enabled: true` 默认):
  - backend resolution → path coverage 评估 (v1.65.0, `backend/config/settings.py` 属后端代码路径, 预期 `decision=covered`, 走正常 CI wait, 不会落 not_applicable 短路)
  - 查本 PR 新 SHA 的 CI: 刚重推必然 `pending` → verdict=wait → 进 wait+retry (退避 `[30,60,120,300,300]`, 上限 30 min)
  - 查 main in-flight: 若 main 正有 CI run (很可能, 因为 main 刚进了引发冲突的那个变更) → 同样 wait, 等它落地
  - CI passing + main 无 in-flight → green
- **pre_merge audit** (仅当 `audit.enabled=true` 且 checkpoint 非 off): PR diff 变了 (含冲突解决 hunk), 审计基于新 diff 重跑。
- **C.2.4.5 Submodule Gate**: 本冲突不涉及 submodule pointer, 但 gate 照常执行 (`mode=block` 默认) — 尤其 rebase 后要确认没有无意把 gitlink 带回旧值 (rebase 是 pointer regression 的经典引入路径, 正是这个 gate 存在的理由)。
- gate 全 green → branch-manager merge → **C.2.5 multi-remote push** (双推 + 逐 remote `ls-remote` SHA 核验, 不信 push 回执) → C.2.6 (如 `upm.milestone_driven` 开启)。

## 5. 明确不做的事 (反面清单)

- 不 `git push --force` 裸推, 不直接 push main 绕过 PR。
- 不用 `-X ours` / `-X theirs` / checkout 单侧整文件了结冲突 — settings.py 双方新增大概率都要留。
- 不因 "只是解决了个冲突" 跳过测试重跑或任何 enabled gate (Rule #10: enabled 闸门不由 AI 临场豁免; "变更小" 不是白名单里的豁免类)。
- 不在 Forgejo Web UI 上点 "resolve conflict" 编辑器草率了事 — 冲突解决要在本地做, 能跑测试验证 (且本项目多远程约束下, 子模块类仓库本就禁服务端合并)。
- 不把 wait 态当 fail: main in-flight CI 是 wait+retry 路径, 不是阻断报错。

## 6. 最终输出 (冲突解决并完成合并后)

```yaml
success: true
steps_executed: [C.1, C.2]
recovery: conflict_resolved_rebase   # 本次异常路径留痕
results:
  C.1:
    commit_sha: "<原 commit>"
  C.2:
    pr_number: <N>
    pr_url: "https://..."
    pre_merge_verdict: "green"
    pr_ci_status: "passing"
    path_coverage: {decision: "covered", ...}
    submodule_gate: "pass"
context_for_next:            # 交给 phase-d-closer
  commit_sha: "<merge 后 SHA>"
  pr_url: "https://..."
  notes: "settings.py 冲突经 rebase 手工解决, 测试于新基底重跑通过"
```

若冲突解决中发现语义级歧义 (双方对同一配置 key 意图相反) 而无法自行裁决 → 保持 blocked, 升级给 owner 决策, 并把裁决点写进 handoff — 这属于 "AI 自作主张的流程判断必须留痕请复议" 的范畴。
