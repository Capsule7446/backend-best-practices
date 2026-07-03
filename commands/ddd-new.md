---
description: 启动 0→1 新建全链路（greenfield）。薄入口：仅启动 workflow-greenfield，不含编排逻辑。
argument-hint: <业务/问题描述> [--lang=java|go|ts|python|csharp|rust|kotlin]
---

# /backend-best-practices:ddd-new

薄入口。把参数交给 **`workflow-greenfield`** 启动，其余全由该 workflow 统筹（路由、文件交接、门禁、回溯）。

- `$ARGUMENTS`：业务/问题描述（必需）。
- `--lang`：目标落地语言（可选，缺省延后到 G3 前确认）。

动作：启动 `workflow-greenfield`，传入 `$ARGUMENTS` 与 `--lang`。命令本身不做建模判断。
