# interface-design-expert

软件接口 / API 契约设计的资深专家顾问技能：为 SMS 主流程与编码技能在**设计、评审、演进**
REST、gRPC、GraphQL、事件驱动 API、库/SDK 门面、ABI 与 IPC 边界时提供**可执行**的专家判断、
评审清单与契约建议。

## 覆盖领域（九叶知识树）

HTTP/REST 语义 · 契约模式（OpenAPI/AsyncAPI/proto/JSON Schema）· 版本与兼容 ·
错误模型 · 分页/过滤/排序 · 安全与鉴权 · 可靠性语义 · 可观测性契约 ·
命名·文档·工具链

## 快速使用

```
python scripts/classify_topic.py --text "这个 v2 接口把 status 改成枚举算破坏性吗" --spec api/openapi.yaml
python scripts/knowledge_index.py --topic versioning-compatibility
python scripts/review_checklist.py --topic error-model --format json
python scripts/contract_lint.py api/openapi.yaml
python scripts/compat_probe.py --old api/v1.yaml --new api/v2.yaml
python scripts/advice_compose.py --topic reliability --verdict tmp/verdict.json
```

## 目录

| 目录 | 内容 |
|---|---|
| SKILL.md | 入口（YAML frontmatter + 一句话提示词） |
| agent/ | 四格式提示词（CLAUDE.md / agent_prompt.md / .cursorrules / instructions.md） |
| branch/流程/ | 十步主流程 + 修改流程 + 横切浏览器学习 |
| asset/knowledge/ | 九份领域判据 |
| asset/checklists/ | 九份评审清单（BLOCK 标记阻塞项） |
| asset/templates/ | openapi / asyncapi / proto / problem-details 脚手架 |
| references/知识树/ | 领域拓扑与出处 |
| references/参考书目/ | 规范与指南联网确证（[联网]/[本地]） |
| branch/流程/浏览器学习/ | 横切节点：先检索学习后作答 |
| resistance/ | 约束与五大机制兜底 |
| scripts/ | 只读体检与产出脚本（标准库实现） |
| dependence/ | 依赖声明（含 deps.json 原始链接） |
| planned_tasks/ | 计划任务声明（由 SMS 调度器执行） |

## 边界

只读评审为默认；不修改调用方契约文件，不改动其他技能目录；结论必带依据、取舍与失效边界。
运行时性能调优、数据库 schema、前端交互设计转派对应专家技能。

## 许可

MIT（见 LICENSE）。
