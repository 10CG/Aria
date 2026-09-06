收到。输入里的英文段和中文段是**同一条需求的翻译对**(不是两条需求), 所以只起草一份 Spec; 按你的指定, proposal 正文用英文, 目录 slug 用 ASCII (`dark-mode`), 我这边的说明仍用中文。

---

## 前置: A.1 认领 (REQUIRE claim, MUST)

本次是**直调** spec-drafter (没经 phase-a-planner), 所以认领块生效, 且直调路径没有 Level 判定 —— 无 Level 1 例外。实参我已解析好:

- `--raw-track-id` = `dark-mode-023236f2` (slug 逐字取 `openspec/changes/dark-mode/`; uuid 段取 `~/.aria/container-id` 的 **`uuid` 字段** `023236f2`, 不取 `label` —— 该机器 label 必须留空)
- `--linked-issue`: 两阶段取法。`linked_issue_field_probe.py` 存在 ⇒ 实参 = 它的 stdout。我对草稿实跑了一次:

```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg <proposal.md>
(空输出, exit 0)
```

  本 Spec 的 Linked Issue 值是哨兵 `none`, 探针据此输出为空 ⇒ **整个 `--linked-issue` 参数省略**(绝不能把 `none` 当值传: 任何非空串都 truthy, 两份毫无关系的 Spec 只要都写哨兵就会互相命中)。

于是认领命令是:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "dark-mode-023236f2" \
  --phase A.1 --mode advisory \
  --include-terminal \
  --repo-path "/home/dev/Aria"
```

省略 `--linked-issue` 的直接后果, 按四态表读: 输出里 `linked_issue_overlap` **键缺席** ⇒ 措辞是「**本轮未检测**」, 不是「无碰撞」。零证据不是正证据, 这两个不能混写。

⚠️ **本轮我没有执行这条命令**: 当前 AB 评测臂被显式禁止产生写入/推送副作用, 而 `phase1_gate` 会写 coordination ref 并推 origin。这是**执行条件不具备的上报, 不是规则豁免** —— 真实会话里这一步必须先跑通、拿到四态判读再起草; 我把实参解析到可直接粘贴执行的程度, 就是为了让这一步零成本补上。

---

## A.1.0 头脑风暴检查

扫过 `docs/decisions/` (共 20+ 条 DEC-*), **没有**与 dark mode / 主题切换相关的 technical decision-log。按集成流程给你三个选项:

1. 先跑 `brainstorm.technical` 讨论技术方案 (推荐: 主题存储位置、是否跟随系统、要不要留给消费方覆盖, 这三点值得先定)
2. 直接创建 OpenSpec (你已明确要 proposal, 我按这条走了)
3. 取消

预填充因此为空, proposal 里没有 `决策来源` / `关键决策` 段。

## A.1.2 Level 判断: **Level 2 (Minimal)**

| 因素 | 命中 | 说明 |
|------|------|------|
| 关键词 | `Add` / `feature` / `添加` / `功能` | Level 2 触发词 (功能开发词), 两种语言各命中一组, 一致 |
| 架构级词 | 无 | 无 refactor / breaking / migration / 架构 |
| 影响范围 | 单模块 | 见下面模块检测 |
| 变更类型 | 非 breaking | 默认外观不变, 纯增量 |

结论 Level 2, 只产 `proposal.md`, 不产 `tasks.md`。

**升级条件 (先说清)**: 若目标其实是多个前端/多个仓的 UI 一起改, 就命中「涉及 2 个及以上模块」⇒ 自动提升 Level 3, 需要补 `tasks.md`。

## A.1.3 模块检测 (这里有个需要你拍板的点)

本仓唯一的 UI 面是 `aria-dashboard` 生成的单文件 HTML。我去读了模板, 发现一个与字面需求相反的事实:

```
aria/skills/aria-dashboard/templates/dashboard.html:12  --bg-primary: #0f1117;
                                                    :13  --bg-secondary: #1a1d27;
                                                    :14  --bg-card: #21242f;
```

**它现在就是深色的** —— 而且是唯一一套硬编码调色板, 没有任何 `prefers-color-scheme` 或主题选择器。所以「添加深色模式」落到本仓, 真正的缺口不是「把界面做暗」, 而是**把已经暗着的那套从隐式常量变成显式可切换的 mode**(dark 保持默认 + 补 light + 跟随系统)。我按这个读法起草了下面这版。

如果你指的是**别的项目/别的 UI**, 告诉我模块名, 我重新 scope (多个 UI 面的话按上面的规则升 Level 3)。这条我也写进了 proposal 的 Open Questions, 没有藏在对话里。

---

## A.1.4 生成预览

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: dark-mode
Module: standards (aria-plugin / aria-dashboard)
Location: openspec/changes/dark-mode/proposal.md
```

> 路径落点是**本项目仓内**的 `openspec/changes/`, 不是 `standards/openspec/changes/` (不可协商规则 #5: standards 是共享子模块, 项目变更写进去会对所有采用方可见且无人拥有)。

──────────────────────────────────────────────────────────

```markdown
# Dark Mode Support

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-05
> **Linked Issue**: `none`

## Why

The dashboard UI ships one hard-coded palette. Today that palette happens to be dark
(`aria/skills/aria-dashboard/templates/dashboard.html:12-16` defines `--bg-primary: #0f1117`
and friends), which means "dark" is an implicit constant rather than a mode: users cannot
follow their OS appearance, cannot switch to a light palette for daylight/projector use, and
the theme cannot be tested or regressed because nothing selects it. Making dark an explicit,
switchable mode is cheap because the stylesheet is already fully tokenized with CSS custom
properties.

## What

Introduce an explicit theme layer with three states — `dark` (current look, stays the default),
`light`, and `system` (follow `prefers-color-scheme`) — plus a visible toggle in the dashboard
header and per-viewer persistence. No visual change to the default rendering.

### Key Deliverables

- `aria/skills/aria-dashboard/templates/dashboard.html` — split the existing `:root` token block
  into a light palette and a dark palette, selected by `[data-theme]` and by
  `@media (prefers-color-scheme: dark)`; today's values become the dark palette verbatim
- `aria/skills/aria-dashboard/templates/dashboard.html` — header theme toggle (dark / light /
  system) with an accessible label and keyboard operation
- `aria/skills/aria-dashboard/templates/dashboard.html` — inline pre-paint script that resolves
  the stored preference from `localStorage` before first paint (no flash of wrong theme), wrapped
  in try/catch so a browser that blocks site data still renders correctly
- `aria/skills/aria-dashboard/SKILL.md` — document the theme states and the persistence key

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Dashboard becomes usable in daylight and matches OS appearance; the palette becomes a named, testable contract instead of an unlabeled constant |
| **Risk** | Token split can silently change the current dark rendering — mitigate by diffing the resolved dark values against today's `:root` block and requiring byte-identical color values for the dark state |
| **Risk** | Light palette can fail contrast requirements — mitigate by checking every text/background pair against WCAG AA (4.5:1) before merge |

## Tasks

- [ ] Extract the current `:root` token block into an explicit dark palette (values unchanged)
- [ ] Author the light palette and verify contrast on every text/background pair
- [ ] Add `[data-theme]` + `prefers-color-scheme` selection and the pre-paint resolver
- [ ] Add the header toggle (dark / light / system) with `localStorage` persistence
- [ ] Update `aria-dashboard` SKILL.md with the theme contract

## Success Criteria

- [ ] Default rendering (no stored preference, no OS preference) is byte-identical in color values
      to the pre-change dashboard — verified by diffing the resolved custom properties
- [ ] Toggling to light and back to dark restores the dark palette with no page reload
- [ ] Preference survives a reload and a dashboard regeneration; a browser with site data blocked
      still renders the default theme without a console error
- [ ] Every text/background pair in the light palette meets WCAG AA (>= 4.5:1)
- [ ] No flash of the wrong theme on first paint in either stored state

## Open Questions

- [ ] Target surface: this draft assumes the `aria-dashboard` generated HTML, the only UI surface
      in this repository. If the intended target is a different application, the module must be
      specified and the deliverables re-scoped (a multi-surface target would also raise this to
      Level 3 per the cross-module rule).
```

──────────────────────────────────────────────────────────

### 头部字段说明

- 字段顺序 `Level` → `Status` → `Created` → `Linked Issue`, 与 SOT 模板 `standards/openspec/templates/proposal-minimal.md` 一致 (从模板起草自然满足)。
- `Linked Issue` 值逐字写 `` `none` `` —— 已核实本需求当前没有关联 issue。**不留空、不删行**; `N/A` / `TBD` / `-` 不是哨兵, 会被机械 check 判不合规。如果你手上有对应 issue, 给我 `<org>/<repo>#<n>`, 我改成 inline code span 形 (多个用 `, ` 写在同一个 code span 内)。
- 验收项我尽量钉成可证伪的量 (byte-identical 色值 diff / >= 4.5:1 对比度 / 无 FOUC), 而不是「主题工作正常」这种代填即真的布尔。

---

🤔 Create this file at `openspec/changes/dark-mode/proposal.md`? [Yes / No / Edit]

确认后我会提示你跑:

```bash
openspec validate dark-mode --strict
```

然后进入 A.2 任务规划 (`task-planner`)。

**需要你先答的一个问题**: 目标 UI 面就是 `aria-dashboard` 吗? 是 ⇒ 上面这版直接落盘; 不是 ⇒ 给我模块名, 我重 scope 并重判 Level。
