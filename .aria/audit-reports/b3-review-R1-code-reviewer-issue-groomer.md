---
checkpoint: b3-adversarial-review
mode: review (two-phase)
rounds: 1
verdict: PASS_WITH_FIXES
timestamp: 2026-10-19 (B.3)
agents: [code-reviewer]
---

# B.3 对抗审查 — code-reviewer 席 (两阶段)

审计对象: aria git diff master..feature/issue-groomer-p1-mvp (11 commits, 25 files, +11194)
套件实跑: 459 passed, 3 skipped, 47 subtests (pytest ~/.local)

## Phase 1 规范合规: **PASS**
抽核 5 关键任务 (001/002/005/017/007) 对照 detailed-tasks verification 逐条实证 (双端点契约+计数对账/裁定①覆盖非合并 fail-closed/裁定④结构性保证/CLI 五层编排+SC-5 差集/十一态+分量级+合成判别)。附带: SKILL.md 11 flag 零漂移; Amendment #1/#2/#4 全体现; stdlib-only 属实; 无超范围变更。

## Phase 2 代码质量
优点: fail-closed 分层真 closed; 结构性保证优先于纪律 (裁定④ API 无写面); 契约机读锚点化; 测试反事实纪律罕见地好; Rule #7 结构性满足; 原子写教科书级。

### Critical: 无
### Important
1. **生产 CLI 运行时依赖 tests/test_schema.py + 全局 pytest stub 注入** (groom.py:496-521): 依赖方向倒置 (生产正确性系于 tests 布局); stub 永久污染 sys.modules (进程内调用场景); except ImportError 不区分缺 pytest 与其他。修法: mini_validate 移 scripts/lib/schema_validate.py, tests 反向 import, stub 整段删。
### Minor
1. tier_a.classify(now=None) naive 本地时钟 (模块自声明 UTC 纪律违约; 生产路径恒注入 aware 不受影响) → datetime.now(timezone.utc).replace(tzinfo=None)
2. 非法 --repos spec 与 --now 不可解析落 exit 1 应为 2 (argparse 预校验 p.error)
3. scan_submodules 作用域可静默收窄仅主仓 (.gitmodules 损坏与合法无子模块塌缩同 [])
4. _extract_owner_repo 带端口 URL 推导失败 → 仓静默出列 (现网 remote 全 ssh 形态, 潜伏)
5. 'conflict' 分类值未入 schema/SKILL 文档面
6. 零评论 issue 仍发一次 comments GET (防御选择, docstring 记取舍)
7. (备案, 预先存在) tests/__init__.py + 顶层 lib 名多 skill 合跑撞名 — 全仓既有模式, 建议开全仓 issue

## verdict: PASS_WITH_FIXES (随 Important-1 一并修复)
