# dogfood 执行记录 — state-scanner-stale-refs-false-parity Phase 4 (v1.62.0)

> **为什么有这份文件**: 归档门的产物分类器 `_ARTIFACT_PATH_TOKEN_RE` 硬编码只认 `ab-results|ab-suite` 路径, 任何非-AB 的 dogfood 声称**结构上恒不可 auto-link** ⇒ 恒 warn (该局限已由姊妹 spec 记为 aria-plugin #114)。本文件是可读产物, 按姊妹 spec `../2026-07-19-state-scanner-openspec-collector-false-green/dogfood-evidence.md` 先例补写。
>
> ⚠️ **本文件曾被 ack 引用但从未创建** —— post_planning R2 (N-1) 抓出: 归档 frontmatter 的 `unverified_ack_reason` 两次引用它作为 3 条 dogfood 声称的核心论据, 而文件不存在 (`git log --all` 零提交)。即用一个不存在的产物去 ack 掉「产物缺失」。这是本 session 第四次同型「提前宣称」, 且发生在专门修复前两次的那个 commit (`f6eea1d`) 里。本文件为补实。

## 1. 执行环境

- 仓库: `/home/dev/Aria` (主仓) + `aria` / `standards` / `aria-orchestrator` 三个子模块
- 主仓 remotes: `origin` (Forgejo) + `github`; `aria` 同; `aria-orchestrator` 仅 `origin`
- 执行者: 主 loop 亲验 (非 agent 转述), 命令 `python3 aria/skills/state-scanner/scripts/scan.py --output <path>`

## 2. 实测输出 (Phase 4 实施前后各一次)

### 2.1 收口过程中 (主仓落后并发 bot 4 commit 时)

```
overall_parity: False | has_unreachable: False | pending_push: True

主仓 remotes:
  github   parity=behind   grade=fresh fetch_ok=true method=local_refs
  origin   parity=behind   grade=fresh fetch_ok=true method=local_refs

子模块:
  standards          github/origin  parity=unknown  grade=fresh reason=detached_head
  aria               github/origin  parity=ahead    grade=fresh reason=None
  aria-orchestrator  origin         parity=unknown  grade=fresh reason=detached_head

gitlink_integrity:
  github/standards          status=ok
  github/aria               status=ok
  github/aria-orchestrator  status=no_matching_remote
  origin/standards          status=ok
  origin/aria               status=ok
  origin/aria-orchestrator  status=ok

errors: []
```

**这一份是本 spec 能力的自证**: `overall_parity=False` 是**诚实的** —— 实测主仓确实落后 `origin/master` 4 个 commit (并发 bot 在本 cycle 期间 ship 了 v1.61.0)。`git rev-list --count HEAD..origin/master` = 4 独立核实。事故形态 (陈旧 refs 下谎报 equal) 未复现。

### 2.2 收尾后 (跨仓落地完成)

```
custom checks: 8/8 pass, 0 fail
overall_parity: True | enforced_remotes_resolved: ['github', 'origin'] | excluded_read_only: []
git clean: True | ahead/behind: 0/0 | errors: 0
active specs: 6 | pending_archive: 0 | archived: 128
```

`overall_parity` 从 False 诚实转 True —— 转变的原因是真实状态改变 (push 完成), 不是判据松动。

## 3. 逐 AC 覆盖状况

| AC | 内容 | dogfood 覆盖 | 判定 |
|----|------|-------------|------|
| **AC-17** | detached-HEAD 子模块 + 全 remote 真 equal ⇒ `overall_parity` 仍 true | `standards` / `aria-orchestrator` 均为 detached-HEAD, 2.2 中 `overall_parity=True` | ✅ 正面验证 |
| **AC-11** | 同 AC-17 (防 R3-C5 恒红) | 同上 | ✅ 正面验证 |
| **AC-16** | 子模块 github 镜像若落后 ⇒ **必须报出来** | **未获正面验证** — 见 §4 限制 | ⚠️ **vacuous** |
| gitlink 诚实性 | 不误报 orphan | `aria-orchestrator` 无 `github` remote ⇒ 报 `no_matching_remote` 而非 `orphaned` | ✅ 正面验证 |
| F5′ 可见性 (I2) | 裁决集可读 | `enforced_remotes_resolved: ['github','origin']` 实见于输出 | ✅ |
| AC-5 检测集 | 不硬编码 origin, 跟随 enforced 集 | 检测集实测 = `['github','origin']` | ✅ (仅检测维度, 裁决维度未实现 — 见归档 proposal C-1 段) |

## 4. 限制 (诚实记录, 不冒充覆盖)

### 4.1 AC-16 正向腿实测 vacuous

AC-16 要求「子模块的 github 镜像若落后 ⇒ 必须报出来」。**本次 dogfood 期间三个子模块的 github 镜像均未落后** (全 `ok` 或 `no_matching_remote`), 因此该 AC 的**正向腿 (真落后必报) 没有被触发过**, 属 vacuous pass。

这一点有实际分量: Aria #165 (「GitHub 镜像漏推第三次复发」) 至今 **open**, 说明该场景在生产里真实发生过三次, 而本次 dogfood 恰好没撞上。**不得据本文件声称 AC-16 已获验证。** 要补正面验证需要构造 fixture (子模块有一个只存在于 remote-A 不存在于 remote-B 的 commit, 主仓 gitlink 指向它) —— 该 fixture 未构造。

### 4.2 未覆盖的场景

- **跨进程同仓并发** (两个终端同时 scan): 未构造。spec 已写明为「已知可接受降级」(依赖 git 自身 ref lock; 争用 ⇒ `fetch_ok=false` ⇒ 降级 unknown, 假红方向)。
- **read_only / enforced 白名单的真实配置**: 本仓 `.aria/config.json` 未设这两个键 (走 auto-discover 全部 remote), 故 policy 过滤在真实 dogfood 中是 **no-op**。该路径的验证完全依赖 mocked 单测 (`TestEnforcedPolicyGovernsVerdict`, 含可证伪性验证: 回退生产调用点后 5 条转红)。
- **AC-15 防饥饿**: 本仓 6-8 腿, 未触及 deadline 砍腿; 且 k_eff=k_min 冷启动 (task 3.16 DEFERRED)。

## 5. 全量测试

- `aria/skills/state-scanner/tests/run_tests.py`: **1250 passed** (起点 1232, 净 +18)
- `aria/skills/session-closer/tests`: **62 passed** (含 post_planning R1 抓出的红测试修复 + 负控)
- 跨全部 12 个 `skills/*/tests` 目录扫描: `issue-triage` / `tdd-enforcer` 两处红为**先前就红**的环境问题 (缺 `pytest`, 在基线 `55ab21d` 上同样红), 与本 cycle 无关
- `validate_schema_doc.py`: 绿

> ⚠️ 测试数声称也曾出错: 文档原写「1219 → 1248」, post_planning R1 (qa-engineer) 双端实跑 + diff 计数交叉验证证明起点是 **1232**。已更正。
