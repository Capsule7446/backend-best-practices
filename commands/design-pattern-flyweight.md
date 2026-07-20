---
description: 使用 GoF Flyweight（享元）模式处理设计问题。薄入口：仅启动 workflow-design-pattern 并指定 flyweight。
argument-hint: <设计问题或代码路径> [--lang=<语言>]
---

> Workflow 文件通过同名 `workflow-*` Skill 注册后调用。

# /backend-best-practices:design-pattern-flyweight

薄入口。相关 Workflow 已作为同名 Skill 注册，把 $ARGUMENTS 交给 **workflow-design-pattern**，并固定候选能力为 design-pattern-flyweight。

动作：启动 workflow；命令本身不实现模式、不选择语言细节。
