# CHANGELOG

## 0.1.0

首次生成（Skill_Generator 创建路径 · 调度方 conv-20261007-010653-2741006）。

### 新增

- SKILL.md：YAML frontmatter + 一句话提示词 + 工作原则/执行路径/工具/知识树/红线（≤50 行）。
- agent/：四格式提示词（CLAUDE.md、agent_prompt.md、.cursorrules、instructions.md）。
- branch/流程/：十一节点（初始化→问题解析→领域定位→知识检索→取证探查→专家判断→
  评审清单→契约建议→输出交付→收尾）+ 修改流程 + 横切节点浏览器学习。
- asset/knowledge/：九叶领域判据（http-rest-semantics、schema-contracts、
  versioning-compatibility、error-model、pagination-filtering-sorting、
  security-authn-authz、reliability、observability-contract、naming-docs-tooling）。
- asset/checklists/：九份评审清单，`BLOCK` 前缀＝阻塞项，由 review_checklist.py 解析。
- asset/templates/：openapi.yaml、openapi-components.yaml、asyncapi.yaml、
  service.proto、problem-details.json 契约脚手架（无真实主机与凭据）。
- asset/knowledge_tree.json：九叶机读索引（classify_topic.py --emit-tree 同构）。
- scripts/：10 个标准库脚本（classify_topic、knowledge_index、review_checklist、
  contract_lint、compat_probe、naming_probe、error_model_probe、codegen_probe、
  advice_compose、check_links）。
- resistance/：评审约束、审查约束、输出约束、约束部分、浏览器学习约束、
  git工作流约束 + 五大机制 + 沙盒机制。
- references/：知识树（拓扑与不可再拓扑判定）、参考书目（19 项 [联网] 确证）。
- dependence/：dependence.md + deps.json（每条附 source_url 原始链接，lint-deps 通过）。
- planned_tasks/：README.md + template.json +
  pt-interface-design-expert-upstream-watch.json（到期由 SMS 调度器执行）。
- LICENSE：MIT。

### 约束

- 只新建 interface-design-expert，未修改 general-programming 或任何既有技能目录。
- 抓取缓存与探针中间产物落工作区 tmp/，不随包交付。
- git 走功能分支→dev→main 本地提交；远端为空，未推送（推送前须用户确认）。
