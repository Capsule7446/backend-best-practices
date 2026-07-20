---
name: design-pattern
description: 启动设计模式选择、实现与审查流程。薄入口：仅启动 workflow-design-pattern。
risk: caution
source: self
---

## 做什么

执行 `design-pattern` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<设计问题或代码路径> [--lang=<语言>]

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# design-pattern

薄入口。把 `$ARGUMENTS` 交给 **`workflow-design-pattern`**。

- `$ARGUMENTS`：设计问题、代码路径、目标重构点、目标语言，或明确的 GoF 模式名。

若用户已经点名某个模式，workflow 直接路由到对应 `design-pattern-<pattern>`；否则先由 `design-pattern-fit-check` 选择。

动作：启动 workflow；命令本身不选择模式、不生成实现。
