# scripts（脚本库）

interface-design-expert 的只读体检与产出脚本。全部**英文文件名**、只用 Python 标准库，
可被调用方直接 `python scripts/<name>.py` 执行。

## 清单

| 脚本 | 作用 | 典型调用 |
|---|---|---|
| classify_topic.py | 诉求/契约 → 九叶标签打分 | `--text "..." --spec api.yaml [--emit-tree out.json]` |
| knowledge_index.py | 取叶判据与清单路径 | `--topic error-model [--all --format json]` |
| review_checklist.py | 解析清单为判定表 | `--topic error-model [--format json]` |
| contract_lint.py | 契约结构缺陷体检 | `api/openapi.yaml [--format json]` |
| compat_probe.py | 新旧契约兼容性分级 | `--old v1.yaml --new v2.yaml` |
| naming_probe.py | 命名一致性与同义异名 | `api/openapi.yaml` |
| error_model_probe.py | 错误模型完备性 | `api/openapi.yaml` |
| codegen_probe.py | 工具在位与可生成性 | `--spec api.yaml [--proto dir]` |
| advice_compose.py | 证据 + 结论 → 交付报告 | `--topic error-model --verdict tmp/verdict.json` |
| check_links.py | 悬空链接与 URL 计数 | `--root . --strict-url` |

## 约定

1. 输出统一 JSON（`--format text` 可选），字段含 `findings[]`、`evidence`、`tool`、`rc`。
2. 只读：脚本不得修改被评审文件；写盘只允许写 `tmp/`（工作区）。
3. 解析失败必须显式报 `parse-skipped`，不得当作「通过」。
4. 禁裸 `except`、禁 `print` 调试残留、禁 >100 字符长行、禁超长函数（脚本不限总行数）。
5. 外部工具（spectral/buf/oasdiff/protoc）在位时优先采信其输出，内置结果标 `fallback`。

## 机制脚本

垃圾回收、上下文压缩、逻辑链、过程链、惩罚、自更新等机制脚本由 `Skill_Generator` 与 SMS 提供
（见 [dependence](../dependence/dependence.md) 薄技能声明），本技能不重复实现。
