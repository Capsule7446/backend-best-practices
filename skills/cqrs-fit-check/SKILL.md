---
name: cqrs-fit-check
description: "判断需求是否真的需要 CQRS 式读模型分离，并给出最小可行读侧方案，避免事件溯源、微服务、双库等过度设计。"
risk: safe
category: discovery
inputs: "业务目标 / 当前领域模型 / 目标视图清单（视图契约或视图需求）/ 查询场景 / 痛点 / 约束 / 团队能力"
outputs: "逐视图适配矩阵（每视图 decision/驱动/最小方案）/ 总体决策 / 风险 / 不推荐模式"
tags: "[cqrs, read-model, fit-check, over-engineering]"
---

# CQRS Fit Check（适配判断）

## 做什么

**逐视图**判断是否需要 CQRS 式 Read Model 解耦。重点不是"读写比例大"，而是识别展示查询是否正在污染 Domain，或查询形状是否明显不同于写模型。一个系统里"报表用读模型、详情页用简单查询"是常态——决策粒度是视图，不是系统。

## 需要什么参数

- **必需**：目标视图清单（视图契约，或至少每视图的字段/筛选/新鲜度需求）、业务目标、当前领域模型或数据模型。
- **可选**：痛点、性能目标、团队能力、基础设施约束、现有实现路径。

## 怎么做

1. 逐视图识别是否跨聚合、跨模块或跨 bounded context。
2. 检查 Domain 是否因页面字段、排序、报表统计、格式化字段而变形。
3. 逐视图检查查询是否需要复杂 join、聚合、搜索、缓存或统计。
4. 每个视图优先评估 DTO、Query Service、Repository Query、DB View 是否足够。
5. 仅对确有驱动的视图选择独立 Read Model 与最小可行方案。
6. 明确不推荐的重型方案及理由。
7. 汇总总体决策：全部 `avoid` → `avoid`；全部 `use` → `use`；混合 → `partial`。

## 返回什么

```yaml
decision: use | partial | avoid        # 总体（由逐视图结论聚合而来）
score: 0-100
views:
  - view_id:
    decision: use | avoid
    drivers:
      - reason
    minimal_approach: dto | query-service | db-view | materialized-view | read-table | cache | search-index
    not_recommended:
      - pattern
risks:
  - risk
required_capabilities:
  - capability
```

> **返回格式自检**：每个输入视图在 `views` 中有且仅有一条结论；视图级 `decision=use` 至少有 3 个真实驱动；`decision=avoid` 的视图必须给 `minimal_approach` 替代方案；总体 `decision` 与逐视图结论一致（混合必为 `partial`）；不得仅因"架构整洁"建议 CQRS。

---

附加参考（按需读取）：`references/read-model-patterns.md`、`references/anti-patterns.md`。
