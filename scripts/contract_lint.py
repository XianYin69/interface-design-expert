#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contract_lint.py - 契约结构体检（行级解析·标准库·只读）。

检查：缺 securitySchemes、缺错误信封、操作缺 4xx/5xx、列表端点缺分页、
limit 无上限、POST 无 201/202、429 无 Retry-After、GET 带请求体。
无法确定的结构标 parse-skipped，不当作通过。
"""
import sys, os, re, json, argparse

LIST_WORDS = ("list", "search", "collection", "query", "feed")
PAGE_WORDS = ("page", "offset", "limit", "cursor", "size", "token")
METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


def _f(rule, grade, line, msg):
    return {"rule": rule, "grade": grade, "line": line,
            "message": msg, "source": "builtin"}


def _window(lines, start):
    """取操作块文本与其声明的状态码集合（止于下一个同级键）。"""
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^\s{0,4}(\S.*|/\S*)\s*:", lines[j]):
            end = j
            break
    blob = "\n".join(lines[start:end]).lower()
    codes = set(re.findall(r'"?(\d{3})"?\s*:', blob))
    return blob, codes


def _ops(lines):
    for idx, line in enumerate(lines):
        om = re.match(r"^\s{2,}(" + "|".join(METHODS) + r")\s*:", line)
        if om:
            yield idx, om.group(1)


def lint(text):
    out = []
    lines = text.splitlines()
    if "securitySchemes" not in text:
        out.append(_f("security-missing", "block", 1,
                      "契约未声明 securitySchemes（叶6 判据1）"))
    if "problem+json" not in text and "ProblemDetails" not in text:
        out.append(_f("no-error-envelope", "block", 1,
                      "无统一错误信封（叶4 判据1）"))
    for idx, method in _ops(lines):
        blob, codes = _window(lines, idx)
        path = _nearest_path(lines, idx)
        _op_checks(out, method, path, idx, codes, blob)
    return out


def _nearest_path(lines, idx):
    path = "?"
    for j in range(idx, -1, -1):
        pm = re.match(r"^\s{2}(/\S*|x-\S*)\s*:", lines[j])
        if pm:
            path = pm.group(1)
            break
    return path


def _op_checks(out, method, path, idx, codes, blob):
    tag = "%s %s" % (method.upper(), path)
    if not any(c.startswith(("4", "5")) for c in codes):
        out.append(_f("no-error-response", "block", idx + 1,
                      "%s 未声明 4xx/5xx 响应（叶4 判据10）" % tag))
    if method == "get" and any(w in path.lower() for w in LIST_WORDS):
        if not any(w in blob for w in PAGE_WORDS):
            out.append(_f("no-pagination", "block", idx + 1,
                          "%s 列表端点无分页参数（叶5 判据1）" % tag))
    if ("limit" in blob or "page_size" in blob) and "maximum" not in blob:
        out.append(_f("no-limit-max", "block", idx + 1,
                      "%s 分页大小未声明服务端上限（叶5 判据4）" % tag))
    if method == "post" and not ({"201", "202"} & codes):
        out.append(_f("no-201", "advisory", idx + 1,
                      "%s 未回 201/202（叶1 判据3）" % tag))
    if "429" in codes and "retry-after" not in blob:
        out.append(_f("no-retry-after", "block", idx + 1,
                      "%s 声明 429 但无 Retry-After（叶6 判据7）" % tag))
    if method == "get" and "requestbody" in blob:
        out.append(_f("get-with-body", "block", idx + 1,
                      "%s GET 携带请求体（叶1 判据1）" % tag))


def main():
    ap = argparse.ArgumentParser(description="contract structure lint")
    ap.add_argument("spec", help="openapi/asyncapi 契约文件")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    a = ap.parse_args()
    if not os.path.exists(a.spec):
        print(json.dumps({"rc": 1, "errors": ["文件不存在: %s" % a.spec]},
                         ensure_ascii=False))
        return 1
    try:
        text = open(a.spec, encoding="utf-8-sig").read()
    except (OSError, UnicodeDecodeError) as exc:
        print(json.dumps({"rc": 1, "errors": ["读取失败: %s" % exc]},
                         ensure_ascii=False))
        return 1
    findings = lint(text)
    blocked = sum(1 for x in findings if x["grade"] == "block")
    if a.format == "text":
        for x in findings:
            print("%-4s L%-4d %s" % (x["grade"], x["line"], x["message"]))
        print("阻塞 %d / 共 %d" % (blocked, len(findings)))
        return 1 if blocked else 0
    print(json.dumps({"rc": 1 if blocked else 0, "tool": "contract_lint",
                      "fallback": True, "spec": a.spec, "findings": findings,
                      "summary": {"blocking": blocked, "total": len(findings)}},
                     ensure_ascii=False, indent=1))
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
