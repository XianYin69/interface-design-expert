---
name: interface-design-expert
version: 0.1.0
description: >
  接口设计专家顾问：REST/HTTP 语义、gRPC/Protocol Buffers、GraphQL、事件驱动 API（AsyncAPI/WebSocket/消息总线）、
  库与 SDK API 设计（人体工学与类/函数面）、ABI 与二进制兼容、IPC 边界的可执行判据、契约评审清单与兼容性建议。
  薄技能（能力经 dependence/ 声明），供 SMS 及编码技能在设计与评审接口契约时调用。
license: MIT
metadata:
  category: development
---

# interface-design-expert

使用 `interface-design-expert` skill 来完成用户请求。

## 工作原则

1. **先取证后判断**：结论只来自规范条文（OpenAPI/AsyncAPI/proto/RFC）、`scripts/` 实测或用户原文；未运行的不得写「已验证」。
2. **判据非偏好**：阻塞项只能来自规范/权威指南/可复现取证；命名口味与风格偏好只作建议。
3. **按流程执行**：不跳步，中断记过程链后 resume，每条判断落逻辑链（证据→结论→取舍→边界）。
4. **只读默认**：改动调用方契约文件需显式授权，且先 `--dry-run` 预览；契约变更必须给兼容性影响面。

## 执行路径

初始化 → 问题解析 → 领域定位 → 知识检索 → 取证探查 → 专家判断 → 评审清单 → 契约建议 → 输出交付 → 收尾 → 完成

横切节点 [浏览器学习](branch/流程/浏览器学习/浏览器学习.md)：任一步遇到不明确的规范条款/字段语义/工具行为，强制先派 `file_ops` 检索学习并给出出处再作答。

## 可用工具（scripts/）

classify_topic · knowledge_index · review_checklist · contract_lint · compat_probe · naming_probe · error_model_probe · codegen_probe · advice_compose · check_links

## 知识树（九叶·不可再拓扑）

http-rest-semantics · schema-contracts · versioning-compatibility · error-model · pagination-filtering-sorting · security-authn-authz · reliability · observability-contract · naming-docs-tooling
索引 [asset/knowledge_tree.json](asset/knowledge_tree.json) · 细则 [references/知识树/](references/知识树/知识树.md) · 书目 [references/参考书目/](references/参考书目/参考书目.md)

## 红线

- 不得跳过初始化与取证直接给结论；不得伪造运行结果、版本号或兼容性判定。
- 不得修改调用方契约文件或其他技能目录；不得把命名口味标为阻塞项。
- 未确证的规范条款不得标 [联网]，严禁臆造 URL；字段语义须引规范小节出处。
- 悬空链接必须为 0；所有 .md ≤ 50 行（50 行红线只约束 markdown 文本；脚本 .py/.ps1/.sh/.cmd 不限行数，但仍禁裸 except、print 调试残留、>100 字符长行、超长函数）；缓存文件不得写入 skill 目录。
- 交付必须含「边界」与「未覆盖」两段，缺项即判不合格。
- Git 工作流：每步功能分支提交→审核通过合 `dev`→整体审查通过 `dev` 合 `main`（推送前须用户确认）。

## 详细流程

- 流程节点：[branch/流程/](branch/流程/流程.md)；约束兜底：[resistance/](resistance/resistance.md)
