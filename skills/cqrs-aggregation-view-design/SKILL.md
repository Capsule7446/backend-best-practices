---
name: cqrs-aggregation-view-design
description: "按用户任务设计业务聚合展示模型，用于 dashboard、报表、详情页、列表、搜索结果和运营后台。"
risk: safe
category: tactical
inputs: "视图名 / 用户目标 / 屏幕或 API 需求 / 字段 / 筛选排序聚合 / 数据来源 / 新鲜度预期"
outputs: "聚合视图契约 / 字段来源 / 派生规则 / 权限 / 性能需求 / 候选读模型"
tags: "[cqrs, aggregation-view, dashboard, reporting, read-model]"
---

# Aggregation View Design（聚合视图设计）

## 做什么

围绕用户任务设计 View Model / Read Model，而不是围绕数据库表或 Domain 类设计展示结构。

## 需要什么参数

- **必需**：视图名称、用户目标、字段需求、筛选/排序/聚合需求、来源领域。
- **可选**：权限规则、分页/搜索/缓存需求、新鲜度预期、延迟目标。

## 怎么做

1. 按用户任务定义视图目的和主要使用者。
2. 列出字段、筛选、排序、聚合、权限要求。
3. 为每个字段标注来源 Domain、是否派生、是否可空。
4. 判断是否需要冗余字段、预计算统计、索引、分页、搜索或缓存。
5. 输出查询侧 View Contract 与候选 Read Model。

## 返回什么

```yaml
view_name:
purpose:
primary_users:
fields:
  - name:
    type:
    source:
    derived: true | false
    nullable: true | false
    calculation:
filters:
  - field
sorts:
  - field
aggregations:
  - metric
permissions:
  - rule
performance_needs:
  expected_rows:
  latency_target:
  pagination:
candidate_read_models:
  - model
```

> **返回格式自检**：视图围绕用户任务；每个字段有来源；派生字段有计算方式；权限字段明确，不默认继承 Domain 权限。

---

附加参考（按需读取）：`references/aggregation-view-patterns.md`。
