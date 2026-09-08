# 已归档检测: `user-auth`

## 结论

**未检出已归档** (`already_archived = false`) —— 归档前置放行, 可以继续走 Step 1 的完成度 + C 分级证据闸。

但你给的 `check_archive` 路径口径和 skill 的判定口径**不一致**, 这点得先对齐, 否则「检测」本身会给出假阴性。详见第 2 节。

---

## 1. 参数口径对齐

本 skill 的输入契约只有 `change_name` 加五个 options (`skip_verification` / `dry_run` / `archive_design_only` / `reason` / `ack_unverified`)。你给的三个 key 这样落:

- `spec_path=openspec/changes/user-auth` → `change_name = user-auth`。路径前缀是固定的, skill 只吃**目录名**。
- `check_archive=openspec/archive/user-auth` → **不是参数**, 而且这个路径形态本身就不是 canonical 归档落点 (见下)。
- `detect_duplicates=true` → **不是开关**。already-archived 检测在 Step 1 是**无条件前置**, 排在完成度判定之前, 没有 `false` 这个取值。你想要的行为本来就默认开着; 传 `true` 不改变任何事, 传 `false` 也关不掉。

---

## 2. 判定规则 (逐字)

Step 1 最前置的那条检查是:

```bash
ls openspec/archive/ | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-user-auth$'
```

**日期前缀锚定 + `$` 收尾**, 目的是防后缀误匹配。canonical 落点形态是 `openspec/archive/YYYY-MM-DD-{change_name}/`, 其中日期取**归档动作发生当日 UTC** (`TZ=UTC date -u +%Y-%m-%d`), 不是 spec 创建日。

这条正则的边界行为:

| 归档目录名 | 是否命中 | 原因 |
|---|---|---|
| `2026-07-05-user-auth` | 命中 | canonical 形态 |
| `2026-07-05-user-auth-v2` | 不命中 | `$` 挡住后缀 |
| `2026-07-05-user-auth-refactor` | 不命中 | 同上 |
| `2026-07-05-legacy-user-auth` | 不命中 | `^` + 日期段紧邻 change_name |
| `user-auth` (裸名, 无日期前缀) | **不命中** | 缺日期前缀 |

最后一行就是你给的 `check_archive=openspec/archive/user-auth`。一个裸名 `openspec/archive/user-auth/` 既不是 canonical 归档落点, 也**不会**被这条前置检出。如果它在你的仓里真实存在, 那它是仓外来源 (手工建 / 旧工具链 / 别的约定), 得由人判定它是不是同一个 spec 的归档 —— skill 不会替你认它。

---

## 3. 本仓实测 (只读)

- 锚定 grep: **无命中**。当前 `openspec/archive/` 下 145 个条目里没有 `YYYY-MM-DD-user-auth`。
- 裸名 `openspec/archive/user-auth`: **不存在**。
- `openspec/changes/archive/` (旧 CLI 错位落点): **不存在**, 这一侧干净。

判定: `already_archived = false` → 前置放行。

一点边界说明: 这条前置只查 **archive 侧**, 不负责源目录存在性。若 `openspec/changes/user-auth` 本身不存在, 那会落到错误处理表里「变更目录不存在 → 检查 openspec/changes/ 目录」那一行, 和 already-archived 是两回事, 别混成一个结论。

---

## 4. 如果命中了会怎样 (abort 语义)

- 立即 abort, 判定码 **`BLOCKED-already-archived`**。
- **不进入完成度判定** —— 不调 `spec_complete.py --gate`, 拿不到也不需要 `complete` / `verdict`。
- **不写任何标记** —— 所有写入都属于 Step 2 (Status 改 `Complete` / `archive_type` + `archived_reason` / warn_overlay 的 `unverified_claims` frontmatter), 所以 abort 路径**零残留**。
- 自然也走不到 Step 7, 不会建 tracker issue。
- **不覆盖**既有归档。要重归档得先人工处置既有条目。

---

## 5. 重复检测真正的承重点: `git mv` 不会替你报错

这是这条前置必须存在、而且必须做**两遍**的原因:

`git mv src dst` 在 dst **已存在为目录**时 **返回 rc 0**, 并把 src **嵌进** dst 里:

```
openspec/archive/2026-09-08-user-auth/user-auth/     ← 实测结果, 无任何报错
```

所以重复归档**不能靠 `git mv` 的退出码兜底**, 只能靠前置断言。因此检测点是两个:

1. **Step 1 前置** —— 归档动作开始前查一次。
2. **Step 3 前置 2** —— `git mv` 之前**再查一次** `openspec/archive/{YYYY-MM-DD}-user-auth/` 不存在, 防 Step 1 到 Step 3 之间的竞态 (多终端 / 并发 session)。

顺带: Step 3 前置 1 要先 `mkdir -p openspec/archive/` —— 父目录不存在时 `git mv` 是**硬失败**, 而且那个失败不在上述分支覆盖内。

---

## 6. 嵌套坏结果只有一条断言抓得到

万一前置被绕过、真产生了嵌套结果, Step 4 的四条断言里:

| 断言 | 嵌套情形下的取值 |
|---|---|
| 1. `openspec/archive/{date}-user-auth/` 存在 | **真** |
| 2. `openspec/changes/user-auth/` 已消失 | **真** |
| 3. `openspec/changes/archive/` 不存在 | **真** |
| 4. `openspec/archive/{date}-user-auth/proposal.md` **直接存在于该层** | **假** ← 只有这条会红 |

所以给重复检测做验收时, **别拿断言 1-3 当证据** —— 它们对这个失败形状天然免疫, 三条全绿时坏结果照样成立。

---

## 7. 另一类「重复落点」: `openspec/changes/archive/`

历史上 OpenSpec CLI 有个 bug, 会把归档写到 `openspec/changes/archive/YYYY-MM-DD-{feature}/` 而不是 `openspec/archive/`。

本仓从未安装该 CLI, 归档一律走 `git mv`, 所以这对本仓是**历史记述, 不是现时风险** (第 3 节实测也确实不存在)。仍在用那条旧工具链的采用方需要自己处置: 把内容搬到 `openspec/archive/` 之后 `rmdir` 掉空的 `changes/archive/`。

---

## 8. Step 7 那层去重是另一回事, 别和这层混

如果归档最终执行、且 `d_payload` 非 null, Step 7 会建 tracker issue, 那里也有去重, 但对象完全不同:

- marker = `<!-- archive-tracker:{spec_id} -->`, **HTML 注释精确子串匹配**, 不是模糊 title 匹配。
- **分页遍历全部 open issue** (`limit=50` 逐页翻, 直到某页不足 50 条), 避免 open issue > 50 的仓库漏掉既有 tracker 而重复开单。
- 命中 → 输出「已存在 tracker issue #N, 未重复创建」, `d_issue_skip_reason=duplicate_found`。

这层去重的对象是 **issue**, 不是归档目录; already-archived 命中时压根到不了这里。

---

## 建议下一步

1. **先确认裸名目录**: `openspec/archive/user-auth` 在你的仓里到底存不存在。存在 → 人工判定后要么重命名成 `YYYY-MM-DD-user-auth` 纳入 canonical, 要么确认它跟这个 spec 无关; 不存在 → 你的 `check_archive` 只是写法问题, 按 canonical 形态写即可。
2. **真要归档前先 dry run**, 拿三路输出确认, 全程不写入任何文件:

```yaml
change_name: user-auth
dry_run: true
```

   dry_run 会跑完 Step 1 的全部判断 (already-archived 前置 + 完成度 + tri-state verdict), 报 `BLOCKED` / `ALLOWED` / `ALLOWED-design-only`, 并保持「未发生任何写入」不变量。

3. 本次我**只做了只读检测**: 没有执行 `git mv`, 没有修改任何文件, 没有建 issue。
