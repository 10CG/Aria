按你的要求, 下面只回答, 不跑任何命令。

## 结论先说 (四条)

1. **认领本身照做, 不跳。** 你的 config 里 `coordination.enabled: true`, 且这不是 Level 1 简单修复 ⇒ skip 的前两条都不成立。`unattended: true` 是第三条, 它置换的只是「怎么请裁」, 不置换「要不要认领」。
2. **零 `AskUserQuestion`。** 无人值守下这条是硬的: 不弹窗、不等人、也不能「等超时了就当默认同意」。
3. **改为写一条「待复议」记录, 状态置 `awaiting_owner`**, 由产品负责人事后复议。
4. **在 owner 复议前不自行放行。** 不自行判定「这大概是两件事, 我继续起草吧」, 也不自行换方向。overlap 非空那条写的是「请裁, 不自行放行」; 无人值守只是把请裁从同步问答改成异步留痕, 并没有把裁量权移交给 AI。反而更硬 —— 没有人在旁边随手纠正错判。

---

## 关键陷阱: 判定依据是配置, 不是运行期能力

不要用「AskUserQuestion 这会儿能不能弹出来 / 有没有人回」去反推该走哪条路。**有没有人可问是 `state_scanner.coordination.unattended` 这个配置事实**, 读的就是你贴的这份 `.aria/config.json`。用运行期行为反推会两头出错: 有人值守时因为一次调用异常就静默降级成自动放行; 无人值守时又去傻等一个永远不会来的答复。

另外 `mode: advisory` 也不构成放行授权 —— advisory 说的是协调 ref 的通告性质, 不是「overlap 可以忽略」。分档请裁那张表没有 advisory 例外分支。

---

## 动手前先把 overlap 读准 (四态别压成一态)

你描述的是 `linked_issue_overlap` **非空**, 即「已检测且确有碰撞」。但写记录时仍要按四态措辞, 别把别的态说成这一态:

| 信号 | 含义 | 措辞 |
|---|---|---|
| 键**缺席** | 未检测 (没传 `--linked-issue`) | 「本轮未检测」 |
| `linked_issue_overlap == []` | 已检测, 无碰撞 | 「无碰撞」 |
| `unknown_schema_claims > 0` | 有 N 条读不懂 schema 的 claim | 「已检测到 N 条无法解析的 claim —— 存在性已确认、内容未知, 按存在处理」 |
| `linked_issue_overlap == null` 且 `linked_issue_overlap_error` 非空 | 本轮没取到任何证据 | 「未能核实, 建议重试」 |

最后一行**绝不可**渲染成「无碰撞」——零证据不是正证据。读这几个键也别用 `.get(key, [])` / `.get(key, 0)`, 那正好把四态压成一态。

同时看一眼 `unknown_schema_claims`: 大于 0 时那 N 条按存在处理, 不能因为读不懂 schema 就当不存在。

---

## 按对方 claim 的 `status` 分档 (决定记录写什么, 不决定谁来裁)

| 对方 status | 记录里该给 owner 的处置选项 |
|---|---|
| `active` | 有人正在做。三个候选: 合并方向 / 换方向 / 确认确实是两件事 |
| `unknown` | 读不懂其 schema, **视同 `active`** 处理 (存在性已确认) |
| `done` / `abandoned` | 同一件事可能**已经做完或已被放弃**。按 `active` 同档请裁, 并注明该终态**也可能是 GC 产物**而非真的做完 |

三档最终都是「上呈请裁」, 差别只在记录里附的背景说明。无人值守不改变分档, 只改变裁决的送达方式。

---

## 「待复议」记录该带哪些字段

写给几小时/几天后才来看的人, 所以要自足:

- 本 Spec 的 `--raw-track-id` 逐字串 (slug 逐字 + `~/.aria/container-id` 的 `uuid` 字段, 不是 `label`)
- 对方 claim 的 container_id / session_id / `status` / 其 linked-issue
- overlap 的原始字段值 + 按上表选定的四态措辞 (含 `unknown_schema_claims` 计数, 若有)
- 三个候选方向 (合并 / 换方向 / 确认是两件事), 以及 `done`/`abandoned` 时的 GC 产物提示
- 本容器此刻已投入到哪一步 (便于 owner 判断合并成本)
- `awaiting_owner` 状态标记本身

---

## 两件不能做

1. **不要去 release 对方的 claim。** 那是对方的东西 —— 对 `done` / `abandoned` 也一样, 因为终态可能只是 GC 产物。
2. **不要顺手 release 自己的。** 自己的 claim 只有两种合法退出: Spec 目录改名 ⇒ `release 旧 + acquire 新`; 真的放弃方向 ⇒ `release_gate.py --raw-track-id <同一串> --status abandoned`。「挂起等 owner 复议」不属于这两种。提前 release 会让并发的另一方看不见你, 恰好制造这套机制要防的那个盲区。等 owner 裁完, 再按裁决执行对应的退出动作 (换方向 → abandoned; 合并 → 按合并后的目录名走改名两步)。

---

## 和有人值守的差别

| 维度 | 有人值守 | 无人值守 (本例) |
|---|---|---|
| 要不要认领 | 要, 早于投入 | **一样要**, 判据不变 |
| 四态读法 | 同 | 同 |
| 按对方 status 分档 | 同 | 同 |
| 请裁通道 | `AskUserQuestion` 同步问 | **零 `AskUserQuestion`**, 写「待复议」记录 |
| 裁决时机 | 会话内当场拿到答复 | 事后异步复议 |
| 拿不到裁决时的状态 | 会话内阻塞等答复 | 置 `awaiting_owner` 挂起 |
| AI 自行放行 | 不允许 | **同样不允许, 且更硬** (无人当场纠正) |
| 走哪条路的判据 | 配置 | 配置 (**不是**「弹窗能不能用」) |
| 退出义务 (改名 / 放弃) | 同 | 同 |

一句话: 无人值守真正动的只有两格 —— **请裁通道**和**裁决时机**; 检测、读法、分档、不自行放行、退出义务全部照旧。
