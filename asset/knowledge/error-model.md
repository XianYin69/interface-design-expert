# 叶4 · 错误模型

权威：RFC 9457（Problem Details for HTTP APIs）、gRPC Status Codes、Google AIP-193、MS REST §800。

## 判据

1. **统一错误信封**：所有 4xx/5xx 走同一结构（RFC 9457：`type`/`title`/`status`/`detail`/`instance`）。
   每个端点各自发明错误体＝blocking（客户端要为每端点写一套解析）。
2. **`type` 是稳定标识**：用 URI（推荐 `urn:` 或文档 URL）作为机器可判定的错误类别；
   `title` 面向人且**不得**被程序解析（RFC 9457 §3.1/3.2）。
3. **错误码分层**：HTTP 状态码＝类别，业务码＝细分（`errors[].code`）。
   只有状态码＝无法自动化处理；只有业务码＝中间件/网关无法判定重试。
4. **字段级错误**：校验失败必须回 `errors[]`（`field`/`code`/`message`），
   并列出**全部**失败字段，不得遇第一个就返回（集成往返成本翻倍）。
5. **重试语义显式化**：每个错误类别必须能推出「可重试 / 不可重试」——
   429/503 带 `Retry-After`，500/504 幂等才可重试，400/403/404 不重试。
   无法从错误模型推出重试策略＝blocking。
6. **不得用 200 承载失败**：`{"success": false}` 与 HTTP 状态并存＝双事实源（blocking）。
7. **gRPC 侧**：`code` 用标准枚举（`INVALID_ARGUMENT`/`NOT_FOUND`/`FAILED_PRECONDITION`…），
   细节进 `google.rpc.Status.details`；不得把业务错误全塞 `UNKNOWN`（丢失可判定性）。
8. **信息泄露边界**：`detail`/`instance` 不得含堆栈、SQL、内部主机名、用户其他数据；
   对外回 trace/request id，内部凭 id 查日志（转叶8 可观测性）。
9. **异步/事件侧**：错误不能只落日志——须有失败通道（dead-letter / error event 类型）
   且 payload 与成功事件同 schema 家族，含 `correlation_id`。
10. **错误即契约**：错误响应必须在契约里声明（OpenAPI 每个操作列 4xx/5xx 的 schema 引用），
    未声明＝消费方无法生成正确客户端（blocking）。

## 取证

`scripts/error_model_probe.py`（状态码族完备性、problem+json 结构、错误码枚举、重试可推性）。
