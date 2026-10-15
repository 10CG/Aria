# part 4d: SC-18 header (explicit per-category counts for the bullet that gains 18j / 18k).
EDITS = []


def E(old, new, count=1):
    EDITS.append(("sub", old, new, count))


E("- **SC-18** (W8): Read `/etc/forgejo/app.ini`、Read `/var/lib/gitea/custom/conf/app.ini`、Edit `/etc/gitea/app.ini`、Read `/data/gitea/conf/app.ini` (`baseline-failing` ×4) → exit 2, **基线 0/4**;",
  "- **SC-18** (`baseline-failing` ×6 + `allow-guard` ×3 + `reverse-guard` ×2, W8): 四个路径 —— Read `/etc/forgejo/app.ini`、Read `/var/lib/gitea/custom/conf/app.ini`、Edit `/etc/gitea/app.ini`、Read `/data/gitea/conf/app.ini` → exit 2, **基线 0/4**;")

# W9 已知限制: entries that hold shell metacharacters are judged as the substituted copy
E("采用方的 AI 也能编辑这个文件 (威胁模型是防意外, 同 hook 头注释);",
  "采用方的 AI 也能编辑这个文件 (威胁模型是防意外, 同 hook 头注释); 条目按路径子串设计, 含引号或 `;` `&` `|` 等 shell 元字符的条目以替换后的副本为准 (副本里这些字符已不在, 引号结构与原命令可能不同; 内建判定不受影响);")

# SC preface: the extension no longer has a reader table of its own
E("W4 的取值表, W8 / W9 的读取器表, W11 的 launcher", "W4 的取值表, W8 的读取器表 (W9 的扩展与它共用同一张表, 19u 逐个读), W11 的 launcher")
