---
name: ddd-new
description: 启动 0→1 新建全链路（greenfield）。薄入口：仅启动 workflow-greenfield，不含编排逻辑。
risk: caution
source: self
---

## 做什么

执行 `ddd-new` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<业务/问题描述> [--lang=java|go|ts|python|csharp|rust|kotlin]

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# ddd-new

薄入口。把参数交给 **`workflow-greenfield`** 启动，其余全由该 workflow 统筹（路由、文件交接、门禁、回溯）。

- `$ARGUMENTS`：业务/问题描述（必需）。
- `--lang`：目标落地语言（可选，缺省延后到 G3 前确认）。

动作：启动 `workflow-greenfield`，传入 `$ARGUMENTS` 与 `--lang`。命令本身不做建模判断。
