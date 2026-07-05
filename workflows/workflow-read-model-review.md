# Workflow：CQRS Read Model Review

> 统筹者。用于审查现有 CQRS Read Model 设计或代码。由 `/backend-best-practices:cqrs-read-model-review` 触发。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | cqrs-review | 设计文档/代码路径 | `01-review.md` | G0 |
| 02 | cqrs-domain-read-decoupling | 原输入,`01-review.md` | `02-domain-read-decoupling.md` | 条件执行 |
| 03 | cqrs-aggregation-view-design | 原输入,`01-review.md` | `03-aggregation-view.md` | 条件执行 |
| 04 | cqrs-read-model-sync | 原输入,`01-review.md` | `04-read-model-sync.md` | 条件执行 |

## 2. 条件执行

- 缺字段来源或发现 Domain 污染：补 `cqrs-domain-read-decoupling`。
- 缺视图契约：补 `cqrs-aggregation-view-design`。
- 缺刷新策略：补 `cqrs-read-model-sync`。

## 3. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 审查 | `01-review.md` 后 | 所有 high/critical 都有最小修正路径；过度设计风险被明确标注 |
