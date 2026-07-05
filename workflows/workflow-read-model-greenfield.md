# Workflow：CQRS Read Model Greenfield

> 统筹者。用于新建业务聚合展示、dashboard、报表、列表、搜索或查询 API。由 `/backend-best-practices:cqrs-read-model-new` 触发。

## 0. 入口

1. 采集业务目标、目标视图、字段、筛选排序、性能和新鲜度预期。
2. 建运行工作区 `<workdir>/`（默认 `./run/`），写入 `_manifest.md`。
3. 先判断是否需要 CQRS 式读模型；若 `decision=avoid`，停止完整流程，只输出替代方案。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | cqrs-fit-check | 用户诉求 | `01-fit-check.md` | G0 |
| 02 | cqrs-aggregation-view-design | 用户诉求,`01-fit-check.md` | `02-aggregation-view.md` | |
| 03 | cqrs-domain-read-decoupling | 用户诉求,`02-aggregation-view.md` | `03-domain-read-decoupling.md` | |
| 04 | cqrs-read-model-design | `02-aggregation-view.md`,`03-domain-read-decoupling.md` | `04-read-model-design.md` | |
| 05 | cqrs-read-model-sync | `04-read-model-design.md` | `05-read-model-sync.md` | |
| 06 | cqrs-review | `01..05-*.md` | `06-review.md` | G1 |

## 2. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 适配 | `01-fit-check.md` 后 | `avoid` 时停止 CQRS；`partial/use` 必须有真实驱动和最小方案 |
| G1 审查 | `06-review.md` 后 | 无 critical/high；每个字段有来源；每个 Read Model 有刷新策略；没有默认事件溯源/微服务/双库 |

## 3. 回溯

| 触发条件 | 重跑 |
| :-- | :-- |
| 需求只是简单 CRUD | cqrs-fit-check，输出替代方案 |
| 字段没有来源 | cqrs-aggregation-view-design / cqrs-domain-read-decoupling |
| Domain 被展示字段污染 | cqrs-domain-read-decoupling |
| 查询 API 暴露 Domain Entity | cqrs-read-model-design |
| 刷新策略不清楚 | cqrs-read-model-sync |
| 方案过重 | cqrs-fit-check / cqrs-read-model-sync |

## 4. 编排纪律

- CQRS 是读写模型分离，不等于双库。
- 小项目优先 DTO、Query Service、DB View。
- Read Model 不能反向污染 Domain。
- Read Model 可以冗余，但必须说明来源和刷新策略。
