# 前向验证任务集（P4）

用 6 个真实任务验证整套工序"跑起来结果对不对"——不是验证工件结构（那是 `scripts/validate_*.py` 的职责），而是验证**决策质量**：该建的层建了、不该上的复杂度没上。

## 无答案泄漏原则

每个任务文件分两段：

- **任务输入**：执行时**只把这一段**交给对应 workflow/命令。不得把判据一并给执行方。
- **判据**：评审人持有。执行完成后对照 run 工件逐条核对"应出现/不应出现"。

## 执行方法

1. 按任务文件标注的入口启动（如 `/backend-best-practices:workflow-greenfield <任务输入>`）。
2. 执行完成后，评审人打开 run 工作区，按判据表逐条核对，记录每条 pass/fail 与证据（工件路径）。
3. 任一"不应出现"命中即该任务 fail——过度设计与漏设计同罪。
4. 可配合 `python scripts/validate_traceability.py <workdir>` 检查追踪链闭合。

## 任务清单

| # | 任务 | 入口 | 核心考点 |
| :-- | :-- | :-- | :-- |
| 01 | 简单 CRUD（书签管理）| workflow-greenfield | 有 Application + 查询契约，但拒绝 CQRS/Saga/GoF |
| 02 | 复杂订单 | workflow-greenfield | Aggregate、编排、Outbox、业务视图、权限齐备 |
| 03 | 跨上下文 Dashboard | workflow-read-model-greenfield | 选 Read Model、字段来源、新鲜度、重建、权限 |
| 04 | Brownfield 查询迁移 | workflow-read-model-brownfield | 特征化/Parity Diff、Backfill、切换与回滚 |
| 05 | 多支付供应商 | design-pattern | 识别 Adapter/Strategy 真实变化轴 |
| 06 | 单支付供应商 | design-pattern | 拒绝为"未来可能"预建模式 |
