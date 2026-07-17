# Workflow：CQRS Read Model Greenfield

> 统筹者。用于新建业务聚合展示、dashboard、报表、列表、搜索或查询 API。由 `/backend-best-practices:cqrs-read-model-new` 触发。
> 顺序纪律：**视图先行**——先明确业务视图与字段需求，再逐视图判断是否需要独立读模型。

## 0. 入口

1. 采集业务目标、目标视图、字段、筛选排序、性能和新鲜度预期。
2. 建运行工作区 `<workdir>/`（默认 `./run/read-model/`），写入 `_manifest.md`。
3. 是否落地实现由用户声明（仅设计 / 设计+实现），登记进 `_manifest.md`。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | cqrs-aggregation-view-design | 用户诉求 | `01-views.md` | |
| 02 | cqrs-fit-check | `01-views.md` | `02-fit-check.md` | G0 |
| 03 | cqrs-domain-read-decoupling | 用户诉求,`01-views.md` | `03-domain-read-decoupling.md` | |
| 04 | cqrs-read-model-design | `01..03-*.md` | `04-read-model-design.md` | 条件执行（`views` 中存在 `use`）|
| 05 | cqrs-read-model-sync | `04-read-model-design.md` | `05-read-model-sync.md` | 条件执行（同上）|
| 06 | cqrs-review | `01..05-*.md` | `06-review.md` | G1 |
| 07 | cqrs-read-model-impl | `01-views.md`,`04..05-*.md` | `07-read-impl.md` | 条件执行（用户要求落地实现）|
| 08 | cqrs-read-model-acceptance | `04..05-*.md`,`07-read-impl.md` | `08-read-acceptance.md` | 条件执行（有 07），G2 |

`02` 输出**逐视图矩阵**：`decision=avoid` 的视图走简单查询方案（DTO / Query Service / DB View），其视图契约与权限已在 `01-views.md`；仅 `decision=use` 的视图进入 04/05 与 07 的投影部分。全部视图 `avoid` 时跳过 04/05，06 审查简化读侧方案。

## 2. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 适配 | `02-fit-check.md` 后 | 每个输入视图在 `views` 矩阵有且仅有一条结论；视图级 `use` 有真实驱动；`avoid` 视图有 `minimal_approach`；总体 `decision` 与逐视图结论一致 |
| G1 审查 | `06-review.md` 后 | 无 critical/high；每个字段有来源；每个 `use` 视图有刷新与重建策略；`avoid` 视图有查询方案与权限、无 Entity 直出；没有默认事件溯源/微服务/双库 |
| G2 读侧验收 | `08-read-acceptance.md` 后 | 权限隔离（含越权负例）、投影收敛（重复/乱序/重放）、重建等价、read-your-writes、性能预算全部有测试证据且通过 |

## 3. 回溯

| 触发条件 | 重跑 |
| :-- | :-- |
| 视图缺字段来源或权限 | cqrs-aggregation-view-design |
| 需求只是简单 CRUD 却判了 `use` | cqrs-fit-check |
| Domain 被展示字段污染 | cqrs-domain-read-decoupling |
| 查询 API 暴露 Domain Entity | cqrs-domain-read-decoupling / cqrs-read-model-design |
| 刷新策略不清楚 | cqrs-read-model-sync |
| 方案过重 | cqrs-fit-check / cqrs-read-model-sync |
| 投影不幂等 / 权限未下推 | cqrs-read-model-impl |
| 验收缺证据 | cqrs-read-model-acceptance |

## 4. 编排纪律

- CQRS 是读写模型分离，不等于双库。
- 决策粒度是**视图**，不是系统：同一系统"报表用读模型、详情页用简单查询"是常态。
- 小项目优先 DTO、Query Service、DB View。
- `avoid` 只是不建独立 Read Model，不是跳过读侧设计：View DTO、Query Service、权限设计仍必须产出。
- Read Model 不能反向污染 Domain；可以冗余，但必须说明来源和刷新策略。
- 权限必须下推进查询计划，禁止查全量后内存过滤。
