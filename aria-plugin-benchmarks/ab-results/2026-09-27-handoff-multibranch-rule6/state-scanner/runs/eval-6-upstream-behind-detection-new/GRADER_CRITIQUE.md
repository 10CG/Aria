# eval-6 upstream-behind-detection-new 评分批评 (grader)

两臂匿名为 X / Y。结果: X 1/6, Y 2/6。

## 环境事实 (两臂相同)

- 当前分支 `feature/handoff-multibranch-subdir-path-fidelity` 没有配置 upstream: `sync_status.current_branch.reason=no_upstream`, ahead/behind 为 null
- 不是 detached HEAD, 也不是浅克隆
- 用户真正关心的差距是: master 比 feature 多 12 个提交 (grader 用 `git rev-list --left-right --count HEAD...origin/master` 只读复核, 结果是 `13 12`)
- 两臂的 `collectors/sync.py` 和 `collectors/git.py` 完全相同 (old-arm-1cb3872 与现行版 diff 只差在 `handoff_multibranch.py` / `scan.py` / `latest_md_writer.py`)。所以跟 upstream 检测有关的采集行为, 两臂在代码层面没有差别。

## 逐条判定

1. **`git rev-parse @{u}` 先于 `rev-list --count`**: 在回答层面恒假。这是 `sync.py:200` 的实现细节, 回答通常不会写出来, 两臂都没提。从产出没法核验 skill 是否真这么做 (只能去读代码, 而代码两臂一样)。建议改成对快照字段 (`upstream_configured` / `reason`) 断言, 或者直接删掉。
2. **upstream 存在时报告 `current_branch.ahead/behind`**: 本环境没有 upstream, 条件结构上触发不了, 两臂都判 FAIL, 属于无法核验。要让这条有意义, 得造一个有 upstream 的 fixture 仓。
3. **缺 upstream 时报 `no_upstream`, 且不以错误退出**: 唯一一条真正被测到的断言, 两臂都 PASS。它本身没有区分度, 因为两臂的 `sync.py` 相同, 实际上恒真。
4. **detached HEAD 报 `reason: detached_head`**: 本环境不是 detached, 所以测不到 skill 的实际行为, 只能测回答有没有向用户说明这个场景怎么处理。Y 给了场景表 (`name=null`, `reason="detached_head"`, 已对照 `sync.py:170/191` 核实属实), 判 PASS; X 只确认了「不是 detached」, 判 FAIL。**两臂在这条上的差异来自回答写得详还是略, 不来自 skill 行为**: 采集代码一样, 不能当作新旧版本的质量信号。
5. **浅克隆: `--is-shallow-repository` 加 `.git/shallow` 回退**: 在回答层面恒假, 两臂都没提检测手段。另外 grader 在现行 collectors 里只找到 `git.py:_is_shallow` 用 `--is-shallow-repository`, **没找到 `.git/shallow` 文件回退**。这条断言的后半截可能跟实现本身就对不上: 即便放到浅克隆环境里去测, 也可能恒假。建议对照代码勘正断言, 或者开 issue 补回退逻辑。
6. **behind >= 5 时推荐 `git pull`**: behind 为 null, 条件触发不了, 两臂都判 FAIL, 属于无法核验。两臂都正确地**没有**推荐 pull: 没有 upstream 时 pull 会报错, 而且就算能 pull 也拉不到 master。两臂都推荐 `git merge origin/master`, 这是对的。

## 没有断言覆盖到的关键结果

- 用户问的其实是「主分支有没有新改动」。Y 在扫描之后自己补做了只读核对, 给出「落后 master 12 个提交, 两边没有重叠文件」, 已核实属实。它还指出本分支读到的 handoff 与 `state-checks.yaml` 已经过期。X 只给了一条让用户自己跑的命令, 理由是「skill 禁止手工采集字段」, 没有给出数字。这是两臂在实际用处上最大的差别, 但 6 条断言都测不到。
- 这个差别也不来自 scan.py (快照里没有 feature 与 master 的对比字段), 而来自臂在 SKILL.md 约束下怎么决定补不补做核对。以后如果想测它, 应该加一条断言, 比如「无 upstream 时, 是否给出 feature 相对默认分支的落后数」。

## 结论

6 条断言里有 4 条在本环境中要么恒假、要么无法核验 (第 1、2、5、6 条), 第 3 条两臂恒真。只有第 4 条两臂结果不同, 而这个差别反映的是回答写得详还是略, 不是 upstream 检测能力。本 eval 在这个环境里基本测不出新旧版本 state-scanner 的差别; 1/6 对 2/6 的分差不应该算作版本回归或改进的证据。
