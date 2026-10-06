# 清单 · 叶3 版本与兼容性

- BLOCK 已列出既有客户端清单与数量（零客户端可标 n-a 并说明）
- BLOCK 破坏性判定有证据：`compat_probe`/`oasdiff`/`buf breaking` 输出或规范小节
- BLOCK 类型变更、必填新增、字段删除、语义变更、默认值变更、校验收紧均已分级
- BLOCK 新增枚举值已按「旧客户端读侧破坏」评估
- BLOCK 客户端严格反序列化（未知字段报错）已确认或已排除
- BLOCK 版本机制唯一且退役策略写明（并存窗口 + 退出条件）
- BLOCK proto 字段号无复用；wire 兼容与 JSON 兼容分别给结论
- BLOCK ABI 变更给出符号/布局证据与 `SOVERSION`，重编译要求写明
- BLOCK 每个废弃项含 `deprecated` 标记 + 替代方案 + sunset 日期/版本
- BLOCK 每个破坏性变更给出旧客户端失败形态与检测手段（日志/指标/契约测试）
- advisory 0.x 版本是否被当作稳定契约使用已声明
- advisory 双版本维护成本与退出条件有量化依据（流量占比/客户端清单）

## 相关

判据 [versioning-compatibility](../knowledge/versioning-compatibility.md) · 取证 `scripts/compat_probe.py`
