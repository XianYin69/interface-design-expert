#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge_index.py - 取九叶判据与清单路径（只读，不写 skill 目录）。"""
import sys, os, json, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE = os.path.join(ROOT, "asset", "knowledge_tree.json")


def load_tree(path):
    if not os.path.exists(path):
        return None, ["知识树缺失: %s" % path]
    try:
        doc = json.load(open(path, encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return None, ["知识树解析失败: %s" % exc]
    leaves = doc.get("leaves") or []
    return leaves, []


def leaf_view(leaf):
    kn = os.path.join(ROOT, "asset", leaf.get("knowledge", ""))
    ck = os.path.join(ROOT, "asset", leaf.get("checklist", ""))
    return {"id": leaf.get("id"), "title": leaf.get("title"),
            "authority": leaf.get("authority"),
            "knowledge_file": kn, "checklist_file": ck,
            "knowledge_exists": os.path.exists(kn), "checklist_exists": os.path.exists(ck),
            "keywords": leaf.get("keywords", [])}


def main():
    ap = argparse.ArgumentParser(description="interface-design-expert knowledge index")
    ap.add_argument("--topic", help="叶 id，如 error-model")
    ap.add_argument("--all", action="store_true", help="列全部九叶")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--tree", default=TREE)
    a = ap.parse_args()
    leaves, errs = load_tree(a.tree)
    if errs:
        print(json.dumps({"rc": 1, "errors": errs}, ensure_ascii=False))
        return 1
    if a.all:
        rows = [leaf_view(x) for x in leaves]
        missing = [r["id"] for r in rows if not (r["knowledge_exists"] and r["checklist_exists"])]
        print(json.dumps({"rc": 0, "count": len(rows), "leaves": rows,
                          "missing_files": missing}, ensure_ascii=False, indent=1))
        return 0 if not missing else 1
    if not a.topic:
        print(json.dumps({"rc": 1, "errors": ["须给 --topic 或 --all"]}, ensure_ascii=False))
        return 1
    hit = [x for x in leaves if x.get("id") == a.topic]
    if not hit:
        ids = [x.get("id") for x in leaves]
        print(json.dumps({"rc": 1, "topic": a.topic, "errors": ["叶不存在"],
                          "known": ids}, ensure_ascii=False))
        return 1
    row = leaf_view(hit[0])
    if a.format == "text":
        print("叶:", row["id"], "|", row["title"])
        print("权威:", row["authority"])
        print("判据:", row["knowledge_file"], "存在" if row["knowledge_exists"] else "缺失")
        print("清单:", row["checklist_file"], "存在" if row["checklist_exists"] else "缺失")
        print("关键词:", " ".join(row["keywords"]))
        return 0
    print(json.dumps({"rc": 0, "leaf": row}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
