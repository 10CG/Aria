# Tasks — shell-jq-crlf-hardening

> 粗粒度功能任务 (Phase.Task)。Agent 分配 (A.3) / 时间估算 / 文件路径细节 (A.2) 不在此。
> 编号一旦创建不可变。Rev1 (post_spec R1 challenge audit 闭合) 调整见各 Phase。

## 1. 测试框架先行 (基础设施)

- [ ] 1.1 泛化 #132 的 jq-shim 为可复用 CRLF 测试框架 (awk 每行补 `\r\n` 模拟 Windows native jq + PATH prepend helper)
- [ ] 1.2 框架须覆盖 **两种消费形态** (R1 M1): `readarray -t < <(jq)` 管道 + `VAR=$(…\|jq)` 命令替换;各形态「非空洞自检」原语须 **双向** (R2 m1): 不激活 shim 断言 CR 不存在 + 激活后断言存在 (防 shim bug 致 trivial-pass)
- [ ] 1.3 框架提供 **双向断言原语** (R1 C1): 支持 silent-bypass 站点的 nofix(期望"无效果")→ fix(期望"有效果") 两态翻转断言;被 hook 测试与 skill 脚本测试共同复用 (单一 SoT)

## 2. Tier 1 — secret-scan.sh (security, 按决策表)

- [ ] 2.1 按决策表修复 `secret-scan.sh`: type-check 门控 (行 116) + tool (行 118, 喂 `case`) 剥尾 CR;**content (行 123) 不剥** (R1 C2 — 数据正文,剥除会篡改写回 LLM 的用户内容)
- [ ] 2.2 **双向非空洞回归** (R1 C1 + R2 m2 执行机制): CRLF shim 下,对 fixed hook 与 pristine-copy (sed 去 fix 的副本,复用 #132 验证手法) 各跑一次 —— nofix 副本期望含 secret 输出**不被** REDACT (bug 复现) / fixed 期望**被** REDACT;断言两态结论相反 (仅 fixed 通过 = 空洞失败)
- [ ] 2.3 **content 保真负向用例** (R1 M1 + R2 NEW-M 测试接入点): **接入点 = 截获 hook stdout 重注入的 envelope** (`secret-scan.sh:368 jq --arg c` 回写),`jq -r '.tool_response.output'` 取回写 content → 与输入逐字节比对。被扫描 content 含合法 `\r` → fix 后 secret 仍 redact 且非 secret 正文 `\r` 不被删。**禁止 mock hook 内部路径**
- [ ] 2.4 验证修复不削弱 / 不误伤 Linux LF 既有行为 (全量 secret-scan 测试 PASS)

## 3. Tier 2 — relay (correctness, 按决策表)

- [ ] 3.1 修复 `setup_relay.sh:44` `__aria_cwd` 捕获剥尾 CR (R1 m2 — 修门控即透传保护下游 :48 写文件,:48 不需独立改)
- [ ] 3.2 修复 `setup_relay.sh:60,71` 安装检测 marker (`cmd`) 剥尾 CR
- [ ] 3.3 修复 `setup_relay.sh:133,134` **注入的 runtime statusLine 片段** (`used`/`model`) 自身 CR-safe (用户 Windows 机每次渲染)
- [ ] 3.4 保证幂等检测兼容旧 (无防护) 片段 — 不导致 Windows 用户反复注入;机验: 连续两次运行注入条目数不变
- [ ] 3.5 修复 `check_context_relay.sh:53` relay-install 检测 (`cmd`) 剥尾 CR
- [ ] 3.6 上述各站点 CRLF 回归 case (复用框架)

## 4. Tier 3 — hygiene (验证后决定改动 vs 文档说明)

- [ ] 4.1 (R1 M2 已实证) `check_parity.sh:383/386/389` 布尔捕获: 确认唯一下游是 `--argjson` 且 jq 容忍 `true\r` → **降 T3,convention 文档说明,不强制代码改动**
- [ ] 4.2 (R1 REFUTE 已实证) JSON 累加器 (`check_parity`/`push_all_remotes` `jq '. + [$entry]'`): jq 转义串内 CR + argjson re-parse 不累积 → **不改动,convention 说明**
- [ ] 4.3 `check_secret_guard_install.sh:74-76` 显示串 (state/sub/adv) 剥尾 CR (按需,低优)

## 5. 回归防线 (防止未来重蹈)

- [ ] 5.1 grep-based 回归 guard: 扫描新增未防护 jq **读取**消费点 (`< <(jq` / `VAR=$(…jq -r '.field')`);**配 allowlist/豁免机制** (R1 m1 — `jq -n` 构造器 15 处 + T3 已知安全站点,类比 `# secret-leak-ok-explicit` 注释豁免)
- [ ] 5.2 guard 自测非空洞: 故意引入一处未防护 `jq -r '.field'` 捕获 → guard 失败;且对 `jq -n` 构造器 + T3 站点不误报
- [ ] 5.3 决定 guard 落点 (倾向 test 阶段 而非 pre-commit,降低误报阻断面 — R1 m1) 并集成

## 6. Convention + 文档同步 (Rule #3)

- [ ] 6.1 新建 `standards/conventions/shell-jq-crlf-hygiene.md`: **CR 处理决策表** (门控/比较值 vs 数据正文 vs 构造器) + 正向 pattern + exception 模板
- [ ] 6.2 exception 收录: 「数据正文不剥 CR」(R1 C2) + 「`tr -d '\r'` 误删合法 CR 局限」(R1 m4) + #61/#131/#132 同源「Windows CRLF/编码边界」家族清单
- [ ] 6.3 CLAUDE.md 信息地图 + 目录导航索引新 convention

## 7. 收尾

- [ ] 7.1 全量 hook + skill shell 测试 PASS (Rule #6 deterministic structural substitute: 双形态 shim + 双向非空洞 + content 保真)
- [ ] 7.2 版本 bump (ship 前 `cat aria/VERSION + plugin.json` 复核当前版本) + 5 SOT + CLAUDE.md doc 同步;**SOT/CLAUDE.md 高竞争区按 `feedback_concurrent_sot_conflict_mechanical_resolve` (version mine-wins + CHANGELOG keep-both) 处理** (R1 m3)
- [ ] 7.3 push 前 `git fetch` + 多远程推送 + post-push SHA 验证 + 关闭关联 issue (如开)
