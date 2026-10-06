#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""classify_topic.py - map a request/contract to interface-design-expert leaves."""
import sys, json, argparse, io, os

TOPICS = {
    "http-rest-semantics": ["rest", "http", "method", "status", "get ", "post", "put",
                            "patch", "delete", "idempotent", "safe", "resource", "uri",
                            "hateoas", "content-type", "accept", "cache-control", "etag",
                            "if-match", "语义", "方法", "状态码", "资源", "幂等", "缓存"],
    "schema-contracts": ["openapi", "swagger", "asyncapi", "proto", "protobuf", "grpc",
                         "graphql", "json schema", "schema", "contract", "oneof", "enum",
                         "nullable", "required", "payload", "契约", "模式", "字段", "消息", "事件"],
    "versioning-compatibility": ["version", "semver", "breaking", "compat", "additive",
                                 "deprecat", "sunset", "migration", "abi", "binary",
                                 "wire", "reserved", "field number", "版本", "兼容",
                                 "破坏性", "废弃", "迁移", "二进制"],
    "error-model": ["error", "problem", "problem+json", "rfc9457", "error code",
                    "details", "retryable", "4xx", "5xx", "fault", "errors[]", "urn",
                    "错误", "报错", "故障", "失败", "校验失败"],
    "pagination-filtering-sorting": ["page", "offset", "limit", "cursor", "pagination",
                                     "page_token", "next_token", "sort", "order_by",
                                     "filter", "fields", "select", "total", "has_more",
                                     "分页", "翻页", "排序", "过滤", "裁剪"],
    "security-authn-authz": ["auth", "oauth", "bearer", "jwt", "api key", "apikey",
                             "scope", "role", "permission", "tls", "mtls", "rate limit",
                             "ratelimit", "429", "retry-after", "rotation", "secret",
                             "安全", "认证", "授权", "限流", "凭据", "越权"],
    "reliability": ["timeout", "deadline", "cancel", "retry", "backoff", "jitter",
                    "circuit", "breaker", "idempotency-key", "dedup", "at-least-once",
                    "exactly-once", "queue", "dead letter", "saga", "可靠性", "超时",
                    "退避", "熔断", "重试", "降级"],
    "observability-contract": ["trace", "traceparent", "tracestate", "correlation",
                               "request id", "x-request-id", "baggage", "span", "otel",
                               "opentelemetry", "metric", "slo", "可观测", "链路",
                               "追踪", "关联", "采样"],
    "naming-docs-tooling": ["naming", "camelcase", "snake_case", "kebab", "plural",
                            "lint", "spectral", "buf", "codegen", "sdk", "pact",
                            "contract test", "mock", "description", "example",
                            "changelog", "命名", "文档", "代码生成", "契约测试", "打桩"],
}


def score(text):
    t = text.lower()
    return {k: sum(t.count(w) for w in ws) for k, ws in TOPICS.items()}


def read_spec(path):
    if not path or not os.path.exists(path):
        return ""
    return io.open(path, encoding="utf-8", errors="replace").read()


def emit_tree(out):
    leaves = [{"id": k, "keywords": v, "knowledge": "knowledge/%s.md" % k,
               "checklist": "checklists/%s.md" % k} for k, v in TOPICS.items()]
    doc = {"version": 1, "skill": "interface-design-expert",
           "root": "接口设计专家知识树（九叶·不可再拓扑时停止）", "leaves": leaves}
    io.open(out, "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser(description="classify interface-design-expert topic")
    ap.add_argument("--text", default="")
    ap.add_argument("--spec", help="契约文件（openapi/proto/asyncapi/graphql）")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--emit-tree", dest="tree")
    a = ap.parse_args()
    if a.tree:
        print("[OK] tree ->", emit_tree(a.tree))
        return 0
    txt = a.text + "\n" + read_spec(a.spec)
    sc = sorted(score(txt).items(), key=lambda kv: -kv[1])[: max(1, a.top)]
    primary = sc[0][0] if sc and sc[0][1] > 0 else None
    print(json.dumps({"scores": dict(sc), "primary": primary,
                      "secondary": [k for k, v in sc[1:] if v > 0],
                      "note": None if primary else "分类未命中，需人工定位"},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
