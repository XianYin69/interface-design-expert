# 叶5 · 分页·过滤·排序

权威：Google AIP-132/158、Microsoft REST API Guidelines §11、OpenAPI cursor/links 惯例、GraphQL Relay 连接。

## 判据

1. **集合端点必须分页**：任何返回列表的端点无分页参数＝blocking（数据增长后必然不可用）。
2. **offset 的适用边界**：offset/limit 只在「结果集稳定 + 需要跳页 + 数据量有界」时可接受；
   高频写入集合、深翻页、需要不漏不重时必须 cursor（AIP-158 page_token）。
   判据：并发插入是否会让同一条记录出现在两页或消失。
3. **cursor 设计**：token 不透明（客户端不得解析）、服务端签名或加密以防篡改、
   排序键变更即 token 失效并回明确错误（不是静默错序）。
4. **上限与默认**：`limit` 必须有服务端最大值（默认值 + 硬上限），
   无上限的 `limit=100000`＝自我 DoS（blocking）。
5. **总数语义**：`total_count` 是昂贵承诺——大集合应给 `total_size_estimated` 或不给，
   并在契约里写明语义（精确/估算/受上限截断）。
6. **排序显式且稳定**：`order_by` 必须有确定的次级排序键（通常是 id），
   否则同值记录跨页漂移；默认排序必须文档化（无默认排序＝分页结果不可复现，blocking）。
7. **过滤表达**：简单场景用重复参数（`status=a&status=b`）；复杂布尔/嵌套才上查询 DSL，
   且 DSL 必须有白名单字段与深度限制（否则注入与性能风险，blocking）。
8. **字段裁剪**：`fields=`/GraphQL 选择集/`?select=` 允许客户端取子集，
   大对象端点无裁剪＝带宽与移动端成本（advisory，公开 API 升 blocking）。
9. **分页与错误共存**：分页越界回 400/404 且带 problem details；不得回空列表掩盖错误参数。
10. **Relay 连接（GraphQL）**：`edges/node/cursor/pageInfo{hasNextPage}` 是标准形状，
    自造 `items + page` 使通用客户端无法复用（advisory）。

## 取证

`scripts/contract_lint.py`（列表端点缺分页参数、缺上限、缺默认排序说明）。
