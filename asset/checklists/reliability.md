# 清单 · 叶7 可靠性语义

- BLOCK 每个操作声明服务端超时与客户端建议超时
- BLOCK 自动重试需同时满足「可重试错误 + 幂等 + 有退避」，否则禁止盲目重试并写明
- BLOCK 退避策略为指数 + 抖动 + 次数上限（无固定间隔重试）
- BLOCK 非幂等写操作支持幂等键，且服务端保存窗口已声明
- BLOCK 消息/事件声明投递语义（at-most-once / at-least-once / 效果等价 exactly-once）
- BLOCK 无序场景给出消费方排序依据（事件时间 / 版本号 / 去重键）
- BLOCK 顺序保证范围写明（同 partition key / message group 内有序）
- BLOCK 跨服务依赖声明失败降级形态，禁止静默返回空数据
- BLOCK 秒级以上长操作走 202 + 操作资源或回调，不挂长连接
- BLOCK 429/RESOURCE_EXHAUSTED 给出恢复时间并与退避预算一致
- advisory 取消/断连是否传播到服务端并中止工作
- advisory 熔断阈值与半开恢复条件已文档化

## 相关

判据 [reliability](../knowledge/reliability.md) · 取证 `scripts/error_model_probe.py`
