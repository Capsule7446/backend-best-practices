---
name: cqrs-fit-check
description: "判断需求是否真的需要 CQRS 式读模型分离，并给出最小可行读侧方案，避免事件溯源、微服务、双库等过度设计。"
risk: safe
category: discovery
inputs: "业务目标 / 当前领域模型 / 目标视图 / 查询场景 / 痛点 / 约束 / 团队能力"
outputs: "CQRS 适配决策 / 驱动因素 / 风险 / 最小方案 / 不推荐模式"
tags: "[cqrs, read-model, fit-check, over-engineering]"
---

# CQRS Fit Check（适配判断）

## 做什么

判断一个需求是否需要 CQRS 式 Read Model 解耦。重点不是"读写比例大"，而是识别展示查询是否正在污染 Domain，或查询形状是否明显不同于写模型。

## 需要什么参数

- **必需**：业务目标、目标视图/报表/API、查询场景、当前领域模型或数据模型。
- **可选**：痛点、性能目标、团队能力、基础设施约束、现有实现路径。

## 怎么做

1. 识别视图是否跨聚合、跨模块或跨 bounded context。
2. 检查 Domain 是否因页面字段、排序、报表统计、格式化字段而变形。
3. 检查查询是否需要复杂 join、聚合、搜索、缓存或统计。
4. 优先评估 DTO、Query Service、Repository Query、DB View 是否足够。
5. 判断是否需要独立 Read Model，并选择最小可行方案。
6. 明确不推荐的重型方案及理由。

## 返回什么

```yaml
decision: use | partial | avoid
score: 0-100
drivers:
  - reason
risks:
  - risk
minimal_approach: dto | query-service | db-view | materialized-view | read-table | cache | search-index
not_recommended:
  - pattern
required_capabilities:
  - capability
```

> **返回格式自检**：`decision=use` 至少有 3 个真实驱动；`decision=avoid` 必须给替代方案；不得仅因"架构整洁"建议 CQRS。

---

附加参考（按需读取）：`references/read-model-patterns.md`、`references/anti-patterns.md`。
