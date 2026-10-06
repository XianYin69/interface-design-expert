# 清单 · 叶1 HTTP 与 REST 语义

`BLOCK`＝阻塞项（未 pass 不得发布）；其余为 advisory。每条三态：pass / fail / n-a（须写理由）。

- BLOCK 集合资源用复数名词路径，无动词式路径（`/getOrders`）
- BLOCK 每个操作声明了 4xx/5xx 响应及其 schema 引用
- BLOCK 业务失败不使用 200 承载（无 `{"success":false}` 型双事实源）
- BLOCK GET/HEAD 无副作用；写操作不放在 GET
- BLOCK PUT 幂等、PATCH 的幂等性由服务端明确说明
- BLOCK 创建成功回 201 + `Location`；异步创建回 202 + 状态资源
- BLOCK 删除无返回数据用 204，不用 200 + 空对象
- BLOCK 有并发更新的资源提供 `ETag` + `If-Match`（乐观锁）
- BLOCK 公开只读端点显式声明 `Cache-Control`（不依赖默认值）
- BLOCK 版本机制唯一（URL / 头 / 媒体类型三选一，不多机制并存）
- advisory 布尔字段命名与取值风格全族一致
- advisory 路径不含实现细节（存储、框架、内部服务名）
- advisory 非幂等写操作支持幂等键请求头（详见叶7）

## 相关

判据 [http-rest-semantics](../knowledge/http-rest-semantics.md) · 解析 `scripts/review_checklist.py`
