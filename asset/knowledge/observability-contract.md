# 叶8 · 可观测性契约

权威：W3C Trace Context（`traceparent`/`tracestate`）、W3C Baggage、OpenTelemetry 语义约定。

## 判据

1. **追踪上下文是接口字段**：跨进程调用必须传播 `traceparent`（W3C 格式），
   自定义 `X-Trace-Id` 与标准头并存＝采样与链路断裂（blocking，公开 API 尤甚）。
2. **请求关联 ID**：每个请求有 `request id`（入站无则生成、出站回显），
   并出现在错误响应 `instance`/`details` 里——用户报障能定位到日志（转叶4）。
3. **ID 不回内部信息**：`request id` 不得是可猜测的自增主键或含租户明文（信息泄露，advisory→blocking）。
4. **Baggage 白名单**：跨服务传递的业务标签必须显式白名单；
   任意键值透传＝带宽放大与敏感信息扩散（blocking）。
5. **日志不进契约**：契约里只声明**头与字段**，不声明日志格式；
   但必须声明「哪些字段不得进日志」（密钥、PII）——缺失即安全缺陷（转叶6）。
6. **指标可推导**：操作命名与状态码设计要能直接产出 QPS/错误率/延迟分位；
   业务失败塞 200 会让错误率指标失真（blocking，与叶4 同源）。
7. **SLO 语义进文档**：公开端点应声明可用性/延迟目标与限流阈值；
   无声明时客户端只能按最坏情况设计退避（advisory）。
8. **异步链路可追**：事件消息必须携带 `correlation_id`/`causation_id` 或 trace 上下文，
   否则跨服务排障不可行（blocking，事件驱动场景）。
9. **采样决策上游定**：契约应说明是否透传 `tracestate` 的采样位，
   服务端不得随意改写采样决策导致链路断尾（advisory）。
10. **时钟与耗时**：跨服务耗时统计依赖单调时钟；契约里的时间戳一律 UTC + RFC 3339（转叶2）。

## 取证

`scripts/naming_probe.py`（头命名风格与标准头一致性）、`scripts/contract_lint.py`（缺 request id 回显声明）。
