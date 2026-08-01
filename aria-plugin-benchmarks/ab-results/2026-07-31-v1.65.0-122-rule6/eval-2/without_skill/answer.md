# Phase C C.2 合并冲突处理推演: feature/oauth2-social-login → main

> 形态: descriptive 推演。按场景前提 (merge 进行中, `backend/config/settings.py` 冲突) 描述处理路径, 不实跑命令。

## 总原则

冲突处理的目标不是"让 merge 命令跑完", 而是**产出一个语义正确、可验证、双方意图都保留的合并结果**。任何一步拿不准, 宁可 abort 回到干净状态, 也不提交一个猜出来的 settings.py — 配置文件冲突解错的代价 (跑起来才炸、甚至静默用错配置) 远高于重新合一次的代价。

## 第 1 步: 先冻结现场, 确认冲突全貌

在动手改任何文件之前, 先收集信息:

1. `git status` — 确认当前处于 merge in-progress 状态, 列出全部 `both modified` 文件。场景说冲突在 `backend/config/settings.py`, 但必须核实**是否只有这一个**冲突文件; 若还有其他文件冲突, 要一并纳入方案, 不能解一个漏一个。
2. `git diff` (merge 冲突态下会显示 combined diff) + 直接读 `backend/config/settings.py`, 找到 `<<<<<<< HEAD` / `=======` / `>>>>>>> feature/oauth2-social-login` 标记块, 逐块登记。
3. `git log --oneline main..feature/oauth2-social-login -- backend/config/settings.py` 和 `git log --oneline feature/oauth2-social-login..main -- backend/config/settings.py` — 看两边各自对这个文件做了什么提交。理解**双方修改意图**比盯着冲突标记猜更可靠: OAuth2 分支大概率是新增了 provider 配置 (client id/secret 的 env 读取、回调 URL、`INSTALLED_APPS`/中间件注册之类); main 侧则是分支开出后别人合入的其他 settings 改动。

## 第 2 步: 判定冲突性质, 决定"就地解决"还是"退回重来"

按冲突块的语义分三类处置:

- **纯叠加型** (最常见): 双方在同一区域各自新增了互不相关的配置项 (比如两边都往同一个 dict / 列表尾部追加)。处置: 保留双方全部内容, 按文件原有排序惯例排好。这是可以就地解决的。
- **交叠修改型**: 双方改了**同一个**配置键的值, 或一方重构了结构 (如把散落常量收进 dataclass / 按环境拆文件) 而另一方在旧结构上加东西。处置: 先在 main 的新结构上重放 feature 的语义 (而不是机械保留文本), 必要时把 feature 的新增项迁移到新结构对应位置。若重构幅度大、就地手改容易漏, 更稳妥的路径是 `git merge --abort`, 回 feature 分支先 `git rebase main` (或 merge main 进 feature), 在分支上从容解冲突并跑全量测试, 再回来重新走 C.2 — merge 冲突态下现场手术的可核验性远不如分支上解完再合。
- **语义冲突型 (无文本冲突也可能存在)**: 例如 main 侧改了 `AUTHENTICATION_BACKENDS` 的顺序或替换了 auth 相关中间件, 与 OAuth2 social login 的假设相抵触。这类 git 根本标不出来, 所以解完文本冲突后**必须**做第 4 步的行为验证, 不能以"没有冲突标记了"为完成判据。

**升级判据**: 若冲突涉及双方对同一配置的**意图性分歧** (比如两边给同一个安全相关开关设了相反的值), 这不是集成工程师能单方面裁决的 — 停下, 不猜。把两侧提交、作者、各自理由整理成一段说明, 升级给 owner / 双方作者裁定, 期间保持 merge abort 后的干净状态。

## 第 3 步: 解决冲突本体

以叠加型为主线描述:

1. 逐块编辑 `settings.py`, 删除三种冲突标记, 合成双方内容。特别注意配置文件的高危细节:
   - 尾随逗号 / 括号闭合 (冲突块常把一个 dict/list 切成两半);
   - 重复键 (Python dict 字面量重复键**不报错、后者静默覆盖前者** — 合并后必须专门扫一遍新旧内容有无同名键);
   - import 区的冲突 (两边都加了 import, 合并后去重);
   - env 变量读取的默认值 — 不把 feature 分支里开发期的临时默认值 (尤其任何形似 secret 的字面量) 带进 main。若发现冲突块里有硬编码 secret, 按 Rule #7 处理: 改为 env 读取, 且泄露过的值要提示轮换。
2. 全文件通读一遍合并结果 (不只看冲突块) — 确认逻辑连贯、没有半截结构。
3. `grep -c '<<<<<<<\|=======\|>>>>>>>' backend/config/settings.py` 机械核验冲突标记归零 (`=======` 要小心误伤合法字符串, 以 `<<<<<<<`/`>>>>>>>` 为准)。

## 第 4 步: 提交前验证 (完成判据在这里, 不在"标记消失")

merge 冲突解得对不对, 必须用行为证据说话:

1. **语法/加载关**: `python -c "import backend.config.settings"` 或项目等价的 config 加载入口 (Django 则 `manage.py check`), 确认文件能被解析且配置图谱完整。
2. **测试关**: 跑受影响面的测试 — 至少覆盖 auth/OAuth2 相关套件 + 任何直接消费 settings 的模块; 时间允许跑全量。理由: 冲突文件是全局配置, 影响面天然是全仓的, "只跑 OAuth 测试" 会漏掉 main 侧改动被我合并时破坏的场景。
3. **双向意图核对**: 对照第 1 步登记的两侧提交, 逐条确认每一侧的每个改动点在合并结果里都还在 (或有意识地被裁决掉并记录理由)。这一步防的是"解冲突时手滑丢了 main 侧某行"这类静默回退。

任何一关失败 → 回第 2/3 步修, 不带病提交。

## 第 5 步: 提交与合并收尾

1. `git add backend/config/settings.py` (及其他解决过的文件), `git commit` 完成 merge commit。commit message 遵循 Conventional Commits, 并在 body 里写清: 冲突文件、冲突性质、裁决方式 (如"保留双方新增配置, main 侧结构为基底重放 feature 的 OAuth2 provider 配置") — 给后人留下可审计的裁决记录。
2. **Rule #8 pre-merge gate**: 合并进 main 前确认 (a) 本分支 CI passing (解完冲突后要以**解冲突后的结果**重新过 CI, 旧的绿不作数); (b) main 无 in-flight CI run。无可用 CI backend 时显式降级并记录, 不静默跳过。
3. 推送后核验: 按多远程约束, 本地双推后对每个 remote `git ls-remote <remote> <branch>` 取 SHA 与本地比对, 全部一致才算推成功, 不信 push 回执。
4. 若走 PR 流程, 在 PR 里补一条冲突处理说明, 让 reviewer 能针对性复核 settings.py 的合并裁决。

## 失败/异常路径汇总

| 情形 | 处置 |
|------|------|
| 冲突块看不懂双方意图 | `git merge --abort`, 读提交史/问作者, 不猜 |
| 冲突是意图性分歧 (同一配置两个相反值) | abort + 升级 owner/双方作者裁定 |
| main 侧大重构, 现场手改风险高 | abort → feature 分支 rebase/merge main 解完并测过 → 重走 C.2 |
| 解完测试红 | 先 `git log -- <测试文件>` 判断是否本次合并触碰所致, 是则回改, 不是也要查清再放行, 不强推 |
| 发现硬编码 secret | 改 env 读取 + 提示轮换, 不让 secret 值进 chat/日志 |
| 解到一半发现还有其他冲突文件被漏 | 回第 1 步重新盘点, 全部文件统一按本流程走 |

## 一句话收束

优雅处理 = 冻结现场看全貌 → 按冲突性质选"就地解 / 退回分支解 / 升级裁决" → 解完以 import + 测试 + 双向意图核对为完成判据 → merge commit 留裁决记录 → 过 pre-merge gate 再进 main; 全程任何拿不准的点都以 abort 保底, 绝不提交猜出来的配置。
