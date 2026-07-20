---
name: cqrs-read-model-refactor
description: 启动既有系统读模型解耦流程。薄入口：仅启动 workflow-read-model-brownfield。
risk: caution
source: self
---

## 做什么

执行 `cqrs-read-model-refactor` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<代码路径或现状描述>

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# cqrs-read-model-refactor

薄入口。把 `$ARGUMENTS` 交给 **`workflow-read-model-brownfield`**。

- `$ARGUMENTS`：代码路径、现状描述、Domain 污染或 Entity-backed API 问题。

动作：启动 workflow；命令本身不做迁移规划。
