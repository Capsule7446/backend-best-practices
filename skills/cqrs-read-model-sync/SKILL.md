---
name: cqrs-read-model-sync
description: "为 Read Model 选择刷新策略，覆盖同步更新、查询时组合、DB View、定时刷新、CDC、队列、Outbox/Inbox 和重建。"
risk: caution
category: implementation
inputs: "读模型 / 真源 / 新鲜度要求 / 写频率 / 读频率 / 运维复杂度 / 现有基础设施"
outputs: "同步策略 / 刷新时机 / 失败处理 / 重建策略 / 风险 / 回退方案"
tags: "[cqrs, read-model, sync, freshness, outbox, materialized-view]"
---

# Read Model Sync（读模型刷新策略）

## 做什么

为读模型选择最小足够的刷新方式。它不默认事件投影，不默认消息队列，也不默认 Outbox/Inbox。

## 需要什么参数

- **必需**：读模型、source of truth、新鲜度要求、写频率、读频率。
- **可选**：现有基础设施、失败处理要求、重建窗口、运维能力。

## 怎么做

1. 从简单策略开始：query-time composition、database view、synchronous application update。
2. 报表优先评估 materialized view refresh 或 scheduled job。
3. 搜索文档优先评估异步刷新和可重建索引。
4. 只有跨服务、可靠投递或已有消息基础设施时，才评估 queue、CDC、Outbox/Inbox。
5. 定义刷新时机、可接受延迟、失败处理、重建策略和回退方案。

## 返回什么

```yaml
sync_strategy:
reason:
refresh_timing: realtime | near_realtime | scheduled | manual | on_query
staleness_tolerance:
failure_handling:
rebuild_strategy:
operational_requirements:
risks:
fallback:
```

> **返回格式自检**：每个 Read Model 有刷新方式；异步策略有失败处理；使用 Outbox/Inbox 必须说明复杂度值得；小型单体项目允许不用 Outbox/Inbox。

---

附加参考（按需读取）：`references/sync-strategies.md`。
