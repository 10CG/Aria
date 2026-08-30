#!/usr/bin/env python3
"""Aria 应用级 Forgejo token 活性 + 指纹漂移检查 (state-check `forgejo-app-token-liveness`)。

背景 (2026-08-29/30): `nomad/jobs/aria-layer2-runner.FORGEJO_BOT_PAT` 里躺着一枚 Forgejo 早已不认的
token (401 `user does not exist [uid: 0]`), 最可能是 2026-05-23 吊销 token 时没枚举 Nomad 变量 store
留下的。它在变量里躺了三个月无人察觉 —— 因为 Aria 侧没有任何东西在问「变量里那枚 token 还能登录吗」。
本检查就是那个「问」。台账 = `.aria/pat-inventory.yaml` (归属判据见其头注)。

做什么 (对台账里 liveness.enabled 的每一条):
  1. 从 Nomad HTTP API 读该变量, 取指定键 (进程内, 不落盘、不打印)
  2. 算指纹 sha256(token)[:8], 与台账登记值比对 → 漂移 = 有人换了值没改台账 (或反之)
  3. 用它 GET Forgejo 内网端点 (与生产消费点同一条路径), 只看 http code

判据 (全分割):
  Nomad 不可达 / 台账缺失或不可解析                → SKIP (exit 0 + 首行 SKIP 前缀 = collector 的 skip 协议; 可见, 非 PASS 非 FAIL —— 零证据不当正证据)
  任一条: 变量缺键 / http 401 (token 不存在)      → FAIL (exit 1)
  任一条: 指纹 != 台账                            → FAIL (漂移; 即使 token 活着, 台账已失真)
  任一条: http 403 (活着但 scope 不够到这个端点)   → FAIL (端点是按该 token 应有 scope 选的)
  任一条: 其他 code / 网络错                       → FAIL (fail-closed)
  全部 200 且指纹一致                              → PASS (exit 0)

Rule #7 (secret-hygiene): token 值只在内存里经过, 任何输出/异常文案都不含它; 输出只有 id / http code /
指纹 8 位 / 判定。urllib 异常只取 code 或 reason 类名。
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# Nomad 与 Forgejo 内网端点一律直连: 本机 shell 设了代理环境变量, urllib 默认跟着走, 内网地址
# 在代理侧回 502 Bad Gateway, 表现成「Nomad 不可达」。2026-08-30 实测: 同一 URL 默认 opener 失败,
# ProxyHandler({}) 直连成功 (curl 同样直连正常)。
_DIRECT = urllib.request.build_opener(urllib.request.ProxyHandler({}))
INVENTORY = ROOT / ".aria" / "pat-inventory.yaml"
HTTP_TIMEOUT = 6


def load_inventory() -> dict | None:
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    try:
        with INVENTORY.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


def nomad_var_items(nomad_addr: str, path: str) -> dict | None:
    """返回变量的 Items dict; 不可达/不存在 → None。绝不打印返回体。"""
    url = f"{nomad_addr.rstrip('/')}/v1/var/{path}"
    try:
        with _DIRECT.open(url, timeout=HTTP_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError):
        return None
    items = data.get("Items") if isinstance(data, dict) else None
    return items if isinstance(items, dict) else None


def forgejo_probe(base: str, endpoint: str, token: str) -> tuple[int, str]:
    """GET base/api/v1/endpoint 带 token; 返回 (http_code, 简短原因)。0 = 网络层失败。"""
    req = urllib.request.Request(
        f"{base.rstrip('/')}/api/v1/{endpoint.lstrip('/')}",
        headers={"Authorization": f"token {token}", "Accept": "application/json",
                 "User-Agent": "aria-token-liveness/1.0"},
    )
    try:
        with _DIRECT.open(req, timeout=HTTP_TIMEOUT) as resp:
            resp.read(200)  # 不保留正文
            return resp.status, "ok"
    except urllib.error.HTTPError as e:
        return e.code, f"http_{e.code}"
    except (urllib.error.URLError, OSError) as e:
        return 0, type(e).__name__


def fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]


def main() -> int:
    inv = load_inventory()
    if inv is None:
        print(f"##SKIP## (台账 {INVENTORY.relative_to(ROOT)} 缺失/不可解析, 或 PyYAML 不可用)")
        return 0
    defaults = inv.get("defaults") or {}
    nomad_addr = os.environ.get("NOMAD_ADDR") or defaults.get("nomad_addr") or "http://127.0.0.1:4646"
    forgejo = (os.environ.get("ARIA_FORGEJO_INTERNAL_URL")
               or defaults.get("forgejo_internal_url") or "http://192.168.69.200:3000")

    targets = [t for t in (inv.get("tokens") or [])
               if isinstance(t, dict) and (t.get("liveness") or {}).get("enabled", False)
               and (t.get("store") or {}).get("type") == "nomad-variable"]
    if not targets:
        print("##SKIP## (台账里没有开启 liveness 的条目)")
        return 0

    lines: list[str] = []
    failed: list[str] = []
    skipped: list[str] = []
    for t in targets:
        tid = str(t.get("id", "?"))
        store = t["store"]
        live = t["liveness"]
        items = nomad_var_items(nomad_addr, store["path"])
        if items is None:
            skipped.append(tid)
            lines.append(f"{tid}: SKIP nomad 变量不可读 ({store['path']})")
            continue
        token = items.get(store["key"])
        if not isinstance(token, str) or not token:
            failed.append(tid)
            lines.append(f"{tid}: FAIL 变量缺键 {store['key']}")
            continue
        fp = fingerprint(token)
        expect_fp = str(t.get("fingerprint") or "")
        code, why = forgejo_probe(forgejo, str(live.get("endpoint", "user")), token)
        want = int(live.get("expect", 200))
        drift = "" if fp == expect_fp else f" 指纹漂移(台账 {expect_fp})"
        if code == want and not drift:
            lines.append(f"{tid}: OK http={code} fp={fp}")
        else:
            failed.append(tid)
            if code == 401:
                verdict = "DEAD (Forgejo 不认这枚 token)"
            elif code == 403:
                verdict = "SCOPE (活着但到不了该端点)"
            elif code == 0:
                verdict = f"NET ({why})"
            else:
                verdict = f"UNEXPECTED http={code}"
            lines.append(f"{tid}: FAIL {verdict} fp={fp}{drift}")

    if failed:
        head = f"FAIL {len(failed)}/{len(targets)} token 异常: " + ", ".join(failed)
        rc = 1
    elif skipped:
        head = f"##SKIP## {len(skipped)}/{len(targets)} 条 nomad 不可达 (其余 OK)"
        rc = 0
    else:
        head = f"OK ({len(targets)} 枚应用级 token 活性正常, 指纹与台账一致)"
        rc = 0
    print(head)
    for ln in lines:
        print("  " + ln)
    return rc


if __name__ == "__main__":
    sys.exit(main())
