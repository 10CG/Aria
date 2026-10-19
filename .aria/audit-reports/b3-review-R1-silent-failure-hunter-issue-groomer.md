---
checkpoint: b3-adversarial-review
mode: review
rounds: 1
verdict: FINDINGS (1 CRITICAL / 3 HIGH / 4 MEDIUM / 7 LOW)
timestamp: 2026-10-19 (B.3)
agents: [silent-failure-hunter]
---

# B.3 对抗审查 — silent-failure-hunter 席

正向面如实记: comments 三态+计数对账/坏 assessments 文件不冒充缺席/宽载严用两级/封闭 reason 枚举判序钉死/mini_validate 有牙齿/截断显式双字段/原子写语义正确。

## A. 静默吞错
- **A-1 [CRITICAL]** 整仓 fetch 失败 → exit 0 + diff.closed 谎报「已关闭」(占位标题) + build_next_state 驱逐该仓条目 (下轮回炉 new, 双向失真) + 文档「可整跑重试」被无条件 state 写废。修法选 (a): repos[].error 非空 ⇒ save_state 前抛 RuntimeError (exit 1, state 不动, 重试幂等)。
- **A-2 [HIGH]** rc=0+空 stdout 静默当空页 (fetch.py:251/314 + regen:154) — issue-list page 1 时整仓判零 issue 且零 error 面; comments 有计数对账兜底, issue-list 无对账 (schema open_issues 自述对账面落空)。修: batch is None ⇒ FetchError。
- **A-3 [MEDIUM]** 指纹降级态 (git_heads/handoff None) 零告知; 稳态 None==None ⇒ 上下文门对该分量永久失明 (只对转变沿成立)。修: stderr log + degraded 分量清单。

## B. fail-closed 撒谎
- **B-1 [HIGH]** scan_submodules 部分推导失败 ⇒ 作用域静默缩窄; ConfigError 只收口空集; 本仓默认生产路径即此 (scan_submodules: true 无 repos 键)。
- **B-2 [HIGH]** resolve_git_roots 静默缩窄 ⇒ 上下文门对未映射仓 fail-OPEN (Level 1 hotfix 不触发重评 — 与「宁重评不误复用」反向)。修: 显式 --repos 映射失败 ⇒ ConfigError; 自动推导失败 ⇒ 警告+degraded 面。
- **B-3 [LOW]** SKILL.md null 两成因漏第三 (gate 过但投影降级)。

## C. 不当回退: C-1 [LOW] DEFAULT_OWNER="10CG" 硬编码回退 (有 error 面, 备案)。
## D. 半状态
- **D-1 [MEDIUM]** state 先写报告后写; --out 失败 ⇒ 本轮 diff 永久吞。修: 报告写盘挪 save 前。
- **D-2 [LOW]** build_next_state 无 dup 检测 (本模块另两入口都有)。**D-3 [LOW]** SIGKILL 孤儿 tmp; regen 三文件非事务混代。
## E. 资源/边界
- **E-1 [MEDIUM]** normalize_issue 出 per-repo try, 「一仓挂不连坐」对数据形态错误失守。**E-2 [MEDIUM]** except ImportError 过宽 + pytest stub 毒井不回收 (与 code-reviewer Important-1 收敛)。**E-3 [LOW]** spec 字符串 vs (owner,repo) 去重键不一致, 别名双写炸指纹层归因误导。**E-4 [LOW]** 非 str title 裸 AttributeError; main catch 集不齐。**E-5 [LOW]** regen 计数字段缺席静默写矛盾语料。

优先处置: A-1+B-1+B-2 同族合并修 (run 级失败策略+作用域显式告知面); A-2 一行; E-2 几行消跨进程毒井。
