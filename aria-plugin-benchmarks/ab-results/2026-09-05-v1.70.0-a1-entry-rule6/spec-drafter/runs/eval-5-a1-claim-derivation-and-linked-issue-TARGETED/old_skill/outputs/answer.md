先说清我的依据边界, 免得你把推断当成规范:

我加载的 spec-drafter 里, 对 **proposal.md 头部 `Linked Issue` 字段的值**有逐条成文规则 (SKILL.md「proposal.md 头部字段要求」三条写法 + 2026-09-01 B8 位置裁定)。但对 **A.1 入口认领的 CLI 参数 `--raw-track-id` 怎么拼**, 这个 skill 里一个字都没有。

所以下面【2】是照成文规则的确定答案, 【1】和【3】是我的推断, 我会标出哪几处需要你确认。

---

## 【1】`--raw-track-id` 的实参

### 三段来源 (这部分我有把握)

| 段 | 值 | 从哪来 |
|----|----|--------|
| 容器 uuid | `1a2b3c4d` | `~/.aria/container-id` 的 `uuid:` 行, 取冒号后去掉前后空白的值 |
| 容器 label | `devbox-A1-very-long-label` | 同一文件的 `label:` 行, 同样取法 |
| Spec 标识 | `add-oauth-login` | 本 Spec 目录 `openspec/changes/add-oauth-login/` 的**目录名**, 不带 `openspec/changes/` 前缀, 不带尾斜杠 |

容器身份进 track id 的原因是多终端场景: 同一个 Spec 可能被两台 devbox 同时起草, claim/reconcile 要能区分「这块是谁在做」, 光有 Spec 名不够。

### 我会传的逐字实参

```
--raw-track-id '1a2b3c4d/add-oauth-login'
```

`raw` 这个前缀我的理解是: 传进去的是**未规范化的原始串**, 长度截断 / 非法字符替换由工具自己做。所以我不会先手工把 `devbox-A1-very-long-label` 截短或改写再传 —— 该截由它截, 我自己截等于把规范化逻辑复制了一份到调用侧, 两边一旦不一致就产生对不上的 track id。

### 两个我要先跟你确认的点

1. **label 进不进 id**。如果进, 逐字实参是 `1a2b3c4d-devbox-A1-very-long-label/add-oauth-login`; 如果不进 (我倾向不进 —— label 是人类可读注记, 可改名, 拿它做标识不稳定), 就是上面那个。你这个夹具特意给了一个 `very-long-label`, 像是在考截断行为, 这让我更怀疑 label 是要进的。
2. **分隔符到底是 `/` 还是 `-` 或 `:`**。我按「uuid 是命名空间, spec 名是命名空间内的键」选了 `/`, 但这是我的类比, 不是查证。

这两点我不打算凭感觉定死。落之前我会去看那个入口的 `--help` 或它的规范文档, 以实际定义为准 —— 现在只当作候选值给你。

---

## 【2】三份 proposal 要不要传 `--linked-issue`

**三份都要传**, 但只有一份能原样传。规则出处是 SKILL.md 的写法三条:

### A: `10CG/Aria#174`

传, 实参就是它本身。

```
--linked-issue '10CG/Aria#174'
```

符合写法 1 的 canonical 形 `<org>/<repo>#<n>`: org 段 `10CG`、repo 段 `Aria`、`#` + 纯数字。这是唯一一份可以直接用的。

### B: `none`

**照样要传**, 实参逐字是 `none`。

```
--linked-issue 'none'
```

这是最容易做错的一份。「没有关联 issue」不等于「不传这个参数」—— 写法 2 说得很直白: 无关联 (已核实) 时逐字写 `none`, **不留空、不删行**, 因为空值和「忘了写」在机读侧不可区分。省掉 `--linked-issue`, 生成的 proposal 头部要么缺这一行要么值为空, 两种都会被 `linked-issue-field-availability` 判不合规。

顺带一句: `none` 是唯一被承认的哨兵。`N/A` / `TBD` / `-` 都不算, 会判不合规。中文侧读取时另认 `无`, 但新写一律用英文 canonical, 所以这里就是 `none`。

### C: `[#174](https://forgejo.10cg.pub/10CG/Aria/issues/174)`

**不能原样传**。先转成 canonical 形再传:

```
--linked-issue '10CG/Aria#174'
```

它有两处不合规, 各自独立致命:

1. **markdown 链接形**。写法 3 明确点名: 不写 `[repo#n](url)` 这种形态, 会被判 `NO_TOKEN`。字段值必须是 inline code span 里的裸 token, 不是链接。
2. **缺 org/repo 段**。就算把链接壳剥掉, 剩下的 `#174` 也只有序号, 没有 `<org>/<repo>` 前缀, 不满足 canonical 形。org/repo 要从 URL 路径 `/10CG/Aria/issues/174` 里还原出来 —— 正好还原成 `10CG/Aria#174`。

也就是说 C 和 A 转换后指向同一个 issue, 最终实参完全相同。

### 小结

| 候选 | 传吗 | 实参 |
|------|------|------|
| A | 传 | `10CG/Aria#174` |
| B | 传 | `none` |
| C | 传 | `10CG/Aria#174` (从 URL 还原 org/repo, 剥掉 markdown 链接壳) |

另外提一句免得你多做无用功: 字段**写在头部第几行不影响机械判定**。check 按 E0 取文档序第一条 depth-1 命中, 不限行号 —— 既有 proposal 把这行写在超长 blockquote 第 45 行也判合规。SKILL.md 里那条「顺序建议 `Level` → `Status` → `Created` → `Linked Issue`」只是起草时对齐模板的建议, 不是判据, 别为了「对齐」去动既有 proposal 的头部顺序。

---

## 【3】起草到一半决定放弃这个方向

分三件事, 顺序按「先解锁别人, 再清自己的盘, 最后留痕」:

### 1. 先把认领放掉 (最要紧, 也是我最没把握的一件)

你既然走了 A.1 入口认领, 那条 claim 就在那儿挂着了。放弃方向而不释放, 后果是**悬空认领**: 别的终端 / 下一个 session 看到 `add-oauth-login` 有人认领, 就绕开它, 这块方向实际上没人做但也没人敢碰。多终端的 claim/reconcile advisory 本来就是防这个的, 悬空 claim 恰好是它防不住的那种脏数据 —— 因为从状态上看它跟「有人正在做」一模一样。

但**我加载的 skill 里没有释放动作的定义**, 我不会替你编一条命令出来。请查那个入口的 `--help` 看有没有 release / abandon / `--drop` 之类的子命令或反向参数。在查清之前, 至少别当它不存在。

### 2. 清掉已落盘的文件

分两种情况:

- **还没落盘** (spec-drafter 默认 `create_file=false`, 停在预览阶段): 什么都不用做, 零成本, 直接放弃。
- **已经落盘**: 直接删掉整个 `openspec/changes/add-oauth-login/` 目录。**不要走 openspec-archive**, 归档是给「做完了的变更」用的, 一份从没进过 Phase B 的草稿归档进去, 会在 archive 里留下一个看起来做完了其实没做的条目, 以后误导人。

### 3. 把「为什么放弃」写进 handoff

写 `docs/handoff/` (Rule #9), 不是 `.aria/handoff/`。

理由不是走流程: 「起草到一半放弃」是最典型的会被重新捡起来的线程 —— 半年后有人再想到 OAuth 登录, 如果没有记录, 会把你今天已经想明白的那个「为什么不做」从零再想一遍, 甚至想出相反结论再放弃一次。要写下来的是**放弃的理由**和**当时排除了什么**, 不是「起草了一份 spec 然后删了」这种流水。

另外: 如果你已经为这个方向开过 Forgejo issue, 一并关掉或补一条 comment 说明放弃原因, 别让 issue 和 handoff 讲两个故事。
