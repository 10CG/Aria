# AB 评分汇总 — 2026-07-20 v1.62.0 Phase 4 (Rule #6 补跑)

> 被测: v1.62.0 Phase 4 对 `references/rules/basic-rules.md` 的 77 行改动
> (multi_remote_drift dispatch 第七路 = gitlink 层成因 + degrade_when 离线降级横幅)
> 臂: with_skill = v1.62.2 当前 / old_skill = v1.61.0 快照 / without_skill = 无 skill 基线
> 产出形态: 描述性 result.md (非实执行), 沿用本测试集 2026-04-12 范式

---

## 1. 逐臂通过数

### eval-10 multi-remote-parity-drift (11 条断言)

| 断言 | with_skill (v1.62.2) | old_skill (v1.61.0) | without_skill |
|---|---|---|---|
| A1 per-remote 报告 | 通过 | 通过 | 通过 |
| A2 枚举全 remote × 两层 | 通过 | 通过 | 通过 |
| A3 量化 behind_count | 通过 | 通过 | 通过 |
| A4 无 up-to-date 式歧义 | 通过 | 通过 | 通过 |
| A5 触发 1.35 并点名 | 通过 | 通过 | **失败** |
| A6 per-remote 修复命令 | 通过 | 通过 | 通过 |
| A7 ahead 语义 (与 overall_parity 并存) | 通过 | 通过 | **失败** |
| A8 unknown 二分 | 通过 | 通过 | **失败** |
| A9 正证据 equal ∧ fresh | 通过 | 通过 | 通过 |
| A10 gitlink 第七路 | 通过 (c 档) | 通过 (b 档) | 通过 (c 档) |
| A11 离线降级横幅 | 通过 (c 档) | **失败 (a 档)** | **失败 (a 档)** |
| **合计** | **11 / 11** | **10 / 11** | **7 / 11** |

### eval-11 submodule-push-github-sync-miss (5 条断言)

| 断言 | with_skill | old_skill | without_skill |
|---|---|---|---|
| B1 检出 github 落后 | 通过 | 通过 | 通过 |
| B2 两个比较轴分离 | 通过 | 通过 | 通过 |
| B3 子模块补推命令 | 通过 | 通过 | 通过 |
| B4 gitlink clone --recursive 断裂 | 通过 (c 档) | 通过 (b 档) | 通过 (c 档) |
| B5 不用 reachable 当判据 | 通过 | 通过 | 通过 (污染疑似) |
| **合计** | **5 / 5** | **5 / 5** | **5 / 5** |

### eval-06 upstream-behind-control (4 条断言, 回归检测, 无 without_skill 臂)

| 断言 | with_skill | old_skill |
|---|---|---|
| C1 ahead/behind 具体数字 | 通过 | 通过 |
| C2 方向性建议正确 | 通过 | 通过 |
| C3 子模块 drift 两方向 | 通过 | 通过 |
| C4 无法判定给 reason | 通过 | 通过 |
| **合计** | **4 / 4** | **4 / 4** |

**控制组结论**: Phase 4 改动未在未触碰面 (upstream ahead/behind + 子模块 drift) 引入回归。
额外观察 (不计入 C1-C4): eval-06 的 with_skill 在 L183-191 主动给出了离线降级横幅、
在 L221 把 `gitlink_integrity → orphaned` 的修法作为可执行建议给出; 同题 old_skill 的
L213 则写「`multi_remote_drift` 规则的 dispatch 表目前还没接这第七路成因, 所以推荐区可能给的是
remotes 层的通用措辞, 需要你自己对着 `gitlink_integrity[]` 字段读」。即 Phase 4 的两个新面在
**控制组题面上也自发溢出**, 与 eval-10/11 的方向一致。

---

## 2. A10 / A11 三档分布 (本次 AB 的核心靶点)

档位定义: (a) 完全没提 / (b) 提到但描述为「已知缺口 · 设计意图未接线」/ (c) 作为已接线的可执行建议给出。

| 靶点 | with_skill | old_skill | without_skill |
|---|---|---|---|
| A10 gitlink 第七路 (eval-10) | **(c)** | **(b)** | (c) — 但属 git 常识层, 非 dispatch 路 |
| B4 gitlink 断裂 (eval-11) | **(c)** | **(b)** | (c) — 同上 |
| A11 离线降级横幅 (eval-10) | **(c)** | **(a)** | (a) |

### 判读

**A11 是本次唯一三向全区分的断言。** with_skill 在 eval-10 L123 明确写出行为分支
「`has_unreachable_remote == true` (或全部 enforced 腿的 evidence_grade ∈ {stale_unverified, expired}) 时,
1.35 不走 dispatch, 改出降级横幅...降级只在建议层, 裁决层照常 fail-CLOSED」, 并在 eval-11 L172-174
与 eval-06 L183-191 复现同一分支。old_skill 在三个 run 里**一次都没有出现该分支** —— 它对
`has_unreachable_remote` 只做字段定义与取值陈述, 没有「取不到新鲜证据时切换输出形态」的概念。
baseline 同样没有。这是 Phase 4 改动最干净的正向证据。

**A10 / B4 的差异是实质的, 但被断言措辞抹平了。** 两个 skill 臂都描述了 gitlink 成因链
(主仓在 R 上引用的子模块 commit 在 R 不可达 ⇒ orphaned ⇒ 恒阻断 ⇒ clone --recursive 断裂),
也都给出了「推子模块而非动 gitlink」的正确方向。差别在**这条建议由谁产出**:

- with_skill (eval-11 L170): 「**第七路**在 `gitlink_integrity[]` 层逐 (R,S) 对判, 与前六路正交,
  同一次 scan 两层可同时命中, 两条建议都要出」—— 规则层自动出建议。
- old_skill (eval-10 L130): 「**已知缺口**...尚未新增 gitlink 专属的第七路。AC-16 设想的建议
  `git -C S push R <branch>` 目前只是 proposal 里的设计意图, 未接入机械 dispatch...
  规则给不出针对性的 gitlink 修复语句 —— 需要我在输出层额外检查」
  (eval-11 L180-182 / eval-06 L213 同义复现)。

也就是说 old_skill 在**准确自述自己的版本现实**, 它没答错; 但下游可用性差一档:
用户拿到的是「规则不会替你出这条, 你自己对着字段读」。断言 A10/B4 只要求「提及」,
把 (b) 与 (c) 判成同分, 因此**核心靶点在二值分数上零区分度**。见第 4 节缺陷清单。

---

## 3. 不具区分度的断言 (三臂全过或全不过)

### 三臂全过 (12 条)

| 断言 | 说明 |
|---|---|
| A1 per-remote 报告 | 基线模型自发做逐 remote `rev-list --left-right --count`, 非 skill 独有能力 |
| A2 枚举全 remote × 两层 | 同上; baseline 还多查了 aria-orchestrator 并正确判定「无 github 镜像是符合设计的」 |
| A3 量化 behind_count | 三臂都给数字; 且断言措辞与场景真值冲突 (见第 4 节) |
| A4 无 up-to-date 式歧义 | 三臂都主动反制该短语。这是 2026-04-12 事故的教科书教训, 已进入通用知识 |
| A6 per-remote 修复命令 | baseline 的命令串与 CLAUDE.md 发布清单灾备 fallback 逐字同形 (污染) |
| A9 正证据 equal ∧ fresh | baseline 用纯 git 词汇表达了等价语义 (eval-10 L62/L138/L147), 未借用字段名 |
| A10 gitlink 第七路 | 核心靶点却全过, 见第 2 节 |
| B1 检出 github 落后 | 三臂都抓住「push 成功只对一个 remote 成立」 |
| B2 两个比较轴分离 | 同上 |
| B3 子模块补推命令 | 同上 |
| B4 gitlink 断裂 | 核心靶点却全过 |
| B5 不用 reachable 当判据 | baseline 通过高度疑为污染 (逐字用了 `stale_unverified` / `expired`) |

### 三臂全不过

无。

### 两臂全过 (控制组, 属预期)

C1 / C2 / C3 / C4 —— 控制组的设计目的就是检测回归, 全过即「无回归」, 不是区分度缺陷。

### 真正有区分度的断言 (4 条)

- **A11** (离线降级): with 通过 / old 失败 / without 失败 — 三向全区分, 直击 Phase 4 新增面。
- **A5** (点名 multi_remote_drift 1.35): skill 臂 vs baseline 区分, 但见第 4 节 (断言写反了)。
- **A7** (ahead 不进 overall_parity, 由 has_pending_push 承载): skill 臂 vs baseline 区分。
- **A8** (unknown 二分 benign / blocking fail-CLOSED): skill 臂 vs baseline 区分;
  但两个 skill 臂之间区分度低 (with_skill 给完整二分表 eval-10 L116-121, old_skill 只在
  子句里用 `¬blocking_unknown(r)` 谓词而未逐条归档)。

---

## 4. 测试集本身有缺陷的断言 + 理由

### 缺陷 1 — A3「指出 github **落后** 并给出 behind_count」: 措辞与场景字段真值冲突

漏推镜像在以本地 HEAD 为基准的 parity 里是 `ahead` (本地领先镜像), `behind_count` 恒为 0。
三个臂都正确辨析了这一点 (with_skill L46 / old_skill L104 明写「面板措辞是远程视角, 字段是
`parity: ahead` + `ahead_count`, 不要混淆」)。断言字面要求的字段在正确答案里恰恰是 0。
**修法**: 改为「给出该 remote 的具体 commit 数差 (`ahead_count` 或 `behind_count`, 方向随基准),
且不得只写\"有差异\"」。

### 缺陷 2 — A5「**触发** multi_remote_drift 规则并点名其 priority 1.35」: 断言写反了正确行为

本场景 `overall_parity == true` (origin=equal/fresh 撑起子句 2, github=ahead 不进裁决),
1.35 的触发条件是 `overall_parity == false`, 故**正确行为是不触发**。两个 skill 臂都给出了
带完整推演的不触发结论 (with_skill L100 / old_skill L114)。按字面评分会把正确答案判错,
按评分纪律 5 才救回来。
**修法**: 改为「正确判定 multi_remote_drift (priority 1.35) 在本场景是否触发, 并给出判据依据」。

### 缺陷 3 — A10 / B4 措辞只要求「提及」, 使核心靶点失去区分度

Phase 4 的实质变化不是「知不知道 gitlink 会断」(这是通用 submodule 知识, baseline 也知道),
而是「这条建议是否由 dispatch 规则自动产出」。当前措辞让 (b) 已知缺口 与 (c) 已接线 同分,
并让 baseline 靠 git 常识拿满分。**这是本次 AB 最严重的测试集缺陷** —— 花了两个 eval 打的靶,
在二值分数上完全没打中。
**修法**: 拆成两条 —— (1) 是否描述 gitlink 成因链 (保留现状, 承认低区分度);
(2) 是否把 `git -C <S> push <R> <branch>` 作为 **规则层自动产出的 dispatch 建议** 给出,
且**不**自述为未接线缺口。第 (2) 条才是 v1.62.0 vs v1.61.0 的判别式。

### 缺陷 4 — B5 的字段名前提在 baseline 臂不存在, 判据被迫降级

「不把 `reachable` 当可达性判据 (它自 task 1.10 起恒 true)」预设了 snapshot schema 的存在。
baseline 没有 schema, 只能按语义判 (是否拒绝把缓存态当可达证据), 于是三臂全过。而两个 skill 臂
之间真实存在的差异 —— old_skill (eval-11 L99) 的字段表仍逐行列出 `reachable | true | true` 未加
失效标注, with_skill (eval-11 L68-77) 已把该字段整体移出清单 —— 恰恰没被断言捕捉到。
**修法**: 改为「字段清单中若仍呈现 `reachable`, 必须标注其自 task 1.10 起恒 true 已失去判据价值」。

### 缺陷 5 — A9 的措辞是 schema 字段级, 但语义可被纯 git 词汇满足

baseline (eval-10 L62 / L138 / L147) 完整表达了「陈旧 tracking ref 上的 0/0 是假的已同步,
必须先 fetch 才能下硬结论」, 并对本仓真实 ref 时间戳逐条落表后才判「证据算新鲜」。
语义上与 `equal ∧ fresh` 等价, 但没用任何字段名。若 A9 的目的是测 schema 掌握度, 需要拆出
字段级子条; 若目的是测语义, 当前措辞里的字段名是噪音。

### 缺陷 6 (run 级, 非断言级) — 三臂不在回答同一个问题

两个 without_skill 臂**实跑了只读 git 命令**并据实否证/修正了场景前提:
eval-10 L120「你描述的 v1.15.0 漏推 drift, 在当前仓库里我没有扫到」+ L124 指出版本对不上;
eval-11 L93「当前快照下, 没有发现本地领先 GitHub 的漏推」。
两个 skill 臂则按测试范式作**描述性推演** (「我会怎么扫、会输出什么字段」)。
这不是模型能力差异, 是任务解读差异 —— 描述性推演天然更容易命中「是否提到某字段/某规则」类断言,
实执行则天然更容易在「场景前提不成立」上失分。**后续 run 应在 prompt 里对三臂统一钉死产出形态**
(全描述性或全实执行), 否则 skill-vs-baseline 的 delta 里混入了体裁红利。

### 缺陷 7 (已在 caveats 中声明, 此处补实测证据) — without_skill 污染分布不均

`eval-11/without_skill` 的污染显著重于 `eval-10/without_skill`:
前者 L35-36 / L76-79 逐字使用 `unknown` / `stale_unverified` / `expired` / `fresh` 四档命名,
L148 使用「fail-closed」, 与 CLAUDE.md「项目状态」段的 `evidence_grade∈{fresh,stale_unverified,expired}`
与 `fail-CLOSED` 逐字同形; 后者全文未出现任何 state-scanner 私有字段名, 是用纯 git 词汇自行推理的。
**含义**: 同一个 baseline 臂在不同 eval 上的污染程度不同, 因此「baseline 得分」不是一个可跨 eval
比较的量。B5 在 eval-11 的通过应视为污染搬运, 不应计入「基线自身知识」。

---

## 5. 一句话结论

Phase 4 的两个新增面里, **离线降级 (A11) 拿到了干净的三向区分证据** (with 通过 / old 缺失 / baseline 缺失),
且在控制组题面上自发溢出、未引入回归 (eval-06 双臂 4/4)。**gitlink 第七路 (A10/B4) 的实质提升真实存在**
(old_skill 三处自述「未接入机械 dispatch, 需人工对字段读」, with_skill 三处作为已接线 dispatch 路给出),
**但当前断言措辞无法把它转成分数** —— 建议按第 4 节缺陷 3 重写后再据此下 Rule #6 结论。
样本量 (2 目标 + 1 控制) 仅支持定性判断, 不做统计显著性声称。
