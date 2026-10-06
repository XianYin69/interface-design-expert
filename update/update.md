# update（自更新接口）

本技能本体内容的**唯一写盘通道**：任何判据、清单、脚本、约束的修改都先落工作区 `tmp/` 镜像，
再经本接口比对释放，禁止就地改写。

## 四步

| 步 | 动作 | 说明 |
|---|---|---|
| report | 登记变更意图 | 记录动机、影响面、涉及的叶与节点 |
| compare | 镜像 vs 本体差异 | 输出差异清单与被引用节点列表 |
| release | 释放回本体 | 通过后落盘并删除 `tmp/` 副本 |
| clean | 清理残留 | 回收缓存、校验悬空链接为 0 |

## 规则

1. `resistance/` 内任何约束条目**不得删除**，只能新增或收紧；放宽须走 [审查约束](../resistance/审查约束/审查约束.md)。
2. 判据变更须同步 `asset/knowledge/` 与 `asset/checklists/`，保持一一对应。
3. 释放后必须跑 `python scripts/check_links.py --root . --strict-url` 与
   `python scripts/knowledge_index.py --all`，两者全绿才算完成。
4. 每次释放记 `CHANGELOG.md`（版本、动机、变更面、验证结果），git 走功能分支→dev→main。
5. 缓存与运行态文件不得写入 skill 目录；链与存档落用户缓存目录。

## 相关

- [修改流程](../branch/流程/修改流程/修改流程.md) · [垃圾回收机制](../resistance/垃圾回收机制/垃圾回收机制.md)
