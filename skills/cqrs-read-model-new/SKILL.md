---
name: cqrs-read-model-new
description: 启动 CQRS 读模型新建设计流程。薄入口：仅启动 workflow-read-model-greenfield。
risk: caution
source: self
---

## 做什么

执行 `cqrs-read-model-new` 的任务入口，处理参数并完成该能力定义的工作。

## 需要什么参数

- **必需**：<业务聚合展示/报表/查询 API 需求>

## 怎么做

1. 读取输入并确认目标范围。
2. 按本 Skill 正文定义的步骤执行。
3. 对关键结论和修改进行验证。

## 返回什么

返回执行结果、产物路径、验证结果、未解决风险和下一步建议。

# cqrs-read-model-new

薄入口。把 `$ARGUMENTS` 交给 **`workflow-read-model-greenfield`**。

- `$ARGUMENTS`：业务聚合展示、dashboard、报表、列表、搜索、详情页或查询 API 需求。

动作：启动 workflow；命令本身不判断是否需要 CQRS。
