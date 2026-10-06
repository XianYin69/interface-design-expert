# 叶6 · 安全·认证·授权

权威：RFC 6749（OAuth 2.0）、RFC 9068（JWT 作为 access token）、OWASP API Security Top 10、mTLS 惯例。

## 判据

1. **认证机制在契约里声明**：OpenAPI `securitySchemes` / proto 元数据约定必须存在；
   「靠网关默认」＝契约不完整（blocking，第三方无法自助集成）。
2. **API Key 的边界**：只适用于低风险、可快速吊销、单一租户场景；
   key 不得进 URL 查询（日志/Referer/浏览器历史泄露），必须走请求头（OWASP API2/API5）。
3. **OAuth2 流程选型**：浏览器内 SPA/PKA + 公共客户端不得持有 client_secret（隐式流已废弃）；
   服务间用 client_credentials 或 mTLS；授权码 + PKCE 是默认答案。
4. **JWT 语义**：access token 必须短寿命 + 可校验（`exp`/`aud`/`iss`/`kid`）；
   不得把 refresh token 当 access 用；`alg: none` 与算法混淆＝blocking 漏洞。
   撤销需求高的场景不得用纯无状态 JWT（须给 jti 黑名单或改 opaque token）。
5. **scope 与授权粒度**：每个操作必须映射到所需 scope/权限点；
   一个 `read` 覆盖全部资源＝越权风险（OWASP API1 Broken Object Level Authorization，blocking）。
6. **对象级授权**：`GET /orders/{id}` 必须校验 id 归属，不得只校验登录态（BOLA 是公开 API 头号漏洞）。
7. **限流与配额分离**：限流（保护服务）与配额（商业/公平使用）是两个契约；
   429 必须带 `Retry-After` 与限额说明头（`X-RateLimit-*` 或标准头），
   无 `Retry-After`＝客户端只能瞎重试（blocking）。
8. **传输层**：对外端点只允许 TLS；HTTP 明文回 301/拒绝。mTLS 用于服务间且需给证书轮换窗口说明。
9. **凭据不进契约**：示例、模板、错误信息里不得出现真实 token/密钥/租户 ID（advisory→blocking 视暴露面）。
10. **输入即攻击面**：所有字段有长度/枚举/格式约束（转叶2 JSON Schema），
    自由文本进日志/SQL/模板必须有转义约定。

## 取证

`scripts/contract_lint.py`（缺 securitySchemes、scope 未映射、429 无 Retry-After）、
`scripts/codegen_probe.py`（工具在位与规则集检查）。
