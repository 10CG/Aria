A.1 的认领必须**早于投入** —— 它要回答的是「远端是不是已经有人在做同一件事」, 起草完再补, 记录的就只是既成事实了。下面三问逐条回答, 不跑命令。

---

## 【1】`--raw-track-id` 的实参

逐字写出来:

```
add-oauth-login-1a2b3c4d
```

分段来源:

| 段 | 值 | 从哪来 |
|---|---|---|
| `<spec-slug>` | `add-oauth-login` | 本 Spec 目录 `openspec/changes/add-oauth-login/` 的**目录名, 逐字取**。不要自己预归一 (大小写 / 连字符 / 去前缀), 归一是 CLI 内部的事 |
| 分隔符 | `-` | 拼接格式就是 `<spec-slug>-<container_uuid>` |
| `<container_uuid>` | `1a2b3c4d` | `~/.aria/container-id` 里的 **`uuid` 字段** |

**这里唯一的坑**: 夹具里同时有 `label: devbox-A1-very-long-label`。**不能取 label**。label 是装饰性的, 改一行 label 就把整条 track-id 换掉 —— 旧 claim 立刻变僵尸, 新 claim 又跟协作方对不上, 认领机制当场失效。所以只认 `uuid` 字段。

放进完整命令 (以候选 A 那份为例):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "add-oauth-login-1a2b3c4d" \
  --phase A.1 --mode advisory \
  --linked-issue "10CG/Aria#174" \
  --include-terminal \
  --repo-path "<Aria 主仓根>"
```

跑之前先做幂等 check: coordination ref 内按 `(container_id, session_id)` 定位 `claims/<container>/<session>.yaml`, **存在且 `status == active` 就跳过**, 不重复 acquire。

另外分清路径: 如果你是经 `phase-a-planner` 委派进来的, 认领上游已经做过了; 本块只在 (a) 未经 planner **直接调用** spec-drafter, 或 (b) planner 因 skip 条件没走到认领 —— 这两种情况下生效。直调路径没有 Level 判定, 所以**没有 Level 1 例外**, 简单需求也得认领。

---

## 【2】三份 proposal 各自传不传 `--linked-issue`

先说取法, 因为它是**两阶段**的:

- 若 `${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/linked_issue_field_probe.py` **存在** → 实参 = `python3 <该脚本> --emit-arg <本 Spec 的 proposal.md>` 的 stdout; **stdout 为空 ⇒ 整个参数省略**。
- 脚本不存在 → 按字段 Spec `linked-issue-field-availability` §3 的 E0–E6 手工判。

下面是手工判分支的结论 (probe 在的话结论应与之一致)。判据 (E6): 只有**字段行冒号后首个 code span 的第一个元素**形如 `<org>/<repo>#<n>` **且非哨兵**时才传。

| 候选 | 字段值 | 传吗 | 实参 | 依据 |
|---|---|---|---|---|
| **A** | `` `10CG/Aria#174` `` | **传** | `--linked-issue "10CG/Aria#174"` | inline code span, 首元素严格是 `<org>/<repo>#<n>`, 非哨兵 |
| **B** | `` `none` `` | **不传 —— 省略整个参数** | 无 | `none` 是**哨兵** (它本身是合规写法, 表示「已核实无关联」), 但不是 issue 标识 |
| **C** | `[#174](https://forgejo.10cg.pub/10CG/Aria/issues/174)` | **不传 —— 省略整个参数** | 无 | markdown 链接形 ⇒ 判 `NO_TOKEN` |

三处最容易做错的地方:

1. **B 绝不能写成 `--linked-issue "none"`**。任何非空字符串都 truthy —— 两份毫无关系的 Spec 只要都老实写了 `none`, 传进去就会**互相命中**, 报出一个纯属虚构的碰撞。哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 一律省略整个参数, 没有例外。

2. **C 不要自己去「把链接解析开」**, 凑出 `10CG/Aria#174` 再传。机械 check 是零裁量的, 链接形就是 `NO_TOKEN`。正确处置是回头把 C 的字段**改写成合规写法** `` `10CG/Aria#174` `` (行首无空白, `>` 后恰一个空格, 字段名两侧各两个星号, ASCII 冒号), 改完它就变成 A 那一档; 而不是在命令行上替它打补丁 —— 那样文档仍然不合规, 只是这一次跑通了。

3. **省略参数的后果, 读输出时要对上**。B / C 这两轮因为没传 `--linked-issue`, 结果里 `linked_issue_overlap` 这个键会**缺席**, 措辞只能是「本轮未检测」, **不是「无碰撞」**。四态两两不同, 别压平:

   | 信号 | 措辞 |
   |---|---|
   | 键**缺席** | 「本轮未检测」 |
   | `linked_issue_overlap == []` | 「无碰撞」 |
   | `unknown_schema_claims > 0` | 「已检测到 N 条无法解析的 claim —— 存在性已确认、内容未知, **按存在处理**」 |
   | `linked_issue_overlap == null` 且 `linked_issue_overlap_error` 非空 | 「**未能核实**, 建议重试」 |

   最后一行绝不可渲染成「无碰撞」—— 零证据不是正证据。同理别用 `.get(key, [])` / `.get(key, 0)` 去读这几个键, 那正好把四态压成一态。

> 顺带一提: 认领是**每份 Spec 一条 track**。【1】里那串 track-id 只对 `add-oauth-login` 这一份成立。如果 A/B/C 其实是三个不同的 Spec 目录, 就要各自拼各自的 slug、各跑一次认领; 如果它们是同一份 proposal 的三种候选写法, 那就是选一种写进去, 只有一条 track。

---

## 【3】起草到一半决定放弃这个方向

跑 release, 并且 `--raw-track-id` 必须是**同一串**:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/release_gate.py" \
  --raw-track-id "add-oauth-login-1a2b3c4d" \
  --status abandoned
```

(SKILL.md 里明写的形态是 `release_gate.py --raw-track-id <同一串> --status abandoned`; 脚本与 `phase1_gate.py` 同目录。)

要点三条:

- **不 release 就留下一条永不释放的僵尸 claim**。后面真想做这件事的容器 (可能就是你自己下一个 session) 会被它挡住, 或者误判成「已经有人在做」而放弃 —— 认领机制的收益直接变成净负债。
- **track-id 必须逐字同一串**。重新拼一遍时若手滑归一了 slug、或换成了 label, release 的就是另一条 track, 原 claim 照样挂着。
- 顺带记住另一条退出义务, 它和「放弃」很容易混: **Spec 目录改名 ⇒ release 旧 + acquire 新**, 两步走, 缺一不可。改名就是换了 track-id, 它不会自己跟着改。比如把 `add-oauth-login` 改名成 `add-oidc-login`, 就要 release `add-oauth-login-1a2b3c4d` 再 acquire `add-oidc-login-1a2b3c4d`。

反过来, 如果你**不是放弃、只是本 session 先搁置**, 那就什么都别做 —— claim 保持 active, 下次同 `(container_id, session_id)` 回来时幂等 check 会命中, 不会重复 acquire。只有「这个方向不做了」才用 `--status abandoned`。

---

认领这步过了, 就可以继续 A.1.0 (查 `docs/decisions/` 有没有 technical decision-log 可预填充) → A.1.1 收集需求 → A.1.2 Level 判断了。`add-oauth-login` 听起来至少 Level 2, 起草时记得 proposal.md 头部 blockquote 的 `Linked Issue` 行按上面 A 那档的写法填 —— 有就写 `` `10CG/Aria#174` ``, 确认无关联就逐字写 `` `none` ``, **不留空、不删行** (`N/A` / `TBD` / `-` 都会被判不合规)。
