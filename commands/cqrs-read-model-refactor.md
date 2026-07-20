---
description: 启动既有系统读模型解耦流程。薄入口：仅启动 workflow-read-model-brownfield。
argument-hint: <代码路径或现状描述>
---


# /backend-best-practices:cqrs-read-model-refactor

薄入口。把 `$ARGUMENTS` 交给 **`workflow-read-model-brownfield`**。

- `$ARGUMENTS`：代码路径、现状描述、Domain 污染或 Entity-backed API 问题。

动作：启动 workflow；命令本身不做迁移规划。
