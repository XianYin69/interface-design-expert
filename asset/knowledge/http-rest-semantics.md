# 叶1 · HTTP 与 REST 语义

权威：RFC 9110（HTTP Semantics）、RFC 9111（缓存）、Microsoft REST API Guidelines、Google AIP-131/133。

## 判据

1. **方法语义**：GET 只读且安全（不得有副作用）；PUT 幂等且整体替换；PATCH 幂等性不由方法保证，
   须服务端自行实现（RFC 9110 §9.3.5）；POST 非幂等。判据：客户端重试同一请求是否产生第二份副作用。
2. **状态码族**：2xx 成功语义必须与响应体一致——返回 200 却带错误对象即 blocking；
   4xx 客户端可自纠、5xx 服务端故障，不得混用（AIP-131/133 与 MS §800）。
3. **201 + Location**：创建成功必须回 201 并带 `Location`；异步创建回 202 且给状态查询资源。
4. **204 无体**：删除成功且无返回数据用 204，不得回 200 + `{}`（消费方解析分支翻倍）。
5. **资源建模**：路径是名词复数集合 + 标识符（`/orders/{id}`），动词进查询或子资源
   （`POST /orders/{id}:cancel`，AIP-136）；不得出现 `/getOrders`、`/doPay`。
6. **条件请求**：可变资源须给 `ETag`；并发更新用 `If-Match`（乐观锁），
   缺失即为「最后写入覆盖」缺陷（blocking，若业务有并发更新）。
7. **缓存契约**：`Cache-Control` 是接口契约的一部分——公开只读端点须显式声明
   `public/private` + `max-age` 或 `no-store`；不得依赖默认值。
8. **内容协商**：`Accept`/`Content-Type` 必须显式；版本化媒体类型（`application/vnd.x.v2+json`）
   与 URL 版本二选一，不得同时两套版本机制。
9. **幂等键**：非幂等写操作（POST 支付/扣款）必须支持 `Idempotency-Key` 类请求头（转叶7 可靠性）。
10. **HEAD/OPTIONS**：公开 API 的 OPTIONS 应回 CORS 与方法列表；不需要则不实现，不得回 501 混淆。

## 反模式（一律 blocking 或 advisory 标注）

- GET 带写副作用（用 GET 触发任务/扣款）。
- 用 200 承载业务失败；用 500 承载校验失败（应 400）。
- 路径含实现细节（`/api/v1/mysql/users`）。
- 布尔字段用 `is_deleted=1/0` 与 `true/false` 混用（同族接口风格不一致）。

## 取证

`scripts/contract_lint.py`（缺 error 响应、200 承载错误、无 Location）、
`scripts/naming_probe.py`（动词路径、单复数、风格混用）。
