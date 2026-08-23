依据 state-scanner SKILL.md (及 references/ 与 docs/) 的文字回答, 不跑命令:

**(1) 传 `--linked-issue 'aria-plugin #152'` 会不会报出那条 claim? 比较规则是什么?**

SKILL.md 对 `--linked-issue` 只有一句说明 (claim 生命周期闭环段, Part B1): phase1_gate 支持可选 `--linked-issue`, 把它写入 claim, 并在输出 JSON 追加 additive 键 `linked_issue_overlap[]` —— 针对「同 issue 不同 track-id」的「同一件事两个名字」advisory 告警。

也就是说, 告警的触发条件是: 另一条 claim 的 `linked_issue` 指向同一个 issue, 且 track_id 不同。你的情况 track_id 不同 (`ci-gate-first-push-fix` vs `pre-merge-gate-no-run-for-branch`), 所以关键就在 "同一个 issue" 怎么判。

**skill 文档没有写比较规则**。SKILL.md、references/layer-l-integration.md、docs/coordination-ref-schema.md 里都找不到 `linked_issue` 的格式要求或归一化说明 (文档里唯一的归一化描述是 track_id 的 `derive_track_id` 和 Status 的 `_normalize_status`, 与 linked_issue 无关)。既然文档没有承诺会把 `aria-plugin #152` 归一成 `10CG/aria-plugin#152`, 就只能按最保守的假设理解: **很可能是字面比较**。那条 claim 存的是 `10CG/aria-plugin#152`, 你传的是裸仓名 + `#` 前带空格的 `aria-plugin #152`, 两个字符串不相等 —— 按文档能支撑的结论, **不能指望它把那条 claim 报出来**。

所以我的建议: 不要赌归一化, 直接传和那条 claim 一模一样的写法 `10CG/aria-plugin#152` (org 前缀 + 无空格), 这样无论比较规则是字面还是归一, 都能命中。

**(2) 如果传 `10CG/Aria#152` 呢?**

不会报。`10CG/Aria#152` 和 `10CG/aria-plugin#152` 是两个不同仓库的 issue (主仓 Aria 的 #152 vs 插件仓 aria-plugin 的 #152), 编号相同只是巧合。任何合理的比较规则 (字面或归一) 都不应把它们判为同一个 issue; 要是真报出来了, 那反而是误报。注意你的真实目标 issue 是 aria-plugin#152, 传成 Aria#152 本身就写错了仓库。

**(3) 这个告警会阻断进 Phase B 吗?**

不会。SKILL.md 明确写的是: `linked_issue_overlap[]` 是 advisory 告警, "渲染为 🔴 提示但不阻断"。放行与否由 `proceed` 字段决定 (outcome 为 passed / advisory_proceed / user_takeover / user_override_proceed 即放行), 而且 coordination mode 默认是 advisory (放行 + 写推自己的 claim + 返回 surface 告警), 最终仲裁交给 reconcile (claimed_at 最早者胜)。linked_issue 重叠只是提示你 "可能和别人在干同一件事", 要不要合并轨道是你自己判断 —— 按 CLAUDE.md 的并发轨规矩, 这种情况应该先读对方轨 (pre-merge-gate-no-run-for-branch, 已在 #152 A.2/A.3 阶段) 的 handoff / spec, 确认你的 `ci-gate-first-push-fix` 不是在重做同一件事。
