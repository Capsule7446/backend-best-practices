---
name: cqrs-read-model-review
description: 审查 CQRS 读模型、聚合视图和同步策略。薄入口：仅启动 workflow-read-model-review。
risk: caution
source: self
---

## 做什么

执行 `cqrs-read-model-review` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<设计文档/代码路径>

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# cqrs-read-model-review

薄入口。把 `$ARGUMENTS` 交给 **`workflow-read-model-review`**。

- `$ARGUMENTS`：CQRS 读模型设计、聚合视图文档、查询 API 或代码路径。

动作：启动 review workflow；命令本身不编排修正。
