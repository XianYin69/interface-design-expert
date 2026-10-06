# dependence（依赖声明）

本技能包依赖的技能包/软件/仓库地址：每行一条 `名称 | 类型 | 来源`，类型为 skill|software|repo。
机读清单 [`deps.json`](deps.json)（每条附 `source_url` 原始链接，`python lint-deps.py` 校验）。

```
python | software | system（>=3.11，脚本只用标准库）
git | software | system（收尾节点提交用）
OpenAPI Specification | repo | https://github.com/OAI/OpenAPI-Specification
AsyncAPI Specification | repo | https://github.com/asyncapi/spec
protocolbuffers/protobuf | repo | https://github.com/protocolbuffers/protobuf
grpc/grpc | repo | https://github.com/grpc/grpc
spectral-stoplight/spectral | software | https://github.com/stoplightio/spectral（可选）
oasdiff | software | https://github.com/oasdiff/oasdiff（可选）
bufbuild/buf | software | https://github.com/bufbuild/buf（可选）
jsonschema (python) | software | https://github.com/python-jsonschema/jsonschema（可选）
Pact | software | https://github.com/pact-foundation/pact-ruby（可选）
Microsoft REST API Guidelines | repo | https://github.com/microsoft/api-guidelines
Google AIP | repo | https://github.com/aip-dev/google.aip.dev
Zalando RESTful API guidelines | repo | https://github.com/zalando/restful-api-guidelines
RFC 9457 Problem Details | repo | https://www.rfc-editor.org/rfc/rfc9457
RFC 9110 HTTP Semantics | repo | https://www.rfc-editor.org/rfc/rfc9110
RFC 6749 OAuth 2.0 | repo | https://www.rfc-editor.org/rfc/rfc6749
JSON Schema | repo | https://github.com/json-schema-org/json-schema-spec
GraphQL Specification | repo | https://github.com/graphql/graphql-spec
W3C Trace Context | repo | https://www.w3.org/TR/trace-context/
semver | repo | https://github.com/semver/semver
file_ops | skill | local://skill_manage_system（联网搜索/抓取）
general-programming | skill | local://general-programming（调用方）
code-guidelines | skill | local://code-guidelines（调用方）
pavedpath-code | skill | local://pavedpath-code（调用方）
skill_manage_system | skill | local://skill_manage_system（调度方）
python-expert | skill | local://python-expert（语言层转派）
cpp-expert | skill | local://cpp-expert（ABI/语言层转派）
concurrency-design | skill | local://concurrency-design（并发架构转派）
database-management | skill | local://database-management（数据层转派）
```
