# git 工作流约束

本技能（interface-design-expert）的版本工作流采用严格功能分支策略，保障可追溯、可回滚、可合入。

## 规则

1. **启动前拉取**：开工前 `git fetch`；远端有更新先 `git pull --ff-only`，不得忽略远端直接工作。
2. **功能分支提交**：每个步骤完成后在 `feature/<topic>` 提交；功能分支名不得为 `main` 或 `dev`。
3. **审核通过合 dev**：双链辩论（`logic_chain.py debate`）与 `check_links` 悬空为 0 后，
   本步功能分支合入 `dev`。
4. **整体审核通过合 main**：九项审查标准（见 [审查约束](../审查约束/审查约束.md)）全绿后，
   `dev` 合入 `main`。
5. **禁止直写 main/dev**：所有变更必须经功能分支进入 `dev`，`main`/`dev` 不接受直接 commit。
6. **重试熔断**：任一审查步骤失败且重试达 10 次 → 触发 [惩罚机制](../惩罚机制/惩罚机制.md)，
   回退当前功能分支或求助用户。
7. **忽略清单**：`.gitignore` 必须含 `tmp/` 与 IDE 目录（`.idea/`、`.vscode/`、`.kilo/`）；
   暂存前核对 `git status`，发现临时产物被跟踪先补 ignore。
8. **自动 git init**：操作仓库前检查 `.git/`，未初始化则 `git init`，不得跳过。
9. **推送前确认**：`git push` 前必须询问用户；未确认不得推送（本技能当前远端为空即为此状态）。
10. **仓库可见性**：含侵权/危害/涉密可能的仓库必须 PRIVATE；判定不了时询问用户，不得擅自 PUBLIC。
11. **附属技能双仓模型**：附属/私有子技能同样入库，进 `private/` 独立私有伴生仓（PRIVATE）；
    本体仓 PUBLIC 且 ignore `private/`，禁止不入库或误推公开仓（`E_LEAK_TO_PUBLIC`）。

## 违反后果

跳过功能分支 → main/dev 被污染、无法按步回滚；未确认即推送 → 未审内容外发不可撤回；
违规/涉密仓设 PUBLIC → 侵权与泄密扩散；附属技能误推公开仓 → 私有内容泄漏。

## 相关

- [resistance](../resistance.md) · [收尾节点](../../branch/流程/收尾/收尾.md) · [SKILL.md 红线](../../SKILL.md)
