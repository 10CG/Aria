# 分支状态检查

好的，我来帮你检查当前分支和 upstream 的状态。

```bash
$ git branch --show-current
feature/state-scanner-v2.9

$ git log --oneline -5
1445da5 chore(spec): archive scan-complexity-security-fix OpenSpec (D.2)
c686916 release: v1.4.2 — scan.sh 安全加固 + complexity_tier rename
ee8ffb5 merge: fix/scan-complexity-security — scan.sh 安全 gap + complexity_tier rename
eb46433 chore: update aria-orchestrator — scan security fix + tier rename
29293c3 feat(spec): scan-complexity-security-fix OpenSpec (Level 2)
```

现在检查 upstream 和 ahead/behind:

```bash
$ git rev-list --count origin/master..HEAD
fatal: ambiguous argument 'origin/master..HEAD': unknown revision or path not in the working tree
```

看起来 origin/master 引用不存在。我试试 fetch 一下:

```bash
$ git fetch origin master
# (假设成功)

$ git status
On branch feature/state-scanner-v2.9
nothing to commit, working tree clean
```

你可以用这个命令查看你的分支是否落后:

```bash
git fetch origin
git log HEAD..origin/master --oneline  # 查看 master 上你没有的 commits
```

如果你想 pull 最新的 master 变更到你的 feature 分支，可以 rebase:

```bash
git fetch origin
git rebase origin/master
```

至于 detached HEAD 和 shallow clone 场景，你可以用:

```bash
# detached HEAD 检测
git symbolic-ref -q HEAD || echo "detached"

# shallow clone 检测
[ -f .git/shallow ] && echo "shallow"
```

总结: 需要先 `git fetch` 才能知道是否落后。
