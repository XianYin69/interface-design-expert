# 清单 · 叶8 可观测性契约

- BLOCK 跨进程调用传播 W3C `traceparent`，不自造并存的多套追踪头
- BLOCK 每个请求有 request/correlation id，入站无则生成、出站回显
- BLOCK 错误响应携带可定位的 request/trace id（与叶4 的 `instance` 对齐）
- BLOCK 事件消息携带 correlation/causation 标识或追踪上下文
- BLOCK 跨服务透传的业务标签有显式白名单（Baggage 不做任意键值透传）
- BLOCK 契约声明「不得进日志」的字段（凭据、PII）
- BLOCK 时间戳一律 UTC + RFC 3339，无本地时区裸字符串
- advisory 公开端点声明可用性/延迟目标与限流阈值（SLO 语义）
- advisory 采样决策由上游决定，服务端不改写采样位导致链路断尾
- advisory request id 不可猜测、不含租户明文

## 相关

判据 [observability-contract](../knowledge/observability-contract.md) · 取证 `scripts/naming_probe.py`
