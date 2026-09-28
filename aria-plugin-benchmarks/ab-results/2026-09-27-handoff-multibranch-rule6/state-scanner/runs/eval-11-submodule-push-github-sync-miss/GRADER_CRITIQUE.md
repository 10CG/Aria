# eval-11 评分员意见 (submodule-push-github-sync-miss)

## 结果

| 臂 | 通过 / 总数 |
|----|-------------|
| X | 4 / 9 |
| Y | 4 / 9 |

两臂逐条判定完全相同 (通过的是断言 1、6、8、9；失败的是 2、3、4、5、7)。

## 根本问题：环境里没有事故状态

prompt 要求「复现」2026-04-12 事故，但 eval 没有搭建事故状态，臂是对真实仓库跑 scan.py。两臂的 snapshot 都显示：`overall_parity=true`，8 条 leg 全部 `fetch_ok=true` 且 `parity=equal`，`gitlink_integrity` 6 对全部 `ok`。两臂补查的 master 三方 SHA 也一致。所以「github 落后」这个前提在本环境里不成立。两臂如实回答「没有需要补推的 remote」，这个回答是正确的。

结论：以「github 落后」为前提的断言在本环境下要么恒假，要么只能空真通过，完全区分不了两个版本。

## 逐条分类

1. **「只推了 origin 时不得报告全部同步」**：在本环境**空真**。前提不成立，报全部同步反而是对的。两臂都说明了结论来自扫描现场 fetch (fresh)，不是 push 回执，因此判通过。这条断言测不出「静默通过」的缺陷。
2. **「github parity = behind」**：**恒假**，原因有两个。(1) 环境里没有分歧；(2) 断言本身和断言 4 矛盾：断言 4 写明这种形态下 behind_count=0、ahead_count 非零，也就是从本地视角看 parity 应为 `ahead`，两臂的假设推演也都写的是 `ahead`。就算搭出了事故状态，这条断言也会惩罚正确答案。建议改成 `ahead`。
3. **「hint_type: 'push'」**：本环境**恒假**，snapshot 中 `hint_type` 全为 null。另外，这个字段属于 `sync_status.submodules[]`，是否会对 multi_remote 的 github leg 输出，要到事故态才能核验。
4. **「报告缺失 remote 名 + ahead_count 非零」**：本环境**恒假**，没有缺失的 remote，ahead_count 全为 0。
5. **「保留 submodules[].remote_commit 指向 origin remote_head」**：**无法从 answer 核验**。snapshot 里有这个字段 (aria=1cb3872)，但它是 schema 兼容性断言，测的是 scan.py 的代码，不是 skill 的回答。两臂同一套 scan 输出结构相同，这条区分不了两臂。更适合改成 scan.py 的结构化测试。两臂回答都没提这个字段，所以判失败。
6. **「两 remote 可达时 has_unreachable_remote: false」**：两臂都照抄了 false 并判通过。但「github behind」前提不成立，它几乎是 snapshot 的直接转述，属于**近乎恒真**。
7. **「helper 可用时输出引用 git-remote-helper」**：**无法核验**。两臂的 snapshot 和回答里都没有任何 helper 字样，也无从判断 helper 是否可用。条件句前提不明，按「举证责任在断言」判失败。
8. **「指出 gitlink 风险 (clone --recursive 断裂)」**：两臂都讲到了，判通过。有一定内容要求，但在干净状态下只能以「假设推演」的方式满足。
9. **DISCRIMINATOR「gitlink 修复作为推荐规则产出而非已知缺口」**：两臂都把 orphaned 的修复写成规则产出 (`git -C aria push github ...`)，判通过。但本环境里规则**没有真实触发**，两臂都只是复述文档行为。本来想用这条做区分器，结果在干净状态下失效了。X 点名了规则路径 (multi_remote_drift 第七路)，Y 只写了规则链的因果；这点差别不影响判定。

## 两臂差异是否来自断言能测到的东西

**否。** 两臂 snapshot 的结构和数值一致，9 条判定完全相同。可以看到的差异都在断言覆盖范围之外：

- Y 输出了完整的 9 区块状态 (需求 / OpenSpec / 审计 / issue 等)；X 只写同步部分，其余简要带过。
- Y 明确指出「单纯 ahead 不触发 multi_remote_drift，只在同步区露出」，并建议把「只比对当前分支」的覆盖缺口开 issue。X 把同一个限制写成「已知限制 §10.7」。两臂都发现了「multi_remote 只比对当前检出分支，看不到 aria master」这个缺口，也都补查了 master。

这些都不是断言测得到的维度。

## 建议

- 在隔离沙箱里构造事故状态：用 file:// clone，配两个 bare remote，只往 origin 推合并提交，必要时再让主仓 bump gitlink 并推到 github，然后再跑两臂。否则本 eval 的 9 条断言里至少 5 条没有区分力。
- 断言 2 的 `behind` 改为 `ahead`，和断言 4 保持一致。
- 断言 5、7 属于 scan.py 的 schema 或环境层面，建议移到结构化测试，或者写清楚如何核验。
- 可以补一条断言：「子模块不在 master 时，是否指出 multi_remote 只比对当前分支的覆盖缺口」。两臂都做到了，但目前没有任何断言检查这一点。
