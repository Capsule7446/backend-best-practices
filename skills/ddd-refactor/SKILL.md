---
name: ddd-refactor
description: 启动既有项目改造全链路（brownfield）。薄入口：调用已注册的 `workflow-brownfield` Skill，不在 Command 中复制编排逻辑。
risk: caution
source: self
---

## 做什么

执行 `ddd-refactor` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<代码路径/模块/仓库> [--goal=解耦|拆分|可测试性] [--lang=沿用现有]

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# ddd-refactor

薄入口。调用已注册的 **`workflow-brownfield` Skill**，其余全由该 Skill 统筹（路由、逆向、切片循环、门禁、回溯）。

- `$ARGUMENTS`：要改造的代码路径/模块/仓库（必需）。
- `--goal`：改造目标（解耦/拆分/可测试性）。
- `--lang`：落地语言，缺省沿用现有技术栈。

动作：调用 `workflow-brownfield` Skill，并传入以上参数。命令本身不做建模判断。
