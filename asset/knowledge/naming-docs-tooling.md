# 叶9 · 命名·文档·工具链

权威：Google AIP-122/123/126/127、Spectral 规则集、buf lint、Pact 消费者驱动契约测试、codegen 惯例。

## 判据

1. **风格一致性优先于个人口味**：同一契约内 JSON 字段风格必须统一（`snake_case` 或 `camelCase`），
   混用＝客户端模型映射失败（blocking）；跨契约与语言惯例冲突时以**消费方主流**为准并写明。
2. **命名可推断**：资源用复数名词集合、操作用动词/子资源（AIP-136）、
   布尔用 `is_/has_/can_` 且语义无歧义；`flag`/`data`/`info`/`misc` 类空名＝advisory 缺陷。
3. **同义异名禁令**：同一概念在契约里只能有一个名字（`userId`/`user_id`/`uid` 三者并存＝blocking）。
4. **文档即生成物**：`description`/`summary` 从契约生成，不得靠外部 wiki 补语义；
   外部文档与契约冲突时以契约为准并记缺陷。
5. **lint 门禁进 CI**：Spectral/buf lint 规则必须可执行且失败阻断合并；
   「有规范但无门禁」＝规范随时间失效（advisory→blocking 视团队规模）。
6. **codegen 可用性**：契约必须能被目标语言生成器消费（`$ref` 可解析、无匿名深层嵌套、
   枚举有名字）；生成失败或生成质量差＝blocking（人工客户端必然漂移）。
7. **消费者驱动契约测试**：公开 API 至少有一个消费方契约测试（Pact 类），
   否则「兼容」只是声明；无测试时破坏性判定必须保守（转叶3）。
8. **Mock 可得性**：契约须足以生成可运行 mock（含错误分支与分页分支），
   只有 happy path schema＝前端阻塞（advisory）。
9. **变更公告机制**：changelog + 废弃日历 + 订阅渠道三者齐备；
   只靠 PR 通知＝第三方错过（blocking，公开 API）。
10. **SDK 门面人体工学**：库/SDK 的公开面要小于内部面（窄接口、显式扩展点），
    参数顺序稳定、可选参数用对象而非位置参数堆叠、异常/错误返回按语言惯例（转派语言专家）。

## 取证

`scripts/naming_probe.py`（风格混用、同义异名、空名）、`scripts/codegen_probe.py`（工具与生成可行性）。
