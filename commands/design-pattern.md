---
description: 启动设计模式选择、实现与审查流程。薄入口：仅启动 workflow-design-pattern。
argument-hint: <设计问题或代码路径> [--lang=<语言>]
---

# /backend-best-practices:design-pattern

薄入口。把 `$ARGUMENTS` 交给 **`workflow-design-pattern`**。

- `$ARGUMENTS`：设计问题、代码路径、目标重构点、目标语言，或明确的 GoF 模式名。

若用户已经点名某个模式，workflow 直接路由到对应 `design-pattern-<pattern>`；否则先由 `design-pattern-fit-check` 选择。

动作：启动 workflow；命令本身不选择模式、不生成实现。
