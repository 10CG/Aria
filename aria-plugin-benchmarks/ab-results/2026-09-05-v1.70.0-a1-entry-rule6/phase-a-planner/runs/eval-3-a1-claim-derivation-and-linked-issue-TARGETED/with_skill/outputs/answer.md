下面按你的四问逐条回答, 不跑任何命令。

---

## 【1】`--raw-track-id` 的实参

逐字就是:

```
add-oauth-login-1a2b3c4d
```

拼法是 `<spec-slug>-<container_uuid>`, 两段各自的来源:

| 段 | 值 | 从哪来 |
|---|---|---|
| `<spec-slug>` | `add-oauth-login` | 本 Spec 目录名 `openspec/changes/add-oauth-login/` 的**逐字**目录名。**不要预先归一** (不改大小写、不换分隔符、不裁前后缀) —— 归一是 CLI 内部做的事, 你在这里动手只会让两次认领算出不同的 track-id |
| `<container_uuid>` | `1a2b3c4d` | `~/.aria/container-id` 里的 **`uuid` 字段** |

关键一点: uuid 段取的是 `uuid: 1a2b3c4d`, **不是 `label: devbox-A1-very-long-label`**。label 是装饰性的, 改一行 label 不该把 track-id 换掉 —— 一旦跟着 label 走, 同一个容器同一件事在改完 label 后就变成了「另一个人在做另一件事」, 认领机制当场失效。

所以完整调用长这样 (mode 用 advisory, 带 `--include-terminal`, `--repo-path` 指主仓根):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "add-oauth-login-1a2b3c4d" \
  --phase A.1 --mode advisory \
  --linked-issue "10CG/Aria#174" \
  --include-terminal \
  --repo-path "/home/dev/Aria"
```

（`--linked-issue` 那行是否出现, 见【2】; 三份候选里只有 A 会让它出现。）

另外提醒一句**幂等**: 真跑之前先看 coordination ref 里按 `(container_id, session_id)` 定位的 `claims/<container>/<session>.yaml` 是否已存在且 `status == active`。已存在就跳过, 不要重复 acquire。

---

## 【2】三份 proposal 各自传不传 `--linked-issue`

先说取法, 这是**两阶段**的, 不是直接肉眼判:

- 若 `${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/linked_issue_field_probe.py` **存在**, 实参 = `python3 <该脚本> --emit-arg <本 Spec 的 proposal.md>` 的 stdout; **stdout 为空 ⇒ 整个 `--linked-issue` 参数省略**。
- 脚本不存在时, 才按字段 Spec E6 手工判: **只有**「`Linked Issue` 字段行冒号后**首个 code span** 的**第一个元素**」形如 `<org>/<repo>#<n>` **且非哨兵**时才传。

按 E6 判你这三份:

| 候选 | 字段值 | 传吗 | 实参 | 理由 |
|---|---|---|---|---|
| A | `10CG/Aria#174` | ✅ 传 | `--linked-issue "10CG/Aria#174"` | 首个 code span 的第一个元素形如 `<org>/<repo>#<n>`, 三段齐全 (org / repo / 数字 issue 号), 且不是哨兵 |
| B | `none` | ❌ **整个参数省略** | 无 | `none` 是**哨兵**, 不是值 |
| C | `[#174](https://forgejo.10cg.pub/10CG/Aria/issues/174)` | ❌ **整个参数省略** | 无 | 这是 markdown 链接, 不是 code span; 就算退一步只看链接文本 `#174`, 它也缺 `<org>/<repo>` 两段, 不满足形状 |

三点必须说清楚的:

1. **哨兵绝不能当值传。** `none` / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 一律是「省略整个参数」, 不是「传个 `none` 进去」。理由很硬: 任何非空字符串都 truthy, 两份**毫无关系**的 Spec 只要都在字段里写了 `none`, 就会在 overlap 检测里互相命中 —— 你会得到一个纯粹凭空造出来的碰撞, 然后为它去请裁。

2. **C 不要自己「翻译」。** 从那条 URL 里人眼当然能读出这就是 `10CG/Aria#174`, 但把它手工还原成规范形式传进去, 等于用你的推断替换了字段的实际内容 —— 这已经不是「读字段」而是「代写字段」了。正确处置是**省略参数**, 顺手去把那份 proposal 的 `Linked Issue` 字段改写成规范的 code span 形式 (`` `10CG/Aria#174` ``), 让它下次自己就合格。

3. **省略参数 ≠ 不认领。** B 和 C 这两份照样要跑 `phase1_gate.py` 做 claim, 只是那次调用里没有 `--linked-issue` 这一行。

顺带把**输出怎么读**也放这儿, 因为 B / C 省略参数会直接影响你看到什么 (四态两两不同, 不能混):

| 信号 | 含义 | 该怎么说 |
|---|---|---|
| 键**缺席** | 本轮没传 `--linked-issue`, 即未检测 (B / C 就是这一档) | 「本轮未检测」 |
| `linked_issue_overlap == []` | 已检测, 无碰撞 | 「无碰撞」 |
| `unknown_schema_claims > 0` | 有 N 条 schema 读不懂的 claim | 「已检测到 N 条无法解析的 claim —— 存在性已确认、内容未知, **按存在处理**」 |
| `linked_issue_overlap == null` 且 `linked_issue_overlap_error` 非空 | 本轮没取到任何证据 | 「**未能核实**, 建议重试」 |

最后一行**绝不可**渲染成「无碰撞」—— 零证据不是正证据。同理别用 `.get(key, [])` / `.get(key, 0)` 去读这几个键, 那正好把四态压成一态。

如果 A 这份真的撞出了非空 overlap, 按对方 claim 的 `status` 分档, 经 `AskUserQuestion` 请裁, 不自行放行: `active` → 请裁 (合并方向 / 换方向 / 确认确实是两件事); `unknown` → **视同 active**; `done` / `abandoned` → 同一件事可能已做完或已被放弃, 按 active 同档请裁, 并注明该终态**也可能是 GC 产物**而不是真的做完 —— 而且**不要提议去释放对方的 claim**, 那是对方的东西。

---

## 【3】起草到一半决定放弃这个方向

跑 release, 显式置终态 `abandoned`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/release_gate.py" \
  --raw-track-id "add-oauth-login-1a2b3c4d" \
  --status abandoned
```

两个要点:

- **track-id 必须是同一串**, 逐字照抄 acquire 时那个 `add-oauth-login-1a2b3c4d`。释放靠的就是这串 id 对上, 重新推导一遍很容易推出个不一样的来, 那就等于没释放。
- **这是硬性退出义务, 不是可选的收尾礼貌。** 不 release 就留下一条永不释放的僵尸 claim: 下一个人来做这件事时会看到一条 `active` claim, 于是停下来请裁 —— 为一个你早就放弃了的方向。

顺带把另一条退出义务也记住, 它和放弃是同一组的: **Spec 目录改名 ⇒ release 旧 + acquire 新**, 必须两步走。改名就是换了 track-id, 只 acquire 新的会把旧 id 那条留成僵尸。

---

## 【4】Level1 命中, 或 `coordination.enabled` 为 false

这两种情况都落在 skip 三条里, 处置一样: **整个 claim 块零调用**。

- `state_scanner.coordination.enabled` 显式 `false` ⇒ 本块整体零调用。owner 关掉了协调机制, 这是配置事实。
- `skip_if: complexity: Level1` 命中 ⇒ 零调用。理由很实际: 否则每个 typo 修复都要写一条永不 release 的僵尸 claim, 外加一次外向 push。

注意 **零调用是彻底的**: 不 acquire, 因此也**不需要** release —— 压根没有 claim 存在, 别去补跑一个 `release_gate.py`。

还有第三条 skip 顺带说明, 因为它形状不同、最容易和上面两条混为一谈:

- `state_scanner.coordination.unattended == true` ⇒ **不是零调用**, claim 照常跑; 变的是**零 `AskUserQuestion`**。真撞上 overlap 时改为写一条「待复议」记录并置 `awaiting_owner`, 由产品负责人事后复议。
- 这里有个坑要避开: **不得以「AskUserQuestion 现在能不能用」做运行期推断**。有没有人可问是**配置事实** (`unattended` 字段), 不是你从当前环境探测出来的东西。

最后一句边界: skip 就这三条, **其余任何理由都不构成 skip**。「这次改动很小」「就一个文件」「已经很晚了」「反正没人会同时做这个」都不算 —— 认领的全部价值就在于它**早于投入**, 十步循环那 10 轮闸门审的都是「这份产物做得对不对」, 没有任何一条问过「远端是不是已经有人在做同一件事 / 它该不该存在」。等做完了再认领, 记录的只是既成事实。
