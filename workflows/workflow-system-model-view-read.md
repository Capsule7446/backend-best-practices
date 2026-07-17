# Workflow：System Model + View Reading

> 统筹者。用于深度阅读既有系统代码，把代码解释成清楚的业务模型、领域边界、聚合行为和业务视图/读模型。由 `/backend-best-practices:system-model-view-read` 触发。

## 0. 入口

1. 采集代码路径、关注模块、已知业务目标、需要解释的页面/API/报表。
2. 建运行工作区 `<workdir>/`（默认 `./run/system-read/`），写入 `_manifest.md`。
3. 全程只产出解释与模型，不默认改代码。

## 1. 文件交接

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 00 | （路由，本层）| 代码路径 + 关注点 | `00-routing.md` | |
| 01 | ddd-code-survey | `00-routing.md` + 代码库 | `01-code-survey.md` | G0 |
| 02 | ddd-discover | `01-code-survey.md` | `02-business-events.md` | |
| 03 | ddd-subdomains | `01-code-survey.md`,`02-business-events.md` | `03-subdomains.md` | |
| 04 | ddd-contexts | `02-business-events.md`,`03-subdomains.md` | `04-contexts.md` | |
| 05 | ddd-context-map | `04-contexts.md`,`01-code-survey.md` | `05-context-map.md` | G1 |
| 06 | ddd-aggregates | `04-contexts.md`,`05-context-map.md`,`02-business-events.md` | `06-aggregates.md` | |
| 07 | ddd-domain-interactions | `06-aggregates.md`,`05-context-map.md` | `07-domain-interactions.md` | |
| 08 | ddd-model-review | `03..07-*.md` | `08-ddd-review.md` | G2 |
| 09 | cqrs-domain-read-decoupling | `01-code-survey.md`,`04-contexts.md`,`06-aggregates.md` | `09-domain-read-decoupling.md` | |
| 10 | cqrs-aggregation-view-design | `01-code-survey.md`,`09-domain-read-decoupling.md` | `10-business-views.md` | |
| 11 | cqrs-fit-check | `10-business-views.md`,`09-domain-read-decoupling.md` | `11-read-fit.md` | |
| 12 | cqrs-read-model-design | `10-business-views.md`,`09-domain-read-decoupling.md` | `12-read-models.md` | |
| 13 | cqrs-read-model-sync | `12-read-models.md`,`01-code-survey.md` | `13-read-model-sync.md` | |
| 14 | cqrs-review | `09..13-*.md` | `14-cqrs-review.md` | G3 |
| 15 | （综合解读，本层）| `01..14-*.md` | `15-system-reading-report.md` | G4 |

## 2. 最终报告结构

`15-system-reading-report.md` 必须包含：

- 系统一句话业务定位。
- 代码入口地图：API/Controller/Job/Consumer 到业务用例的映射。
- 领域模型图谱：子域、上下文、聚合、不变量、领域交互。
- 业务视图图谱：页面/API/报表、字段来源、查询模型、刷新策略。
- 写侧与读侧边界：哪些是 Domain 真源，哪些是 Read Model / View Model。
- 关键代码解读：按业务能力解释核心文件，而不是按目录流水账。
- 风险与坏味道：Domain 污染、Entity-backed API、读模型缺来源、刷新不清楚。
- 后续建议：只给最小修正路径，不默认重构。

## 3. 门禁

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 代码盘点 | `01-code-survey.md` 后 | 关键入口、核心数据结构、行为黑盒、坏味道已列清 |
| G1 边界 | `05-context-map.md` 后 | 上下文边界和跨界关系能解释主要代码路径 |
| G2 模型 | `08-ddd-review.md` 后 | 聚合、不变量、领域交互能解释主要写侧行为 |
| G3 视图 | `14-cqrs-review.md` 后 | 业务视图字段有来源，读模型和刷新策略清楚 |
| G4 解读 | `15-system-reading-report.md` 后 | 能从业务概念反查代码，也能从代码入口反查业务含义 |

## 4. 回溯

| 触发条件 | 重跑 |
| :-- | :-- |
| 找不到入口或行为链路 | ddd-code-survey |
| 事件流无法解释代码行为 | ddd-discover / ddd-code-survey |
| 上下文边界解释不了模块关系 | ddd-contexts / ddd-context-map |
| 聚合只是数据表映射 | ddd-aggregates |
| 页面/API 字段没有来源 | cqrs-domain-read-decoupling / cqrs-aggregation-view-design |
| Read Model 刷新方式缺失 | cqrs-read-model-sync |
| 最终报告变成目录说明 | 回到综合解读，改为业务能力导向 |

## 5. 编排纪律

- 读码模式下 `11-read-fit.md` 的逐视图矩阵是**对现状读侧设计的适配评估**（哪些视图过度设计、哪些不足），不用于中断流程；12-15 照常执行（解释现状，系统无独立读结构时如实说明），评估结论并入 `15` 报告的风险与建议。
- 不把代码目录结构当业务模型。
- 不把 ORM Entity 直接等同于 Aggregate。
- 不把 API Response 直接等同于 Read Model。
- 先解释现状，再给建议；没有明确要求不改代码。
- 输出必须支持双向追踪：业务概念 → 代码位置，代码入口 → 业务含义。
