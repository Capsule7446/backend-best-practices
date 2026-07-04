---
description: 启动既有项目改造全链路（brownfield）。薄入口：仅启动 workflow-brownfield，不含编排逻辑。
argument-hint: <代码路径/模块/仓库> [--goal=解耦|拆分|可测试性] [--lang=沿用现有]
---

# /backend-best-practices:ddd-refactor

薄入口。把参数交给 **`workflow-brownfield`** 启动，其余全由该 workflow 统筹（路由、逆向、切片循环、门禁、回溯）。

- `$ARGUMENTS`：要改造的代码路径/模块/仓库（必需）。
- `--goal`：改造目标（解耦/拆分/可测试性）。
- `--lang`：落地语言，缺省沿用现有技术栈。

动作：启动 `workflow-brownfield`，传入以上参数。命令本身不做建模判断。
