---
description: 深度阅读既有系统，调度 DDD + CQRS Read Model workflow，输出业务模型、业务视图和代码解读报告。
argument-hint: <代码路径> [--focus=<模块/API/页面/报表>]
---


# /backend-best-practices:system-model-view-read

薄入口。把 `$ARGUMENTS` 交给 **`workflow-system-model-view-read`**。

- `$ARGUMENTS`：代码路径或系统现状描述。
- `--focus`：可选，限定关注模块、API、页面、报表或业务流程。

动作：启动综合 workflow；命令本身不做建模、不读代码、不改代码。
