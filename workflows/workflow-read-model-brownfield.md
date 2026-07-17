# Workflow：CQRS Read Model Brownfield

> 统筹者。用于从既有 Entity-backed API、Domain 污染或复杂查询中拆出 Read Model。由 `/backend-best-practices:cqrs-read-model-refactor` 触发。

## 0. 入口

1. 采集代码路径、当前查询/API/UI 痛点、可回滚约束。
2. 建运行工作区 `<workdir>/`（默认 `./run/read-model/`），写入 `_manifest.md`。
3. 先识别耦合和适配度，再设计目标读模型；`decision=avoid` 时仍完成 03 与 06，产出查询侧契约，不得以 `avoid` 为由维持 Entity 直出 API 的现状。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 01 | cqrs-domain-read-decoupling | 现状描述/代码路径 | `01-domain-read-decoupling.md` | |
| 02 | cqrs-fit-check | `01-domain-read-decoupling.md` | `02-fit-check.md` | G0 |
| 03 | cqrs-aggregation-view-design | `01..02-*.md` | `03-aggregation-view.md` | |
| 04 | cqrs-read-model-design | `03-aggregation-view.md`,`01-domain-read-decoupling.md` | `04-read-model-design.md` | 条件执行（`partial/use`）|
| 05 | cqrs-read-model-sync | `04-read-model-design.md` | `05-read-model-sync.md` | 条件执行（`partial/use`）|
| 06 | cqrs-review | `01..05-*.md`（`avoid` 路径为 `01..03-*.md`）| `06-review.md` | G1 |

## 2. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 适配 | `02-fit-check.md` 后 | `decision` 字段存在；简单 DTO/Query Service 足够时不升级（`avoid`，跳过 04-05，03 与 06 仍执行）；需要 Read Model 时有明确驱动 |
| G1 审查 | `06-review.md` 后 | 迁移路径可分步；旧行为可验证；字段来源和刷新策略齐全 |

## 3. 推荐迁移路径

1. 识别被污染的查询/API/页面。
2. 提取 Query DTO。
3. 建立 Query Service。
4. 必要时增加 View / Read Table / Cache。
5. 双跑新旧查询并做 parity diff。
6. 切换调用方。
7. 删除 Domain 中展示字段。
