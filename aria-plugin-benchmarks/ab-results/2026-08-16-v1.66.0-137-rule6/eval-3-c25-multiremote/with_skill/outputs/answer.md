# Phase C.2.5 — Multi-Remote Push Enforcement 执行流程

> 场景: PR 已合并到 `master` (aria 子模块仓), remote = `origin` (Forgejo) + `github` (mirror), 仓内 1 个子模块。
> 本 skill 段落 = phase-c-integrator §C.2.5 (v1.15.0+), 消费 `git-remote-helper`。

---

## 0. 前置断言 (跑任何 push 之前)

**0.1 合并必须是本地发生的。** C.2.5 的触发条件是「Phase C.2 合并成功 (master 已 fast-forward)」——
指的是**本地** master 已 fast-forward。如果这次 PR 是用 Forgejo Web UI / API 的 `Do: merge` 合的,
merge commit 只存在于 Forgejo 服务端, 本地 master 从未前进 ⇒ C.2.5 结构上不会被触发,
随后主仓 bump gitlink 就产生 orphaned gitlink (GitHub `clone --recursive` 断裂)。
所以第一步是断言而不是假设:

```bash
REPO=/path/to/aria            # 本次合并发生的仓 = aria 子模块根
BRANCH=master                 # ⚠️ 本项目主干叫 master, 不是 main
git -C "$REPO" rev-parse --abbrev-ref HEAD          # 期望: master
git -C "$REPO" merge-base --is-ancestor origin/$BRANCH HEAD   # 期望 rc=0 (本地领先或齐平)
```

不满足 → 不进 C.2.5, 报「服务端合并路径, 需本地重做 merge」并停。

**0.2 分支名不照抄缺省值。** 下面每一处 `<BRANCH>` 都取本项目主干的真实名字 `master`。
写死 `main` 在这里的后果和 #137 同形: `git ls-remote <remote> refs/heads/main` 零命中,
而 `git ls-remote` **零命中也返 rc=0** ⇒ 拿退出码判「推上去了吗」永远判成功 ⇒ 核验变摆设。

**0.3 读配置** (`.aria/config.json`, 经 config-loader):

| 字段 | 本次取值 | 来源 |
|------|---------|------|
| `phase_c_integrator.multi_remote_push.enabled` | `true` | 默认 |
| `...multi_remote_push.enforced_remotes` | `null` → 继承顶层 `multi_remote.enforced_remotes`; 仍空 → 自动发现 | skill 级为 null 时的继承链 |
| `...read_only_remotes` | `[]` | 默认 |
| `...fail_on_partial_push` | `true` | 默认 = 阻断 |

自动发现: `git -C "$REPO" remote` → `origin`, `github` ⇒ `ENFORCED_REMOTES=(origin github)`。

**0.4 helper 可用性探测** (决定是否降级):

```bash
test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md" && HELPER=1 || HELPER=0
```

不可用 → 走内联降级 (不重试、简化实现), **输出 schema 仍与 helper 路径一致**。

---

## 1. 快照 expected_sha + 枚举子模块

```bash
EXPECTED_SHA=$(git -C "$REPO" rev-parse HEAD)     # 例: e3f9c11a7b2d4e6f80c15a9d3b7e42f18c60d9ab
git -C "$REPO" submodule status --recursive       # 例: -a1b2c3d... sub1 (heads/master)
```

`EXPECTED_SHA` 是本轮唯一的比对基准 —— 后面每个 remote 的核验都拿它比, **不拿 remote 之间互比**
(两个 remote 都停在旧 SHA 时互比是"一致"的, 但一致地错)。

⚠️ 子模块口径消歧: `git submodule status --recursive` 只列**本仓内嵌套的**子模块。
题面「还有 1 个子模块」若指的是**外层主仓 (Aria) 把 aria 当子模块**, 那不属于 C.2.5 的推送矩阵,
而是 §4 的下游义务 (gitlink bump), 顺序上必须在两个 remote 都核验通过之后。
下面按「本仓内嵌 1 个子模块 `sub1`」执行, 两种口径都在本文覆盖。

---

## 2. Per-Remote Matrix Gating

对每个 `REMOTE ∈ (origin, github)` **独立**走 a→d 四步; 一个 remote 的失败不影响另一个已完成的 remote,
但会阻断**本 remote** 上主仓库那一步 (子模块没推上去就推主仓 = 制造该 remote 上的悬空 gitlink)。

### a. 子模块先推 (每 remote 内, 子模块 → 主仓 顺序不可换)

```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo="$REPO/sub1" --branch=master --remotes="$REMOTE"
```

`success` 判据取 helper 的严格定义: `exit_code == 0 AND post_remote_head == pre_local_head`
—— **不**靠 "Everything up-to-date" 之类文本匹配。

### b. 子模块任一失败 → 按失败优先级决策, 阻断则跳过本 REMOTE 的主仓推送

### c. 子模块全绿 → 推主仓

```bash
bash aria/skills/git-remote-helper/scripts/push_all_remotes.sh \
  --repo="$REPO" --branch=master --remotes="$REMOTE"
```

### d. 主仓推送成功 → **独立核验** (这一步才是判定成功与否的那一步)

```bash
python3 aria/skills/git-remote-helper/scripts/verify_post_push.py \
  --repo="$REPO" --branch=master \
  --expected-sha="$EXPECTED_SHA" \
  --remotes="$REMOTE" \
  --max-retries=3 --initial-backoff=2 --timeout=15
```

内部等价于对每个 remote 单独取真值再比:

```bash
git ls-remote "$REMOTE" "refs/heads/master"     # → "<sha>\trefs/heads/master"
```

**核验判据 (三条硬性)**:

1. **判据落在「解析出的 ref 名列表」上做精确字符串比对** —— `refs/heads/master` 是否逐字出现在输出的第二列, 且其 SHA == `EXPECTED_SHA`。
2. ⛔ **退出码只用来判「这次核验做成了没有」, 永不用来判「推没推上去」**: 零命中返 rc=0; `--exit-code` 无命中返 rc=2 (会被 catch-all 误分类成"核验失败")。
3. ⛔ **不用 glob / 前缀 / pattern**: `mast*` / `m[a]ster` / `maste?` 都会命中 `master`, 用近似名做判据等于放行一切。

**为什么必须独立核验而不是信 push 回执**: push 的退出码和回执**两个方向都会骗人** ——
假阴性 (实际推上去了却报失败) 会诱发误 force; 假阳性 / 半推会造成镜像分叉。
`ls-remote` 是从远端取真值, 是这里唯一可信的信号。

**复制延迟**: Forgejo/GitHub 有 10-30s 复制延迟, 所以是「立即 + 2s + 4s + 8s = 4 次 attempt」
(per-remote 时间上界 ≈ 74s @ timeout=15)。**4 次全部 match=false → 默认阻断**, 记 `possible race condition`,
不得自行放行。

**输出解码卫生** (自己解析 ls-remote 时): 用 `capture_output=True` 取 bytes + `surrogateescape` 解码,
⛔ 不传 `text=True` —— 远端返回非 UTF-8 stderr 时抛的 `UnicodeDecodeError` **不是 `OSError` 子类**,
会裸穿过 `(TimeoutExpired, FileNotFoundError, OSError)` 这类捕获元组; 出口再做
`s.encode("utf-8","replace").decode("utf-8")` 净化, 否则孤立代理码位会在下游 `json.dumps` 才炸。

---

## 3. 本次执行矩阵 (走一遍 + 失败分支)

### 3.1 全绿路径

```
expected_sha = e3f9c11

origin : sub1 push ✅ → main push ✅ → ls-remote origin refs/heads/master = e3f9c11 ✅ (attempt 1)
github : sub1 push ✅ → main push ✅ → ls-remote github refs/heads/master = e3f9c11 ✅ (attempt 2, +2s)
```

两个 remote 全部 `verified` ⇒ C.2.5 PASS ⇒ 进 C.2.6 / Phase D。

### 3.2 失败分支 (真实会遇到的三种)

**(i) github 子模块推送网络超时 —— 部分推送**

```
origin : sub1 ✅ sub2 —  main ✅ verify ✅ (已完成, 不回滚)
github : sub1 ❌ (network timeout) → 跳过 github 的主仓推送
```

处置: `fail_on_partial_push: true` 且 `github ∉ read_only_remotes` ⇒ **阻断**, 输出具体失败 remote + 修复命令:

```bash
git -C /path/to/aria/sub1 push github master
git -C /path/to/aria     push github master
python3 .../verify_post_push.py --repo=/path/to/aria --branch=master \
  --expected-sha=e3f9c11 --remotes=github
```

阻断态的性质要写清楚: **origin 已 ship, github 未 ship = 镜像分叉**, 此时
⛔ 不得继续 bump 外层主仓 gitlink (会造成 GitHub 侧 `clone --recursive` 断裂),
⛔ 不得对任一侧 force push 去"对齐"。修完重跑 C.2.5 即可 (幂等)。

**(ii) push 报成功但 ls-remote 4 次都不是 expected_sha**

判定 `verdict=blocked`, `reason=possible_race_condition`。不假设是延迟, 不重试到天荒地老 ——
先查是不是有人在同一窗口推了新 commit (`git ls-remote github refs/heads/master` 拿到的 SHA
是否是 `EXPECTED_SHA` 的后代): 是后代 → 别人已推进, 本地 fetch 后重判; 不是后代 → 分叉, 上报 owner。

**(iii) ls-remote 本身失败 (CF Access / 认证 / 网络)**

`exit 128` = auth_failed, 超时 = network_timeout。这两种是「**核验没做成**」,
与「**核验做成了但 SHA 不符**」是两类, ⛔ 不可混为一谈, 也 ⛔ 不可当成"推成功"。
重试只对 timeout 有意义 (`rc != 0` / `FileNotFoundError` 是确定性失败, 重试只是白等);
仍失败 → `verdict=blocked`, `reason=verify_failed`, 附人工核验命令。

**(iv) 子模块 detached HEAD**: 沿用 helper canonical (`detached_head: true` + 用 HEAD SHA 比较),
**警告但不阻断**。

### 3.3 失败优先级 (决策表, 按优先级从高到低)

| 条件 | 行为 |
|------|------|
| remote ∈ `read_only_remotes` | warning 降级, 继续 (最高优先级) |
| `fail_on_partial_push: false` + 非 read_only | warning, 继续 |
| `fail_on_partial_push: true` + 非 read_only (**本次默认**) | **阻断** + 输出修复命令 |

---

## 4. 收口顺序 (下游义务)

1. 两个 remote 全部 `verified` ⇒ C.2.5 PASS。
2. **此时才**允许外层主仓 (Aria) bump 到 aria 的 post-merge master SHA `e3f9c11`,
   并对主仓自身同样跑一遍双推 + 双核验。顺序颠倒 = orphaned gitlink。
3. 再进 C.2.6 (UPM milestone append, 若 `upm.milestone_driven: true`) / Phase D。

---

## 5. 输出

```json
{
  "step": "C.2.5",
  "verdict": "pass",
  "expected_sha": "e3f9c11a7b2d4e6f80c15a9d3b7e42f18c60d9ab",
  "branch": "master",
  "enforced_remotes": ["origin", "github"],
  "enforced_remotes_source": "auto_discovered",
  "helper_used": "git-remote-helper",
  "matrix": [
    {
      "remote": "origin",
      "submodules": [{"path": "sub1", "pushed": true, "detached_head": false}],
      "main_repo_pushed": true,
      "verify": {"match": true, "attempts": 1, "observed_sha": "e3f9c11a7b2d4e6f80c15a9d3b7e42f18c60d9ab",
                 "method": "ls-remote-exact-ref-name-match"}
    },
    {
      "remote": "github",
      "submodules": [{"path": "sub1", "pushed": true, "detached_head": false}],
      "main_repo_pushed": true,
      "verify": {"match": true, "attempts": 2, "observed_sha": "e3f9c11a7b2d4e6f80c15a9d3b7e42f18c60d9ab",
                 "method": "ls-remote-exact-ref-name-match"}
    }
  ],
  "blocked_remotes": [],
  "remediation_commands": []
}
```

workflow report 行:

```
  ✅ C.2.5 完成 → master @ e3f9c11 已推送并核验: origin ✅ (1 attempt) / github ✅ (2 attempts)
     子模块 sub1: 两 remote 均已推送
     核验方式: 每 remote 独立 git ls-remote + refs/heads/master 精确比对 (未采信 push 回执)
```

阻断态的对应行:

```
  ⛔ C.2.5 阻断 → github 未达成 parity (sub1 push network timeout)
     已 ship: origin @ e3f9c11 | 未 ship: github @ 4d1a0c8 (镜像分叉)
     ⚠️ 在 github 补推并核验通过前, 不得 bump 主仓 gitlink
     修复: git -C <repo>/sub1 push github master && git -C <repo> push github master && <重跑 C.2.5>
```

---

## 6. 一句话总结这一步在防什么

C.2.5 不是"再 push 一次"的冗余动作, 它防的是两件已实测发生过的事:
**(a) 只推 Forgejo 漏推 GitHub 造成的镜像分叉** —— 靠纪律防不住, 所以做成合并后的强制步骤;
**(b) 把 push 回执当成到达证明** —— 回执两个方向都会骗人, 所以判定必须落在
每个 remote 独立 `git ls-remote` 取回的、按 ref 名精确比对的真值上。
