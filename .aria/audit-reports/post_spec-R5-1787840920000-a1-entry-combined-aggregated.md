---
checkpoint: post_spec
round: 5
converged: false
overridden_by_user: false
incomplete: false
verdict: REVISE
---

# post_spec R5 (combined) — a1-entry 三份 Spec · **`max_rounds=5` 的最后一轮**

> **模式**: convergence · **席位 5/5, 第三批全新镜头** (R3 = aria 五席; R4 = type-design/silent-failure/architect/pr-test/explorer; R5 = 下表)
> **审计对象 SHA**: `b0c16ff` (主控**全程未改被审文件** —— R4 的流程失误未重复)
> **基线**: aria `origin/master` = `d50f9c3`
>
> | 席 | 镜头 | verdict | counts |
> |---|---|---|---|
> | `feature-dev:code-reviewer` | 高置信度缺陷 (只报有把握的) | REVISE | 1C/0M/0m |
> | `plugin-dev:skill-reviewer` | **SKILL.md 指令面质量** (四轮来首次) | REVISE | 4C/10M/4m |
> | `code-simplifier` | **简化/过度设计** (四轮来首次) | REVISE | 3C/8M/5m |
> | `pr-review-toolkit:comment-analyzer` | 文档准确性/注释腐烂 | REVISE | 7C/10M/5m |
> | `general-purpose` (factcheck) | 独立事实核验 | REVISE | 0C/3M/19m |

## 判定

**REVISE, 未收敛 —— 但走势与前两轮性质不同, 必须分开陈述。**

| 轮次 | critical | 形态 |
|---|---|---|
| R2 | 3 | 设计缺陷 |
| R3 | 3 | 设计缺陷 (内容全换) |
| R4 | 9 | 设计缺陷 (内容全换, 8/9 由上轮 fix 引入) |
| **R5** | **≈6 簇** | **性质分裂 —— 见下** |

### 🔑 本轮最重要的结论: **设计侧收敛了, 落版侧系统性失败了**

- **`feature-dev` 席独立判定: R4 的 9 条 critical 中 **8 条已由可核验的文本级修复实质关闭** (K1/K3–K9), 且**未发现净新增 critical 簇**。
- **`factcheck` 席**: 22 条 finding **无一条改变任何设计结论**, 全是引用/计数/锚点类, 其中 19 条可由机械检查抓住。
- **但 `comment-analyzer` 席指出了本轮的真实形状**, 主控逐条实测确认:

> **主控把 K1–K9 九条修复全部写成了「诊断 blockquote」, 一条都没有回灌到 A.2 真正消费的三张表 (§Impact / SC 表 / 代码落点)。**

| 实测 | 结果 |
|---|---|
| `SC-30/31/32/33` 在 SC 表的行数 | **0 / 0 / 0 / 0** (全文各 3/2/1/1 处, 全在 K 段内) |
| 字段 `SC-9` / 探针 `SC-19` 在各自 SC 表的行数 | **0 / 0** |
| Impact `:721` 是否仍写被 K2 判为错误命名的 `fail-CLOSED` | **仍写着** |
| `gc.py` / `heartbeat:244-256` (K1 本体) 是否进 Impact 表 | **0 行** |
| K3 自称已删的 `compose` 字样 | **`:642` 仍在** (只改了前半句) |

⇒ **同一份文档对同一件事同时给出两个相反规定**, 而 A.2 是**从表派生任务**的 ⇒ **现状不可进 A.2** (从哪张表派生就实现哪一版)。
这是**机械失败不是设计失败** —— 五席一致认为**剩下是机械活**。

## Critical 簇 (去重后 ≈6) + 2 个结构性选项

| # | 簇 | 席位 | 性质 |
|---|---|---|---|
| **R5-1** | **落版未回灌三张表** (上表五项实测) | comment-analyzer C-2~C-5 · factcheck M2 | **机械**, 主控担责 |
| **R5-2** | **K2 残余矛盾 + day-one 悬崖**: `:453` 判「`track_form is None` ⇒ 报错退出」而 `:497`/`:722` 仍写「零影响」; 两字段同批引入 ⇒ **ship 当天全部存量 claim 命中**, 而 D.2b 无人值守 (AD10) ⇒ **无恢复路径的脚本级失败悬崖** | feature-dev | 设计, 主控担责 |
| **R5-3** ⭐ | **跑「照跑档」AB 会对生产 `refs/aria/coordination` 真实 push**: `coordination_ref.py:322` `push=True` + `:347` `git push` + `phase-b-developer:97-98` 逐字「auto_bootstrap 会自动建 ref 并 push 到项目 origin」+ `ab-suite/phase-a-planner.json` eval 1 是**不命中任何 skip 条件的真实 feature** | skill-reviewer | **活风险, 与本 Spec 收敛无关** |
| **R5-4** | **rule6_note 漏 5 个处方性 hunk 且按文件目录划范围** (`:591` 写「SKILL.md/frontmatter 6 处」, 实为 **11 hunk / 9 文件**; Rule #6 判据表逐字「不按文件目录判」) | skill-reviewer | 设计 |
| **R5-5** ⭐ | **字段 Spec 的立项目标在主路径上不成立**: AI 渲染预览时照抄的是 `spec-drafter/SKILL.md:127-162` 的**内联骨架** (实测已与 SOT 漂移两处: 缺 `Created`、缺 `## Impact`; 全文 `关联 Issue` = **0**), 而本 Spec `:557` 的「不重复模板正文」**明令禁止修它** | skill-reviewer | 设计 |
| **R5-6** | **探针 Spec 唯一被机械钉住的指令是一个 9 字名词短语** (`每轮入口: 竞品 spec 探针`, SC-17 断言「计数恰 2」) ⇒ 插两行短语即全绿, 运行时 AI 无从知道跑什么 | skill-reviewer | 设计 |
| **选项 A** | **恒用回落形 `<spec-slug>-<uuid>`, 取消 issue 派生形** ⇒ 两个新字段 / K1 前半 / K2 / K4 / SC-1/4/15/27C/30/31 / D12 / 5 行 Impact **结构性消失** (≈27KB, 母 Spec 17%)。overlap 靠 `linked_issue` 不靠 track_id; 三方向 = 三 slug ⇒ **连坐被结构性消灭** | code-simplifier | **从未呈给 owner** |
| **选项 B** | **K1 应修类不修实例**: `ClaimRecord` 是 `@dataclass(frozen=True)` (`claim_schema.py:69`), 四处重建逐字同形 ⇒ `dataclasses.replace()` 一次修完且对未来每个 additive 字段免疫; 主控的 8 行透传表**下一个字段会原样复发** | code-simplifier | memory `fix-the-class` |

## 席位分歧 (主控独立裁决, memory `cross_agent_verdict_independent_verify`)

**K3 的「SC 降级」是否正当 —— 两席结论相反**:
- `feature-dev`: 「Closed (诚实, 正当), 不是 paper-fix」;
- `comment-analyzer`: 「**不正当, 且方向反了**」。

**主控独立核验后判: 两边各对一半, 按 SC 逐条裁**:
- **SC-1 / SC-4** 断言的是**派生属性** (改名不变性 / `#007`==`#7`) —— 确无代码宿主 ⇒ **降级成立, 维持**;
- **SC-15** 断言的是**生命周期** (release 旧 + acquire 新后无孤儿), 宿主 `release_claim_by_track:377` 与 `acquire_claim:99` **都实存**, 夹具手写两个串即可测 ⇒ **降级错误, 应回滚为代码类**;
- **SC-2** 可以是代码类, 但必须**改写它声称钉住的对象** —— 它钉的是 `linked_issue_overlaps` 的行为, **不是派生**; 原文声称钉派生才是恒绿的根源。

## 本轮实读**证实**的部分 (下轮免重复)

- K1 的两条承重事实**逐字精确**: `claim_lifecycle.py:244-256` 逐字段重建**恰 11 个字段**; `linked_issue=` 先例 **17 处 / 5 文件** (逐文件 4/1/1/5/6 全中);
- **K5 / K6 / K7 / K8 / K9 全部逐字或实跑成立**;
- 跨 skill import 先例 `handoff_autofill.py:403-407` **逐字节一致**; `release_claim_by_track` docstring `:396-399` 逐字一致 (**上一轮 grep-拼接的订正是对的**);
- 探针层 0 三臂对照 **9 个数字 + 簇成员零偏差重现**; 字段 spec 的 6 条 first-code-span / 14-of-14 / 9 份作用域判定**逐条命中**;
- 审计轨 §5 实测 **34 行 id 连续**, 6 处「见清单 #N」**全可 resolve**;
- `--phase A.1` **不会被 argparse 拒** (`:1191` 无 `choices=`); 全仓 `前置: REQUIRE claim` **恰 1 命中** ⇒ 新锚点未被占用;
- 母 Spec「§未做/存疑 #1」(spike S3 `:72` 未复核) 已由 factcheck 席代为核实, **FIX-18 勘误成立, 可关闭**。

## ⚠️ 主控本轮的两条自证 (Rule #10 留痕)

1. **第二次误标「逐字」**: `:238` 把一段引文归给 `coordination_probe.py:4-25`, 实读该文件**零命中** —— 真身在 `phase1_gate.py:1048` (实质结论仍成立, 该 probe `:18-21` 独立支持)。与本 session 早前的 grep-拼接是**同一类**: 没读源文件就标「逐字」。
2. **九次「只改叙述不改表」**: 见 R5-1。

> **factcheck 席在自己身上复现了同一条教训并主动留痕**: 它一度用带过滤的 grep 数审计轨表行得 17, 几乎误报一条 Critical「34 行只剩 17」; 改用不带过滤重数得 **34 行齐全**。⇒ memory `delegate-verify` 的「grep 只能定位不能取证」本轮**被两个独立主体各验证一次**。

## 收敛判定 (`max_rounds=5` 已用尽)

- **五席一致建议: 不要再加第 6 轮通用审计。** 理由各自独立: feature-dev「小而定向的修复, 不是新一轮 rework」· comment-analyzer「剩余是机械活不是设计活」· factcheck「22 条无一改变设计结论, 19 条可机械抓」· skill-reviewer「6/8 落在自己新写的条款上 = 75% > 拐点判据」· code-simplifier「前四轮 15 席全是正确性镜头, 没有一席问过『这条需要吗』」。
- **comment-analyzer 给出了可机械验收的收敛判据** (今天**三条全红**, 清账后应全绿):
  1. 正文出现的**每个 `SC-NN` 必须在 SC 表内有一行**;
  2. 正文出现的**每个 `--flag` 必须在 Impact 表内被点名**;
  3. **同一枚举全文只有一种拼写**。
  ⇒ 这比再跑一轮主观审计强得多: 它把「回灌」这件事变成了**可证伪的不变量**。

## 主控处置建议 (非裁定 — **AI 不自行选**, Rule #10)

**提问顺序很重要** (code-simplifier 席点明): **先问结构, 再问宿主, 最后问清账** —— 顺序颠倒会白做。

| 顺序 | 问题 | 若采纳的效果 |
|---|---|---|
| **①** | **要不要取消 issue 派生形, 恒用 `<spec-slug>-<uuid>`?** (选项 A) | 两个新字段 + K1 前半 + K2 + K4 + 6 条 SC + D12 + 5 行 Impact **结构性消失**; 代价 = **SC-1 的改名不变性丢失** (改名须 release+acquire 两步), 且同容器多方向互报一条 advisory 噪声 |
| **②** | **要不要给派生一个代码宿主?** (R4 选项 d) | 让 SC-1/2/4/15 从 AB fixture 回滚为代码类。**但若①已采纳, 派生缩为一行拼接, 这个模块会白建** |
| **③** | **清账方式**: (a) 一次机械清账 (三张表回灌 + 三处字面 + 三条 grep 不变量验收) / (b) 再跑 R6 通用审计 | 五席一致推荐 (a); **(b) 无人推荐** |
| **④** | **R5-3 (AB 推生产 ref) 是否单独先行处置?** | 它**与三份 Spec 的收敛无关**, 不修就会在下次跑 benchmark 时污染生产 `refs/aria/coordination`; 不该被收敛节奏挟持 |
| **⑤** | **K3 的部分回撤** (SC-15 恢复代码类 / SC-2 改写声称对象) 是否采纳主控的裁决? | 见「席位分歧」节 |
| **⑥** | 字段 Spec 的 `无` 哨兵是 **CJK-only**, 撞英文 AB eval 与跨项目分发面 —— (i) 扩为 `{"无","none"}` / (ii) 维持并成文「英文 proposal 亦不得译写」+ 同批改该 eval expectations | skill-reviewer 上呈, 属 owner 权限面 |
