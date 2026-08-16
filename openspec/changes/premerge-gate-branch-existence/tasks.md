# Tasks: premerge-gate-branch-existence (Spec A)

> **Level**: **3** (proposal.md + 本文件) — 依 [DEC-20260816-002](../../../docs/decisions/DEC-20260816-002-fix-first-outcome-oriented.md) §2:
> owner 裁定「先修 bug」, 按 Level 3 走 A (Level 3 天然包含 Level 2 的交付面, 不欠交付),
> **版本档留到发版前再定** (版本只在发版那一刻承重, 不改变这三处代码怎么写)。
> ⚠️ **本文件⛔不得预写任何版本号字面量** —— 见 `TASK-013`。
>
> **A.2 入口状态**: post_spec `converged: false` · **`overridden_by_user: true`** (owner 2026-08-16) ·
> `max_rounds` 6 **仍余 1 轮未用** (override 不消耗它)。
> ⇒ **override 时仍有 4 条 `blocks_phase_b` 未闭合**, 由 `TASK-019` 显式承接, ⛔ 不得静默带过。
>
> **执行顺序的唯一 SOT = 各任务的 `依赖` 行**, 不是 TG 编号 (B 侧实测组号与 DAG 方向 7 处倒置, 两条编排面互相矛盾)。
> 🔴 **`后继:` 是非规范性导读, ⛔ 不参与调度** (本轮补) —— 它此前是本文件的**第二条编排面且与 SOT 矛盾**:
> `TASK-001` 写「后继: 全部」, 而实跑 `grep -n '依赖:' tasks.md` 逐行可验 —— **零个任务**把 `TASK-001` 写进 `依赖`。
> ⇒ 凡真正承重的先后关系**必须写进依赖方的 `依赖` 行**; 号一律写**全称 `TASK-0NN`**,
> ⛔ 不得用「`TASK-003, 004, …`」简写 —— 简写使机械提取只看得见第一个号 (旧版 `TASK-011` 的 8 个前置里 **7 个**对提取器不可见)。
> **行号约定**: 本文件一切 `:NNN` 以基线 `aria = af87cae` 为准 (本轮实跑 `git -C aria rev-parse --short HEAD` = `af87cae`, 工作树干净),
> 是**定位辅助不是验收量**; 一律按内容锚重定位。
> **求值时点约定**: 每条验收必须在**该任务完成的那一刻**可求值; 比较对象若由下游产生, 须拆半并在下游点名。

---

## TG-0 · 红窗与接缝 (必须先看到红)

- [ ] **TASK-001** **建立 18 条 SC 的红窗**, 逐条实跑今日值并留证。
      **交付**: `tests/` 下的失败用例集 + 一份逐条今日实测记录。
      **验收**: 18 条**逐条**有今日实测值; 其中 proposal SC 表标「必红 / 今日无核验 ⇒ green」的各条**当场为红**。
      ⚠️ **不是所有 18 条今日都该红** —— `SC-A-note (a)` 是负控, 今日**本就该绿**; `SC-A-sc22` 今日 PASS;
      `SC-A-baseline` 今日 111 passed。**把它们算成红是假红**, 把该红的算成绿是假绿, 两向都要点名。
      **怎么会红**: 任一条给不出今日实测值 (只写「应该会红」而没跑)。
      依赖: 无 · 后继: 全部

- [ ] **TASK-002** **建测试打桩接缝** (proposal §6 的 mixin) + **受控裸仓 fixture 工厂**。
      **交付**: `tests/test_pre_merge_gate.py` 的 mixin/fixture; 裸仓工厂 (建 `refs/heads/...` 受控组合)。
      **验收**: (a) 🔴 **总体先写明 (本轮更正 —— 上一稿写「四档」而实跑 proposal §打桩边界表 = **6 档**)**:
      与本任务相关的是**涉 subprocess / 打桩的前 4 档** (真实 `ls-remote`+受控裸仓 · 两种手段皆可 · 必须 mock ·
      走 §6 mixin 接缝), **各至少一条**用例跑通其档位要求; 后 2 档 (纯文件读取 · 元断言/全量跑) 结构上不经打桩接缝,
      **不属本任务**, ⛔ 不得被算进「各档」也⛔不得据此声称覆盖全表
      · 复跑总体 (⛔ 不钉行号, 按锚抽表):
      `awk '/^\| 档位 \| SC \|/{f=1;next} f&&/^\|---/{next} f&&/^\|/{c++;next} f&&!/^\|/{exit} END{print c}' proposal.md` = **6**;
      (b) `SC-A-sc22` 的既有守卫
      **仍拦得住真实 git 子进程** —— 用一个**故意违规的桩**验证它会红 (⛔ 放宽守卫而非建接缝的实现必红)。
      ⚠️ **可达前提 (全表适用)**: 11 条「断言核验确实发生」的 SC 必须显式提供可解析 mock backend
      (`probe()`→True · `precheck()`→`(True,"")` · `query_branch_in_flight` 返受控值),
      **⛔ 不得依赖 ambient `aether`/`gh` binary**;
      **唯一例外 `SC-A10c`**: 必须打桩 backend 但 `precheck()` 须返 `(False, …)` (它断言的就是那道早退);
      `SC-A10b` 须 mock `resolve_ci_backend` 返 `None`, ⛔ 不得依赖「这台机器碰巧没有 binary」。
      ⚠️ **前向兼容前提**: A 新增的**每一条**用例都必须**显式传 `main_branch`** (含三条负控) ——
      B 的 D5 会使该参数必填, 不传的 fixture 在 B 落地当天全部 `TypeError`。
      依赖: 无 · 后继: 003-012

---

## TG-1 · 代码实现 (`aria/skills/phase-c-integrator/scripts/pre_merge_gate.py`)

- [ ] **TASK-003** **新增 `--remote` 参数 (additive)** — `gate_check(..., remote: str = "origin")` 带默认值,
      并**接线 `main()` 的 `remote=args.remote`**。
      **验收**: `SC-A-cli` 转绿。**怎么会红**: 只加 `add_argument("--remote")` 而漏接线 ⇒ 查的仍是 ambient origin。
      ⚠️ 该 SC 的 fixture **必须自带受控 `origin`** —— 否则漏接线的实现会因无网络也返 128 而**意外全绿**。
      依赖: TASK-002

- [ ] **TASK-004** **分支存在性核验 — 判据是精确字符串比对**: 在解析出的 ref 名列表中查找
      `== "refs/heads/" + main_branch` 的**精确匹配**。
      ⛔ **不得读退出码** (`ls-remote` 零命中亦返 rc=0) · ⛔ **不得用 `--exit-code`** (无命中返 rc=2, 会被 catch-all 误分类)
      · ⛔ **不得用 pattern/锚定匹配**。
      **验收 (五条)**: `SC-A6` (受控裸仓只有 `wip/master`, 传 `master` ⇒ fail+`main-branch-not-found`) ·
      `SC-A13` (三个 glob `mast*`/`m[a]ster`/`maste?` 全 fail) · `SC-A-zero` (零命中仍 fail) ·
      **`SC-A11`** (负控: 受控裸仓中分支**确实存在** + mock backend 提供 in-flight runs ⇒ `verdict=wait` **不变**
      —— 核验⛔不得改变正常路径判决; ⚠️ 本条**不得打桩核验入口**, 打了就退化为恒真) ·
      **`SC-A-cwd`** (同一实现同一参数 `main_branch="master"`/`remote="origin"`, 分别以进程 cwd = W₁
      (`origin`→ 无 `master` 的裸仓) 与 W₂ (`origin`→ 有 `master` 的裸仓) 各跑一次 ⇒ W₁ fail+not-found、W₂ 不因核验 fail
      —— **任何不从进程 cwd 解析仓根的实现必红** (常量路径 / `__file__` / 脚本目录 ⇒ 两次得同一判决))。
      **怎么会红**: 读退出码的实现在 `SC-A-zero` 上必红; 锚定/pattern 实现在 `SC-A13` 上必红;
      恒判 not-found 的实现在 `SC-A11` 上必红; 不从 cwd 解析仓根的实现在 `SC-A-cwd` 上必红。
      ⚠️ **`SC-A-cwd` 的诚实限制 (proposal 逐字)**: 它**不能**区分「继承 ambient cwd」与「显式传 `cwd=`」——
      两者都过。那条要求由 proposal §3 正面规定承担, **无机械锚, ⛔ 不为它编造断言**。
      依赖: TASK-002

- [ ] **TASK-005** **核验点插入** — 落在 `enabled=false` / `backend is None` / `precheck` 失败**三道早退之后**,
      `evaluate_path_coverage` **之前**。
      **验收**: `SC-A-order` **两腿** — 腿 1 (顺序轴): 核验判 fail 时 `evaluate_path_coverage` **未被调用**;
      腿 2 (条件轴): 同 fixture 传 `config={"path_coverage_enabled": False}` 仍 fail+`not-found`。
      **怎么会红**: 腿 1 拦「插在 path coverage 之后」; 腿 2 拦「误嵌进 `if cfg.get("path_coverage_enabled", True):` 块内」
      —— 那是紧邻插入点最自然的误植位置, 而其余 17 条 SC 全用默认配置 ⇒ 对该误植全绿。
      另: `SC-A10` / `SC-A10b` / `SC-A10c` 三条负控各带 `assert ls-remote 未被调用` 转绿。
      依赖: TASK-004

- [ ] **TASK-006** **诊断信息** — `raw_message` 是**主通道**, `gate_error` 是 **additive 副本**。
      **验收**: `SC-A6` / `SC-A7` / `SC-A8` / `SC-A14 腿 1` 的 `raw_message` **含分支名与 remote 名**
      (写空串亦红); 六键 schema 零改动, `gate_error` 为可选新增键。
      依赖: TASK-004

- [ ] **TASK-007** **异常与重试 — 按轴分派两个既有先例, ⛔ 不得再造第三份**:
      异常轴复用 `path_coverage.py:93` 的元组; 重试轴复用 `aether.py:38`。
      **验收**: `SC-A7` (rc=128 ⇒ fail+`main-branch-verify-failed` 且**未重试**) ·
      `SC-A8` (`TimeoutExpired`, mock `time.sleep` ⇒ 3 attempts 后 fail) ·
      `SC-A14` **两腿** — 腿 1 参数化探针 (`FileNotFoundError`/`OSError`/输出不可解析/`UnicodeDecodeError`/
      **任取一个不在实现 `except` 元组里的异常类**) 一律 fail+`verify-failed`;
      腿 2 **出口净化**: 喂含孤立代理码位的 stderr, 对 `out["raw_message"]` 与在场时的
      `out["gate_error"]["message"]` 各跑 `s.encode("utf-8","strict")`, **两次均不得抛**。
      ⚠️ `issubclass(UnicodeDecodeError, OSError)` = **False** ⇒ 照 §5 两轴逐字照做 + `text=True` 的实现,
      `UnicodeDecodeError` 会**裸抛穿过 `gate_check()`**。
      依赖: TASK-004

---

## TG-2 · 文档同步 (不可协商规则 #3) — `aria/skills/phase-c-integrator/SKILL.md`

- [ ] **TASK-008** **hunk ① — §C.2.4 执行流程新增步骤**。
      **验收**: `SC-A-step` 三腿。🔴 **两个锚一律取 `### C.2.4` 标题行 (今日 `:218`) 之后、下一个 `###` 标题行
      (今日 `:306`) 之前的首个匹配**, ⛔ 不得对锚点短语做不限章节的全文件搜索 —— 本轮补齐**终点**锚 (上一稿只限定了起点),
      依据 proposal `SC-A-note` 逐字「⚠️ `SC-A-step` 的起点/终点锚同受本条约束」。
      区块 = `**执行流程**:` 与 `**Subprocess 调用规范**:` 之间
      (⚠️ 起点锚**必须写「首个」** —— 我实跑 `grep -n '\*\*执行流程\*\*:' SKILL.md` 全文件命中 `[238, 582]`,
      取末次匹配得起点 582 > 终点 257 ⇒ 空/负区间 ⇒ 恒红; 终点锚我实跑得**唯一** (`257`), 但**唯一性今日成立 ≠ 被写死**,
      故一并纳入章节限定 —— 这正是 `TASK-019` 第 3 条那类 finding 的形状),
      按出现顺序提取行首步骤编号: **(a)** 存在 `N` 满足 `2 < N < 2.5`; **(b)** `N` 的位置恰在 `2` 与 `2.5` 之间;
      **(c)** 该步骤正文 (自编号行起到下一个行首编号行前, **含缩进续行**) ⛔ 不含任何 `--` 起头的 CLI flag 字面量
      · ⛔ 不含 `aether ci status` · ⛔ 不含 `aether `/`git `/`python3 `/`bash ` 起头的裸命令; 且**含** `#137`。
      **今日实测**: 该区块编号序列 = `1. 2. 2.5. 3. 4. 5. 6.` ⇒ 区间 `(2, 2.5)` 内**零编号** ⇒ **今日必红**。
      ⚠️ **R3 改判后的对抗验证尚未成套复跑** (proposal 逐字标注「本轮未重跑」) ⇒ **本任务须补跑**
      「1 好 + N 坏」四个新判别点: 起点锚取末次匹配 ⇒ 应恒红 · 违规命令写在缩进续行 ⇒ 应 `RED(c-禁3)` ·
      正文含 `--pr-branch` ⇒ 应 `RED(c-禁1)` · `SC-A-note (d)` 只改 SKILL.md 不改 docstring ⇒ 应 `RED(d)`。
      依赖: TASK-005

- [ ] **TASK-009** **hunk ② — Output schema json 块增 `gate_error` 键**。
      **验收**: `SC-A-doc` — 从 json 块**实际解析**出的**顶层**键名集合 == `_build_output` 实产键全集。
      **解析规则 (⛔ 规定不是建议)**:
      🔴 **规则 0 — 区块定位 (本轮新补; 上一稿此处缺失, 而 `TASK-019` 第 3 条却声称本任务「已按该规则写」)**:
      json 块 = `### C.2.4` 标题行 (今日 `:218`) 之后、下一个 `###` (今日 `:306`) 之前的**首个** `**Output schema**` 锚
      之后的 json 围栏 (今日 `:265`–`:277`), ⛔ 不得对该锚做不限章节的全文件搜索。
      **今日实测 (我复跑)**: `grep -n '\*\*Output schema\*\*' SKILL.md` = **`264` 与 `501`** 两行; `:501` 属
      `### C.2.4.5 Submodule Pointer Regression Gate`, 其顶层键 = `verdict` / `affected_submodules` / `telemetry_files`
      (**3 键**, 与 `_build_output` 的 7 键**只共享 `verdict` 一个** —— ⚠️ 我不照抄审计席「无一重叠」那句, 实读得共享 1 个;
      结论不变: 集合**永不相等** ⇒ 取末次匹配的实现**对任何实现恒红**)。
      **规则 1** ⛔ 不得用 `json.loads` (块内 `"verdict": "green" | "wait" | "fail"`
      是 pipe 联合伪类型, 实跑抛 `JSONDecodeError`); **规则 2** 只取**行首恰两个空格**的 `"<key>":`
      (正则 `^  "([A-Za-z_]+)":`, 多行模式) —— 朴素 `"key":` 正则实测取到 **16** 键, 与 code 侧永不相等 ⇒ 恒红。
      **今日实测**: doc 侧 7 / code 侧 7 相等。**怎么会红**: 只落 `.py` 而漏 schema 键 (或反之); 单独回退该 hunk。
      依赖: TASK-006

- [ ] **TASK-010** **hunk ③ — 早退分支归纳句 + `_build_output` docstring 同步**。
      **验收**: `SC-A-note` 四腿。区块取 §C.2.4 内 Output schema json 围栏结束行之后、`**配置参数**:` 之前;
      ⚠️ **两个锚一律取 `### C.2.4` 标题行之后、下一个 `###` 之前的首个匹配** (实跑该两锚全文件 4 行:
      `264/281/501/523`, 后两者落在 §C.2.4.5 且结构同形 ⇒ 取末次匹配会抓错块, (a) 恒绿 (b)(c) 恒红)。
      **解析规则**: 先 `re.sub(r'\s+','',区块)` **抹掉全部空白**再匹配 (docstring 里那句被 Python 换行拆开,
      不抹空白则锚零命中 ⇒ (d) 恒红; 压成单空格也不行, CJK 换行处会留空格)。
      四腿: **(a)** 负控 —— 「保持六键不变」括号内枚举**仍恰 4 项**且不含 `main-branch`;
      **(b)** 区块另有一处同时含 `gate_error` 与 `main-branch`; **(c)** 含逐字 `无 path_coverage`;
      **(d)** 对 `_build_output` 的 docstring (经 `ast.get_docstring` 取, ⛔ 不得按行号切) 跑同款三问。
      **今日实测**: (a) 绿 (负控本就该绿) · (b)(c)(d) **必红**。
      依赖: TASK-006

---

## TG-3 · 验收收口

- [ ] **TASK-011** **18 条 SC 逐条转绿**, 并对每条贴实跑输出。
      **验收**: 18 条**逐条**给出转绿证据; 且**与 TASK-001 的今日值逐条对照** (红→绿 / 本就该绿的仍绿)。
      **怎么会红**: 任一条只贴「PASS」而无法与 TASK-001 的红窗对上; 或负控由绿变红。
      🔴 **`TASK-001` 本轮补进依赖 (上一稿缺)**: 本条验收逐字要求「与 `TASK-001` 的今日值逐条对照」⇒ **比较对象由 `TASK-001` 生产**,
      而上一稿的依赖行不含它 ⇒ 照「依赖行是唯一 SOT」调度的执行者可在红窗记录尚不存在时开工 ⇒ **本条验收结构上不可求值**。
      依赖: TASK-001, TASK-003, TASK-004, TASK-005, TASK-006, TASK-007, TASK-008, TASK-009, TASK-010

- [ ] **TASK-012** **全量套件基线**。
      **验收**: `SC-A-baseline` — `phase-c-integrator` 全量套件 **基线 + 新增 ≥ 全绿**, 零回归。
      ⚠️ **⛔ 不得照抄 `111`** —— 该数是「基线 `af87cae` 且 B 尚未 ship」这个时序下的量; B 的 `TASK-010`/`TASK-021`
      会改同一套件的用例数与调用形状。**若 B 先 ship, 必须以 B ship 后的实跑数重定基线**
      (新鲜度只能获取不能测量)。**本任务须先记录取数时点与当时的 B 侧状态, 再给数。**
      依赖: TASK-011

---

## TG-4 · 交付义务 (proposal §交付义务 逐字: 「A.2 须为下列六项**各出一条 task**; ⛔ 不得因『变更小』跳过」)

- [ ] **TASK-013** **O-1 发版同步面**: `aria` 子模块 5 文件 (`plugin.json` SOT + `marketplace.json` + `VERSION`
      + `CHANGELOG.md` + `README.md`) + **主仓 gitlink** + 主仓 `VERSION` + root README badge + i18n README。
      **验收**: 逐项贴 `git show --stat` / `git diff` 证据; **gitlink 一项须贴
      `git show --submodule=short <ship-commit> -- aria`** 显示指针前后两个 SHA。
      ⚠️ **⛔ 不得用 `git diff --submodule=short`** —— 实测它在提交后**恒空**, 已 bump 与从未 bump 的仓输出**逐字节相同**,
      对唯一要防的方向零区分力; 换用的命令实测对已 bump 的 commit 输出两行 `Subproject commit`, 对未 bump 的输出 0 行。
      ⚠️ **本项无机械兜底 — 本 Spec 不假装它有**: `m6-version-badge-match` 只比 badge ↔ `plugin.json`;
      §C.2.4.5 判 no-change = PASS; §C.2.5 与双推 `ls-remote` 核的是另一条轴。
      ⚠️ **版本号字面量由发版时计算, 本文件⛔不预写** (版本档按 DEC-20260816-002 留到发版前裁)。
      ⚠️ **求值时点**: gitlink 一项的比较对象由 **Phase C.2** 产生 (子模块本地 merge + 双推之后主仓才 bump)
      ⇒ 该项**不计入 Phase B 完成判据**, 但⛔**不得因此从本任务删除**。
      🔴 **下游落点本轮点名 (上一稿只写「须在 Phase C 交接材料里显式列出」—— 「交接材料」不是本文件里的任何具体落点,
      等于把半条挂在一个没有地址的下游)**: 落点 = 本文件 `## D.2 交接事实` **第 2 条**。
      ⇒ **本任务完成判据 = 该条已在场** (机械可查, 当场可求值); **该条自身的求值**留 Phase C.2, 由那一条自己承担。
      依赖: TASK-012

- [ ] **TASK-014** **O-2 Rule #6 照跑 AB (第二行, 零裁量, 本 Spec 不申请任何豁免)**。
      **验收**: 两套件 `ab-suite/phase-c-integrator.json` + `ab-suite/phase-c-integrator-pre-merge-gate.json`
      **各跑完**, 结果落 `ab-results/`; 并**带上 §Rule #6 已成文的有效性限定**。
      ⚠️ 本 change 确实改 `SKILL.md` 的**指令流程** (hunk ①) ⇒ 判据表**第二行**, 无豁免空间。
      依赖: TASK-011

- [ ] **TASK-015** **O-3 「不得据 A ship 关闭 #137」的仓外落点**。
      **验收**: 在 #137 留下逐字说明「A 只加固了 `gate_check()` 这一份实现; `SKILL.md` 散文流程那份
      由 B 侧 D1 承接 ⇒ **A ship 不构成 #137 闭环**」。
      ⚠️ **仓外写动作** — owner 已于 DEC-20260816-002 §3 裁定 3「**全报**」授权, 但**逐件先把标题 + 正文给 owner 过目再发**
      (🔴 本轮更正转录漂移: DEC 逐字是「逐件先把**标题+正文**给 owner 过目再发」, 上一稿只写了「正文」, 漏「标题」)。
      依赖: TASK-012

- [ ] **TASK-016** **F-1**: 抽取共享重试 helper (`_run_with_retry` 跨 backend 抽象) 开 follow-up issue。
      **验收**: issue 已建且编号回写本文件。⚠️ 仓外写动作, 同 TASK-015 的授权与过目要求。
      依赖: TASK-007

- [ ] **TASK-017** **F-2**: catch-all 不重试在 **168h 无人值守**下的可用性权衡, 开 follow-up issue。
      **验收**: 同上。依赖: TASK-007

- [ ] **TASK-018** **F-3**: 同形兄弟位置 (`fetch_gate.py` / `worktree_manager.py:170`) 开 follow-up issue。
      **验收**: 同上, 并带 §非目标 的去重规则。依赖: TASK-007

---

## TG-5 · 承接 override 时未闭合的项

- [ ] **TASK-019** **逐条承接 post_spec R5 遗留的 4 条 `blocks_phase_b`** —— 每条**要么修, 要么显式声明不修+理由**,
      ⛔ 不得静默带过 (owner override 只是放行进 A.2, **不是判定它们已解决**)。
      1. **M-1** `CLAUDE.md:113` 规则 #8 的 SOT 同步在 A/B 划界里无归属, 而其触发点是 A 的 ship
         (⚠️ 该条的归属曾在 DEC-20260816-001 被裁「移交 A 侧」, 但该 DEC **全部作废** ⇒ **回到未裁**, 须重新上呈);
      2. **M-2** B 的 `TASK-013` (pending) 与 A 的 hunk ②③ **是同一份交付物** —— 跨 Spec 重叠, 须定归属;
      3. **code-reviewer M-2** (报告 `.aria/audit-reports/post_spec-R5-3-premerge-gate-branch-existence-code-reviewer.md`
         §1 的 `M-2` 小节) 「章节内首个匹配」规则逐字只扩到
         `SC-A-step`, **漏了 `SC-A-doc`**。
         🔴 **本轮更正上一稿的假声称**: 上一稿此处逐字写「本文件 `TASK-009`/`TASK-010` 已按该规则写」——
         **我实读为假**: `TASK-010` 写了, **`TASK-009` 一个字都没写**。⇒ 这条承接项**在声称闭合的同时并未闭合**,
         正是它自己承接的那个 finding 的形状。**本轮已补**: `TASK-009` 加「规则 0 — 区块定位」· `TASK-008` 补终点锚章节限定。
         **本任务剩余的那一半 = proposal SC 表自身仍未同步** (`SC-A-doc` 行的操作数定义仍只写「实际解析」而无定位算法)
         —— 那是 **proposal 的勘正面**, 由本任务落实或上呈, ⛔ 不得因「tasks.md 这边已修」就算本条闭合;
      4. **knowledge-manager** 一条 —— 🔴 **本轮精确化 (上一稿只写「一条 (锚点唯一性同族)」, 无 locator、不可核)**:
         该席报告 `.aria/audit-reports/post_spec-R5-4-premerge-gate-branch-existence-knowledge-manager.md`
         自标 `blocks_phase_b` 的是**两条**:
         **§1** (`SC-A-doc` 锚未纳入「章节内首个匹配」, 逐字「blocks_phase_b: 建议是」) 与
         **§2** (`CLAUDE.md:113` Rule #8 因 A 新增第三条阻断腿而失实且无人认领, 逐字「blocks_phase_b」);
         而 aggregate 的席位表把 knowledge-manager 计为 **1** ⇒ **其中一条已与别席去重**
         (§1 ≡ 上面第 3 条 · §2 ≡ 上面第 1 条)。
         ⛔ **本条⛔不得因「都是重复」就一笔勾销** —— 处置须**逐条写明去重映射成立与否**;
         另该席 §3 (B 侧 `detailed-tasks.yaml` 因 6 条 `cancelled` 留下悬空依赖边, Major, `introduced_by_r4fix: 是`)
         **未被标 `blocks_phase_b`**, aggregate 声称「✅ 已补执行」—— 该声称**由 B 侧文件承载, 本任务须去 B 侧实测复核**
         (memory `cross_doc_claim_verify_at_target`: 文档 A 写「已在 B 做了 X」必去 B 实测), 复核结果写进处置记录。
      **验收**: 4 条逐条有处置记录 (含第 4 条的去重映射逐条判定 + §3 声称的 B 侧实测复核);
      属跨 Spec 或需 owner 裁的**上呈而非自决** (规则 #10)。
      依赖: 无
      🔴 **⛔ 阻断维度 — 本轮改回原判 (上一稿把它降了一级)**: 这 4 条审计原判逐字是 **`blocks_phase_b`**(阻断 **Phase B**),
      上一稿写成「未完成前不得进 **Phase C**」并配「可与 TG-1 并行」⇒ **等于 AI 自行把闸门放宽一整个 Phase**
      (规则 #10: 不得以任何价值评估跳过、降级或**改序** enabled 闸门的判定; owner override 逐字只是「放行进 A.2」)。
      ⇒ **本文件按原判记 = 阻断 Phase B**。⚠️ 其中第 1、2 条**结构上需 owner 裁**(一条回到未裁、一条跨 Spec 归属)
      ⇒ 照原判则 Phase B 卡在 owner 上。**「是否允许 TASK-019 与 Phase B 并行」是 owner 的裁量, 不是执笔方的** ——
      已列入 handoff 待裁, ⛔ 本文件不代裁、不预设答案。

---

## D.2 交接事实 (非 task, 但必须写进 handoff)

**1. A ship 会打爆 B 侧三条任务级预写量**: B `tasks.md:85` 的「24 处」· B `detailed-tasks.yaml:488` 的「显式传 0 处」·
B `tasks.md:122` 的基线 `111`。**A 不改 B 的这三处** (跨轨改会撞车), 但**必须交接**。

**2. `TASK-013` (O-1) 的 gitlink 半条 —— 求值时点落在 Phase C.2, 由本条承接** (🔴 本轮新增, 承 `TASK-013` 的显式点名):
A ship 的主仓 gitlink bump 只有在**子模块本地 merge + 双推之后**才存在比较对象 ⇒ 该项在 Phase B 完成时**结构上不可求值**。
**Phase C.2 须贴的证据 (逐字, 不得改量)**: `git show --submodule=short <ship-commit> -- aria`, 输出须含
`-Subproject commit …` / `+Subproject commit …` **两行**。
⛔ **不得改用 `git diff --submodule=short`** —— 我本轮实测: 干净工作树上它 **0 行**, 而 `git show` 对已 bump 的 commit
(`fb5ed36`) 输出 **2 行** `Subproject commit`、对未 bump 的 (`98ad1f5`) 输出 **0 行** ⇒ 只有后者两向可区分。
⚠️ **本项今日无任何机械兜底** (`m6-version-badge-match` 只比 badge ↔ `plugin.json` · §C.2.4.5 判 no-change = PASS ·
§C.2.5 与双推 `ls-remote` 核的是另一条轴) —— 见 proposal 文首 `D-b`, **本文件不假装它有**。

---

## 计数与自查

> ⚠️ **本节的数是实跑出来的, 不是写下来的** —— 每条都给了复跑命令。
> 🔴 **第一稿的自查曾声称「18 条 SC 全部有 owning task」而实测漏了 2 条** (`SC-A11` / `SC-A-cwd`),
> 由落盘后的机械自检当场抓到并补进 `TASK-004`。**逐字留痕**: 那正是本仓反复抓的
> 「声称完整而实际不完整」形状 —— 出现在一份**专门为防它而写**的清单的自查段里。
> 🔴 **第二稿 (换执笔方后) 又在本节抓到同形状 3 处, 一并留痕**: (i) SC 覆盖的 owning-task 映射漏写 `TASK-002`
> (它是 `SC-A-sc22` 的 owner, 而映射只写「TASK-003~010」); (ii) SC 覆盖的复跑命令是**朴素 grep**,
> 对 `SC-A10` 这类**前缀家族**天然失明 —— 我在上一稿上朴素法与加边界法各跑一遍, 两者对该号**给出不同的数**,
> 即「`SC-A10` 这一条整条消失, 朴素法照样绿」(⛔ **此处不钉具体计数** —— 那个数随任何人多提一次该号而变,
> 钉下来就是又一条自指判据; 承重的是「**朴素法对前缀家族失明**」这个性质); (iii) `TASK-002` 声称「打桩边界表**四档**」而实跑该表 = **6 档**。
> ⇒ **本节的每条「全部 / 逐条 / 各」都必须带一条今日实跑得出的命令与数, 命令本身也必须先被对抗验证过**
> (memory `adversarial-fixture`: 验断言要验它**拒不拒得掉坏实现**, 不是当前取值对不对)。

- **任务数**: **19** (TG-0: 2 · TG-1: 5 · TG-2: 3 · TG-3: 2 · TG-4: 6 · TG-5: 1)
  · 复跑 `grep -cE '^- \[[ x]\] \*\*TASK-' tasks.md`
  · 🔴 **本轮换掉旧命令 `grep -cE '^- \[ \] \*\*TASK-'`**: 它把**未勾选**写进了 pattern ⇒ 任一任务被勾掉即得 18 ≠ 19,
  而它转红与「任务数是否仍为 19」**无关** —— 一条在本清单**被正常执行的过程中必然转红**的判据。
  对抗验证 (我实跑, 在 scratch 副本上做): 副本里勾掉一条任务后, **旧命令少算 1 (红) 而新命令仍得 19** ✅
- **SC 覆盖**: **18/18** 有 owning task。映射 (🔴 本轮补 `TASK-002`, 上一稿漏):
  `TASK-001` 建红窗 → **`TASK-002`** (`SC-A-sc22`) + `TASK-003`~`TASK-010` 转绿 → `TASK-011`/`TASK-012` 收口
  · 复跑 (⛔ **必须带边界**, 否则前缀家族假绿):
  `for sc in $(grep -oE '^\| \*\*(SC-A[A-Za-z0-9_-]*)\*\*' proposal.md | sed 's/^| \*\*//; s/\*\*$//'); do printf '%s %s\n' "$sc" "$(grep -cE "${sc}([^A-Za-z0-9_-]|\$)" tasks.md)"; done`
  **18 行应全部 ≥ 1** (我实跑: 18/18 全部 ≥ 1)
  · ⚠️ **计数 ≥1 只证明「被提到」, 不证明「被拥有」** —— owning task 由上一行的**显式映射**承担, 本计数只作**漏项闸门**;
  ⛔ 也**不得**把各号的具体计数写死进本文件 (任何人多提一次某个号, 那个数就变 ⇒ 又一条自指恒红判据)
  · 总体计数 `grep -cE '^\| \*\*SC-A' proposal.md` = **18** (我实跑; 操作数是 proposal, 非本文件 ⇒ 无自指)
- **交付义务覆盖**: O-1/O-2/O-3/F-1/F-2/F-3 **六项各一条 task** (`TASK-013`~`TASK-018`), 符合 proposal 逐字要求
  · 复跑 `for o in O-1 O-2 O-3 F-1 F-2 F-3; do printf '%s:%s ' "$o" "$(grep -cE "^- \[[ x]\] \*\*TASK-[0-9]{3}\*\* \*\*$o" tasks.md)"; done` **应全为 1**
  · 🔴 **本轮把命令锚到任务行**: 旧命令的操作数是**整份文件**且只匹配「粗体 + 义务号」, 今日恰为 1 纯属自查段
  碰巧没以那个形态写过义务号; 对抗验证 (我实跑, 在 scratch 副本上做, ⛔ 字面样本不写进本文件):
  副本文末补一行**以粗体形态提及某个义务号**的自查话 ⇒ **旧命令得 2 (红) 而新命令仍得 1** ✅
  —— 与下面那条同族: **判据的操作数落在本文件自身时, 后来者写下一句话就能把它弄红**
- **未闭合项覆盖**: 4 条 `blocks_phase_b` → `TASK-019` (⚠️ 其阻断维度按原判 = **Phase B**, 见该任务内的留痕)
- **依赖完整性**: 依赖行引用的 TASK 全部已定义, **零悬空**
  · 复跑 `comm -23 <(grep -oE '依赖: [^·]*' tasks.md | grep -oE 'TASK-[0-9]{3}' | sort -u) <(grep -oE '^- \[[ x]\] \*\*TASK-[0-9]{3}' tasks.md | grep -oE 'TASK-[0-9]{3}' | sort -u)` **应为空**
  · 🔴 **上一稿此处只有散文「提取…求差」而无可跑命令**, 且当时 `TASK-011` 的依赖行用简写 (`TASK-003` 之后只写裸三位号)
  ⇒ 该提取器**只看得见 8 个前置里的第 1 个**, 「零悬空」这个结论有 7/8 的盲区。本轮已把该行改为全称。
  对抗验证 (我实跑, 在 scratch 副本上做): 注入一条指向**未定义号**的依赖行后, 命令把该号打印出来 (红) ✅
  · ⛔ **对抗用的假号⛔不得以字面形式写进本文件** —— 我本轮第一次写留痕时正是把它写成了字面,
  当场把这条判据变成**恒红** (自查实跑抓到)。**判据的操作数是整份文件时, 举例就等于注入。**
- ⛔ **不含版本号字面量** (版本档未裁)
  · 复跑 `grep -oE '(^|[^0-9C.])[0-9]+\.[0-9]+\.[0-9]+' tasks.md` **应为空** (我实跑 = 空)
  · 🔴 **本轮换的是量, 不是阈值** (memory `redfix-change-quantity`): 旧命令按**值**硬排除**某一个**章节号,
  于是本文件将来引用**任何别的**章节号都会把它弄红 —— 而那与「是否预写了版本号」无关。
  对抗验证 (我实跑, 均在 scratch 副本上做, ⛔ 字面样本不写进本文件):
  (i) 副本加一个**新章节号** ⇒ **旧命令红 / 新命令仍空** ✅;
  (ii) 副本加一个**带 `v` 前缀的三段串** ⇒ 新命令红 ✅;
  (iii) 副本加一个**裸三段串** ⇒ 新命令红 ✅。
  新命令排除的是**形状**(前导字符为 `C`/数字/点 ⇒ 章节号), 不是某个具体值
- ⛔ **不含对不存在文件的机械判据委派** —— 🔴 **本轮由点名法升级为类级** (memory `fix-the-class`;
  与 proposal 把 `SC-A-step (c-禁1)` 从点名 `--main-branch` 升级为「任何 `--` flag」是同一处方)
  · 复跑 (**类级**: 本文件引用的每个文件名 token 都必须在仓内真实存在)
  `grep -oE '[A-Za-z0-9_./-]+\.(py|md|json|yaml)' tasks.md | sed 's#^\(\.\./\)*##' | sort -u | while read -r p; do [ -n "$(find /home/dev/Aria -path "*/$p" -not -path '*/.git/*' -print -quit)" ] || echo "MISSING: $p"; done`
  **应为空** (我实跑 = 空)。对抗验证 (我实跑, 在 scratch 副本上做, ⛔ 字面样本不写进本文件):
  副本里注入**两个仓内不存在的文件名** —— 一个**带路径前缀**、一个**裸文件名** —— **两者都被报 MISSING** ✅
  ⇒ 该判据对「带路径」与「裸名」两种写法**都拦得住**, 不再依赖某个具体名字
  · ⚠️ **为什么废掉点名法**: 旧判据只认识**一个**历史文件名, 下一次把机械判据委派给**另一个**不存在的文件时它全绿
  —— 正是 proposal 把 `SC-A-step (c-禁1)` 从点名一个 flag 升级为「任何 `--` flag」时诊断过的同一个病。
  · ⚠️ **旧判据同时还是自指恒红的**: 它的操作数是本文件自身, 而**要禁的那个 token 必须被写下来才能解释禁令**
  ⇒ 「描述它」就「违反」它 (B 侧逐字留痕过的形状的**镜像形态**)。
  ⇒ **本轮的处置 = 换操作数, 不是调 pattern**: 类级命令的操作数是**文件系统**(某路径是否真实存在),
  本文件里写什么都不改变它 ⇒ **结构上不可能自指**
