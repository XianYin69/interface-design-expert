# 清单 · 叶9 命名·文档·工具链

- BLOCK 同一契约内字段命名风格统一（全 `snake_case` 或全 `camelCase`），无混用
- BLOCK 同一概念只有一个名字（无 `userId`/`user_id`/`uid` 并存）
- BLOCK 契约可被目标语言 codegen 消费（引用可解析、枚举有名字、无匿名深层嵌套）
- BLOCK lint 规则（Spectral/buf）可在 CI 执行且失败阻断合并
- BLOCK 公开 API 至少有一个消费者驱动契约测试（Pact 类），否则破坏性判定按保守取
- BLOCK 文档语义来自契约（description/summary），外部文档与契约冲突以契约为准并记缺陷
- BLOCK 变更公告机制齐备：changelog + 废弃日历 + 订阅渠道
- advisory 资源用复数名词、操作用子资源/动词形式（AIP-136 风格）
- advisory 布尔命名 `is_/has_/can_` 且无歧义；无 `data`/`info`/`misc`/`flag` 空名
- advisory 契约足以生成含错误分支与分页分支的 mock
- advisory SDK/库公开面小于内部面，可选参数用对象而非位置参数堆叠

## 相关

判据 [naming-docs-tooling](../knowledge/naming-docs-tooling.md) · 取证 `scripts/naming_probe.py`、`scripts/codegen_probe.py`
