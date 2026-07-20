---
name: workflow-read-model-review
description: 执行 workflow-read-model-review 编排流程，负责阶段顺序、输入输出交接、门禁和回溯。
risk: caution
source: self
---

## 做什么

执行 `workflow-read-model-review` 的完整编排流程。

## 需要什么参数

- **必需**：项目路径、目标和当前上下文。
- **可选**：技术栈、约束、工单号和已有运行工件。

## 怎么做

按下方流程执行阶段、门禁和回溯。

## 返回什么

返回阶段工件、门禁结果、未解决风险和下一步建议。

# Workflow：CQRS Read Model Review

> 统筹者。用于审查现有 CQRS Read Model 设计或代码。由 `/backend-best-practices:workflow-read-model-review` 触发。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | cqrs-review | 设计文档/代码路径 | `01-review.md` | G0 |
| 02 | cqrs-domain-read-decoupling | 原输入,`01-review.md` | `02-domain-read-decoupling.md` | 条件执行 |
| 03 | cqrs-aggregation-view-design | 原输入,`01-review.md` | `03-aggregation-view.md` | 条件执行 |
| 04 | cqrs-read-model-sync | 原输入,`01-review.md` | `04-read-model-sync.md` | 条件执行 |
| 05 | cqrs-review | 原输入,`01-review.md`,`02?,03?,04?-*.md` | `05-recheck.md` | G1，条件执行 |

## 2. 条件执行

- 缺字段来源或发现 Domain 污染：补 `cqrs-domain-read-decoupling`。
- 缺视图契约：补 `cqrs-aggregation-view-design`。
- 缺刷新策略：补 `cqrs-read-model-sync`。
- 触发过任一补析（02/03/04）：**必须**执行 05 复审；一项补析都没触发时跳过 05，以 G0 结果结案。

## 3. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 审查 | `01-review.md` 后 | 所有 high/critical 都有最小修正路径；过度设计风险被明确标注 |
| G1 复审 | `05-recheck.md` 后 | 补析针对的 high/critical 已闭环且未引入新的 high/critical；复审仍有 high/critical 时回到对应补析步骤（最多再一轮，仍不过则停下交用户决策）|
