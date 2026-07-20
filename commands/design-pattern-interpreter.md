---
description: 使用 GoF Interpreter（解释器）模式处理设计问题。薄入口：仅启动 workflow-design-pattern 并指定 interpreter。
argument-hint: <设计问题或代码路径> [--lang=<语言>]
---

# /backend-best-practices:design-pattern-interpreter

薄入口。把 $ARGUMENTS 交给 **workflow-design-pattern**，并固定候选能力为 design-pattern-interpreter。

动作：启动 workflow；命令本身不实现模式、不选择语言细节。
