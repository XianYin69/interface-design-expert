# 清单 · 叶6 安全·认证·授权

- BLOCK 契约声明了认证机制（`securitySchemes` 或等价约定），第三方可自助集成
- BLOCK API Key 只经请求头传递，不出现在 URL 查询串
- BLOCK 公共客户端（SPA/移动端）不使用隐式流、不持有 client_secret（授权码 + PKCE）
- BLOCK access token 校验 `exp`/`iss`/`aud`/`kid`；拒绝 `alg: none` 与算法混淆
- BLOCK 每个操作映射到所需 scope/权限点，不存在一个 `read` 覆盖全部资源
- BLOCK 按 id 访问的资源校验对象归属（防 BOLA），不只校验登录态
- BLOCK 429 带 `Retry-After` 与限额头；限流与配额语义分离并写明
- BLOCK 对外端点仅接受 TLS；明文请求重定向或拒绝
- BLOCK 示例/模板/错误信息中无真实凭据、租户 ID、密钥
- BLOCK 所有输入字段有长度/枚举/格式约束（与叶2 schema 一致）
- advisory 高撤销需求场景是否改用 opaque token 或提供 jti 黑名单
- advisory mTLS 场景给出证书轮换窗口与双证书并存期

## 相关

判据 [security-authn-authz](../knowledge/security-authn-authz.md) · 取证 `scripts/contract_lint.py`
