---
name: cqrs-read-model-design
description: "把聚合视图转成具体查询优化模型：DTO、DB View、Materialized View、Read Table、Cache 或 Search Document。"
risk: safe
category: implementation
inputs: "聚合视图 / 真源 / 查询模式 / 性能目标 / 存储约束"
outputs: "读模型类型 / 字段映射 / 索引 / 查询契约 / 所有权"
tags: "[cqrs, read-model, dto, db-view, materialized-view, cache, search]"
---

# Read Model Design（读模型设计）

## 做什么

将聚合视图需求落成独立于写侧 Domain 的查询模型，并保持字段来源、查询契约和所有权清楚。

## 需要什么参数

- **必需**：聚合视图契约、字段真源、查询模式、性能目标。
- **可选**：存储限制、现有数据库能力、缓存/搜索基础设施、分页约束。

## 怎么做

1. 选择模型类型：DTO、DB View、Materialized View、Read Table、Cache、Search Document。
2. 定义字段、类型、来源、转换规则。
3. 定义筛选、排序、分页、索引和查询契约。
4. 说明冗余是否允许，以及冗余字段如何追溯。
5. 明确 source of truth 与 read model owner。

## 返回什么

```yaml
read_model_name:
model_type: dto | db_view | materialized_view | read_table | cache | search_document
fields:
  - name:
    type:
    source:
    transform:
indexes:
  - fields:
    reason:
query_contracts:
  - name:
    filters:
    sorts:
    pagination:
ownership:
  source_of_truth:
  read_model_owner:
```

> **返回格式自检**：Read Model 不拥有业务真源；冗余字段有来源；查询 API 不直接暴露 Domain Entity。

---

附加参考（按需读取）：`references/read-model-patterns.md`。
