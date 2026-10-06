#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""error_model_probe.py - 错误模型完备性体检。

检查：统一信封（RFC 9457 键）、错误响应声明覆盖率、业务码、字段级错误、
重试语义可推性、200 承载失败、内部信息泄露。只读、标准库。
"""
import sys, os, re, json, argparse

P9457 = ("type", "title", "status", "detail", "instance")
RETRYABLE = {"408", "425", "429", "500", "502", "503", "504"}
NON_RETRYABLE = {"400", "401", "403", "404", "405", "409", "410", "415", "422"}
LEAK = ("traceback", "stack", "sql", "jdbc:", "password", "token=", "secret")


def _f(rule, grade, line, msg):
    return {"rule": rule, "grade": grade, "line": line, "message": msg,
            "source": "builtin"}


def probe(text):
    out = []
    low = text.lower()
    keys = sum(1 for k in P9457 if re.search(r"^\s*-?\s*%s\s*:" % k, text, re.M))
    if keys < 3:
        out.append(_f("no-envelope", "block", 1,
                      "未见 RFC 9457 错误信封（命中键 %d/5，叶4 判据1）" % keys))
    ops = re.findall(r"^\s{4}(get|post|put|patch|delete)\s*:", text, re.M)
    err_declared = len(re.findall(r'"?[45]\d\d"?\s*:', text))
    if ops and err_declared == 0:
        out.append(_f("errors-undeclared", "block", 1,
                      "%d 个操作但契约未声明任何错误响应（叶4 判据10）" % len(ops)))
    if "success" in low and re.search(r"success.{0,20}false", low):
        out.append(_f("success-flag", "block", 1,
                      "存在 success=false 型载荷（与状态码构成双事实源，叶4 判据6）"))
    if not re.search(r"\bcode\b", low):
        out.append(_f("no-biz-code", "advisory", 1,
                      "未见业务码字段，自动化处理困难（叶4 判据3）"))
    if not re.search(r"errors\s*:|field\s*:", text, re.I):
        out.append(_f("no-field-errors", "advisory", 1,
                      "未见字段级错误结构（叶4 判据4）"))
    for kw in LEAK:
        if kw in low:
            ln = low.count("\n", 0, low.find(kw)) + 1
            out.append(_f("info-leak", "block", ln,
                          "错误样例含内部信息 %s（叶4 判据8）" % kw))
    codes = set(re.findall(r'"?(\d{3})"?\s*:', text))
    for c in codes & RETRYABLE:
        if c == "429" and "retry-after" not in low:
            out.append(_f("no-retry-after", "block", 1,
                          "429 无 Retry-After，重试语义不可推（叶4 判据5）"))
    return out


def main():
    ap = argparse.ArgumentParser(description="error model probe")
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--text", default="")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    a = ap.parse_args()
    text = a.text
    if a.spec:
        if not os.path.exists(a.spec):
            print(json.dumps({"rc": 1, "errors": ["文件不存在"]}, ensure_ascii=False))
            return 1
        text = open(a.spec, encoding="utf-8-sig").read()
    if not text.strip():
        print(json.dumps({"rc": 1, "errors": ["无输入"]}, ensure_ascii=False))
        return 1
    found = probe(text)
    blocked = sum(1 for x in found if x["grade"] == "block")
    if a.format == "text":
        for x in found:
            print("%-8s L%-4d %s" % (x["grade"], x["line"], x["message"]))
    else:
        print(json.dumps({"rc": 1 if blocked else 0, "tool": "error_model_probe",
                          "fallback": True, "findings": found,
                          "retryable_codes": sorted(RETRYABLE),
                          "summary": {"blocking": blocked, "total": len(found)}},
                         ensure_ascii=False, indent=1))
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
