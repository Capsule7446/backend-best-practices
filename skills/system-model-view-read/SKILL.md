---
name: system-model-view-read
description: 深度阅读既有系统，调度 DDD + CQRS Read Model workflow，输出业务模型、业务视图和代码解读报告。
risk: caution
source: self
---

## 做什么

执行 `system-model-view-read` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<代码路径> [--focus=<模块/API/页面/报表>]

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# system-model-view-read

薄入口。把 `$ARGUMENTS` 交给 **`workflow-system-model-view-read`**。

- `$ARGUMENTS`：代码路径或系统现状描述。
- `--focus`：可选，限定关注模块、API、页面、报表或业务流程。

动作：启动综合 workflow；命令本身不做建模、不读代码、不改代码。
