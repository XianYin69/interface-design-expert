# 清单 · 叶2 契约模式与 Schema

- BLOCK 契约文件是生成源（代码/客户端由它生成），非事后手写文档
- BLOCK 必填（required）与可空（nullable/presence）分别声明，消费方可区分「未给」与「null」
- BLOCK proto 删除字段已 `reserved` 字段号与字段名
- BLOCK 枚举含零值 `UNKNOWN`/`UNSPECIFIED`，且新增枚举值已按破坏性评估
- BLOCK 多形态载荷用 oneof/union，不用「可选字段堆叠 + 注释互斥」
- BLOCK 金额/时间/ID 类型有明确精度与时区语义（无裸 double 金额、无裸 string 时间）
- BLOCK 事件契约声明投递语义、排序保证、重试与死信策略
- BLOCK 每个字段有 description，每个操作有至少一个 example
- BLOCK 服务端实现的校验强度不小于 schema 声明（pattern/format/minimum）
- BLOCK `$ref`/引用可解析，无循环不可展开或匿名深层嵌套导致 codegen 失败
- advisory GraphQL 暴露节点/连接标准形状以便通用客户端复用
- advisory 复杂对象给出错误分支示例而不止 happy path

## 相关

判据 [schema-contracts](../knowledge/schema-contracts.md) · 模板 [templates](../templates/)
