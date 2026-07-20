---
description: 审查 CQRS 读模型、聚合视图和同步策略。薄入口：仅启动 workflow-read-model-review。
argument-hint: <设计文档/代码路径>
---


# /backend-best-practices:cqrs-read-model-review

薄入口。把 `$ARGUMENTS` 交给 **`workflow-read-model-review`**。

- `$ARGUMENTS`：CQRS 读模型设计、聚合视图文档、查询 API 或代码路径。

动作：启动 review workflow；命令本身不编排修正。
