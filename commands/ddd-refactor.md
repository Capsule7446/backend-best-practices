---
description: 启动既有项目改造全链路（brownfield）。薄入口：调用已注册的 `workflow-brownfield` Skill，不在 Command 中复制编排逻辑。
argument-hint: <代码路径/模块/仓库> [--goal=解耦|拆分|可测试性] [--lang=沿用现有]
---

> Workflow 文件通过同名 `workflow-*` Skill 注册后调用。

# /backend-best-practices:ddd-refactor

薄入口。相关 Workflow 已作为同名 Skill 注册，调用已注册的 **`workflow-brownfield` Skill**，其余全由该 Skill 统筹（路由、逆向、切片循环、门禁、回溯）。

- `$ARGUMENTS`：要改造的代码路径/模块/仓库（必需）。
- `--goal`：改造目标（解耦/拆分/可测试性）。
- `--lang`：落地语言，缺省沿用现有技术栈。

动作：调用 `workflow-brownfield` Skill，并传入以上参数。命令本身不做建模判断。
