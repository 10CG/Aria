先纠一处落点: 你给的 `expected_archive` 不对。

## 1. 正确归档路径 = `openspec/archive/2026-09-08-user-auth`

Aria 的归档目录规范是 `openspec/archive/YYYY-MM-DD-{change_name}` —— **带日期前缀**, 且日期取**归档动作发生当日 UTC** (`TZ=UTC date -u +%Y-%m-%d`), 不是 spec 的创建日。今天是 2026-09-08, 所以:

```
❌ openspec/archive/user-auth                     # 你写的 expected_archive, 缺日期前缀
❌ openspec/changes/archive/2026-09-08-user-auth  # 旧 openspec CLI 的已知 bug 落点 (见下 §5)
✅ openspec/archive/2026-09-08-user-auth          # 正确
```

归档后的目录形状:

```
openspec/
├── archive/                            # 归档区
│   └── 2026-09-08-user-auth/
│       ├── proposal.md
│       ├── tasks.md
│       └── detailed-tasks.yaml
└── changes/                            # 活跃变更区, user-auth 归档后从这里消失
```

## 2. 执行前提: 这个 project_root 我这边够不着

`/workspace/my-project` 在我当前的环境里不存在 (`ls: cannot access '/workspace'`), 所以我**没有**对它执行任何创建/移动/删除。下面是可以直接照跑的命令 —— 请你在 `project_root` 下执行, 或者把仓库挂进来我再跑。

## 3. 归档流程 (十步循环 D.2)

### Step 1 — 完成 gate + C 分级证据闸 (先跑, 不能跳)

```bash
cd /workspace/my-project

# 前置: already-archived 检查 (日期前缀锚定, 防后缀误匹配)
ls openspec/archive/ | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-user-auth$'
#   有输出 ⇒ 立即 abort (BLOCKED-already-archived); 此路径零残留, 不写任何标记

# 主判定: 走单一可执行 SOT 的 tri-state gate, 一次调用同时拿 complete 与 verdict
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/lib/spec_complete.py" \
  --gate "openspec/changes/user-auth"
```

读 stdout 的 JSON, **按 `verdict` 字段路由, 不能只看 exit code** —— exit 0 是 `pass|warn` 二合一的粗粒度信号, 区分不出这两态 (warn 还要额外写 frontmatter + surface 提示)。

| gate 结果 | 处置 |
|---|---|
| `complete=true ∧ verdict=pass` | 放行, 正常归档 |
| `complete=true ∧ verdict=warn` | 放行 + Step 2 warn_overlay 把 `unverified_claims` 写进 proposal.md frontmatter |
| `complete=true ∧ verdict=block` | **BLOCK** —— 高置信死代码, tasks.md 全 `[x]` 也不放行 (完成是跑出来的, 不是勾出来的); 回显 `blocking_reasons` |
| `complete=false` 且未配逃生舱 | **BLOCK**, 回显 `complete_reason` 的缺口清单 |

确需归档未实施稿, 用逃生舱 `--archive-design-only` + `reason` (去空白后 ≥10 字符); 它同时豁免 completeness 与 C-block, 但输出里必须把被豁免的 `blocking_reasons` 显式回显, 不静默吞掉。注意 `skip_verification=true` **不能**绕过 C-block, 也不绕过 Status 归一化 gate。

### Step 2 — 写 proposal.md

`complete=true` 走正常路径: Status 非 done 时更新为 Complete。`verdict=warn` 时叠加 warn 覆盖层, 往 frontmatter 落 `unverified_claims` / `unverified_ack`。

### Step 3 — 执行归档 (`git mv`)

```bash
mkdir -p openspec/archive/                          # 前置 1: 父目录不在时 git mv 硬失败
test ! -e openspec/archive/2026-09-08-user-auth     # 前置 2: 承重断言, 见下方警告
git mv openspec/changes/user-auth openspec/archive/2026-09-08-user-auth
```

⚠️ **前置 2 是承重的, 不能省**: `git mv src dst` 在 dst 已存在为目录时**返回 rc 0**, 并把 src 整个**嵌进** dst 里 (→ `openspec/archive/2026-09-08-user-auth/user-auth/`), 不报任何错。所以重复归档不能靠 `git mv` 的返回码兜底。

### Step 4 — 归档后位置校验 (四条断言)

```bash
test -d openspec/archive/2026-09-08-user-auth              # 1. 目标存在
test ! -e openspec/changes/user-auth                       # 2. 源已消失
test ! -e openspec/changes/archive                         # 3. 无 CLI 错位残留
test -f openspec/archive/2026-09-08-user-auth/proposal.md  # 4. proposal.md 直接在该层
```

断言 4 不是冗余: Step 3 那个嵌套坏结果下, 断言 1-3 **全为真** (目标目录确实存在 / 源确实消失 / 确实没有 `changes/archive/`), 只有断言 4 会红。断言 3 若真红了, 说明历史上有人走过旧 CLI 路径, 把内容搬到 `openspec/archive/` 后再 `rmdir`。

### Step 6 — 验证归档结果

确认 `openspec/archive/2026-09-08-user-auth/` 下 `proposal.md` / `tasks.md` / `detailed-tasks.yaml` 完整。

### Step 7 — D auto-issue (归档不吞未完成)

gate 返回的 `d_payload` 非 null 时 (有未勾选项 / carry-forward 注释 / unverified 声称), 用 marker `<!-- archive-tracker:user-auth -->` 先搜后建, 分页遍历全部 open issue 去重, 命中就不重复开。干净归档 `d_payload=null` ⇒ 本步整段跳过, 零输出。非 Forgejo 仓或 CLI 不可用则降级打印待创建草稿, 归档本身不受影响。

## 4. 预期输出

```yaml
success: true
change_name: "user-auth"
archive_path: "openspec/archive/2026-09-08-user-auth"   # ← 不是 openspec/archive/user-auth
archive_method: "git mv"
verification:
  archive_exists: true
  contains_proposal: true
  contains_tasks: true
  contains_detailed_tasks: true
```

## 5. 关于 `openspec/changes/archive/`

老版 `openspec archive` CLI 会把变更输出到 `openspec/changes/archive/YYYY-MM-DD-{feature}/` 这个错位置。本 Skill 走 `git mv`, **不经过那条工具链**, 因此不会产生该错位 —— 对你这个仓来说它是历史记述, 只在你仍用旧 CLI 归档时才需要自行处置 (Step 4 断言 3 就是它的哨兵)。

## 6. 两点提醒

- 本 Skill 自身**不执行 `git commit`** —— 归档产生的 rename 由 Phase D 收尾时统一提交。
- 你要是想先看一眼不落盘, 加 `dry_run: true`, 它会跑完 Step 1 全部判断并给出三路结果 (ALLOWED / BLOCKED / ALLOWED-design-only), 保持零写入。

要我按上面的命令跑吗? 需要你先把 `/workspace/my-project` 挂到我能访问的路径, 或者告诉我它在这台机器上的真实位置。
