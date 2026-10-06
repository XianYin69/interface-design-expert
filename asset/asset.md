# asset（技能包资产）

本目录存放随包交付的结构化资产：机读索引、判据正文、评审清单、契约脚手架。

## 内容

- [knowledge_tree.json](knowledge_tree.json)：九叶机读索引（id/title/authority/keywords/路径），
  由 `scripts/classify_topic.py --emit-tree` 生成、`scripts/knowledge_index.py` 检索。
- [knowledge/](knowledge/)：九份领域判据（每份 ≤50 行，每条带权威出处键）。
- [checklists/](checklists/)：九份评审清单，`BLOCK` 前缀＝阻塞项，由 `scripts/review_checklist.py` 解析。
- [templates/](templates/)：契约脚手架（openapi / asyncapi / proto / problem-details）。

## 规则

1. 知识条目与清单一一对应，叶 id 相同；新增叶须同时补三处（json、knowledge、checklists）。
2. 模板只给**形状**，不给具体业务字段；模板内不得出现真实密钥、真实主机名。
3. 本目录不放缓存、不放抓取中间产物、不放运行日志（一律工作区 `tmp/`）。

## 相关

- [知识树](../references/知识树/知识树.md) · [scripts](../scripts/scripts.md)
