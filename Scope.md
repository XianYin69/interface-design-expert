# Scope — interface-design-expert

## 本技能负责

- **接口契约设计评审**：REST/HTTP、gRPC/Protocol Buffers、GraphQL、AsyncAPI/事件驱动 API 的语义与结构。
- **版本兼容性分析**：字段增删改的破坏性判定（semver、buf breaking、oasdiff）。
- **错误模型规范**：RFC 9457 Problem Details、gRPC status code、AIP-193 错误响应。
- **集合语义契约**：分页（AIP-132/158）、过滤、排序策略。
- **安全与鉴权边界**：OAuth 2.0、scope、JWT、速率限制。
- **可靠性语义**：重试策略、幂等键、最终一致性。
- **可观测性契约**：W3C Trace Context、Baggage、OTel 传播头。
- **命名与文档规范**：AIP-122/123、Spectral lint、protobuf 命名。

## 本技能不负责

- 运行时性能调优（CPU/内存/网络延迟优化）——转 `general-programming` 或语言专家技能。
- 数据库 schema 设计、SQL 查询优化——转 `database-management`。
- 前端交互实现、UI/UX 设计——转 `frontend-dev`、`ui-design`、`web-design-expert`。
- 业务逻辑设计、领域建模——转 `general-software-dev`。
- 特定语言运行时内部细节（如 JVM 垃圾回收、Go goroutine 调度器）——需派 file_ops 联网学习后引用结论。

## 依赖能力

| 依赖 | 用途 |
|---|---|
| file_ops | 不明规范条款/工具行为联网学习（须 `:grant network`） |
| general-programming | 性能调优转派 |
| database-management | 数据库 schema 转派 |
| frontend-dev | 前端实现转派 |
| python | 脚本运行时（标准库实现） |
| git | 分支工作流 |
