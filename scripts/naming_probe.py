#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""naming_probe.py - 命名一致性体检：风格混用、同义异名、空泛名、动词式路径。

只读、标准库。规范关键字（OpenAPI/JSON Schema/AsyncAPI 结构键）不参与风格统计，
避免把 `operationId`/`maxLength` 误判成与业务字段风格混用。
"""
import sys, os, re, json, argparse

SNAKE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")
CAMEL = re.compile(r"^[a-z][a-z0-9]*([A-Z][a-z0-9]*)+$")
PASCAL = re.compile(r"^[A-Z][a-z0-9]*([A-Z][a-z0-9]*)*$")
EMPTY = ("data", "info", "misc", "flag", "temp", "extra", "stuff", "value2")
VERB_PATH = re.compile(r"^(get|create|update|delete|do|query|fetch|set)[A-Z]")

RESERVED = {
    "operationId", "requestBody", "securitySchemes", "bearerFormat", "minLength",
    "maxLength", "minItems", "maxItems", "uniqueItems", "additionalProperties",
    "patternProperties", "exclusiveMinimum", "exclusiveMaximum", "discriminator",
    "responseRequired", "propertyNames", "contains", "const", "contentEncoding",
    "contentMediaType", "default", "example", "examples", "format", "pattern",
    "deprecated", "nullable", "readOnly", "writeOnly", "contentType",
    "correlationId", "deliveryGuarantee", "maxAttempts", "retryCount",
    "deadLetter", "backoff", "ordering", "bindings", "headers", "payload",
    "message", "messages", "channel", "channels", "operations", "action",
    "address", "servers", "server", "paths", "components", "schemas",
    "responses", "parameters", "request", "security", "tags", "externalDocs",
    "version", "title", "description", "summary", "type", "items", "required",
    "properties", "schema", "content", "in", "name", "url", "openapi",
    "status", "detail", "instance", "errors", "field", "code", "retryable",
    "info", "contact", "license", "termsOfService", "asyncapi", "syntax",
    "package", "import", "option", "message", "enum", "reserved", "rpc",
    "service", "returns", "oneof", "map", "extend", "groups", "input",
    "directive", "scalar", "interface", "union", "impl", "query", "mutation",
}

SYNONYM_GROUPS = (
    {"id", "uuid", "guid", "identifier"},
    {"userid", "uid", "userkey", "userkeyid"},
    {"createdat", "createdtime", "createtime", "ctime", "createdtimestamp"},
    {"updatedat", "updatedtime", "mtime", "modifiedat"},
    {"pagetotal", "totalcount", "totalsize", "recordcount", "count"},
    {"isdeleted", "deleted", "softdeleted", "trashed"},
)


def style_of(name):
    if SNAKE.match(name):
        return "snake_case"
    if CAMEL.match(name):
        return "camelCase"
    if PASCAL.match(name):
        return "PascalCase"
    return "other"


def norm(name):
    return re.sub(r"[_\-\s]", "", name).lower()


def names_from(text):
    """抽字段名：YAML/JSON 键 + proto 字段（含 repeated/optional 前缀）。"""
    out = []
    for m in re.finditer(r"^\s*-?\s*([A-Za-z_]\w*)\s*:", text, re.M):
        out.append((m.group(1), text[:m.start()].count("\n") + 1))
    for m in re.finditer(PROTO_FIELD, text, re.M):
        out.append((m.group(1), text[:m.start()].count("\n") + 1))
    return [(n, ln) for n, ln in out if n not in RESERVED]


def _style_mix(pairs):
    styles = {}
    for nm, ln in pairs:
        st = style_of(nm)
        if st not in ("snake_case", "camelCase"):
            continue
        styles.setdefault(st, []).append((nm, ln))
    if len(styles) < 2:
        return []
    main = max(styles, key=lambda k: len(styles[k]))
    found = []
    for st, lst in styles.items():
        if st == main:
            continue
        for nm, ln in lst[:5]:
            found.append({"rule": "style-mix", "grade": "block", "line": ln,
                          "message": "%s(%s) 与主风格 %s 混用（叶9 判据1）" % (
                              nm, st, main), "source": "builtin"})
    return found


def _synonyms(pairs):
    buckets = {}
    for nm, ln in pairs:
        buckets.setdefault(norm(nm), []).append((nm, ln))
    found = []
    for grp in SYNONYM_GROUPS:
        uniq = {}
        for key, vals in buckets.items():
            if key in grp:
                for nm, ln in vals:
                    uniq.setdefault(nm, ln)
        if len(uniq) > 1:
            found.append({"rule": "synonym", "grade": "block",
                          "line": min(uniq.values()),
                          "message": "同一概念多个名字 %s（叶9 判据3）" % sorted(uniq),
                          "source": "builtin"})
    return found


PROTO_FIELD = (r"^\s*(?:(?:repeated|optional)\s+)?"
               r"(?:string|int32|int64|bool|bytes|float|double)"
               r"\s+(\w+)\s*=\s*\d+")


def _vague(pairs):
    found = []
    for nm, ln in pairs:
        if nm.lower() in EMPTY:
            found.append({"rule": "vague-name", "grade": "advisory", "line": ln,
                          "message": "空泛命名 %s（叶9 判据2）" % nm,
                          "source": "builtin"})
    return found


def _verb_paths(text):
    found = []
    for m in re.finditer(r"^\s{2}(/(\w+))", text, re.M):
        seg = m.group(2)
        if VERB_PATH.match(seg):
            found.append({"rule": "verb-path", "grade": "block",
                          "line": text[:m.start()].count("\n") + 1,
                          "message": "动词式路径 /%s（叶1 判据5）" % seg,
                          "source": "builtin"})
    return found


def probe(text):
    pairs = names_from(text)
    out = []
    out.extend(_style_mix(pairs))
    out.extend(_synonyms(pairs))
    out.extend(_vague(pairs))
    out.extend(_verb_paths(text))
    return out


def main():
    ap = argparse.ArgumentParser(description="naming consistency probe")
    ap.add_argument("spec", nargs="?", help="契约文件；缺省读 --text")
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
        print("阻塞 %d / 共 %d" % (blocked, len(found)))
    else:
        print(json.dumps({"rc": 1 if blocked else 0, "tool": "naming_probe",
                          "fallback": True, "findings": found,
                          "summary": {"blocking": blocked, "total": len(found)}},
                         ensure_ascii=False, indent=1))
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
