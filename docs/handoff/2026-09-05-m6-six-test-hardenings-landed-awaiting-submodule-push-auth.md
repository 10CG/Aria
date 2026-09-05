---
track-id: aria-2-0-m6-dispatch-input-delivery
owner-container: aria-runner-bot/bfe8285d
phase: B.2
status: active
updated-at: 2026-09-05T09:20:00Z
---

# Aria — Handoff (2026-09-05) — M6 输入投递 B.2 补强: 六处测试补强落地 + 两个真 bug (HCL 未声明 meta / S1_SCAN 键漂移)

> **一句话**: owner 确认「与双子星不冲突, 执行推荐 [1]」→ 重新认领 M6 轨 (旧 claim 已被对方 sweep 成 abandoned) → 按 08-27 账目核实的 partial 批逐条补强, **每条都跑了反事实 (撤销 fix 看新断言红不红)**, 7 条 TASK 从 in_progress 转 done, 随后 owner 裁定 TASK-005/023 各选 A (改条文/改论据, 不动代码与决定) 再转 2 条 → M6 账目 18/30 → **27/30** (剩 021 build / 022 freeze / 029 168h 跑, 全在门后)。补强途中抓出两个不是「测试缺」而是「生产会挂」的问题: (1) Layer 1 写的三个 Nomad meta 键 HCL 从未声明 ⇒ 每次自主 dispatch 都会被 Nomad 拒; (2) S1_SCAN 仍按内部 id 键候选而 seed 已改复合键 ⇒ 幂等守卫失效 + 复合键被覆写成裸数字。两处都修了并有反事实证据。**aria-orchestrator feature 分支 commit `9ec1fcc` 已由 owner 授权推送 (08:3x): origin + github 双推, 逐 remote `ls-remote` 均 MATCH 9ec1fcc。**
>
> ⭐ **最该留下的**: 08-27 recon 给 TASK-009 的补法写的是「断 FINAL_OUTCOME=ASSERTION_MISMATCH」, 实跑发现无 commit 在 Step 8 先判成 CLAUDE_NO_OP, 三条件函数只对 PENDING 生效 —— **补测试前先跑一遍真路径, 别照 recon 的预期断言写**, 否则写出来的是一条永远红的「假 RED」。

## §0 入口 (新 session 优先读)

1. `/aria:state-scanner`。主仓 master 在 `a259ebf` + 本 commit; aria `7dd0135` (v1.69.1) / standards `cc864ee` / aria-orchestrator gitlink仍 `237045a` (master, **有意不 bump**: M6 代码在 feature 分支, 合并门未开)。
2. **aria-orchestrator `feature/m6-dispatch-input-delivery` = `9ec1fcc`** (基于 `1ee225a`), owner 授权后已双推: origin `1ee225a..9ec1fcc`, github 新建分支; 两端 `ls-remote` MATCH。
3. 本容器 claim `aria-2-0-m6-dispatch-input-delivery` phase B **active** (2026-09-05T07:20Z 重新认领, session `s-00ec@0720`, push_success=true)。旧 claim `s-2cea@1704` 已被对方 `--sweep-stale` 标 abandoned (心跳停在 08-29) —— 这是机制正常工作, 不是冲突。
4. 双子星 (`simonfish/023236f2`) 在飞: `carry-spec-drafter-path-rule5-drift` (PR #194 已合, 剩 claim 释放) + 母 Spec `a1-entry-claim-duplicate-work-guard` B.1。**本容器不接**。

## §1 已完成 (2026-09-05, UTC)

| 时间 | 事件 | 证据 |
|------|------|------|
| 09:1x | **owner 两裁定 (005 选 A / 023 选 A)**: AC-7「YAML-safe 转义」→「控制字符剥离」(proposal §A.4/AC-7 + yaml + AD 风险 5) + unit 3 条锁定 (30/30); AD-M6-10 背景 1 + Alternatives D 论据勘正 (heavy 卷实为共享 virtiofs over NFS, 决定不变; proposal §Alternatives D 同步) → tasks 27/30 | aria-orchestrator `0227ff3` (feature, **本地待授权推**) + 主仓本 commit |
| 06:5x | `/aria:state-scanner` 两轮: 第一轮发现主仓分叉 (本地 09-03 收尾 commit 从未推出 + 远端多 4 commit), rebase + latest.md 多 track 合并 + 勘正 09-03 handoff §0/§7 同步声明 → 双推 `55b7446` 两端 MATCH; 第二轮远端又进 3 commit (对方 v1.69.1 PR #194 已含我的 55b7446) → FF 到 `a259ebf`, 14/14 check 全绿 | 主仓 `55b7446` / `a259ebf` |
| 07:20 | 冲突核实: origin coordination ref 无对方 active claim; 对方在飞分支只在主仓/aria/standards; aria-orchestrator feature 分支最后一次改动是本容器 07-04 → `phase1_gate --phase B --mode advisory` outcome=passed | claim `s-00ec@0720` |
| 07:2x | 基线: initial-sh-unit 23/23, initial-sh-integration 5/5, compute-assertions 8/8, Layer 1 unittest 946 OK | /tmp 日志 (本机) |
| 07:3x | **TASK-002** scenario 6 (缺失/空/非 YAML 三 die) · **TASK-003** scenario 1 +3 断言 (body/title/files_hint 真进 claude prompt, stub claude 落盘 argv) · **TASK-007** scenario 7 (空 expected_changes → unknown/ASSERTION_MISMATCH/exit 1) · **TASK-008** 换掉重言式断言 · **TASK-009** scenario 8/9 + unit 4 例 | `9ec1fcc` |
| 07:3x | 五组反事实 (撤销对应 fix 后跑套件): TASK-008 → 2 红 / TASK-003 body → 1 红 / files_hint → 1 红 / TASK-002 → 1 红 / TASK-007 → 5 红; 每组后 `git diff` 确认已还原 | 见 commit message |
| 07:4x | **TASK-013** HCL `meta_optional` +TARGET_REPO/BASE_BRANCH/FILES_HINT (`nomad job validate` 过) + inventory guard M6 三键 + **结构性 fence** (extension.py 全部 extra_meta 键 ⊆ HCL 声明); 反事实去 FILES_HINT → 2 红 | `9ec1fcc` |
| 07:5x | **TASK-020** `_compose_dispatch_issue_id` helper, seed 与 `_handle_s1_scan` 共用; 新测 6 例 (id≠number 夹具) 修前 3 FAIL + 3 ERROR, 修后 6 过; Layer 1 全套 **955/955** | `9ec1fcc` |
| 08:0x | tasks.md 7 条 `[ ]`→`[x]` (25/30) + detailed-tasks.yaml 7 条 done + 本 handoff + latest.md; aria-orchestrator 切回 master 停泊 (gitlink 不动) | 本 commit |

## §2 未完成 / Carry-forward

- ✅ ~~owner 授权推送 9ec1fcc~~ 已完成 (08:3x, 双端 MATCH)。TASK-021 build 现在能打进这批修复 (含 HCL 三键)。
- 🔴 M6 门链不变: TASK-021 build (owner 触发 `/aether:aether-build-container`, 顺序疑问未决: feature 先 build 供 dogfood vs 合并后 build) → TASK-022 freeze 同批 → TASK-029 = Blocker 4 + 022。
- 🔴 Blocker 4: SilkNode #1058 已 7 天无回复 (20 tok/s 越 60s timeout)。建议 owner 内部渠道催或授权 nudge。
- ✅ ~~两条待 owner 裁定的 partial~~ 09:1x owner 裁定: TASK-005 选 A (改条文对齐实现) / TASK-023 选 A (只改论据不改决定), 已落地 `0227ff3` + 主仓同步; DEC-20260702-001 为日期化决策记录未改 (其 §D 行对 light-1 的判断仍被引用为写方证据)。
- 🔴 **owner 授权推送** aria-orchestrator feature `0227ff3` (在 9ec1fcc 之上, 仅 AD 文档 + unit 测试) → origin + github, 推后逐 remote ls-remote。
- 🟡 TASK-009 recon 补法勘误已记进 tasks.md 注释 (ASSERTION_MISMATCH → 实况 CLAUDE_NO_OP), recon note 本身是 08-27 快照不改。
- 🟡 承前: memory 索引 24.14KB 贴上限; #182 / #184 / #147。

## §3 关键风险 / 已知陷阱

- **TASK-020 修法改了 S1_SCAN 的候选键**: 既有 8 条 S1_SCAN 测试 (`_make_issue` 只带 `id` 无 `number`) 靠 helper 的「无 number 回退 str(id)」保持绿; 真 Forgejo 载荷恒有 `number`, 生产走复合键分支。若将来有人把回退删掉, 那 8 条会一起红 —— 那是信号不是噪声。
- **结构性 fence 靠正则读 extension.py**: 只认 `extra_meta["KEY"] =` 与 dict 字面量 `"KEY":` 两种写法, 已加自检 (必须看见 ISSUE_URL/TARGET_REPO/REWORK_MODE 否则测试自己红) 防真空绿。改用别的写法 (如 `extra_meta.update({...})`) 需同步扩正则。
- stub claude 现在把 argv 写到 `$ws/claude-prompt.txt`; 若哪天 initial.sh 改成 stdin 喂 prompt, scenario 1 的三条 TASK-003 断言会红 —— 也是信号。
- 反事实全部在真文件上 sed 后 `cp` 还原, 每组末 `git diff --stat modes lib` 为空已核; 但这套手法没有落成脚本, 下次重跑要手工。

## §4 实战教训 (memory 沉淀候选)

1. **补测试前先跑真路径再写断言** (TASK-009 recon 预期 ≠ 实现顺序)。候选 memory: `feedback_write_red_assertion_from_real_run_not_from_recon_expectation`。
2. **「测试缺」清单里常混着「生产会挂」**: TASK-013/020 的缺口表面是守卫没扩, 实质是 dispatch 会被拒 / 键会被覆写。partial 批不要当纯补测试活排优先级。
3. 对方容器的 `--sweep-stale` 会把本容器 6 天没心跳的 claim 标 abandoned —— 长门等待期间 claim 会自然过期, Phase B 再入口重新 `phase1_gate` 即可, 不必视为被抢。
4. secret-guard 会拦 heredoc 里出现 `os.environ`+`.env` 形态的 python 脚本 (误报), 走 Write 落脚本文件再执行 (memory `feedback_secret_guard_ack_reason_first_token_8_chars` 已有同类建议, 本次再撞一次)。

## §5 同步状态 (收尾时)

```
[main]              master = a259ebf (+本 commit) | 推后 origin/github 逐 remote ls-remote 核验 (见 §7)
[aria]              gitlink 7dd0135 (v1.69.1, 双子星 09-04 ship) | [standards] cc864ee | 均 = 远端 master
[aria-orchestrator] gitlink 237045a (master, 不动) | feature/m6-dispatch-input-delivery 本地 0227ff3 (9ec1fcc 已双推 MATCH; 0227ff3 待授权推)
[coord ref]         claims/bfe8285d/s-00ec@0720 (aria-2-0-m6-dispatch-input-delivery, phase B) active, 已推
[tests]             initial-sh-unit 30/30 | initial-sh-integration 9/9 | compute-assertions 8/8 | Layer 1 955/955 (skipped 4)
```

## §6 Next session 入口 + 优先级建议

`/aria:state-scanner`。

1. **owner 一句话**: 授权推 aria-orchestrator feature `0227ff3` (子模块, 双推 + ls-remote)。
2. ~~两裁定~~ 已裁已落地 (005 A / 023 A)。
3. 不等人的活已做完; 剩余 M6 任务全在门后 (021 build → 022 freeze → 029)。
4. 承前: 催 #1058 / 插件缓存已到 1.69.1 (转绿, 不再是事)。

**结构化 carry-id**:
- `{id: aria-2-0-m6-dispatch-input-delivery, desc: "B.2 补强 9ec1fcc 已双推 + 裁定落地 0227ff3 待授权推; 账目 27/30; 剩 021 build → 022 freeze → 029 (Blocker4 #1058)"}`

## §7 提交清单

- aria-orchestrator `feature/m6-dispatch-input-delivery`: `9ec1fcc` test(m6) 六处测试补强 (6 文件, +404/-16) — owner 授权后双推, origin MATCH / github MATCH (新建分支)
- aria-orchestrator `feature/m6-dispatch-input-delivery`: `0227ff3` docs(m6) owner 两裁定落地 (AD-M6-10 勘正 + unit 3 锁定) — **本地, 待授权推**
- 主仓: `94db971` (补强账目 25/30) → `a2cf0e4` (9ec1fcc 推送回填) → 本 commit (裁定落地 27/30; proposal/tasks/yaml/本 handoff/latest.md) — 均双推 + ls-remote

## Cross-references

- 缺口来源: `.aria/notes/2026-08-27-m6-task-ledger-recon.md` (逐条明细) + `docs/handoff/2026-08-27-m6-ledger-recon-agent-team.md` §2
- 上一份本轨 handoff: `docs/handoff/2026-09-03-m6-pat-closure-and-token-governance.md`
- Spec: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/{proposal.md,tasks.md,detailed-tasks.yaml}`
