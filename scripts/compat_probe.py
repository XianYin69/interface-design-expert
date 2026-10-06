#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compat_probe.py - 新旧契约兼容性分级（additive / breaking / unknown）。

支持 .proto（消息字段号）与 OpenAPI/JSON 风格（路径、方法、必填、枚举）。
外部工具（buf/oasdiff）在位时优先采信其输出，本脚本结果标 fallback。
"""
import sys, os, re, json, argparse


def proto_fields(text):
    """{message: {field_no: (name, type)}}，并跳过 reserved 声明行。"""
    out, cur = {}, None
    for line in text.splitlines():
        mm = re.match(r"\s*message\s+(\w+)", line)
        if mm:
            cur = mm.group(1)
            out[cur] = {}
            continue
        if re.match(r"\s*reserved\s", line):
            continue
        if cur:
            fm = re.match(r"\s*(?:repeated\s+|optional\s+)?([\w.]+)\s+(\w+)"
                          r"\s*=\s*(\d+)\s*;", line)
            if fm:
                out[cur][int(fm.group(3))] = (fm.group(2), fm.group(1))
    return out


def proto_reserved(text):
    """已 reserved 的字段号与字段名（删除字段的安全凭据）。"""
    nums, names = set(), set()
    for m in re.finditer(r"reserved\s+([^;]+);", text):
        for tok in m.group(1).split(","):
            tok = tok.strip()
            if re.match(r"^\d+$", tok):
                nums.add(int(tok))
            elif tok.strip('"'):
                names.add(tok.strip('"'))
    return nums, names


def proto_enums(text):
    """{enum: {value_name: number}}"""
    out, cur = {}, None
    for line in text.splitlines():
        em = re.match(r"\s*enum\s+(\w+)", line)
        if em:
            cur = em.group(1)
            out[cur] = {}
            continue
        if cur:
            vm = re.match(r"\s*([A-Z][A-Z0-9_]+)\s*=\s*(\d+)\s*;", line)
            if vm:
                out[cur][vm.group(1)] = int(vm.group(2))
            elif re.match(r"\s*}", line):
                cur = None
    return out


def openapi_ops(text):
    """{(path, method): {"required": [...], "enum": [...]}} 行级抽取。"""
    ops, cur_path = {}, "?"
    for line in text.splitlines():
        pm = re.match(r"^\s{2}(/\S*|x-\S*)\s*:", line)
        if pm:
            cur_path = pm.group(1)
            continue
        om = re.match(r"^\s{4}(get|post|put|patch|delete|head|options)\s*:", line)
        if om:
            ops[(cur_path, om.group(1))] = {"required": set(), "enum": set()}
            continue
        cur = ops.get((cur_path, _last_method(ops, cur_path)))
        if cur is None:
            continue
        for req in re.findall(r"^\s+-\s+(\w+)\s*$", line):
            if "required" in line.lower():
                cur["required"].add(req)
        for val in re.findall(r"enum:\s*\[([^\]]*)\]", line):
            cur["enum"].update(v.strip() for v in val.split(",") if v.strip())
    return ops


def _last_method(ops, path):
    for (p, m) in reversed(list(ops)):
        if p == path:
            return m
    return None


def diff_proto(old, new):
    findings = []
    o, n = proto_fields(old), proto_fields(new)
    rnums, rnames = proto_reserved(new)
    for msg, ofields in o.items():
        nfields = n.get(msg, {})
        for no, (name, typ) in ofields.items():
            if no not in nfields:
                if no in rnums or name in rnames:
                    findings.append(("additive", msg,
                                     "field %d(%s) 已删除且 reserved" % (no, name),
                                     "号与名不可复用，安全"))
                else:
                    findings.append(("breaking", msg,
                                     "field %d(%s) 被删除且未 reserved" % (no, name),
                                     "旧号可能被复用为静默错值"))
            elif nfields[no][1] != typ:
                findings.append(("breaking", msg, "field %d 类型 %s→%s" % (no, typ,
                                 nfields[no][1]), "wire 兼容需分别声明"))
            elif nfields[no][0] != name:
                findings.append(("breaking", msg, "field %d 改名 %s→%s" % (no, name,
                                 nfields[no][0]), "JSON 侧按名匹配"))
        for no, (name, typ) in nfields.items():
            if no not in ofields:
                findings.append(("additive", msg, "新增 field %d(%s)" % (no, name),
                                 "字段号不得复用旧号"))
    for msg in set(n) - set(o):
        findings.append(("additive", msg, "新增 message", "旧客户端不读取，安全"))
    oe, ne = proto_enums(old), proto_enums(new)
    for en, ovals in oe.items():
        nvals = ne.get(en, {})
        for v in set(nvals) - set(ovals):
            findings.append(("unknown", en, "枚举新增 %s=%d" % (v, nvals[v]),
                             "旧客户端读侧可能破坏，须取证（叶2 判据4）"))
        for v in set(ovals) - set(nvals):
            findings.append(("breaking", en, "枚举值 %s 被移除" % v,
                             "旧数据无法解码"))
    return findings


def diff_openapi(old, new):
    findings = []
    o, n = openapi_ops(old), openapi_ops(new)
    for key in set(o) - set(n):
        findings.append(("breaking", key, "端点被移除", "旧客户端 404"))
    for key in set(n) - set(o):
        findings.append(("additive", key, "端点新增", "需声明版本机制唯一"))
    for key in set(o) & set(n):
        added = n[key]["required"] - o[key]["required"]
        if added:
            findings.append(("breaking", key, "新增必填 %s" % sorted(added),
                             "旧客户端不发即 400"))
        enum_added = n[key]["enum"] - o[key]["enum"]
        if enum_added:
            findings.append(("unknown", key, "枚举新增值 %s" % sorted(enum_added),
                             "旧客户端读侧可能破坏，须取证"))
    return findings


def classify(kind, old, new):
    if kind == "proto":
        return diff_proto(old, new)
    return diff_openapi(old, new)


def read(path):
    if not path or not os.path.exists(path):
        return None
    return open(path, encoding="utf-8-sig").read()


def main():
    ap = argparse.ArgumentParser(description="contract compatibility probe")
    ap.add_argument("--old", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--kind", choices=["auto", "proto", "openapi"], default="auto")
    a = ap.parse_args()
    old, new = read(a.old), read(a.new)
    if old is None or new is None:
        print(json.dumps({"rc": 1, "errors": ["旧版或新版契约缺失"]}, ensure_ascii=False))
        return 1
    kind = a.kind
    if kind == "auto":
        kind = "proto" if (a.old.endswith(".proto") or "syntax = \"proto3\"" in old) \
            else "openapi"
    rows = classify(kind, old, new)
    items = [{"grade": g, "target": str(t), "change": c, "note": nt}
             for g, t, c, nt in rows]
    summary = {k: sum(1 for x in items if x["grade"] == k)
               for k in ("breaking", "additive", "unknown")}
    print(json.dumps({"rc": 0, "tool": "compat_probe", "kind": kind,
                      "fallback": True, "items": items, "summary": summary,
                      "verdict": "breaking" if summary["breaking"] else
                                 ("unknown" if summary["unknown"] else "additive")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
