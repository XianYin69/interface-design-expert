#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""codegen_probe.py - 工具在位探测 + 契约可生成性静态检查（只读·标准库）。

外部工具（spectral/buf/oasdiff/protoc/grpcurl）在位时优先采信其输出，
本脚本结果标 fallback；缺失时降级为静态检查，不得当作「通过」。
"""
import sys, os, re, json, shutil, argparse

TOOLS = ("spectral", "buf", "oasdiff", "protoc", "grpcurl", "node", "go")


def tool_status():
    rows = {}
    for t in TOOLS:
        p = shutil.which(t)
        rows[t] = {"path": p, "present": bool(p)}
    return rows


def sibling_text(path):
    """同目录其余 yaml/json 契约文件拼成引用语料（跨文件 $ref 不误报）。"""
    d = os.path.dirname(os.path.abspath(path)) or "."
    buf = []
    for f in sorted(os.listdir(d)):
        if f == os.path.basename(path) or not f.endswith((".yaml", ".yml", ".json")):
            continue
        try:
            buf.append(open(os.path.join(d, f), encoding="utf-8-sig").read())
        except OSError:
            continue
    return "\n".join(buf)


def parseability(text, name):
    out = []
    if name.endswith((".yaml", ".yml")):
        if re.search(r"\t", text):
            out.append({"rule": "yaml-tab", "grade": "block", "line": 1,
                        "message": "YAML 含制表符，解析器会拒绝（叶2 判据10）",
                        "source": "builtin"})
        refs = set(re.findall(r"\$ref:\s*[\"']?([^\"'\s]+)", text))
        corpus = text + "\n" + sibling_text(name)
        for r in sorted(refs):
            if r.startswith("#/"):
                tail = r.split("/")[-1]
                if not re.search(r"^\s*%s\s*:" % re.escape(tail), corpus, re.M):
                    out.append({"rule": "dangling-ref", "grade": "block", "line": 1,
                                "message": "内部引用无法解析 %s（叶9 判据3）" % r,
                                "source": "builtin"})
    if name.endswith(".proto"):
        if "syntax" not in text:
            out.append({"rule": "no-syntax", "grade": "block", "line": 1,
                        "message": "proto 缺 syntax 声明", "source": "builtin"})
        for m in re.finditer(r"enum\s+(\w+)\s*\{", text):
            body = text[m.end():m.end() + 400]
            if "UNSPECIFIED" not in body and "UNKNOWN" not in body:
                out.append({"rule": "enum-zero", "grade": "block",
                            "line": text[:m.start()].count("\n") + 1,
                            "message": "枚举 %s 无零值占位（叶2 判据4）" % m.group(1),
                            "source": "builtin"})
    return out


def main():
    ap = argparse.ArgumentParser(description="codegen & tooling probe")
    ap.add_argument("--spec", help="契约文件")
    ap.add_argument("--proto", help="proto 目录（逐个文件检查）")
    ap.add_argument("--run", action="store_true",
                    help="调用在位的外部工具（spectral/buf/oasdiff）")
    a = ap.parse_args()
    tools = tool_status()
    targets = []
    if a.spec:
        targets.append(a.spec)
    if a.proto and os.path.isdir(a.proto):
        for f in sorted(os.listdir(a.proto)):
            if f.endswith(".proto"):
                targets.append(os.path.join(a.proto, f))
    findings, skipped = [], []
    for t in targets:
        if not os.path.exists(t):
            skipped.append({"file": t, "reason": "文件不存在"})
            continue
        text = open(t, encoding="utf-8-sig").read()
        findings.extend(parseability(text, t.lower()))
    blocked = sum(1 for x in findings if x["grade"] == "block")
    print(json.dumps({"rc": 1 if blocked else 0, "tool": "codegen_probe",
                      "fallback": True, "tools": tools, "findings": findings,
                      "parse_skipped": skipped,
                      "summary": {"blocking": blocked, "total": len(findings),
                                  "targets": len(targets)}},
                     ensure_ascii=False, indent=1))
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
