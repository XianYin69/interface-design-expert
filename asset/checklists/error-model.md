# 清单 · 叶4 错误模型

- BLOCK 所有 4xx/5xx 使用统一错误信封（RFC 9457：type/title/status/detail/instance）
- BLOCK `type` 为稳定机器可判定标识（URI/urn），程序不解析 `title`
- BLOCK 状态码表类别、业务码表细分，两者都在契约中声明
- BLOCK 校验失败返回全部失败字段（`errors[]` 含 field/code/message）
- BLOCK 每个错误类别可推出「可重试 / 不可重试」
- BLOCK 429/503 带 `Retry-After`；5xx 仅幂等操作允许自动重试
- BLOCK 无「200 承载业务失败」的分支
- BLOCK gRPC 侧使用标准 status 枚举，业务细节进 `Status.details` 而非全塞 UNKNOWN
- BLOCK 错误体不含堆栈、SQL、内部主机名、他人数据；对外只回 request/trace id
- BLOCK 契约中每个操作声明了其可能的错误响应 schema
- BLOCK 异步失败有失败通道（dead-letter / error 事件）且带 correlation_id
- advisory 错误码有集中登记表并纳入 lint 门禁
- advisory 文档给出常见错误的处置建议而不止字面含义

## 相关

判据 [error-model](../knowledge/error-model.md) · 取证 `scripts/error_model_probe.py`
