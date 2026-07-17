# Workflow：CQRS Read Model Brownfield

> 统筹者。用于从既有 Entity-backed API、Domain 污染或复杂查询中拆出 Read Model。由 `/backend-best-practices:cqrs-read-model-refactor` 触发。
> 第一纪律：旧查询路径全程可用、可回滚；新读侧灰度接管。

## 0. 入口

1. 采集代码路径、当前查询/API/UI 痛点、可回滚约束。
2. 建运行工作区 `<workdir>/`（默认 `./run/read-model/`），写入 `_manifest.md`。
3. 先识别耦合，再按目标视图逐个判定读侧方案；`avoid` 视图也必须产出查询侧契约，不得以 `avoid` 为由维持 Entity 直出 API 的现状。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | cqrs-domain-read-decoupling | 现状描述/代码路径 | `01-domain-read-decoupling.md` | |
| 02 | cqrs-aggregation-view-design | `01-domain-read-decoupling.md` + 现状查询/页面 | `02-views.md` | |
| 03 | cqrs-fit-check | `02-views.md`,`01-domain-read-decoupling.md` | `03-fit-check.md` | G0 |
| 04 | cqrs-read-model-design | `01..03-*.md` | `04-read-model-design.md` | 条件执行（`views` 中存在 `use`）|
| 05 | cqrs-read-model-sync | `04-read-model-design.md` | `05-read-model-sync.md` | 条件执行（同上）|
| 06 | cqrs-review | `01,02,03,04?,05?-*.md` | `06-review.md` | G1 |
| 07 | cqrs-read-model-impl | `02-views.md`,`03-fit-check.md`,`04?,05?-*.md` | `07-read-impl.md` | 条件执行（进入落地阶段）|
| 08 | （迁移执行，本层）| `07-read-impl.md` + 旧查询路径 | `08-migration-log.md` | G2 |
| 09 | cqrs-read-model-acceptance | `04?,05?-*.md`,`07-read-impl.md`,`08-migration-log.md` | `09-read-acceptance.md` | G3 |

07 按逐视图结论分路实现：`avoid` 视图 → 从 Entity 直出提取 Query Service / View DTO；`use` 视图 → 投影与独立读存储。全 `avoid` 时 04/05 缺席不阻塞 07；09 的验收项按适用性裁剪（无 `use` 视图时投影收敛/重建等价记 N/A 并给理由）。

## 2. 迁移执行（步骤 08，本层持有）

每个切换的视图按以下顺序推进，全程记录在 `08-migration-log.md`：

1. **Backfill**：从真源全量回填读存储，记录回填水位与校验和。
2. **Shadow Read**：新读侧只读不服务，与旧查询并行运行。
3. **Parity Diff**：对同一请求比对新旧结果（抽样 + 关键用例全量），差异归零或差异原因全部解释（如格式化口径）前不切换。
4. **Cutover**：按视图灰度切换调用方；保留旧路径开关。
5. **Rollback 预案**：切换后出现差异/延迟超标时一键回旧路径；读存储可从真源重建。
6. **退役**：稳定期后删除旧查询路径与 Domain 中的展示字段，登记退役日期。

## 3. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 适配 | `03-fit-check.md` 后 | 每个视图在 `views` 矩阵有结论；简单 DTO/Query Service 足够时不升级（`avoid`）；`use` 视图有明确驱动 |
| G1 审查 | `06-review.md` 后 | 迁移路径可分步；旧行为可验证；字段来源和刷新策略齐全；`avoid` 视图有查询方案与权限 |
| G2 迁移 | `08-migration-log.md` 每视图切换前 | Backfill 水位可核对；Parity Diff 差异归零或全部有解释；回滚开关已演练 |
| G3 读侧验收 | `09-read-acceptance.md` 后 | 权限隔离、投影收敛、重建等价、read-your-writes、性能预算全部有测试证据且通过 |

## 4. 回溯

| 触发条件 | 重跑 |
| :-- | :-- |
| 视图缺字段来源或权限 | cqrs-aggregation-view-design |
| Domain 污染定位不清 | cqrs-domain-read-decoupling |
| fit 结论与查询复杂度不符 | cqrs-fit-check |
| 刷新/重建策略缺失 | cqrs-read-model-sync |
| Parity Diff 差异无法解释 | cqrs-read-model-impl / cqrs-domain-read-decoupling |
| 验收缺证据 | cqrs-read-model-acceptance |

## 5. 编排纪律

- 决策粒度是视图；一次只迁移一个视图，稳定后取下一个。
- 没有 Parity Diff 归零不切流；没有回滚开关不切流。
- 权限必须下推进查询计划，禁止查全量后内存过滤。
- 临时双写/双读是过渡态，必须有退役计划。
