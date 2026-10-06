#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""advice_compose.py - 证据 + 结论 → 交付报告（六段式，含边界与未覆盖）。

用法：
  python advice_compose.py --topic error-model --verdict tmp/verdict.json
  python advice_compose.py --topic error-model --evidence tmp/lint.json --out tmp/report.md
verdict.json 期望键：findings[]/blocking/advisory/boundary/uncovered/evidence。
缺 boundary 或 uncovered 即判不合格（rc=1）。
"""
import sys, os, json, argparse

HEAD = ("结论", "阻塞项", "建议", "取证", "边界", "未覆盖")


def load(path):
    if not path or not os.path.exists(path):
        return {}
    try:
        return json.load(open(path, encoding="utf-8-sig"))
    except ValueError as exc:
        return {"_error": "verdict 解析失败: %s" % exc}


def compose(topic, verdict, evidence):
    items = verdict.get("findings") or []
    blocking = [x for x in items if str(x.get("grade", "")).lower() == "block"]
    advisory = [x for x in items if str(x.get("grade", "")).lower() == "advisory"]
    lines = []
    lines.append("结论：%s · blocking %d · advisory %d · info %d" % (
        topic, len(blocking), len(advisory),
        len(items) - len(blocking) - len(advisory)))
    lines.append(verdict.get("headline", "（缺主判断，须补一句话结论）"))
    lines.append("")
    lines.append("阻塞项：")
    for x in blocking or []:
        lines.append("- %s → 证据：%s → 最小修复：%s" % (
            x.get("message", "?"), x.get("evidence", "无取证"),
            x.get("fix", "未给（须补）")))
    if not blocking:
        lines.append("- 无")
    lines.append("")
    lines.append("建议：")
    for x in verdict.get("advice", []) or []:
        lines.append("- 形状：%s → 理由：%s → 迁移窗口：%s" % (
            x.get("shape", "?"), x.get("reason", "缺出处"), x.get("window", "未声明")))
    lines.append("")
    lines.append("取证：")
    for e in (verdict.get("evidence") or []) + (evidence or []):
        lines.append("- %s" % (e if isinstance(e, str) else json.dumps(
            e, ensure_ascii=False)))
    lines.append("")
    lines.append("边界：%s" % verdict.get("boundary", "【缺项·判不合格】"))
    lines.append("未覆盖：%s" % verdict.get("uncovered", "【缺项·判不合格】"))
    transfer = verdict.get("transfer") or []
    if transfer:
        lines.append("转派：" + "；".join(
            "%s→%s" % (t.get("issue", "?"), t.get("skill", "?")) for t in transfer))
    ok = bool(verdict.get("boundary")) and bool(verdict.get("uncovered"))
    return "\n".join(lines), ok


def main():
    ap = argparse.ArgumentParser(description="compose delivery report")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--verdict", help="结构化结论 JSON")
    ap.add_argument("--evidence", help="探针输出 JSON（追加到取证段）")
    ap.add_argument("--out", help="写入路径（仅允许工作区 tmp/）")
    a = ap.parse_args()
    verdict = load(a.verdict)
    if verdict.get("_error"):
        print(json.dumps({"rc": 1, "errors": [verdict["_error"]]}, ensure_ascii=False))
        return 1
    evidence = []
    ev = load(a.evidence)
    if ev:
        evidence = [json.dumps(ev, ensure_ascii=False)]
    text, ok = compose(a.topic, verdict, evidence)
    if a.out:
        norm = os.path.normpath(a.out)
        if "tmp" not in norm.split(os.sep):
            print(json.dumps({"rc": 1,
                              "errors": ["交付写盘只允许 tmp/（垃圾回收约束）"]},
                             ensure_ascii=False))
            return 1
        os.makedirs(os.path.dirname(norm) or ".", exist_ok=True)
        open(norm, "w", encoding="utf-8").write(text + "\n")
    print(text)
    if not ok:
        print("\n[不合格] 缺「边界」或「未覆盖」段（输出约束）")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
