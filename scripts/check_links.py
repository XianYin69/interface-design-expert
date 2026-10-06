#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_links.py - 悬空链接校验（红线：悬空=0）+ [联网]/[本地] 与 URL 计数。

用法：python check_links.py [--root <dir>] [--strict-url] [--max-md-lines N]
  --root          扫描根（默认＝本脚本所在 skill 目录）
  --strict-url    额外统计 [联网]/[本地] 计数与 URL 数
  --max-md-lines  附带 .md 行数红线检查（默认 50）
"""
import os, re, sys, json, argparse

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
NET = re.compile(r"\[联网\]")
LOC = re.compile(r"\[本地\]")
URL = re.compile(r"https?://[^\s)\]|]+")
SKIP_DIRS = ("tmp", ".git", "__pycache__", "node_modules")


def scan(root, max_lines):
    bad, long_md, net, loc, urls, md_count = [], [], 0, 0, set(), 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.endswith(".md"):
                continue
            md_count += 1
            p = os.path.join(dp, f)
            txt = open(p, encoding="utf-8-sig").read()
            n = len(txt.splitlines())
            if n > max_lines:
                long_md.append((os.path.relpath(p, root), n))
            for m in LINK.finditer(txt):
                tgt = m.group(1).split("#")[0].strip()
                if not tgt or tgt.startswith(("http:", "https:", "mailto:")):
                    continue
                full = os.path.normpath(os.path.join(dp, tgt))
                if not os.path.exists(full):
                    bad.append((os.path.relpath(p, root), tgt))
            net += len(NET.findall(txt))
            loc += len(LOC.findall(txt))
            urls.update(URL.findall(txt))
    return bad, long_md, net, loc, urls, md_count


def main():
    ap = argparse.ArgumentParser(description="dangling link & md line check")
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--root", default=default_root)
    ap.add_argument("--strict-url", action="store_true")
    ap.add_argument("--max-md-lines", type=int, default=50)
    a = ap.parse_args()
    bad, long_md, net, loc, urls, md_count = scan(a.root, a.max_md_lines)
    for p, t in bad:
        print("悬空:", p, "->", t)
    for p, n in long_md:
        print("超行:", p, "=", n, "行")
    print(json.dumps({"dangling": len(bad), "md_over_limit": len(long_md),
                      "md_files": md_count}, ensure_ascii=False))
    if a.strict_url:
        print(json.dumps({"online_cited": net, "local_only": loc,
                          "unique_urls": len(urls)}, ensure_ascii=False))
    return 1 if (bad or long_md) else 0


if __name__ == "__main__":
    sys.exit(main())
