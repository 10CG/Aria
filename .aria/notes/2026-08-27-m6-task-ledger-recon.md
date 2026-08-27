# M6 `aria-2.0-m6-dispatch-input-delivery` — 账目核实结果 (2026-08-27)

> **怎么来的**: owner 指派动态工作流 + agent team。按 TG 分六组并行核实 (A.3 锁定的
> backend-architect / qa-engineer / knowledge-manager 各司其职), 每组核实完立刻由
> `aria:code-reviewer` 做**对抗轮**试图推翻 done 判定。11 agents / 0 error。
> 判定纪律: 逐条对照 task 的 `verification`; 代码存在 ≠ 完成; **文档存在 ≠ 动作已执行**。

## 结论: done **17** / in_progress **10** / pending **3** (对抗轮推翻 **5** 条)

**代码侧基本完成, 卡的是四道执行门 + 六处测试补强。** 此前 yaml 显示「30/30 未勾、已 54 天」
是账目失真, 不是进度真相。

## 四道门的真实状态 (owner 关心的那四个)

| 门 | TASK | 判定 | 差什么 |
|---|---|---|---|
| build | TASK-021 | **partial** | 需要 owner 实际触发 /aether:aether-build-container (或手工 docker build) 对 post-merge master SHA 构建镜像并 push 到 forgejo.10cg.pub/10 |
| deploy/freeze | TASK-022 | **not_done** | TASK-021 的真实构建必须先完成 (前置依赖) |
| egress | TASK-028 | **not_done** | 需要 owner/infra 在真实 Aether heavy-node 上实际执行 nomad/jobs/aria-smoke-forgejo-egress-probe.hcl (文档 §2.1 给出的现成 HCL), 并用 `nomad |
| E2E | TASK-029 | **not_done** | 依赖 TASK-028 (egress probe) 先产出真实 PASS 结果 —— 该依赖未满足 |

⇒ 四门**没有一道是待决策**, 全部是待执行的基建动作, 且互为前置: 021 → 022, 028 → 029。

## 对抗轮推翻的 5 条 (最有价值的产出)

### TASK-003 (TG-1) — 原判 `done` → **`partial`**

AC-3 的 body 半边零验证 + 证据含不存在的事实。反事实实证: 在副本 modes/initial.sh:567 把 `ARIA_ISSUE_DESCRIPTION=$(wrap_untrusted_content "$(sanitize_issue_text "$RAW_BODY")")` 换成常量 "BODY_DROPPED_COUNTERFACTUAL"(等于抓回的 issue body 整个丢弃), 整套集成仍 `5 PASS / 0 FAIL` —— 没有任何断言检查 fetched body 是否经 envsubst(:637 WHITELIST) 进入 rendered prompt。title 半边确实被验证(空 title 在 :561-563 die, scenario 1 exit 0 反证 title 来自 ISSUE_URL), target_repo 也真被 META 驱动(否则 clone 失败)。但他写的 “integration ... stderr 含 title/body 已用” 是不存在的: 对一次真实 scenario-1 run 做 `grep -n -i "fix the thing|title" $ws/stderr.log` 返回空, `grep -n -i title modes/initial.sh` 证实全文无任何打印 title/body 的 log 行, scenario_fetch_happy_path(:215-232) 的 5 条 check 也没有一条碰 title/body 内容。另 AC-5 点名的 files_hint(:545 NOMAD_META_FILES_HINT→ARIA_FILES_LISTING) 无任何测试设置过该 env(grep 全套件 0 命中), 属次要(proposal:111 标 optional)。代码实现正确, 故 partial。补法: scenario 1 断言 rendered prompt/PR body 含 fetched body 字面量 + 

### TASK-008 (TG-1) — 原判 `done` → **`partial`**

verification 硬性要求 “RED test MUST exercise the REAL initial.sh call-chain”, 但该测试对本 fix 是重言式, 撤销 fix 也全绿。反事实实证: 在副本把 modes/initial.sh:880 的 `if [[ "$INPUT_MODE" == "fetch" ]]` 改成 `== "__NEVER__"`(即撤销 TASK-008 的跳过, compute-assertions.sh call-site 无条件执行), 重跑集成套件 scenario_fetch_happy_path 5 条 check 全 PASS, 含那条 “assertion-results.json NEVER created (call-site SKIPPED, TASK-008)”。原因: fetch 模式无 issue.yaml, lib/compute-assertions.sh 在 :37-39 就 exit 1, 本来就写不出 assertion-results.json; 而 ASSERTION_MISMATCH 死路已被 TASK-009 的 :906 `if [[ "$INPUT_MODE" == "fetch" ]]` 分支拦掉。撤销前后唯一可观测差异是 stdout.log 多一行 `ERROR: issue yaml not found: .../inputs/ARIA-testrepo-42/issue.yaml`(我实跑打印确认), 而 :893 的 `2>&1 | tail -5` 把它送 stdout, 没有任何断言看。测试文件自身 :16-25 也承认 `RED reproduction (pre-fix history, not re-run here)` —— RED 从未在本套件跑过, 他 “符合 verification 里对 RED-test-at-real-call-site 的明确要求” 的判断不成立。代码(:880-891 只 log 不落 stub)是对的, 故 

### TASK-013 (TG-2) — 原判 `done` → **`partial`**

extension.py:2262/2265/2268 向 Nomad dispatch meta 新写 TARGET_REPO/BASE_BRANCH/FILES_HINT 三个键, 但生产 job HCL 从未声明它们: nomad/jobs/aria-layer2-runner.hcl:64-70 meta_required 仍是 5 键 (ISSUE_ID/ISSUE_URL/DISPATCH_ID/IMAGE_SHA/IDEMPOTENCY_KEY), :100-117 meta_optional 仍是 BUDGET_CAP_USD/TRIAGE_BODY_JSON/PROMPT_PATH/REWORK_MODE/REWORK_FEEDBACK/PARENT_PR_ID/REWORK_OF/REWORK_ROUND/TARGET_NODE; 我实跑 `git diff --stat daf7c79..HEAD -- nomad/` 输出为空 (整个分支没动过 HCL)。Nomad dispatch 校验对 meta_required ∪ meta_optional 之外的键直接拒绝 (unpermitted metadata keys), 即每次 autonomous dispatch 都会在 S4_LAUNCH 被拒; 而容器侧 docker/aria-runner/modes/initial.sh:543-545 读 NOMAD_META_TARGET_REPO, :575 拿不到即 die。仓内先例证明这是成对动作: docs/architecture-decisions.md:3611 记 Spec Y 是 'T-pre.1 (Layer 1 extra_meta) + T-pre.2 (HCL meta_optional 5th key)' 才闭环。漏检是结构性的: 专为此类漂移设的守卫 tests/test_t_hcl_meta_inventory.py 的 SPEC_X_LAYER1_WRITTEN_KEYS 未扩到 3 个新键 (该测试只断言 

### TASK-020 (TG-3) — 原判 `done` → **`partial`**

verification 第一条 "AC-8: every issue_id-keyed query tolerates new format" 未满足: 普查的模块枚举 (SURVEY FINDINGS #2 = db.py, #3 = comment_poll/feishu_webhook/failure_analysis/prompt_render/replay/forgejo_client/spec_drift/transitions/review_caller/reconciler/schema_migrate) 整个漏掉 extension.py —— issue_id 最大消费方。extension.py:1906 `candidate_issue_id = str(candidate.get("id",""))` 用内部 id (老格式), 与 seed 的 issue.get("number") composite 构造不一致, 然后喂给 :1921 `repo.count_active_for_issue(candidate_issue_id)` 这个 issue_id-keyed 查询, 并在 :2013 `return (S2_DECIDE, {"issue_id": candidate_issue_id})` 经 _advance_dispatch :1436-1441 原样透传进 transition_state(extra_fields=...) 覆写 DB 列。我用真 schema + 真 DispatchRepository + 真 _handle_s1_scan 实跑 (脚本 /tmp/claude-1000/-home-dev-Aria/74c30677-5f93-451b-b919-fe7912516a0c/scratchpad/probe_task020.py, issue id=705/number=147) 输出: count_active_for_issue(composite)=1, count_active_for_i

### TASK-023 (TG-5) — 原判 `done` → **`partial`**

AD-M6-10 六段结构 + 单节点作用域声明确已写入 architecture-decisions.md(分支版 :4041 起), 这部分推不翻; 但必需的 Alternatives 段里否 D 的载重论据是伪核实且与本仓实测证据相反: (1) AD :4074 写「诚实核实后拒绝: nomad/client-config/host-volume.hcl:26-29 确认 heavy 节点卷本地 ext4, 非 NFS」, 我把该文件整份取出(共 30 行), 26-29 行只有 host_volume "aria-runner-inputs" { path=/opt/aether-volumes/aria-runner/inputs; read_only=true }, 全文件零处出现 ext4/NFS(git grep -n ext4 -- nomad/ 无命中), 引用支撑不了该断言; (2) 方向相反: aria-orchestrator/docs/m0-report.md:80-81 (R8 Accepted) 与 openspec/archive/2026-04-17-aria-2.0-m0-prerequisite/artifacts/t2/decision-r8-virtiofs-vs-nfs.md 实测栈为 NAS NFS → PVE /mnt/pve/nfs-vms/aether-share → virtiofs → heavy guest /opt/aether-volumes/, 明写「三个 heavy guest…看到的 /opt/aether-volumes/ 都是同一份 NFS 数据」, 同目录 storage-validation-report.md 有 T2.3 跨节点 md5 交叉校验实证「三节点视图完全一致/产物跨节点可见」, 而 aria-runner-inputs 的 path 正在这棵树下(t2-1-volume-setup-evidence.md:34), 故 AD :4055/:4061「每-heavy-节点本地卷…

## 逐条明细

| TASK | 组 | 判定 | 证据 / 缺口 |
|---|---|---|---|
| TASK-001 | TG-1 | done | docker/aria-runner/modes/initial.sh:91-94 is_valid_issue_id regex `^[A-Z][A-Za-z0-9-]+$`；调用点 :365 (Step 1)。单测 docker/aria-runner/tests/initial-sh-unit |
| TASK-002 | TG-1 | partial | 缺一个 file-mode 失败路径测试: issue.yaml 缺失 / 空文件 / 非法 YAML 结构三选一, 断言 die() 触发 (exit!=0, stderr 含对应 FATAL 文案), 证明 initial.sh:460/461/490 的 die 分支真被走到而非只是代码存在 |
| TASK-003 ⟲ | TG-1 | partial | AC-3 的 body 半边零验证 + 证据含不存在的事实。反事实实证: 在副本 modes/initial.sh:567 把 `ARIA_ISSUE_DESCRIPTION=$(wrap_untrusted_content "$(sanitize_issue_text "$RAW_BODY")") |
| TASK-004 | TG-1 | done | classify_http_result (:160-186) 完整 2xx/JSON-schema 校验 + retriable(408/429/5xx/000)/non-retriable(404/401/403/其余) 分类; fetch_forgejo_issue (:199-238) 有界 |
| TASK-005 | TG-1 | partial | verification 第一项『YAML-safe escape』在代码里找不到对应实现: sanitize_issue_text 只做控制字符剥离，未对 YAML 特殊字符 (引号/冒号/`\|`/`-` 等) 做转义；而实际数据流 (ARIA_ISSUE_TITLE/DESCRIPTION)  |
| TASK-006 | TG-1 | done | resolve_base_branch (:256-278) META-first (:258-261) + Forgejo default_branch API fallback (:266-277)，无硬编码 master (全仓 grep 只在注释里出现 "master" 字样，代码路径无)。 |
| TASK-007 | TG-1 | partial | 需要在 initial-sh-integration/test.sh 补一个 scenario: file 模式下 issue.yaml 存在但 expected_changes.expected_file_touched/expected_diff_contains 均为空数组，走真实 initi |
| TASK-008 ⟲ | TG-1 | partial | verification 硬性要求 “RED test MUST exercise the REAL initial.sh call-chain”, 但该测试对本 fix 是重言式, 撤销 fix 也全绿。反事实实证: 在副本把 modes/initial.sh:880 的 `if [[ "$INP |
| TASK-009 | TG-1 | partial | 补一个 scenario: 设 ARIA_TEST_CLAUDE_NO_OP=1 (stub claude 不产生 commit) 走 fetch 模式真实调用链，断言 FINAL_OUTCOME=ASSERTION_MISMATCH 且 exit 1 (证明三条件里任一为假时不会被错判为 AUTO |
| TASK-010 | TG-1 | done | emit_outcome_marker (:305-308) 固定格式写 stderr (`>&2`)。success 侧: initial.sh:981-983 SUCCESS/AUTONOMOUS_COMPLETED 都调用它，scenario_fetch_happy_path 断言 marke |
| TASK-011 | TG-2 | done | 迁移文件 hermes-extensions/aria-layer1/aria_layer1/migrations/008_schema_v5.1_additive.sql 新增 5 列 (raw_issue_number/target_repo/base_branch/files_hint/out |
| TASK-012 | TG-2 | done | extension.py:1230-1234: target_repo=f"{org}/{repo}"; issue_id=f"ARIA-{repo}-{raw_issue_number}" 用 issue.get("number") 非内部 id, letter-prefixed。测试 test_ |
| TASK-013 ⟲ | TG-2 | partial | extension.py:2262/2265/2268 向 Nomad dispatch meta 新写 TARGET_REPO/BASE_BRANCH/FILES_HINT 三个键, 但生产 job HCL 从未声明它们: nomad/jobs/aria-layer2-runner.hcl:64- |
| TASK-014 | TG-2 | done | extension.py:2233-2237: ISSUE_URL=f"{forgejo_base}/{target_repo}/issues/{raw_issue_number}" 由持久化列构造, 不解析 composite issue_id、不用 hardcode env fallback ( |
| TASK-015 | TG-2 | done | extension.py:3190 head_branch=f"aria/{issue_id}", issue_id 取自 ctx.dispatch_row.get("issue_id") (extension.py 附近 _handle_s6_review 顶部)。TASK-012 使 issue |
| TASK-016 | TG-2 | done | interfaces.py:110 FailReason.INPUT_FETCH_FAILED="input_fetch_failed" 新增枚举成员, 与 CONTAINER_CRASH 区分。extension.py:2727-2745 (exit_code==0 分支): 读 marker → |
| TASK-017 | TG-2 | done | acceptance/check-m6-e2e-acceptance.py:117-119 _UNVERIFIED_OUTCOME_CLASSES=("AUTONOMOUS_COMPLETED","UNKNOWN") + _VERIFIED_S9_FILTER; :243-269 total_s9  |
| TASK-018 | TG-3 | done | 写入点: hermes-extensions/aria-layer1/aria_layer1/extension.py:1234 `issue_id = f"ARIA-{forgejo_repo_name}-{raw_issue_number}"` (seed 时构造, _phase1_scan_a |
| TASK-019 | TG-3 | done | 决策记录落在 migrations/008_schema_v5.1_additive.sql 的 `## TASK-019 决策` header 注释段 (相对 master diff 新增, 110 行), 明确写 DECISION: no historical migration / no ba |
| TASK-020 ⟲ | TG-3 | partial | verification 第一条 "AC-8: every issue_id-keyed query tolerates new format" 未满足: 普查的模块枚举 (SURVEY FINDINGS #2 = db.py, #3 = comment_poll/feishu_webhook/fa |
| TASK-021 | TG-4 | partial | 需要 owner 实际触发 /aether:aether-build-container (或手工 docker build) 对 post-merge master SHA 构建镜像并 push 到 forgejo.10cg.pub/10cg/aria-runner |
| TASK-022 | TG-4 | not_done | TASK-021 的真实构建必须先完成 (前置依赖) |
| TASK-023 ⟲ | TG-5 | partial | AD-M6-10 六段结构 + 单节点作用域声明确已写入 architecture-decisions.md(分支版 :4041 起), 这部分推不翻; 但必需的 Alternatives 段里否 D 的载重论据是伪核实且与本仓实测证据相反: (1) AD :4074 写「诚实核实后拒绝: noma |
| TASK-024 | TG-5 | done | architecture-decisions.md:384 风险表 cell 由 diff 确认已改写: 原文 'AD-M0-5 约定: prompt 写 bind mount 文件...' → 新文字显式标注'2026-07-04 M6 correction — 之前误标"AD-M0-5 约定"; |
| TASK-025 | TG-5 | done | architecture-decisions.md 新增 '#### AD-M1-4 amend (2026-07-04)' 小节(diff +18 行, 紧接原 AD-M1-4 决议之后)。逐条核对: (1) 生成代际澄清段先行区分 entrypoint-m1.sh(原 9-enum/6-AND, |
| TASK-026 | TG-5 | done | layer-boundary-contract.md diff(+46 行)新增 '## §5 Task Content Delivery Mechanism': 含 '### Channel selection' 双通道对比表(File mode vs Fetch mode, 列 Trigger/ |
| TASK-027 | TG-5 | done | 主仓 commit 55f7221 (2026-07-04, git merge-base --is-ancestor 55f7221 HEAD → YES, 已在当前 HEAD 历史中) 对 CLAUDE.md :529 一行做了改写, 新增: '遥测 Spec (AC-6 评分依赖, 独立, 待 |
| TASK-028 | TG-6 | not_done | 需要 owner/infra 在真实 Aether heavy-node 上实际执行 nomad/jobs/aria-smoke-forgejo-egress-probe.hcl (文档 §2.1 给出的现成 HCL), 并用 `nomad alloc logs <alloc-id>` 取回真实 P |
| TASK-029 | TG-6 | not_done | 依赖 TASK-028 (egress probe) 先产出真实 PASS 结果 —— 该依赖未满足 |
| TASK-030 | TG-6 | done | hermes-extensions/aria-layer1/tests/test_task030_fetch_failure_class_qa.py (161 行代码, commit a3a4e2d 首次落地, 未再变更) 直接调用生产路径 AriaLayer1Extension._handle_s |

> ⟲ = 被对抗轮推翻。完整证据 (含每条的 file:line 与反事实实验) 见工作流 transcript:
> `.claude/projects/*/subagents/workflows/wf_4ee913aa-65f/`