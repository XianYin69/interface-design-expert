# 叶2 · 契约模式与 Schema

权威：OpenAPI 3.1、AsyncAPI 3、proto3、JSON Schema 2020-12、GraphQL Specification。

## 判据

1. **单一事实源**：契约文件必须是生成源而非事后文档；手写文档与代码并存即 blocking
   （漂移不可避免）。codegen 可行性由 `codegen_probe.py` 判定。
2. **必填与可空分离**：`required` 与 nullable 是两件事（OpenAPI 3.1 用 `type: [X, "null"]`）。
   判据：消费方能否区分「没给」与「给了 null」——proto3 需 `optional` 才有显式 presence。
3. **proto 字段号纪律**：字段号＝兼容性地基，删除字段必须 `reserved` 号与名（proto 规范）；
   复用旧号＝静默解码错值，blocking 且不可回滚。
4. **枚举演进**：枚举必须含 `UNKNOWN`/`UNSPECIFIED` 零值（proto3 默认零值），
   否则新客户端读到旧数据无法区分「未设置」；新增枚举值＝对旧客户端是破坏（AIP-126）。
5. **oneof 与联合类型**：多形态载荷用 `oneof`/`oneOf`/GraphQL union，不得用「可选字段堆叠 + 文档说明互斥」。
6. **类型精度**：金额/时间戳/ID 不得用裸 `string`/`double`——金额用最小货币单位整数或 decimal 字符串，
   时间用 RFC 3339 或 proto `Timestamp`，ID 用带前缀字符串（避免跨系统 64 位溢出与 JS 精度丢失）。
7. **AsyncAPI 语义**：事件契约必须声明投递语义（at-least-once / exactly-once）、
   排序保证、重试与死信策略；只写 topic 名与 payload＝契约不完整（blocking）。
8. **GraphQL 契约**：暴露 `__typename`/节点接口以支持缓存与分页；错误走 `errors` 数组且
   与业务扩展码分离；不得把 REST 的 200/4xx 语义硬套进单 endpoint。
9. **描述与示例**：每个字段有 `description`，每个操作有至少一个 `example`；
   无描述的公开字段＝文档缺陷（advisory），无示例的复杂对象＝集成成本 blocking。
10. **校验语义**：JSON Schema 关键字（`pattern`/`format`/`minimum`）是契约的一部分，
    服务端必须实现同等校验，不得只靠客户端。

## 取证

`scripts/contract_lint.py`（结构完备性）、`scripts/codegen_probe.py`（可生成性与工具在位）。
