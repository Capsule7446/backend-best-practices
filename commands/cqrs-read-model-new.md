---
description: 启动 CQRS 读模型新建设计流程。薄入口：仅启动 workflow-read-model-greenfield。
argument-hint: <业务聚合展示/报表/查询 API 需求>
---

> Workflow 文件通过同名 `workflow-*` Skill 注册后调用。

# /backend-best-practices:cqrs-read-model-new

薄入口。相关 Workflow 已作为同名 Skill 注册，把 `$ARGUMENTS` 交给 **`workflow-read-model-greenfield`**。

- `$ARGUMENTS`：业务聚合展示、dashboard、报表、列表、搜索、详情页或查询 API 需求。

动作：启动 workflow；命令本身不判断是否需要 CQRS。
