# 清单 · 叶5 分页·过滤·排序

- BLOCK 每个返回列表的端点都有分页参数（无分页＝blocking）
- BLOCK `limit` 有服务端默认值与硬上限
- BLOCK 排序有确定的次级排序键（通常 id），默认排序已文档化
- BLOCK 高频写入/深翻页/不漏不重场景使用 cursor 而非 offset
- BLOCK cursor token 不透明且防篡改（客户端不得解析），排序键变更时明确失效
- BLOCK 分页越界返回明确错误（400/404 + 错误信封），不以空列表掩盖
- BLOCK 总数语义写明（精确 / 估算 / 上限截断），大集合不承诺精确 total
- BLOCK 过滤字段有白名单；查询 DSL 有深度与复杂度限制
- advisory 大对象端点支持字段裁剪（`fields=` / 选择集）
- advisory 分页响应含下一页链接或 token 的标准位置（`links` / `pageInfo`）

## 相关

判据 [pagination-filtering-sorting](../knowledge/pagination-filtering-sorting.md) · 取证 `scripts/contract_lint.py`
