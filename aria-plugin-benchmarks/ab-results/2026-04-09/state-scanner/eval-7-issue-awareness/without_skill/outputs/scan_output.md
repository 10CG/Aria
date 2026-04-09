# Open Issues 查看

好的，你用的是 Forgejo 平台。我试试看能不能查到 open issues。

```bash
# 先看看 remote URL 确认仓库地址
$ git remote -v
github	git@github.com:10CG/Aria.git (fetch)
github	git@github.com:10CG/Aria.git (push)
origin	ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git (fetch)
origin	ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git (push)
```

看起来你的仓库在 `forgejo.10cg.pub/10CG/Aria`。

Forgejo 的 API 兼容 Gitea，可以用 curl 调用。我试一下:

```bash
$ curl -s "https://forgejo.10cg.pub/api/v1/repos/10CG/Aria/issues?state=open"
# 可能需要 token 或走 Cloudflare Access
```

这个 endpoint 如果是受 Cloudflare Access 保护的话，直接 curl 会失败。你可能需要:

1. 在 Forgejo web UI 直接查看: https://forgejo.10cg.pub/10CG/Aria/issues
2. 配置 `GITEA_TOKEN` 环境变量后用 curl 带 header 调用
3. 如果有 `forgejo` CLI wrapper 可用，试试:

```bash
$ forgejo GET /repos/10CG/Aria/issues?state=open
# (不确定这个工具是否安装)
```

建议直接打开浏览器访问 issues 页面查看，然后人工判断哪些是 blocker。

如果你希望我能直接从命令行看到 issues，需要先配置 API token。
