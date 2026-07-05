---
name: cqrs-domain-read-decoupling
description: "识别 Domain Model 与展示/查询需求之间的耦合，划清写侧模型与读侧模型职责边界。"
risk: safe
category: tactical
inputs: "领域实体 / 聚合 / 用例 / UI 视图 / 查询 API / 当前痛点"
outputs: "领域职责 / 读侧职责 / 污染迹象 / 解耦动作 / 字段真源规则"
tags: "[cqrs, domain-model, read-model, decoupling]"
---

# Domain Read Decoupling（读写职责解耦）

## 做什么

找出展示、查询、报表、排序、格式化需求是否进入了 Domain Entity、Aggregate、Repository 或业务不变量，并给出解耦边界。

## 需要什么参数

- **必需**：领域实体/聚合、核心用例、UI 视图或查询 API、当前痛点。
- **可选**：已有 DTO、Repository 查询、报表字段、性能或权限约束。

## 怎么做

1. 标记 Domain 真正负责的行为和不变量。
2. 标记只服务展示、筛选、排序、统计、格式化的字段。
3. 识别污染迹象：展示字段进入 Aggregate、Entity-backed API、Repository 被页面形状驱动。
4. 定义写侧模型与读侧模型的职责边界。
5. 为读模型字段标注 source of truth，说明是否允许冗余、反范式化或缓存。

## 返回什么

```yaml
domain_responsibilities:
  - item
read_responsibilities:
  - item
pollution_found:
  - symptom
decoupling_actions:
  - action
source_of_truth:
  entity_or_field: source
rules:
  - read model must not enforce write invariants
  - read model must not become source of truth
```

> **返回格式自检**：每个读侧字段可追溯来源；没有让 Read Model 反向写 Domain；没有建议为页面方便把展示字段塞进 Aggregate。

---

附加参考（按需读取）：`references/domain-decoupling.md`、`references/anti-patterns.md`。
