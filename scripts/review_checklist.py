#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""review_checklist.py - 解析 asset/checklists/<叶>.md 为判定表骨架。"""
import sys, os, re, json, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEM = re.compile(r"^[-*]\s*(BLOCK|advisory|info)\s+(.+)$", re.I)


def parse(md_path):
    if not os.path.exists(md_path):
        return None, ["清单缺失: %s" % md_path]
    items, errs = [], []
    for n, line in enumerate(open(md_path, encoding="utf-8-sig"), 1):
        m = ITEM.match(line.strip())
        if not m:
            continue
        items.append({"no": len(items) + 1, "line": n,
                      "grade": m.group(1).lower(), "item": m.group(2).strip(),
                      "state": "todo", "evidence": "", "fix": ""})
    if not items:
        errs.append("未解析到条目（检查 BLOCK/advisory 前缀）")
    return items, errs


def main():
    ap = argparse.ArgumentParser(description="review checklist loader")
    ap.add_argument("--topic", required=True, help="叶 id")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--blocking-only", action="store_true", help="临时评审只取阻塞项")
    a = ap.parse_args()
    path = os.path.join(ROOT, "asset", "checklists", "%s.md" % a.topic)
    items, errs = parse(path)
    if errs:
        print(json.dumps({"rc": 1, "topic": a.topic, "errors": errs}, ensure_ascii=False))
        return 1
    rows = items
    if a.blocking_only:
        rows = [x for x in items if x["grade"] == "block"]
    summary = {"total": len(items),
               "blocking": sum(1 for x in items if x["grade"] == "block"),
               "advisory": sum(1 for x in items if x["grade"] == "advisory"),
               "info": sum(1 for x in items if x["grade"] == "info")}
    if a.format == "text":
        print("叶:", a.topic, "| 条目", summary["total"], "| 阻塞", summary["blocking"])
        for x in rows:
            print("  [%s] %d. %s" % (x["grade"][:4], x["no"], x["item"]))
        return 0
    print(json.dumps({"rc": 0, "topic": a.topic, "summary": summary,
                      "items": rows,
                      "note": "state 由评审人/上游节点填 pass|fail|n-a"},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
