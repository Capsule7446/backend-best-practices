---
name: design-pattern-chain-of-responsibility
description: 使用 GoF Chain of Responsibility（责任链）模式处理设计问题。薄入口：仅启动 workflow-design-pattern 并指定 chain-of-responsibility。
risk: caution
source: self
---

## 做什么

执行 `design-pattern-chain-of-responsibility` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<设计问题或代码路径> [--lang=<语言>]

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# design-pattern-chain-of-responsibility

薄入口。把 $ARGUMENTS 交给 **workflow-design-pattern**，并固定候选能力为 design-pattern-chain-of-responsibility。

动作：启动 workflow；命令本身不实现模式、不选择语言细节。
