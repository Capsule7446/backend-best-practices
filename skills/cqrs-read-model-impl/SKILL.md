---
name: cqrs-read-model-impl
description: "把读模型设计落成可运行实现：Query Handler、View DTO、Read Repository、Projection Handler、读存储结构、权限下推与 freshness 元数据。"
risk: caution
category: implementation
inputs: "视图契约（含逐视图适配结论）+ 权限约束（租户/行级/字段级）+ [存在 use 视图时] 读模型设计与同步策略 + 目标语言与读存储"
outputs: "Query Handler / View DTO / Read Repository / Projection Handler / 读存储结构 / Projection Checkpoint / 迁移与重建脚本"
tags: "[cqrs, read-model, query-handler, projection, authorization, freshness]"
---

# Read Model Impl（读侧实现）

## 做什么

把读侧设计落成实现，**按逐视图结论分路**：`avoid` 视图落 Query Handler / Query Service / View DTO 简单查询路径；`use` 视图另落事件投影与独立读存储。权限下推与新鲜度元数据是实现的一等约束，不是事后补丁。不得把 `avoid` 视图擅自升级成独立读模型。

## 需要什么参数

- **必需**：视图契约（字段/筛选/排序/权限，含逐视图适配结论）；权限约束（租户/行级/字段级）。
- **必需（仅当存在 `use` 视图）**：读模型设计（模型类型、字段映射、查询契约、索引）；同步/刷新策略。
- **可选**：目标语言与框架、读存储基础设施（DB/缓存/搜索）、事件流格式与序号语义、性能预算、重建窗口。

## 怎么做

1. **实现 View DTO**：按查询契约定义字段与类型；不复用写侧 Entity，不向调用方暴露 Domain 对象。
2. **附 freshness 元数据**：DTO 或响应信封携带 `as_of` / `generated_at` / `projection_version` / `stale` 标记，让读侧延迟对调用方可见。
3. **实现 Query Handler / Query Service**：一个查询契约一个入口；校验筛选/排序/分页参数（排序字段白名单、分页上限），组装 DTO 返回。
4. **实现 Read Repository / Reader**：封装读存储访问，只读；查询由契约驱动，不拼接自由 SQL。
5. **权限下推**：租户/行级/字段级约束必须进入 SQL / 搜索查询 / 缓存查询计划——
   - SQL：租户与行级条件进 WHERE；字段级用列裁剪或投影视图。
   - 搜索：约束作为 filter query 与查询同发，不在结果集上二次筛。
   - 缓存：缓存键包含租户/权限维度，禁止跨租户共享条目。
   - **禁止先查全量再内存过滤**：总数、分页游标、排序位次、聚合值、缓存键都会泄漏被过滤数据。
6. **实现读存储结构**：按设计落 DB View / Materialized View / Read Table / Cache / Search Document；索引覆盖查询契约的筛选与排序键，分页用稳定排序（唯一性尾键）。
7. **实现 Projection Handler**：消费事件更新读存储；幂等——重复事件不重复生效，乱序事件按版本/序号判断后应用或跳过。
8. **实现 Projection Checkpoint**：记录已消费位置（offset / sequence / 时间戳）；崩溃恢复从 checkpoint 续跑，支持归零全量重放。
9. **写迁移与重建脚本**：读存储结构初始化；全量重建可从真源或事件流重放；重建期间的双写/切换策略明确。

## 约束

- 读侧实现不得 import 写侧 Domain Entity / Aggregate；可共享的只有事件契约与标识类型。
- Projection Handler 不回写真源、不发领域命令；投影失败走重试/告警，不静默吞错。
- 缓存与搜索文档同样承载权限语义：键与文档内容都不得混入未授权字段。

## 返回什么

| 工件 | 结构 |
| :--- | :--- |
| View DTO | 查询契约字段 + freshness 元数据（as_of / generated_at / projection_version / stale） |
| Query Handler / Query Service | 每查询契约一入口；参数校验 + 权限上下文传入 |
| Read Repository / Reader | 只读访问封装；权限条件下推到存储查询计划 |
| Projection Handler | 事件 → 读存储更新；幂等 + 乱序安全 |
| 读存储结构 | DDL / 视图定义 / 缓存键设计 / 搜索 mapping + 索引与排序键 |
| Projection Checkpoint | 消费位置存储 + 恢复与重放逻辑 |
| 迁移与重建脚本 | 结构初始化 + 全量重建 + 切换策略 |

> **返回格式自检**：所有权限约束（租户/行级/字段级）已下推进存储查询计划，无"先查全量再内存过滤"路径；查询出口只返回 View DTO，无 Domain Entity 直出；Projection Handler 幂等，重复/乱序事件下读模型收敛到同一终态；Checkpoint 可定位任意重放起点，重建脚本可从真源/事件流完整重建。

---

附加文件（按需读取）：`examples.md` — 走查示例。
